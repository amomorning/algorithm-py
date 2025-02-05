from point import *
from triangle import *

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


MAX_BLOCK_SIZE = 100
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
        return iter
    
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
        if i == len(self.blocks_): i -= 1
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


sweepx = 0.0
class Arc:
    def __init__(self, p, q, i, id=0):
        self.p = p
        self.q = q
        self.i = i
        self.id = id
    
    def __str__(self):
        return f'Arc({self.p}, {self.q}, {self.i}, {self.id})'
    
    def __repr__(self):
        return f'Arc({self.p}, {self.q}, {self.i}, {self.id})'
    
    def get_y(self, x):
        if self.q.y == INF: return INF
        x += EPS
        mid = (self.p + self.q) * 0.5
        dir = (self.p - mid).rotate_90()
        D = (x - self.p.x) * (x - self.q.x) 
        if cmp(dir.y) == 0: return INF/2
        return mid.y + ((mid.x - x) * dir.x + math.sqrt(D) * abs(dir) ) / dir.y
    
    def __eq__(self, o):
        global sweepx
        if type(o) is Arc:
            return cmp(self.get_y(sweepx) - o.get_y(sweepx)) == 0
        return cmp(self.get_y(sweepx) - o) == 0    

    def __lt__(self, o):
        global sweepx
        if type(o) is Arc:
            return cmp(self.get_y(sweepx) - o.get_y(sweepx)) < 0
        return cmp(self.get_y(sweepx) - o) < 0

    def __ge__(self, o):
        global sweepx
        if type(o) is Arc:
            return cmp(self.get_y(sweepx) - o.get_y(sweepx)) >= 0
        return cmp(self.get_y(sweepx) - o) >= 0 
    
import heapq, bisect


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
        random_angle = random.uniform(0, math.pi*2)
        tiny = 1e-6
        points = [Point(pt[0] + random.uniform(-tiny, tiny), pt[1]  + random.uniform(-tiny, tiny)).rotate(random_angle) for pt in points]
        self.points = sorted([(points[i], i) for i in range(self.n)])

        self.Q = []
        self.edges = [] # delaunay edges
        self.valid = [] # valid[-id] == True if the vertex event is valid
        self.beachline = SortedBlockList()
        
    
    def update(self, iter):
        global sweepx
        item = self.beachline.access(iter)
        if item.i == -1: return
        self.valid[-item.id] = False
        a = self.beachline.access(self.beachline.prev(iter))
        
        # print(self.beachline.blocks_)
        u, v = item.q - item.p, a.p - item.p
        # print(iter)
        # print(u.cross(v))
        if cmp(abs(u.cross(v))) == 0: return # collinear: doesn't generate a vertex event

        self.ti -= 1
        item.id = self.ti

        self.valid.append(True)
        if u.cross(v) > 0: tri = Triangle(item.p, item.q, a.p)
        else: tri = Triangle(item.p, a.p, item.q)
        c, r = tri.circumcircle()
        x = c.x + r
        if cmp(x - sweepx) >= 0 and cmp(a.get_y(x) - item.get_y(x)) >= 0:
            heapq.heappush(self.Q, (x, item.id, iter))

    def add_edge(self, i, j):
        if i == -1 or j == -1: return
        self.edges.append((self.points[i][1], self.points[j][1]))
    
    def add(self, i):
        p = self.points[i][0]
        # find arc to split
        c = self.beachline.lower_bound(p.y)
        c_obj = self.beachline.access(c)
        b = self.beachline.add(Arc(p, c_obj.p, i))
        a = self.beachline.add(Arc(c_obj.p, p, c_obj.i))
        self.add_edge(i, c_obj.i)

        self.update(a)
        self.update(b)
        self.update(c)
    
    def remove(self, iter):
        global sweepx
        a = self.beachline.prev(iter)
        b = self.beachline.next(iter)
        self.beachline.delete(iter)

        a_obj = self.beachline.access(a)
        b_obj = self.beachline.access(b)
        self.beachline.delete(a)
        a = self.beachline.add(Arc(a_obj.p, b_obj.p, a_obj.i, a_obj.id))
        self.add_edge(a_obj.i, b_obj.i)

        self.update(a)
        self.update(b)

    
    def build(self, X = 1e9):
        global sweepx
        X *= 3

        self.beachline.add(Arc(Point(-X, -X), Point(-X, X), -1))
        self.beachline.add(Arc(Point(-X, X), Point(INF, INF), -1))

        for i in range(self.n):
            heapq.heappush(self.Q, (self.points[i][0].x, i, self.beachline.end()))

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
    pts = set()
    for _ in range(1000):
        x = random.uniform(1, 100)
        y = random.uniform(1, 100)
        pts.add((x, y))
    # print(len(pts))
    # for x, y in pts:
    #     print(x, y)
    # pts = [(2, 4), (10, 4), (10, 10), (3, 3), (8, 2), (4, 1)]
    # pts = [(9, 10), (2, 1), (5, 8), (8, 10), (5, 7), (6, 3), (2, 6), (2, 5), (1, 3)]

    # print(list(pts))

    # n = int(input())
    # for i in range(n):
    #     x, y = map(float, input().split())
    #     pts.add((x, y))
    import timeit
    start = timeit.default_timer()
    pts = [Point(pt) for pt in pts]
    delaunay = DelaunayTrianglation(pts)
    delaunay.build()
    # print(delaunay.points)
    # elapsed time
    elapsed = (timeit.default_timer() - start)
    print(elapsed)

    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111)

    # print(delaunay.edges)
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
