"""AI 작가실: 바이블 → 비트 → 회차 대본 → 스토리보드.

'개요 먼저, 그다음 집필'(outline-then-write) 구조다. 회차를 쓸 때마다
① 바이블에서 그 회차 인물·관계·규칙만 골라 넣고(RAG) ② 앞 회차 요약과 마지막 장면을 넣어
긴 연재에서 설정이 무너지는 것을 막는다.
"""

from __future__ import annotations

from typing import Optional

from .models import Beat, BeatSheet, Bible, EpisodeScript, Scene, Storyboard

CRAFT = (
    "너는 한국 세로형 숏드라마(회당 60~120초, 9:16) 전문 작가다. 원칙:\n"
    "- 첫 3초 안에 갈등이나 의문을 던진다. 회차 끝은 반드시 다음 화를 보게 만드는 클리프행어.\n"
    "- 지문은 짧게, 카메라로 찍을 수 있는 것만 쓴다. 감정을 설명하지 말고 행동으로 보여준다.\n"
    "- 인물마다 바이블의 말투를 지킨다. 같은 어미·상투구('숨을 삼켰다', '묘한 기분' 등)를 반복하지 않는다.\n"
    "- 바이블에 없는 인물·설정을 만들지 않는다. 사망 인물은 '회상' 장면에서만 등장한다.\n"
    "- 금칙 목록과 세계관 규칙을 어기지 않는다. 모든 텍스트는 한국어."
)


def bible_context(bible: Bible, names: Optional[list[str]] = None) -> str:
    """회차에 필요한 설정만 골라 텍스트로 만든다. names 가 없으면 전체."""
    chars = [c for c in bible.characters if not names or c.name in names]
    if names:  # 관계로 연결된 인물도 함께
        ids = {c.id for c in chars}
        linked = {r.target for r in bible.relations if r.source in ids} | {r.source for r in bible.relations if r.target in ids}
        chars += [c for c in bible.characters if c.id in linked and c not in chars]
    out = [f"제목: {bible.title}", f"로그라인: {bible.logline}", f"장르: {bible.genre} / 톤: {bible.tone or '-'}",
           f"극중 현재: {bible.story_year}년 / 등급 상한: {bible.target_rating}", "", "[인물]"]
    for c in chars:
        age = bible.age_of(c)
        line = f"- {c.name}"
        if age is not None:
            line += f" ({age}세)"
        if c.occupation:
            line += f", {c.occupation}"
        if c.deceased_in_story_year:
            line += f" ※{c.deceased_in_story_year}년 사망 — 회상 장면에서만 등장"
        out.append(line)
        for label, v in [("성향", ", ".join(c.traits)), ("외형", c.appearance), ("말투", c.speech_style),
                         ("前事", c.backstory)]:
            if v:
                out.append(f"    {label}: {v}")
        for k, v in c.attributes.items():
            if k != "publicity_consent":
                out.append(f"    {k}: {v}")
        for e in c.life_events:
            out.append(f"    {e.age}세: {e.description}")
    by_id = {c.id: c.name for c in bible.characters}
    rels = [r for r in bible.relations if r.source in {c.id for c in chars} or r.target in {c.id for c in chars}]
    if rels:
        out.append("[관계]")
        out += [f"- {by_id.get(r.source, r.source)} → {by_id.get(r.target, r.target)}: {r.kind}"
                + (f" ({r.note})" if r.note else "") for r in rels]
    if bible.places:
        out.append("[장소] " + ", ".join(p.name for p in bible.places))
    if bible.rules:
        out.append("[세계관 규칙]")
        out += [f"- {r.text}" for r in bible.rules]
    if bible.ng_list:
        out.append("[금칙] " + ", ".join(bible.ng_list))
    return "\n".join(out)


class WritersRoom:
    def __init__(self, provider):
        self.p = provider

    def generate_bible(self, logline: str, genre: str, title: str, story_year: int) -> Bible:
        prompt = (f"다음 기획으로 숏드라마 캐논 바이블을 만들어라.\n제목: {title}\n로그라인: {logline}\n장르: {genre}\n"
                  f"극중 현재 연도: {story_year}\n주요 인물 3~6명(이름·출생연도·직업·성향·외형·말투·前事·연령별 사건), "
                  f"장소 3곳 이상, 인물 관계, 세계관 규칙, 금칙 목록을 포함하라. 실존 인물은 쓰지 않는다.")
        return self.p.complete_json("bible", CRAFT, prompt, Bible,
                                    {"logline": logline, "genre": genre, "title": title, "story_year": story_year})

    def beats(self, bible: Bible, hook_variant: str, episodes: list[int]) -> BeatSheet:
        prompt = (f"{bible_context(bible)}\n\n위 바이블로 {episodes[0]}~{episodes[-1]}화의 비트 시트를 써라. "
                  f"훅 방향: {hook_variant}. 회차마다 summary(2~3문장), 등장 인물 이름 목록, 회차 끝 hook 을 쓴다. "
                  f"episode 번호는 {episodes} 를 그대로 쓴다.")
        bs = self.p.complete_json("beats", CRAFT, prompt, BeatSheet,
                                  {"bible": bible, "hook_variant": hook_variant, "episodes": episodes})
        want = set(episodes)
        bs.beats = sorted([b for b in bs.beats if b.episode in want], key=lambda b: b.episode)
        return bs

    def episode(self, bible: Bible, beat: Beat, prev: list[Beat], prev_scene: Optional[Scene]) -> EpisodeScript:
        recap = "\n".join(f"{b.episode}화: {b.summary} / 엔딩: {b.hook or '-'}" for b in prev) or "(첫 회)"
        last = prev_scene.text() if prev_scene else "(없음)"
        prompt = (f"{bible_context(bible, beat.characters)}\n\n[지난 회차 요약]\n{recap}\n\n[직전 장면]\n{last}\n\n"
                  f"[이번 회차 비트]\n{beat.episode}화: {beat.summary}\n엔딩 훅: {beat.hook or '-'}\n\n"
                  f"이 회차 대본을 1~3개 장면으로 써라. 각 장면 episode={beat.episode}, heading 은 'S#번호. 장소 - 시간', "
                  f"action 은 지문, dialogue 는 speaker/line 목록. 마지막 장면은 엔딩 훅으로 끝낸다.")
        ep = self.p.complete_json("episode", CRAFT, prompt, EpisodeScript,
                                  {"bible": bible, "beat": beat, "prev": prev})
        for s in ep.scenes:
            s.episode = beat.episode
        return ep

    def repair(self, bible: Bible, scenes: list[Scene], issues: list) -> EpisodeScript:
        names = sorted({d.speaker for s in scenes for d in s.dialogue})
        prompt = (f"{bible_context(bible, names)}\n\n[대본]\n" + "\n\n".join(s.text() for s in scenes)
                  + "\n\n[연속성 오류]\n" + "\n".join(f"- {i.message}" for i in issues)
                  + "\n\n오류만 고치고 나머지 내용과 문체는 최대한 유지해 같은 형식으로 다시 써라.")
        ep = self.p.complete_json("repair_episode", CRAFT, prompt, EpisodeScript,
                                  {"bible": bible, "scenes": scenes, "issues": issues})
        if scenes:
            for s in ep.scenes:
                s.episode = scenes[0].episode
        return ep

    def storyboard(self, bible: Bible, scenes: list[Scene]) -> Storyboard:
        prompt = (f"{bible_context(bible, sorted({d.speaker for s in scenes for d in s.dialogue}))}\n\n[대본]\n"
                  + "\n\n".join(s.text() for s in scenes)
                  + "\n\n이 대본을 세로형 숏드라마 샷 목록으로 나눠라. 샷마다 episode, index(회차 내 0부터), "
                    "description(화면에 보이는 것만, 영상 생성 프롬프트로 쓸 수 있게 구체적으로), characters, "
                    "duration_sec(2~6), camera(와이드/미디엄/클로즈업/인서트 등).")
        sb = self.p.complete_json("storyboard", CRAFT, prompt, Storyboard, {"bible": bible, "scenes": scenes})
        return sb
