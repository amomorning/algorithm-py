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
 