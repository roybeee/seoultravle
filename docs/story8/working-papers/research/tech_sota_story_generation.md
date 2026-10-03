# 리서치 노트: 2026년 기준 장편 서사 생성·캐릭터 일관성 기술 수준(SOTA)과 현실적 아키텍처·비용

- 작성일: 2026-10-03 / 작성자: AI·콘텐츠 산업 리서처(서브에이전트)
- 분석 대상: ㈜채널옥트 "STORY 8 OPERATION PLAN"(26p, PDF 생성 2026-04-24)의 기술 맵(블록체인·딥러닝 캐릭터 생성·300~500자 교대 집필·흥행 예측)
- 원칙: 모든 수치에 기준 시점과 출처 URL을 붙임. 확인 불가한 것은 "미확인"으로 표기. 가격은 공식 요금표를 우선하고, 집계 사이트(aggregator) 수치는 "집계 사이트 기준"으로 구분.

---

## 1. 프론티어 모델: 2026년 창작 능력·컨텍스트·API 가격

### 1-1. 공식 요금표(2026-10-03 조회 기준)

**Anthropic (공식 요금 페이지, platform.claude.com/docs/en/about-claude/pricing, 2026-10-03 조회)**
| 모델 | 입력/MTok | 출력/MTok | 캐시 읽기 | Batch(입/출) | 비고 |
|---|---|---|---|---|---|
| Claude Fable 5.1 | $10 | $50 | $0.25 | $5/$25 | 최상위 |
| Claude Opus 5.5 | $4 | $20 | $0.20 | $2/$10 | |
| Claude Opus 5 / 4.8 / 4.7 / 4.6 | $5 | $25 | $0.50 | $2.50/$12.50 | |
| Claude Sonnet 5.5 / Sonnet 5 | $2 | $10 | $0.20 | $1/$5 | Sonnet 5의 $2/$10은 "정식 가격으로 확정"(9월 인상 취소) |
| Claude Sonnet 4.6 / 4.5 | $3 | $15 | $0.30 | $1.50/$7.50 | |
| Claude Haiku 4.5 | $1 | $5 | $0.10 | $0.50/$2.50 | 대량 생성용 |
- 컨텍스트: "Claude 4.6 이후 모델은 1M 토큰 컨텍스트를 표준 가격에 제공(90만 토큰 요청도 9천 토큰 요청과 동일 단가)". 장문 할증 없음.
- 주의: "Claude 4.7 이후 모델은 새 토크나이저를 사용하며 같은 텍스트에 약 30% 더 많은 토큰을 생성" → 한국어 비용 산정 시 반영 필요.
- 출처: https://platform.claude.com/docs/en/about-claude/pricing

**OpenAI (공식 요금 페이지 developers.openai.com/api/docs/pricing, 2026-10-03 조회)**
| 모델 | 입력/MTok | 캐시 입력 | 출력/MTok |
|---|---|---|---|
| gpt-6-astra | $10.00 | $1.00 | $50.00 |
| gpt-6.1-sol / gpt-6-sol | $2.00 | $0.10~0.20 | $10.00 |
| gpt-6-luna | $0.10 | $0.01 | $0.50 |
| gpt-5.6-sol | $4.00 | $0.40 | $20.00 |
| gpt-5.6-terra | $2.00 | $0.20 | $12.00 |
| gpt-5.5 (<272K) | $5.00 | $0.50 | $30.00 |
| gpt-5.4 (<272K) | $2.50 | $0.25 | $15.00 |
| gpt-5.4-mini / nano | $0.75 / $0.20 | | $4.50 / $1.25 |
| gpt-5 / 5.1 | $1.25 | $0.125 | $10.00 |
| gpt-5-nano | $0.05 | | $0.40 |
- 컨텍스트 구간: "Short context ≤272K 입력 토큰, Long context >272K"(공식). 집계 사이트는 GPT-5.5/5.4가 1M/1.05M 컨텍스트라 기재(https://www.morphllm.com/openai-api-pricing, 미검증). GPT-5.5 출시 2026-04-23에 GPT-5 계열 단가가 2배로 인상(집계 사이트 기준).
- 이미지: gpt-image-2 / gpt-image-2.5 출력 $30/MTok(이미지 토큰), gpt-image-1.5 $32/MTok. Sora 가격은 공식 요금표에 없음(미확인).
- 출처: https://developers.openai.com/api/docs/pricing

**Google (공식 ai.google.dev/gemini-api/docs/pricing, 2026-10-03 조회)**
- Gemini 3.1 Pro Preview: $2.00/$12.00(≤200K), $4.00/$18.00(>200K), 1M 컨텍스트; Batch 50% 할인; 캐시 입력 $0.20/MTok(집계 사이트 기준).
- Gemini 3.5 Flash $1.50/$9.00; Gemini 3.6~3.8 Flash $0.75/$3.75(2026-12-31까지 프로모션); 3.5 Flash-Lite $0.30/$2.50; 3.1 Flash-Lite $0.25/$1.50.
- 이미지: Gemini 3.1 Flash Image 약 $0.045/장(1K), Gemini 3 Pro Image 약 $0.134/장(1K/2K), $0.24/장(4K); 2.5 Flash Image 약 $0.039/장.
- 영상: Veo 3.1 $0.40~0.60/초(720p~4K). 임베딩: Gemini Embedding 2 $0.20/MTok.
- 출처: https://ai.google.dev/gemini-api/docs/pricing

**xAI (집계 사이트 기준, 2026-08 조회분)**: Grok-4 $3/$15, 256K; Grok 4.5 $2/$6, 500K; Grok 4 Fast $0.20/$0.50, 2M 컨텍스트. 출처: https://pricepertoken.com/pricing-page/model/xai-grok-4 , https://anotherwrapper.com/tools/llm-pricing/grok-4.5 (공식 미확인)

### 1-2. 창작 품질 평가(벤치마크)
- EQ-Bench Creative Writing v3(LLM 심사, 32개 프롬프트×3회): 2026-09 기준 Claude Opus 5 Elo 2121 1위, Kimi K3(Moonshot) 2071 2위, GPT-5.6 Sol 1963 3위(집계 기사 기준). 오픈웨이트 중 Kimi K2.6 루브릭 16.67, DeepSeek-V4-Pro 16.45, GLM-5.2 16.44로 최상위권. 출처: https://www.digitalapplied.com/blog/which-ai-model-writes-best-leaderboards-disagree , https://eqbench.com/about.html , https://owl.eqbench.com/
- 한계: 이 리더보드는 LLM(Claude 3.5 Sonnet 등)을 심사관으로 쓰므로 "LLM이 좋아하는 글"로 편향될 수 있음(아래 §2-5 참고). 보드 간 순위가 서로 어긋난다는 점도 보고됨(같은 출처).

### 1-3. 오픈웨이트 모델(가격·창작)
- OpenRouter 기준(2026-09): DeepSeek V4 Pro $0.209/$0.418, DeepSeek V4 Flash $0.042/$0.084, Qwen3-235B-A22B $0.09/$0.10, Kimi K2.6 $0.65/$3.41, Llama 4 Maverick $0.15/$0.60 (집계 사이트 기준, 공급자별 상이). 출처: https://betonai.net/openrouter-pricing-2026-complete-guide-to-every-model-tier-and-hidden-cost/ , https://www.teamday.ai/blog/top-ai-models-openrouter-2026
- 창작 품질은 Kimi/DeepSeek/GLM이 프론티어와 격차를 좁혔다는 평가(§1-2). 한국어 창작 품질은 별도 검증 필요(미확인).

### 1-4. 한국어 특화 모델
- 독자 AI 파운데이션 모델(독파모) 2차 평가(2026-08-18, 과기정통부): LG AI연구원 K-EXAONE 2.0, SKT A.X K2(688B), 업스테이지 Solar Open 2(250B, 2026-07-22 공개)가 3차 진출. 모티프 탈락. 최종 2개 팀은 2026년 말 발표. 출처: https://view.asiae.co.kr/article/2026081811194974583 , https://kidd.co.kr/news/244661 , https://supple.kr/news/cms5eie1w00bmtw9twmwp6z7k
- KMMLU(2026 리더보드): Solar 80.1, HyperCLOVA X 78.4, A.X 78.0, K-EXAONE 76.0, EXAONE 4.0 75.2. 출처: https://benchlm.ai/leaderboards/korean-benchmarks
- 'LLM 한국어 사용성 순위 v2'(2026-04-07): CLOVA X 70.51(23위), EXAONE-4.0.1-32B 60.00(36위), Solar-Pro 55.46(39위), A.X 4.0 52.95(41위) — 상위권은 글로벌 프론티어 모델. 출처: https://wikidocs.net/277814
- 시사점: 한국어 '창작' 전용 공개 벤치마크는 사실상 없음(미확인). 한국어 모델은 "소버린·데이터 주권·온프레미스 파인튜닝" 용도로 가치가 있지만, 2026년 시점의 장편 창작 품질은 글로벌 프론티어가 앞선다는 것이 공개 지표의 공통된 방향.
- 토큰 효율: Claude에서 한국어는 100자당 약 106토큰(영어 32토큰), 의미 단위 기준 영어 대비 약 1.85배. GPT-5.5 토크나이저가 한국어에 가장 효율적이라는 측정도 있음. 출처: https://dev.to/claudeguide/korean-vs-english-do-you-pay-more-tokens-for-the-same-prompt-jm8 , https://dev.to/synthorai/which-llm-is-cheapest-for-your-language-tokenizer-costs-measured-1k5m (개인 측정, 중간 신뢰도)

---

## 2. 장편 스토리 생성 연구·시스템

### 2-1. 계보
- Dramatron(DeepMind, 2022-09, arXiv 2209.14958): 로그라인→제목·인물·플롯(장면 비트)·장소·대사의 계층적 생성. 15명의 극작가 2시간 세션 평가 — "전체 희곡을 쓰는 데는 쓰지 않겠다", 출력이 "공식적(formulaic)", 대신 세계관 구축·대안 탐색·아이디어 발상에 유용. 출처: https://arxiv.org/pdf/2209.14958 , https://github.com/google-deepmind/dramatron
- WHAT-IF(UPenn/UMBC, 2024-12, arXiv 2412.10582): 기존 선형 플롯에서 주인공의 결정 지점마다 분기 생성, 분기 트리를 그래프로 저장해 인터랙티브 픽션으로 플레이. 출처: https://arxiv.org/abs/2412.10582v2
- Agents' Room(2024-10, arXiv 2410.02603): 오케스트레이터가 계획 에이전트·집필 에이전트를 조정, 1,000~2,000단어 수준. 출처: https://github.com/Picrew/awesome-llm-story-generation
- StoryWriter(2025-06-19, arXiv 2506.16445, 칭화대 Li Juanzi 그룹): 아웃라인(사건·인물관계) → 플래닝(사건 상세·챕터 배분) → 집필(스토리 히스토리 동적 압축) 3-에이전트. 평균 약 8,000단어, LongStory 데이터셋 약 6,000편, Llama3.1-8B/GLM4-9B SFT 공개. 출처: https://arxiv.org/abs/2506.16445
- MAGNET "From Personas to Plot"(2026-07-01, arXiv 2607.00918): 페르소나 기반 캐릭터 에이전트가 공유 월드 스테이트와 목표에 따라 행동 제안, 100페이지급 서사. ATLAS(그래프 기반 장면별 월드 표현 비교)로 환각 검출. 단일 모델 프롬프팅 대비 환각 50% 감소, IBSEN 대비 45% 개선. 출처: https://arxiv.org/abs/2607.00918
- 기타 2025~2026: ConWriter(전이 제약·상태 기반 신경-기호 일관성 제어, arXiv 2608.05169), StoryBox(멀티에이전트 시뮬레이션 기반 bottom-up 장편, arXiv 2510.11618), CreAgentive(arXiv 2509.26461), 장기 일관성 벤치마크(arXiv 2608.08160). 출처: https://arxiv.org/pdf/2608.05169 , https://arxiv.org/pdf/2510.11618

### 2-2. 캐릭터·세계관 일관성(핵심 병목)
- "Lost in Stories: Consistency Bugs in Long Story Generation by LLMs"(ACL 2026 Findings, arXiv 2603.05890, 2026-03-06): ConStory-Bench 2,000 프롬프트·4개 시나리오, 5개 오류 범주·19개 세부 유형, ConStory-Checker(텍스트 근거 제시형 자동 모순 검출). 발견: 일관성 오류는 사실·시간 차원에 집중, 서사 중반부에 빈발, 토큰 엔트로피가 높은 구간에서 발생, 오류 유형 간 동시발생 경향. 출처: https://arxiv.org/abs/2603.05890 , https://aclanthology.org/2026.findings-acl.410/ , https://github.com/Picrew/ConStory-Bench
- 실무 함의: 캐릭터 바이블(character bible)을 구조화 데이터(JSON/그래프)로 두고, 매 장면마다 (a) 관련 엔티티만 검색(RAG)해 주입, (b) 생성 후 월드 스테이트 그래프와 대조하는 '검증기(checker)'를 두는 것이 2026년 표준. MAGNET의 ATLAS, Lost in Stories의 Checker가 그 레퍼런스.
- 1M 컨텍스트(Claude 4.6+, Gemini 3.1 Pro)로 30만 자 원고 전체를 넣는 것은 가능하지만, 비용·주의력 희석 문제로 "전체 원고 + 구조화 바이블 + 롤링 요약"의 하이브리드가 현실적.

### 2-3. 보상 모델·독자 데이터 활용(RLHF/DPO)
- StoryAlign(2026-05-06, arXiv 2605.04831, 칭화대): StoryRMB(1,133개 인간 검증 사례, 선호 1 + 기각 3) 기준 기존 보상 모델 정확도 66.3%에 그침. 약 10만 쌍 선호 데이터로 학습한 StoryReward가 SOTA, best-of-n 선택에서 인간 선호 정렬 개선. 코드·데이터·모델 공개. 출처: https://arxiv.org/abs/2605.04831
- DPO는 2026년 오픈웨이트 파이프라인의 기본 선호 학습법(보상모델·온라인 샘플링 불필요). 합성 데이터 레시피: 인간 시드 200~2,000개 + 10~100배 합성 + 품질 필터. 출처: https://futureagi.com/blog/fine-tuning-llms-unlocking-peak-performance/
- 독자 반응 데이터(열람·이탈·결제·별점)로 웹소설 모델을 DPO한 공개 상업 사례: **미확인**(공개된 1차 자료 없음). 다만 STORY 8의 '챕터별 평점 필수' 설계는 StoryAlign류의 선호 쌍 데이터 수집과 정확히 맞물리므로, 설계만 바꾸면 자산이 된다.

### 2-4. 멀티에이전트 '작가실' 구조
- 공통 패턴: Outline-then-write(아웃라인→챕터 플랜→집필→검수), 역할 분리(쇼러너/플롯/캐릭터/대사/연속성 검수/편집), 월드 스테이트 공유, 반복 수정 루프. StoryWriter·MAGNET·Agents' Room이 모두 이 틀. 300~500자 단위로 AI와 작가가 교대하는 STORY 8 방식은 이 패턴과 반대(계획 없는 국소 이어쓰기)라 일관성 오류가 누적되기 쉬움(§2-2의 "중반부 오류 집중"과 직결).

### 2-5. 서사 품질 자동 평가의 한계(LLM-as-judge)
- 위치 편향, 장문 선호(verbosity) 편향, 자기 선호(self-enhancement) 편향이 반복 보고. 창작처럼 정답이 없는 과제에서는 참조 기반 평가가 부적절. LLM은 "개념적 창의성" 판단에 취약. 출처: https://aclanthology.org/2025.emnlp-main.138.pdf , https://arxiv.org/pdf/2508.05470 , https://arxiv.org/html/2606.01629v1
- 실무 기준: 고정 루브릭 + 인간 라벨과의 Cohen's kappa 측정 + 위치/길이 편향 통제 + 타 모델 계열 교차 검증이 있어야 "생산 투입 가능"한 심사관. 출처: https://llm-academy.dev/observability/llm-as-judge/
- 함의: STORY 8의 '흥행 예측 인공신경망'은 LLM 점수가 아니라 실제 독자 행동 데이터(완독률·결제·이탈 지점)로 학습해야 하며, 초기에는 예측이 아니라 'A/B 노출 실험'이 현실적.

---

## 3. 상업 적용(2025~2026)

- **Netflix**: 2026-07-16 실적 발표에서 "2026년 약 300편에 GenAI 워크플로 사용", 컨셉·프리비즈·VFX·샷 플래닝·후반에 집중. 대본 자체는 WGA 협약(AI가 문학적 자료를 쓰거나 고쳐 쓸 수 없고 AI 생성물은 원천자료로 인정 안 됨)으로 인간이 작성. 출처: https://pulse2.com/netflix-says-genai-was-used-in-roughly-300-titles-in-2026/ , https://cdt.org/insights/new-wga-labor-agreement-gives-hollywood-writers-important-protections-in-the-era-of-ai/
- **CJ ENM**: 2025-06-30 'AI 스튜디오' 전략 발표 — AI Script(트렌드·소비자 데이터 기반 유망 원천 IP 발굴·장르/포맷 추천), AI Production, AI Publishing, AI Cinematic Video; 2026-05 AI 영화 '아파트'. 캐릭터·배경 3D 데이터 자동 변환으로 캐릭터 일관성 확보 주장. 출처: https://www.fnnews.com/news/202506301834563533 , https://news.mtn.co.kr/news-detail/2026050716174085893 , https://www.dt.co.kr/article/12000754
- **카카오엔터테인먼트**: AI 브랜드 '헬릭스'(큐레이션 2024-04, 숏츠 — 웹툰·웹소설을 숏폼 영상으로). 2026-09 "읽는 독자에서 만드는 팬으로" AI 2차 창작 확산 보도. 출처: https://m.ddaily.co.kr/page/view/2024043010090827373 , https://m.news.nate.com/view/20260920n01287
- **중국 숏드라마**: 2026-09-17 보도, 중국 당국 발표 인용 — 2026년 1~8월 출시 숏폼 드라마 43만 편, 그중 90% 이상에 AI 활용(출처: https://news.nate.com/view/20260917n31859 , 수치는 한국 언론의 중국 기관 인용, 중간 신뢰도). 완전 AI 생성 마이크로드라마 1편 제작비 약 10만원, 편집팀 5~6명→1명 사례(https://www.mediapia.co.kr/news/articleView.html?idxno=79038). AI 제작물 표시 의무 및 인간의 최종 심사 요구. 바이트플러스 '드라매직'(대본 입력→숏드라마 생성) 공개(https://www.aitimes.com/news/articleView.html?idxno=215569).
- **중국 웹소설 플랫폼의 역풍**(Rest of World, 2026-07-06): Tomato Novel(바이트댄스) 2026-06 한 달에 저품질(AI 포함) 투고 10.4만 건 반려, 계정별 일일 글자수 상한 도입; Jinjiang은 AI를 리서치·교정에만 허용하고 독자 신고 요청; 2025년 신작 수 400→5,606(13배). 독자: "빨리 만든 걸 읽는 건 시간 낭비". 2024-07 Tomato의 AI 학습 동의 조항(3.2.10)에 작가 집단 반발. 출처: https://restofworld.org/2026/china-ai-web-novels/ , https://news.aibase.com/news/22934 , https://news.aibase.com/news/10492
- **한국 웹소설**(머니투데이 2026-03-11): AI 사용 적발 시 '별점 테러'·연재 중단 사례, 네이버시리즈·카카오페이지는 별도 규정 없음, 문피아는 공모전에서 생성형 AI 금지, 웹소설은 웹툰보다 AI 적발이 사실상 불가. 2026-09 플랫폼들이 '복붙' AI 웹소설로 골머리(https://supple.kr/news/cmud18gqo003zi2mqvkxpnvk9). 출처: https://www.mt.co.kr/tech/2026/03/11/2026022508052980108
- **웹툰**: 2023-05 네이버웹툰 '신과함께 돌아온 기사왕님' AI 후보정 논란·보이콧, 네이버·카카오 공모전 "인간 작품만"(https://www.nocutnews.co.kr/news/5952678). 2026년 기준 플랫폼 AI 표시 정책의 구체 조문은 미확인.
- **AI 캐릭터·인터랙티브 픽션 경쟁자**: 스캐터랩 '제타'(2024-04 출시) 누적 가입자 1,300만 명 돌파(2026-09), 2026-04 일본 엔터 앱 총사용시간 1위, 2026-06 시리즈D 약 500억원, 2026-09-23 '비주얼 노벨 모드'(스토리에 따라 캐릭터·배경 실시간 변화) 정식 출시(https://zdnet.co.kr/view/?no=20260928135821 , https://platum.kr/archives/295221). 글로벌: Character.AI(18세 미만 채팅 전면 차단·연령 확인), NovelAI $10~25/월, Sudowrite $19~59/월(https://listicler.com/best/best-ai-roleplay-creative-writing-platforms). 국내 '단편.ai', '문호는 안다' 등 AI 웹소설 생성 앱 존재(품질 데이터 미확인).

---

## 4. 비용 계산(추정, 2026-10-03 공식 요금 기준)

### 4-1. 가정
- 한국어 30만 자 장편 1편 ≈ 출력 약 300K 토큰(Claude 계열 100자≈106토큰 기준; GPT/Gemini는 더 적을 수 있어 200K~320K 범위). 영어 10만 단어 ≈ 133K 토큰(≈ 한국어 케이스의 45%).
- 3패스: (1) 플롯/바이블 — 입력 10K·출력 20K, (2) 초고 — 60개 챕터 × 입력 30K(바이블+아웃라인+롤링 요약+직전 장, 대부분 캐시 가능) = 입력 1.8M·출력 300K, (3) 퇴고 — 입력 1.8M·출력 300K. 합계 입력 ≈ 3.7M(약 70% 캐시 히트 가능), 출력 ≈ 620K. 사고(thinking) 토큰 사용 시 출력이 1.2~2배가 될 수 있음.

### 4-2. 모델별 1편 비용(캐시 미사용 → 캐시 70% 적용 → Batch 50%)
| 모델(공식 단가) | 캐시 없음 | 캐시 70% | Batch+캐시 |
|---|---|---|---|
| Claude Fable 5.1 ($10/$50) | ≈$68 | ≈$43 | ≈$22 |
| Claude Opus 5.5 ($4/$20) | ≈$27 | ≈$17 | ≈$9 |
| Claude Sonnet 5 ($2/$10) | ≈$14 | ≈$9 | ≈$5 |
| gpt-5.5 ($5/$30) | ≈$37 | ≈$26 | (Batch 별도) |
| gpt-5.4 ($2.5/$15) | ≈$19 | ≈$13 | |
| gpt-5.6-sol ($4/$20) | ≈$27 | ≈$17 | |
| Gemini 3.1 Pro ($2/$12, ≤200K) | ≈$15 | ≈$10 | ≈$7 |
| Gemini 3.5 Flash ($1.5/$9) | ≈$11 | | ≈$6 |
| Kimi K2.6 ($0.65/$3.41, 집계) | ≈$4.5 | | |
| DeepSeek V4 Pro ($0.209/$0.418, 집계) | ≈$1 | | |
| Qwen3-235B ($0.09/$0.10, 집계) | ≈$0.4 | | |
- 결론: 장편 1편의 순수 API 비용은 프론티어 모델로도 수십 달러, 오픈웨이트로는 1달러 내외. **비용은 병목이 아니다.** 병목은 일관성 검증·인간 편집·독자 검증 비용이다.

### 4-3. 캐릭터 100만 개 프로필 생성
- 가정: 프로필 1개 ≈ 입력 500·출력 1,500 토큰 → 총 입력 0.5B·출력 1.5B 토큰.
- Haiku 4.5($1/$5): ≈$8,000(Batch ≈$4,000) / Sonnet 5: ≈$16,000(Batch ≈$8,000) / Gemini 3.5 Flash-Lite($0.30/$2.50): ≈$3,900(Batch ≈$2,000) / gpt-5.4-nano($0.20/$1.25): ≈$2,000 / DeepSeek V4 Flash(집계): ≈$150 / Qwen3-235B(집계): ≈$200.
- 중복 제거용 임베딩 1.5B 토큰: text-embedding-3-small($0.02/MTok) ≈$30, Gemini Embedding 2($0.20/MTok) ≈$300.
- 핵심: 100만 개는 비용 문제가 아니라 **다양성·중복·유용성** 문제. 사전 생성한 100만 개보다 "구조화 시드(성격·직업·시대·트라우마 등 조합 공간) + 온디맨드 생성 + 임베딩 기반 중복 검사"가 합리적이며, '세계 최다 보유'는 지표로서 무의미해졌다(모든 경쟁자가 즉시 복제 가능).

### 4-4. 이미지·웹툰·영상화(2026 공식/집계 단가)
- 이미지: Gemini 3.1 Flash Image ≈$0.045/장, Gemini 3 Pro Image ≈$0.134/장(1K/2K)·$0.24(4K)(공식); gpt-image-2 출력 $30/M 이미지토큰(공식, 장당 환산은 해상도 의존); FLUX.2 ≈$0.014/MP·Flux 2 Pro ≈$0.05/장, Midjourney API ≈$0.08~0.20/장(집계: https://www.digitalapplied.com/blog/ai-image-generation-api-pricing-comparison-2026).
- 웹툰 1회차(60~80컷, 컷당 3~5회 재생성 가정 → 약 300장): 원시 생성비 ≈$13~40. 실제 비용의 대부분은 캐릭터 시트·레퍼런스 관리와 인간 리터치 인건비.
- 영상: Veo 3.1 $0.40~0.60/초(공식), Sora 2 ≈$0.10/초(720p)·Pro $0.30~0.50/초, Kling ≈$0.084~0.168/초, Seedance 2.0 Fast ≈$0.011/초(집계: https://devtk.ai/en/blog/ai-video-generation-pricing-2026/ , https://atlascloud.ai/blog/guides/cheapest-ai-video-generation-api-2026). 1분 숏드라마 1화(5테이크=300초): Seedance Fast ≈$3, Kling ≈$25~50, Veo 3.1 ≈$120~180. Sora 2 API 2026-09 종료 예정이라는 집계 정보 있음(미확인).

---

## 5. 평가·안전·규제

- **AI 생성 텍스트 탐지의 한계**: 원문 그대로의 AI 출력엔 85~95% 정확도이나, 편집/휴머나이즈된 텍스트엔 3~8%까지 급락(2026 비교 테스트). Turnitin 비원어민 오탐 최대 18%, Curtin대 2026-01 AI 탐지 비활성화. 한국어 지원은 Copyleaks(30개+ 언어)가 상대적으로 넓음. 출처: https://hub.paper-checker.com/blog/ai-detector-comparison-guide-2026/ , https://gptzero.me/news/gptzero-vs-copyleaks-vs-originality/ → 플랫폼은 '탐지'가 아니라 '출처 기록(provenance)'로 가야 함.
- **워터마킹·출처 표시**: Google SynthID(텍스트는 2024년부터 Gemini에 적용, 2026-05-26 이미지·영상·오디오 1,000억 건+ 워터마킹, Content Detection API 프리뷰, Kakao·OpenAI·Nvidia·ElevenLabs 채택)(https://www.infoq.com/news/2026/05/google-synthid-content-detection/); OpenAI 2026-05-20 C2PA 가입·SynthID 이미지 워터마크(https://enterprisedna.co/resources/news/openai-content-provenance-c2pa-synthid-watermarking-2026/); Anthropic 2026-08-11 발표 — 2026-08-02 이후 출시 모델의 모든 생성 텍스트에 비가시 워터마크, 파일엔 C2PA 서명(EU AI Act 50(2)조 행동강령 서명)(https://www.revolgy.com/insights/blog/anthropic-claude-watermark-ai-text-detection , 2차 보도 기준, Anthropic 공식 문서 직접 확인은 미완). EU AI Act 투명성 의무 2026-08-02 적용, 위반 시 최대 €15M 또는 매출 3%.
- **한국 AI 기본법**: 2026-01-22 시행. 생성형 AI 결과물임을 이용자가 인식할 수 있게 고지·표시 의무, 딥페이크류는 가시적 표시 원칙, 과태료는 1년 이상 유예(계도기간). 창작 과정의 AI 활용 범위 규정은 없음. 출처: https://www.shinkim.com/kor/media/newsletter/3114 , https://thecodit.com/blog/AI-act-enforcement-decree-kr , https://www.tsisalaw.com/news/article.html?no=27856
- **저작권**: 문체부·한국저작권위원회 '생성형 AI 활용 저작물 저작권 등록 안내서'(2025-06-30; 영문판 2025-11-03) — AI 단독 생성물은 등록 불가, 인간의 창작적 기여 부분만 'AI 활용 창작물'로 등록, AI 생성 부분과 인간 창작 부분을 구분 명시 요구. 미국 저작권청 보고서 Part 2(2025-01) — 프롬프트만으로는 저작권 불가, 선택·배열·수정이 실질적이어야 함. 출처: https://www.kimchang.com/en/insights/detail.kc?sch_section=4&idx=32432 , https://www.copyright.or.kr/eng/doc/etc_pdf/Guide_to_Copyright_Registration_for_Generative_AI-Assisted_Works.pdf , https://www.jonesday.com/en/insights/2025/02/copyrightability-of-ai-outputs-us-copyright-office-analyzes-human-authorship-requirement → "IP 프로바이더"가 되려면 **인간 기여 로그(누가 무엇을 썼는지)**가 곧 권리의 근거.
- **미성년자 보호**: 캘리포니아 SB 243(2026-01-01 시행) — 동반자형 챗봇의 미성년자 보호(성적 콘텐츠 차단, AI 고지, 3시간마다 휴식 알림, 자살 위기 프로토콜); Character.AI 18세 미만 채팅 금지. 한국은 정보통신망법·청소년보호법이 사후 대응 중심이라 1:1 실시간 생성 대화에 공백, 국회에서 연령확인·보호자 동의·이용시간 제한 등 논의 중이며 통과 시 제타·크랙 등이 직접 적용 대상. 출처: https://www.gunder.com/en/news-insights/insights/client-insight-california-sb-243-new-compliance-requirements-for-operators-of-ai-companion-chatbots , https://zdnet.co.kr/view/?no=20260725131835 , https://www.newsway.co.kr/news/view?ud=2026091716220632837 . 웹소설 텍스트는 청소년유해매체물 심의(간행물윤리위) 대상이 될 수 있으므로 생성 단계 필터(폭력·성·자해) + 연령 등급 자동 분류가 필요.

---

## 6. STORY 8 기술 맵 진단: 무엇이 낡았고 무엇으로 대체되는가

| 계획서 항목(2022 인식) | 2026 진단 | 대체 |
|---|---|---|
| 블록체인(오리지널리티 검증·리워드·트래킹) | 상업 창작 플랫폼에서 블록체인 채택 사례 거의 소멸; 법적 권리 근거는 '인간 기여 기록'이지 체인이 아님 | 서명된 버전 히스토리(Git형 이벤트 로그) + C2PA 콘텐츠 자격증명 + 모델 워터마크(SynthID/Claude) + 타임스탬프 서버. 리워드는 일반 결제·정산 |
| "딥러닝으로 캐릭터 100만 개 생성" | 2026년엔 1주일·수천 달러면 누구나 생성 가능(§4-3). 보유량은 해자가 아님 | 구조화 캐릭터 바이블 스키마 + 온디맨드 생성 + 임베딩 중복검사 + 독자 반응으로 가중치가 붙는 '검증된 캐릭터' 큐레이션 |
| 300~500자 교대 집필(30~50회) | 계획 없는 국소 이어쓰기는 중반부 일관성 붕괴를 부름(Lost in Stories). 연구 SOTA는 outline-then-write·월드 스테이트 공유 | 작가가 로그라인·바이블·비트를 확정 → AI 작가실(플롯/캐릭터/대사/연속성 검수 에이전트)이 초고 → 작가 퇴고 → 검증기 통과 → 독자 공개. 교대는 '장면 단위'·'역할 단위'로 |
| 챕터 평점 강제 → 흥행 예측 신경망 | 강제 평점은 노이즈가 크고 LLM 심사관은 편향. '예측' 모델은 데이터가 쌓인 뒤에나 가능 | 행동 데이터(완독·이탈 지점·결제·재방문)를 StoryAlign형 선호 쌍으로 변환 → 자체 보상모델/DPO. 초기엔 A/B 노출 실험 |
| 스토리 업로드 플랫폼(조아라·문피아 모델) + 작가 등록비 | AI 웹소설 '복붙' 역풍(한·중 공통), 작가 유료 등록은 신뢰 훼손 | 작가 무료, AI 사용 비율·기여 로그를 독자에게 투명 표시(AI 기본법 선제 준수), 수익 배분 중심 |
| 데이터 크롤링으로 유사도 검사 | AI 텍스트 탐지는 편집본에 무력(§5) | 플랫폼 내부 임베딩 유사도(표절·자기복제) + 출처 기록. 외부 '탐지' 의존 금지 |
| Web3.0·C2E·메타버스 확장 | 용어·시장 모두 2022 기준 | 숏드라마·비주얼 노벨·AI 캐릭터 챗(제타형)·OSMU 파이프라인(이미지→영상 API) |

### 2026년 최고 수준 레퍼런스 아키텍처(요약)
1. **데이터 계층**: 캐릭터/세계관 바이블을 그래프 DB(엔티티·관계·사건·시간선)로 저장, 각 장면이 참조한 노드·버전 기록. 작가·AI 기여를 이벤트 로그로 서명 저장(저작권 등록·분쟁 대응의 근거).
2. **생성 계층(작가실 오케스트레이션)**: Showrunner(계획) → Plot/Beat 에이전트 → Character 에이전트(페르소나 기반, MAGNET 방식) → Dialogue/Prose 에이전트 → Continuity Checker(ConStory-Checker/ATLAS 방식, 그래프 대조) → Editor. 모델 라우팅: 플롯·퇴고는 프론티어(Opus 5.5/Sonnet 5/gpt-5.6/Gemini 3.1 Pro), 대량 초고·프로필은 저가 모델(Haiku 4.5/Flash-Lite/DeepSeek/Qwen), 한국어 온프레미스 필요 시 K-EXAONE/A.X/Solar 파인튜닝.
3. **인간-AI 협업 UI**: 작가는 로그라인·바이블·비트·톤을 '결정'하고 AI 초고를 '수정'한다(수정 비율이 곧 저작권 기여). 300~500자 교대가 아니라 장면·역할 단위 분업.
4. **평가 계층**: (a) 자동 — 일관성 검증기(모순 0건 통과 조건), 루브릭 LLM 심사(인간 kappa 측정·편향 통제), 내부 임베딩 유사도; (b) 인간 — 전문 편집자 샘플링; (c) 독자 — 행동 데이터(완독·이탈·결제) → 선호 쌍 → StoryReward형 보상모델 → DPO 주기 재학습.
5. **안전·규제 계층**: 생성 단계 유해 콘텐츠 필터·연령 등급 자동 분류, 미성년자 연령 확인·시간 알림(SB 243 수준 선제 적용), AI 기본법 표시 의무(기여 비율 표시), C2PA + 모델 워터마크 보존, 학습 데이터 동의 관리(Tomato 역풍 교훈).
6. **OSMU 계층**: 바이블→캐릭터 시트(Gemini 3 Pro Image/gpt-image-2, 레퍼런스 고정)→웹툰 컷·비주얼 노벨 자산→숏드라마(Kling/Veo/Seedance). 캐릭터 일관성은 3D/레퍼런스 자산으로 고정(CJ ENM 접근과 동일).
7. **비용 모델**: 장편 1편 API ≈$5~45, 숏드라마 1화 영상 ≈$3~180, 캐릭터 100만 개 ≈$150~16,000(모델별) — 모두 인건비보다 작음. 투자 논리는 '모델 보유'가 아니라 '검증된 캐릭터·독자 데이터·기여 로그'라는 데이터 자산과 작가 커뮤니티.

---

## 7. 미확인·추가 조사 필요
- STORY 8 특허(10-2022-0131471)의 등록 여부·청구항 범위(KIPRIS 확인 필요).
- 네이버시리즈·카카오페이지·문피아의 2026년 현재 AI 생성물 표시/제재 규정 원문.
- 한국어 '창작 품질' 공개 벤치마크 부재 → 자체 블라인드 독자 테스트 필요.
- 독자 반응 데이터로 DPO한 상업 사례의 1차 자료(현재 미확인).
- Sora 2 API 종료, GPT-5.5 1M 컨텍스트 등 집계 사이트 수치의 공식 확인.
- Anthropic 텍스트 워터마크의 공식 문서·탐지 API 제공 여부.

---

## 8. 보강: 모델 라우팅 매트릭스와 단계별 도입 로드맵(리서치 결과의 실행 번역)

### 8-1. 용도별 모델 선택(2026-10 기준 공식 단가·공개 지표 근거)
| 작업 | 1순위 | 대안 | 근거 |
|---|---|---|---|
| 로그라인→플롯·비트·캐릭터 바이블 설계 | Claude Opus 5.5 ($4/$20) 또는 gpt-5.6-sol ($4/$20) | Gemini 3.1 Pro ($2/$12) | 창작 리더보드 상위(Opus 5·GPT-5.6 Sol), 긴 계획 추론에 강점, 호출 수가 적어 단가 민감도 낮음 |
| 장면 초고(대량) | Claude Sonnet 5 ($2/$10) | Gemini 3.5 Flash ($1.5/$9), Kimi K2.6(집계 $0.65/$3.41) | 품질/비용 균형, 1M 컨텍스트 표준가(Claude 4.6+) |
| 연속성 검증기(모순 검출) | Gemini 3.5 Flash-Lite ($0.30/$2.50) 또는 Haiku 4.5 ($1/$5) | DeepSeek V4 Flash(집계) | 장면마다 호출되므로 저가 모델 + 그래프 대조 규칙 결합 |
| 캐릭터 프로필 온디맨드 생성 | gpt-5.4-nano ($0.20/$1.25) / Flash-Lite | Qwen3-235B(집계 $0.09/$0.10) 자체 호스팅 | 구조화 JSON 출력, 수백만 호출 전제 |
| 퇴고·문체 통일 | Opus 5.5 / Sonnet 5 | Gemini 3.1 Pro Batch($1/$6) | 작가 피드백 반영, Batch로 야간 일괄 처리 가능 |
| 한국어 온프레미스(데이터 주권·파인튜닝) | K-EXAONE 2.0 / A.X K2 / Solar Open 2 | — | 독파모 3차 진출 3사, 오픈웨이트 공개(Solar Open 2 250B, 2026-07-22) |
| 보상모델·DPO | StoryReward(공개) 초기화 → 자체 독자 데이터로 재학습 | — | StoryAlign(2026-05) 코드·데이터 공개 |

### 8-2. 단계별 도입(기술 관점, 기간은 가정)
- **0~3개월(검증)**: 작가 5~10명과 장편 3편을 '작가실 파이프라인'으로 제작. 측정 지표 — ConStory-Checker형 모순 건수/편, 작가 수정 비율(저작권 기여 근거), 블라인드 독자 테스트 완독률. 이 단계 API 비용은 편당 $10~50 수준(§4-2)으로 사실상 무시 가능.
- **3~9개월(플랫폼화)**: 바이블 그래프 DB·기여 로그·C2PA/워터마크 보존·AI 표시 UI 구축. AI 기본법 표시 의무와 저작권 등록 안내서 요건(AI 생성/인간 창작 구분)을 제품 데이터 모델에 내장.
- **9~18개월(데이터 플라이휠)**: 독자 행동 데이터 → 선호 쌍 → 보상모델 → DPO 주기 재학습. 이때부터 '흥행 예측'이 아니라 '선호 정렬'이 가능해짐. 미성년자 보호(연령 확인·시간 알림·유해 필터)는 캐릭터 챗 기능 도입 전에 선행.
- **18개월~(OSMU)**: 검증된 IP만 웹툰·비주얼 노벨·숏드라마로 확장. 영상 단가(§4-4)가 낮아 '다작·저비용 테스트 → 반응 좋은 IP에 인간 제작비 집중' 구조가 가능.

### 8-3. 리스크 요약
- 독자 역풍: 한·중 모두 AI 티가 나는 웹소설에 별점 테러·시간 낭비 인식(§3). 투명 표시 + 인간 편집 품질 보증이 없으면 플랫폼 신뢰가 먼저 무너진다.
- 규제: AI 기본법 표시 의무(과태료 유예 중), EU AI Act 2026-08-02 적용(해외 서비스 시), 미성년자 보호 입법(국회 논의 중).
- 기술: 프론티어 모델 가격·토크나이저 변동(Claude 4.7+ 토큰 30% 증가, GPT-5 계열 2026-04 단가 2배)이 비용 모델에 직접 영향 → 모델 추상화 계층·라우팅 필수.
- 데이터: 작가 원고를 AI 학습에 쓰려면 명시적 동의·보상 설계 필요(Tomato Novel 3.2.10 조항 역풍).
