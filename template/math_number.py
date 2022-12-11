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

# prime table 
import math
class PrimeTable:
    def __init__(self, n:int) -> None:
        self.n = n

        self.primes = []
        self.min_div = [0] * (n+1)
        self.min_div[1] = 1

        mu = [0] * (n+1)
        phi = [0] * (n+1)
        mu[1] = 1
        phi[1] = 1

        for i in range(2, n+1):
            if not self.min_div[i]:
                self.primes.append(i)
                self.min_div[i] = i
                mu[i] = -1
                phi[i] = i-1
            for p in self.primes:
                if i * p > n: break
                self.min_div[i*p] = p
                if i % p == 0:
                    phi[i*p] = phi[i] * p
                    break
                else:
                    mu[i*p] = -mu[i]
                    phi[i*p] = phi[i] * (p - 1)

    def is_prime(self, x:int):
        if x < 2: return False
        if x <= self.n: return self.min_div[x] == x
        for p in self.primes:
            if p * p > x: break
            if x % p == 0: return False
        for i in range(self.n+1, int(math.sqrt(x))+1):
            if x % i == 0: return False
        return True
    
    def prime_factorization(self, x:int):
        for p in self.primes:
            if p * p > x or x <= self.n: break
            if x % p == 0:
                cnt = 0
                while x % p == 0: 
                    cnt += 1
                    x //= p
                yield p, cnt
        for p in range(len(self.min_div), int(math.sqrt(x))+1):
            if x <= self.n: break
            if x % p == 0:
                cnt = 0
                while x % p == 0: cnt += 1; x //= p
                yield p, cnt
        while (1 < x and x <= self.n):
            p, cnt = self.min_div[x], 0
            while x % p == 0: cnt += 1; x //= p
            yield p, cnt
        if x >= self.n and x > 1:
            yield x, 1
    
    def get_factors(self, x:int):
        """ Not in ascending order"""
        factors = [1]
        for p, b in self.prime_factorization(x):
            n = len(factors)
            for j in range(1, b+1):
                for d in factors[:n]:
                    factors.append(d * (p ** j))
        return factors


# chinese remainder theorem
def exgcd(a, b):
    x = [1, 0, 0, 1]
    while b != 0:
        c = a // b
        x, a, b = [x[2], x[3], x[0] - x[2] * c, x[1] - x[3] * c], b, a % b
    return a, x[0], x[1]


def linear_diophantine(a, b, c):
    """ Solution for ax + by = c
        return: gcd(a, b), x, y
    """
    if a == 0 and b == 0: return 0, 0, 0 if c == 0 else False
    if a == 0: return abs(b), 0, c//b if c%b == 0 else False
    if b == 0: return abs(a), c//a, 0 if c%a == 0 else False
    d, x, y = exgcd(a, b)
    if c % d != 0: return False
    dx = c // a; c -= dx * a
    dy = c // b; c -= dy * b
    x = dx + x * (c // d) % b
    y = dy + y * (c // d) % a
    return abs(d), x, y


def linear_congruence(k1, m1, k2, m2):
    """ Solution for x = k1(mod m1)
                     x = k2(mod m2)			   
        return: x, lcm(m1, m2)  (0 <= x < lcm(m1, m2))
    """
    k1 %= m1; k2 %= m2
    if k1 < 0: k1 += m1
    if k2 < 0: k2 += m2

    tmp = linear_diophantine(m1, -m2, k2-k1)
    if tmp == False: return False
    
    d, x, _ = tmp
    dx = m2 // d
    delta = x // dx - int(x % dx < 0)
    return m1 * (x - dx * delta) + k1, m1 // d * m2


def count_coprime(primes, at, rest):
    """ count number of coprime between [1, rest] with primes[at:]
        notes: primes should be sorted in ascending order
    """
    if rest == 0: return 0
    ret = rest
    for i in range(at, len(primes)):
        if primes[i] > rest: break
        ret -= count_coprime(primes, i+1, rest // primes[i])
    return ret


class MillerRabin:
    @classmethod
    def pow_mod(self, a, b, mod):
        ans = 1
        while b:
            if b & 1: ans = ans * a % mod
            a = a * a % mod; b >>= 1
        return ans

    @classmethod
    def is_prime(self, n:int):
        if n <= 1: return False
        return not self.miller_rabin(n)

    @classmethod
    def miller_rabin(self, n:int):
        x, t = n-1, 0
        while ~x & 1: 
            x >>= 1 
            t += 1

        flag = True
        if t >= 1 and x & 1:
            cs = [2, 325, 9375, 28178, 450775, 9780504, 1795265022]
            for a in cs:
                if self.check_prime(a, n, x, t):
                    flag = True
                    break
                flag = False
        if not flag or n == 2: return False
        return True

    @classmethod
    def check_prime(self, a, n, x, t):
        ret = self.pow_mod(a, x, n)
        last = ret
        for i in range(1, t+1):
            ret = self.pow_mod(ret, 2, n)
            if ret == 1 and last != 1 and last != n-1:
                return True
            last = ret
        if ret != 1: return True
        return False
