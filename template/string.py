gchr = lambda c, a='a': ord(c) - ord(a)
gord = lambda c, a='a': chr(c + ord(a))

class Hash:
    def __init__(self, s, seed=214131331, mod=9898798161):
        self.n = len(s)
        self.pow = [1]
        self.mod = mod
        self.table = [0] * (self.n + 1)

        for i in range(1, self.n):
            self.pow.append(self.pow[-1] * seed % mod)
        
        for i in range(self.n-1, -1, -1):
            self.table[i] = self.table[i+1] * seed + ord(s[i])
            self.table[i] %= mod

    def get(self, l, r):
        return (self.table[l] - self.table[r+1] * self.pow[r-l+1] + self.mod) % self.mod
    
    def get_lcd(self, x, y):
        l, r = 1, min(self.n-x, self.n-y)
        while l <= r:
            m = (l+r) >> 1
            if self.get(x, x+m-1) == self.get(y, y+m-1):
                l = m + 1
            else:
                r = m - 1
        return l - 1


class KMP:
    def __init__(self, s):
        self.next = [0] * len(s)
        self.next[0], j = -1, -1
        self.s = s
        for i in range(1, len(s)):
            while j >= 0 and s[i] != s[j+1]: 
                j = self.next[j]
            if s[i] == s[j+1]:
                j += 1
                self.next[i] = j
            else:
                self.next[i] = -1
    
    def fit(self, b, c):
        if b + 1 == len(self.s): b = self.next[b]
        while b >= 0 and self.s[b + 1] != c:
            b = self.next[b]
        return b + int(self.s[b+1] == c)
    
    def count(self, t):
        j = -1
        ret = []
        for i in range(len(t)):
            j = self.fit(j, t[i])
            if j+1 == len(self.s):
                ret.append(i)
        return ret

class Manacher:
    def __init__(self, s, bogus='#'):
        self.s = [bogus]
        for x in s:
            self.s.append(x)
            self.s.append(bogus)
        self.bogus = bogus
        self.solve()
    
    def solve(self):
        n = len(self.s)
        self.p = [0] * n
        c, r = 0, 0
        for i in range(n):
            if r > i: self.p[i] = min(self.p[2*c-i], r-i)

            while i+self.p[i]+1 < n and self.s[i+self.p[i]+1] == self.s[i-self.p[i]-1]: 
                self.p[i] += 1

            if i + self.p[i] > r:
                c, r = i, i + self.p[i]

        return self.p
    
    def result(self, join=False):
        r = max(self.p)
        c = self.p.index(r)
        ret = [x for x in self.s[c-r:c+r] if x != self.bogus]
        if join: ret = ''.join(map(str, ret))
        return ret
    
    def max(self):
        return max(self.p)


def LongestPalindromicPrefix(s, bogus='#'):
    tmp = s + bogus + s[::-1]
    n = len(tmp)
    lps = [0] * n
    for i in range(1, n):
        m = lps[i - 1]
        while (m > 0 and tmp[m] != tmp[i]):
            m = lps[m - 1]
        if (tmp[i] == tmp[m]):
            m += 1
        lps[i] = m
    return tmp[0 : lps[n - 1]]


class Trie:
    def __init__(self, n=100000):
        self.n = n
        self.cnt = 0
        self.nxt = make_arr(n, 26)(lambda:0)
        self.exist = [False] * n
    
    def insert(self, s):
        p = 0
        for c in s:
            c = gchr(c)
            if not self.nxt[p][c]:
                self.cnt += 1
                self.nxt[p][c] = self.cnt
            p = self.nxt[p][c]
        self.exist[p] = True
    
    def find(self, s):
        p = 0
        for c in s:
            c = gchr(c)
            if not self.nxt[p][c]:
                return False
            p = self.nxt[p][c]
        return self.exist[p]


class BinaryTrie:
    MAXBIT = 30
    class Node:
        def __init__(self, v):
            self.l = None
            self.r = None
            self.v = v
            self.cnt = 0
            self.xor = 1<<BinaryTrie.MAXBIT
    
    def __init__(self):
        self.root = self.Node(1<<self.MAXBIT)
    
    def insert(self, v):
        u = self.root
        stack = []
        for b in range(self.MAXBIT)[::-1]:
            stack.append(u)
            if v & (1<<b):
                if u.r is None:
                    u.r = self.Node(v)
                u = u.r
            else:
                if u.l is None:
                    u.l = self.Node(v)
                u = u.l
        u.cnt = 1
        u.v = v
        u.xor = 1<<self.MAXBIT
    
        for u in stack[::-1]:
            u.cnt = 0
            if u.l and u.l.cnt:
                u.cnt += u.l.cnt
                u.xor = min(u.xor, u.l.xor)
                u.v = u.l.v
            if u.r and u.r.cnt:
                u.cnt += u.r.cnt
                u.xor = min(u.xor, u.r.xor)
                u.v = u.r.v
            if u.l and u.r and u.l.cnt and u.r.cnt:
                u.xor = min(u.xor, u.l.v ^ u.r.v)

    def erase(self, v):
        u = self.root
        stack = []
        for b in range(self.MAXBIT)[::-1]:
            stack.append(u)
            if v & (1<<b):
                u = u.r
            else:
                u = u.l
        u.cnt = 0
        u.v = -1
        u.xor = 1<<self.MAXBIT

        for u in stack[::-1]:
            u.cnt = 0
            u.xor = 1<<self.MAXBIT
            if u.l and u.l.cnt:
                u.cnt += u.l.cnt
                u.xor = min(u.xor, u.l.xor)
                u.v = u.l.v
            if u.r and u.r.cnt:
                u.cnt += u.r.cnt
                u.xor = min(u.xor, u.r.xor)
                u.v = u.r.v
            if u.l and u.r and u.l.cnt and u.r.cnt:
                u.xor = min(u.xor, u.l.v ^ u.r.v)
            if u.cnt == 0:
                u.v = -1

if __name__ == "__main__":
    s = 'aabcaabxaaa'
    print(KMP(s).next)
