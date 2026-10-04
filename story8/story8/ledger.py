"""권리 원장: 추가만 가능한 해시 체인.

각 이벤트는 직전 이벤트의 해시를 포함하므로 중간 기록을 고치면 검증이 깨진다.
타임스탬프는 기본적으로 로컬 시계를 쓰며, 운영 환경에서는 RFC 3161 TSA 로 교체할 수 있다(TimestampAuthority).
"""

from __future__ import annotations

import hashlib
import hmac
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Protocol

from pydantic import BaseModel

from .models import Actor, utcnow

GENESIS = "0" * 64


def sha256(data: str | bytes) -> str:
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def canonical(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


class TimestampAuthority(Protocol):
    def stamp(self, digest: str) -> dict: ...


class LocalTimestamp:
    """개발용 타임스탬프. HMAC 서명으로 위·변조를 탐지한다(법적 시점 증명은 TSA 사용)."""

    def __init__(self, secret: str = "story8-dev-secret"):
        self.secret = secret.encode()

    def stamp(self, digest: str) -> dict:
        t = utcnow()
        sig = hmac.new(self.secret, f"{digest}|{t}".encode(), hashlib.sha256).hexdigest()
        return {"authority": "local-hmac", "time": t, "signature": sig}

    def verify(self, digest: str, token: dict) -> bool:
        sig = hmac.new(self.secret, f"{digest}|{token['time']}".encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(sig, token["signature"])


class LedgerEvent(BaseModel):
    seq: int
    subject: str  # 대상: bible | character:<id> | beats | scene:<ep> | pilot:<id> ...
    action: str  # create | ai_draft | human_edit | approve | auto_approve | check | export | promote
    actor: Actor
    content_hash: str  # 내용 자체 대신 해시만 저장
    detail: dict = {}
    prev_hash: str
    timestamp: dict
    hash: str = ""

    def body(self) -> dict:
        d = self.model_dump(exclude={"hash"})
        return d


class Ledger:
    def __init__(self, path: Optional[Path] = None, tsa: Optional[TimestampAuthority] = None):
        self.path = path
        self.tsa = tsa or LocalTimestamp()
        self.events: list[LedgerEvent] = []
        if path and path.exists():
            for line in path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    self.events.append(LedgerEvent.model_validate_json(line))

    @property
    def head(self) -> str:
        return self.events[-1].hash if self.events else GENESIS

    def append(self, subject: str, action: str, actor: Actor, content: str | dict,
               detail: Optional[dict] = None) -> LedgerEvent:
        content_hash = sha256(content if isinstance(content, str) else canonical(content))
        ev = LedgerEvent(
            seq=len(self.events), subject=subject, action=action, actor=actor,
            content_hash=content_hash, detail=detail or {}, prev_hash=self.head,
            timestamp=self.tsa.stamp(content_hash),
        )
        ev.hash = sha256(canonical(ev.body()))
        self.events.append(ev)
        if self.path:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("a", encoding="utf-8") as f:
                f.write(ev.model_dump_json() + "\n")
        return ev

    def verify(self) -> tuple[bool, list[str]]:
        errors: list[str] = []
        prev = GENESIS
        for i, ev in enumerate(self.events):
            if ev.seq != i:
                errors.append(f"#{i}: 순번 불일치")
            if ev.prev_hash != prev:
                errors.append(f"#{i}: 이전 해시 불일치(체인 단절)")
            if sha256(canonical(ev.body())) != ev.hash:
                errors.append(f"#{i}: 이벤트 내용이 변조됨")
            if isinstance(self.tsa, LocalTimestamp) and ev.timestamp.get("authority") == "local-hmac":
                if not self.tsa.verify(ev.content_hash, ev.timestamp):
                    errors.append(f"#{i}: 타임스탬프 서명 불일치")
            prev = ev.hash
        return (not errors, errors)

    def for_subject(self, prefix: str) -> list[LedgerEvent]:
        return [e for e in self.events if e.subject.startswith(prefix)]
