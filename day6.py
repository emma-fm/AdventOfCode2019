import inputProcessor as iP
import networkx as nx

# We'll use a directed graph to calculate our orbits.
# The sum of the orbits of a planet A will be the lenght of the path from A to COM
orbits = iP.dump_list_newline("day6")

# Get nodes and edges
edges = [(x.split(")")[0],x.split(")")[1]) for x in orbits] # COM)B -> (COM,B) -> Edge between COM and B
nodes_one = [x[0] for x in edges]
nodes_two = [x[1] for x in edges]
nodes = list(set().union(nodes_one, nodes_two))

orbit_graph = nx.Graph()
orbit_graph.add_nodes_from(nodes)
orbit_graph.add_edges_from(edges)

orb = 0
for n in list(orbit_graph.nodes):
    orb = orb + nx.shortest_path_length(orbit_graph, n, 'COM')

print("Total number of orbits: ", orb)

# The distance between you and Santa is again a path find problem
distance = nx.shortest_path_length(orbit_graph, 'YOU', 'SAN') - 2 #-2 because we don't count YOU and SAN
print("Orbital transfers to Santa: ", distance)