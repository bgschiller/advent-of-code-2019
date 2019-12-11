import networkx as nx
import sys

g = nx.Graph()

for line in sys.stdin:
  center, orbiter = line.strip().split(')')
  g.add_edge(orbiter, center)

path = nx.shortest_path(g, 'SAN', 'YOU')
print(len(path) - 3)
