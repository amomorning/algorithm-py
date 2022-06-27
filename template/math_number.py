import math


# closed range
def crange(start, end, step=1):
    dir = 1 if step > 0 else -1
    return range(start, end + dir, step)


# quick power
def qpow(x, y, p):
    ans = 1
    while y:
        if y & 1:
            ans *= x
            ans %= p
        x *= x
        x %= p
        y >>= 1
    return ans
 
 
# binomial
class Binomial:
    def __init__(self, n, mod):
        n = min(n, mod)
        self.mod = mod
        self.fact = [1, 1]
        self.inv_fact = [1, 1]
        self.inv = [0, 1]
        
        for i in crange(2, n):
            self.fact.append(self.fact[-1] * i % mod)
            self.inv.append((mod - mod // i) * self.inv[mod % i] % mod)
            self.inv_fact.append(self.inv_fact[-1] * self.inv[-1] % mod)
    

    def comb(self, n, m):
        if m < 0 or m > n:
            return 0
        m = min(m, n-m)
        return self.fact[n] * self.inv_fact[m] * self.inv_fact[n-m] % self.mod

    ''' Lucas theorem
    - mod should be less than 1e5
    '''
    def lucas(self, n, m): 
        if m == 0:
            return 1
        return self.comb(n % self.mod, m % self.mod) * \
            self.lucas(n // self.mod, m // self.mod) % self.mod

