import importlib
import sys
import resource

mem_init = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

# do something


# used memory
mem_final = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
print('Initial RAM usage: {:14,}'.format(mem_init))
print('  Final RAM usage: {:14,}'.format(mem_final))

