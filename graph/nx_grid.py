import matplotlib.pyplot as plt
import networkx as nx



G = nx.grid_2d_graph(5, 5)  # 5x5 grid
# This example needs Graphviz and PyGraphviz
nx.nx_agraph.write_dot(G, "nx_grid.dot")
# Having created the dot file, graphviz can be invoked via the command line
# to generate an image on disk, e.g.
print("Now run: dot -Tps grid.dot >grid.ps")

# Alternatively, the and image can be created directly via AGraph.draw
A = nx.nx_agraph.to_agraph(G)
A.draw("imgs/5x5.png", prog="neato")
