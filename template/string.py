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


if __name__ == "__main__":
    s = 'aabcaabxaaa'
    print(KMP(s).next)
