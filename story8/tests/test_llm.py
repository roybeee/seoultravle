import json

import httpx
import pytest

from story8.llm import HermesProvider, LLMError, extract_json, provider_from_env
from story8.models import BeatSheet


def test_extract_json_variants():
    assert json.loads(extract_json('설명 ```json\n{"a": 1}\n``` 끝')) == {"a": 1}
    assert json.loads(extract_json('앞 {"a": "}{", "b": {"c": 2}} 뒤')) == {"a": "}{", "b": {"c": 2}}
    with pytest.raises(LLMError):
        extract_json("no json")


def _client(responses, seen):
    it = iter(responses)

    def handler(req: httpx.Request):
        seen.append(req)
        if req.url.path.endswith("/models"):
            return httpx.Response(200, json={"data": [{"id": "hermes-agent"}]})
        return httpx.Response(200, json={"choices": [{"message": {"content": next(it)}, "finish_reason": "stop"}],
                                         "usage": {"prompt_tokens": 10, "completion_tokens": 5}})
    return httpx.Client(transport=httpx.MockTransport(handler))


def test_hermes_retry_on_invalid_then_success():
    seen = []
    good = {"beats": [{"episode": 1, "summary": "s", "characters": ["a"], "hook": "h"}]}
    h = HermesProvider(base_url="http://hermes.local/v1", api_key="k", model="hermes-agent",
                       client=_client(["{\"beats\": 3}", json.dumps(good)], seen))
    out = h.complete_json("beats", "sys", "prompt", BeatSheet)
    assert out.beats[0].episode == 1
    assert h.usage["calls"] == 2
    assert seen[0].headers["authorization"] == "Bearer k"
    body = json.loads(seen[1].content)
    assert body["model"] == "hermes-agent" and "스키마 검증에 실패" in body["messages"][-1]["content"]
    assert h.health()["data"][0]["id"] == "hermes-agent"


def test_hermes_gives_up():
    h = HermesProvider(base_url="http://x/v1", client=_client(["nope"] * 3, []), max_retries=2)
    with pytest.raises(LLMError):
        h.complete_json("beats", "s", "p", BeatSheet)


def test_provider_from_env(monkeypatch):
    monkeypatch.delenv("STORY8_PROVIDER", raising=False)
    monkeypatch.delenv("HERMES_BASE_URL", raising=False)
    monkeypatch.delenv("HERMES_API_KEY", raising=False)
    assert provider_from_env().name == "offline"
    monkeypatch.setenv("HERMES_BASE_URL", "http://127.0.0.1:8642/v1")
    assert provider_from_env().name == "hermes"
