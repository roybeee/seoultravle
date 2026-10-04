"""내보내기: 플랫폼 게시용(platform) / 납품용(delivery) 패키지.

잠금: AI 생성 표시·매니페스트는 항상 포함. 법적 차단 항목이 있으면 내보내지 않는다.
토글: delivery_export_warning(기여 기록 없는 작품의 납품 경고), contribution_grade_display, brand_separation.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from . import labeling, safety
from .models import Mode, Pilot, utcnow
from .studio import StudioError


def script_markdown(title: str, p: Pilot) -> str:
    out = [f"# {title} — 파일럿 {p.id}", f"훅 방향: {p.hook_variant}", ""]
    if p.beats:
        out.append("## 비트 시트")
        for b in p.beats.beats:
            out.append(f"- **{b.episode}화** {b.summary}" + (f"  \n  엔딩 훅: {b.hook}" if b.hook else ""))
        out.append("")
    cur = None
    for s in p.scenes:
        if s.episode != cur:
            cur = s.episode
            out.append(f"## {cur}화")
        out += [f"### {s.heading}", s.action, ""]
        out += [f"**{d.speaker}**: {d.line}  " for d in s.dialogue]
        out.append("")
    return "\n".join(out)


def build_package(studio, pid: str, plt: str, kind: str = "platform", out: Optional[Path] = None) -> dict:
    if kind not in ("platform", "delivery"):
        raise ValueError("kind 는 platform 또는 delivery")
    pr = studio.project(pid)
    pol = studio.policy(pid)
    p = studio.pilot(pid, plt)
    if p.stage != "done":
        raise StudioError(f"파일럿이 완료되지 않았습니다(현재 단계: {p.stage}, 승인 대기: {p.pending_review}).")
    blocks = safety.blocking(p.issues)
    if blocks:
        raise StudioError("법적 차단 항목 때문에 내보낼 수 없습니다: " + "; ".join(i.message for i in blocks))

    ledger = studio.ledger(pid)
    cert = studio.certificate(pid) if pol.on("contribution_record") else None
    grade = cert["grade"] if cert else None
    human = bool(cert and grade != "D")
    flags = (p.render_plan or {}).get("safety", {})
    deepfake = bool(flags.get("deepfake_visible_label_required"))

    warnings: list[str] = []
    if kind == "delivery" and pol.on("delivery_export_warning"):
        if cert is None:
            warnings.append("인간 기여 기록이 꺼져 있어 권리 증빙이 없습니다. 납품 계약의 권리보증 조항을 확인하세요.")
        elif grade in ("C", "D"):
            warnings.append(f"인간 기여 등급 {grade}({cert['grade_text']}): 저작권 보호 범위가 제한될 수 있습니다.")
    if flags.get("adult_age_verification_required"):
        warnings.append("19 등급 추정: 게시 플랫폼에서 연령 확인을 적용해야 합니다(법적 의무).")
    errors = [i for i in p.issues if i.severity == "error"]
    if errors:
        warnings.append(f"해결되지 않은 검수 오류 {len(errors)}건이 있습니다(qc.json).")

    if pr.mode == Mode.AUTO and pol.on("brand_separation"):
        brand = "STORY8 Lab (자동 생성)"
    else:
        brand = pr.brand or "STORY8"

    script = script_markdown(pr.name, p)
    shown_grade = grade if pol.on("contribution_grade_display") else None
    files = {
        "script.md": script,
        "beats.json": p.beats.model_dump_json(indent=2) if p.beats else "{}",
        "storyboard.json": p.storyboard.model_dump_json(indent=2) if p.storyboard else "{}",
        "render_plan.json": json.dumps(p.render_plan or {}, ensure_ascii=False, indent=2),
        "qc.json": json.dumps({"issues": [i.model_dump() for i in p.issues], "ai_tell": p.ai_tell,
                               "safety": flags}, ensure_ascii=False, indent=2),
    }
    disclosure = labeling.disclosure(human, deepfake, shown_grade)
    manifest = labeling.manifest(pr.name, files, human, deepfake, ledger.head, shown_grade)
    meta = {
        "project": pr.id, "pilot": p.id, "kind": kind, "mode": pr.mode.value, "brand": brand,
        "exported_at": utcnow(), "estimated_rating": p.rating, "warnings": warnings,
        "training_opt_in": pol.on("training_opt_in"), "settings": pol.settings,
    }
    files["disclosure.json"] = json.dumps(disclosure, ensure_ascii=False, indent=2)
    files["manifest.json"] = json.dumps(manifest, ensure_ascii=False, indent=2)
    files["package.json"] = json.dumps(meta, ensure_ascii=False, indent=2)
    if cert:
        files["s8proof.json"] = json.dumps(cert, ensure_ascii=False, indent=2)

    out = out or (studio._dir(pid) / "exports" / f"{p.id}-{kind}")
    out.mkdir(parents=True, exist_ok=True)
    for name, content in files.items():
        (out / name).write_text(content, encoding="utf-8")
    studio._log(pid, f"{p.id}/export", "export", studio.system, manifest, stage="export", kind=kind,
                recorded=False)
    return {"path": str(out), "files": sorted(files), "warnings": warnings, "grade": grade, "brand": brand,
            "disclosure": disclosure}
