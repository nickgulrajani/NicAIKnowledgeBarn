import random
from datetime import datetime, timedelta
from py2neo import Graph, Node, Relationship
import networkx as nx
import matplotlib.pyplot as plt

# Connect to Neo4j (update with your credentials)
graph = Graph("bolt://localhost:7687", auth=("neo4j", ""))

# Clear existing data
graph.delete_all()

# Helper function to generate random dates
def random_date(start, end):
    return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))

# Generate sample data
suppliers = [f"Supplier_{i}" for i in range(1, 11)]
manufacturers = [f"Manufacturer_{i}" for i in range(1, 6)]
distributors = [f"Distributor_{i}" for i in range(1, 4)]
retailers = [f"Retailer_{i}" for i in range(1, 21)]
products = [f"Product_{i}" for i in range(1, 51)]

# Create nodes
for entity in suppliers + manufacturers + distributors + retailers + products:
    node_type = entity.split('_')[0]
    node = Node(node_type, name=entity)
    graph.create(node)

# Create relationships
for product in products:
    # Supplier to Manufacturer
    supplier = random.choice(suppliers)
    manufacturer = random.choice(manufacturers)
    supply_time = random.randint(1, 10)
    graph.create(Relationship(
        graph.nodes.match(name=supplier).first(),
        "SUPPLIES",
        graph.nodes.match(name=manufacturer).first(),
        product=product, supply_time=supply_time
    ))

    # Manufacturer to Distributor
    distributor = random.choice(distributors)
    production_time = random.randint(5, 20)
    graph.create(Relationship(
        graph.nodes.match(name=manufacturer).first(),
        "PRODUCES_FOR",
        graph.nodes.match(name=distributor).first(),
        product=product, production_time=production_time
    ))

    # Distributor to Retailer
    retailer = random.choice(retailers)
    delivery_time = random.randint(1, 5)
    graph.create(Relationship(
        graph.nodes.match(name=distributor).first(),
        "DISTRIBUTES_TO",
        graph.nodes.match(name=retailer).first(),
        product=product, delivery_time=delivery_time
    ))

print("Supply chain knowledge graph created successfully!")

# Query to analyze the supply chain
query = """
MATCH path = (s:Supplier)-[r1:SUPPLIES]->(m:Manufacturer)-[r2:PRODUCES_FOR]->(d:Distributor)-[r3:DISTRIBUTES_TO]->(r:Retailer)
RETURN s.name AS supplier, m.name AS manufacturer, d.name AS distributor, r.name AS retailer,
       r1.product AS product, r1.supply_time + r2.production_time + r3.delivery_time AS total_time
ORDER BY total_time DESC
LIMIT 10
"""

results = graph.run(query)

# Create a NetworkX graph for visualization
G = nx.DiGraph()

for record in results:
    supplier = record['supplier']
    manufacturer = record['manufacturer']
    distributor = record['distributor']
    retailer = record['retailer']
    product = record['product']
    total_time = record['total_time']

    G.add_edge(supplier, manufacturer, product=product, time=total_time)
    G.add_edge(manufacturer, distributor, product=product, time=total_time)
    G.add_edge(distributor, retailer, product=product, time=total_time)

    G.nodes[supplier]['node_type'] = 'Supplier'
    G.nodes[manufacturer]['node_type'] = 'Manufacturer'
    G.nodes[distributor]['node_type'] = 'Distributor'
    G.nodes[retailer]['node_type'] = 'Retailer'

# Set up colors for different node types
color_map = {'Supplier': 'lightblue', 'Manufacturer': 'lightgreen', 
             'Distributor': 'lightcoral', 'Retailer': 'yellow'}
node_colors = [color_map[G.nodes[node]['node_type']] for node in G.nodes()]

# Draw the graph
pos = nx.spring_layout(G)
plt.figure(figsize=(15, 10))
nx.draw(G, pos, node_color=node_colors, with_labels=True, node_size=3000, font_size=8, font_weight='bold')

# Add edge labels
edge_labels = nx.get_edge_attributes(G, 'product')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

# Add a legend
legend_elements = [plt.Line2D([0], [0], marker='o', color='w', label=node_type,
                              markerfacecolor=color, markersize=15)
                   for node_type, color in color_map.items()]
plt.legend(handles=legend_elements, loc='upper right')

plt.title("Supply Chain Knowledge Graph - Longest Paths")
plt.axis('off')
plt.tight_layout()
plt.show()

print("Supply chain paths with longest total times:")
for record in results:
    print(f"Path: {record['supplier']} -> {record['manufacturer']} -> {record['distributor']} -> {record['retailer']}")
    print(f"Product: {record['product']}, Total Time: {record['total_time']} days\n")
