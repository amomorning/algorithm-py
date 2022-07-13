import collections, math, bisect, heapq, random, functools, itertools, copy, typing
import platform; LOCAL = (platform.uname().node == 'AMO')

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

def check(op, lhs, rhs=None):
    if not op(lhs, rhs):
        debug('Error: ', lhs, 'not', op.__name__, rhs)
    else:
        printf(lhs, op.__name__, rhs)


import math, operator
EPS = 1e-6
def cmp(x): return -1 if x < -EPS else int(x > EPS)

def polar_cmp(a, b):
    if cmp(a.y) * cmp(b.y) <= 0:
        if cmp(a.y) > 0 or cmp(b.y) > 0: return cmp(a.y - b.y)
        if cmp(a.y) == 0 and cmp(b.y) == 0: return cmp(a.x - b.x)
    return cmp(a.cross(b)) 

def find_points_in_aabb(xs, ys, aabb, boundary=True):
    """ pts: Sorted Points in [(x, y, id), ...]
        aabb: [[minx, miny], [maxx, maxy]]
        Returns: index list
    """
    if boundary:
        xl = bisect.bisect_right(xs, (aabb[0][0]-EPS, -1))
        xr = bisect.bisect_left(xs, (aabb[1][0]+EPS, -1))
        # print(xs)
        # print(xs[xl: xr])

        yl = bisect.bisect_right(ys, (aabb[0][1]-EPS, -1))
        yr = bisect.bisect_left(ys, (aabb[1][1]+EPS, -1))
    
        # print(ys)
        # print(ys[yl: yr])
    else:
        xl = bisect.bisect_left(xs, (aabb[0][0]+EPS, -1))
        xr = bisect.bisect_right(xs, (aabb[1][0]-EPS, -1))

        yl = bisect.bisect_left(ys, (aabb[0][1]+EPS, -1))
        yr = bisect.bisect_right(ys, (aabb[1][1]-EPS, -1))
    idx = set([x[1] for x in xs[xl:xr]])
    idy = set([y[1] for y in ys[yl:yr]])
    return idx & idy

    # (x0, y0), (x1, y1) = aabb
    # l = bisect.bisect_left(pts, (x0, -math.inf, -math.inf))
    # r = bisect.bisect_right(pts, (x1, math.inf, math.inf))
    

    pass

class Point:
    def __init__(self, *args):
        if len(args) == 1:
            args = args[0]
        self.__v = list(args)
        
    def __len__(self):
        return len(self.__v)

    def __str__(self):
        return 'Point' + str(tuple(self.__v))
    
    def print(self):
        return ' '.join(map(str, self.__v))
    
    def __hash__(self):
        return hash(tuple(self.__v))
        
    def __getitem__(self, key):
        if type(key) is int or slice:
            return self.__v[key]

    def __getattr__(self, key):
        if key == 'x':
            return self.__v[0]
        if key == 'y':
            return self.__v[1]
        if key == 'z':
            return self.__v[2]
        if key == 'w':
            return self.__v[3]
        raise KeyError('Invalid key: %s' % key)
    
    def __setitem__(self, key, value):
        if type(key) is int and key < len(self.__v):
            self.__v[key] = value
        if key == 'x':
            self.__v[0] = value
        if key == 'y':
            self.__v[1] = value
        if key == 'z':
            self.__v[2] = value
        if key == 'w':
            self.__v[3] = value        
        raise KeyError('Invalid key: %s' % key)
        
    def __neg__(self):
        ret = []
        for x in self:
            ret.append(-x)
        return Point(ret)
    
    def __eq__(self, rhs):
        if type(rhs) != Point: rhs = Point(rhs)
        assert len(rhs) == len(self)

        for i in range(len(self)):
            if cmp(self[i] - rhs[i]) != 0:
                return False
        return True
        
    def __le__(self, rhs):
        if type(rhs) != Point: rhs = Point(rhs)
        assert len(rhs) == len(self)

        for i in range(len(self)):
            if cmp(self[i] - rhs[i]) < 0:
                return True
            if cmp(self[i] - rhs[i]) > 0:
                return False
        return True
        
    def __lt__(self, rhs):
        if type(rhs) != Point: rhs = Point(rhs)
        assert len(rhs) == len(self)

        for i in range(len(self)):
            if cmp(self[i] - rhs[i]) < 0:
                return True
            if cmp(self[i] - rhs[i]) > 0:
                return False
        return False
    
    def __add__(self, rhs):
        if type(rhs) != Point: rhs = Point(rhs)
        ret = []        
        for i in range(len(self)):
            ret.append(self[i] + rhs[i])
        return Point(ret)

    def __sub__(self, rhs):
        return self + (-rhs)
    
    def __mul__(self, scale):
        ret = []
        for x in self:
            ret.append(x * scale)
        return Point(ret)

    def __rmul__(self, scale):
        return self * scale
    
    def __truediv__(self, scale):
        return self * (1.0/scale)
    
    def __floordiv__(self, scale):
        ret = []
        for x in self:
            ret.append(x // scale)
        return Point(ret)
    
    def __matmul__(self, rhs):
        if type(rhs) != Point: rhs = Point(rhs)
        ret = []
        for i in range(len(rhs)):
            ret.append(self[i] * rhs[i])
        return Point(ret)
    
    def __pow__(self, scale):
        tot = 0
        for x in self:
            tot += x ** scale
        return tot
    
    def __abs__(self):
        return (self ** 2) ** 0.5
    
    @property
    def polar(self):
        assert len(self) == 2
        return self.norm(), 

    
    def norm(self, v = 2, maxd = 50):
        return (self ** v) ** (1.0/v) if v <= maxd else max(self)
    
    def normalized(self):
        return self / self.norm() 
    
    def dot(self, rhs):
        if type(rhs) != Point: rhs = Point(rhs)
        return sum(self @ rhs)
    
    def cross(self, rhs):
        if type(rhs) != Point: rhs = Point(rhs)
        if len(self.__v) == 3:
            a, b, c = self
            x, y, z = rhs
            return Point(-c*y + b*z, c*x - a*z, -b*x + a*y)
        elif len(self.__v) == 2:
            return self.x * rhs.y - self.y * rhs.x
        raise ValueError("Invalid coordinates")

        
    def proj(self, rhs):
        if type(rhs) != Point: rhs = Point(rhs)
        return rhs * self.dot(rhs) / rhs.dot(rhs)
    
    def select(self, dim):
        assert len(dim) > 1
        return Point([self[d] for d in dim])
    
    # Quaternion
    def conj(self):
        ret = [self[0]]
        for i in range(1, len(self)):
            ret.append(-self[i])
        return Point(ret)
    
    def inv(self):
        l2 = self.dot(self)
        return self.conj() / l2

    def mulq(self, rhs):
        assert len(self.__v)  == 4
        if type(rhs) != Point: rhs = Point(rhs)

        q0, q1, q2, q3 = self
        p0, p1, p2, p3 = rhs

        return Point(q0*p0 - q1*p1 - q2*p2 - q3*p3, \
                     q0*p1 + q1*p0 + q2*p3 - q3*p2, \
                     q0*p2 - q1*p3 + q2*p0 + q3*p1, \
                     q0*p3 + q1*p2 - q2*p1 + q3*p0)

    # rotate
    def rotate(self, angle):
        assert len(self.__v) == 2
        c, s = math.cos(angle), math.sin(angle)
        return Point(self.x * c - self.y * s, self.x * s + self.y * c)
        
    def rotate_90(self):
        assert len(self.__v) == 2
        return Point(-self.y, self.x)
    
    def rotate_x(self, angle):
        assert len(self.__v)  == 3
        c, s = math.cos(angle), math.sin(angle)
        x, y, z = self
        return Point(x, y * c - z * s, y * s + z * c)
    
    def rotate_y(self, angle):
        assert len(self.__v)  == 3
        c, s = math.cos(angle), math.sin(angle)
        x, y, z = self
        return Point(x * c + z * s, y, -x * s + z * c)

    def rotate_z(self, angle):
        assert len(self.__v)  == 3
        c, s = math.cos(angle), math.sin(angle)
        x, y, z = self
        return Point(x * c - y * s, x * s + y * c, z)
    
    def rotate_by(self, axis, angle):
        assert len(self.__v)  == 3
        if type(axis) != Point: axis = Point(axis)
        
        c, s = math.cos(angle), math.sin(angle)
        x, y, z = self
        ux, uy, uz = axis.normalized()

        return Point((c+ux*ux*(1-c))*x + (ux*uy*(1-c)-uz*s)*y + (ux*uz*(1-c)+uy*s)*z, \
                     (uy*ux*(1-c)+uz*s)*x + (c+uy*uy*(1-c))*y + (uy*uz*(1-c)-ux*s)*z, \
                     (uz*ux*(1-c)-uy*s)*x + (uz*uy*(1-c)+ux*s)*y + (c+uz*uz*(1-c))*z)

    def rotate_by_quaternion(self, axis, angle): 
        assert len(self.__v) == 3
        if type(axis) != Point: axis = Point(axis)
        axis = axis.normalized() * math.sin(angle*0.5)
        q = Point(math.cos(angle*0.5), axis.x, axis.y, axis.z)
        return self.apply_quaternion(q)

    def apply_quaternion(self, q):
        p = Point(1.0, self.x, self.y, self.z)
        return Point(q.mulq(p).mulq(q.inv())[1:])

    def apply_matrix(self, m):
        """ row major matrix 
        """
        n = len(self)

        ret = []
        for i in range(n):
            tot = 0
            for j in range(n):
                tot += self[j] * m[i][j]
            ret.append(tot)

        return Point(ret)


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


class Plane:
    def __init__(self, base, normal):
        self.base = base
        self.normal = normal
        self.normal.normalized()
    
    def project_point(self, point):
        vector = point - self.base
        return vector - vector.proj(self.normal)
    
    def project_segment(self, segment):
        a = self.project_point(segment.a)
        b = self.project_point(segment.b)
        return Segment(a, b)
    
    def to_plane(self, plane):
        move = self.base - plane.base
        # rotate = 

class Matrix:
    def __init__(self, size=4):
        self.size = 4
        self.m = [[0] * size for _ in range(size)]
        for i in range(size):
            self.m[i][i] = 1
    
    def from_translate(self, translate):
        translate = Point(translate)
        for i in range(self.size-1):
            self.m[i][-1] = translate[i]
    
    def from_rotate_axis(self, axis, angle):
        pass

class Triangle:
    def __init__(self, a, b, c):
        self.a = Point(a)
        self.b = Point(b)
        self.c = Point(c)
    
    def __getitem__(self, key):
        if key == 0:
            return self.a
        if key == 1:
            return self.b
        if key == 2:
            return self.c
        raise KeyError('Invalid item: %s' % key)
    
    def __str__(self) -> str:
        return 'Triangle: [' + str(self.a) + ', ' + str(self.b) + ', ' + str(self.c) + ']'

    @property
    def normal(self):
        assert len(self.a) == 3
        b, c = self.b - self.a, self.c - self.a
        return b.cross(c).normalized()

    @property
    def aabb(self):
        d = len(self.a)
        mn = [math.inf] * d
        mx = [-math.inf] * d
        for i in range(3):
            for j in range(d):
                mn[j] = min(mn[j], self[i][j])
                mx[j] = max(mx[j], self[i][j])
        return mn, mx

    def inside_point(self, p):
        assert len(p) == len(self.a)
        if len(p) == 2:
            p, b, c = p - self.a, self.b - self.a, self.c - self.a
            if b.cross(c) < 0:
                b, c = c, b
            if b.cross(p) < 0 or p.cross(c) < 0 or (c-b).cross(p-b) < 0:
                return False
            return True
        if len(p) == 3:
            p, b, c = p - self.a, self.b - self.a, self.c - self.a
            def is_zero(v):
                if cmp(abs(v)) == 0: return True
                if cmp(abs(v.normalized()-self.normal)) == 0: return True
                return False            

            if is_zero(b.cross(p)) and is_zero(p.cross(c)) and is_zero((c-b).cross(p-b)):
                return True
            return False
        raise NotImplementedError("Higher dimensions are not supported")
            

    def uniform_sample(self, num):
        """ Reference: 
            [1] https://math.stackexchange.com/questions/18686/uniform-random-point-in-triangle-in-3d
        """
        ret = []
        for i in range(num):
            r1 = random.uniform(0, 1)
            r2 = random.uniform(0, 1)
            p = self.a * (1-math.sqrt(r1)) + self.b * math.sqrt(r1)*(1-r2)\
                + self.c * math.sqrt(r1)*r2
            ret.append(p)
            
        return ret
    
    def uniform_sample_parallelogram(self, num):
        b, c = self.b - self.a, self.c - self.a
        ret = []
        for _ in range(num):
            p = b * random.uniform(0, 1) + c * random.uniform(0, 1)

            if not self.inside_point(p+self.a):
                p = b + c - p
            ret.append(p+self.a)
        return ret
    
    def uniform_sample_rectangle(self, num):
        mn, mx = self.aabb
        ret = []
        for _ in range(num):
            x = random.uniform(mn[0], mx[0])
            y = random.uniform(mn[1], mx[1])
            while not self.inside_point(Point(x, y)):
                x = random.uniform(mn[0], mx[0])
                y = random.uniform(mn[1], mx[1])
            ret.append(Point(x, y))
        return ret
    

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
        # TODO: triangulate
        tris = []
        if self.is_convex:
            p0 = self.points[0]
            for p1, p2 in zip(self.points, self.points[1:]):
                tris.append(Triangle(p0, p1, p2))
        else:     
            # earcut
            trids = self.earcut()
            for a, b, c in trids:
                tris.append(Triangle(self.points[a], self.points[b], self.points[c]))
        return tris

    @property
    def area(self, doubled = True):
        self.A = 0
        for tri in self.triangles:
            self.A += tri.area
        if not doubled: self.A /= 2
        return self.A
    
    
    def earcut_benchmark(self):
        n, p = len(self.points), self.points
        prev = [n-1] + list(range(n-1))
        next = list(range(1, n)) + [0]
        convex, refvex = collections.deque(), set()
        for i in range(n):
            if (p[prev[i]] - p[i]).cross(p[next[i]] - p[i]) <= 0:
                convex.append(i)
            else:
                refvex.add(i)
        vis, res = [0] * n, []
        while convex:
            m = convex.popleft()
            if vis[m] == 1 or n - len(res) < 3:
                continue
            l, r = prev[m], next[m]
            
            tri = Triangle(p[l], p[m], p[r])
            is_ear = True
            for i in refvex:
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

    def earcut(self):
        n, p = len(self.points), self.points
        cur = range(n)
        remain = [0]
        tris = []

        xs = sorted([(p[i].x, i) for i in range(n)])
        ys = sorted([(p[i].y, i) for i in range(n)])
        while len(cur) > 3:
            for c in range(1, len(cur)):
                l = remain[-1]
                m = cur[c]
                r = remain[0] if c == len(cur) - 1 else cur[c+1]

                if (p[r] - p[m]).cross(p[l] - p[m]) > 0:
                    tri = Triangle(p[l], p[m], p[r]) 
                    is_ear = True
                    ids = find_points_in_aabb(xs, ys, tri.aabb, False)
                    for i in ids:
                        if i == l or i == m or i == r: continue
                        if tri.inside_point(p[i]):
                            is_ear = False

                    if is_ear == True:
                        tris.append((l, m, r))
                        continue
                remain.append(m)
            cur = remain
            remain = [cur[0]]
        if len(cur) == 3: tris.append(cur)
        return tris
                    

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

class ConvexHull:
    def __init__(self, points):
        self.points = list(map(Point, points))
        self.build()

    def add_point(self, point):
        self.points.append(point)
        self.build()
    
    def build(self):
        pts = sorted(self.points)
        n, k = len(pts), 0
        convex = [None] * (n*2)
        for p in pts:
            while k > 1 and cmp((convex[k-1] - p).cross(convex[k-2] - p)) <= 0:
                k -= 1
            convex[k] = p
            k += 1
        t = k
        for p in pts[-2::-1]:
            while k > t and cmp((convex[k-1] - p).cross(convex[k-2] - p)) <= 0:
                k -= 1
            convex[k] = p
            k += 1
        
        self.points = convex[:min(n,k-1)]
        self.polygon = Polygon(self.points)



def main():
    # test_points()
    # test_segments()
    test_polygon()
    # test_earcut()
    # test_convex()
    # test_inside_aabb()

    # pts = gen_polygon(1000)
    # print(len(pts))
    # for x, y in pts:
    #     print(x, y)

def test_points():
    check(operator.lt, Point(1, 2), Point(1, 2))
    check(operator.le, Point(1, 2), Point(1, 2))
    
    # 按 y 排序
    a = [Point(3, 4), Point(1, 2), Point(3, 5), Point(2,7)]
    a = sorted(a, key=lambda p: p[1])
    debug('Sorted by Y:', a)

    a = sorted(a, key=functools.cmp_to_key(polar_cmp), reverse=True)
    debug('sorted by Polar:', a)

    check(operator.eq, sum(a, start=Point(0, 0)), Point(9, 18))
    

    a = Point(1, 2)
    b = Point(0, 4)

    check(operator.eq, a.proj(b), Point(0, 2))
    debug(a.rotate(0.1))

    a = Point(1, 2, 3)
    check(operator.eq, a.rotate_by_quaternion((1, 1, 1), 0.5), a.rotate_by((1, 1, 1), 0.5))

    a = Point(1, 2, 3, 1)
    check(operator.eq, Point(2, 3, 4, 1), a.apply_matrix([[1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 1], [0, 0, 0, 1]]))

    # a = Point(1)
def test_segments():
    # print(a.rotate(math.pi/3))
    l = Segment(Point(0, 0), Point(3, 3))
    check(operator.eq, l.lerp(0.3), Point(0.9, 0.9))
    check(operator.eq, l.intersection(Segment(Point(1, 0), Point(0, 1))), Point(0.5, 0.5))
    # (3, 8)

    check(operator.eq, Point(1, 2, 3).select((0, 2)), Point(1, 3))

    l = Segment(Point(0, 0, 0), Point(2, 4, 6))
    r = Segment(Point(5, 0, 0), Point(-3, 4, 6))
    r_ = Segment(Point(5, 0, 0), Point(2, 4, 6))
    check(operator.eq, l.intersection_3d(r), Point(1, 2, 3))
    # >>>: Point(1.0, 2.0, 3.0) eq Point(1, 2, 3)
    check(operator.eq, l.intersection_3d(r_), Point(2, 4, 6))
    # >>>: None eq None

    l = Segment(Point(0, 0, 0), Point(3, 3, 0))
    check(operator.eq, l.distance(Point(1, 0, 0)), math.sqrt(2) * 0.5)

    check(operator.eq, l.project_point(Point(-1, 0, 0)), Point(-0.5, -0.5, 0))

    p = Plane(Point(0, 0, 0), Point(0, 1, 0))
    debug(p.project_segment(Segment(Point(2, 1, 0), Point(4, 0, 5))))

    check(operator.eq, l.distance(r), 5.0/math.sqrt(6))

def test_inside_aabb():
    n = 1000
    pts = [Point(random.randint(0, 100), random.randint(0, 100)) for _ in range(n)]
    print(' '.join(map(str, pts)))
    xs = sorted([(pts[i].x, i) for i in range(n)])
    ys = sorted([(pts[i].y, i) for i in range(n)])
    res = find_points_in_aabb(xs, ys, [[20, 20], [40, 60]], False)
    print(res)

    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1)
    inside = [[], []]
    outside = [[], []]
    for i in range(n):
        if i in res:
            inside[0].append(pts[i].x)
            inside[1].append(pts[i].y)
        else:
            outside[0].append(pts[i].x)
            outside[1].append(pts[i].y)
    ax.scatter(inside[0], inside[1], c='r')
    ax.scatter(outside[0], outside[1], c='k')
    plt.show()


def gen_polygon(n):
    cur = 0
    res = []
    for _ in range(n-1):
        len = random.random()
        angle = min(random.random()*math.pi*3/n, random.random() * (math.pi * 2 - cur))
        angle += math.pi / 10 / n
        cur += angle
        res.append((len * math.cos(cur), len * math.sin(cur)))
    
    len = random.random()
    angle = math.pi * 2
    res.append((len * math.cos(angle), len * math.sin(angle)))

    return res

def test_earcut():
    n = int(input())
    pts = []
    for i in range(n):
        x, y = map(float, input().split())
        pts.append((x, y))
    ply = Polygon(*pts)
    print(ply.earcut())

    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1)

    for i, p in enumerate(ply.points):
        ax.text(p.x, p.y, str(i), c='r')
    
    for tri in ply.triangles:
        a, b, c = tri.a, tri.b, tri.c
        ax.plot([a.x, b.x, c.x, a.x], [a.y, b.y, c.y, a.y], c='b')
    # for seg in ply.segments:
    #     a, b = seg.a, seg.b
    #     ax.plot([a.x, b.x], [a.y, b.y], c='k')
    debug(', '.join(map(str, ply.points)))  
    plt.show()

def test_polygon():


    tri = Triangle((10, 10), (7,3), (3, 7))
    check(operator.eq, tri.inside_point(Point(0, 0)), False)

    tri3d = Triangle((10, 10, 0), (7,3, 0), (3, 7,0))
    check(operator.eq, tri3d.inside_point(Point(5, 5, 0)), True)


    ply = Polygon((0, 0), (1, 0), (2, 0), (2, 1), (0, 1))

    debug(ply)
    debug(isinstance(ply, Polygon))
    debug(ply.is_convex)
    debug(ply.is_convex)

    print(ply.earcut_benchmark())
    ply = Polygon((1, 0), (6, 1), (4, 3), (3, 2), (2, 4), (0, 5))
    print(ply.earcut_benchmark())

    import random, timeit
         
    ply = Polygon((2, 0), (1, 2), (3, 2), (3, 0), (5, 2), (5, 0), (6, 4), (4, 2), (1, 4), (0, 1))
    
    ply = Polygon(*gen_polygon(1000))



    start = timeit.default_timer()
    # do something
    
    print(len(ply.earcut_benchmark()))
        
    # elapsed time
    elapsed = (timeit.default_timer() - start)
    print(elapsed)
    
    start = timeit.default_timer()
    # do something
    
    print(len(ply.earcut()))
    
    # elapsed time
    elapsed = (timeit.default_timer() - start)
    print(elapsed)

    # print(ply.earcut_benchmark())
    # print(ply.earcut())
    # if len(ply.earcut()) < len(ply.earcut_benchmark()):

    #     import matplotlib.pyplot as plt
    #     fig = plt.figure(figsize=(10, 10))
    #     ax = fig.add_subplot(1, 1, 1)

    #     for i, p in enumerate(ply.points):
    #         ax.text(p.x, p.y, str(i), c='r')
        
    #     for tri in ply.triangles:
    #         a, b, c = tri.a, tri.b, tri.c
    #         ax.plot([a.x, b.x, c.x, a.x], [a.y, b.y, c.y, a.y], c='b')
    #     for seg in ply.segments:
    #         a, b = seg.a, seg.b
    #         ax.plot([a.x, b.x], [a.y, b.y], c='k')
        
    #     print(len(ply.points))
    #     for x, y in ply.points:
    #         print(x, y)
    #     plt.show()

def test_convex():
    pts = []
    for _ in range(100):
        length = random.uniform(1, 10)
        theta = random.uniform(0,1)*math.pi*2
        pts.append((length*math.cos(theta) + 10, length*math.sin(theta) + 10))
        
    # for _ in range(200):
    #     pts.append((random.randint(0, 10), random.randint(0, 10)))
    

    ply = ConvexHull(pts).polygon
    # print(' '.join(map(str, pts)))
    # print(' '.join(map(str, ply.points)))

    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1)
    for seg in ply.segments:
        a, b = seg.a, seg.b
        ax.plot([a.x, b.x], [a.y, b.y], c='k')
    ax.scatter([p[0] for p in pts],[p[1] for p in pts], c='r')

    plt.show()


if __name__ == '__main__':
    main()
