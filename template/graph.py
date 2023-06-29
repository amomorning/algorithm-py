import collections, math, heapq

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
                co[v] = not co[u]
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
    q = collections.deque([u for u, du in enumerate(d) if du == 0])
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

def spdag(G, s):
    # G is DAG
    topo = []
    assert toposort(G, topo)
    d = [math.inf] * len(G)
    d[s] = 0
    for u in topo:
        for v, w in G[u]:
            d[v] = min(d[v], d[u] + w)
    
    return d

def floyd(G):
    # G[u][v] = w, O(n^3)
    n = len(G)
    for k in range(n):
        for j in range(n):
            for i in range(n):
                G[i][j] = min(G[i][j], G[i][k] + G[k][j])

def spfa(G, s):
    d = [math.inf] * len(G)
    vis = [False] * len(G)
    d[s] = 0
    vis[s] = True
    q = collections.deque([s])

    while q:
        u = q.popleft()
        vis[u] = False
        for v, w in G[u]:
            if d[v] > d[u] + w:
                d[v] = d[u] + w
                
                if vis[v] == False:
                    vis[v] = True
                    if q and d[q[0]] > d[v]:
                        q.appendleft(v)
                    else:
                        q.append(v)
    return d


def dijkstra(G, s):
    q = []
    d = [math.inf] * len(G)
    d[s] = 0
    heapq.heappush(q, (d[s], s))

    while q:
        du, u = heapq.heappop(q)
        if d[u] < du: continue 

        for v, w in G[u]:
            if d[v] > d[u] + w:
                d[v] = d[u] + w
                heapq.heappush(q, (d[v], v))
    
    return d

def prim(G):
    q = []
    d = [math.inf] * len(G)
    d[0] = 0
    heapq.heappush(q, (d[0], 0))
    tot = 0
    while q:
        du, u = heapq.heappop(q)
        tot += du
        for v, w in G[u]:
            if d[v] > w:
                d[v] = w
                heapq.heappush(q, (d[v], v))
    
    return tot

class UnionFind:
    def __init__(self, x) -> None:
        self.uf = [-1] * x
 
    def find(self, x):
        r = x
        while self.uf[x] >= 0:
            x = self.uf[x]
        while r != x:
            self.uf[r], r = x, self.uf[r]
        return x
 
    def same(self, x, y):
        return self.find(x) == self.find(y)

    def union(self, x, y):
        ux, uy = self.find(x), self.find(y)
        if ux == uy:
            return False
        if self.uf[ux] >= self.uf[uy]:
            self.uf[uy] += self.uf[ux]
            self.uf[ux] = uy
        else:
            self.uf[ux] += self.uf[uy]
            self.uf[uy] = ux
        return True
 
    def count(self):
        return sum(f < 0 for f in self.uf)
 
    def valid(self):
        n = len(self.uf)
        for c in range(n):
            if self.uf[c] == -n:
                return True
        return False
    
    def roots(self):
        return [i for i, f in enumerate(self.uf) if f < 0]

    def groups(self):
        n = len(self.uf)
        ret = [[] for _ in range(n)]
        for i in range(n):
            f = self.find(i)
            ret[f].append(i)
        return ret
 
    def __print__(self):
        return self.uf

def kruskal(n, edges):
    edges = sorted(edges, key=lambda x: x[2])
    uf = UnionFind(n)
    tot = 0
    for u, v, w in edges:
        if uf.same(u, v): continue
        tot += w
        uf.union(u, v)
    return tot
        

if __name__ == '__main__':
    n, m = map(int, input().split())
    G = [[] for _ in range(n)]
    for i in range(m):
        u, v = map(int, input().split())
        u -= 1; v -= 1
        G[u].append(v)
    
    spdag(G, 0)

        
class Edge:
    def __init__(self, v, next, cap):
        self.v = v
        self.next = next
        self.cap = cap

class MaxFlow:
    s, t = -1, -1
    def __init__(self, n):
        self.n = n
        self.g = []
        self.head = [-1] * self.n

    def add_edge(self, u, v, w):
        self.g.append(Edge(v, self.head[u], w))
        self.head[u] = len(self.g) - 1
        self.g.append(Edge(u, self.head[v], 0))
        self.head[v] = len(self.g) - 1

    def dinic(self, s, t):
        self.s = s
        self.t = t
        flow = 0
        while self.bfs():
            flow += self.dfs(s, math.inf)
        return flow
    
    def get_cuts(self, s, t):
        mark = [False] * self.n
        def remark(u):
            if mark[u]: return
            mark[u] = True
            i = self.head[u]
            while i != -1:
                if self.g[i].cap > 0: remark(self.g[i].v)
                i = self.g[i].next
        remark(s)
        cuts = []
        for u in range(self.n):
            if not mark[u]: continue
            i = self.head[u]
            while i != -1:
                if not mark[self.g[i].v]: 
                    cuts.append((u, self.g[i].v, self.g[i^1].cap))
                i = self.g[i].next
        return cuts


    def bfs(self):
        q = collections.deque([self.t])
        self.dis = [-1] * self.n
        self.cur = [x for x in self.head]
        self.dis[self.t] = self.n
        while q:
            u = q.popleft()
            i = self.head[u]
            while i != -1:
                e = self.g[i]
                if self.g[i^1].cap and self.dis[e.v] == -1:
                    self.dis[e.v] = self.dis[u] - 1
                    q.append(e.v)
                
                i = self.g[i].next
        return self.dis[self.s] != -1
    
    def dfs(self, u, a):
        if u == self.t: return a
        flow, f = 0, 0
        i = self.cur[u]
        while i != -1:
            e = self.g[i]
            if e.cap and self.dis[e.v] > self.dis[u]:
                f = self.dfs(e.v, min(a, e.cap))
                flow += f
                e.cap -= f
                self.g[i^1].cap += f
                a -= f
                if a == 0: break
            i = self.g[i].next
        if flow == 0: self.dis[u] = -1
        return flow
    