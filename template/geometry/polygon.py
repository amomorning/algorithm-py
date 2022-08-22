from point import *
from segment import Segment
from triangle import Triangle

import collections, math, bisect, heapq, random, functools, itertools, copy, typing
import platform; LOCAL = (platform.uname().node == 'AMO')


import sys; input = lambda: sys.stdin.readline().rstrip("\r\n")
inp = lambda : list(map(int, input().split()))

def debug(*args):
    if LOCAL:
        print('\033[92m', end='')
        printf(*args)
        print('\033[0m', end='')

def printf(*args):
    if LOCAL:
        print('>>>: ', end='')
    for arg in args:
        if isinstance(arg, typing.Iterable) and \
                not isinstance(arg, str) and \
                not isinstance(arg, dict):
            print(' '.join(map(str, arg)), end=' ')
        else:
            print(arg, end=' ')
    print()

    

class Polygon:
    """ 2D Polygon Implementation
    """
    def __init__(self, *args) -> None:
        if len(args) == 1:
            args = args[0]
        self.points = [Point(pt[0], pt[1]) for pt in args]
        self.__convex = None
        self.__area = None

    def __getitem__(self, key):
        return self.points[key]

    def __setitem__(self, key, value):
        self.points[key] = Point(value)
    
    def __str__(self):
        return 'Polygon[%s]' % ', '.join(map(str, self.points))

    def __len__(self):
        return len(self.points)
    
    def __iter__(self):
        return iter(self.points)
    
    @property
    def is_convex(self):
        if self.__convex is not None: 
            return self.__convex
        
        self.__convex = True
        for p0, p1, p2 in zip(self.points, self.points[1:], self.points[2:]):
            if (p1 - p0).cross(p2 - p0) < 0:
                self.__convex = False
        return self.__convex
    
    @property
    def segments(self):
        segs = [Segment(p0, p1) for p0, p1 in zip(self.points, self.points[1:])]
        segs.append(Segment(self.points[-1], self.points[0]))
        return segs
    
    @property
    def triangles(self):
        tris = []
        if self.is_convex:
            p0 = self.points[0]
            for p1, p2 in zip(self.points[1:], self.points[2:]):
                tris.append(Triangle(p0, p1, p2))
        else:     
            trids = self.earcut()
            for a, b, c in trids:
                tris.append(Triangle(self.points[a], self.points[b], self.points[c]))
        return tris
    
    def signed_area(self, doubled = True):
        self.A = 0
        p0 = self.points[0]
        for p1, p2 in zip(self.points[1:], self.points[2:]):
            self.A += (p1 - p0).cross(p2 - p0)
        if not doubled: A /= 2
        return self.A

    @property
    def length(self):
        return sum([seg.length for seg in self.segments])
    
    def area(self, doubled = False):
        self.__area = 0
        for tri in self.triangles:
            self.__area += tri.area(True)
        if not doubled: self.__area /= 2
        return self.__area
    
    def centroid(self):
        self.__center = Point(0.0, 0.0)
        for tri in self.triangles:
            self.__center += tri.area() * tri.centroid
        return self.__center / self.area() 

    def earcut(self):
        """ Reference
            [1] https://www.geometrictools.com/Documentation/TriangulationByEarClipping.pdf
        """
        n, p = len(self.points), self.points
        prev = [n-1] + list(range(n-1))
        next = list(range(1, n)) + [0]
        convex, refvex = [], set()
        for i in range(n):
            if (p[prev[i]] - p[i]).cross(p[next[i]] - p[i]) < 0:
                convex.append(i)
            elif (p[prev[i]] - p[i]).cross(p[next[i]] - p[i]) > 0:
                refvex.add(i)
        vis, res = [0] * n, []
        xs = sorted([(p[i].x, i) for i in range(n)])
        ys = sorted([(p[i].y, i) for i in range(n)])
        while convex:
            m = convex.pop()
            if vis[m] == 1 or n - len(res) < 3:
                continue
            l, r = prev[m], next[m]
            
            tri = Triangle(p[l], p[m], p[r])
            ids = find_points_in_aabb(xs, ys, tri.aabb, False) & refvex
            is_ear = True
            for i in ids:
                if i == l or i == r: continue
                is_ear &= (not tri.inside_point(p[i]))
                if not is_ear: break
            # debug(l, m, r, is_ear)
            if is_ear:
                res.append((l, m, r))
                vis[m] = 1
                next[l] = r
                prev[r] = l
                for i in [l, r]:
                    if (p[prev[i]] - p[i]).cross(p[next[i]] - p[i]) <= 0:
                        convex.append(i)
                        refvex.discard(i)
        return res

    def inside_point(self, p, boundary=True):
        t = 0
        for seg in self.segments:
            if seg.on_point(p):
                return boundary 
            a, b = seg
            if cmp(a.y - b.y) > 0: a, b = b, a
            if cmp((a - p).cross(b - p)) < 0 and cmp(a.y - p.y) < 0 and cmp(p.y - b.y) <= 0:
                t += 1
        return bool(t & 1)

    def divide_by_distance(self, distance):
        remain = 0
        pts = []
        for seg in self.segments:
            remain += seg.length
            while cmp(remain - distance) >= 0:
                remain -= distance
                t = (seg.length - remain) / seg.length
                pts.append(seg.lerp(t))
        return pts
    
    def divide_by_ray(self, n, center=None):
        if center is None: center = self.centroid()
        radius = 0
        pts = []
        for p in self.points:
            radius = max(radius, (p-center).norm())
        for i in range(n):
            angle = 2 * i * math.pi / n
            x, y = radius * math.cos(angle), radius * math.sin(angle)
            ray = Segment(center, center+Point(x, y))
            mn = math.inf
            for seg in self.segments:
                p = seg.intersection(ray)
                if p is None: continue
                if (p - center).norm() < mn:
                    mn = (p - center).norm()
                    mnp = p
            pts.append(mnp)
        return pts

    

def test_polygon_centroid():
    # pts = [(2, 0), (1, 2), (3, 2), (3, 0), (5, 2), (5, 0), (6, 4), (4, 2), (1, 4), (0, 1)]
    # pts = [(0, 0), (5, 0), (5, 8), (4, 8), (4, 5), (0, 5)]
    pts = [(0, 0), (1, 0), (1, 2), (0, 1)]
    ply = Polygon(pts)

    printf(ply.area())

    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1)

    for seg in ply.segments:
        a, b = seg.a, seg.b
        ax.plot([a.x, b.x], [a.y, b.y], c='k')

    tri_pt = [tri.centroid for tri in ply.triangles]
    ax.scatter([p[0] for p in tri_pt],[p[1] for p in tri_pt], c='b')

    center = sum(ply.points, Point(0, 0))/len(ply.points)
    ax.scatter(center[0], center[1], c='r')
    ax.text(center[0], center[1], 'average', c='r')

    b = ply.centroid()
    ax.scatter(b[0], b[1], c='y')
    ax.text(b[0], b[1],'centroid', c='y')

    plt.show()

def test_polygon_divide():
    pts = [(0, 0), (1, 0), (1, 2), (0, 1)]
    ply = Polygon(pts)

    print(ply.length)
    N = 20
    # divs = ply.divide_by_distance(ply.length/N)
    divs = ply.divide_by_ray(N)
    
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111)

    c = ply.centroid()
    r = 0
    for p in ply.points:
        r = max(r, (p-c).norm())
    for i in range(N):
        angle = 2*i*math.pi/N
        x, y = r*math.cos(angle), r*math.sin(angle)
        ax.plot([c.x, c.x+x], [c.y, c.y+y], c='r')



    for seg in ply.segments:
        a, b = seg.a, seg.b
        ax.plot([a.x, b.x], [a.y, b.y], c='k')    
    
    for i in range(len(divs)):
        x, y = divs[i]
        ax.text(x, y, str(i), c='k')
        
    ax.scatter([p.x for p in divs], [p.y for p in divs], c='b', zorder=10)
    plt.show()

if __name__ == '__main__':
    # test_polygon_centroid()
    test_polygon_divide()
