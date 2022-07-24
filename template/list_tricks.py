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
