"""도메인 모델: 캐논 바이블, 비트·장면, 파일럿, 프로젝트."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class Mode(str, Enum):
    AUTO = "auto"  # 자동 모드: 사람 개입 없이 생성
    COLLAB = "collab"  # 협업 모드: 단계별 사람 결정·승인


class Actor(BaseModel):
    """기여자. kind=human 이면 사람, ai 이면 모델."""

    kind: str  # "human" | "ai" | "system"
    id: str  # 사용자 id 또는 모델 이름

    @property
    def label(self) -> str:
        return f"{self.kind}:{self.id}"


# ── 캐논 바이블 ─────────────────────────────────────────────


class LifeEvent(BaseModel):
    age: int
    description: str


class Character(BaseModel):
    id: str = Field(default_factory=lambda: new_id("chr"))
    name: str
    birth_year: Optional[int] = None
    gender: Optional[str] = None
    nationality: Optional[str] = None
    occupation: Optional[str] = None
    traits: list[str] = Field(default_factory=list)  # 성향·습관
    appearance: Optional[str] = None
    speech_style: Optional[str] = None  # 말투
    backstory: Optional[str] = None  # 前事
    life_events: list[LifeEvent] = Field(default_factory=list)  # 연령별 주요 사건
    attributes: dict[str, str] = Field(default_factory=dict)  # 키·체중·질병 등 고정 속성
    deceased_in_story_year: Optional[int] = None  # 극중 사망 연도(이후 등장 금지)
    real_person: bool = False  # 실존 인물 모델링 여부(퍼블리시티권 검토 대상)


class Place(BaseModel):
    id: str = Field(default_factory=lambda: new_id("plc"))
    name: str
    description: Optional[str] = None


class Relation(BaseModel):
    source: str  # character id
    target: str  # character id
    kind: str  # 가족·연인·적대·스승 등
    note: Optional[str] = None


class WorldRule(BaseModel):
    id: str = Field(default_factory=lambda: new_id("rul"))
    text: str


class Bible(BaseModel):
    """캐논 바이블: 인간 작가가 결정하는 설정의 단일 원천."""

    title: str
    logline: str
    genre: str
    story_year: int  # 극중 현재 연도
    tone: Optional[str] = None
    target_rating: str = "15"  # 전체 | 15 | 19
    characters: list[Character] = Field(default_factory=list)
    places: list[Place] = Field(default_factory=list)
    relations: list[Relation] = Field(default_factory=list)
    rules: list[WorldRule] = Field(default_factory=list)
    ng_list: list[str] = Field(default_factory=list)  # 금칙(쓰면 안 되는 표현·전개)

    def character(self, ref: str) -> Optional[Character]:
        for c in self.characters:
            if c.id == ref or c.name == ref:
                return c
        return None

    def age_of(self, ch: Character, year: Optional[int] = None) -> Optional[int]:
        if ch.birth_year is None:
            return None
        return (year or self.story_year) - ch.birth_year


# ── 작가실 산출물 ───────────────────────────────────────────


class Beat(BaseModel):
    episode: int
    summary: str
    characters: list[str] = Field(default_factory=list)  # 등장 인물 이름
    hook: Optional[str] = None  # 회차 끝 클리프행어


class BeatSheet(BaseModel):
    beats: list[Beat]


class DialogueLine(BaseModel):
    speaker: str
    line: str


class Scene(BaseModel):
    episode: int
    heading: str  # 장소·시간
    action: str  # 지문
    dialogue: list[DialogueLine] = Field(default_factory=list)

    def text(self) -> str:
        lines = [self.heading, self.action]
        lines += [f"{d.speaker}: {d.line}" for d in self.dialogue]
        return "\n".join(lines)


class Shot(BaseModel):
    episode: int
    index: int
    description: str  # 화면 묘사(영상 생성 프롬프트의 원천)
    characters: list[str] = Field(default_factory=list)
    duration_sec: float = 4.0
    camera: Optional[str] = None


class Storyboard(BaseModel):
    shots: list[Shot]


class EpisodeScript(BaseModel):
    scenes: list[Scene]


# ── 파일럿·평가 ─────────────────────────────────────────────


class Issue(BaseModel):
    severity: str  # error | warning | info
    code: str
    message: str
    episode: Optional[int] = None


class Pilot(BaseModel):
    id: str = Field(default_factory=lambda: new_id("plt"))
    hook_variant: str  # 예: "복수 선언 훅", "로맨스 훅"
    episodes: list[int] = Field(default_factory=lambda: [1, 2, 3])
    stage: str = "beats"  # beats | script | storyboard | done
    pending_review: Optional[str] = None  # 사람 승인을 기다리는 단계
    beats: Optional[BeatSheet] = None
    scenes: list[Scene] = Field(default_factory=list)
    storyboard: Optional[Storyboard] = None
    render_plan: Optional[dict] = None
    issues: list[Issue] = Field(default_factory=list)
    ai_tell: Optional[dict] = None
    rating: Optional[str] = None
    status: str = "draft"  # draft | ready | published | promoted | archived


class PanelRating(BaseModel):
    """비공개 독자단 블라인드 평가(1~5)."""

    rater: str
    pilot_id: str
    completion_intent: int = Field(ge=1, le=5)
    rewatch: int = Field(ge=1, le=5)
    recommend: int = Field(ge=1, le=5)
    dropoff_episode: Optional[int] = None


class ABResult(BaseModel):
    """동일 노출 A/B 집계."""

    pilot_id: str
    impressions: int
    completions: int  # 3화 완주
    follows: int = 0


class Project(BaseModel):
    id: str = Field(default_factory=lambda: new_id("prj"))
    name: str
    mode: Mode = Mode.COLLAB
    settings: dict[str, bool | str] = Field(default_factory=dict)
    created_at: str = Field(default_factory=utcnow)
    promoted_from: Optional[str] = None  # 자동 모드에서 승격된 원 프로젝트 id
    brand: Optional[str] = None  # 협업 모드 작품에 붙일 스튜디오 브랜드
    bible_approved: bool = False
    bible_source: Optional[str] = None  # human | ai
