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

