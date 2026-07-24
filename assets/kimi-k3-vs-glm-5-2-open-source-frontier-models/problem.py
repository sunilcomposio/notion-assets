import sys

def held_karp(dist):
    n = len(dist)
    dp = [[sys.maxsize] * (1 << n) for _ in range(n)]
    parent = [[-1] * (1 << n) for _ in range(n)]
    
    # Buggy base case
    dp[0][1] = 0
    
    for mask in range(1 << n):
        for u in range(n):
            if dp[u][mask] == sys.maxsize:
                continue
            for v in range(n):
                if (mask & (1 << v)) == 0:
                    new_mask = mask | (1 << v)
                    new_cost = dp[u][mask] + dist[u][v]
                    if new_cost < dp[v][new_mask]:
                        dp[v][new_mask] = new_cost
                        parent[v][new_mask] = u  # buggy parent tracking
    
    # Buggy final cost + reconstruction
    final_mask = (1 << n) - 1
    min_cost = sys.maxsize
    last = -1
    for i in range(n):
        cost = dp[i][final_mask] + dist[i][0]
        if cost < min_cost:
            min_cost = cost
            last = i
    
    # Broken path reconstruction
    path = []
    mask = final_mask
    u = last
    while u != -1:
        path.append(u)
        prev = parent[u][mask]
        mask ^= (1 << u)
        u = prev
    path.append(0)
    path.reverse()
    
    return min_cost, path

# 12-city distance matrix (symmetric for simplicity)
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
    [25, 17, 22, 24, 23, 30, 79, 18, 26, 31, 9, 0]
]

cost, tour = held_karp(dist)
print("Optimal Cost:", cost)
print("Tour:", tour)