## algorithm_py
Algorithm template for online contests, available on  
- [Codeforces](https://codeforces.com/)(pypy 3.9.10) 
- [Atcoder](https://atcoder.jp/)(Python 3.8.2 | pypy 3.6.9)

### basic usage
- [basic](https://github.com/amomorning/algorithm-py/blob/master/basic/basic.py)
- [input and output](https://github.com/amomorning/algorithm-py/blob/master/basic/io.py)
- [math and cmath](https://github.com/amomorning/algorithm-py/blob/master/basic/use_math.py)
- [itertools](https://github.com/amomorning/algorithm-py/blob/master/basic/use_itertools.py)
- [collections](https://github.com/amomorning/algorithm-py/blob/master/basic/use_collections.py)
- [regular expressions](https://github.com/amomorning/algorithm-py/blob/master/basic/use_re.py)

### algorithm template
- [data structure](https://github.com/amomorning/algorithm-py/blob/master/template/data_structures.py)
    - Segment Tree
    - Fenwick Tree
    - Sparse Table
    - Union Find
    - Encoded Dict
    - Sorted List
- [math and number theory](https://github.com/amomorning/algorithm-py/blob/master/template/math_number.py)
    - Quick Power
    - Binomial
    - Modulo Integral
      - Note: this's not faster than python big number with proper modulo operations
- graph
    - dijkstra


### errors and other notes
- [pypy](https://github.com/amomorning/algorithm-py/blob/master/basic/use_pypy.py) notes

### basic skills

#### Mock interactive problem
<!-- TODO -->

#### Diff with brute force methods
``` bash
python gen.py > data.in && \ # generate random data
    python brute.py > brute.out && \ # brute force output
    python e.py > e.out && \ # algorithm output
    diff e.out brute.out # diff
```
