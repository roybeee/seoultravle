import pytest

from story8.models import Mode
from story8.policy import LOCKED, PolicyEngine, PolicyError


def test_locked_cannot_be_disabled():
    pol = PolicyEngine(Mode.AUTO)
    for r in LOCKED:
        with pytest.raises(PolicyError):
            pol.set(r.key, False)
        assert pol.on(r.key)


def test_mode_defaults():
    auto, collab = PolicyEngine(Mode.AUTO), PolicyEngine(Mode.COLLAB)
    assert not auto.requires_human("script") and collab.requires_human("script")
    assert not auto.on("contribution_record") and collab.on("contribution_record")
    assert auto.on("continuity_check") and collab.on("continuity_check")


def test_toggle_off_gives_notice_and_validates():
    pol = PolicyEngine(Mode.COLLAB)
    n = pol.set("approve_script", False)
    assert n and "확정" in n.message
    assert not pol.requires_human("script")
    with pytest.raises(PolicyError):
        pol.set("content_rating", "18")
    with pytest.raises(PolicyError):
        pol.set("approve_beats", "yes")
    pol.set("content_rating", "19")
    assert pol.value("content_rating") == "19"
