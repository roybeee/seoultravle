from story8 import aitell, continuity, safety
from story8.models import DialogueLine, Scene


def sc(heading, action, lines, ep=1):
    return Scene(episode=ep, heading=heading, action=action,
                 dialogue=[DialogueLine(speaker=s, line=l) for s, l in lines])


def codes(issues):
    return {i.code for i in issues}


def test_deceased_speaker_flagged_unless_flashback(bible):
    s = sc("S#1. 연습실 - 밤", "서윤이 건반 앞에 앉는다.", [("한미경", "다시 쳐 봐.")])
    assert "deceased_speaks" in codes(continuity.check_scene(bible, s))
    s2 = sc("S#1. 연습실 - 밤 (회상)", "어린 서윤.", [("한미경", "다시 쳐 봐.")])
    assert "deceased_speaks" not in codes(continuity.check_scene(bible, s2))


def test_age_attribute_ng_unknown(bible):
    s = sc("S#2. 리허설룸 - 낮", "한서윤은 올해 35살이다. 도현우의 키는 170cm 정도로 보인다. 그날의 기억상실.",
           [("낯선남자", "누구시죠?")])
    c = codes(continuity.check_scene(bible, s))
    assert {"age_mismatch", "attribute_mismatch", "ng_word", "unknown_speaker"} <= c


def test_world_rule(bible):
    s = sc("S#3. 홀 - 밤", "서윤은 타임슬립으로 5년 전으로 돌아간다.", [])
    assert "world_rule" in codes(continuity.check_scene(bible, s))


def test_clean_scene_has_no_errors(bible):
    s = sc("S#1. 성수동 지하 연습실 - 새벽", "서윤이 왼손으로만 건반을 누른다. 현우가 문가에 기대 서 있다.",
           [("한서윤", "...보고 계셨어요?"), ("도현우", "응. 아니, 네. 다 봤습니다.")])
    assert not [i for i in continuity.check_scene(bible, s) if i.severity == "error"]


def test_aitell_detects_monotone():
    mono = [sc("S#1", " ".join(["그녀는 숨을 삼켰다. 묘한 기분이 들었다. 정적이 흘렀다."] * 5),
               [("A", "그래요."), ("B", "그래요.")])]
    varied = [sc("S#1", "문이 열린다. 비에 젖은 남자가 들어와 아무 말 없이 서류를 내민다. 서윤, 받지 않는다.",
                 [("A", "늦었네."), ("B", "차가 막혔다니까? 너 진짜 그렇게 나올 거야?")])]
    assert aitell.analyze(mono)["score"] > aitell.analyze(varied)["score"]
    assert aitell.analyze(mono)["level"] in ("medium", "high")


def test_safety_blocks_minor_sexual_and_rating(bible):
    s = sc("S#1", "고등학생 인물과 성관계 묘사", [])
    issues, flags = safety.check(bible, [s], "19")
    assert "csam_block" in codes(issues)
    s2 = sc("S#1", "남자가 칼로 위협하고 폭행한다. 마약 거래.", [])
    issues, flags = safety.check(bible, [s2], "15")
    assert "rating_exceeded" in codes(issues) and flags["adult_age_verification_required"]


def test_publicity_block_needs_consent(bible):
    real = bible.characters[1].model_copy(update={"real_person": True})
    b = bible.model_copy(update={"characters": [bible.characters[0], real]})
    s = sc("S#1", "도현우가 웃는다.", [])
    issues, flags = safety.check(b, [s], "15")
    assert "publicity_block" in codes(issues) and flags["deepfake_visible_label_required"]
    real.attributes["publicity_consent"] = "yes"
    issues, _ = safety.check(b, [s], "15")
    assert "publicity_block" not in codes(issues)
