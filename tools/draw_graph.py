# usage
# cat .\example_graph.txt | python .\draw_graph.py 

import matplotlib.pyplot as plt
import networkx as nx
import sys

G = nx.parse_edgelist(sys.stdin, nodetype = int, data = (('w', int), ))
print(G.nodes())
print(G.edges(data = True))

pos = []
try:
    pos = nx.planar_layout(G)
except nx.NetworkXException as e:
    pos = nx.circular_layout(G)

plt.axis('off')
nx.draw_networkx(G, pos, with_labels = True)
nx.draw_networkx_edge_labels(G, pos)

plt.show()
