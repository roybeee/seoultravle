"""
통합안 '성수 럭키 넘버' 사양으로 돌린 어뷰징 시뮬레이션.  python3 analysis/simulate_lucky_number.py

사양: 응모자 N(기본 3,000)이 1..M(M=10,000 고정, 참가자 수와 무관)에서 정수 하나를 고른다.
      마감 후 공개되는 난수 목표값 t(1..M 균등)에 가장 가까운 '단독' 숫자가 당첨.
      같은 거리의 단독 숫자가 둘이면 큰 쪽. 단독 숫자가 없으면 가장 가까운 숫자를 낸 사람들 중 무작위 1명.
공격자: 참가권 K장(=계정 K개 또는 친구 K명 담합)을 들고 최적 전략(균등 간격 배치)으로 깐다.
정직한 참가자 행동 가정 두 가지:
  uniform   : 전부 무작위
  clustered : 30%는 '인기 숫자' 50개(7, 77, 777, 1004, 2026, 1111 …)에 몰리고 70%는 무작위
비교 기준: 공정한 추첨이라면 당첨확률 = K/(N+K).
표준 라이브러리만 사용. 약 1분.
"""
import random
import sys
from collections import Counter

SEED = 20261003
TRIALS = 1500
M = 10_000
N_HONEST = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
POPULAR = [7, 77, 777, 7777, 1004, 2026, 1111, 2222, 3333, 4444, 5555, 6666, 8888, 9999, 10000, 1,
           100, 1000, 500, 5000, 1234, 4321, 2580, 1313, 1004, 486, 143, 520, 1314, 3, 13, 21, 42, 69,
           88, 99, 101, 365, 404, 808, 911, 1212, 2020, 2024, 2025, 7000, 9000, 1999, 2000, 6000]


def honest_number(profile, rng):
    if profile == "clustered" and rng.random() < 0.30:
        return rng.choice(POPULAR)
    return rng.randint(1, M)


def winner(bids, target, rng):
    """bids: [(number, owner)] → owner"""
    c = Counter(n for n, _ in bids)
    uniques = [(abs(n - target), -n, o) for n, o in bids if c[n] == 1]
    if uniques:
        return min(uniques)[2], True
    # 단독 숫자가 없으면 가장 가까운 숫자의 응모자들 중 무작위
    best = min(abs(n - target) for n, _ in bids)
    pool = [o for n, o in bids if abs(n - target) == best]
    return rng.choice(pool), False


def run(profile, k, rng):
    hits = no_unique = 0
    for _ in range(TRIALS):
        bids = [(honest_number(profile, rng), i) for i in range(N_HONEST)]
        step = max(1, M // max(1, k))
        attacker = [(min(M, 1 + j * step + rng.randint(0, max(0, step // 10))), -1) for j in range(k)]
        bids += attacker
        t = rng.randint(1, M)
        w, had_unique = winner(bids, t, rng)
        if not had_unique:
            no_unique += 1
        if w == -1:
            hits += 1
    return hits / TRIALS, no_unique / TRIALS


def main():
    rng = random.Random(SEED)
    ks = (1, 10, 30, 100, 300)
    print(f"응모자 {N_HONEST:,}명 + 공격자 1명(참가권 K장, 균등 간격 배치), 범위 1..{M:,} 고정, 시행 {TRIALS}회/조합")
    print()
    hdr = f"{'행동 가정':<12}" + "".join(f"{'K='+str(k):>9}" for k in ks) + f"{'단독 없음':>10}"
    print(hdr)
    print("-" * len(hdr))
    row = f"{'비례 기준선':<12}" + "".join(f"{k/(N_HONEST+k):>9.2%}" for k in ks) + f"{'':>10}"
    print(row)
    for profile in ("uniform", "clustered"):
        row = f"{profile:<12}"
        nu = None
        for k in ks:
            p, n = run(profile, k, rng)
            if k == 1:
                nu = n
            row += f"{p:>9.2%}"
        row += f"{nu:>10.2%}"
        print(row)
    print()
    print("읽는 법: 공격자 당첨확률이 비례 기준선과 같으면 참가권을 더 사거나 친구와 담합해도 초과 이득이 없다.")
    print("        '단독 없음'은 단독 숫자가 하나도 없어 폴백 규칙(최근접자 중 무작위)이 쓰인 라운드 비율.")


if __name__ == "__main__":
    main()
