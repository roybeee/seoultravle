"""
서울여행경매 회차(라운드)당 손익 계산기.  python3 analysis/unit_economics.py

모든 숫자는 가정이다. 가정을 바꿔서 다시 돌려 보는 용도.
1부는 사전 진단(docs/seoul-travel-auction-analysis.md)과 같은 기준선이고,
2부는 NYSAC 자료 분석에서 드러난 누락 비용(KYC, 경품 원천징수, PG 리저브, 회차 성립률, 고정비)을 더한 확장 시나리오다.
"""

FX = 1400  # 원/달러 (가정)

# ── 상품 원가(원) ─ 녹취 기준: 호텔 7박 x 50만, 공연 2장, 용돈 200만, 항공 최대 300만
HOTEL = 7 * 500_000
TICKETS = 500_000
POCKET = 2_000_000
FULFILLMENT = 300_000  # 예약대행·여행자보험·CS·지상교통 등 (녹취엔 없음, 추가 가정)

# 당첨자 출발지별 왕복 이코노미 항공료(원)와 참가자 비중(가정)
ORIGINS = {
    "일본": (500_000, 0.25),
    "중국·대만·홍콩": (600_000, 0.20),
    "동남아": (800_000, 0.30),
    "미주": (2_000_000, 0.15),
    "유럽·중동": (1_800_000, 0.10),
}

# ── 확장 시나리오 가정 (2부) ─ 신뢰도는 주석 참고
KYC_PER_USER_USD = 1.5     # 실명·여권 수준 신원확인 단가 (업계 통상치, 신뢰도 중)
PRIZE_TAX_RATE = 0.22      # 경품 기타소득 원천징수 22% (비거주자 포함). 현물 경품이라 운영사 부담 시 22/78 그로스업 (세무 자문 필요)
RESERVE_RATE = 0.075       # 고위험 PG 롤링 리저브 5~10%, 90~180일 유보 (현금흐름 항목, 손익 아님)
FILL_RATE = 0.80           # 회차 성립률 (모집 미달 시 전액 환불) — 가정
REFUND_FEE_LOSS = 0.04     # 환불 시 돌려받지 못하는 결제수수료 비율 (2019~2020년 이후 Stripe·PayPal 정책)
FIXED_SETUP = 75_000_000   # 법률 의견(국내+타깃국 3곳), PG 사전승인, KYC·봇 차단, 다국어 약관 — 5,000만~1억 원 추정(신뢰도 중~하)


def prize_cost(airfare):
    return HOTEL + TICKETS + POCKET + FULFILLMENT + airfare


def expected_prize_cost():
    return sum(prize_cost(f) * w for f, w in ORIGINS.values())


def round_pnl(n, fee_usd, cac_usd, win_bid_ratio=0.9, pay_fee=0.08,
              chargeback=0.02, worst_case=False):
    """
    n: 참가자 수, fee_usd: 참가비, cac_usd: 참가권 1장 확보에 드는 마케팅비
    win_bid_ratio: 낙찰가 / n (시뮬레이션상 0.9 내외)
    pay_fee: 고위험 업종 결제수수료+환전, chargeback: 환불·차지백 손실률
    """
    entry_rev = n * fee_usd * FX
    bid_rev = n * win_bid_ratio * FX
    gross = entry_rev + bid_rev
    cost_prize = prize_cost(3_000_000) if worst_case else expected_prize_cost()
    cost_pay = gross * (pay_fee + chargeback)
    cost_mkt = n * cac_usd * FX
    profit = gross - cost_prize - cost_pay - cost_mkt
    return gross, cost_prize, cost_pay, cost_mkt, profit


def round_pnl_extended(n, fee_usd, cac_usd, win_bid_ratio=0.9, pay_fee=0.08, chargeback=0.02):
    """기준선에 KYC·경품세 그로스업·회차 성립률을 더한 '시도 1회당 기대 손익'."""
    gross, cost_prize, cost_pay, cost_mkt, _ = round_pnl(n, fee_usd, cac_usd, win_bid_ratio, pay_fee, chargeback)
    cost_kyc = n * KYC_PER_USER_USD * FX
    cost_tax = cost_prize * PRIZE_TAX_RATE / (1 - PRIZE_TAX_RATE)  # 운영사가 세금을 떠안을 때
    profit_success = gross - cost_prize - cost_pay - cost_mkt - cost_kyc - cost_tax
    # 미달 회차: 참가비 전액 환불, 수수료 손실 + 이미 쓴 마케팅비·KYC비는 매몰
    loss_fail = n * fee_usd * FX * REFUND_FEE_LOSS + cost_mkt + cost_kyc
    expected = FILL_RATE * profit_success - (1 - FILL_RATE) * loss_fail
    reserve_held = gross * RESERVE_RATE
    return profit_success, loss_fail, expected, reserve_held, cost_kyc, cost_tax


def fmt(won):
    return f"{won/10_000:>8,.0f}만"


def main():
    print("=" * 78)
    print("1부. 기준선 (사전 진단과 동일한 가정)")
    print("=" * 78)
    print(f"기대 상품원가: {fmt(expected_prize_cost())}  /  최악(항공 300만): {fmt(prize_cost(3_000_000))}")
    print()
    print("녹취 원안 계산(참가비만, 마케팅·수수료 0)")
    for n in (850, 1000):
        rev = n * 10 * FX
        print(f"  N={n:>5}: 참가비 {fmt(rev)} - 상품 900만 = {fmt(rev - 9_000_000)}")
    print()
    hdr = f"{'N':>6} {'참가비':>5} {'CAC($)':>6} {'매출':>10} {'상품원가':>10} {'결제/환불':>10} {'마케팅':>10} {'회차이익':>10}"
    print(hdr)
    print("-" * len(hdr))
    for n in (1000, 2000):
        for cac in (0, 2, 5, 10):
            g, c, p, m, pr = round_pnl(n, 10, cac)
            print(f"{n:>6} {'$10':>5} {cac:>6} {fmt(g):>10} {fmt(c):>10} {fmt(p):>10} {fmt(m):>10} {fmt(pr):>10}")
    print()
    print("손익분기 CAC (참가권 1장당 마케팅비 상한, 기대원가 기준)")
    for n in (700, 1000, 1500, 2000):
        g, c, p, _, _ = round_pnl(n, 10, 0)
        be = (g - c - p) / n / FX
        print(f"  N={n:>5}: 장당 ${be:,.2f} 까지 써도 본전")

    print()
    print("=" * 78)
    print("2부. 확장 시나리오 (KYC·경품세 그로스업·PG 리저브·회차 성립률·고정비 반영)")
    print("=" * 78)
    print(f"가정: KYC ${KYC_PER_USER_USD}/인, 경품세 {PRIZE_TAX_RATE:.0%}(운영사 부담 그로스업), 리저브 {RESERVE_RATE:.1%}, "
          f"성립률 {FILL_RATE:.0%}, 환불 수수료 손실 {REFUND_FEE_LOSS:.0%}, 고정비 {fmt(FIXED_SETUP)}")
    print()
    hdr2 = f"{'N':>6} {'CAC($)':>6} {'성립 시 이익':>12} {'미달 시 손실':>12} {'시도당 기대이익':>14} {'리저브 유보':>10}"
    print(hdr2)
    print("-" * len(hdr2))
    for n in (1000, 2000):
        for cac in (0, 1, 2, 5):
            ps, lf, ex, rs, _, _ = round_pnl_extended(n, 10, cac)
            print(f"{n:>6} {cac:>6} {fmt(ps):>12} {fmt(-lf):>12} {fmt(ex):>14} {fmt(rs):>10}")
    print()
    print("확장 기준 손익분기 CAC (성립률 100% 가정, KYC·경품세 포함)")
    for n in (700, 1000, 1500, 2000):
        ps0, _, _, _, _, _ = round_pnl_extended(n, 10, 0)
        be = ps0 / n / FX
        print(f"  N={n:>5}: 장당 ${be:,.2f}")
    print()
    print("고정비 회수에 필요한 '성립한 회차' 수 (CAC 0 → CAC $1)")
    for n in (1000, 2000):
        ps0 = round_pnl_extended(n, 10, 0)[0]
        ps1 = round_pnl_extended(n, 10, 1)[0]
        r0 = FIXED_SETUP / ps0 if ps0 > 0 else float("inf")
        r1 = FIXED_SETUP / ps1 if ps1 > 0 else float("inf")
        print(f"  N={n:>5}: {r0:,.0f}회 → {r1:,.0f}회")
    print()
    print("참고: 2013 NYSAC 535i 회차($40×2,500, MSRP $70,225)에 뉴욕시 판매세 8.875%·결제수수료·차지백·배송·CS·기부를 넣으면")
    print("      광고비 집행 전 이익은 약 $14,400~18,500(14~18%), 손익분기 마케팅비는 참가권당 $5.75~7.41 (문서 상 '30% 마진'과 대비).")


if __name__ == "__main__":
    main()
