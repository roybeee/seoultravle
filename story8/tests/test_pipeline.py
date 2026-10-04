import json

import pytest

from story8.models import Mode
from story8.proof import verify_certificate
from story8.studio import StudioError


def test_auto_mode_runs_without_humans(studio):
    pr = studio.create_project("자동 실험", Mode.AUTO)
    studio.generate_bible(pr.id, "기억을 파는 전당포", "미스터리")
    p = studio.new_pilot(pr.id, "미스터리 훅")
    p = studio.run(pr.id, p.id)
    assert p.stage == "done" and p.status == "ready" and p.pending_review is None
    assert p.storyboard and p.render_plan["estimate_usd"]["generation"] > 0
    out = studio.export(pr.id, p.id, "delivery")
    assert "s8proof.json" not in out["files"]  # 자동 모드 기본: 기여 기록 꺼짐
    assert any("기여 기록" in w for w in out["warnings"])
    assert out["brand"].startswith("STORY8 Lab")
    assert "AI로 생성" in out["disclosure"]["ko"]
    ok, errors = studio.ledger(pr.id).verify()
    assert ok, errors


def test_collab_mode_gates_and_grade(studio, bible, writer):
    pr = studio.create_project("다시, 왼손", Mode.COLLAB, brand="채널옥트")
    studio.import_bible(pr.id, bible, writer)
    p = studio.new_pilot(pr.id, "복수 선언 훅")
    p = studio.run(pr.id, p.id)
    assert p.pending_review == "beats" and p.stage == "beats"
    with pytest.raises(StudioError):
        studio.export(pr.id, p.id)
    p = studio.approve(pr.id, p.id, writer)
    assert p.pending_review == "script"
    # 사람이 대본을 크게 고친다
    edited = [s.model_dump() for s in p.scenes]
    for s in edited:
        s["action"] = "서윤이 왼손으로만 쇼팽을 친다. 현우는 박수 대신 만년필 뚜껑을 닫는다. 비가 그친다."
        s["dialogue"] = [{"speaker": "한서윤", "line": "끝까지 들으셨네요."},
                         {"speaker": "도현우", "line": "그날 계단에서, 나 너 봤어. 이제야 말하는 거 미안합니다."}]
    p = studio.approve(pr.id, p.id, writer, edited, note="대사 전면 수정")
    assert p.pending_review == "storyboard"
    p = studio.approve(pr.id, p.id, writer)
    assert p.stage == "done" and p.status == "ready"
    cert = studio.certificate(pr.id)
    assert cert["grade"] == "A" and cert["ledger_verified"]
    assert verify_certificate(cert, "test-secret")
    out = studio.export(pr.id, p.id, "delivery")
    assert "s8proof.json" in out["files"] and out["brand"] == "채널옥트"
    assert "contribution_grade" not in out["disclosure"]  # 등급 표시는 기본 꺼짐
    studio.set_setting(pr.id, "contribution_grade_display", True)
    out = studio.export(pr.id, p.id, "delivery")
    assert out["disclosure"]["contribution_grade"] == "A"


def test_approval_only_gives_grade_c(studio, writer):
    pr = studio.create_project("선택만", Mode.COLLAB)
    studio.generate_bible(pr.id, "로그라인", "로맨스")
    with pytest.raises(StudioError):
        studio.run(pr.id, studio.new_pilot(pr.id, "로맨스 훅").id)
    studio.approve_bible(pr.id, writer)
    p = studio.pilots(pr.id)[0]
    studio.run(pr.id, p.id)
    for _ in range(3):
        p = studio.approve(pr.id, p.id, writer)
    assert p.stage == "done"
    assert studio.certificate(pr.id)["grade"] == "C"


def test_toggle_off_contribution_no_retroactive(studio, bible, writer):
    pr = studio.create_project("기록 끔", Mode.COLLAB)
    studio.set_setting(pr.id, "contribution_record", False)
    studio.import_bible(pr.id, bible, writer)
    p = studio.new_pilot(pr.id, "훅")
    studio.run(pr.id, p.id)
    studio.approve(pr.id, p.id, writer)
    # 나중에 다시 켜도 앞선 사람 작업은 인정되지 않는다
    studio.set_setting(pr.id, "contribution_record", True)
    assert studio.certificate(pr.id)["grade"] == "D"


def test_collab_with_gates_off_runs_through(studio, bible, writer):
    pr = studio.create_project("게이트 끔", Mode.COLLAB)
    for k in ("approve_beats", "approve_script", "approve_edit"):
        studio.set_setting(pr.id, k, False)
    studio.import_bible(pr.id, bible, writer)
    p = studio.run(pr.id, studio.new_pilot(pr.id, "훅").id)
    assert p.stage == "done"
    assert studio.certificate(pr.id)["grade"] == "C"  # 사람 바이블만 있음, 편집 없음


def test_promote_auto_to_collab(studio, writer):
    pr = studio.create_project("자동", Mode.AUTO)
    studio.generate_bible(pr.id, "로그라인", "복수")
    pilots = [studio.new_pilot(pr.id, h) for h in ("복수 훅", "로맨스 훅", "미스터리 훅", "복수 훅 B")]
    for p in pilots:
        studio.run(pr.id, p.id)
    for i, p in enumerate(pilots):
        studio.add_ab(pr.id, {"pilot_id": p.id, "impressions": 1000, "completions": 100 + i * 60})
        studio.add_rating(pr.id, {"rater": "r1", "pilot_id": p.id, "completion_intent": 2 + i % 4,
                                  "rewatch": 3, "recommend": 3})
    board = studio.evaluate(pr.id)
    winners = [r for r in board if r["promote"]]
    assert len(winners) == 1 and winners[0]["pilot_id"] == pilots[3].id
    new = studio.promote(pr.id, winners[0]["pilot_id"], writer)
    assert new.mode == Mode.COLLAB and new.promoted_from == pr.id
    assert not new.bible_approved
    assert studio.certificate(new.id)["grade"] == "D"  # 승격 직후: 소급 인정 없음
    studio.approve_bible(new.id, writer)
    carried = studio.pilots(new.id)[0]
    assert carried.pending_review == "beats"
    studio.approve(new.id, carried.id, writer)
    assert studio.certificate(new.id)["grade"] == "C"
    assert studio.pilot(pr.id, winners[0]["pilot_id"]).status == "promoted"


def test_blocked_content_requires_human_fix(studio, bible, writer):
    pr = studio.create_project("차단", Mode.AUTO)
    b = bible.model_copy(deep=True)
    b.characters[1].real_person = True  # 동의 없는 실존 인물
    studio.import_bible(pr.id, b, writer)
    p = studio.run(pr.id, studio.new_pilot(pr.id, "훅").id)
    assert p.status == "blocked" and p.pending_review == "script"
    with pytest.raises(StudioError):
        studio.approve(pr.id, p.id, writer)
    name = b.characters[1].name
    edited = []
    for s in p.scenes:
        d = s.model_dump()
        d["action"] = d["action"].replace(name, "남자")
        d["dialogue"] = [x for x in d["dialogue"] if x["speaker"] != name]
        for x in d["dialogue"]:
            x["line"] = x["line"].replace(name, "당신")
        edited.append(d)
    p = studio.approve(pr.id, p.id, writer, edited)
    assert p.status != "blocked" and p.stage == "done"


def test_ledger_tamper_detected(studio, bible, writer):
    pr = studio.create_project("변조", Mode.COLLAB)
    studio.import_bible(pr.id, bible, writer)
    path = studio._dir(pr.id) / "ledger.jsonl"
    lines = path.read_text(encoding="utf-8").splitlines()
    ev = json.loads(lines[-1]); ev["actor"]["id"] = "someone-else"
    lines[-1] = json.dumps(ev, ensure_ascii=False)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    ok, errors = studio.ledger(pr.id).verify()
    assert not ok and errors
