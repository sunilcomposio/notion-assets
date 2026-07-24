import sys


def held_karp(dist):
    n = len(dist)
    INF = sys.maxsize
    size = 1 << n
    dp = [[INF] * size for _ in range(n)]
    parent = [[-1] * size for _ in range(n)]

    # Base case: at city 0, having visited only city 0 (mask = ...0001)
    dp[0][1] = 0

    for mask in range(size):
        if not (mask & 1):
            continue  # every valid state must include the start city 0
        for u in range(n):
            if not (mask & (1 << u)):
                continue  # u must actually be in the visited set
            if dp[u][mask] == INF:
                continue
            for v in range(n):
                if mask & (1 << v):
                    continue  # v already visited
                new_mask = mask | (1 << v)
                new_cost = dp[u][mask] + dist[u][v]
                if new_cost < dp[v][new_mask]:
                    dp[v][new_mask] = new_cost
                    parent[v][new_mask] = u

    # Close the tour: end at some city i (i != 0), then return to 0
    final_mask = size - 1
    min_cost = INF
    last = -1
    for i in range(1, n):
        cost = dp[i][final_mask] + dist[i][0]
        if cost < min_cost:
            min_cost = cost
            last = i

    # Reconstruct path by walking parents back from `last` to 0.
    # The walk itself ends at city 0, so after reversing we just append
    # a single 0 for the return leg -- no duplicate 0 anywhere.
    path = []
    mask = final_mask
    u = last
    while u != -1:
        path.append(u)
        prev = parent[u][mask]
        mask ^= (1 << u)
        u = prev
    path.reverse()   # now [0, ..., last]
    path.append(0)   # return to start

    return min_cost, path


# 12-city distance matrix (symmetric)
dist = [
    [0, 29, 20, 21, 16, 31, 100, 12, 4, 31, 18, 25],
    [29, 0, 15, 29, 28, 40, 72, 21, 29, 41, 12, 17],
    [20, 15, 0, 15, 14, 25, 81, 9, 23, 27, 13, 22],
    [21, 29, 15, 0, 4, 12, 92, 12, 25, 13, 25, 24],
    [16, 28, 14, 4, 0, 16, 94, 9, 20, 16, 22, 23],
    [31, 40, 25, 12, 16, 0, 95, 24, 36, 3, 37, 30],
    [100, 72, 81, 92, 94, 95, 0, 90, 101, 99, 84, 79],
    [12, 21, 9, 12, 9, 24, 90, 0, 15, 25, 13, 18],
    [4, 29, 23, 25, 20, 36, 101, 15, 0, 35, 18, 26],
    [31, 41, 27, 13, 16, 3, 99, 25, 35, 0, 38, 31],
    [18, 12, 13, 25, 22, 37, 84, 13, 18, 38, 0, 9],
    [25, 17, 22, 24, 23, 30, 79, 18, 26, 31, 9, 0],
]

cost, tour = held_karp(dist)

# Sanity checks: valid permutation starting/ending at 0, and cost matches tour
assert tour[0] == 0 and tour[-1] == 0, "tour must start and end at 0"
assert sorted(tour[:-1]) == list(range(len(dist))), "tour must visit each city once"
tour_cost = sum(dist[tour[i]][tour[i + 1]] for i in range(len(tour) - 1))
assert tour_cost == cost, f"reported cost {cost} != actual tour cost {tour_cost}"

print("Optimal Cost:", cost)
print("Tour:", tour)
