import numpy as np
from timeit import timeit


################################
### 0. 基本用法
################################

## 数据类型 dtype
Z = np.ones(4*1000000, np.float32)
Z[...] = 0
# np.int16      0.03001
# np.float16    0.02912
# np.int32      0.02862
# np.float32    0.02861
# np.int64      0.02863
# np.float32    0.02878
# np.complex128 0.03980
# np.int8       0.03862
print("%.5f" %timeit("Z.view(np.int16)[...] = 0", globals=globals(), number=100)) 
print("%.5f" %timeit("Z.view(np.float16)[...] = 0", globals=globals(), number=100))
print("%.5f" %timeit("Z.view(np.int32)[...] = 0", globals=globals(), number=100)) 
print("%.5f" %timeit("Z.view(np.float32)[...] = 0", globals=globals(), number=100)) 
print("%.5f" %timeit("Z.view(np.int64)[...] = 0", globals=globals(), number=100)) 
print("%.5f" %timeit("Z.view(np.float64)[...] = 0", globals=globals(), number=100)) 
print("%.5f" %timeit("Z.view(np.complex128)[...] = 0", globals=globals(), number=100)) 
print("%.5f" %timeit("Z.view(np.int8)[...] = 0", globals=globals(), number=100)) 

## Memory Layout
# ndarray 类的实例主要是连续的内存块，使用索引方案来访问数组中的元素
Z = np.arange(9).reshape(3, 3).astype(np.int16)
print(Z.itemsize) # 2
print(Z.shape) # (3, 3)
print(Z.nbytes) # 18
print(Z.strides) # (6, 2) = (Z.itemsize * Z.shape[1], Z.itemsize)

## Views and Copies
# - indexing returns a view
# - fancy indexing returns a copy
Z = np.random.uniform(0, 1, (5, 5))
Z1 = Z[:3, :]
Z2 = Z[[0, 1, 2], :]
print(np.allclose(Z1, Z2)) # True
print(Z1.base is Z) # True
print(Z2.base is Z) # False
print(Z2.base is None) # True



## 初始化

dp = np.zeros((1<<20, 20), dtype=bool)
dp.shape

np.ones(9) * 2 # [2. 2. 2. 2. 2. 2. 2. 2. 2.]
np.arange(9) # [0 1 2 3 4 5 6 7 8]
np.array([1, 0, 1, 1])
np.arange(9).reshape(3,3) #[[0 1 2] [3 4 5] [6 7 8]]
np.linspace(0, 1, 5) # [0.   0.25 0.5  0.75 1.  ]
Z = np.gradient(np.arange(9).reshape(3,3)) 
# [[3., 3., 3.], [3., 3., 3.], [3., 3., 3.]]
# [[1., 1., 1.], [1., 1., 1.], [1., 1., 1.]]


## 索引
Z = np.arange(9).reshape(3,3)
# [[0 1 2]
#  [3 4 5]
#  [6 7 8]]
print(Z[0,0]) # 0 - view
print(Z[::2, ::2]) # [[0 2] [6 8]] - view
print(Z[[0, 1], [0, 2]]) # [0, 5] - copy

## Reshaping
Z = np.array([0,0,0,0,0,0,0,0,0,0,1,0])
Z = np.array([0,0,0,0,0,0,0,0,0,0,1,0]).reshape(12, 1)
Z = np.array([0,0,0,0,0,0,0,0,0,0,1,0]).reshape(3, 4)
Z = np.array([0,0,0,0,0,0,0,0,0,0,1,0]).reshape(4, 3)
Z = np.array([0,0,0,0,0,0,0,0,0,0,1,0]).reshape(6, 2)
Z = np.array([0,0,0,0,0,0,0,0,0,0,1,0]).reshape(2, 6)

## Broadcasting
Z1 = np.arange(9).reshape(3,3) # [[0 1 2] [3 4 5] [6 7 8]]
Z2 = 1  # 1 -> [[1 1 1] [1 1 1] [1 1 1]]
Z1 + Z2 # [[1 2 3] [4 5 6] [7 8 9]]

Z1 = np.arange(9).reshape(3,3) # [[0 1 2] [3 4 5] [6 7 8]]
Z2 = np.arange(3)[::-1].reshape(3,1) # [[2] [1] [0]] -> [[2, 2, 2], [1, 1, 1], [0, 0, 0]]
print(Z1+Z2) # [[2 3 4] [4 5 6] [6 7 8]]

Z1 = np.arange(9).reshape(3,3) # [[0 1 2] [3 4 5] [6 7 8]]
Z2 = np.arange(3)[::-1] # [2, 1, 0] -> [[2, 1, 0], [2, 1, 0], [2, 1, 0]]
print(Z1+Z2) # [[2 2 2] [5 5 5] [8 8 8]]

Z1 = np.arange(3).reshape(3,1) # [[0] [1] [2]] -> [[0, 0, 0], [1, 1, 1], [2, 2, 2]]
Z2 = np.arange(3).reshape(1,3) # [[0, 1, 2]] -> [[0, 1, 2], [0, 1, 2], [0, 1, 2]]
print(Z1+Z2) # [[0 1 2] [1 2 3] [2 3 4]]

################################
### 1. 爱因斯坦求和约定
################################

## 转置 B_ji=A_ij
a = np.arange(0, 9).reshape(3, 3)
b = np.einsum('ij->ji', a)
# => array([[0, 3, 6],
#           [1, 4, 7],
#           [2, 5, 8]])

## 求和 sum_ij A_ij
b = np.einsum('ij->', a) # => 36

## 维度求和 sum_i A_ij
b = np.einsum('ij->i', a) # => array([ 3, 12, 21])

## 矩阵点积
a = np.arange(0, 12).reshape(3, 4)
b = np.arange(0, 12).reshape(3, 4)
c = np.einsum('ij,ij->', a, b) # => 506

## 矩阵外积 
a = np.arange(0, 12).reshape(3, 4)
b = np.arange(0, 12).reshape(4, 3)
c = np.einsum('ik,kj->ij', a, b)
# => array([[ 42,  48,  54],
#           [114, 136, 158],
#           [186, 224, 262]])

a = np.array([1, 2])
b = np.array([1, 3])

print(np.cross(a, b))
