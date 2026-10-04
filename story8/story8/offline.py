"""오프라인 생성기: 서버·키 없이 파이프라인 전체를 시험하기 위한 결정적 생성기.

실제 창작 품질을 내지 않는다. 데이터 흐름·검증·권리 기록·내보내기를 시험하는 용도다.
"""

from __future__ import annotations

import hashlib
from typing import Optional, TypeVar

from pydantic import BaseModel

from .models import (Beat, BeatSheet, Bible, Character, DialogueLine, EpisodeScript, LifeEvent, Place,
                     Relation, Scene, Shot, Storyboard, WorldRule)

T = TypeVar("T", bound=BaseModel)

TIMES = ["밤", "새벽", "오후", "저녁", "아침"]
HOOKS = {
    "복수": "{a}가 마침내 진실의 조각을 손에 넣는다. 그리고 {b}의 이름이 적힌 문서를 발견한다.",
    "로맨스": "{a}와 {b}의 손이 닿는 순간, 문이 열리고 누군가 그 장면을 본다.",
    "미스터리": "{a}의 휴대폰에 존재하지 않아야 할 번호로 문자가 도착한다.",
}


def _pick(seq, key: str, salt: str = ""):
    h = int(hashlib.sha256((key + salt).encode()).hexdigest(), 16)
    return seq[h % len(seq)]


class OfflineProvider:
    name = "offline"
    model = "offline-deterministic"

    def __init__(self):
        self.usage = {"calls": 0}

    def complete_json(self, task: str, system: str, prompt: str, schema: type[T],
                      context: Optional[dict] = None) -> T:
        self.usage["calls"] += 1
        ctx = context or {}
        fn = getattr(self, f"_task_{task}", None)
        if fn is None:
            raise NotImplementedError(f"offline provider: {task}")
        return schema.model_validate(fn(ctx).model_dump())

    # ── tasks ──
    def _task_beats(self, ctx) -> BeatSheet:
        bible: Bible = ctx["bible"]
        names = [c.name for c in bible.characters if c.deceased_in_story_year is None] or ["주인공"]
        a = names[0]
        b = names[1] if len(names) > 1 else names[0]
        variant = ctx.get("hook_variant", "미스터리")
        hook_t = next((v for k, v in HOOKS.items() if k in variant), HOOKS["미스터리"])
        beats = []
        for ep in ctx["episodes"]:
            beats.append(Beat(
                episode=ep,
                summary=f"{bible.logline} — {a}는 {b}와 부딪히며 감춰진 사정에 한 걸음 다가간다.",
                characters=[a, b] if a != b else [a],
                hook=hook_t.format(a=a, b=b),
            ))
        return BeatSheet(beats=beats)

    def _task_bible(self, ctx) -> Bible:
        seed = ctx.get("logline", "")
        year = int(ctx.get("story_year") or 2026)
        a = Character(name=_pick(["서하윤", "강도현", "윤재희"], seed), birth_year=year - 29, gender="여",
                      nationality="한국", occupation="변호사", traits=["집요함", "감정을 숨김"],
                      appearance="검은 단발, 회색 트렌치코트", speech_style="짧고 단정한 존댓말",
                      backstory="아버지의 죽음 뒤 사건을 혼자 추적해 왔다.",
                      life_events=[LifeEvent(age=19, description="아버지가 사고로 사망")])
        b = Character(name=_pick(["차민혁", "한지오", "백승우"], seed, "b"), birth_year=year - 32, gender="남",
                      nationality="한국", occupation="재벌 2세", traits=["오만함", "죄책감"],
                      appearance="흰 셔츠, 은색 시계", speech_style="반말과 존댓말을 섞는 냉소적 말투",
                      backstory="그날 밤 사고 현장에 있었다.")
        c = Character(name="서정훈", birth_year=year - 60, gender="남", occupation="회계사",
                      deceased_in_story_year=year - 10, backstory=f"{a.name}의 아버지.")
        return Bible(
            title=ctx.get("title") or "무제", logline=seed or "숨겨진 진실을 쫓는 이야기",
            genre=ctx.get("genre") or "복수 로맨스", story_year=year, tone="차갑고 긴장감 있는",
            characters=[a, b, c],
            places=[Place(name="한강 펜트하우스"), Place(name="법률사무소 옥상"), Place(name="폐공장")],
            relations=[Relation(source=a.id, target=b.id, kind="적대→연인"),
                       Relation(source=c.id, target=a.id, kind="부녀")],
            rules=[WorldRule(text="초자연 현상 없음. '타임슬립' 금지")],
            ng_list=["막장 출생의 비밀"],
        )

    def _task_episode(self, ctx) -> EpisodeScript:
        return EpisodeScript(scenes=[self._task_scene(ctx)])

    def _task_repair_episode(self, ctx) -> EpisodeScript:
        return EpisodeScript(scenes=[self._task_repair_scene({"scene": s, "bible": ctx["bible"]})
                                     for s in ctx["scenes"]])

    def _task_scene(self, ctx) -> Scene:
        bible: Bible = ctx["bible"]
        beat: Beat = ctx["beat"]
        place = _pick([p.name for p in bible.places] or ["작업실"], beat.summary)
        time = _pick(TIMES, beat.summary, "t")
        speakers = beat.characters or [bible.characters[0].name]
        a = speakers[0]
        b = speakers[1] if len(speakers) > 1 else speakers[0]
        lines = [
            DialogueLine(speaker=a, line=f"{b}, 오늘은 피하지 마. 그날 일, 너도 알고 있었잖아."),
            DialogueLine(speaker=b, line="알았다면 내가 여기 서 있을 것 같아?"),
            DialogueLine(speaker=a, line="그럼 이 문서는 뭔데. 네 이름이 왜 여기 있어."),
        ]
        return Scene(
            episode=beat.episode,
            heading=f"S#{beat.episode}. {place} - {time}",
            action=f"{a}가 낡은 서류철을 탁자에 내려놓는다. {b}의 시선이 잠깐 흔들린다. {beat.hook or ''}",
            dialogue=lines,
        )

    def _task_repair_scene(self, ctx) -> Scene:
        scene: Scene = ctx["scene"]
        bible: Bible = ctx["bible"]
        ng = [w for w in bible.ng_list]
        alive = {c.name for c in bible.characters if c.deceased_in_story_year is None}
        dialogue = [d for d in scene.dialogue if d.speaker in alive] or scene.dialogue[:1]
        action = scene.action
        for w in ng:
            action = action.replace(w, "")
        return Scene(episode=scene.episode, heading=scene.heading, action=action,
                     dialogue=[DialogueLine(speaker=d.speaker, line=_strip(d.line, ng)) for d in dialogue])

    def _task_storyboard(self, ctx) -> Storyboard:
        scenes: list[Scene] = ctx["scenes"]
        shots = []
        for sc in scenes:
            chars = sorted({d.speaker for d in sc.dialogue})
            base = [
                ("와이드. " + sc.heading.split(". ", 1)[-1] + " 전경, 인물 등장", 3.0, "와이드"),
                (sc.action[:80], 5.0, "미디엄"),
            ]
            base += [(f"{d.speaker} 클로즈업: \"{d.line[:40]}\"", 4.0, "클로즈업") for d in sc.dialogue]
            for i, (desc, dur, cam) in enumerate(base):
                shots.append(Shot(episode=sc.episode, index=i, description=desc, characters=chars,
                                  duration_sec=dur, camera=cam))
        return Storyboard(shots=shots)

    def _task_continuity(self, ctx):
        from .continuity import SemanticReport
        return SemanticReport(issues=[])


def _strip(text: str, words: list[str]) -> str:
    for w in words:
        text = text.replace(w, "")
    return text
