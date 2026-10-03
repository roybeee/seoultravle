"""
서울여행경매 회차(라운드)당 손익 계산기.  python3 analysis/unit_economics.py

모든 숫자는 가정이다. 가정을 바꿔서 다시 돌려 보는 용도.
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


def fmt(won):
    return f"{won/10_000:>8,.0f}만"


def main():
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


if __name__ == "__main__":
    main()
