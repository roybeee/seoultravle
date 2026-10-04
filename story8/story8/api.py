"""HTTP API + 웹 스튜디오.

실행: story8 serve  (또는 uvicorn story8.api:app)
사람 작가 식별: 요청 헤더 X-Story8-User. STORY8_API_TOKEN 을 설정하면 Authorization: Bearer 토큰을 요구한다.
"""

from __future__ import annotations

import os
from importlib import resources
from typing import Any, Optional

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

from .llm import LLMError, provider_from_env
from .models import Actor, Bible, Mode
from .policy import LOCKED, TOGGLES, PolicyError
from .studio import Studio, StudioError

app = FastAPI(title="STORY 8 SHORTS", version="0.1.0")
_studio: Optional[Studio] = None


def studio() -> Studio:
    global _studio
    if _studio is None:
        _studio = Studio(os.environ.get("STORY8_HOME", "story8-workspace"), provider_from_env())
    return _studio


def set_studio(s: Studio) -> None:
    global _studio
    _studio = s


def auth(authorization: Optional[str] = Header(None)):
    token = os.environ.get("STORY8_API_TOKEN")
    if token and authorization != f"Bearer {token}":
        raise HTTPException(401, "인증 실패")


def human(x_story8_user: Optional[str] = Header(None)) -> Actor:
    return Actor(kind="human", id=x_story8_user or "anonymous")


@app.exception_handler(StudioError)
@app.exception_handler(PolicyError)
@app.exception_handler(ValueError)
async def _bad(_: Request, e: Exception):
    return JSONResponse({"detail": str(e)}, status_code=400)


@app.exception_handler(LLMError)
async def _llm(_: Request, e: Exception):
    return JSONResponse({"detail": f"LLM 오류: {e}"}, status_code=502)


@app.get("/", response_class=HTMLResponse)
def index():
    return resources.files("story8").joinpath("web/index.html").read_text(encoding="utf-8")


api = Depends(auth)


@app.get("/api/health", dependencies=[api])
def health():
    s = studio()
    info: dict[str, Any] = {"provider": s.provider.name, "model": getattr(s.provider, "model", None)}
    if s.provider.name == "hermes":
        try:
            s.provider.health(); info["reachable"] = True
        except Exception as e:  # noqa: BLE001
            info["reachable"] = False; info["error"] = str(e)[:200]
    return info


@app.get("/api/policy/catalog", dependencies=[api])
def catalog():
    return {"locked": [r.__dict__ for r in LOCKED],
            "toggles": [dict(t.__dict__, choices=list(t.choices)) for t in TOGGLES]}


class NewProject(BaseModel):
    name: str
    mode: Mode = Mode.COLLAB
    brand: Optional[str] = None
    settings: dict = {}


@app.get("/api/projects", dependencies=[api])
def list_projects():
    return [p.model_dump() for p in studio().projects()]


@app.post("/api/projects", dependencies=[api])
def new_project(body: NewProject, who: Actor = Depends(human)):
    return studio().create_project(body.name, body.mode, body.settings, body.brand, who).model_dump()


@app.get("/api/projects/{pid}", dependencies=[api])
def get_project(pid: str):
    s = studio()
    pr = s.project(pid)
    return {"project": pr.model_dump(), "policy": s.policy(pid).describe(),
            "pilots": [p.model_dump() for p in s.pilots(pid)]}


class Setting(BaseModel):
    key: str
    value: Any


@app.put("/api/projects/{pid}/settings", dependencies=[api])
def put_setting(pid: str, body: Setting, who: Actor = Depends(human)):
    notice = studio().set_setting(pid, body.key, body.value, who)
    return {"notice": notice, "policy": studio().policy(pid).describe()}


@app.get("/api/projects/{pid}/bible", dependencies=[api])
def get_bible(pid: str):
    return studio().bible(pid).model_dump()


@app.put("/api/projects/{pid}/bible", dependencies=[api])
def put_bible(pid: str, body: Bible, who: Actor = Depends(human)):
    return studio().import_bible(pid, body, who).model_dump()


class GenBible(BaseModel):
    logline: str
    genre: str = "로맨스"
    title: Optional[str] = None
    story_year: int = 2026


@app.post("/api/projects/{pid}/bible/generate", dependencies=[api])
def gen_bible(pid: str, body: GenBible):
    return studio().generate_bible(pid, body.logline, body.genre, body.title, body.story_year).model_dump()


class Approve(BaseModel):
    edited: Optional[Any] = None
    note: Optional[str] = None


@app.post("/api/projects/{pid}/bible/approve", dependencies=[api])
def approve_bible(pid: str, body: Approve, who: Actor = Depends(human)):
    return studio().approve_bible(pid, who, body.edited).model_dump()


class NewPilot(BaseModel):
    hook_variant: str
    episodes: list[int] = [1, 2, 3]


@app.post("/api/projects/{pid}/pilots", dependencies=[api])
def new_pilot(pid: str, body: NewPilot):
    return studio().new_pilot(pid, body.hook_variant, body.episodes).model_dump()


@app.get("/api/projects/{pid}/pilots/{plt}", dependencies=[api])
def get_pilot(pid: str, plt: str):
    return studio().pilot(pid, plt).model_dump()


@app.post("/api/projects/{pid}/pilots/{plt}/run", dependencies=[api])
def run_pilot(pid: str, plt: str):
    return studio().run(pid, plt).model_dump()


@app.post("/api/projects/{pid}/pilots/{plt}/approve", dependencies=[api])
def approve_pilot(pid: str, plt: str, body: Approve, who: Actor = Depends(human)):
    return studio().approve(pid, plt, who, body.edited, body.note).model_dump()


@app.post("/api/projects/{pid}/ratings", dependencies=[api])
def add_ratings(pid: str, body: list[dict]):
    for r in body:
        studio().add_rating(pid, r)
    return {"added": len(body)}


@app.post("/api/projects/{pid}/ab", dependencies=[api])
def add_ab(pid: str, body: list[dict]):
    for r in body:
        studio().add_ab(pid, r)
    return {"added": len(body)}


@app.get("/api/projects/{pid}/evaluation", dependencies=[api])
def evaluation(pid: str, top: float = 0.25):
    return studio().evaluate(pid, top)


@app.post("/api/projects/{pid}/pilots/{plt}/promote", dependencies=[api])
def promote(pid: str, plt: str, who: Actor = Depends(human)):
    return studio().promote(pid, plt, who).model_dump()


class Export(BaseModel):
    kind: str = "platform"


@app.post("/api/projects/{pid}/pilots/{plt}/export", dependencies=[api])
def export(pid: str, plt: str, body: Export):
    return studio().export(pid, plt, body.kind)


@app.get("/api/projects/{pid}/proof", dependencies=[api])
def proof_cert(pid: str):
    return studio().certificate(pid)


@app.get("/api/projects/{pid}/ledger", dependencies=[api])
def ledger(pid: str):
    lg = studio().ledger(pid)
    ok, errors = lg.verify()
    return {"ok": ok, "errors": errors, "events": [e.model_dump() for e in lg.events]}
