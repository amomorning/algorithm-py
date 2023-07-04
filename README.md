# algorithm_py

Algorithm template for online contests, available on  

- [Codeforces](https://codeforces.com/)(pypy 3.9.10)
- [Atcoder](https://atcoder.jp/)(Python 3.8.2 | pypy 3.6.9)

## basic usage

- [basic](https://github.com/amomorning/algorithm-py/blob/master/basic/basic.py)
- [input and output](https://github.com/amomorning/algorithm-py/blob/master/basic/io.py)
- [math and cmath](https://github.com/amomorning/algorithm-py/blob/master/basic/use_math.py)
- [itertools](https://github.com/amomorning/algorithm-py/blob/master/basic/use_itertools.py)
- [collections](https://github.com/amomorning/algorithm-py/blob/master/basic/use_collections.py)
- [regular expressions](https://github.com/amomorning/algorithm-py/blob/master/basic/use_re.py)

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
- [geometry](https://github.com/amomorning/algorithm-py/tree/master/template/geometry)
  - Point (E^d)
    - quaternion
    - rotate
    - matrix (row major)
    - polar_cmp
    - find_points_in_aabb
  - Segment
    - intersection
    - point on segment
    - projection of point
    - distance to point / segment
  - Plane
    - projection of point / segment
  - Matrix
    - from translate
    - from rotate
    - from scale
  - Triangle
    - normal
    - area
    - bounding box
    - centriod
    - incircle (内心)
    - circumcircle (外心)
    - point in triangle
    - uniform sample in triangle(three kinds of algorithm)
  - Polygon
    - is convex or not
    - signed area / area
    - centriod (area based)
    - triangulation by earcut algorithm
    - point in polygon
  - Convex Hull
    - 2d quick convex hull from point cloud
  - Delaunay Trianglation
    - Fortune algorithm (o(n log n))
  - other

- [bit tricks](https://github.com/amomorning/algorithm-py/blob/master/template/bit_tricks.ipynb)
  - BitSet
- [list tricks](https://github.com/amomorning/algorithm-py/blob/master/template/list_tricks.py)

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
