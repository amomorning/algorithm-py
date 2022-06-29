# closed range

def crange(start, end, step=1):
    dir = 1 if start > end else -1
    if start > end and step > 0:
        step = -step
    return range(start, end + dir, step)


# quick power
def qpow(a, b, mod):
    ans = 1
    while b:
        if b & 1: ans = ans * a % mod
        a = a * a % mod; b >>= 1
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

def norm(v, mod):
    v = v % mod
    if v < 0: v += mod
    return v

class Integral:
    def __init__(self, v, mod = 998244353):
        self.mod = mod
        self.v = norm(v, mod)

    def __str__(self):
        return str(self.v)
    
    def __neg__(self):
        return Integral(-self.v, self.mod)

    def __iadd__(self, rhs):
        if type(rhs) == Integral: rhs = rhs.v
        self.v = norm(self.v + rhs, self.mod)
        return self
    
    def __isub__(self, rhs):
        self += -rhs
        return self
        
    def __imul__(self, rhs):
        if type(rhs) == int: rhs = Integral(rhs, self.mod)
        self.v = norm(self.v * rhs.v, self.mod)
        return self
    
    def __itruediv__(self, rhs):
        if type(rhs) == int: rhs = Integral(rhs, self.mod)
        self.v = norm(self.v * rhs.inv().v, self.mod)
        return self
    
    def copy(self):
        return Integral(self.v, self.mod)
    
    def pow(self, b):
        assert type(b) == int
        ret, a = 1, self.v
        while b > 0:
            if b & 1:
                ret = ret * a % self.mod
            b >>= 1
            a = a * a % self.mod
        return Integral(ret, self.mod)
    
    def inv(self):
        return self.pow(self.mod-2)
    
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
        return Integral(self.v << rhs, self.mod)

    def __rshift__(self, rhs):
        if type(rhs) == Integral: rhs = rhs.v
        return Integral(self.v >> rhs, self.mod)
    
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
    

