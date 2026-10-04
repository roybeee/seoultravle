"""잠금(법적 의무) 안전 검사. 사용자 설정으로 끌 수 없다.

- 아동·청소년 성적 표현 차단(청소년성보호법)
- 실존 인물(퍼블리시티) 무단 이용 차단(부정경쟁방지법 타목) — 동의 기록이 있으면 허용
- 콘텐츠 강도 추정과 설정 등급 초과 차단, 19 등급이면 연령 확인 의무 표시
- 실존 인물처럼 보이는 합성물은 가시적 표시 의무 표시

키워드 기반 1차 필터다. 상용 서비스에서는 전용 분류 모델과 사람 검수를 함께 써야 한다.
"""

from __future__ import annotations

from .models import Bible, Issue, Scene

MINOR_WORDS = ("미성년", "초등학생", "중학생", "고등학생", "고딩", "중딩", "아동", "어린이", "소녀 교복", "여고생", "남고생")
SEXUAL_WORDS = ("성관계", "섹스", "알몸", "나체", "애무", "성적", "야한", "벗기", "침대에서 뒤엉")
VIOLENCE_STRONG = ("난도질", "참수", "토막", "피가 솟", "내장", "고문")
VIOLENCE = ("피", "칼", "총", "폭행", "때리", "살해", "죽여", "흉기")
DRUG = ("마약", "필로폰", "대마", "코카인")
PROFANITY = ("씨발", "시발", "개새끼", "좆", "병신", "지랄")

RANK = {"전체": 0, "15": 1, "19": 2}


def estimate_rating(text: str) -> tuple[str, list[str]]:
    reasons = []
    level = 0
    if any(w in text for w in SEXUAL_WORDS):
        level = 2; reasons.append("성적 표현")
    if any(w in text for w in VIOLENCE_STRONG):
        level = 2; reasons.append("잔혹한 폭력")
    if any(w in text for w in DRUG):
        level = max(level, 2); reasons.append("마약 묘사")
    if level < 2 and any(w in text for w in VIOLENCE):
        level = max(level, 1); reasons.append("폭력 묘사")
    if any(w in text for w in PROFANITY):
        level = max(level, 1); reasons.append("욕설")
    return ({0: "전체", 1: "15", 2: "19"}[level], reasons)


def _minor_names(bible: Bible) -> set[str]:
    out = set()
    for c in bible.characters:
        age = bible.age_of(c)
        if age is not None and age < 19:
            out.add(c.name)
    return out


def check(bible: Bible, scenes: list[Scene], allowed_rating: str) -> tuple[list[Issue], dict]:
    issues: list[Issue] = []
    minors = _minor_names(bible)
    for sc in scenes:
        t = sc.text()
        sexual = any(w in t for w in SEXUAL_WORDS)
        minor = any(w in t for w in MINOR_WORDS) or any(n in t for n in minors)
        if sexual and minor:
            issues.append(Issue(severity="block", code="csam_block", episode=sc.episode,
                                message="미성년자(또는 미성년으로 보이는 인물)와 성적 표현이 함께 나옵니다. "
                                        "생성을 차단합니다(법적 의무, 끌 수 없음)."))
    full = "\n".join(s.text() for s in scenes)
    rating, reasons = estimate_rating(full)
    if RANK[rating] > RANK.get(allowed_rating, 1):
        issues.append(Issue(severity="error", code="rating_exceeded",
                            message=f"추정 등급 {rating}({', '.join(reasons)})이 설정 등급 {allowed_rating}을 넘습니다."))

    real = [c for c in bible.characters if c.real_person]
    for c in real:
        if c.attributes.get("publicity_consent", "").lower() not in ("yes", "y", "true", "동의"):
            if any(c.name in s.text() for s in scenes):
                issues.append(Issue(severity="block", code="publicity_block",
                                    message=f"실존 인물 '{c.name}'의 동의 기록(attributes.publicity_consent)이 없습니다. "
                                            "성명·초상·음성의 상업 이용을 차단합니다."))
    flags = {
        "estimated_rating": rating,
        "rating_reasons": reasons,
        "adult_age_verification_required": rating == "19",
        "deepfake_visible_label_required": bool(real),
        "real_persons": [c.name for c in real],
    }
    return issues, flags


def blocking(issues: list[Issue]) -> list[Issue]:
    return [i for i in issues if i.severity == "block"]
