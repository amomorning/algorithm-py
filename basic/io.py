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
np.array(input().split(),np.int64)


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
#
# H W
# S1
# ⋮
# SH
h, w = map(int, input().split())
s = [input() for _ in range(h)]
#
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
    pass

# a1
# a2
# ⋮⋮
# (EOF)
import sys
for e in sys.stdin:
    # 処理
    pass


################################
### 3. 快速读入
################################
import collections, math, bisect, heapq, random, functools, itertools, copy, typing
import platform; LOCAL = (platform.uname().node == 'AMO')

# Fast IO Region
import os, sys; from io import BytesIO, IOBase
BUFSIZE = 8192


class FastIO(IOBase):
    newlines = 0

    def __init__(self, file):
        self._fd = file.fileno()
        self.buffer = BytesIO()
        self.writable = "x" in file.mode or "r" not in file.mode
        self.write = self.buffer.write if self.writable else None

    def read(self):
        while True:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            if not b:
                break
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines = 0
        return self.buffer.read()

    def readline(self):
        while self.newlines == 0:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            self.newlines = b.count(b"\n") + (not b)
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines -= 1
        return self.buffer.readline()

    def flush(self):
        if self.writable:
            os.write(self._fd, self.buffer.getvalue())
            self.buffer.truncate(0), self.buffer.seek(0)


class IOWrapper(IOBase):
    def __init__(self, file):
        self.buffer = FastIO(file)
        self.flush = self.buffer.flush
        self.writable = self.buffer.writable
        self.write = lambda s: self.buffer.write(s.encode("ascii"))
        self.read = lambda: self.buffer.read().decode("ascii")
        self.readline = lambda: self.buffer.readline().decode("ascii")


sys.stdin, sys.stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)
import sys; input = lambda: sys.stdin.readline().rstrip("\r\n")
inp = lambda : list(map(int, input().split()))

def debug(*args):
    if LOCAL:
        print('\033[92m', end='')
        printf(*args)
        print('\033[0m', end='')

def printf(*args):
    if LOCAL:
        print('>>>: ', end='')
    for arg in args:
        if isinstance(arg, typing.Iterable) and \
                not isinstance(arg, str) and \
                not isinstance(arg, dict):
            print(' '.join(map(str, arg)), end=' ')
        else:
            print(arg, end=' ')
    print()

for _ in range(int(input())):
    pass
################################
### 4. 交互题
################################

# TODO
