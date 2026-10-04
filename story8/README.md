# STORY 8 SHORTS — AI 하이브리드 숏드라마 스튜디오

캐논 바이블 → AI 작가실(비트·대본·스토리보드) → 검수(연속성·AI 티·안전) → 파일럿 검증 → 승격 → 권리 증명·내보내기.
제작할 때마다 **자동 모드**(사람 개입 없음)와 **협업 모드**(단계별 사람 승인·수정)를 고를 수 있고, 법적 의무가 아닌 기능은 모두 켜고 끌 수 있습니다.

## 설치

```bash
cd story8
pip install -e ".[server,dev]"
pytest            # 서버·키 없이 23개 테스트(오프라인 생성기)
```

## Hermes 연결 (API 키가 필요한 생성은 모두 Hermes로)

LLM 호출은 전부 [Hermes Agent](https://github.com/NousResearch/hermes-agent)의 OpenAI 호환 API 서버로 보냅니다.

1. Hermes 쪽 `~/.hermes/.env`에 다음을 넣고 게이트웨이를 실행합니다.
   ```
   API_SERVER_ENABLED=true
   API_SERVER_KEY=원하는-긴-비밀값
   ```
   (기본 주소 `http://127.0.0.1:8642/v1`)
2. STORY 8 쪽 환경 변수를 설정합니다.
   ```bash
   export HERMES_BASE_URL=http://127.0.0.1:8642/v1
   export HERMES_API_KEY=위의-API_SERVER_KEY
   export HERMES_MODEL=hermes-agent
   story8 hermes-check        # 연결 확인
   ```
   OpenRouter의 Hermes 4를 직접 쓸 때는 `HERMES_BASE_URL=https://openrouter.ai/api/v1`,
   `HERMES_MODEL=nousresearch/hermes-4-405b`, `HERMES_API_KEY=<OpenRouter 키>`로 바꾸면 됩니다.
3. `STORY8_PROVIDER=offline`이면 서버 없이 결정적 시험 생성기로 동작합니다(품질 없음, 흐름 시험용).

생성 응답은 `JSON 스키마 지시 → JSON 추출 → pydantic 검증 → 실패 시 오류를 알려 재시도` 순서로 처리하므로 모델이 `response_format`을 지원하지 않아도 동작합니다.
`STORY8_SEMANTIC_CHECK=1`이면 규칙 검사 외에 LLM 의미 연속성 검사를 추가로 돌립니다.

## 사용 (CLI)

```bash
export STORY8_USER=writer-kim
story8 project new "다시, 왼손" --mode collab --brand 채널옥트
story8 bible import <PID> examples/pianist_bible.json     # 또는: story8 bible generate <PID> --logline "..." --genre 복수
story8 pilot new <PID> --hook "복수 선언 훅"
story8 pilot run <PID> <PLT>                               # 협업 모드: 승인 지점에서 멈춤
story8 pilot approve <PID> <PLT> [--file 수정본.json]       # 수정본을 주면 편집률이 원장에 기록됨
story8 export <PID> <PLT> --kind delivery
story8 proof <PID> ; story8 verify <PID>
story8 settings <PID> approve_script off                  # 기능 끄기(잠금 항목은 거부됨)
story8 serve                                              # 웹 스튜디오 http://127.0.0.1:8800
```

자동 모드: `--mode auto` → `bible generate` → `pilot run` 한 번으로 완료. 여러 훅으로 파일럿을 만든 뒤
`rate`/`ab`로 결과를 넣고 `evaluate` → `promote`로 상위 작품을 협업 프로젝트로 승격합니다.

## 구성

| 모듈 | 역할 |
|---|---|
| `policy.py` | 잠금(법적 의무 7개) / 토글(12개) 정책 엔진, 모드별 기본값 |
| `llm.py` | Hermes(OpenAI 호환) 클라이언트, 스키마 검증·재시도 |
| `writers_room.py` | 개요 먼저 쓰고 집필, 회차별 바이블 발췌(RAG)·이전 회차 요약 주입 |
| `continuity.py` | 사망 인물 등장, 미등록 화자, 금칙, 나이·속성 불일치, 세계관 규칙 + 선택적 LLM 검사 |
| `aitell.py` | 어미 단조·문장 길이 변동·상투구·반복·말투 구분 'AI 티' 점수 |
| `safety.py` | 아동 성적 표현 차단, 실존 인물 동의 확인, 등급 추정·초과 차단(잠금) |
| `ledger.py` | 해시 체인 권리 원장(내용 해시만 저장, 타임스탬프 서명 교체 가능) |
| `proof.py` | S8 Proof 기여 증명서(A~D 등급, 소급 상향 금지, 서명) |
| `media.py` | 샷 프롬프트(9:16, 인물 일관성 토큰, 라벨 오버레이)·렌더 비용 견적, 영상 모델 어댑터 |
| `evaluation.py` | 독자단 점수 + A/B 완주율 윌슨 하한, 상위 25% 승격 |
| `export.py` | 플랫폼/납품 패키지: 대본·스토리보드·QC·AI 고지·C2PA형 매니페스트·증명서 |
| `studio.py` / `api.py` / `web/` | 오케스트레이션, HTTP API, 웹 스튜디오 |

## 정직한 한계

- 영상 생성은 어댑터 인터페이스와 렌더 계획·비용 견적까지입니다. 실제 영상 모델 연결은 계약 업체 API로 `VideoProvider`를 구현해야 합니다.
- 안전·등급 검사는 키워드 기반 1차 필터입니다. 상용 서비스에는 분류 모델과 사람 검수가 필요합니다.
- 매니페스트는 C2PA 구조를 본뜬 사이드카이며, 서명은 c2patool 등 외부 도구로 붙여야 합니다.
- 'AI 티' 기준값과 승격 기준은 가정치입니다. 실제 시청 데이터로 다시 맞춰야 합니다.
- 법적 잠금 목록은 법률 자문이 아닙니다. 출시 전 변호사 검토가 필요합니다.
