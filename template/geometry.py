import math


class Point:
    def __init__(self, *args):
        if len(args) == 1:
            args = args[0]
        if len(args) == 2:
            self.x, self.y = args
            self.__d = 2
        if len(args) == 3:
            self.x, self.y, self.z = args
            self.__d = 3
        if len(args) == 4:
            # Quaternion
            self.x, self.y, self.z, self.w = args
            self.__d = 4
        
    def __len__(self):
        return self.__d

    def __str__(self):
        if self.__d == 4:
            return str((self.x, self.y, self.z, self.w))
        elif self.__d == 3:
            return str((self.x, self.y, self.z))
        else:
            return str((self.x, self.y))
    
    def __hash__(self):
        if self.__d == 4:
            return hash((self.x, self.y, self.z, self.w))
        elif self.__d == 3:
            return hash((self.x, self.y, self.z))
        else:
            return hash((self.x, self.y))
        
    def __getitem__(self, key):
        if key == 'x' or key == 0:
            return self.x
        if key == 'y' or key == 1:
            return self.y
        if key == 'z' or key == 2:
            return self.z
        if key == 'w' or key == 3:
            return self.w
        raise KeyError('Invalid key: %s' % key)
    
    def __setitem__(self, key, value):
        if key == 'x' or key == 0:
            self.x = value
        if key == 'y' or key == 1:
            self.y = value
        if key == 'z' or key == 2:
            self.z = value
        if key == 'w' or key == 3:
            self.w = value
        raise KeyError('Invalid key: %s' % key)
    
    
    def __iter__(self):
        if self.__d == 4:
            return iter((self.x, self.y, self.z, self.w))
        elif self.__d == 3:
            return iter((self.x, self.y, self.z))
        else:
            return iter((self.x, self.y))
        
    def __neg__(self):
        ret = []
        for x in self:
            ret.append(-x)
        return Point(ret)
    
    def __eq__(self, rhs):
        if type(rhs) != Point: rhs = Point(rhs)
        assert len(rhs) == len(self)

        for i in range(len(self)):
            if self[i] != rhs[i]:
                return False
        return True
        
    def __le__(self, rhs):
        if type(rhs) != Point: rhs = Point(rhs)
        assert len(rhs) == len(self)

        for i in range(len(self)):
            if self[i] < rhs[i]:
                return True
            if self[i] > rhs[i]:
                return False
        return True
        
        
    def __lt__(self, rhs):
        if type(rhs) != Point: rhs = Point(rhs)
        assert len(rhs) == len(self)

        for i in range(len(self)):
            if self[i] < rhs[i]:
                return True
            if self[i] > rhs[i]:
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
    
    def norm(self, v = 2):
        return (self ** v) ** (1.0/v) if v <= 50 else max(self)
    
    def normalized(self):
        return self / self.norm() 
    
    def dot(self, rhs):
        if type(rhs) != Point: rhs = Point(rhs)
        return sum(self @ rhs)
    
    def cross(self, rhs):
        if type(rhs) != Point: rhs = Point(rhs)
        if self.__d == 3:
            a, b, c = self
            x, y, z = rhs
            return Point(-c*y + b*z, c*x - a*z, -b*x + a*y)
        elif self.__d == 2:
            return self.x * rhs.y - self.y * rhs.x
        raise ValueError("Invalid coordinates")

        
    def proj(self, rhs):
        if type(rhs) != Point: rhs = Point(rhs)
        return rhs * self.dot(rhs) / rhs.dot(rhs)
    
    # Quaternion
    def conj(self):
        ret = [self[0]]
        for i in range(1, len(self)):
            ret.append(-self[i])
        return Point(ret)
    
    def inv(self):
        l2 = self.dot(self)
        return self.conj() / l2

    def mulQ(self, rhs):
        assert self.__d == 4
        if type(rhs) != Point: rhs = Point(rhs)

        q0, q1, q2, q3 = self
        p0, p1, p2, p3 = rhs

        return Point(q0*p0 - q1*p1 - q2*p2 - q3*p3, \
                     q0*p1 + q1*p0 + q2*p3 - q3*p2, \
                     q0*p2 - q1*p3 + q2*p0 + q3*p1, \
                     q0*p3 + q1*p2 - q2*p1 + q3*p0)

    # rotate
    def rotate(self, angle):
        assert self.__d == 2
        c, s = math.cos(angle), math.sin(angle)
        x, y = self
        return Point(x * c - y * s, x * s + y * c)
        
    def rotate90(self):
        assert self.__d == 2
        return Point(-self.y, self.x)
    
    def rotateX(self, angle):
        if self.__d < 3: self.z = 0; self.__d = 3
        assert self.__d == 3
        c, s = math.cos(angle), math.sin(angle)
        x, y, z = self
        return Point(x, y * c - z * s, y * s + z * c)
    
    def rotateY(self, angle):
        if self.__d < 3: self.z = 0; self.__d = 3
        assert self.__d == 3
        c, s = math.cos(angle), math.sin(angle)
        x, y, z = self
        return Point(x * c + z * s, y, -x * s + z * c)

    def rotateZ(self, angle):
        if self.__d < 3: self.z = 0; self.__d = 3
        assert self.__d == 3
        c, s = math.cos(angle), math.sin(angle)
        x, y, z = self
        return Point(x * c - y * s, x * s + y * c, z)
    
    def rotateBy(self, axis, angle):
        if self.__d < 3: self.z = 0; self.__d = 3
        assert self.__d == 3
        if type(axis) != Point: axis = Point(axis)
        
        c, s = math.cos(angle), math.sin(angle)
        x, y, z = self
        ux, uy, uz = axis.normalized()

        return Point((c+ux*ux*(1-c))*x + (ux*uy*(1-c)-uz*s)*y + (ux*uz*(1-c)+uy*s)*z, \
                     (uy*ux*(1-c)+uz*s)*x + (c+uy*uy*(1-c))*y + (uy*uz*(1-c)-ux*s)*z, \
                     (uz*ux*(1-c)-uy*s)*x + (uz*uy*(1-c)+ux*s)*y + (c+uz*uz*(1-c))*z)


    def rotateByQ(self, axis, angle): 
        if self.__d < 3: self.z = 0; self.__d = 3
        assert self.__d == 3
        if type(axis) != Point: axis = Point(axis)
        
        axis = axis.normalized() * math.sin(angle*0.5)
        q = Point(math.cos(angle*0.5), axis.x, axis.y, axis.z)
        p = Point(1.0, self.x, self.y, self.z)

        return q.mulQ(p).mulQ(q.inv())


    def applyM(self, m):
        n = len(self)

        ret = []
        for i in range(n):
            tot = 0
            for j in range(n):
                tot += self[j] * m[i][j]
            ret.append(tot)

        return Point(ret)

if __name__ == '__main__':
    a = [Point(3, 4), Point(1, 2), Point(3, 5), Point(2,7)]
    # 按 y 排序
    a = sorted(a, key=lambda p: p.y)
    print(' '.join(map(str, (a))))

    

    a = Point(1, 2)
    b = Point(3, 4)

    print(a.proj(b))
    print(a.rotate(0.1))

    a = Point(1, 2, 3)
    print(a.rotateByQ((1, 1, 1), 0.5))
    print(a.rotateBy((1, 1, 1), 0.5))

    a = Point(1, 2, 3, 1)
    print(a.applyM([[1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 1], [0, 0, 0, 1]]))


    # print(a.rotate(math.pi/3))

    # (3, 8)

    # print(a.dot(b))
