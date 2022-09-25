from point import *
from triangle import *


class Iterator:
    def __init__(self, label):
        self.label = label

    def __lt__(self, other) -> bool:
        return self.label < other.label

    def __eq__(self, other) -> bool:
        return self.label == other.label

    def __repr__(self):
        return f'Iterator({self.label})'


class Multiset:
    def __init__(self):
        self.v = []
        self.it = 0

    def update(self, iter, new_item):
        """ o(N) """
        self.remove(iter)
        return self.insert(new_item)

    def get(self, iter):
        idx = self.find(iter)
        return self.v[idx][0]

    def find(self, iter):
        """ o(N) """
        for i, item in enumerate(self.v):
            if item[1] == iter:
                return i
        return -1

    def remove(self, iter):
        """ o(N) """
        idx = self.find(iter)
        del self.v[idx]

    def insert(self, item):
        """ o(N) """
        iter = Iterator(self.it)
        self.it += 1
        bisect.insort_left(self.v, (item, iter))
        return iter

    def next(self, iter):
        """ o(logN): return iterator"""
        idx = self.find(iter)
        if idx == len(self.v): return self.v[idx][1]
        return self.v[idx + 1][1]

    def prev(self, iter):
        """ o(logN) """
        idx = self.find(iter)
        if idx == 0: return self.v[idx][1]
        return self.v[idx - 1][1]

    def lower_bound(self, item):
        """ o(logN) """
        idx = bisect.bisect_left(self.v, (item, -math.inf))
        return self.v[idx][1]

    def end(self):
        """ o(1) """
        return self.v[-1][1]


def lineline(a, b, c, d):
    return a + (b - a) * ((c - a).cross(d - c) / (b - a).cross(d - c))


def circumcenter(a, b, c):
    b = (a + b) * 0.5
    c = (a + c) * 0.5
    return lineline(b, b + (b - a).rotate_90(), c, c + (c - a).rotate_90())


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
        if cmp(dir.y) == 0: return INF / 2
        return mid.y + ((mid.x - x) * dir.x + math.sqrt(D) * abs(dir)) / dir.y

    def __lt__(self, o):
        global sweepx
        if type(o) is Arc:
            return cmp(self.get_y(sweepx) - o.get_y(sweepx)) < 0
        return cmp(self.get_y(sweepx) - o) < 0


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
        random_angle = random.uniform(0, math.pi * 2)
        tiny = 1e-6
        points = [Point(pt[0] + random.uniform(-tiny, tiny), pt[1] + random.uniform(-tiny, tiny)).rotate(random_angle)
                  for pt in points]
        self.points = sorted([(points[i], i) for i in range(self.n)])

        self.Q = []
        self.edges = []  # delaunay edges
        self.valid = []  # valid[-id] == True if the vertex event is valid
        self.beachline = Multiset()

    def update(self, iter):
        global sweepx
        item = self.beachline.get(iter)
        if item.i == -1: return
        self.valid[-item.id] = False
        a = self.beachline.get(self.beachline.prev(iter))

        u, v = item.q - item.p, a.p - item.p
        # print(iter)
        # print(u.cross(v))
        if cmp(abs(u.cross(v))) == 0: return  # collinear: doesn't generate a vertex event

        self.ti -= 1
        item.id = self.ti

        self.valid.append(True)
        if u.cross(v) > 0:
            tri = Triangle(item.p, item.q, a.p)
        else:
            tri = Triangle(item.p, a.p, item.q)
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
        c_obj = self.beachline.get(c)
        b = self.beachline.insert(Arc(p, c_obj.p, i))
        a = self.beachline.insert(Arc(c_obj.p, p, c_obj.i))
        self.add_edge(i, c_obj.i)

        self.update(a)
        self.update(b)
        self.update(c)

    def remove(self, iter):
        global sweepx
        a = self.beachline.prev(iter)
        b = self.beachline.next(iter)
        self.beachline.remove(iter)

        a_obj = self.beachline.get(a)
        b_obj = self.beachline.get(b)
        a = self.beachline.update(a, Arc(a_obj.p, b_obj.p, a_obj.i, a_obj.id))
        self.add_edge(a_obj.i, b_obj.i)

        self.update(a)
        self.update(b)

    def build(self, X=1e9):
        global sweepx
        X *= 3

        self.beachline.insert(Arc(Point(-X, -X), Point(-X, X), -1))
        self.beachline.insert(Arc(Point(-X, X), Point(INF, INF), -1))

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
    for _ in range(200):
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

    # do something
    pts = [Point(pt) for pt in pts]
    delaunay = DelaunayTrianglation(pts)
    delaunay.build()
    # print(delaunay.points)
    # elapsed time

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
    plt.savefig('imgs/delaunay_fortune_2.png')
    # plt.show()


if __name__ == '__main__':
    test_delaunay()
