import collections

# initialize G
# always 0 based, nodes [0, n)
N = int(1e5)
G = [[] for _ in range(N)]

# traverse
# no dfs thanks
def bfs(G, s):
    q = collections.deque([s])
    vis = [0] * len(G)
    vis[s] = 1
    while q:
        u = q.popleft()
        vis[u] = 1
        for v in G[u]:
            if not vis[v]:
                q.append(v)

# colorize graph with 2 colors, 
# Welsh—Powell algorithm for more kinds of colors
# G: undirected graph without self-loops
def colorize(G, s):
    co = [None] * len(G)
    co[s] = True
    q = collections.deque([s])
    while q:
        u = q.popleft()
        for v in G[u]:
            if co[v] is None:
                co[u] = not co[v]
                q.append(v)
            elif co[v] == co[u]:
                return False
    for c in co:
        if c is None: return False
    return True


def toposort(G, topo=[]):
    d = [0] * len(G)
    for vs in G:
        for v in vs:
            d[v] += 1

    q = collections.deque([u for u in range(len(G)) if d[u] == 0])
    while q:
        u = q.popleft()
        topo.append(u)
        for v in G[u]:
            d[v] -= 1
            if d[v] == 0:
                q.append(v)

    if sum(d):
        return False
    return True

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

class Dijkstra():
    class Edge():
        def __init__(self, _to, _cost):
            self.to = _to
            self.cost = _cost

    def __init__(self, V):
        self.G = [[] for i in range(V)]
        self._E = 0
        self._V = V

    @property
    def E(self):
        return self._E

    @property
    def V(self):
        return self._V

    def add_edge(self, _from, _to, _cost):
        self.G[_from].append(self.Edge(_to, _cost))
        self._E += 1

    def shortest_path(self, s):
        import heapq
        que = []
        d = [10**15] * self.V
        d[s] = 0
        heapq.heappush(que, (0, s))

        while len(que) != 0:
            cost, v = heapq.heappop(que)
            if d[v] < cost: continue

            for i in range(len(self.G[v])):
                e = self.G[v][i]
                if d[e.to] > d[v] + e.cost:
                    d[e.to] = d[v] + e.cost
                    heapq.heappush(que, (d[e.to], e.to))
        return d
