import networkx as nx
import matplotlib.pyplot as plt
import momepy
import geopandas as gpd
from shapely.geometry import LineString
import numpy as np


pos = [(0, 0), (3, 0), (3, 2), (2, 2), (0, 2), (4, 0), (4, 0.4), (4, 2), (6, 0.4), (6, 2), (5, 2), (5, 4), (2, 4)]
edge_idx = [(0, 1), (1, 5), (0, 4), (1, 2), (2, 3), (3, 4), (5, 6), (6, 8), (8, 9), (9, 10), (7, 10), (2, 7), (6,7), (10, 11), (3, 12), (11, 12)]

geoms = [LineString([pos[idx[0]], pos[idx[1]]]) for idx in edge_idx]

dataframe = gpd.GeoDataFrame({ 'geometry': geoms})

G = momepy.gdf_to_nx(dataframe, approach='primal')
G_dual = momepy.gdf_to_nx(dataframe, approach='dual')

f, ax = plt.subplots(1, 2, figsize=(12, 6), sharex=True, sharey=True)

nx.draw(G, {n: [n[0], n[1]] for n in list(G.nodes)}, ax=ax[0], node_size=0)
nx.draw(G_dual, {n: [n[0], n[1]] for n in list(G_dual.nodes)}, ax=ax[1], node_size=100, node_color=[1/float(G_dual.degree(n)) for n in G_dual.nodes] ,cmap='tab20b')

plt.show()
