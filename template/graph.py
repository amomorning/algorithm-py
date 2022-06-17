def spfa(x, g, n):
    dis = [float('inf') for i in range(n)]
    dis[x] = 0
    vis = [False for i in range(n)]
    vis[x] = True
    q = collections.deque()
    q.append(x)
    while q:
        u = q.popleft()
        vis[u] = False
        for v in g[u]:
            if dis[v] > dis[u] + 1:
                dis[v] = dis[u] + 1
                if vis[v] == False:
                    vis[v] = True
                    if q and dis[q[0]] > dis[v]:
                        q.appendleft(v)
                    else:
                        q.append(v)
    return dis

