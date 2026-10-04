"""프리비즈·렌더 계획: 스토리보드를 영상 생성 프롬프트와 비용 견적으로 바꾼다.

영상 생성 모델은 빠르게 바뀌므로 어댑터로 분리한다. 기본 제공 어댑터는
- DryRunVideoProvider: 실제 호출 없이 계획만 만든다.
- ExternalPromptExport: 샷 프롬프트를 외부 도구(Higgsfield·Kling·Veo 등) 입력 형식으로 내보낸다.
가격표는 가정치이며 계약 단가로 덮어쓴다(STORY8_PRICE_PER_SEC 환경 변수 또는 인자).
"""

from __future__ import annotations

import os
from typing import Optional, Protocol

from .models import Bible, Shot, Storyboard

# 초당 생성 단가(USD) — 2026 공개 단가 범위를 단순화한 가정치. 반드시 실제 견적으로 교체.
DEFAULT_PRICE_PER_SEC = {"economy": 0.05, "standard": 0.15, "premium": 0.40}
RETAKE_FACTOR = 2.5  # 쓸 수 있는 컷 1개를 얻기 위한 평균 재생성 배수(가정)


class VideoProvider(Protocol):
    name: str

    def submit(self, prompt: dict) -> dict: ...


class DryRunVideoProvider:
    name = "dry-run"

    def submit(self, prompt: dict) -> dict:
        return {"status": "planned", "shot": prompt["shot_id"]}


def character_sheet(bible: Bible, names: list[str]) -> dict[str, str]:
    """인물 일관성 토큰: 모든 샷 프롬프트에 같은 외형 묘사를 붙인다."""
    out = {}
    for n in names:
        c = bible.character(n)
        if c is None:
            continue
        age = bible.age_of(c)
        parts = [p for p in [f"{age}세" if age else None, c.gender, c.nationality, c.appearance] if p]
        out[c.name] = ", ".join(parts) or c.name
    return out


def shot_prompt(bible: Bible, shot: Shot, style: str, label_deepfake: bool) -> dict:
    sheet = character_sheet(bible, shot.characters)
    text = f"{style}. {shot.camera or ''} shot. {shot.description}."
    if sheet:
        text += " Characters: " + "; ".join(f"{k} ({v})" for k, v in sheet.items()) + "."
    p = {
        "shot_id": f"E{shot.episode:02d}-S{shot.index:03d}",
        "episode": shot.episode,
        "prompt": text.strip(),
        "negative": "text artifacts, extra fingers, face morphing, inconsistent outfit",
        "aspect_ratio": "9:16",
        "duration_sec": shot.duration_sec,
        "characters": sheet,
        "overlay_labels": ["AI 생성 · AI-generated"],
    }
    if label_deepfake:
        p["overlay_labels"].append("실존 인물이 아닌 AI 합성 영상입니다")
    return p


def render_plan(bible: Bible, sb: Storyboard, tier: str = "standard", style: Optional[str] = None,
                label_deepfake: bool = False, price_per_sec: Optional[float] = None,
                provider: Optional[VideoProvider] = None) -> dict:
    style = style or f"vertical short drama, cinematic, Korean {bible.genre}, {bible.tone or 'dramatic'} lighting"
    price = price_per_sec or float(os.environ.get("STORY8_PRICE_PER_SEC", 0) or 0) or DEFAULT_PRICE_PER_SEC[tier]
    prov = provider or DryRunVideoProvider()
    shots = [shot_prompt(bible, s, style, label_deepfake) for s in sb.shots]
    jobs = [prov.submit(p) for p in shots]
    seconds = sum(s.duration_sec for s in sb.shots)
    by_ep: dict[int, float] = {}
    for s in sb.shots:
        by_ep[s.episode] = by_ep.get(s.episode, 0) + s.duration_sec
    gen_cost = seconds * price * RETAKE_FACTOR
    return {
        "provider": prov.name,
        "tier": tier,
        "style": style,
        "shots": shots,
        "jobs": jobs,
        "total_seconds": round(seconds, 1),
        "seconds_by_episode": by_ep,
        "estimate_usd": {
            "price_per_sec": price,
            "retake_factor": RETAKE_FACTOR,
            "generation": round(gen_cost, 2),
            "note": "가정 단가 기반 추정. 음성·음악·편집·검수 인건비 제외.",
        },
    }
