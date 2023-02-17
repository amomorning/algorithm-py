import math

class SegmentTree:
    def __init__(self, size, select=min, elem=math.inf):
        self.size = 1 << size.bit_length()
        self.tree = [elem] * (self.size << 1)
        self.select = select
        self.elem = elem
 
    def __getitem__(self, i):
        return self.tree[i + self.size]
 
    def update(self, i, x):
        i0 = i + self.size
        while i0:
            self.tree[i0] = x
            x = self.select(self.tree[i0], self.tree[i0 ^ 1])
            i0 >>= 1
 
    def query(self, i, j):
        """ query range [i, j)
        """
        x = self.elem
        l = i + self.size
        r = j + self.size
        while l < r:
            if l & 1:
                x = self.select(x, self.tree[l])
                l += 1
            if r & 1:
                x = self.select(x, self.tree[r - 1])
            l >>= 1
            r >>= 1
        return x


class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bits = [0] * n
    
    def ask(self, p, tot=0):
        while p >= 0: tot += self.bits[p]; p -= ~p & p + 1
        return tot
    
    def add(self, p, x):
        while p < self.n: self.bits[p] += x; p += ~p & p + 1

    ''' k in [1, n]
    '''
    def kth(self, k):
        p, t = -1, 0
        b = self.n.bit_length()
        while ~b:
            p += 1 << b
            if p >= self.n or t + self.bits[p] >= k: 
                p -= 1 << b
            else:
                t += self.bits[p]
            b -= 1
        return -1 if p+1 >= self.n else p + 1



class SparseTable:
    def __init__(self, a, select=min):
        N = len(a); 
        L = N.bit_length()

        self.u = [[0] * N for _ in range(L)]
        self.select = select

        for i in range(N):
            self.u[0][i] = a[i]
        for i in range(1, L):
            for j in range(N-(1<<i)+1):
                self.u[i][j] = self.select(self.u[i-1][j], self.u[i-1][j+(1<<(i-1))])
        
    def ask(self, l, r):
        i = (r - l).bit_length()-1
        return self.select(self.u[i][l], self.u[i][r-(1<<i)+1])

class UnionFind:
    def __init__(self, x):
        self.uf = [-1] * x
 
    def find(self, x):
        r = x
        while self.uf[x] >= 0:
            x = self.uf[x]
        while r != x:
            self.uf[r], r = x, self.uf[r]
        return x
 
    def same(self, x, y):
        return self.find(x) == self.find(y)

    def union(self, x, y):
        ux, uy = self.find(x), self.find(y)
        if ux == uy:
            return False
        if self.uf[ux] >= self.uf[uy]:
            self.uf[uy] += self.uf[ux]
            self.uf[ux] = uy
        else:
            self.uf[ux] += self.uf[uy]
            self.uf[uy] = ux
        return True
 
    def count(self):
        return sum(f < 0 for f in self.uf)
 
    def valid(self):
        n = len(self.uf)
        for c in range(n):
            if self.uf[c] == -n:
                return True
        return False
    
    def roots(self):
        return [i for i, f in enumerate(self.uf) if f < 0]

    def groups(self):
        n = len(self.uf)
        ret = [[] for _ in range(n)]
        for i in range(n):
            f = self.find(i)
            ret[f].append(i)
        return ret
 
    def __print__(self):
        return self.uf


import random
class Encodict:
    def __init__(self, func=lambda : 0):
        self.RANDOM = random.randint(0, 1<<32)
        self.default = func
        self.dict = {}
    
    def __getitem__(self, key):
        k = self.RANDOM ^ key
        if k not in self.dict:
            self.dict[k] = self.default()
        return self.dict[k]
    
    def __setitem__(self, key, item):
        k = self.RANDOM ^ key
        self.dict[k] = item

    def keys(self):
        return [self.RANDOM ^ i for i in self.dict]
    
    def items(self):
        return [(self.RANDOM ^ i, self.dict[i]) for i in self.dict]
    
    def sorted(self, by_value=False, reverse=False):
        if by_value:
            self.dict = dict(sorted(self.dict.items(), \
                key=lambda x:x[1], reverse=reverse))
        else:
            self.dict = dict(sorted(self.dict.items(), \
                key=lambda x:self.RANDOM^x[0], reverse=reverse))

# 有序 map
# TODO: implement c++ std::map

# 有序 set
class SortedList:
    def __init__(self, iterable=[], _load=200):
        """Initialize sorted list instance."""
        values = sorted(iterable)
        self._len = _len = len(values)
        self._load = _load
        self._lists = _lists = [values[i:i + _load] for i in range(0, _len, _load)]
        self._list_lens = [len(_list) for _list in _lists]
        self._mins = [_list[0] for _list in _lists]
        self._fen_tree = []
        self._rebuild = True

    def _fen_build(self):
        """Build a fenwick tree instance."""
        self._fen_tree[:] = self._list_lens
        _fen_tree = self._fen_tree
        for i in range(len(_fen_tree)):
            if i | i + 1 < len(_fen_tree):
                _fen_tree[i | i + 1] += _fen_tree[i]
        self._rebuild = False

    def _fen_update(self, index, value):
        """Update `fen_tree[index] += value`."""
        if not self._rebuild:
            _fen_tree = self._fen_tree
            while index < len(_fen_tree):
                _fen_tree[index] += value
                index |= index + 1

    def _fen_query(self, end):
        """Return `sum(_fen_tree[:end])`."""
        if self._rebuild:
            self._fen_build()

        _fen_tree = self._fen_tree
        x = 0
        while end:
            x += _fen_tree[end - 1]
            end &= end - 1
        return x

    def _fen_findkth(self, k):
        """Return a pair of (the largest `idx` such that `sum(_fen_tree[:idx]) <= k`, `k - sum(_fen_tree[:idx])`)."""
        _list_lens = self._list_lens
        if k < _list_lens[0]:
            return 0, k
        if k >= self._len - _list_lens[-1]:
            return len(_list_lens) - 1, k + _list_lens[-1] - self._len
        if self._rebuild:
            self._fen_build()

        _fen_tree = self._fen_tree
        idx = -1
        for d in reversed(range(len(_fen_tree).bit_length())):
            right_idx = idx + (1 << d)
            if right_idx < len(_fen_tree) and k >= _fen_tree[right_idx]:
                idx = right_idx
                k -= _fen_tree[idx]
        return idx + 1, k

    def _delete(self, pos, idx):
        """Delete value at the given `(pos, idx)`."""
        _lists = self._lists
        _mins = self._mins
        _list_lens = self._list_lens

        self._len -= 1
        self._fen_update(pos, -1)
        del _lists[pos][idx]
        _list_lens[pos] -= 1

        if _list_lens[pos]:
            _mins[pos] = _lists[pos][0]
        else:
            del _lists[pos]
            del _list_lens[pos]
            del _mins[pos]
            self._rebuild = True

    def _loc_left(self, value):
        """Return an index pair that corresponds to the first position of `value` in the sorted list."""
        if not self._len:
            return 0, 0

        _lists = self._lists
        _mins = self._mins

        lo, pos = -1, len(_lists) - 1
        while lo + 1 < pos:
            mi = (lo + pos) >> 1
            if value <= _mins[mi]:
                pos = mi
            else:
                lo = mi

        if pos and value <= _lists[pos - 1][-1]:
            pos -= 1

        _list = _lists[pos]
        lo, idx = -1, len(_list)
        while lo + 1 < idx:
            mi = (lo + idx) >> 1
            if value <= _list[mi]:
                idx = mi
            else:
                lo = mi

        return pos, idx

    def _loc_right(self, value):
        """Return an index pair that corresponds to the last position of `value` in the sorted list."""
        if not self._len:
            return 0, 0

        _lists = self._lists
        _mins = self._mins

        pos, hi = 0, len(_lists)
        while pos + 1 < hi:
            mi = (pos + hi) >> 1
            if value < _mins[mi]:
                hi = mi
            else:
                pos = mi

        _list = _lists[pos]
        lo, idx = -1, len(_list)
        while lo + 1 < idx:
            mi = (lo + idx) >> 1
            if value < _list[mi]:
                idx = mi
            else:
                lo = mi

        return pos, idx

    def add(self, value):
        """Add `value` to sorted list."""
        _load = self._load
        _lists = self._lists
        _mins = self._mins
        _list_lens = self._list_lens

        self._len += 1
        if _lists:
            pos, idx = self._loc_right(value)
            self._fen_update(pos, 1)
            _list = _lists[pos]
            _list.insert(idx, value)
            _list_lens[pos] += 1
            _mins[pos] = _list[0]
            if _load + _load < len(_list):
                _lists.insert(pos + 1, _list[_load:])
                _list_lens.insert(pos + 1, len(_list) - _load)
                _mins.insert(pos + 1, _list[_load])
                _list_lens[pos] = _load
                del _list[_load:]
                self._rebuild = True
        else:
            _lists.append([value])
            _mins.append(value)
            _list_lens.append(1)
            self._rebuild = True

    def discard(self, value):
        """Remove `value` from sorted list if it is a member."""
        _lists = self._lists
        if _lists:
            pos, idx = self._loc_right(value)
            if idx and _lists[pos][idx - 1] == value:
                self._delete(pos, idx - 1)

    def remove(self, value):
        """Remove `value` from sorted list; `value` must be a member."""
        _len = self._len
        self.discard(value)
        if _len == self._len:
            raise ValueError('{0!r} not in list'.format(value))

    def pop(self, index=-1):
        """Remove and return value at `index` in sorted list."""
        pos, idx = self._fen_findkth(self._len + index if index < 0 else index)
        value = self._lists[pos][idx]
        self._delete(pos, idx)
        return value

    def bisect_left(self, value):
        """Return the first index to insert `value` in the sorted list."""
        pos, idx = self._loc_left(value)
        return self._fen_query(pos) + idx

    def bisect_right(self, value):
        """Return the last index to insert `value` in the sorted list."""
        pos, idx = self._loc_right(value)
        return self._fen_query(pos) + idx

    def count(self, value):
        """Return number of occurrences of `value` in the sorted list."""
        return self.bisect_right(value) - self.bisect_left(value)

    def __len__(self):
        """Return the size of the sorted list."""
        return self._len

    def __getitem__(self, index):
        """Lookup value at `index` in sorted list."""
        pos, idx = self._fen_findkth(self._len + index if index < 0 else index)
        return self._lists[pos][idx]

    def __delitem__(self, index):
        """Remove value at `index` from sorted list."""
        pos, idx = self._fen_findkth(self._len + index if index < 0 else index)
        self._delete(pos, idx)

    def __contains__(self, value):
        """Return true if `value` is an element of the sorted list."""
        _lists = self._lists
        if _lists:
            pos, idx = self._loc_left(value)
            return idx < len(_lists[pos]) and _lists[pos][idx] == value
        return False

    def __iter__(self):
        """Return an iterator over the sorted list."""
        return (value for _list in self._lists for value in _list)

    def __reversed__(self):
        """Return a reverse iterator over the sorted list."""
        return (value for _list in reversed(self._lists) for value in reversed(_list))

    def __repr__(self):
        """Return string representation of sorted list."""
        return 'SortedList({0})'.format(list(self))


import bisect
label_counter_ = 0 
class Iterator:
    def __init__(self, label = None):
        if label is None:
            global label_counter_
            self.label = label_counter_
            label_counter_ += 1
        else: self.label = label
   
    def __lt__(self, other)-> bool:
        return self.label < other.label
    
    def __eq__(self, other) -> bool:
        return self.label == other.label

    def __repr__(self):
        return f'Iterator({self.label})'
    
    def __hash__(self):
        return hash(self.label)


class SortedBlock:
    def __init__(self):
        self.data_ = list()
        self.iterator_set_ = dict()
    
    def __repr__(self):
        return str(self.data_) + '; ' + str(self.iterator_set_)
    
    def add(self, item, iter):
        self.iterator_set_[iter] = 1
        bisect.insort_left(self.data_, (item, iter))
    
    def delete(self, iter):
        if not self.contains(iter): return False
        self.iterator_set_[iter] = 0
        for i in range(0, len(self.data_)):
            if self.data_[i][1] == iter:
                del self.data_[i]
                return True
        assert False
    
    def contains(self, iter):
        if iter in self.iterator_set_: 
            return bool(self.iterator_set_[iter])
        return False

    def access(self, iter):
        for item, it in self.data_:
            if it == iter: return item

    @property
    def smallest_elem(self):
        return self.data_[0][0]
    
    @property
    def smallest_elem_iter(self):
        return self.data_[0][1]

    @property
    def largest_elem(self):
        return self.data_[-1][0]

    @property
    def largest_elem_iter(self):
        return self.data_[-1][1]
    
    def __len__(self):
        return len(self.data_)
    
    def size(self):
        return len(self.data_)
    
    def empty(self):
        return len(self) == 0
    
    def next(self, iter):
        for i in range(len(self)):
            if self.data_[i][1] == iter:
                return self.data_[i+1][1]
    
    def prev(self, iter):
        for i in range(len(self)):
            if self.data_[i][1] == iter:
                return self.data_[i-1][1]


    def push_back(self, item, iter):
        self.data_.append((item, iter))

    def pop_tail(self, size):
        tail = SortedBlock()
        for i in range(-size, 0):
            item, iter = self.data_[i]
            tail.push_back(item, iter)
            del self.iterator_set_[iter]
            # self.iterator_set_[iter] = 0
            tail.iterator_set_[iter] = 1
        self.data_ = self.data_[:-size]
        return tail
    
    def lower_bound(self, item):
        i = len(self.data_)
        while i > 0 and item <= self.data_[i-1][0]:
            i -= 1
        return self.data_[i][1]
    
    def upper_bound(self, item):
        i = len(self.data_)
        while i > 0 and item < self.data_[i-1][0]:
            i -= 1
        return self.data_[i][1]


# sorted block list
MAX_BLOCK_SIZE = 4
HALF_MAX_BLOCK_SIZE = (MAX_BLOCK_SIZE + 1) // 2

class SortedBlockList:
    def __init__(self):
        self.blocks_ = []
        self.end_ = Iterator()
    
    
    def adjust(self, i):
        while self.blocks_[i].size() >= MAX_BLOCK_SIZE:
            self.blocks_.insert(i+1, self.blocks_[i].pop_tail(HALF_MAX_BLOCK_SIZE))
        if self.blocks_[i].empty():
            del self.blocks_[i]

    def add(self, elem, iter = None):
        if iter is None: iter = Iterator()
        i = 0
        while i < len(self.blocks_) and self.blocks_[i].largest_elem < elem:
            i += 1
        if i == len(self.blocks_): 
            if len(self.blocks_) == 0: self.blocks_.append(SortedBlock())
            else: i -= 1
        self.blocks_[i].add(elem, iter)
        self.adjust(i)
    
    def delete(self, iter):
        i = 0
        while i < len(self.blocks_) and not self.blocks_[i].delete(iter):
            i += 1
        self.adjust(i)
    
    def access(self, iter):
        for i in range(len(self.blocks_)):
            if self.blocks_[i].contains(iter):
                return self.blocks_[i].access(iter)
        
    def begin(self):
        if len(self.blocks_) == 0: return self.end_
        return self.blocks_[0].smallest_elem_iter
    
    def end(self):
        return self.end_
    
    def prev(self, iter):
        i = len(self.blocks_)
        while i > 0 and not self.blocks_[i-1].contains(iter):
            i -= 1
        if iter == self.blocks_[i].smallest_elem_iter:
            return self.blocks_[i-1].largest_elem_iter
        return self.blocks_[i].prev(iter)
    
    def next(self, iter):
        i = 0
        while i < len(self.blocks_) and not self.blocks_[i].contains(iter):
            i += 1
        if iter == self.blocks_[i].largest_elem_iter:
            if i == len(self.blocks_) - 1: return self.end_
            return self.blocks_[i+1].smallest_elem_iter
        return self.blocks_[i].next(iter)
    
    def lower_bound(self, elem):
        i = 0
        while i < len(self.blocks_) and self.blocks_[i].largest_elem < elem:
            i += 1
        if i == len(self.blocks_): return self.end_
        return self.blocks_[i].lower_bound(elem)
    
    def upper_bound(self, elem):
        i = 0
        while i < len(self.blocks_) and self.blocks_[i].largest_elem <= elem:
            i += 1
        if i == len(self.blocks_): return self.end_
        return self.blocks_[i].upper_bound(elem)

class Stack(list):
    def __init__(self, iterable=None):
        if iterable is not None:
            super().__init__(item for item in iterable)
    
    def push(self, *args):
        if len(args) == 1:
            self.append(args[0])
        else:
            self.append(args)
    
    def back(self):
        return self[-1]
    
    def empty(self):
        return len(self) == 0
    
    def length(self):
        return len(self)
