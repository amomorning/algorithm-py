# algorithm_py

Algorithm template for online contests, available on  

- [Codeforces](https://codeforces.com/)(pypy 3.10)
- [Atcoder](https://atcoder.jp/)(CPython 3.11.4 | pypy 3.10)

## basic usage

- [basic](https://github.com/amomorning/algorithm-py/blob/master/basic/basic.py)
- [input and output](https://github.com/amomorning/algorithm-py/blob/master/basic/io.py)
- [math and cmath](https://github.com/amomorning/algorithm-py/blob/master/basic/use_math.py)
- [random](https://github.com/amomorning/algorithm-py/tree/master/basic/random)
- [copy](https://github.com/amomorning/algorithm-py/blob/master/basic/use_copy.py)
- [itertools](https://github.com/amomorning/algorithm-py/blob/master/basic/use_itertools.py)
- [functools](https://github.com/amomorning/algorithm-py/blob/master/basic/use_functools.py)
- [collections](https://github.com/amomorning/algorithm-py/blob/master/basic/use_collections.py)
- [regular expressions](https://github.com/amomorning/algorithm-py/blob/master/basic/use_re.py)

## useful modules

- [numpy](https://github.com/amomorning/algorithm-py/blob/master/basic/use_numpy.py)
- [networkx](https://github.com/amomorning/algorithm-py/blob/master/basic/use_networkx.py) 

## algorithm template

- [data structure](https://github.com/amomorning/algorithm-py/blob/master/template/data_structures.py)
  - Segment Tree
  - Lazy Segment Tree (Monoid)
  - ZKW Segment Tree
  - Fenwick Tree
  - Sparse Table
  - Union Find
  - Encoded Dict
  - Sorted List
  - Sorted Blocks
- [math and number theory](https://github.com/amomorning/algorithm-py/blob/master/template/math_number.py)
  - Quick Power
  - Binomial
  - Modulo Integral
    - Note: this's not faster than python big number with proper modulo operations
  - Prime Table
  - Exgcd and Chinese remainder theorem
- [graph](https://github.com/amomorning/algorithm-py/blob/master/template/graph.py)
  - BFS
  - Colorize bipartite graph
  - Topo sort
  - Shortest path
    - Floyd $O(n^3)$
    - Single source
      - $O(n)$ on DAG
      - Dijkstra
      - Spfa
  - Minimal spinning tree
    - Prim
    - Kruskal
  - MaxFlow
    - Dinic
- [string](https://github.com/amomorning/algorithm-py/blob/master/template/string.py)
  - 1d Hash
  - KMP
  - Manacher
  - Longest Palindromic Prefix
  - Binary Trie(Min XOR)
  - Trie

### tricks

- [bit tricks](https://github.com/amomorning/algorithm-py/blob/master/template/bit_tricks.ipynb)
  - BitSet
- [list tricks](https://github.com/amomorning/algorithm-py/blob/master/template/list_tricks.py)

## geometry

- [geometry](https://github.com/amomorning/algorithm-py/tree/master/geometry)
  - [Point (E^d)](https://github.com/amomorning/algorithm-py/tree/master/geometry/point.py)
    - quaternion
    - rotate
    - matrix (row major)
    - polar_cmp
    - find_points_in_aabb
  - [Segment]((https://github.com/amomorning/algorithm-py/tree/master/geometry/segment.py))
    - intersection
    - point on segment
    - projection of point
    - distance to point / segment
  - [Plane]((https://github.com/amomorning/algorithm-py/tree/master/geometry/plane.py))
    - projection of point / segment
  - [Matrix](https://github.com/amomorning/algorithm-py/tree/master/geometry/matrix.py)
    - from translate
    - from rotate
    - from scale
  - [Triangle](https://github.com/amomorning/algorithm-py/tree/master/geometry/triangle.py)
    - normal
    - area
    - bounding box
    - centriod
    - incircle (内心)
    - circumcircle (外心)
    - point in triangle
    - uniform sample in triangle(three kinds of algorithm)
  - [Polygon](https://github.com/amomorning/algorithm-py/tree/master/geometry/polygon.py)
    - is convex or not
    - signed area / area
    - centriod (area based)
    - triangulation by earcut algorithm
    - point in polygon
  - [Convex Hull](https://github.com/amomorning/algorithm-py/tree/master/geometry/convexhull.py)
    - 2d quick convex hull from point cloud
  - [Delaunay Trianglation](https://github.com/amomorning/algorithm-py/tree/master/geometry/delaunay.py)
    - Fortune algorithm (o(n log n))
  - other

## errors and other notes

### known pypy errors

- [pypy](https://github.com/amomorning/algorithm-py/blob/master/basic/use_pypy.py) notes

### `sqrt` precision error

``` py
s = int(1e18)-2

x = math.floor(math.sqrt(s))
while (x+1) * (x+1) <= s: x += 1
while x * x > s: x -= 1
```

## Time complexity of python operations

### list

#### O(1)

- Append
- pop last
- get item
- set item
- get length

#### O(k)

- get slice
- extend(k)

#### O(n)

- copy
- insert
- pop(id)
- x in list
- del item
- iteration
- min, max, sum

#### O(n log n)

- sort

### collections.deque

#### O(1)

- append
- appendleft
- pop
- popleft

#### O(k)

- extend
- extendleft
- rotate

#### O(n)

- copy
- remove


### set

#### O(1)

- x in s

#### O(len(s))

- s-t
- s^t

#### O(len(t))

- s.difference_update(t)
- s.symmetric_difference_update(t)

#### O(min(len(s), len(t)))

- s&t

#### O(len(s)+len(t))

- s|t

### dict

#### O(1)

- k in d
- get item
- set item
- del item

#### O(n)

- copy
- iteration

### heapq

#### O(logn)

- heappush
- heappop
- heappushpop
- heapreplace

#### O(nlogk)

- merge

#### O(n)

- heapify

#### O(n+klog(n))

- nsmallest
- nlargest

### bisect

#### O(logn)

- bisect
- bisect_left
- bisect_right

#### O(n)

- insort
- insort_left
- insort_right

### References

- [TimeComplexity - Python Wiki](https://wiki.python.org/moin/TimeComplexity#list)
- [heapq — Heap queue algorithm — Python 3.10.6 documentation](https://docs.python.org/3/library/heapq.html#module-heapq)
- [Python's heapq module](https://johnlekberg.com/blog/2020-11-01-stdlib-heapq.html)
- [bisect — Array bisection algorithm — Python 3.10.6 documentation](https://docs.python.org/3/library/bisect.html)

### complexity analysis

#### Big O

**Big O** notation is used to give an **upper bound** on the asymptotic growth

- `O(1)`: constant
- `O(log n)`: logarithmic
- `O(n)`: linear
- `O(n log n)`: log-linear
- `O(n^k)`: polynomial, where `k` is a constant
- `O(c^n)`: exponential, where `c` is a constant



## tricks

### mock interactive problem
<!-- TODO -->

### diff with brute force methods

``` bash
python gen.py > data.in && \ # generate random data
    python brute.py > brute.out && \ # brute force output
    python e.py > e.out && \ # algorithm output
    diff e.out brute.out # diff
```
