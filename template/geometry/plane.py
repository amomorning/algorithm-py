import segment
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
        return segment.Segment(a, b)
    
    def to_plane(self, plane):
        move = self.base - plane.base
