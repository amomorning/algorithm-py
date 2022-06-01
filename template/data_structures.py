class SegmentTree:
    def __init__(self, size):
        self.size = 1 << size.bit_length()
        self.tree = [0] * (self.size << 1)
 
    def __getitem__(self, i):
        return self.tree[i + self.size]
 
    def update(self, i, x):
        i0 = i + self.size
        while i0:
            self.tree[i0] = x
            x = max(self.tree[i0], self.tree[i0 ^ 1])
            i0 >>= 1
 
    def range(self, i, j):
        x = 0
        i0 = i + self.size
        j0 = j + self.size
        while i0 < j0:
            if i0 & 1:
                x = max(x, self.tree[i0])
                i0 += 1
            if j0 & 1:
                x = max(x, self.tree[j0 - 1])
            i0 >>= 1
            j0 >>= 1
        return x
 

class SparseTable:
    def __init__(self, a, select=min):
        n = len(a); L = 1
        while (1 << L) <= n: L += 1

        self.lg = [-1] * (n + 1)
        self.u = [[0] * (L+1) for _ in range(n)]
        self.select = select

        for i in range(n):
            self.u[i][0] = a[i]
        for i in range(1, n + 1):
            self.lg[i] = self.lg[i >> 1] + 1
        for j in range(1, L):
            for i in range(n-(1<<j)+1):
                self.u[i][j] = self.select(self.u[i][j - 1], self.u[i + (1 << (j - 1))][j - 1])
        
    def ask(self, a, b):
        k = self.lg[b-a+1]
        return self.select(self.u[a][k], self.u[b - (1 << k) + 1][k])
