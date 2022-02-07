import networkx as nx
import matplotlib.pyplot as plt
from numpy import sqrt

def dist(a, b):
    return sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

G = nx.Graph()
G.add_edge(0, 1, weight=1)
G.add_edge(1, 2, weight=1)
G.add_edge(1, 3, weight=1)
G.add_edge(2, 3, weight=1)
G.add_edge(2, 5, weight=1)
G.add_edge(2, 8, weight=1)
G.add_edge(3, 4, weight=1)
G.add_edge(4, 5, weight=1)
G.add_edge(5, 6, weight=1)
G.add_edge(6, 7, weight=1)
G.add_edge(7, 8, weight=1)

print(G.edges)

    

pos = nx.kamada_kawai_layout(G)
for u, v in G.edges:
    G.edges[u, v]['weight'] = dist(pos[u], pos[v])
    print(G.edges[u, v]['weight'])
A = nx.algorithms.approximation.steiner_tree(G, G.nodes())


nx.draw(G, pos, node_size=30, node_color='k')
nx.draw(A, pos, node_size=40, node_color='r', edge_color='r', width=2)


ax = plt.gca()
ax.margins(0.20)
plt.axis("off")
plt.show()
