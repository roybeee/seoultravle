# seoultravle — 서울여행경매 사업 검토

K-culture 거점 맵달SEOUL(성수동)에서 검토한 '서울 여행 경품' 사업의 분석 자료와 재현 가능한 계산 스크립트.

## 문서

| 문서 | 내용 |
|---|---|
| `docs/seoul-travel-auction-analysis.md` | 1차 진단. 회의 녹취의 '유료 단독 최고가 경매' 구상에 대한 법률·수익성·어뷰징 분석과 대안 |
| `docs/nysac-deep-analysis-and-strategy.md` | 2차. 2013년 NYSAC(New York Style Auction) 자료 4종 심층 분석, 메커니즘 변형 시뮬레이션, 전략안 6개 패널 채점, 통합 사업화 전략('성수 타임'), 90일 실행 계획, 영문 요약 |

## 스크립트 (표준 라이브러리만 사용)

```bash
python3 analysis/simulate_unique_bid.py                   # 원안의 다중 참가권 어뷰징
python3 analysis/simulate_mechanism_variants.py           # 변형 A~E 비교 (현실형 행동 가정)
python3 analysis/simulate_mechanism_variants.py uniform   # 같은 비교, 무작위 행동 가정
python3 analysis/simulate_lucky_number.py                 # 통합안 '럭키 넘버' 사양의 어뷰징 저항
python3 analysis/unit_economics.py                        # 유료 원안 회차 손익 기준선 + 확장 시나리오
```

모든 수치는 스크립트 상단의 가정에 따른다. 법률 판단은 변호사 서면 의견으로 대체해야 한다.
