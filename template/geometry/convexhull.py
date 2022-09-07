import random
from point import *
from segment import Segment
import polygon


class ConvexHull:
    def __init__(self, points):
        self.polygon = None
        self.points = list(map(Point, points))
        self.build()

    def add_point(self, point):
        self.points.append(point)
        self.build()

    def build(self):
        pts = sorted(self.points)
        n, k = len(pts), 0
        convex = [None] * (n * 2)
        for p in pts:
            while k > 1 and cmp((convex[k - 1] - p).cross(convex[k - 2] - p)) <= 0:
                k -= 1
            convex[k] = p
            k += 1
        t = k
        for p in pts[-2::-1]:
            while k > t and cmp((convex[k - 1] - p).cross(convex[k - 2] - p)) <= 0:
                k -= 1
            convex[k] = p
            k += 1

        self.points = convex[:min(n, k - 1)]
        self.polygon = polygon.Polygon(self.points)

    def diameter(self, squared=False):
        n = len(self.points)
        if n <= 1: return 0, []
        if n == 2:
            u, v = self.points[0], self.points[1]
            return (u - v) ** 2, [u, v]

        j, d = 0, 0
        next_ = lambda i: 0 if i + 1 == n else i + 1

        for i in range(n):
            p, q = self.points[i], self.points[next_(i)]
            while cmp((self.points[j] - self.points[next_(j)]).cross(q - p)) <= 0:
                j = next_(j)
            u = self.points[j]
            for v in [p, q]:
                tmp = (u - v) ** 2
                if tmp > d:
                    d, pts = tmp, [u, v]
        return (d, pts) if squared else (math.sqrt(d), pts)

    def smallest_enclosing_box(self):
        n = len(self.points)

        area = math.inf
        next_ = lambda i: 0 if i + 1 == n else i + 1

        j, l, r = 0, 0, 0

        for i in range(n):
            p, q = self.points[i], self.points[next_(i)]
            while cmp((self.points[j] - self.points[next_(j)]).cross(q - p)) <= 0:
                j = next_(j)
            m = self.points[j]
            while cmp((self.points[r] - self.points[next_(r)]).dot(q - p)) <= 0:
                r = next_(r)
            if i == 0: l = r
            while cmp((self.points[l] - self.points[next_(l)]).dot(p - q)) <= 0:
                l = next_(l)
            seg = self.polygon.segments[i]

            u, v = seg.project_point(self.points[l]), seg.project_point(self.points[r])
            tmp = (u - v).norm() * seg.distance(m)

            if tmp <= area:
                area = tmp
                d = Segment(m, m + q - p)
                uu, vv = d.project_point(self.points[l]), d.project_point(self.points[r])
                pts = [u, v, vv, uu]
            if (pts[1] - pts[2]).cross(pts[0]):
                pts.reverse()
        return area, pts


def test_convex():
    pts = []
    for _ in range(100):
        length = random.uniform(1, 10)
        theta = random.uniform(0, 1) * math.pi * 2
        pts.append((length * math.cos(theta) + 10, length * math.sin(theta) + 10))

    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1)
    plt.xlim(-2, 22)
    plt.ylim(-2, 22)

    convexhull = ConvexHull(pts)
    d, ps = convexhull.diameter()
    print(d)
    ax.scatter([ps[0].x, ps[1].x], [ps[0].y, ps[1].y], color='c', zorder=10)
    ax.plot([ps[0].x, ps[1].x], [ps[0].y, ps[1].y], color='c', zorder=10, ls='dashed')

    area, ps = convexhull.smallest_enclosing_box()
    ps += [ps[0]]
    print(area)
    ax.scatter([p.x for p in ps], [p.y for p in ps], color='b', zorder=20)
    ax.plot([p.x for p in ps], [p.y for p in ps], color='b', ls='dotted', zorder=20)

    ply = convexhull.polygon

    for seg in ply.segments:
        a, b = seg.a, seg.b
        ax.plot([a.x, b.x], [a.y, b.y], c='k')
    ax.scatter([p[0] for p in pts], [p[1] for p in pts], c='r')

    # plt.show()
    plt.savefig('./imgs/polygon_bounding_box.png')
    


if __name__ == '__main__':
    test_convex()
