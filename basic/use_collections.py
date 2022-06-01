import collections
print(dir(collections))

from collections import Counter
dict(Counter('eleven'))
# {'e': 3, 'l': 1, 'v': 1, 'n': 1}

# 为tuple命名
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y', 'z'])  # 定义名字为Point的元祖，字段属性有x,y,z
lst = [Point(1.5, 2, 3.0), Point(-0.3, -1.0, 2.1), Point(1.3, 2.8, -2.5)]
print(lst[0].y - lst[1].y) # => 3.0


# 用 deque 作为队列
from collections import deque
def bfs(x):
    q = deque()
    q.append((x, 0))
    vis = {}

    while q:
        # pop()默认为popright, 取队首使用popleft()
        u = q.popleft() 

        # do something
        q.append()


# 用 heapq 作为优先队列（默认为最小值在堆顶）
from heapq import heappush, heappop
from heapq import heapify

q = []
while q:
    u = heappop(q)

    v = u + 1
    heappush(q, v)

# 返回字典d前n个最大值对应的键
from heapq import nlargest
dic ={'d': 10, 'b': 8, 'c': 9, 'a': 10} 
nlargest(3, dic, key = lambda k: dic[k])
