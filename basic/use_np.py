# Can not be used in current contest environment
# 2022-06-01
import numpy as np

################################
### 0. 基本用法
################################
 
## 初始化

## 二维数组
dp = np.zeros((1<<20, 20), dtype=np.bool)
dp.shape()

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

