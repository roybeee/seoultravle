"""'AI 티' 역검출: 생성 대본에서 시청자가 'AI 같다'고 느끼는 신호를 수치로 잡는다.

한국어 숏드라마 대본 기준 휴리스틱:
- 문장 끝 단조로움(지문의 '~다.' 비율, 최빈 어미 점유율)
- 문장 길이 변동 부족(변동계수)
- 상투구(LLM이 남발하는 표현) 빈도
- 장면 간 반복 구절(같은 3어절 묶음 재사용)
- 인물 말투 구분 부족(화자 간 어미 분포 유사도)
점수 0~100, 높을수록 'AI 티'가 강하다. 판정 기준은 출시 전 실제 시청자 데이터로 다시 맞춰야 한다.
"""

from __future__ import annotations

import re
import statistics
from collections import Counter

from .models import Scene

CLICHES = (
    "숨을 들이켰다", "숨을 삼켰다", "심장이 쿵", "묘한 기분", "알 수 없는 감정", "눈빛이 흔들렸다",
    "정적이 흘렀다", "입꼬리가 올라갔다", "입꼬리를 올렸다", "주먹을 꽉 쥐었다", "시간이 멈춘 듯",
    "운명의 수레바퀴", "그 순간", "어쩌면", "마치", "한 줄기", "가슴 한켠", "미묘한", "복잡한 감정",
    "깊은 한숨", "결연한 표정", "의미심장한", "새로운 시작", "모든 것이 달라졌다",
)


def _sents(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?…])\s+|\n", text) if s.strip()]


def _ending(s: str) -> str:
    s = s.rstrip(" .!?…\"'”’")
    return s[-2:] if len(s) >= 2 else s


def analyze(scenes: list[Scene]) -> dict:
    action = " ".join(s.action for s in scenes)
    lines = [d.line for s in scenes for d in s.dialogue]
    all_text = action + " " + " ".join(lines)
    a_sents = _sents(action)
    all_sents = _sents(all_text)
    flags: list[str] = []

    da_ratio = (sum(1 for s in a_sents if s.rstrip().endswith("다.")) / len(a_sents)) if a_sents else 0.0
    endings = Counter(_ending(s) for s in all_sents)
    top_share = (endings.most_common(1)[0][1] / len(all_sents)) if all_sents else 0.0

    lens = [len(s) for s in all_sents]
    cv = (statistics.pstdev(lens) / statistics.mean(lens)) if len(lens) >= 3 and statistics.mean(lens) else 1.0

    cliche_hits = {c: all_text.count(c) for c in CLICHES if c in all_text}
    words = len(all_text.split()) or 1
    cliche_rate = sum(cliche_hits.values()) / words * 100  # 100어절당

    # 장면 간 3어절 반복
    grams_per_scene = []
    for s in scenes:
        toks = s.text().split()
        grams_per_scene.append({" ".join(toks[i:i + 3]) for i in range(len(toks) - 2)})
    cnt = Counter(g for gs in grams_per_scene for g in gs)
    repeated = [g for g, n in cnt.items() if n >= 3]
    rep_rate = len(repeated) / max(1, len(cnt))

    # 화자별 말투 구분
    by_speaker: dict[str, Counter] = {}
    for s in scenes:
        for d in s.dialogue:
            by_speaker.setdefault(d.speaker, Counter())[_ending(d.line)] += 1
    voice_sim = _avg_similarity(list(by_speaker.values()))

    score = 0.0
    if a_sents and da_ratio > 0.85:
        score += 20; flags.append(f"지문의 {da_ratio:.0%}가 '~다.'로 끝납니다(리듬 단조).")
    if top_share > 0.5:
        score += 15; flags.append(f"한 어미('{endings.most_common(1)[0][0]}')가 문장의 {top_share:.0%}를 차지합니다.")
    if cv < 0.3:
        score += 20; flags.append(f"문장 길이 변화가 작습니다(변동계수 {cv:.2f}).")
    if cliche_rate > 1.0:
        score += min(25, cliche_rate * 8); flags.append(f"상투구 {sum(cliche_hits.values())}회: "
                                                       + ", ".join(list(cliche_hits)[:6]))
    if rep_rate > 0.05:
        score += 10; flags.append(f"장면 간 반복 구절 {len(repeated)}개.")
    if len(by_speaker) >= 2 and voice_sim > 0.8:
        score += 10; flags.append(f"인물 간 말투 구분이 약합니다(어미 분포 유사도 {voice_sim:.2f}).")

    return {
        "score": round(min(100.0, score), 1),
        "level": "high" if score >= 50 else "medium" if score >= 25 else "low",
        "flags": flags,
        "metrics": {
            "da_ending_ratio": round(da_ratio, 3), "top_ending_share": round(top_share, 3),
            "sentence_length_cv": round(cv, 3), "cliche_per_100_words": round(cliche_rate, 2),
            "repeated_trigrams": len(repeated), "voice_similarity": round(voice_sim, 3),
            "sentences": len(all_sents),
        },
    }


def _avg_similarity(dists: list[Counter]) -> float:
    if len(dists) < 2:
        return 0.0
    sims = []
    for i in range(len(dists)):
        for j in range(i + 1, len(dists)):
            a, b = dists[i], dists[j]
            keys = set(a) | set(b)
            dot = sum(a[k] * b[k] for k in keys)
            na = sum(v * v for v in a.values()) ** 0.5
            nb = sum(v * v for v in b.values()) ** 0.5
            if na and nb:
                sims.append(dot / (na * nb))
    return statistics.mean(sims) if sims else 0.0
