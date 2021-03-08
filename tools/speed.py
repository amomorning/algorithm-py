import timeit

start = timeit.default_timer()
# do something
test = [[0x3f3f3f3f0 for i in range(1<<20)] for j in range(20)]
elapsed = (timeit.default_timer() - start)
print(elapsed)

start = timeit.default_timer()
# do something
import numpy as np
test = np.full((1<<20, 20), 0x3f3f3f3f, dtype=np.int32)
elapsed = (timeit.default_timer() - start)
print(elapsed)
