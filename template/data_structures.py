


class SegmentTree:
    def __init__(self, size, select=min):
        self.size = 1 << size.bit_length()
        self.tree = [0] * (self.size << 1)
        self.select = select
 
    def __getitem__(self, i):
        return self.tree[i + self.size]
 
    def update(self, i, x):
        i0 = i + self.size
        while i0:
            self.tree[i0] = x
            x = self.select(self.tree[i0], self.tree[i0 ^ 1])
            i0 >>= 1
 
    def range(self, i, j):
        x = 0
        l = i + self.size
        r = j + self.size
        while l < r:
            if l & 1:
                x = self.select(x, self.tree[l])
                l += 1
            if r & 1:
                x = self.select(x, self.tree[r - 1])
            l >>= 1
            r >>= 1
        return x
 

class SparseTable:
    def __init__(self, a, select=min):
        N = len(a); 
        L = N.bit_length()

        self.u = [[0] * N for _ in range(L)]
        self.select = select

        for i in range(N):
            self.u[0][i] = a[i]
        for i in range(1, L):
            for j in range(N-(1<<i)+1):
                self.u[i][j] = self.select(self.u[i-1][j], self.u[i-1][j+(1<<(i-1))])
        
    def ask(self, l, r):
        i = (r - l).bit_length()-1
        return self.select(self.u[i][l], self.u[i][r-(1<<i)+1])

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
 
    def union(self, x, y):
        ux, uy = self.find(x), self.find(y)
        if ux == uy:
            return
        if self.uf[ux] >= self.uf[uy]:
            self.uf[uy] += self.uf[ux]
            self.uf[ux] = uy
        else:
            self.uf[ux] += self.uf[uy]
            self.uf[uy] = ux
        return
 
    def count(self):
        ans = 0
        for c in self.uf:
            if c < 0:
                ans += 1
        return ans
 
    def valid(self):
        n = len(self.uf)
        for c in range(n):
            if self.uf[c] == -n:
                return True
        return False
 
    def __print__(self):
        return self.uf
