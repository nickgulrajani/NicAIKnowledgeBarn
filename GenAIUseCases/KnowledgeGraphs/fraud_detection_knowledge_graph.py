#Author: Nicholas Gulrajani

import networkx as nx
import matplotlib.pyplot as plt
from py2neo import Graph

# Connect to Neo4j
graph = Graph("bolt://localhost:7687", auth=("neo4j", ""))

# Query to get a sample of nodes and relationships
query = """
MATCH (c:Customer)-[r:INITIATES]->(t:Transaction)-[s:IS_OF_TYPE]->(tt:TransactionType)
RETURN c.name AS customer, t.amount AS amount, tt.name AS type
LIMIT 50
"""

# Execute the query
results = graph.run(query)

# Create a NetworkX graph
G = nx.Graph()

# Add nodes and edges to the graph
for record in results:
    customer = record['customer']
    amount = record['amount']
    t_type = record['type']
    
    G.add_node(customer, node_type='Customer')
    G.add_node(f"${amount}", node_type='Transaction')
    G.add_node(t_type, node_type='TransactionType')
    
    G.add_edge(customer, f"${amount}")
    G.add_edge(f"${amount}", t_type)

# Set up colors for different node types
color_map = {'Customer': 'lightblue', 'Transaction': 'lightgreen', 'TransactionType': 'lightcoral'}
node_colors = [color_map[G.nodes[node]['node_type']] for node in G.nodes()]

# Draw the graph
pos = nx.spring_layout(G)
plt.figure(figsize=(15, 10))
nx.draw(G, pos, node_color=node_colors, with_labels=True, node_size=3000, font_size=8, font_weight='bold')

# Add a legend
legend_elements = [plt.Line2D([0], [0], marker='o', color='w', label=node_type,
                              markerfacecolor=color, markersize=15)
                   for node_type, color in color_map.items()]
plt.legend(handles=legend_elements, loc='upper right')

plt.title("Financial Transaction Knowledge Graph Sample")
plt.axis('off')
plt.tight_layout()
plt.show()



