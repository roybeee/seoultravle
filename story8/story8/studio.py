"""스튜디오: 프로젝트 저장, 모드·정책 적용, 파이프라인 진행, 승인, 평가, 승격, 내보내기.

저장 구조(파일 기반, DB 없이 동작):
  <root>/projects/<project_id>/
      project.json  bible.json  ledger.jsonl  ratings.jsonl  ab.jsonl
      pilots/<pilot_id>.json   exports/<pilot_id>-<kind>/...
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Optional

from . import aitell, continuity, labeling, media, proof, safety
from .evaluation import leaderboard
from .ledger import Ledger, LocalTimestamp, canonical
from .models import (ABResult, Actor, BeatSheet, Bible, Issue, Mode, PanelRating, Pilot, Project, Scene,
                     utcnow)
from .policy import PolicyEngine
from .writers_room import WritersRoom, bible_context

STAGES = ("beats", "script", "storyboard", "edit")


class StudioError(RuntimeError):
    pass


class Studio:
    def __init__(self, root: str | Path, provider=None, secret: Optional[str] = None):
        self.root = Path(root)
        (self.root / "projects").mkdir(parents=True, exist_ok=True)
        if provider is None:
            from .llm import provider_from_env
            provider = provider_from_env()
        self.provider = provider
        self.room = WritersRoom(provider)
        self.secret = secret or os.environ.get("STORY8_SECRET", "story8-dev-secret")
        self.ai = Actor(kind="ai", id=getattr(provider, "model", getattr(provider, "name", "llm")))
        self.system = Actor(kind="system", id="story8")

    # ── 저장 ──────────────────────────────────────────────
    def _dir(self, pid: str) -> Path:
        d = self.root / "projects" / pid
        if not d.exists():
            raise StudioError(f"프로젝트 없음: {pid}")
        return d

    def _write(self, path: Path, obj) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        data = obj.model_dump_json(indent=2) if hasattr(obj, "model_dump_json") else json.dumps(obj, ensure_ascii=False, indent=2)
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_text(data, encoding="utf-8")
        tmp.replace(path)

    def project(self, pid: str) -> Project:
        return Project.model_validate_json((self._dir(pid) / "project.json").read_text(encoding="utf-8"))

    def projects(self) -> list[Project]:
        out = []
        for d in sorted((self.root / "projects").iterdir()):
            if (d / "project.json").exists():
                out.append(Project.model_validate_json((d / "project.json").read_text(encoding="utf-8")))
        return out

    def bible(self, pid: str) -> Bible:
        f = self._dir(pid) / "bible.json"
        if not f.exists():
            raise StudioError("바이블이 아직 없습니다.")
        return Bible.model_validate_json(f.read_text(encoding="utf-8"))

    def pilot(self, pid: str, plt: str) -> Pilot:
        f = self._dir(pid) / "pilots" / f"{plt}.json"
        if not f.exists():
            raise StudioError(f"파일럿 없음: {plt}")
        return Pilot.model_validate_json(f.read_text(encoding="utf-8"))

    def pilots(self, pid: str) -> list[Pilot]:
        d = self._dir(pid) / "pilots"
        if not d.exists():
            return []
        return [Pilot.model_validate_json(f.read_text(encoding="utf-8")) for f in sorted(d.glob("*.json"))]

    def _save_pilot(self, pid: str, p: Pilot) -> None:
        self._write(self._dir(pid) / "pilots" / f"{p.id}.json", p)

    def ledger(self, pid: str) -> Ledger:
        return Ledger(self._dir(pid) / "ledger.jsonl", LocalTimestamp(self.secret))

    def policy(self, pid: str) -> PolicyEngine:
        pr = self.project(pid)
        return PolicyEngine(pr.mode, pr.settings)

    def _log(self, pid: str, subject: str, action: str, actor: Actor, content, **detail):
        pol = self.policy(pid)
        detail.setdefault("recorded", pol.on("contribution_record"))
        detail.setdefault("mode", pol.mode.value)
        return self.ledger(pid).append(f"{pid}/{subject}", action, actor, content, detail)

    # ── 프로젝트·설정 ─────────────────────────────────────
    def create_project(self, name: str, mode: Mode | str = Mode.COLLAB, settings: Optional[dict] = None,
                       brand: Optional[str] = None, actor: Optional[Actor] = None) -> Project:
        mode = Mode(mode)
        pol = PolicyEngine(mode, settings)
        pr = Project(name=name, mode=mode, settings=pol.settings, brand=brand)
        d = self.root / "projects" / pr.id
        d.mkdir(parents=True)
        self._write(d / "project.json", pr)
        self._log(pr.id, "project", "create", actor or self.system,
                  {"name": name, "mode": mode.value, "settings": pol.settings},
                  stage="project", recorded=False)  # 프로젝트 생성은 창작 기여가 아니다
        return pr

    def set_setting(self, pid: str, key: str, value, actor: Optional[Actor] = None) -> Optional[str]:
        pr = self.project(pid)
        pol = PolicyEngine(pr.mode, pr.settings)
        notice = pol.set(key, value)
        pr.settings = pol.settings
        self._write(self._dir(pid) / "project.json", pr)
        self._log(pid, "settings", "check", actor or self.system, {key: value}, setting=key)
        return notice.message if notice else None

    # ── 바이블 ────────────────────────────────────────────
    def import_bible(self, pid: str, bible: Bible | dict, actor: Actor) -> Bible:
        bible = bible if isinstance(bible, Bible) else Bible.model_validate(bible)
        pr = self.project(pid)
        self._write(self._dir(pid) / "bible.json", bible)
        self._log(pid, "bible", "create", actor, bible.model_dump(), stage="bible")
        pr.bible_source = actor.kind
        # 사람이 직접 쓴 바이블은 쓴 것 자체가 결정이므로 별도 승인이 필요 없다.
        pr.bible_approved = actor.kind == "human" or not PolicyEngine(pr.mode, pr.settings).requires_human("bible")
        self._write(self._dir(pid) / "project.json", pr)
        return bible

    def generate_bible(self, pid: str, logline: str, genre: str, title: Optional[str] = None,
                       story_year: int = 2026) -> Bible:
        pr = self.project(pid)
        bible = self.room.generate_bible(logline, genre, title or pr.name, story_year)
        self._write(self._dir(pid) / "bible.json", bible)
        self._log(pid, "bible", "ai_draft", self.ai, bible.model_dump(), stage="bible")
        pol = self.policy(pid)
        pr.bible_source = "ai"
        if pol.requires_human("bible"):
            pr.bible_approved = False
        else:
            pr.bible_approved = True
            self._log(pid, "bible", "auto_approve", self.system, bible.model_dump(), stage="bible")
        self._write(self._dir(pid) / "project.json", pr)
        return bible

    def approve_bible(self, pid: str, actor: Actor, edited: Optional[Bible | dict] = None) -> Bible:
        pr = self.project(pid)
        before = self.bible(pid)
        bible = before
        if edited is not None:
            bible = edited if isinstance(edited, Bible) else Bible.model_validate(edited)
            ratio = proof.edit_ratio(canonical(before.model_dump()), canonical(bible.model_dump()))
            self._write(self._dir(pid) / "bible.json", bible)
            self._log(pid, "bible", "human_edit", actor, bible.model_dump(), stage="bible", edit_ratio=ratio)
        self._log(pid, "bible", "approve", actor, bible.model_dump(), stage="bible")
        pr.bible_approved = True
        self._write(self._dir(pid) / "project.json", pr)
        return bible

    # ── 파일럿 파이프라인 ─────────────────────────────────
    def new_pilot(self, pid: str, hook_variant: str, episodes: Optional[list[int]] = None) -> Pilot:
        p = Pilot(hook_variant=hook_variant, episodes=episodes or [1, 2, 3])
        self._save_pilot(pid, p)
        self._log(pid, f"{p.id}", "create", self.system, p.model_dump(), stage="pilot")
        return p

    def run(self, pid: str, plt: str) -> Pilot:
        """사람 승인이 필요한 지점이나 완료까지 진행한다."""
        pr = self.project(pid)
        if not pr.bible_approved:
            raise StudioError("바이블 승인이 먼저 필요합니다(approve_bible).")
        p = self.pilot(pid, plt)
        if p.pending_review:
            return p
        while p.stage != "done" and p.status != "blocked":
            stage = p.stage
            getattr(self, f"_stage_{stage}")(pid, p)
            self._save_pilot(pid, p)
            if p.status == "blocked":
                # 법적 차단: 모드와 무관하게 사람이 고쳐야 진행된다.
                p.pending_review = stage
                self._save_pilot(pid, p)
                return p
            gate = "script" if stage == "script" else stage
            if stage == "storyboard":
                gate = "edit"
            if self.policy(pid).requires_human(gate):
                p.pending_review = stage
                self._save_pilot(pid, p)
                return p
            self._log(pid, f"{p.id}/{stage}", "auto_approve", self.system, self._stage_content(p, stage), stage=stage)
            p.stage = self._next(stage)
            self._save_pilot(pid, p)
        if p.stage == "done" and p.status == "draft":
            p.status = "ready"
            self._save_pilot(pid, p)
        return p

    @staticmethod
    def _next(stage: str) -> str:
        return {"beats": "script", "script": "storyboard", "storyboard": "done"}[stage]

    @staticmethod
    def _stage_content(p: Pilot, stage: str):
        if stage == "beats":
            return p.beats.model_dump() if p.beats else {}
        if stage == "script":
            return [s.model_dump() for s in p.scenes]
        return p.render_plan or {}

    def _stage_beats(self, pid: str, p: Pilot) -> None:
        bible = self.bible(pid)
        bs = self.room.beats(bible, p.hook_variant, p.episodes)
        p.beats = bs
        pol = self.policy(pid)
        p.issues = continuity.check_beats(bible, bs.beats) if pol.on("continuity_check") else []
        self._log(pid, f"{p.id}/beats", "ai_draft", self.ai, bs.model_dump(), stage="beats")

    def _stage_script(self, pid: str, p: Pilot) -> None:
        bible = self.bible(pid)
        pol = self.policy(pid)
        scenes: list[Scene] = []
        prev = []
        for beat in p.beats.beats:
            ep = self.room.episode(bible, beat, prev, scenes[-1] if scenes else None)
            if pol.on("continuity_check"):
                errs = [i for i in continuity.check_script(bible, ep.scenes) if i.severity == "error"]
                if errs:  # 한 번 자동 수선
                    ep = self.room.repair(bible, ep.scenes, errs)
            scenes += ep.scenes
            prev.append(beat)
        p.scenes = scenes
        self._log(pid, f"{p.id}/script", "ai_draft", self.ai, [s.model_dump() for s in scenes], stage="script")
        self._qc(pid, p, bible, pol)

    def _qc(self, pid: str, p: Pilot, bible: Bible, pol: PolicyEngine) -> None:
        issues: list[Issue] = []
        if pol.on("continuity_check"):
            issues += continuity.check_script(bible, p.scenes)
            if getattr(self.provider, "name", "") != "offline" and os.environ.get("STORY8_SEMANTIC_CHECK") == "1":
                issues += continuity.semantic_check(self.provider, bible, p.scenes, bible_context(bible))
        p.ai_tell = aitell.analyze(p.scenes) if pol.on("ai_tell_check") else None
        s_issues, flags = safety.check(bible, p.scenes, str(pol.value("content_rating")))
        issues += s_issues
        p.rating = flags["estimated_rating"]
        p.render_plan = dict(p.render_plan or {}, safety=flags)
        p.issues = continuity.dedupe(issues)
        self._log(pid, f"{p.id}/script", "check", self.system,
                  {"issues": [i.model_dump() for i in p.issues], "ai_tell": p.ai_tell, "safety": flags}, stage="qc")
        if safety.blocking(p.issues):
            p.status = "blocked"
        elif p.status == "blocked":
            p.status = "draft"

    def _stage_storyboard(self, pid: str, p: Pilot) -> None:
        bible = self.bible(pid)
        sb = self.room.storyboard(bible, p.scenes)
        p.storyboard = sb
        flags = (p.render_plan or {}).get("safety", {})
        plan = media.render_plan(bible, sb, label_deepfake=flags.get("deepfake_visible_label_required", False))
        plan["safety"] = flags
        p.render_plan = plan
        self._log(pid, f"{p.id}/storyboard", "ai_draft", self.ai, sb.model_dump(), stage="storyboard")

    def approve(self, pid: str, plt: str, actor: Actor, edited: Optional[dict | list] = None,
                note: Optional[str] = None) -> Pilot:
        """사람 승인. edited 가 있으면 그 단계 산출물을 사람 수정본으로 바꾼다.
        beats: BeatSheet dict / script: Scene dict 목록 / storyboard: Storyboard dict."""
        if actor.kind != "human":
            raise StudioError("승인은 사람만 할 수 있습니다.")
        p = self.pilot(pid, plt)
        stage = p.pending_review
        if not stage:
            raise StudioError("승인 대기 중인 단계가 없습니다.")
        before = canonical(self._stage_content(p, stage))
        if edited is not None:
            if stage == "beats":
                p.beats = BeatSheet.model_validate(edited)
            elif stage == "script":
                p.scenes = [Scene.model_validate(s) for s in edited]
                pol = self.policy(pid)
                self._qc(pid, p, self.bible(pid), pol)
            elif stage == "storyboard":
                from .models import Storyboard
                p.storyboard = Storyboard.model_validate(edited)
                flags = (p.render_plan or {}).get("safety", {})
                p.render_plan = dict(media.render_plan(self.bible(pid), p.storyboard,
                                                       label_deepfake=flags.get("deepfake_visible_label_required", False)),
                                     safety=flags)
            after = canonical(self._stage_content(p, stage))
            self._log(pid, f"{p.id}/{stage}", "human_edit", actor, after, stage=stage,
                      edit_ratio=proof.edit_ratio(before, after), note=note)
        if p.status == "blocked":
            self._save_pilot(pid, p)
            raise StudioError("법적 차단 항목이 남아 있어 승인할 수 없습니다: "
                              + "; ".join(i.message for i in safety.blocking(p.issues)))
        self._log(pid, f"{p.id}/{stage}", "approve", actor, self._stage_content(p, stage), stage=stage, note=note)
        p.pending_review = None
        p.stage = self._next(stage)
        self._save_pilot(pid, p)
        return self.run(pid, plt)

    # ── 평가·승격 ─────────────────────────────────────────
    def add_rating(self, pid: str, r: PanelRating | dict) -> None:
        r = r if isinstance(r, PanelRating) else PanelRating.model_validate(r)
        with (self._dir(pid) / "ratings.jsonl").open("a", encoding="utf-8") as f:
            f.write(r.model_dump_json() + "\n")

    def add_ab(self, pid: str, r: ABResult | dict) -> None:
        r = r if isinstance(r, ABResult) else ABResult.model_validate(r)
        with (self._dir(pid) / "ab.jsonl").open("a", encoding="utf-8") as f:
            f.write(r.model_dump_json() + "\n")

    def _jsonl(self, pid: str, name: str, model):
        f = self._dir(pid) / name
        if not f.exists():
            return []
        return [model.model_validate_json(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]

    def evaluate(self, pid: str, top_fraction: float = 0.25) -> list[dict]:
        ids = [p.id for p in self.pilots(pid) if p.status in ("ready", "published", "promoted")]
        board = leaderboard(ids, self._jsonl(pid, "ratings.jsonl", PanelRating),
                            self._jsonl(pid, "ab.jsonl", ABResult), top_fraction)
        self._log(pid, "evaluation", "check", self.system, board, stage="evaluation")
        return board

    def promote(self, pid: str, plt: str, actor: Actor, name: Optional[str] = None) -> Project:
        """자동 모드 파일럿을 협업 모드 프로젝트로 승격. 새 원장에서 승격 이후 기여만 기록한다."""
        src = self.project(pid)
        p = self.pilot(pid, plt)
        src_head = self.ledger(pid).head
        new = self.create_project(name or f"{src.name} (협업)", Mode.COLLAB, brand=src.brand, actor=actor)
        new.promoted_from = pid
        self._write(self._dir(new.id) / "project.json", new)
        bible = self.bible(pid)
        self._write(self._dir(new.id) / "bible.json", bible)
        self._log(new.id, "project", "promote", actor,
                  {"from_project": pid, "from_pilot": plt, "from_ledger_head": src_head},
                  stage="promote", recorded=False,
                  note="승격 이전 작업은 AI 생성으로 간주하며 인간 기여로 소급 인정하지 않는다.")
        # 바이블은 AI 산출물로 넘어오므로 협업 모드 바이블 승인을 다시 받는다.
        self._log(new.id, "bible", "ai_draft", self.ai, bible.model_dump(), stage="bible", recorded=False)
        new = self.project(new.id)
        new.bible_source = "ai"
        new.bible_approved = not PolicyEngine(new.mode, new.settings).requires_human("bible")
        self._write(self._dir(new.id) / "project.json", new)
        carried = Pilot(hook_variant=p.hook_variant, episodes=p.episodes, stage="beats", beats=p.beats)
        if p.beats:
            carried.pending_review = "beats"
        self._save_pilot(new.id, carried)
        self._log(new.id, carried.id, "create", self.system, carried.model_dump(), stage="pilot", recorded=False)
        p.status = "promoted"
        self._save_pilot(pid, p)
        self._log(pid, p.id, "promote", actor, {"to_project": new.id}, stage="promote", recorded=False)
        return self.project(new.id)

    # ── 증명·내보내기 ─────────────────────────────────────
    def certificate(self, pid: str) -> dict:
        pr = self.project(pid)
        return proof.certificate(self.ledger(pid), pid, pr.name, secret=self.secret)

    def export(self, pid: str, plt: str, kind: str = "platform", out: Optional[Path] = None) -> dict:
        from .export import build_package
        return build_package(self, pid, plt, kind, out)
