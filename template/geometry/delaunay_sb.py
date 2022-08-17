from functools import cmp_to_key
from point import *
from triangle import *
import heapq

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

tot_arc = 0
def generate_unique_id():
    global tot_arc
    tot_arc += 1
    return tot_arc


sweepx = 0.0
class Arc:
    def __init__(self, p, q, i, id=0):
        self.p = p
        self.q = q
        self.i = i
        self.id = id
        self.unique = generate_unique_id()
    
    def __str__(self):
        return f'Arc({self.p}, {self.q}, {self.i}, {self.id}, {self.unique})'
    
    def __repr__(self):
        return f'Arc({self.p}, {self.q}, {self.i}, {self.id}, {self.unique})'
    
    def get_y(self, x):
        if self.q.y == INF: return INF
        x += EPS
        mid = (self.p + self.q) * 0.5
        dir = (self.p - mid).rotate_90()
        D = (x - self.p.x) * (x - self.q.x)
        if cmp(dir.y) == 0: return INF/2
        return mid.y + ((mid.x - x) * dir.x + math.sqrt(D) * abs(dir)) / dir.y
    
    def __eq__(self, o):
        return self.unique == o.unique
    
    def __lt__(self, o):
        global sweepx
        if type(o) is Arc:
            return cmp(self.get_y(sweepx) - o.get_y(sweepx)) < 0
        return cmp(self.get_y(sweepx) - o) < 0
        
    def __le__(self, o):
        global sweepx
        if type(o) is Arc:
            if cmp(self.get_y(sweepx) - o.get_y(sweepx)) == 0:
                return self.unique <= o.unique
            return cmp(self.get_y(sweepx) - o.get_y(sweepx)) < 0
        return cmp(self.get_y(sweepx) - o) <= 0
     
    def __gt__(self, o):
        global sweepx
        if type(o) is Arc:
            return cmp(self.get_y(sweepx) - o.get_y(sweepx)) > 0
        return cmp(self.get_y(sweepx) - o) > 0

    def __ge__(self, o):
        global sweepx
        if type(o) is Arc:
            if cmp(self.get_y(sweepx) - o.get_y(sweepx)) == 0:
                return self.unique >= o.unique
            return cmp(self.get_y(sweepx) - o.get_y(sweepx)) > 0
        
        return cmp(self.get_y(sweepx) - o) >= 0

class DelaunayTrianglation:
    """ Reference
        [1] Improving Worst-Case Optimal Delaunay Triangulation Algorithms. https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.56.2323
        [2] DeWall: A fast divide and conquer Delaunay triangulation algorithm in E^d. https://www.sciencedirect.com/science/article/pii/S0010448597000821?via%3Dihub
        The divide and conquer algorithm has been shown to be the fastest DT generation technique sequentially.
        [3] https://codeforces.com/blog/entry/85638
        [4] https://www2.cs.sfu.ca/~binay/813.2011/Fortune.pdf
    """
    def __init__(self, points):
        self.n = len(points)
        random_angle = random.random() * math.pi / 233
        points = [Point(pt).rotate(random_angle) for pt in points]
        self.points = sorted([(points[i], i) for i in range(self.n)])

        self.Q = []
        self.edges = [] # delaunay edges
        self.valid = [] # valid[-id] == True if the vertex event is valid
        self.beachline = SortedList()
        
    
    def update(self, item):
        global sweepx

        if item.i == -1: return
        self.valid[-item.id] = False
        idx = self.beachline.bisect_left(item)
        a = self.beachline[idx - 1]

        u, v = item.q - item.p, a.p - item.p
        if cmp(abs(u.cross(v))) == 0: return # collinear: doesn't generate a vertex event

        self.ti -= 1
        item.id = self.ti

        self.valid.append(True)
        if u.cross(v) > 0: tri = Triangle(item.p, item.q, a.p)
        else: tri = Triangle(item.p, a.p, item.q)
        c, r = tri.circumcircle()
        x = c.x + r
        if cmp(x - sweepx) >= 0 and cmp(a.get_y(x) - item.get_y(x)) >= 0:
            heapq.heappush(self.Q, (x, item.id, item))

    def add_edge(self, i, j):
        if i == -1 or j == -1: return
        self.edges.append((self.points[i][1], self.points[j][1]))
    
    def add(self, i):
        p = self.points[i][0]
        # find arc to split
        c = self.beachline[self.beachline.bisect_left(p.y)]
        b = Arc(p, c.p, i)
        a = Arc(c.p, p, c.i)
        self.beachline.add(a); self.beachline.add(b)

        self.add_edge(i, c.i)

        self.update(a)
        self.update(b)
        self.update(c)
    
    def remove(self, item):
        global sweepx
        a = self.beachline.pop(self.beachline.bisect_left(item) - 1)

        idx = self.beachline.bisect_left(item)
        if idx >= len(self.beachline) - 2: idx = len(self.beachline) - 2
        b = self.beachline[idx + 1]

        print(self.beachline)
        print([ix.get_y(sweepx) for ix in self.beachline])
        self.beachline.remove(item)

        a = Arc(a.p, b.p, a.i, a.id)
        self.beachline.add(a)
        self.add_edge(a.i, b.i)

        self.update(a)
        self.update(b)

    
    def build(self, X = 1e9):
        global sweepx
        X *= 3

        self.beachline.add(Arc(Point(-X, -X), Point(-X, X), -1))
        self.beachline.add(Arc(Point(-X, X), Point(INF, INF), -1))

        for i in range(self.n):
            heapq.heappush(self.Q, (self.points[i][0].x, i, self.beachline[-1]))

        self.ti = 0
        self.valid = [False]
        while self.Q:
            e = heapq.heappop(self.Q)
            sweepx = e[0]

            if e[1] >= 0:
                self.add(e[1])
            elif self.valid[-e[1]]:
                self.remove(e[2])

def test_delaunay():
    # pts = [(3, 5), (2, 0), (1, 2), (3, 2), (3, 0), (5, 2), (5, 0), (6, 4), (4, 2), (1, 4), (0, 1)]
    # pts = [(0, 0), (1, -1), (3, 1), (1.5, 2), (4, 3), (3, 5), (1, 3)]
    pts = [(0, 0), (1, -1), (1.5, 2), (3, 1), (4, 3)]#, (3, 5), (1, 3)]
    # pts = set()
    # for _ in range(200):
    #     x = random.randint(1, 1000)
    #     y = random.randint(1, 1000)
    #     pts.add((x, y))
    # pts = [(2, 4), (10, 4), (10, 10), (3, 3), (8, 2), (4, 1)]
    # pts = [(9, 10), (2, 1), (5, 8), (8, 10), (5, 7), (6, 3), (2, 6), (2, 5), (1, 3)]

    print(list(pts))
    print(len(pts))
    for x, y in pts:
        print(x, y)
    
    
    pts = [Point(pt) for pt in pts]
    delaunay = DelaunayTrianglation(pts)
    delaunay.build()
    print(delaunay.points)

    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(6, 4))
    ax = fig.add_subplot(111)

    print(delaunay.edges)
    ax.scatter([p.x for p in pts], [p.y for p in pts], c='r')
    for i in range(len(pts)):
        x, y = pts[i].x, pts[i].y
        ax.text(x, y, str(i), c='c')
    for u, v in delaunay.edges:
        a, b = pts[u], pts[v]
        ax.plot([a.x, b.x], [a.y, b.y], color='k', zorder=-1)
    plt.show()


if __name__ == '__main__':
    test_delaunay()
