from copy import copy, deepcopy
l = [3, [4, 99, 1], (1, 2, 3)]

r = list(l)
sr = copy(l)
dr = deepcopy(l)

l.append(100)
r[1] += [3, 4]
r[2] += (4, )

print(l) # [3, [4, 99, 1, 3, 4], (1, 2, 3), 100]
print(r) # [3, [4, 99, 1, 3, 4], (1, 2, 3, 4)]
print(sr) # [3, [4, 99, 1, 3, 4], (1, 2, 3)]
print(dr) # [3, [4, 99, 1], (1, 2, 3)]


class Bus:
    def __init__(self, passengers = None):
        if passengers is None:
            self.passengers = []
        else:
            self.passengers = passengers
    
    def pick(self, name):
        self.passengers.append(name)
    
    def drop(self, name):
        self.passengers.remove(name)

a = Bus(['Alice', 'Bob'])
b = deepcopy(a)
a.pick('Clarie')
print(a.passengers)
print(b.passengers)


class GhostBus:
    def __init__(self, passengers = []):
        self.passengers = passengers
    
    def pick(self, name):
        self.passengers.append(name)
    
    def drop(self, name):
        self.passengers.remove(name)

c = GhostBus()
d = deepcopy(c)
e = GhostBus()
c.pick('Clarie')
print(c.passengers)
print(d.passengers)
print(e.passengers)


def bye():
    print("Byebye")

import weakref

s1 = {1, 2, 3}
s2 = s1
ender = weakref.finalize(s1, bye)
print(ender.alive)
del s1
print(s2)
s2 = 'hello'
print(ender.alive)

