import json

from fastapi.testclient import TestClient

from story8 import api
from story8.offline import OfflineProvider
from story8.studio import Studio


def test_api_flow(tmp_path, bible):
    api.set_studio(Studio(tmp_path, OfflineProvider(), secret="s"))
    c = TestClient(api.app)
    H = {"X-Story8-User": "writer-lee"}
    assert "STORY 8" in c.get("/").text
    assert c.get("/api/health").json()["provider"] == "offline"
    pid = c.post("/api/projects", json={"name": "웹", "mode": "collab"}, headers=H).json()["id"]
    r = c.put(f"/api/projects/{pid}/settings", json={"key": "ai_output_label", "value": False})
    assert r.status_code == 400 and "끌 수 없습니다" in r.json()["detail"]
    r = c.put(f"/api/projects/{pid}/settings", json={"key": "approve_edit", "value": False})
    assert r.json()["notice"]
    assert c.put(f"/api/projects/{pid}/bible", json=json.loads(bible.model_dump_json()), headers=H).status_code == 200
    plt = c.post(f"/api/projects/{pid}/pilots", json={"hook_variant": "복수 훅"}).json()["id"]
    assert c.post(f"/api/projects/{pid}/pilots/{plt}/run").json()["pending_review"] == "beats"
    assert c.post(f"/api/projects/{pid}/pilots/{plt}/approve", json={}, headers=H).json()["pending_review"] == "script"
    p = c.post(f"/api/projects/{pid}/pilots/{plt}/approve", json={}, headers=H).json()
    assert p["stage"] == "done"  # 최종 편집 승인 꺼짐
    out = c.post(f"/api/projects/{pid}/pilots/{plt}/export", json={"kind": "delivery"}).json()
    assert "manifest.json" in out["files"]
    assert c.get(f"/api/projects/{pid}/ledger").json()["ok"]
    assert c.get(f"/api/projects/{pid}/proof").json()["grade"] == "C"
