################################
### 1. 基本输入输出
################################

# 常见的三种输入方式
#
# - input()
# - sys.stdin
# - open(0)


# 对输入的处理
#
# 字符串
input()
# 整数
int(input())
# 浮点数
float(input())
# 列表
map(int, input().split())
# numpy
import numpy as np
np.array(input().split(),np.int64))


# 输入形式
#
# N
# A1 A2 … AN
#
n = int(input())
a = list(map(int, input().split()))

# 可以使用逗号分隔读入两个变量
# N K
# A1 A2 … AN
#
n, k = map(int, input().split())
a = list(map(int, input().split()))

# 使用read(0)可以无视换行
# stdin
n, k, *a = map(int,open(0).read().split())

# local file
n, k, *a = map(int,open('test.in').read().split())


# 在大量换行输入的情况下用 sys.stdin.readline
import sys
input = sys.stdin.readline

# H W
# S1
# ⋮
# SH
h, w = map(int, input().split())
s = [input() for _ in range(h)]

# N
# t1 x1 y1
# t2 x2 y2
# ⋮
# tN xN yN
n = int(input())
t = [0] * n
x = [0] * n
y = [0] * n
for i in range(n):
    t[i], x[i], y[i] = map(int, input().split())



################################
### 2. 读到文件末尾
################################

# a1
# a2
# ⋮
# −1
for e in iter(input, '-1'):
    # 处理输入

# a1
# a2
# ⋮⋮
# (EOF)
import sys
for e in sys.stdin:
    # 処理


################################
### 3. 交互题
################################

# TODO
