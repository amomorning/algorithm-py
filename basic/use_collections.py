import collections
print(dir(collections))

from collections import Counter
dict(Counter('eleven'))
# {'e': 3, 'l': 1, 'v': 1, 'n': 1}

# 返回字典d前n个最大值对应的键
from heapq import nlargest

dic ={'d': 10, 'b': 8, 'c': 9, 'a': 10} 
nlargest(3, dic, key = lambda k: dic[k])

# 为tuple命名
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y', 'z'])  # 定义名字为Point的元祖，字段属性有x,y,z
lst = [Point(1.5, 2, 3.0), Point(-0.3, -1.0, 2.1), Point(1.3, 2.8, -2.5)]
print(lst[0].y - lst[1].y) # => 3.0
