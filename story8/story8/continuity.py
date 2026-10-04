"""연속성 검증기: 캐논 바이블과 대본의 모순을 찾는다.

1차는 규칙 기반(결정적·무료), 2차는 선택적으로 LLM 의미 검사를 더한다.
규칙 검사로 잡는 것: 사망 인물 등장, 미등록 화자, 금칙어, 나이 불일치, 고정 속성(키·체중 등) 불일치,
세계관 규칙의 '금지' 문구 위반.
"""

from __future__ import annotations

import re
from typing import Optional

from pydantic import BaseModel, Field

from .models import Beat, Bible, Issue, Scene

FLASHBACK = ("회상", "과거", "플래시백", "flashback")
_NUM = re.compile(r"(\d+(?:\.\d+)?)")
_AGE = re.compile(r"(\d{1,3})\s*(?:살|세)")


class SemanticReport(BaseModel):
    issues: list[Issue] = Field(default_factory=list)


def _sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?。])\s+|\n", text) if s.strip()]


def _is_flashback(scene: Scene) -> bool:
    return any(k in scene.heading for k in FLASHBACK)


def check_beats(bible: Bible, beats: list[Beat]) -> list[Issue]:
    issues: list[Issue] = []
    names = {c.name for c in bible.characters}
    for b in beats:
        for n in b.characters:
            ch = bible.character(n)
            if ch is None:
                issues.append(Issue(severity="warning", code="unknown_character", episode=b.episode,
                                    message=f"바이블에 없는 인물 '{n}'이 비트에 등장합니다."))
            elif ch.deceased_in_story_year is not None and ch.deceased_in_story_year <= bible.story_year \
                    and not any(k in b.summary for k in FLASHBACK):
                issues.append(Issue(severity="error", code="deceased_appears", episode=b.episode,
                                    message=f"'{n}'은(는) {ch.deceased_in_story_year}년에 사망했는데 "
                                            f"{bible.story_year}년 비트에 등장합니다(회상 표시 없음)."))
        issues += _ng(bible, b.summary + " " + (b.hook or ""), b.episode)
    if not names:
        issues.append(Issue(severity="warning", code="empty_bible", message="바이블에 인물이 없습니다."))
    return issues


def _ng(bible: Bible, text: str, episode: Optional[int]) -> list[Issue]:
    return [Issue(severity="error", code="ng_word", episode=episode,
                  message=f"금칙 표현 '{w}'이(가) 쓰였습니다.")
            for w in bible.ng_list if w and w in text]


def check_scene(bible: Bible, scene: Scene) -> list[Issue]:
    issues: list[Issue] = []
    ep = scene.episode
    flash = _is_flashback(scene)
    text = scene.text()

    for d in scene.dialogue:
        ch = bible.character(d.speaker)
        if ch is None:
            if d.speaker not in ("내레이션", "NA", "N", "목소리", "V.O."):
                issues.append(Issue(severity="warning", code="unknown_speaker", episode=ep,
                                    message=f"바이블에 없는 화자 '{d.speaker}'."))
            continue
        if ch.deceased_in_story_year is not None and ch.deceased_in_story_year <= bible.story_year and not flash:
            issues.append(Issue(severity="error", code="deceased_speaks", episode=ep,
                                message=f"'{ch.name}'은(는) {ch.deceased_in_story_year}년 사망 인물인데 "
                                        f"대사가 있습니다. 회상 장면이면 장면 제목에 '회상'을 표시하세요."))

    issues += _ng(bible, text, ep)

    for sent in _sentences(text):
        for ch in bible.characters:
            if ch.name not in sent:
                continue
            # 나이
            age = bible.age_of(ch)
            m = _AGE.search(sent)
            if age is not None and m and not flash:
                stated = int(m.group(1))
                # 같은 문장에 다른 인물 이름이 있으면 누구 나이인지 모호하므로 건너뛴다
                others = [o for o in bible.characters if o is not ch and o.name in sent]
                if not others and abs(stated - age) > 1:
                    issues.append(Issue(severity="warning", code="age_mismatch", episode=ep,
                                        message=f"'{ch.name}'의 극중 나이는 {age}세인데 '{m.group(0)}'로 쓰였습니다."))
            # 고정 속성(숫자 값)
            for key, val in ch.attributes.items():
                vnum = _NUM.search(val)
                if not vnum or key not in sent:
                    continue
                after = sent[sent.find(key):]
                snum = _NUM.search(after)
                if snum and abs(float(snum.group(1)) - float(vnum.group(1))) > 0.5:
                    issues.append(Issue(severity="warning", code="attribute_mismatch", episode=ep,
                                        message=f"'{ch.name}'의 {key}는 바이블상 {val}인데 대본에는 "
                                                f"{snum.group(1)}(으)로 쓰였습니다."))

    for rule in bible.rules:
        for banned in re.findall(r"'([^']+)'\s*(?:금지|불가|없다)", rule.text):
            if banned in text:
                issues.append(Issue(severity="error", code="world_rule", episode=ep,
                                    message=f"세계관 규칙 위반: {rule.text}"))
    return issues


def check_script(bible: Bible, scenes: list[Scene]) -> list[Issue]:
    out: list[Issue] = []
    for sc in scenes:
        out += check_scene(bible, sc)
    return dedupe(out)


def dedupe(issues: list[Issue]) -> list[Issue]:
    seen, out = set(), []
    for i in issues:
        k = (i.code, i.message, i.episode)
        if k not in seen:
            seen.add(k)
            out.append(i)
    return out


SEMANTIC_SYSTEM = (
    "너는 드라마 연속성 감수자다. 캐논 바이블과 대본을 비교해 설정 모순만 찾는다. "
    "문체 취향이나 개선 제안은 하지 않는다. 모순이 없으면 빈 목록을 낸다. "
    "severity 는 error(설정과 정면 충돌) 또는 warning(의심)만 쓴다. code 는 'semantic'."
)


def semantic_check(provider, bible: Bible, scenes: list[Scene], context_text: str) -> list[Issue]:
    prompt = f"[바이블]\n{context_text}\n\n[대본]\n" + "\n\n".join(s.text() for s in scenes)
    rep = provider.complete_json("continuity", SEMANTIC_SYSTEM, prompt, SemanticReport,
                                 {"bible": bible, "scenes": scenes})
    return [i for i in rep.issues if i.severity in ("error", "warning")]
