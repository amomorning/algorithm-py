import math

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
 
 
def comb(n, m, p):
    a = (math.factorial(n)) % p
    b = (qpow(math.factorial(m), (p - 2), p)) % p
    c = (qpow(math.factorial(n - m), (p - 2), p)) % p
    return a * b * c % p
 
 
def lucas(n, m, p):
    if m == 0:
        return 1
    return comb(n % p, m % p, p) * lucas(n // p, m // p, p) % p
