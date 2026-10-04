"""LLM 연결 계층.

- HermesProvider: Nous Research Hermes Agent 의 OpenAI 호환 API 서버(기본 http://127.0.0.1:8642/v1)에 연결한다.
  같은 형식이므로 OpenRouter(nousresearch/hermes-4-405b 등)나 다른 OpenAI 호환 엔드포인트에도 base_url 만 바꿔 쓸 수 있다.
- OfflineProvider: API 키·서버 없이 전체 파이프라인을 시험하는 결정적(deterministic) 생성기.

모든 생성은 'JSON 스키마를 지시 → 응답에서 JSON 추출 → pydantic 검증 → 실패 시 오류를 알려 재시도' 순서로 동작하므로
response_format 지원 여부와 무관하게 동작한다.
"""

from __future__ import annotations

import json
import os
import re
from typing import Optional, Protocol, TypeVar

import httpx
from pydantic import BaseModel, ValidationError

T = TypeVar("T", bound=BaseModel)


class LLMError(RuntimeError):
    pass


class LLMProvider(Protocol):
    name: str

    def complete_json(self, task: str, system: str, prompt: str, schema: type[T],
                      context: Optional[dict] = None) -> T: ...


def extract_json(text: str) -> str:
    """응답 문자열에서 JSON 객체를 꺼낸다(코드펜스·앞뒤 설명 허용)."""
    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.S)
    if fence:
        return fence.group(1)
    start = text.find("{")
    if start < 0:
        raise LLMError("응답에 JSON 객체가 없습니다.")
    depth, in_str, esc = 0, False, False
    for i in range(start, len(text)):
        ch = text[i]
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return text[start:i + 1]
    raise LLMError("JSON 객체가 닫히지 않았습니다(출력이 잘렸을 수 있음).")


class HermesProvider:
    """Hermes Agent API 서버(OpenAI Chat Completions 호환) 클라이언트.

    환경 변수:
      HERMES_BASE_URL  기본 http://127.0.0.1:8642/v1  (OpenRouter: https://openrouter.ai/api/v1)
      HERMES_API_KEY   Hermes 의 API_SERVER_KEY (OpenRouter 사용 시 OpenRouter 키)
      HERMES_MODEL     기본 hermes-agent (OpenRouter 예: nousresearch/hermes-4-405b)
    """

    name = "hermes"

    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None,
                 model: Optional[str] = None, timeout: float = 600.0, max_retries: int = 2,
                 temperature: float = 0.7, client: Optional[httpx.Client] = None):
        self.base_url = (base_url or os.environ.get("HERMES_BASE_URL") or "http://127.0.0.1:8642/v1").rstrip("/")
        self.api_key = api_key or os.environ.get("HERMES_API_KEY") or ""
        self.model = model or os.environ.get("HERMES_MODEL") or "hermes-agent"
        self.max_retries = max_retries
        self.temperature = temperature
        self.client = client or httpx.Client(timeout=timeout)
        self.usage = {"prompt_tokens": 0, "completion_tokens": 0, "calls": 0}

    def _headers(self) -> dict:
        h = {"Content-Type": "application/json"}
        if self.api_key:
            h["Authorization"] = f"Bearer {self.api_key}"
        return h

    def health(self) -> dict:
        r = self.client.get(f"{self.base_url}/models", headers=self._headers())
        r.raise_for_status()
        return r.json()

    def chat(self, messages: list[dict]) -> str:
        payload = {"model": self.model, "messages": messages, "temperature": self.temperature}
        try:
            r = self.client.post(f"{self.base_url}/chat/completions", headers=self._headers(), json=payload)
        except httpx.HTTPError as e:
            raise LLMError(f"Hermes 연결 실패({self.base_url}): {e}") from e
        if r.status_code >= 400:
            raise LLMError(f"Hermes 오류 {r.status_code}: {r.text[:500]}")
        data = r.json()
        usage = data.get("usage") or {}
        self.usage["calls"] += 1
        self.usage["prompt_tokens"] += usage.get("prompt_tokens", 0) or 0
        self.usage["completion_tokens"] += usage.get("completion_tokens", 0) or 0
        choice = (data.get("choices") or [{}])[0]
        if choice.get("finish_reason") == "length":
            raise LLMError("출력이 길이 제한으로 잘렸습니다.")
        content = (choice.get("message") or {}).get("content")
        if not content:
            raise LLMError("빈 응답")
        return content

    def complete_json(self, task: str, system: str, prompt: str, schema: type[T],
                      context: Optional[dict] = None) -> T:
        schema_txt = json.dumps(schema.model_json_schema(), ensure_ascii=False)
        sys = (f"{system}\n\n응답은 반드시 아래 JSON 스키마를 만족하는 JSON 객체 하나만 출력하라. "
               f"설명 문장이나 코드펜스 없이 JSON 만 출력한다.\nJSON 스키마:\n{schema_txt}")
        messages = [{"role": "system", "content": sys}, {"role": "user", "content": prompt}]
        last_err = ""
        for _ in range(self.max_retries + 1):
            text = self.chat(messages)
            try:
                return schema.model_validate_json(extract_json(text))
            except (ValidationError, LLMError, json.JSONDecodeError) as e:
                last_err = str(e)[:1500]
                messages += [
                    {"role": "assistant", "content": text},
                    {"role": "user", "content": f"JSON 이 스키마 검증에 실패했다. 오류:\n{last_err}\n"
                                                f"스키마를 지켜 JSON 객체만 다시 출력하라."},
                ]
        raise LLMError(f"[{task}] 스키마 검증 실패: {last_err}")


def provider_from_env(name: Optional[str] = None) -> LLMProvider:
    """STORY8_PROVIDER=hermes|offline (기본: Hermes 설정이 있으면 hermes, 없으면 offline)."""
    name = name or os.environ.get("STORY8_PROVIDER")
    if not name:
        name = "hermes" if (os.environ.get("HERMES_BASE_URL") or os.environ.get("HERMES_API_KEY")) else "offline"
    if name == "hermes":
        return HermesProvider()
    if name == "offline":
        from .offline import OfflineProvider
        return OfflineProvider()
    raise ValueError(f"알 수 없는 provider: {name}")
