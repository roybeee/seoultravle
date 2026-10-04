"""파일럿 검증: 비공개 독자단 블라인드 평가 + 동일 노출 A/B.

승격 규칙(기본): 종합 점수 상위 25%(최소 1편), 단 A/B 완주율이 기준 이하이면 제외.
통계는 표본이 작을 때 과신하지 않도록 윌슨 신뢰구간 하한을 쓴다.
"""

from __future__ import annotations

import math
from statistics import mean
from typing import Optional

from .models import ABResult, PanelRating


def wilson_lower(success: int, n: int, z: float = 1.96) -> float:
    if n == 0:
        return 0.0
    p = success / n
    denom = 1 + z * z / n
    centre = p + z * z / (2 * n)
    margin = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return max(0.0, (centre - margin) / denom)


def two_proportion_p(s1: int, n1: int, s2: int, n2: int) -> float:
    """양측 검정 p값."""
    if n1 == 0 or n2 == 0:
        return 1.0
    p = (s1 + s2) / (n1 + n2)
    se = math.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    if se == 0:
        return 1.0
    z = (s1 / n1 - s2 / n2) / se
    return math.erfc(abs(z) / math.sqrt(2))


def panel_score(ratings: list[PanelRating]) -> Optional[float]:
    if not ratings:
        return None
    vals = [(r.completion_intent * 0.5 + r.rewatch * 0.2 + r.recommend * 0.3) for r in ratings]
    return round((mean(vals) - 1) / 4, 4)  # 0~1


def leaderboard(pilot_ids: list[str], ratings: list[PanelRating], ab: list[ABResult],
                top_fraction: float = 0.25, min_completion_lb: float = 0.05) -> list[dict]:
    ab_by = {}
    for r in ab:
        cur = ab_by.setdefault(r.pilot_id, [0, 0, 0])
        cur[0] += r.impressions; cur[1] += r.completions; cur[2] += r.follows
    rows = []
    for pid in pilot_ids:
        ps = panel_score([r for r in ratings if r.pilot_id == pid])
        imp, comp, fol = ab_by.get(pid, [0, 0, 0])
        comp_lb = wilson_lower(comp, imp) if imp else None
        parts = [x for x in [ps, (comp_lb * 4 if comp_lb is not None else None)] if x is not None]
        score = round(mean(min(1.0, x) for x in parts), 4) if parts else None
        rows.append({"pilot_id": pid, "panel_score": ps, "impressions": imp, "completions": comp,
                     "follows": fol, "completion_rate": round(comp / imp, 4) if imp else None,
                     "completion_lb95": round(comp_lb, 4) if comp_lb is not None else None,
                     "score": score, "panel_n": len([r for r in ratings if r.pilot_id == pid])})
    scored = sorted([r for r in rows if r["score"] is not None], key=lambda r: r["score"], reverse=True)
    k = max(1, math.ceil(len(scored) * top_fraction)) if scored else 0
    for i, r in enumerate(scored):
        r["rank"] = i + 1
        eligible = r["completion_lb95"] is None or r["completion_lb95"] >= min_completion_lb
        r["promote"] = i < k and eligible
    if len(scored) >= 2 and scored[0]["impressions"] and scored[1]["impressions"]:
        a, b = scored[0], scored[1]
        scored[0]["p_vs_next"] = round(two_proportion_p(a["completions"], a["impressions"],
                                                        b["completions"], b["impressions"]), 4)
    unscored = [dict(r, rank=None, promote=False) for r in rows if r["score"] is None]
    return scored + unscored
