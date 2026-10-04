"""S8 Proof: 권리 원장에서 인간 기여를 집계해 기여 증명서를 만든다.

등급(인간 기여 강도):
  A 인간 집필  — 사람이 바이블을 만들고 대본을 상당 부분(편집률 30% 이상) 직접 고쳤다
  B 인간 주도  — 사람이 바이블을 만들고 단계별로 결정·수정했다
  C 인간 선택  — 사람은 승인·선택만 했다
  D AI 생성    — 기록된 인간 기여가 없다
원칙:
  - contribution_record 가 켜진 상태에서 기록된 이벤트(detail.recorded=True)만 센다.
  - 소급 상향 금지: 기록되지 않은 과거 작업은 나중에 기록을 켜도 인정하지 않는다.
  - 증명서는 원장 머리 해시와 원장 무결성 검증 결과를 함께 싣는다.
"""

from __future__ import annotations

import hashlib
import hmac
from typing import Optional

from .ledger import Ledger, canonical
from .models import utcnow

GRADE_TEXT = {"A": "인간 집필", "B": "인간 주도", "C": "인간 선택", "D": "AI 생성"}


def tally(ledger: Ledger, subject_prefix: str) -> dict:
    counts = {"human_create": 0, "human_edit": 0, "human_approve": 0, "ai_draft": 0, "auto_approve": 0}
    stages_human: set[str] = set()
    edit_ratios: dict[str, float] = {}
    bible_by_human = False
    for ev in ledger.for_subject(subject_prefix):
        human = ev.actor.kind == "human" and ev.detail.get("recorded", False)
        stage = ev.detail.get("stage", "")
        if ev.action == "ai_draft":
            counts["ai_draft"] += 1
        elif ev.action == "auto_approve":
            counts["auto_approve"] += 1
        elif human and ev.action == "create":
            counts["human_create"] += 1
            if stage == "bible":
                bible_by_human = True
            stages_human.add(stage)
        elif human and ev.action == "human_edit":
            counts["human_edit"] += 1
            stages_human.add(stage)
            r = float(ev.detail.get("edit_ratio", 0.0))
            edit_ratios[stage] = max(edit_ratios.get(stage, 0.0), r)
        elif human and ev.action == "approve":
            counts["human_approve"] += 1
            stages_human.add(stage)
    return {"counts": counts, "stages_human": sorted(s for s in stages_human if s),
            "edit_ratios": edit_ratios, "bible_by_human": bible_by_human}


def grade_of(t: dict) -> str:
    c = t["counts"]
    if c["human_create"] + c["human_edit"] + c["human_approve"] == 0:
        return "D"
    if t["bible_by_human"] and t["edit_ratios"].get("script", 0.0) >= 0.30:
        return "A"
    if t["bible_by_human"] and c["human_edit"] > 0:
        return "B"
    return "C"


def certificate(ledger: Ledger, project_id: str, title: str, subject_prefix: Optional[str] = None,
                secret: str = "story8-dev-secret") -> dict:
    t = tally(ledger, subject_prefix or project_id)
    g = grade_of(t)
    ok, errors = ledger.verify()
    body = {
        "type": "S8Proof/contribution-certificate",
        "project_id": project_id,
        "title": title,
        "issued_at": utcnow(),
        "grade": g,
        "grade_text": GRADE_TEXT[g],
        "tally": t,
        "ledger_head": ledger.head,
        "ledger_events": len(ledger.events),
        "ledger_verified": ok,
        "ledger_errors": errors,
        "note": "인간 기여 사실의 기록이며 저작권 성립을 보장하지 않는다. 등록·분쟁 시 법률 검토가 필요하다.",
    }
    body["signature"] = hmac.new(secret.encode(), canonical(body).encode(), hashlib.sha256).hexdigest()
    return body


def verify_certificate(cert: dict, secret: str = "story8-dev-secret") -> bool:
    body = {k: v for k, v in cert.items() if k != "signature"}
    sig = hmac.new(secret.encode(), canonical(body).encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(sig, cert.get("signature", ""))


def edit_ratio(before: str, after: str) -> float:
    """사람 편집량(0~1). 문자 단위 유사도의 보수."""
    from difflib import SequenceMatcher
    if not before and not after:
        return 0.0
    return round(1.0 - SequenceMatcher(None, before, after, autojunk=False).ratio(), 4)
