"""story8 명령행 도구."""

from __future__ import annotations

import argparse
import getpass
import json
import os
import sys
from pathlib import Path

from .models import Actor, Bible, Mode


def _studio(args):
    from .llm import provider_from_env
    from .studio import Studio
    return Studio(args.root, provider_from_env(args.provider))


def _human(args) -> Actor:
    return Actor(kind="human", id=args.user or os.environ.get("STORY8_USER") or getpass.getuser())


def _print(obj):
    if hasattr(obj, "model_dump"):
        obj = obj.model_dump()
    print(json.dumps(obj, ensure_ascii=False, indent=2, default=str))


def _val(v: str):
    return {"on": True, "true": True, "off": False, "false": False}.get(v.lower(), v)


def _pilot_summary(p):
    return {"id": p.id, "hook": p.hook_variant, "stage": p.stage, "pending_review": p.pending_review,
            "status": p.status, "rating": p.rating, "issues": [i.message for i in p.issues],
            "ai_tell": (p.ai_tell or {}).get("score"),
            "estimate_usd": ((p.render_plan or {}).get("estimate_usd") or {}).get("generation")}


def main(argv=None):
    ap = argparse.ArgumentParser(prog="story8", description="STORY 8 SHORTS — AI 하이브리드 숏드라마 스튜디오")
    ap.add_argument("--root", default=os.environ.get("STORY8_HOME", "story8-workspace"))
    ap.add_argument("--provider", choices=["hermes", "offline"], default=None)
    ap.add_argument("--user", default=None, help="사람 작가 id(승인·편집 기록용)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("project"); ss = s.add_subparsers(dest="sub", required=True)
    x = ss.add_parser("new"); x.add_argument("name"); x.add_argument("--mode", choices=["auto", "collab"], default="collab")
    x.add_argument("--brand")
    ss.add_parser("list")

    s = sub.add_parser("settings"); s.add_argument("project"); s.add_argument("key", nargs="?"); s.add_argument("value", nargs="?")

    s = sub.add_parser("bible"); ss = s.add_subparsers(dest="sub", required=True)
    x = ss.add_parser("import"); x.add_argument("project"); x.add_argument("file")
    x = ss.add_parser("generate"); x.add_argument("project"); x.add_argument("--logline", required=True)
    x.add_argument("--genre", default="로맨스"); x.add_argument("--year", type=int, default=2026)
    x = ss.add_parser("approve"); x.add_argument("project"); x.add_argument("--file")
    x = ss.add_parser("show"); x.add_argument("project")

    s = sub.add_parser("pilot"); ss = s.add_subparsers(dest="sub", required=True)
    x = ss.add_parser("new"); x.add_argument("project"); x.add_argument("--hook", required=True)
    x.add_argument("--episodes", default="1,2,3")
    for name in ("run", "show"):
        x = ss.add_parser(name); x.add_argument("project"); x.add_argument("pilot")
    x = ss.add_parser("approve"); x.add_argument("project"); x.add_argument("pilot"); x.add_argument("--file")
    x.add_argument("--note")
    x = ss.add_parser("list"); x.add_argument("project")

    s = sub.add_parser("rate"); s.add_argument("project"); s.add_argument("file", help="PanelRating 목록 JSON")
    s = sub.add_parser("ab"); s.add_argument("project"); s.add_argument("file", help="ABResult 목록 JSON")
    s = sub.add_parser("evaluate"); s.add_argument("project"); s.add_argument("--top", type=float, default=0.25)
    s = sub.add_parser("promote"); s.add_argument("project"); s.add_argument("pilot")
    s = sub.add_parser("export"); s.add_argument("project"); s.add_argument("pilot")
    s.add_argument("--kind", choices=["platform", "delivery"], default="platform"); s.add_argument("--out")
    s = sub.add_parser("proof"); s.add_argument("project")
    s = sub.add_parser("verify"); s.add_argument("project")
    sub.add_parser("hermes-check")
    s = sub.add_parser("serve"); s.add_argument("--host", default="127.0.0.1"); s.add_argument("--port", type=int, default=8800)

    args = ap.parse_args(argv)
    try:
        return _dispatch(args)
    except Exception as e:  # 사용자에게 한 줄 오류
        print(f"오류: {e}", file=sys.stderr)
        return 1


def _dispatch(args):
    if args.cmd == "hermes-check":
        from .llm import HermesProvider
        h = HermesProvider()
        _print({"base_url": h.base_url, "model": h.model, "models": h.health()})
        return 0
    if args.cmd == "serve":
        import uvicorn
        os.environ["STORY8_HOME"] = args.root
        if args.provider:
            os.environ["STORY8_PROVIDER"] = args.provider
        uvicorn.run("story8.api:app", host=args.host, port=args.port)
        return 0

    st = _studio(args)
    c = args.cmd
    if c == "project":
        if args.sub == "new":
            pr = st.create_project(args.name, Mode(args.mode), brand=args.brand, actor=_human(args))
            _print({"project": pr.id, "mode": pr.mode.value, "policy": st.policy(pr.id).describe()})
        else:
            _print([{"id": p.id, "name": p.name, "mode": p.mode.value, "promoted_from": p.promoted_from}
                    for p in st.projects()])
    elif c == "settings":
        if args.key:
            notice = st.set_setting(args.project, args.key, _val(args.value), _human(args))
            if notice:
                print(f"안내: {notice}")
        _print(st.policy(args.project).describe())
    elif c == "bible":
        if args.sub == "import":
            b = Bible.model_validate_json(Path(args.file).read_text(encoding="utf-8"))
            st.import_bible(args.project, b, _human(args)); print("바이블을 가져왔습니다.")
        elif args.sub == "generate":
            b = st.generate_bible(args.project, args.logline, args.genre, story_year=args.year); _print(b)
        elif args.sub == "approve":
            edited = json.loads(Path(args.file).read_text(encoding="utf-8")) if args.file else None
            st.approve_bible(args.project, _human(args), edited); print("바이블 승인 완료.")
        else:
            _print(st.bible(args.project))
    elif c == "pilot":
        if args.sub == "new":
            p = st.new_pilot(args.project, args.hook, [int(x) for x in args.episodes.split(",")])
            _print(_pilot_summary(p))
        elif args.sub == "run":
            _print(_pilot_summary(st.run(args.project, args.pilot)))
        elif args.sub == "show":
            _print(st.pilot(args.project, args.pilot))
        elif args.sub == "list":
            _print([_pilot_summary(p) for p in st.pilots(args.project)])
        else:
            edited = json.loads(Path(args.file).read_text(encoding="utf-8")) if args.file else None
            _print(_pilot_summary(st.approve(args.project, args.pilot, _human(args), edited, args.note)))
    elif c == "rate":
        for r in json.loads(Path(args.file).read_text(encoding="utf-8")):
            st.add_rating(args.project, r)
        print("평가를 기록했습니다.")
    elif c == "ab":
        for r in json.loads(Path(args.file).read_text(encoding="utf-8")):
            st.add_ab(args.project, r)
        print("A/B 결과를 기록했습니다.")
    elif c == "evaluate":
        _print(st.evaluate(args.project, args.top))
    elif c == "promote":
        pr = st.promote(args.project, args.pilot, _human(args))
        _print({"new_project": pr.id, "mode": pr.mode.value, "promoted_from": pr.promoted_from})
    elif c == "export":
        _print(st.export(args.project, args.pilot, args.kind, Path(args.out) if args.out else None))
    elif c == "proof":
        _print(st.certificate(args.project))
    elif c == "verify":
        ok, errors = st.ledger(args.project).verify()
        _print({"ok": ok, "errors": errors, "events": len(st.ledger(args.project).events)})
        return 0 if ok else 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
