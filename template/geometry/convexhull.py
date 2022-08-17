from point import *
from polygon import Polygon

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
