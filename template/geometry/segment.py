from point import *
from plane import Plane

class Segment:
    def __init__(self, a, b):
        self.a = Point(a)
        self.b = Point(b)

    def __getitem__(self, item):
        if item == 0: return self.a
        if item == 1: return self.b
        raise KeyError('Invalid item: %s' % item)

    def __str__(self) -> str:
        return 'Line: [' + str(self.a) + ', ' + str(self.b) + ']'

    @property
    def length(self):
        return abs(self.a - self.b)

    def on_point(self, point):
        if type(point) != Point: point = Point(point)
        u, v = self.a-point, self.b-point
        return abs(u.cross(v)) == 0 and u.dot(v) <= 0
    
    def lerp(self, t):
        return (1 - t) * self.a + t * self.b

    def project_on(self, dim):        
        return Segment(self.a.select(dim), self.b.select(dim))

    def is_proper_intersect(self, line):
        assert len(self.a) == 2
        c1 = (self.b - self.a).cross(line.a - self.a)
        c2 = (self.b - self.a).cross(line.b - self.a)
        c3 = (line.b - line.a).cross(self.a - line.a)
        c4 = (line.b - line.a).cross(self.b - self.a)
        return c1 * c2  < 0 and c3 * c4 < 0

    def is_intersect(self, line):
        if self.is_proper_intersect(line):
            return True
        return self.on_point(line.a) or self.on_point(line.b) or\
            line.on_point(self.a) or line.on_point(self.b)
    
    def intersection(self, line):
        if len(line.a) == 3:
            return self.intersection_3d(line)

        if not self.is_intersect(line):
            return None
        u, v, w = line.a - self.a, self.b - self.a, line.b - line.a
        if cmp(v.cross(w)) == 0:
            if line.on_point(self.a):
                return self.a
            if line.on_point(self.b):
                return self.b
            return None
        t = w.cross(u) / w.cross(v)
        # debug(t)
        return self.lerp(t)
    
    def intersection_3d(self, line):
        assert len(self.a) == 3

        x_p = self.project_on((1, 2)).intersection(line.project_on((1, 2)))
        y_p = self.project_on((0, 2)).intersection(line.project_on((0, 2)))
        z_p = self.project_on((0, 1)).intersection(line.project_on((0, 1)))

        if x_p is None or y_p is None or z_p is None:
            return None

        for x in [y_p.x, z_p.x]:
            for y in [x_p.x, z_p.y]:
                for z in [x_p.y, y_p.y]:
                    pt = Point(x, y, z)
                    if self.on_point(pt) and line.on_point(pt):
                        return pt
        return None

    
    def project_point(self, point):
        u, v = point - self.a, self.b - self.a
        return self.a + u.proj(v)
    
    def distance(self, rhs):
        if type(rhs) == Point:
            u, v, w = self.b - self.a, rhs - self.a, rhs - self.b
            if cmp(u.dot(v)) < 0: return abs(v)
            elif cmp(u.dot(w)) > 0: return abs(w)
            else: return abs(u.cross(v)) / abs(u)
        
        if type(rhs) == Segment:
            if self.intersection(rhs) != None:
                return 0
            ret = min(self.distance(rhs.a), self.distance(rhs.b))
            ret = min(ret, min(rhs.distance(self.a), rhs.distance(self.b)))

            if len(self.a) == 3:
                """ Reference
                    for line line distance
                    [1] https://mathworld.wolfram.com/Line-LineDistance.html
                
                    # a, b, c = self.b - self.a, rhs.b - rhs.a, rhs.a - self.a
                    # return abs(a.cross(b).dot(c)) / abs(a.cross(b))

                    but here we should calculate the distance between two segments
                    [2] https://zalo.github.io/blog/closest-point-between-segments/
                """
                p = Plane(self.a, self.b-self.a)
                line = p.project_segment(rhs)
                closest = line.project_point(self.a)                
                if line.on_point(closest):
                    ret = min(ret, line.distance(self.a))

            return ret
            
        raise NotImplementedError("distance is not implemented for type %s" % type(rhs))
