import networkx as nx
G = nx.Graph()

# basic add nodes
G.add_node(1)

n = 10
G.add_nodes_from(range(n))

# add a group of nodes at once
H = nx.path_graph(10)
G.add_nodes_from(H)

# add edges using similar methods
G.add_edge(1, 2)
e = (2, 3)
G.add_edge(*e)
G.add_edges_from([(1, 2), (1, 3)])
G.add_edges_from(H.edges())

# can also remove or clear
G.remove_node(H)
G.clear()

# get the number of nodes and edges
G.number_of_nodes(), G.number_of_edges()


# draw graph
import matplotlib.pyplot as plt
nx.draw(G)


# directed graph
DG = nx.DiGraph()
DG.add_weighted_edges_from([(1, 2 ,0.5), (3, 1, 0.75)])
DG.out_degree(1, weight='weight')

DG.degree(1, weight='weight')
DG.successors(1)
DG.predecessors(1)
