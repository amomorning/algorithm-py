import random
import time

seed = 1
random.seed(seed)

#
# random range

# 随机 (0, 1) 不闭合区间
random.random()

# 随机 [a, b) 
random.uniform(1.0, 2.0)

# 随机整数[a, b]闭合区间
random.randint(0, 10)

# 随机整数[a, b)左闭右开：不常用
random.randrange(0, 10, 2)

#
# sequence

# 随机打乱
random.shuffle([1, 2, 3])

# 随机选 1 个
random.choice([1, 2, 3])

# 可重复选择 k 个
random.choices([1, 2, 3], k=2)

# 不重复选择 k 个
random.sample([1, 2, 3], k=2)

# 

# 高斯随机 
random.gauss(3, 1)

