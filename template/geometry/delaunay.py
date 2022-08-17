from point import *
from triangle import *

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
        # dir.y += EPS
        if cmp(dir.y) == 0: return math.nan
        return mid.y + ((mid.x - x) * dir.x + math.sqrt(D) * abs(dir)) / dir.y
    
    def __lt__(self, o):
        global sweepx
        if type(o) is Arc:
            return self.get_y(sweepx) < o.get_y(sweepx)
        return self.get_y(sweepx) < o
    
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
        random_angle = random.random() * math.pi / 233
        points = [Point(pt).rotate(random_angle) for pt in points]
        self.points = sorted([(points[i], i) for i in range(self.n)])

        self.Q = []
        self.edges = [] # delaunay edges
        self.valid = [] # valid[-id] == True if the vertex event is valid
        self.beachline = Multiset()
        
    
    def update(self, iter):
        global sweepx
        item = self.beachline.get(iter)
        if item.i == -1: return
        self.valid[-item.id] = False
        a = self.beachline.get(self.beachline.prev(iter))

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

    
    def build(self, X = 1e9):
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
