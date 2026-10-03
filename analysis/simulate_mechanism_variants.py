"""
메커니즘 변형별 어뷰징(다중 참가권) 취약도 비교.  python3 analysis/simulate_mechanism_variants.py  (약 2분)

비교하는 변형:
  A. 기본     : 1인 1입찰, 범위 1..N, 단독 최고가 낙찰 (녹취 원안)
  B. NYSAC    : 1인 3입찰, 범위 1..N, 단독 최고가 낙찰 (2013 설계)
  C. 범위확장 : 1인 1입찰, 범위 1..10N, 단독 최고가 낙찰
  D. 비밀목표 : 1인 1입찰, 범위 1..N, 마감 후 공개되는 난수 목표값에 가장 가까운 '단독' 입찰이 낙찰
  E. 무작위배정: 숫자를 고르지 않고 시스템이 무작위 배정, 단독 최고가 낙찰 (= 사실상 추첨)

각 변형에서 정직한 참가자 N명 + 공격자 1명이 참가권 K장을 사서 '최적 시작점'으로 연속 번호를 깔 때의
당첨확률을 본다. 공격자는 여러 시작점 중 가장 잘 먹히는 것을 고른다(공격자에게 유리하게 가정).
표준 라이브러리만 사용.
"""

import random
import sys
from collections import Counter

SEED = 20261003
TRIALS = 500
N_HONEST = 1000
START_RATIOS = (1.0, 0.995, 0.99, 0.98, 0.97, 0.95, 0.92, 0.88)
# 참가자 행동 가정. 인자로 'uniform'을 주면 모두 무작위로 숫자를 고른다고 가정한다(강건성 점검용).
PROFILE = sys.argv[1] if len(sys.argv) > 1 else "behavioral"


def honest_bid(top, rng):
    """현실형 혼합 행동: 20% 무작위, 45% 최상단 근처, 35% 조금 아래로 회피. (uniform이면 전부 무작위)"""
    if PROFILE == "uniform":
        return rng.randint(1, top)
    r = rng.random()
    if r < 0.20:
        return rng.randint(1, top)
    if r < 0.65:
        off = int(rng.expovariate(1 / (0.04 * top)))
    else:
        off = int(rng.expovariate(1 / (0.15 * top)))
    return max(1, top - off)


def honest_bids(top, k, rng):
    s = set()
    while len(s) < k:
        s.add(honest_bid(top, rng))
    return list(s)


def highest_unique(bids):
    c = Counter(a for a, _ in bids)
    u = [(a, o) for a, o in bids if c[a] == 1]
    return max(u) if u else None


def closest_unique_to_target(bids, target):
    c = Counter(a for a, _ in bids)
    u = [(abs(a - target), -a, o) for a, o in bids if c[a] == 1]
    if not u:
        return None
    d, neg_a, o = min(u)
    return (-neg_a, o)


def one_round(variant, k, ratio, rng):
    """(낙찰자 owner 또는 None, 낙찰가/상한 비율 또는 None)"""
    n = N_HONEST
    if variant == "A":
        top = n + k
        bids = [(honest_bid(top, rng), i) for i in range(n)]
        s = max(k, int(top * ratio))
        bids += [(s - j, -1) for j in range(k)]
        w = highest_unique(bids)
    elif variant == "B":
        top = n + k
        bids = []
        for i in range(n):
            bids += [(b, i) for b in honest_bids(top, 3, rng)]
        s = max(3 * k, int(top * ratio))
        bids += [(s - j, -1) for j in range(3 * k)]
        w = highest_unique(bids)
    elif variant == "C":
        top = 10 * (n + k)
        bids = [(honest_bid(top, rng), i) for i in range(n)]
        s = max(k, int(top * ratio))
        bids += [(s - j, -1) for j in range(k)]
        w = highest_unique(bids)
    elif variant == "D":
        top = n + k
        bids = [(rng.randint(1, top), i) for i in range(n)]
        step = max(1, top // max(1, k))
        bids += [(min(top, 1 + j * step), -1) for j in range(k)]
        target = rng.randint(1, top)
        w = closest_unique_to_target(bids, target)
    elif variant == "E":
        top = n + k
        bids = [(rng.randint(1, top), i) for i in range(n)]
        bids += [(rng.randint(1, top), -1) for _ in range(k)]
        w = highest_unique(bids)
    else:
        raise ValueError(variant)
    if w is None:
        return None, None
    return w[1], w[0] / top


def run_variant(variant, k, rng):
    """공격자가 최적 시작점을 고른다고 가정. 반환: (최대 당첨확률, 그때 시작점, 무효율, 낙찰가비율 중앙값)"""
    ratios = START_RATIOS if variant in ("A", "B", "C") else (1.0,)
    best = (-1.0, None, 0.0, None)
    for ratio in ratios:
        hits = nowin = 0
        prices = []
        for _ in range(TRIALS):
            owner, price = one_round(variant, k, ratio, rng)
            if owner is None:
                nowin += 1
            else:
                prices.append(price)
                if owner == -1:
                    hits += 1
        p = hits / TRIALS
        prices.sort()
        med = prices[len(prices) // 2] if prices else None
        if p > best[0]:
            best = (p, ratio, nowin / TRIALS, med)
    return best


def main():
    rng = random.Random(SEED)
    names = {
        "A": "A 기본(1입찰, 1..N)",
        "B": "B NYSAC(3입찰, 1..N)",
        "C": "C 범위확장(1입찰, 1..10N)",
        "D": "D 비밀목표(난수 근접 단독)",
        "E": "E 무작위배정(추첨)",
    }
    ks = (1, 10, 30, 100)
    print(f"참가자 행동 가정: {PROFILE}")
    print(f"정직 참가자 {N_HONEST:,}명 + 공격자 1명(참가권 K장, 최적 시작점). 시행 {TRIALS}회/조합.")
    print("비례 기준선(공정한 추첨): K=1 0.1%, K=10 1.0%, K=30 2.9%, K=100 9.1%")
    print()
    hdr = f"{'변형':<28}" + "".join(f"{'K='+str(k):>9}" for k in ks) + f"{'무효율':>8}{'낙찰가/상한':>12}"
    print(hdr)
    print("-" * len(hdr))
    for v in ("A", "B", "C", "D", "E"):
        row = f"{names[v]:<28}"
        nowin1 = med1 = None
        for k in ks:
            p, ratio, nowin, med = run_variant(v, k, rng)
            if k == 1:
                nowin1, med1 = nowin, med
            row += f"{p:>9.1%}"
        row += f"{nowin1:>8.1%}"
        row += f"{(med1 if med1 is not None else float('nan')):>12.3f}"
        print(row)
    print()
    print("읽는 법:")
    print(" - 값이 '비례 기준선'에 가까울수록 다중 참가권의 초과 이득이 없다(어뷰징 유인 작음).")
    print(" - 무효율: 단독 입찰이 없어 낙찰자가 안 나오는 라운드 비율(K=1 기준).")
    print(" - 낙찰가/상한: 정상 상황(K=1)에서 낙찰가가 범위 상한의 몇 배인지(운영사 추가 매출 지표).")


if __name__ == "__main__":
    main()
