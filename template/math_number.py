# closed range

def crange(start, end, step=1):
    dir = 1 if start < end else -1
    if start > end and step > 0: step = -step
    return range(start, end + dir, step)


# quick power
MOD = 998244353
def qpow(a, b):
    ans = 1
    while b:
        if b & 1: ans = ans * a % MOD
        a = a * a % MOD; b >>= 1
    return ans

 
# binomial
MOD = 998244353
class Binomial:
    def __init__(self, n):
        n = min(n, MOD)
        self.fact = [1, 1]
        self.inv_fact = [1, 1]
        self.inv = [0, 1]
        
        for i in crange(2, n):
            self.fact.append(self.fact[-1] * i % MOD)
            self.inv.append((MOD - MOD // i) * self.inv[MOD % i] % MOD)
            self.inv_fact.append(self.inv_fact[-1] * self.inv[-1] % MOD)
    

    def comb(self, n, m):
        if m < 0 or m > n:
            return 0
        m = min(m, n-m)
        return self.fact[n] * self.inv_fact[m] * self.inv_fact[n-m] % MOD

    ''' Lucas theorem
    - mod should be less than 1e5
    '''
    def lucas(self, n, m): 
        if m == 0:
            return 1
        return self.comb(n % MOD, m % MOD) * \
            self.lucas(n // MOD, m // MOD) % MOD

MOD = 998244353
def norm(v):
    v = v % MOD
    if v < 0: v += MOD
    return v

class Integral:
    def __init__(self, v):
        self.v = norm(v, MOD)

    def __str__(self):
        return str(self.v)
    
    def __neg__(self):
        return Integral(-self.v, MOD)

    def __iadd__(self, rhs):
        if type(rhs) == Integral: rhs = rhs.v
        self.v = norm(self.v + rhs, MOD)
        return self
    
    def __isub__(self, rhs):
        self += -rhs
        return self
        
    def __imul__(self, rhs):
        if type(rhs) == int: rhs = Integral(rhs, MOD)
        self.v = norm(self.v * rhs.v, MOD)
        return self
    
    def __itruediv__(self, rhs):
        if type(rhs) == int: rhs = Integral(rhs, MOD)
        self.v = norm(self.v * rhs.inv().v, MOD)
        return self
    
    def copy(self):
        return Integral(self.v, MOD)
    
    def pow(self, b):
        assert type(b) == int
        ret, a = 1, self.v
        while b > 0:
            if b & 1:
                ret = ret * a % MOD
            b >>= 1
            a = a * a % MOD
        return Integral(ret, MOD)
    
    def inv(self):
        return self.pow(MOD-2)
    
    def __add__(self, rhs):
        ret = self.copy(); ret += rhs
        return ret

    def __sub__(self, rhs):
        ret = self.copy(); ret -= rhs
        return ret
    
    def __mul__(self, rhs):
        ret = self.copy(); ret *= rhs
        return ret
    
    def __truediv__(self, rhs):
        ret = self.copy(); ret /= rhs
        return ret
    
    def __lshift__(self, rhs):
        if type(rhs) == Integral: rhs = rhs.v
        return Integral(self.v << rhs, MOD)

    def __rshift__(self, rhs):
        if type(rhs) == Integral: rhs = rhs.v
        return Integral(self.v >> rhs, MOD)
    
    def __pow__(self, rhs):
        return self.pow(rhs)
    
    def __eq__(self, rhs):
        if type(rhs) == Integral: rhs = rhs.v
        return self.v == rhs
    
    def __lt__(self, rhs):
        if type(rhs) == Integral: rhs = rhs.v
        return self.v < rhs
    
    def __le__(self, rhs):
        if type(rhs) == Integral: rhs = rhs.v
        return self.v <= rhs
    

