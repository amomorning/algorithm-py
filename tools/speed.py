import random
n = 1000000
a = []
for i in range(n):
    a.append(random.randint(0, i))
     


import timeit
start = timeit.default_timer()
# do something


st = set(range(n)) - set(a)
    
# elapsed time
elapsed = (timeit.default_timer() - start)
print(elapsed)

start = timeit.default_timer()
# do something

deg = [0] * n
for x in a:
    deg[x] += 1
leaves = []
for i in range(n):
    if deg[i] == 0:
        leaves.append(i)

# elapsed time
elapsed = (timeit.default_timer() - start)
print(elapsed)
