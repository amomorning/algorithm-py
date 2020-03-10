import itertools

# 累加
x = itertools.accumulate(range(10))
list(x) # => [0, 1, 3, 6, 10, 15, 21, 28, 36, 45]

# 连接
x = itertools.chain(range(3), range(4), [3, 2, 1])
list(x) # => [0, 1, 2, 0, 1, 2, 3, 3, 2, 1]

# 重复
x = itertools.repeat(0, 5)
list(x) # => [0, 0, 0, 0, 0]

# 排列 Permutation
x = itertools.permutations(range(4), 3)
list(x) # => [(0, 1, 2), (0, 1, 3), (0, 2, 1), (0, 2, 3), (0, 3, 1), (0, 3, 2), (1, 0, 2), (1, 0, 3), (1, 2, 0), (1, 2, 3), (1, 3, 0), (1, 3, 2), (2, 0, 1), (2, 0, 3), (2, 1, 0), (2, 1, 3), (2, 3, 0), (2, 3, 1), (3, 0, 1), (3, 0, 2), (3, 1, 0), (3, 1, 2), (3, 2, 0), (3, 2, 1)] 

# 组合
x = itertools.combinations(range(4), 3) # (it, r)对it产生长度为r的组合
list(x) # => [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]

# 允许重复元素的组合
x = itertools.combinations_with_replacement('ABC', 2)
list(x) # => [('A', 'A'), ('A', 'B'), ('A', 'C'), ('B', 'B'), ('B', 'C'), ('C', 'C')]

# 笛卡尔积
x = itertools.product('ABC', range(3))
list(x) # => [('A', 0), ('A', 1), ('A', 2), ('B', 0), ('B', 1), ('B', 2), ('C', 0), ('C', 1), ('C', 2)]

# 拼接
x = itertools.zip_longest(range(3), range(5))
y = zip(range(3), range(5))
list(x) # => [(0, 0), (1, 1), (2, 2), (None, 3), (None, 4)]
list(y) # => [(0, 0), (1, 1), (2, 2)] 

# 映射
x = itertools.starmap(str.islower, 'aBCDefGhI')
list(x) # => [True, False, False, False, True, True, False, True, False]
y = map(str.islower, 'aBCDefGhI')
list(y) # => [True, False, False, False, True, True, False, True, False]

# 计数器
x = itertools.count(start=20, step=-1)
list(itertools.islice(x, 0, 10, 1)) 
# => [20, 19, 18, 17, 16, 15, 14, 13, 12, 11]
list(itertools.islice(x, 0, 20, 1)) 
# => [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, -1, -2, -3, -4, -5, -6, -7, -8, -9]

# 循环
x = itertools.cycle('ABC')
list(itertools.islice(x, 0, 10, 1)) 
# => ['A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A']
list(itertools.islice(x, 0, 10, 2)) 
# => ['B', 'A', 'C', 'B', 'A']
list(itertools.islice(x, 0, 10, 1)) 
# => ['C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C']

# 按真值表筛选
x = itertools.compress(range(5), (True, False, True, True, False))
list(x) # => [0, 2, 3]

# 按真值函数筛选
# dropwhile
x = itertools.dropwhile(lambda e: e < 5, range(10))
list(x) # => [5, 6, 7, 8, 9]
# takewhile
x = itertools.takewhile(lambda e: e < 5, range(10))
list(x) # => [0, 1, 2, 3, 4]

# 分组
x = itertools.groupby(range(10), lambda x: x < 5 or x > 8)
for condition, numbers in x:
    print(condition, list(numbers))

""" 
True [0, 1, 2, 3, 4]
False [5, 6, 7, 8]
True [9]
"""

