import math


# 常量
math.pi # 3.141592653589793
math.e # 2.718281828459045
math.tau # 6.283185307179586
math.inf # inf


# 整数处理
math.ceil(1.23) # 2
math.ceil(-1.23) # -1
math.floor(1.23) # 1
math.floor(-1.23) # -2

# 四舍五入
math.floor(x + .5)

# 强制转换向0取整
int(1.23) # 1 
int(-1.23) # -1 
math.trunc(1.23) # 1
math.trunc(-1.23) # -1

# 组合数
math.comb(6, 3)
math.perm(6, 3)
math.factorial(6)

math.prod([1, 2, 4, 2])
math.fsum([1.1, 1.2]) # 2.3

# 组合数取模
# TODO


# 浮点处理
math.fabs(-1.23) # 1.23
math.modf(1.23) #(0.23, 1.0)
math.fmod(1.23, 0.2) # 0.03


# gcd
math.gcd(12, 23)


# 三角函数
math.sin(math.pi/6) # 0.5
math.asin(.5) # 0.5235987755982988

math.cos(math.pi/3) # 0.5
math.acos(.5) # 1.0471975511965976


# cmath 可以处理复数！
import cmath
cmath.sqrt(-1) # 1j

# 复数三角函数
cmath.asinh(.5j) # 0.5235987755982989j


# 极坐标与笛卡尔坐标转换
cmath.polar(1 + 2j)
# (2.23606797749979, 1.1071487177940904)
cmath.rect(2.236, 1.107) 
# (1., 2.)
