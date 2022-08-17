from point import *
from segment import Segment
from triangle import Triangle

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
