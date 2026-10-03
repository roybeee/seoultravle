# 글로벌 AI 네이티브 스토리·픽션·캐릭터 플랫폼 경쟁 지형 (2026-10-03 기준)

작성: AI·콘텐츠 산업 리서치 (STORY 8 사업계획서 분석 입력용)
방법: WebSearch 27회(한·영, extended 모드 위주) + 1차 출처 WebFetch 검증. 수치는 모두 "기준 시점"을 병기했고, 1차 출처(회사 공시·공식 페이지·주요 언론)로 확인되지 않은 항목은 **미확인** 또는 신뢰도(중/하)로 표시했다. 2차 통계 사이트(sqmagazine, udonis, aicompanionpick 등)의 수치는 참고용으로만 썼다.

---

## 0. 한 줄 결론

2026년 현재 "AI와 사람이 함께 이야기를 만드는 플랫폼"은 더 이상 희소한 개념이 아니다. 돈이 되는 것은 **캐릭터 챗(소비자 구독)** 이고, 작가용 AI 집필 도구는 월 $10~44의 소규모 SaaS이며, 웹소설 플랫폼들은 오히려 **AI 생성 텍스트를 규제·배제**하는 방향으로 움직이고 있다. STORY 8이 내세운 "세계 최초 AI-작가 협업 창작 시스템"이라는 포지셔닝은 2026년 시장에서 성립하지 않으며, 계획서의 핵심 수익 가정(참여작가 등록비, 독자 평점 기반 AI 학습, 블록체인 저작권)은 선행 사례의 교훈과 정면으로 어긋난다.

---

## 1. 소비자용 AI 캐릭터챗·인터랙티브 픽션

### 1-1. 시장 규모와 투자자 지표
- Appfigures 집계(TechCrunch, 2025-08-12): AI 컴패니언 앱 카테고리는 2025년 상반기 매출 $82M, 연간 $120M 초과 전망. 상반기 다운로드 6,000만 건(+88% YoY), 활성 수익 앱 337개 중 2025년 신규 128개. 상위 10% 앱이 카테고리 매출의 89%를 가져가는 극단적 승자독식. 다운로드당 매출(ARPD) $0.52(2024)→$1.18(2025). https://techcrunch.com/2025/08/12/ai-companion-apps-on-track-to-pull-in-120m-in-2025
- Sensor Tower 기반 2차 집계(신뢰도 중): 2026년 1분기 AI 컴패니언 앱 매출 약 $150M, 2023년 1분기 대비 12배 이상. 미국 이용자 2026년 1분기 컴패니언 앱 사용시간 약 7.05억 시간(데이팅·소셜디스커버리 2.8억 시간의 2.5배). https://voxbooster.com/blog/ai-companion-apps-statistics-2026/ , https://track360.io/blog/ai-companion-industry-report-market-size-growth-retention-2026
- 투자자가 보는 핵심 지표(2차 분석 종합, 신뢰도 중): (1) 리텐션이 최대 제약 — 월간 구독의 12개월 유지율이 한 자릿수%까지 떨어지는 경우가 흔함, (2) DAU/MAU(스티키니스), (3) 무료→유료 전환율(낮은 한 자릿수%), (4) ARPU 밴드: 광고형 <$2/년, 하이브리드 $3~15, 구독주도 $30~100+, (5) 유료 사용자 LTV는 비AI 구독앱 대비 약 40% 높지만 이탈도 가장 빠름. https://tripleminds.co/blogs/strategies/ai-companion-cac-ltv-churn-benchmarks/ , https://track360.io/blog/ai-companion-industry-report-market-size-growth-retention-2026
- a16z "Top 100 Gen AI Consumer Apps" 2026년 3월호(2026-03-09)는 범용 어시스턴트·에이전트·크리에이티브 툴 중심으로 논평하며 캐릭터챗 카테고리를 별도로 부각하지 않음(요약 기준, 신뢰도 중). https://www.a16z.news/p/top-100-gen-ai-consumer-apps-march

### 1-2. Character.AI (미국)
- 규모: MAU 2,000만(Sacra, 2024년 초 기준). 2차 통계 사이트는 2024년 중반 2,800만 피크→2026년 초 약 2,000만으로 감소했다고 집계(신뢰도 중). 연환산 매출 $30M(2025-07, Sacra 추정), 2025년 말 $50M 목표. 구독 c.ai+ $9.99/월. https://sacra.com/c/character-ai/ , https://sqmagazine.co.uk/character-ai-statistics/
- 구글 딜: 2024년 구글이 약 $2.7B에 비독점 모델 라이선스 + 공동창업자(Noam Shazeer, Daniel De Freitas) 재영입. 이후 Character.AI는 자체 모델 개발을 접고 Meta·DeepSeek 등 오픈소스 모델로 전환(Sacra). https://sacra.com/c/character-ai/
- 미성년자 이슈: 2025-10-29 발표, 2025-11-25부로 18세 미만 오픈엔드 챗 전면 차단, 연령추정(자체 모델+Persona) 도입. 같은 날 18세 미만용 대안으로 **"Stories"(가이드형 인터랙티브 픽션, 선택지 기반)** 출시 — CEO Karandeep Anand: "18세 미만에게 오픈엔드 챗은 아마 답이 아니다". https://techcrunch.com/2025/11/25/character-ai-will-offer-interactive-stories-to-kids-instead-of-open-ended-chat/
- 소송: 2026-01-07~08 Character.AI와 구글이 플로리다(Sewell Setzer 사건)·콜로라도·뉴욕·텍사스 유족 소송을 비공개 조건으로 합의(책임 인정 없음). https://gulfnews.com/world/americas/google-characterai-agree-to-settle-suits-involving-teen-suicide-1.500401643 , https://www.cnn.com/2026/01/07/business/character-ai-google-settle-teen-suicide-lawsuit

### 1-3. Talkie / MiniMax (중국)
- MiniMax는 2026년 1월 홍콩거래소 상장(HKEX: 0100). 누적 조달 $1.15B, 2025-07 시리즈B 연장 후 기업가치 $4B. Sacra 추정 연환산 매출: 2025년 말 $100M → 2026-02 $150M+ → 2026-04 $400M → 2026-08 $800M(API 비중 급증). https://sacra.com/c/minimax/
- 상장 투자설명서 기반 보도(신뢰도 중): 2025년 1~9월 매출 $53.4M 중 소비자 앱 71%, Talkie 단독 35%. Talkie/Xingye 평균 MAU 2023년 310만→2025-09 2,760만, 유료 사용자 177만, ARPPU $6(2023)→$15. https://news.futunn.com/en/post/66478828/in-depth-analysis-of-the-unicorn-ai-large-model-prospectus
- 교훈: 캐릭터챗 자체는 MiniMax 전체 매출에서 "이미 소수"가 됐고, 회사 가치는 모델 API로 이동 중. 앱 사업만으로는 밸류에이션이 서지 않는다.

### 1-4. Chai (미국·영국)
- 회사 공식 페이지(2026-10-01 기준): ARR $120M, DAU 100만+, 최근 12개월 사용자 1,000만+, 직원 15~20명, 누적 조달 $55M(CoreWeave, AMD Ventures 등), "마케팅비 제외 흑자". 2025년 ARR $40M → 2026-07 $100M. 비즈니스 모델은 구독+인앱결제, 모델은 오픈소스 기반 자체 포스트트레이닝. https://www.chai-research.com/company-facts/
- 2026-04-30 보도자료: ARR $80M, 기업가치 $2.4B 협상 중, 3년 연속 3배 성장. https://www.prnewswire.com/news-releases/chai-ai-backed-by-coreweave-and-amd-hits-80m-arr-with-talks-of-2-4b-valuation-302759626.html
- 교훈: UGC 캐릭터(사용자가 만든 캐릭터를 다른 사용자가 소비) + 극단적 소수 인력 + 오픈소스 모델 = 가장 자본효율적인 성공 사례.

### 1-5. PolyBuzz, Replika, Tolan
- PolyBuzz(구 Poly.AI): 2차 집계 기준 MAU 1,300만, 누적 다운로드 4,280만~5,600만, 매출 $8.3M(2026, 신뢰도 하). MAU 대비 매출이 매우 낮은 "볼륨형" 앱. https://www.blog.udonis.co/mobile-marketing/mobile-apps/top-ai-apps
- Replika(Luka): 사용자 4,000만+(2025, Wikipedia), 유료 비율 약 25%(시점 미상). 2025-05-19 이탈리아 Garante가 법적 근거 없는 데이터 처리·연령확인 부재로 €5M 과징금, 학습데이터 사용은 별도 조사. 2025-01 Tech Justice Law Project 등이 FTC에 기만적 설계 민원. https://en.wikipedia.org/wiki/Replika , https://www.bipc.com/european-authority-fined-emotional-ai-company-for-privacy-violations
- Tolan(Portola): 2025-02 시드 $10M(Lachy Groom) → 2025-07 시리즈A $20M(Khosla Ventures/Keith Rabois), 반년 만에 $30M. 다운로드 300만+, 유료 10만+, 월매출 $100만+, 가격 $4.99/주·$10/월·$70/년, 직원 12명. 의도적으로 비인간(외계인) 캐릭터·"폰을 내려놓게 하는" 반중독 설계로 규제 리스크를 회피. https://eu.36kr.com/en/p/3378446113298949 , https://www.geekwire.com/2025/ai-companionship-app-tolan-raises-20m-to-help-more-people-grow-with-a-virtual-alien-friend/

### 1-6. 인터랙티브 픽션: AI Dungeon/Latitude, Hidden Door, Sekai, Giant
- Latitude(AI Dungeon, 2019~): 2026-04-21 창작자가 세계관·규칙을 설계하고 NPC와 비스크립트 상호작용하는 플랫폼 **Voyage** 출시. 투자자 Google AI Futures Fund, Midjourney, Griffin Gaming Partners, NFX, Album VC, 전 Roblox CBO Craig Donato(이사). 5년 개발한 "World Engine", 베타에서 AI 캐릭터 16만 개 생성. 요금제 무료 + $15/$30/$50 월 구독. 조달액 비공개. https://techcrunch.com/2026/04/21/voyage-is-an-ai-rpg-platform-for-creating-custom-gaming-worlds-with-ai-generated-npc-interactions/
- Hidden Door(Hilary Mason): 2025-08 얼리액세스(텍스트 웹, 과금 미시작, 2025-10-20 기준). **라이선스 IP 안에서 팬이 이야기를 플레이** — The Crow(Pressman Film), Dead Man's Tale(Alan Dean Foster), 831 Stories(로맨스), 퍼블릭도메인(오만과 편견, 오즈, 크툴루). Audible식 크레딧 모델, IP 보유자와 직접 수익 배분. 누적 조달 약 $7M(Tracxn, 신뢰도 중). Mason: "기계는 창의적이지 않다. 창의성은 작가에게서 나온다" — 스토리 비트는 내러티브 디자이너가 결정. https://aigamechangers.substack.com/p/the-machine-is-not-itself-creative , https://tracxn.com/d/companies/hidden-door/__DEEpimT5lup2Ka4OsbHxTGewc-6mqkwjQXwWx_E49y4
- Sekai: 2024-12-05 시드 $3.1M(Hashed 리드, a16z CSX, Azuki, Orange DAO). Story Protocol(IP 전용 L1 블록체인, 개발자 메인넷 2025-01-19) 위에서 "여러 사람+AI 공동 창작, IP 토큰화·수익화" 표방. 사용자 수는 홍보성 기사("수백만 크리에이터")만 있고 1차 확인 **미확인**. https://www.theblock.co/post/329456/story-protocol-based-ai-startup-sekai-raises-3-million-in-seed-round-led-by-hashed
- Giant(아동용 개인화 스토리): 시드 $8M(Matrix 리드, Griffin Gaming 등), 2025-05 출시 후 개인화 에피소드 20만+ 생성, 광고·추적 없음(기사 게재일 표기 불일치, 2025~2026 사이로 추정). https://www.edtechinnovationhub.com/news/giant-raises-8m-to-scale-ai-driven-interactive-storytelling-for-children
- 폐업·철수 사례: Lore Machine(AI 비주얼 스토리텔링, 2022 설립)은 Tracxn 기준 "무펀딩" 상태로 사실상 정체(폐업 여부 미확인). 카카오엔터 Radish(웹소설) 2025년 서비스 종료, Tapas 2026-09-22 종료 발표(아래 3장). Naver/Wattpad WEBTOON의 Yonder(한국 웹소설 영역 앱) 2025-07-31 종료.

### 1-7. 한국: 제타(스캐터랩), 크랙(뤼튼)
- 제타: 2025-07-14 기준 2025년 2분기 매출 52억원·영업이익 9억원, 3분기 연속 흑자, 가입자 약 300만·MAU 110만, 월 대화량 23억 건, 일본 DAU 1위(앱에이프). https://www.unicornfactory.co.kr/article/2025071414555512583
- 2026-06-14 서울경제 단독: 시리즈D 500억원(에이티넘·SBVA·미래에셋벤처), 2025년 연매출 약 260억원·영업이익 약 30억원, 누적 가입 600만·MAU 140만(2026-05), 일본 WAU 약 75만·1인당 일평균 약 4시간. 같은 기사 인용 모바일인덱스: 크랙 MAU 55만(2026-05). "AI 캐릭터 채팅을 제외하고 매출이 나오는 (생성 AI 소비자 서비스는) 거의 없다". https://www.sedaily.com/article/20055557
- 네이버웹툰 '캐릭터챗'·카카오엔터 AI 챗 서비스 관련 수치는 기사 본문에서 재확인 불가 → **미확인**.

### 1-8. 규제 지형(2025~2026)
- 캘리포니아 SB 243(2025-10-13 서명, 2026-01-01 시행): 컴패니언 챗봇 사업자에 AI 고지, 미성년자 대상 3시간마다 휴식 알림, 자해 위기 프로토콜 의무. 텍사스 TRAIGA(HB 149, 2026-01-01 시행) 챗봇 고지 의무, 위반 시 최대 $200,000. https://natlawreview.com/article/ai-regulatory-update-californias-sb-243-mandates-companion-ai-safety-and , https://fpf.org/blog/understanding-the-new-wave-of-chatbot-legislation-california-sb-243-and-beyond/
- FTC 6(b) 조사(2025-09-11): Alphabet, Character Technologies, Meta, OpenAI, Snap, xAI 등 7개사에 안전성 테스트·참여 기반 수익화·COPPA 준수 자료 요구. https://www.kelleydrye.com/viewpoints/blogs/ad-law-access/ai-chatbots-face-rising-legal-and-legislative-scrutiny
- 함의: 캐릭터챗은 2026년부터 **연령확인·고지·위기대응이 기본 비용**인 카테고리가 됐다. 한국 AI기본법(2026-01 시행)과 결합하면 STORY 8류 서비스도 설계 단계에서 컴플라이언스를 넣어야 한다.

---

## 2. 작가용 AI 집필 도구

| 도구 | 가격(2026) | 핵심 기능 | 비고 |
|---|---|---|---|
| Sudowrite | Hobby $10 / Pro $22 / Max $44 월, 크레딧제(22.5만~200만) | Write·Rewrite·Describe·Expand, 스타일 매칭, 시리즈 연속성, 자체 소설 특화 모델 Muse·Ballad + 30여 외부 모델, 입력물 권리 불주장 | 공식 가격 페이지 확인. "10만 작가" 주장은 마케팅 자료(신뢰도 중) |
| NovelAI (Anlatan) | $10~25/월(2차 자료) | Lorebook(세계관·캐릭터 일관성), 자체 모델(Erato 등), 이미지 생성, 암호화 저장 | 사용자 수·매출 **미확인** |
| NovelCrafter | $4~20/월 + 외부 모델 API 비용(BYO키) | 코덱스(스토리 바이블), 모델 자유 선택 | 2차 자료 |
| Squibler | Pro $29/월 | Smart Writer, 코르크보드, 텍스트→이미지 | 2차 자료 |
| Jasper | Pro $69/월, Business 맞춤 | 마케팅 카피 중심, 픽션 포기 | 2차 자료 |

출처: https://sudowrite.com/pricing , https://www.eesel.ai/blog/ai-novel-writing-software , https://blog.mylifenote.ai/the-11-best-ai-tools-for-writing-fiction-in-2026/ , https://www.demandsage.com/jasper-ai-pricing/ , https://reedsy.com/studio/resources/squibler-review/

2025~2026 변화: (1) 범용 LLM이 아닌 **소설 특화 파인튜닝 모델**(Sudowrite Muse 1.5, 2025년 중반 공개)로 차별화, (2) 스토리 바이블/로어북이 표준 기능이 되어 "캐릭터 일관성"은 더 이상 차별점이 아님, (3) 가격은 월 $10~44에 고정, 크레딧제로 전환, (4) 작가 데이터 권리 불주장이 신뢰의 전제 조건. 중국 Caiyun Xiaomeng, 덴마크 Laika(2022~, 활동 중), 구글 Wordcraft(2022 연구 프로젝트) 등 "AI와 이어쓰기" 도구는 2021~2022년에 이미 다수 등장했다.

---

## 3. 웹소설·연재 플랫폼의 AI 정책

### 3-1. Wattpad / WEBTOON Entertainment (Naver 계열)
- Wattys 2026 공모 규정: "생성형 AI로 스토리를 쓰는 것을 강력히 권장하지 않음". 편집·개요·조사·문법 교정용 AI는 허용. AI 생성 콘텐츠는 **저작권 보호를 못 받을 수 있고**, 출판·영상화·상금 자격에 영향, "도구 선택의 모든 리스크는 창작자 책임". https://www.wattpad.com/1619601800-the-wattys-2026-the-entry-requirements
- Wattpad 사장 David Lee(2026-05-28): "세계 최고의 스토리텔러인 인간을 대체하려는 건 좋은 사업이 아니다". AI는 아이디어·제작기간 단축 보조로만. AI 저품질 범람 대응은 "독자와 팬이 인기를 결정" — 별도 검출 정책 없음. Wattpad+WEBTOON 합산 MAU 약 1.45억, 창작자 2,700만+, 웹소설 6,700만 편. https://www.theglobeandmail.com/culture/article-wattpads-new-president-david-lee-on-ai-fandoms-and-sending-stories-to/
- 재무: WEBTOON Ent. FY2025 매출 +3.9%(환율중립), 조정 EBITDA $19.4M(전년 $68M), 2025년 4분기 영업권 손상으로 순손실 $336.5M, 글로벌 MAU 1.57억(-7.1%). Wattpad의 광고 모델 전환이 수익 개선으로 이어지지 않아 손상 발생(SEC ARS). AI는 "개인화 추천"에 집중, 한국에서 유료 전환 개선. https://www.gurufocus.com/news/8675399/webtoon-entertainment-inc-wbtn-q4-2025-earnings-call-highlights-strategic-disney-partnership-and-ai-innovations-amidst-revenue-challenges , https://www.sec.gov/Archives/edgar/data/0001997859/000199785926000057/ars.pdf
- Yonder(한국 웹소설 영역 앱) 2025-07-31 종료. https://www.animenewsnetwork.com/news/2025-02-02/serialized-fiction-app-yonder-to-end-service-on-july-31/.220746

### 3-2. Webnovel / 阅文(China Literature, Tencent)
- 2025년 상반기 실적(공식 보도자료): 매출 RMB 3,190.6M(-23.9% YoY). WebNovel: 중국어 번역작 1만+ 중 **AI 번역 7,200편(번역작의 70%)**, AI 번역작 매출 +38%, WebNovel 소설 매출의 35% 이상. 현지 창작 오리지널 77만 편. 작가용 "Writer Assistant" DAU +40%, **주간 AI 사용률 약 70%**. https://www.prnewswire.com/apac/news-releases/china-literature-announces-2025-interim-results-302527570.html
- 2025년 연간: AI 번역작 17,000편+(중국사회과학원 보고서, 2026-04-14 China Daily). 중국 온라인문학 산업 해외 매출 56.4억 위안(약 $820M, +11.2%), 해외 활성 사용자 약 2억, 현지 창작자 130만. https://www.chinadaily.com.cn/a/202604/14/WS69de142fa310d6866eb435ec.html
- **역풍(Rest of World, 2026-07-06)**: 번치(ByteDance 番茄/Tomato)는 작가 계정에 일일 글자수 제한, 6월 한 달 "저품질" 투고 10.4만 건 반려. 晋江(Jinjiang) 창업자는 AI를 조사·교정으로만 제한, 독자에게 AI 의심작 신고 요청. 독자 불만("빨리 찍어낸 걸 읽는 건 시간 낭비", 프롬프트가 본문에 노출된 사례). 자동 집필 시스템 InkOS 다운로드 5만+. https://restofworld.org/2026/china-ai-web-novels/
- 2024-07 번치 "AI 학습 보충협약" 사태: 작품을 AI 학습에 쓰고 생성물은 플랫폼 소유 → 웨이보 1,800만 뷰 반발 → 2024-07-23 해지 기능 제공. https://asiaiplaw.com/article/bytedance-web-novel-platforms-ai-clause-sparks-author-outrage

### 3-3. Inkitt / Galatea
- 2024-02-26 시리즈C $37M(Khosla 리드, NEA, Kleiner Perkins), 포스트머니 약 $400M, 누적 $117M, 사용자 3,300만. AI 용도: 인간이 쓴 트리트먼트 기반 스토리 생성, 독자별 개인화, 제목·훅·클리프행어 A/B, DeepL 번역, ElevenLabs 오디오북, Leonardo 표지. CEO Ali Albazaz: "LLM은 매우 나쁜~평균 수준의 글을 쓴다. LLM만으로는 베스트셀러를 못 만든다". https://techcrunch.com/2024/02/26/inkitt-ai-publishing-37-million
- Bloomberg(2025) "AI 로맨스 공장": Galatea 약 400명 작가 카탈로그를 편집장 1명+"스토리 인텔리전스 분석가" 5명이 AI로 반복 수정(신뢰도 중). 2026년 마이크로드라마 플랫폼 "Ironblood" 발표, 2026-05 세컨더리 거래(PitchBook). https://www.bloomberg.com/features/2025-ai-romance-factory/ , https://pitchbook.com/profiles/company/123047-02
- 교훈: Inkitt는 "AI-작가 협업"을 공개 슬로건이 아니라 **내부 제작 파이프라인**으로 쓰고, 독자 데이터(완독률·이탈)로 어떤 작품을 밀지 결정한다. 작가에게 돈을 받는 게 아니라 작가 작품을 사들여(계약) 증폭한다.

### 3-4. 카카오엔터(Tapas·Radish), Royal Road, ScribbleHub, 한국 플랫폼
- 카카오엔터: Radish 2025년 종료, Tapas 2026-09-22 종료 발표(2차 보도 기준 서비스 종료 2027-03-31, 창작자 7.5만·작품 10만·누적 가입 1,000만 — 신뢰도 중). 2021년 인수액은 영문 기사의 "$8.4B"가 원화 오역으로 보여 **미확인**(당시 보도는 약 1.1조원). 카카오페이지·카카오웹툰은 2026년 내 통합, "이용자 구독 패턴 데이터 통합 + AI 역량 접목"으로 고도화(2026-09-22 파이낸셜뉴스). https://www.mt.co.kr/en/tech/2026/09/22/2026092118091880735 , https://www.animenewsnetwork.com/news/2026-09-22/kakao-entertainment-to-shut-down-n-american-webtoon-platform-tapas/.242090 , https://www.fnnews.com/news/202609221508350424
- Royal Road: "AI-Assisted"(교정·편집 수준, 작가 창의성·구조 유지) vs "AI-Generated"(작가가 프롬프트·편집) 분류와 태그 요구(공식 블로그 페이지 접근 차단으로 검색 요약 기준, 신뢰도 중). ScribbleHub: "대부분 AI로 쓴 작품은 반려". https://www.royalroad.com/blog/57/royal-road-ai-text-policy , https://forum.scribblehub.com/threads/update-content-warnings-to-include-ai-usage.21730/page-5
- 한국(머니투데이 2026-03-11): 웹소설은 AI 사용 고지 의무가 없고 플랫폼 심의는 선정성·폭력성 중심이라 **AI 사용 판별이 사실상 불가**. 독자는 AI 개입이 인지되는 순간 "별점 테러". 문체부 가이드라인 검토 중, 웹툰은 표기·워터마크 가이드 정비 추세이나 웹소설은 지침 부재. https://www.mt.co.kr/tech/2026/03/11/2026022508052980108

---

## 4. 2025~2026 주요 딜·M&A·폐업 요약

| 시점 | 기업 | 내용 |
|---|---|---|
| 2024-12 | Sekai | 시드 $3.1M(Hashed) — Story Protocol 기반 공동창작 |
| 2025-02/07 | Tolan(Portola) | 시드 $10M → 시리즈A $20M(Khosla) |
| 2025-05 | Replika | 이탈리아 €5M 과징금 |
| 2025-07 | MiniMax | 시리즈B 연장 $300M, $4B → 2026-01 홍콩 상장 |
| 2025-07 | 스캐터랩 | 3분기 연속 흑자 공개 |
| 2025-08 | Hidden Door | 얼리액세스, 라이선스 IP 모델 |
| 2025-09 | FTC | 7개사 6(b) 조사 |
| 2025-10/11 | Character.AI | SB 243 서명, 18세 미만 챗 차단, "Stories" 출시 |
| 2026-01 | Character.AI/Google | 유족 소송 합의 |
| 2026-01 | Holywater | $22M(Horizon Capital), 앱 설치 1억+, AI 시리즈 생성 "My Muse" |
| 2026-02 | Holywater | AI VFX 스튜디오 Jeynix 인수 |
| 2026-04 | Latitude | Voyage 출시(Google AI Futures Fund 등) |
| 2026-04 | Chai | ARR $80M, $2.4B 협상 → 2026-10 ARR $120M |
| 2026-06 | 스캐터랩 | 시리즈D 500억원 |
| 2026-07 | 중국 플랫폼 | AI 소설 규제 강화(번치·진장) |
| 2026-09 | 카카오엔터 | Tapas 종료 발표, 카카오페이지 통합 |
| 2026-09 | 인도 | AI 스토리 스타트업 4곳 $64M(2차 보도, 신뢰도 하) |

출처: 위 각 절 및 https://en.wikipedia.org/wiki/Holywater_(company) , https://techinnovators.in/startups/why-the-64-million-funding-surge-in-ai-interactive-content-i-608234

---

## 5. "AI와 인간 작가의 협업 플랫폼" 선행 사례와 교훈

1. **Google Wordcraft Writers Workshop(2022)**: 전문 작가 13명이 8주간 LaMDA와 공동 집필. 결론은 "AI는 작가를 대체하지 못하지만 과정을 빠르고 재밌게 할 수 있다". 그러나 참여 작가들은 이후 "모든 창작자를 배신했다"는 보이콧 압박을 받았다(Engadget). 교훈: **작가 커뮤니티의 정서적 반발**이 제품 기능보다 더 큰 리스크. https://wordcraft-writers-workshop.appspot.com/ , https://www.engadget.com/2234838/authors-face-backlash-for-participation-in-2022-google-ai-study/
2. **AI Dungeon → Voyage(2019~2026)**: 턴제 "사용자 한 줄, AI 한 단락" 모델의 원조. 7년 만에 "작가가 세계·규칙을 설계하고 AI는 실행"하는 창작자 플랫폼으로 진화. 교훈: 교대 집필 자체는 2019년 UX이며, 가치는 **세계관 설계권과 창작자 경제**로 이동.
3. **Character.AI Stories(2025-11)**: 오픈엔드 챗의 안전 리스크를 "가이드형 인터랙티브 픽션"으로 우회. 교훈: 규제 환경에서 **경계가 있는 스토리 포맷**이 오히려 성장 여지.
4. **Hidden Door**: "AI는 창의적이지 않다, 작가가 창의적이다" — 작가·IP 보유자가 스토리 비트를 정하고 AI는 즉흥 실행, 수익은 IP 보유자와 배분. 교훈: 협업의 설득력은 **인간 작가에게 돈과 크레딧이 흐르는 구조**에서 나온다.
5. **Inkitt**: 독자 데이터 기반 선별 + 내부 AI 증폭. 교훈: "독자 평점으로 AI를 학습"보다 **완독·리텐션 데이터로 어떤 인간 작품에 투자할지**를 고르는 게 검증된 모델.
6. **중국 웹소설 플랫폼(2023 장려 → 2026 규제)**: AI 집필 장려가 저품질 범람·독자 이탈·작가 저작권 반발로 되돌아옴. 교훈: AI 생성 본문을 독자에게 직접 파는 모델은 **독자 신뢰를 소모**한다.
7. **Sekai/Story Protocol**: 블록체인 IP 등록을 결합한 유일한 공동창작 사례이나 실사용 트랙션 미확인. 교훈: 2022년식 "블록체인 오리지널리티 검증"은 2026년 투자자에게 가산점이 아니라 감점 요인.

---

## 6. STORY 8의 2026년 위치 평가

- "세계 최초 AI-작가 협업 창작 시스템": **성립하지 않음.** AI Dungeon(2019), Wordcraft(2022), Sudowrite/NovelAI(2021~), Caiyun·Laika, Sekai(2024), Character.AI Stories(2025), Hidden Door(2025), Voyage(2026)가 모두 선행. 특허 10-2022-0131471은 "캐릭터 창출 방법" 특허이지 협업 시스템의 선점을 의미하지 않으며 등록 여부 미확인.
- 300~500자 교대 집필 + 챕터별 강제 평점: 독자 입장에서는 2019년 AI Dungeon보다 느리고, 작가 입장에서는 Sudowrite($10/월)보다 통제권이 적다. 교대 집필로 생긴 본문은 조아라·문피아·Wattpad·Royal Road 어디서도 환영받지 못하고(저작권 불확실·AI 태그·별점 테러), 중국 사례처럼 독자 신뢰를 깎는다.
- 참여작가 "등록비·참여비": 경쟁자들은 전부 창작자에게 **지급**(Hidden Door 수익배분, Voyage 창작자 경제, Chai UGC, Inkitt 계약금). 거꾸로 받는 구조는 작가 공급 자체를 막는다.
- 블록체인·메타버스·C2E: 2026년 투자자 체크리스트(리텐션, DAU/MAU, 전환율, ARPPU, 안전 컴플라이언스, 토큰당 원가)에 없는 항목.
- 유효한 자산: (1) 구조화된 캐릭터 DB(OCT UNIVERSE)의 아이디어 — Hidden Door·Voyage처럼 "세계관·캐릭터를 설계하는 인간 + 실행하는 AI" 구조와 호환, (2) 한국 시장에서 제타가 증명한 캐릭터챗 수요(MAU 140만, 흑자, 일본 WAU 75만), (3) 카카오엔터가 북미를 접고 AI·데이터 중심으로 재편하는 지금이 **국내 IP 공급 파트너**가 비는 시점.
- 결론: STORY 8은 "AI 공동 집필 웹소설 플랫폼"이 아니라 **"인간 작가가 설계한 캐릭터·세계관을 AI가 실시간으로 연기하는 캐릭터 인터랙티브 픽션 + IP 라이선싱"** 으로 재정의해야 2026년 시장 언어에 맞는다. 수익 엔진은 (a) 캐릭터챗 구독/인앱(검증됨), (b) 작가·IP 보유자와의 수익배분형 라이선스(Hidden Door형), (c) 독자 데이터 기반 IP 선별→2차 저작(Inkitt형) 순서여야 한다.


## 7. 포지셔닝 맵: STORY 8이 들어갈 수 있는 빈칸

경쟁 지형을 두 축(① 창작 주체: 플랫폼/AI 중심 ↔ 인간 작가·IP 중심, ② 소비 형태: 읽기 중심 ↔ 상호작용 중심)으로 놓으면 네 사분면이 나온다.

- **AI 중심 × 읽기**: 중국 번치·진장의 AI 양산 소설, InkOS. 2026년에 독자·플랫폼 양쪽에서 거부당한 영역. STORY 8의 교대 집필 결과물은 독자 눈에는 이 사분면으로 분류될 위험이 크다.
- **AI 중심 × 상호작용**: Character.AI, Chai, Talkie, PolyBuzz, 제타, 크랙. 매출은 가장 크지만 UGC 캐릭터가 수천만 개라 품질·IP 차별화가 어렵고, 미성년자 규제의 직격탄을 맞는 영역.
- **인간 작가 중심 × 읽기**: Wattpad, 카카오페이지, 문피아, Royal Road, Inkitt. AI는 추천·번역·편집 보조로만 허용. 신규 플랫폼이 들어가기엔 기존 네트워크 효과가 너무 크다.
- **인간 작가 중심 × 상호작용**: Hidden Door, Voyage, Character.AI Stories, Sekai. 2025~2026년에 투자자(Google AI Futures Fund, Midjourney, Griffin, Khosla 계열)가 새로 돈을 넣는 영역이며, 아직 지배적 승자가 없고 **한국어·K-IP 기반 플레이어가 부재**하다.

STORY 8의 현재 설계는 1사분면(AI 중심 × 읽기)에 가깝지만, 보유 아이디어(작가가 만든 캐릭터 아카이브, 관계도 기반 시뮬레이션)는 4사분면(인간 작가 중심 × 상호작용)의 핵심 부품이다. 업그레이드의 방향은 "같은 부품으로 사분면을 옮기는 것"이다: 작가는 캐릭터·세계관·스토리 비트를 설계해 권리를 유지하고, AI는 독자와의 실시간 상호작용을 연기하며, 플랫폼은 구독·크레딧 매출을 작가와 나누고 완독·체류 데이터로 2차 저작 IP를 선별한다. 이렇게 하면 Wattpad·카카오페이지의 AI 정책과도 충돌하지 않고(본문은 인간 집필), SB 243·AI기본법형 규제에는 "경계가 있는 스토리 포맷"으로 대응할 수 있다.

---

## 8. 수익모델 비교: 무엇이 실제로 돈을 벌고 있는가

| 모델 | 대표 사례 | 검증 수준(2026) | 단위경제 특징 |
|---|---|---|---|
| 캐릭터챗 구독·인앱 | Chai(ARR $120M), Talkie(MiniMax 소비자 매출의 핵심), 제타(연매출 260억원·흑자), Tolan(월 $1M+) | 가장 강함. 소수 인력으로 흑자 가능 | 유료 전환 낮으나 헤비유저 ARPPU 높음($15, Talkie). 12개월 유지율 낮음. 토큰 원가가 매출원가의 핵심 |
| 작가용 집필 SaaS | Sudowrite($10~44), NovelAI, NovelCrafter | 안정적이나 소규모. 상한이 명확 | 크레딧제로 원가 전가. 작가 데이터 권리 불주장이 필수 |
| 라이선스 IP 인터랙티브 픽션 | Hidden Door(크레딧, IP 보유자 수익배분), Character.AI Stories | 초기. 과금 미시작(Hidden Door) | IP 보유자와의 계약이 공급 병목. 안전·연령 규제에 가장 유리 |
| 창작자 경제형 세계관 플랫폼 | Voyage($15/30/50 구독), Chai UGC 캐릭터 | 성장 초기(Voyage 2026-04 출시) | 창작자가 공급을 만들고 플랫폼은 실행 엔진·결제·발견을 제공 |
| 독자 데이터 기반 IP 증폭·2차 저작 | Inkitt/Galatea(~$400M 밸류), Holywater(앱 설치 1억+, $22M) | 검증됨. 다만 "AI 협업"은 내부 공정 | 작가에게 지급하고 플랫폼이 IP를 확보. 마이크로드라마로 확장 중 |
| AI 생성 본문을 독자에게 직접 판매 | 중국 번치·진장(2023~2025 장려) | **역풍 확인**(2026-07) | 저품질 범람 → 독자 이탈 → 플랫폼 규제. 저작권 분쟁 |
| 블록체인 IP 등록·토큰화 | Sekai/Story Protocol | 트랙션 미확인 | 투자자 관심 2024년 이후 급감 |

핵심 관찰: STORY 8 계획서의 수익 가정(참여작가 등록비·참여비, 도네이션, 2차 저작물 배분)은 위 표에서 검증된 어느 행에도 해당하지 않는다. 반대로 검증된 모델들(캐릭터챗 구독, 라이선스 IP, 창작자 경제, 독자 데이터 기반 IP 선별)은 모두 **작가·IP 보유자에게 돈이 흘러가는 구조**를 전제로 한다.

## 9. 기술 스택에서 얻는 교훈

- **자체 LLM 개발은 비용 대비 효과가 없다.** Character.AI는 창업자 이탈 후 자체 모델을 포기하고 Meta·DeepSeek 오픈소스로 전환(Sacra). Chai는 오픈소스 모델을 포스트트레이닝해 15~20명으로 ARR $120M을 만든다. MiniMax만 자체 모델을 유지하지만 그 가치는 앱이 아니라 API 사업에서 나온다. STORY 8 계획서의 "딥러닝 자체 학습으로 100만 캐릭터 유니버스 구축"은 2026년 기준으로는 오픈 모델 + 구조화 데이터(캐릭터 시트·세계관 바이블) + 검색증강(RAG)으로 대체하는 것이 정석이다.
- **차별화는 모델이 아니라 데이터 구조와 UX에서 나온다.** Sudowrite의 Story Bible, NovelAI의 Lorebook, NovelCrafter의 Codex, Latitude의 World Engine(5년 개발, 캐릭터 16만 개 베타)처럼 "캐릭터·세계관을 구조화해 모델에 넣는 계층"이 제품의 본체다. OCT UNIVERSE의 캐릭터 입력폼(기본정보·연령별 사건·전사)은 이 계층의 초기 형태로 재해석할 수 있다.
- **안전·연령 계층은 선택이 아니라 필수 인프라다.** Character.AI는 자체 연령추정 모델 + Persona(제3자 신원확인)를 도입했고, SB 243은 3시간마다 휴식 알림과 위기 프로토콜을 요구한다. 한국에서 10대 이용이 많은 제타류 서비스는 같은 규제 압력을 받게 된다.
- **원가 구조**: 캐릭터챗의 매출원가는 추론 토큰 비용이다. Chai·Tolan이 소수 인력으로 흑자를 내는 이유는 모델 크기·컨텍스트 길이·캐시 전략을 제품 설계에 넣었기 때문이다. 교대 집필 30~50회(챕터당 300~500자)는 토큰 효율 면에서는 가볍지만, 그만큼 생성 가치도 낮아 과금 명분이 약하다.

## 10. 한국 시장 특수 상황(2026)

- **수요 검증 완료**: 제타(스캐터랩)가 MAU 140만·연매출 260억원·영업이익 30억원(2025)으로 국내 캐릭터챗 수요와 수익성을 증명했고, 일본에서 WAU 75만·1인당 일평균 4시간이라는 해외 확장 가능성까지 보여줬다. 크랙(뤼튼)이 MAU 55만으로 2위. 즉 "한국어 캐릭터 인터랙션" 시장은 이미 존재하며, 신규 진입자는 **캐릭터·세계관 품질과 IP**로 차별화해야 한다.
- **공급 측 공백**: 카카오엔터가 Radish(2025)·Tapas(2026-09 발표) 북미 플랫폼을 접고 카카오페이지 중심 "데이터·AI 고도화"로 선회했고, 네이버의 Yonder도 2025-07 종료됐다. 대형 플랫폼이 직접 "AI 인터랙티브 픽션"을 만들기보다 추천·개인화에 AI를 쓰는 지금, **국내 웹소설 IP를 캐릭터 인터랙션으로 전환해 주는 B2B2C 레이어**가 비어 있다.
- **규범 공백**: 웹소설에는 AI 사용 고지 의무가 없고 플랫폼은 판별 능력이 없다(머니투데이 2026-03-11). 독자는 AI 개입이 드러나면 별점 테러로 응징한다. 따라서 "AI가 챕터를 썼다"를 전면에 내세우는 STORY 8 방식은 국내 독자 정서와 정면충돌하며, 반대로 "작가가 만든 캐릭터와 독자가 대화한다"는 프레임은 정서적 저항이 훨씬 적다.
- **법제**: AI기본법(2026-01 시행)의 고지·표시 의무와 문체부 가이드라인 정비 방향을 고려하면, AI 생성 여부 표시·연령 확인·대화 데이터 처리 동의를 처음부터 제품에 넣어야 한다. 이탈리아 Garante의 Replika 제재(€5M)는 **대화 데이터로 모델을 학습시키는 행위** 자체가 별도 조사 대상이 됨을 보여준다 — STORY 8의 "독자 평점·작품 수집→딥러닝" 설계는 동의 체계 없이는 위험하다.

## 11. 투자자·파트너 관점의 실사 체크리스트(이 지형에서 도출)

1. 창작자 공급: 작가에게 **지급**하는가, 받는가. 작가가 캐릭터·세계관의 권리를 유지하는가(Sudowrite "입력물 권리 불주장", Hidden Door 수익배분).
2. 독자 지표: D1/D7/D30 리텐션, DAU/MAU, 세션당 체류시간(제타 일본 4시간/일, Character.AI 75분/일), 무료→유료 전환율, ARPPU.
3. 원가: 대화 1건당 추론비용, 모델 전략(오픈소스 포스트트레이닝 여부), 캐시율.
4. 안전·규제: 연령확인 방식, 미성년자 모드(Character.AI Stories형 경계 설정), 위기 프로토콜, AI 고지, 데이터 학습 동의.
5. IP 파이프라인: 플랫폼에서 나온 캐릭터·스토리가 실제로 2차 저작(웹툰·마이크로드라마·게임)으로 넘어간 건수와 매출(Inkitt "Beautiful Mistake" $500K, Holywater 200편 시리즈).
6. 기존 플랫폼과의 호환: 결과물이 카카오페이지·문피아·Wattpad의 AI 정책에 걸리지 않는가(인간 집필 본문 + AI 인터랙션 분리).
7. 차별화의 실체: "세계 최초" 같은 주장 대신, 경쟁자(Chai·제타·Voyage·Hidden Door)가 못 하는 것이 무엇인지 — 가장 설득력 있는 답은 **검증된 한국 장르 IP와 작가 네트워크**다.

---

## 12. 미확인·추가 확인 필요 항목
- ㈜채널옥트 현황: channeloct.com은 2026-10-03 현재 404/미동작, 특허 등록 여부·현재 트랙션·팀 구성 모두 미확인.
- Character.AI 2026년 MAU·매출의 1차 출처(Sacra 2024년 초 수치 외 공식 공개 없음).
- PolyBuzz 매출·MAU(2차 통계 사이트만 존재).
- Royal Road AI 정책 원문(사이트 접근 차단), NovelAI·NovelCrafter 공식 가격·사용자 수.
- 네이버웹툰 '캐릭터챗', 카카오엔터 AI 챗 서비스의 공식 수치.
- 카카오엔터의 Tapas·Radish 인수액 원화 기준, Tapas 종료일(ANN 보도 2027-03-31)의 공식 공지.
- Sekai의 실사용자·매출, Giant 기사 게재일.
- 한국 AI기본법(2026-01 시행)이 캐릭터챗·AI 창작물 표기에 적용되는 세부 고시.

---

## 13. 출처 신뢰도 등급과 사용 원칙

- **높음**: 회사 공식 페이지·보도자료(Chai company-facts, China Literature 실적, Sudowrite 가격, Wattys 규정), SEC 공시(WEBTOON ARS), 주요 언론 1차 보도(TechCrunch, CNN/Gulf News, Rest of World, 서울경제, 유니콘팩토리, 파이낸셜뉴스, 머니투데이, 36Kr, The Block).
- **중간**: 1차 자료를 인용하는 리서치 데스크·분석 매체(Sacra, Tracxn, PitchBook, futunn의 투자설명서 분석, Substack 인터뷰), 접근이 차단돼 검색 요약으로만 확인한 공식 페이지(Royal Road 정책).
- **낮음**: 통계 집계 사이트와 리뷰 블로그(udonis, sqmagazine, aicompanionpick, voxbooster, techinnovators). 본문에서는 방향성 참고로만 썼고 핵심 결론의 근거로 쓰지 않았다.
- 모든 수치는 "기준 시점"을 함께 적었다. 시점이 없는 수치는 원문에 시점이 없는 경우이며, 의사결정 근거로 쓰려면 재확인이 필요하다.
