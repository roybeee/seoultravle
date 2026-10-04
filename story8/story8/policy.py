"""정책 엔진: 법적 의무는 잠그고, 그 외 기능은 사용자가 켜고 끈다.

잠금 항목은 사용자 설정으로 우회할 수 없다. 법이 바뀌면 이 파일의 LOCKED 만 고친다.
법률 자문이 아니며, 출시 전 변호사 검토가 필요하다.
"""

from __future__ import annotations

from dataclasses import dataclass

from .models import Mode


@dataclass(frozen=True)
class LockedRule:
    key: str
    title: str
    basis: str


@dataclass(frozen=True)
class Toggle:
    key: str
    title: str
    default_auto: bool | str
    default_collab: bool | str
    consequence_off: str  # 끌 때 한 번 안내하는 결과
    choices: tuple[str, ...] = ()


LOCKED: tuple[LockedRule, ...] = (
    LockedRule("ai_service_notice", "AI 기반 서비스 사전 고지", "인공지능기본법 제31조(2026-01-22 시행)"),
    LockedRule("ai_output_label", "결과물 AI 생성 표시(서비스 내 표시, 반출 시 메타데이터·워터마크)",
               "인공지능기본법 제31조, 과기정통부 AI 투명성 확보 가이드라인"),
    LockedRule("deepfake_visible_label", "실존 인물처럼 보이는 합성물의 가시적 표시", "AI 투명성 확보 가이드라인"),
    LockedRule("eu_transparency", "EU 배포 시 AI 생성·상호작용 고지", "EU AI Act 제50조(2026-08-02 적용)"),
    LockedRule("csam_block", "아동·청소년 성착취물 생성 차단", "청소년성보호법 제11조"),
    LockedRule("adult_age_verification", "성인 등급 콘텐츠 제공 시 연령 확인", "청소년보호법 제16조"),
    LockedRule("publicity_block", "유명인 성명·초상·음성의 무단 상업 이용 차단",
               "부정경쟁방지법 제2조 제1호 타목"),
)

TOGGLES: tuple[Toggle, ...] = (
    Toggle("contribution_record", "인간 기여 기록(S8 Proof)", False, True,
           "저작권 등록·납품 권리보증에 쓸 증빙이 남지 않습니다."),
    Toggle("contribution_grade_display", "인간 기여 등급 외부 표시", False, False,
           "결과물에 인간 기여 등급을 표시하지 않습니다(AI 생성 표시는 유지)."),
    Toggle("approve_bible", "바이블 사람 승인", False, True, "AI가 바이블 보완을 자동 확정합니다."),
    Toggle("approve_beats", "비트 사람 승인", False, True, "AI가 비트 시트를 자동 확정합니다."),
    Toggle("approve_script", "대본 사람 승인", False, True, "AI 대본이 수정 없이 확정됩니다."),
    Toggle("approve_edit", "최종 편집 사람 승인", False, True, "최종 결과물이 사람 검수 없이 확정됩니다."),
    Toggle("continuity_check", "연속성 검증기", True, True, "설정 모순을 검사하지 않습니다."),
    Toggle("ai_tell_check", "'AI 티' 역검출", True, True, "단조로운 문체·일관성 붕괴 경고가 없습니다."),
    Toggle("delivery_export_warning", "납품용 내보내기 경고", True, True,
           "기여 기록이 없는 작품도 경고 없이 납품 양식으로 내보냅니다."),
    Toggle("brand_separation", "브랜드 분리", True, True,
           "자동 모드 결과물에도 지정 브랜드가 붙을 수 있습니다."),
    Toggle("training_opt_in", "학습 데이터 제공", False, False, ""),
    Toggle("content_rating", "유해 콘텐츠 강도", "15", "15", "", choices=("전체", "15", "19")),
)

_TOGGLE_MAP = {t.key: t for t in TOGGLES}
_LOCKED_MAP = {r.key: r for r in LOCKED}


class PolicyError(ValueError):
    pass


def default_settings(mode: Mode) -> dict[str, bool | str]:
    return {t.key: (t.default_auto if mode == Mode.AUTO else t.default_collab) for t in TOGGLES}


@dataclass
class Notice:
    key: str
    message: str


class PolicyEngine:
    def __init__(self, mode: Mode, settings: dict[str, bool | str] | None = None):
        self.mode = mode
        self.settings = default_settings(mode)
        self.notices: list[Notice] = []
        for k, v in (settings or {}).items():
            self.set(k, v, record_notice=False)

    def is_locked(self, key: str) -> bool:
        return key in _LOCKED_MAP

    def set(self, key: str, value: bool | str, record_notice: bool = True) -> Notice | None:
        if key in _LOCKED_MAP:
            r = _LOCKED_MAP[key]
            raise PolicyError(f"'{r.title}'은(는) 법적 의무라 끌 수 없습니다. 근거: {r.basis}")
        if key not in _TOGGLE_MAP:
            raise PolicyError(f"알 수 없는 설정: {key}")
        t = _TOGGLE_MAP[key]
        if t.choices:
            if value not in t.choices:
                raise PolicyError(f"{t.title}: {t.choices} 중 하나여야 합니다.")
        elif not isinstance(value, bool):
            raise PolicyError(f"{t.title}: on/off(bool) 값이어야 합니다.")
        self.settings[key] = value
        notice = None
        if record_notice and value is False and t.consequence_off:
            notice = Notice(key, t.consequence_off)
            self.notices.append(notice)
        return notice

    def on(self, key: str) -> bool:
        if key in _LOCKED_MAP:
            return True
        return bool(self.settings.get(key))

    def value(self, key: str):
        return self.settings.get(key)

    def requires_human(self, stage: str) -> bool:
        """stage: bible | beats | script | edit"""
        if self.mode == Mode.AUTO:
            return False
        return self.on(f"approve_{stage}")

    def describe(self) -> dict:
        return {
            "mode": self.mode.value,
            "locked": [{"key": r.key, "title": r.title, "basis": r.basis} for r in LOCKED],
            "toggles": [
                {"key": t.key, "title": t.title, "value": self.settings[t.key],
                 "choices": list(t.choices) or None}
                for t in TOGGLES
            ],
        }
