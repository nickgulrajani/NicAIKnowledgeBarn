import heapq
import networkx as nx
import matplotlib.pyplot as plt

# Define the network graph with distances in milliseconds (ms)
network_graph = {
    'A': {'B': 5, 'C': 3},
    'B': {'A': 5, 'C': 2, 'D': 4},
    'C': {'A': 3, 'B': 2, 'D': 1},
    'D': {'B': 4, 'C': 1}
}

# Function to find the shortest path using Dijkstra's algorithm
def dijkstra(graph, start, end, traffic):
    queue = [(0, start, [])]
    seen = set()
    mins = {start: 0}
    
    while queue:
        (cost, node, path) = heapq.heappop(queue)
        
        if node in seen:
            continue
        
        seen.add(node)
        path = path + [node]
        
        if node == end:
            return cost, path
        
        for neighbor, weight in graph[node].items():
            if neighbor in seen:
                continue
            prev = mins.get(neighbor, None)
            # The cost calculation includes both the edge weight (latency in ms) and the traffic (Bytes per Second)
            next_cost = cost + weight + traffic[neighbor]
            if prev is None or next_cost < prev:
                mins[neighbor] = next_cost
                heapq.heappush(queue, (next_cost, neighbor, path))
    
    return float("inf"), []

# Simulated real-time network traffic data in Bytes per Second (Bps)
traffic_data = {'A': 10, 'B': 25, 'C': 12, 'D': 20}

# Example usage
start_node = 'A'
end_node = 'D'

total_cost, optimal_path = dijkstra(network_graph, start_node, end_node, traffic_data)

# Output the results to a file
with open("results.txt", "w") as file:
    file.write(f"Optimal path from {start_node} to {end_node}: {' -> '.join(optimal_path)}\n")
    file.write("\nExplanation:\n")
    for i in range(len(optimal_path) - 1):
        current = optimal_path[i]
        next_node = optimal_path[i + 1]
        distance = network_graph[current][next_node]
        file.write(f"From {current} to {next_node}:\n")
        file.write(f"- Distance: {distance} ms\n")
        file.write(f"- Current network traffic at {current}: {traffic_data[current]} Bps\n")
        file.write(f"- Current network traffic at {next_node}: {traffic_data[next_node]} Bps\n")
        file.write(f"- Chose {next_node} because it has the least combined cost of distance ({distance} ms) and traffic ({traffic_data[next_node]} Bps).\n\n")

# Print the results to the terminal as well for immediate feedback
print(f"Optimal path from {start_node} to {end_node}: {' -> '.join(optimal_path)}\n")
print("Explanation:")
for i in range(len(optimal_path) - 1):
    current = optimal_path[i]
    next_node = optimal_path[i + 1]
    distance = network_graph[current][next_node]
    print(f"From {current} to {next_node}:")
    print(f"- Distance: {distance} ms")
    print(f"- Current network traffic at {current}: {traffic_data[current]} Bps")
    print(f"- Current network traffic at {next_node}: {traffic_data[next_node]} Bps")
    print(f"- Chose {next_node} because it has the least combined cost of distance ({distance} ms) and traffic ({traffic_data[next_node]} Bps).\n")

# Visualize the network graph and optimal path
G = nx.DiGraph()

# Add nodes to the graph
for node in network_graph:
    G.add_node(node)

# Add edges to the graph
for node, connections in network_graph.items():
    for dest_node, distance in connections.items():
        G.add_edge(node, dest_node, weight=distance)

# Draw the graph
pos = nx.spring_layout(G)
fig, ax = plt.subplots()
nx.draw(G, pos, with_labels=True, node_size=500, node_color='lightblue', font_size=16, font_weight='bold', ax=ax)

# Highlight the optimal path
path_edges = [(optimal_path[i], optimal_path[i+1]) for i in range(len(optimal_path)-1)]
nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=2, ax=ax)

plt.title("Network Graph with Optimal Path")
plt.axis('off')
plt.show()
