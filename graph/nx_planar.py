import networkx as nx
import matplotlib.pyplot as plt
import random

from networkx.drawing.nx_pylab import draw_planar

# G = nx.Graph()
# G.add_edge(0, 1)
# G.add_edge(1, 2)
# G.add_edge(1, 3)
# G.add_edge(2, 3)
# G.add_edge(2, 5)
# G.add_edge(2, 8)
# G.add_edge(3, 4)
# G.add_edge(4, 5)
# G.add_edge(5, 6)
# G.add_edge(6, 7)
# G.add_edge(7, 8)

G = nx.Graph()
N = 20

for i in range(N):
    v = random.randint(0, N)
    if(v != i):
        G.add_edge(i, v)
    rnd = random.random()
    if(rnd > 0.5): 
        u = random.randint(0, N)
        if(u != i and u != v):
            G.add_edge(i, u)


options = {
    "font_size": 36,
    "node_size": 100,
    "node_color": "white",
    "edgecolors": "black",
    "linewidths": 2,
    "width": 2,
}

is_planar, embedding = nx.check_planarity(G)
if(is_planar):
    nx.draw_planar(G, **options)
else:
    nx.draw_random(G, **options)

ax = plt.gca()
ax.margins(0.20)
plt.axis("off")

if(is_planar):
    plt.title("Planar Graph")
else:
    plt.title("Random Graph")
plt.show()
