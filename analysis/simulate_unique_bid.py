"""
'단독 최고가 낙찰(Highest Unique Bid)' 메커니즘 몬테카를로 시뮬레이션.

규칙(녹취 기준):
  - 참가자 N명이 각자 1..N 사이 정수 하나를 제출한다.
  - 정확히 1명만 제출한 금액 중 가장 높은 금액이 낙찰된다.
  - 낙찰자는 그 금액을 추가로 지불하고 상품을 받는다.

확인하려는 질문:
  1. 낙찰가는 보통 얼마인가? (= 운영사의 추가 매출)
  2. '단독 금액이 하나도 없는' 무효 라운드가 생길 확률은?
  3. 한 사람이 계정 K개(=참가권 K장)를 사면 당첨 확률이 얼마나 올라가는가? (어뷰징)

표준 라이브러리만 사용한다:  python3 analysis/simulate_unique_bid.py
"""

import math
import random
from collections import Counter

SEED = 20261003
TRIALS = 4000


def honest_bid(n, rng, profile):
    """참가자 1명의 입찰 금액. profile 은 참가자 행동 가정."""
    if profile == "uniform":
        # 아무 전략 없이 무작위로 쓰는 참가자만 있다고 가정 (하한선 시나리오)
        return rng.randint(1, n)
    # 'behavioral': 대부분 '높게, 하지만 남들과 겹치지 않게' 쓰려는 현실적 혼합
    r = rng.random()
    if r < 0.20:  # 무작위형
        return rng.randint(1, n)
    if r < 0.65:  # 최상단 집착형: 최고가 근처
        offset = int(rng.expovariate(1 / (0.04 * n)))
    else:  # 전략형: 약간 더 아래로 피해서 씀
        offset = int(rng.expovariate(1 / (0.15 * n)))
    return max(1, n - offset)


def winner_of(bids_with_owner):
    """bids_with_owner: [(amount, owner)] -> (amount, owner) 또는 None"""
    counts = Counter(a for a, _ in bids_with_owner)
    unique = [(a, o) for a, o in bids_with_owner if counts[a] == 1]
    return max(unique) if unique else None


def pct(sorted_vals, p):
    if not sorted_vals:
        return float("nan")
    k = min(len(sorted_vals) - 1, max(0, int(round(p * (len(sorted_vals) - 1)))))
    return sorted_vals[k]


def run_baseline(n, profile, rng):
    wins, no_winner = [], 0
    for _ in range(TRIALS):
        bids = [(honest_bid(n, rng, profile), i) for i in range(n)]
        w = winner_of(bids)
        if w is None:
            no_winner += 1
        else:
            wins.append(w[0])
    wins.sort()
    return {
        "p50": pct(wins, 0.5),
        "p10": pct(wins, 0.1),
        "p90": pct(wins, 0.9),
        "mean": sum(wins) / len(wins) if wins else float("nan"),
        "no_winner": no_winner / TRIALS,
    }


def run_sybil(n, k, profile, rng, start_ratios=(1.0, 0.95, 0.9, 0.85, 0.8, 0.75, 0.7)):
    """
    공격자 1명이 참가권 k장을 추가 구매(정직한 참가자 n명 + 공격자 k장 = 총 n+k장).
    공격자는 연속된 금액 k개 [s, s-1, ..., s-k+1] 를 쓴다. 가장 잘 먹히는 s를 찾는다.
    입찰 범위는 1..(n+k).
    """
    total = n + k
    best = (0.0, None)
    for ratio in start_ratios:
        s = int(total * ratio)
        if s - k + 1 < 1:
            continue
        hits = 0
        trials = TRIALS // 4
        for _ in range(trials):
            bids = [(honest_bid(total, rng, profile), i) for i in range(n)]
            bids += [(s - j, -1) for j in range(k)]
            w = winner_of(bids)
            if w is not None and w[1] == -1:
                hits += 1
        p = hits / trials
        if p > best[0]:
            best = (p, ratio)
    return best


def main():
    rng = random.Random(SEED)
    print("=" * 72)
    print("1) 낙찰가 분포 / 무효 라운드 확률  (시행 %d회)" % TRIALS)
    print("=" * 72)
    print(f"{'N':>6} {'행동가정':>10} {'P10':>7} {'중앙값':>7} {'P90':>7} {'평균':>8} {'무효확률':>8}")
    for n in (300, 700, 1000):
        for profile in ("uniform", "behavioral"):
            r = run_baseline(n, profile, rng)
            print(f"{n:>6} {profile:>10} {r['p10']:>7} {r['p50']:>7} {r['p90']:>7} "
                  f"{r['mean']:>8.1f} {r['no_winner']:>8.2%}")

    print()
    print("=" * 72)
    print("2) 어뷰징: 1명이 참가권 K장을 사서 연속 금액을 깔 때 당첨확률")
    print("   (정직한 참가자 1,000명, 행동가정=behavioral, 정상 1장 확률 ≈ 0.1%)")
    print("=" * 72)
    n = 1000
    prize_usd = 6400  # 상품 원가 약 900만원 / 1,400원
    print(f"{'K장':>5} {'비용($)':>8} {'당첨확률':>9} {'기대 상품가치($)':>16} {'최적 시작점':>10}")
    for k in (1, 10, 30, 60, 100, 200):
        p, ratio = run_sybil(n, k, "behavioral", rng)
        print(f"{k:>5} {k*10:>8} {p:>9.1%} {p*prize_usd:>16,.0f} {str(ratio):>10}")


if __name__ == "__main__":
    main()
