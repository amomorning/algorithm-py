# 求众数
lst = [1, 3, 3, 2, 1, 1, 2]
r = max(lst, key=lambda v: lst.count(v))

# 字典赋值
dict(a='a',b='b') # => {'a': 'a', 'b': 'b'}
dict(zip(['a','b'],[1,2])) # => {'a': 1, 'b': 2}
dict([('a',1),('b',2)]) # => {'a': 1, 'b': 2}

# 合并字典
def merge_dict(dic1, dic2):
    return {**dic1, **dic2}  # python3.5后支持的一行代码实现合并字典

merge_dict({'a': 1, 'b': 2}, {'c': 3})  # {'a': 1, 'b': 2, 'c': 3}

# 按key排序
dic = sorted(d.items(), key=lambda z: z[0], reverse=True)

# 去重
a = [3, 1, 1, 2, 5, 3, 6]
list(set(a))

# 离散化
from bisect import bisect_left
def discretization(arr:list) -> list:
    ret = []
    idx = sorted(set(arr))
    for a in arr:
        x = bisect_left(idx, a)
        ret.append(x)
    return ret

# 绑定
list(zip(a, range(len(a))))


# 获取 ban 一些 id 后的第 k 大
def get_kth(k, arr, ref):
    k = k - len(ref) + 2

    for x in ref:
        if k < len(arr) and x <= arr[k][0]: k += 1
    
    if k >= len(arr): return math.inf
    return arr[k][0]

a = []
ids = []

arr = sorted(list(zip(a, range(len(a)))))
ref = [a[i] for i in ids]
k = 2
print(get_kth(k, arr, ref))

a = [1, 2, 4, 5]
list(filter(lambda x: x%2 == 0, a))
