import heapq
import os
import time
import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def read_graph_from_file(file_path):
    graph = {}
    with open(file_path, 'r') as file:
        num_nodes = int(file.readline().strip())
        num_edges = int(file.readline().strip())

        for _ in range(num_edges):
            line = file.readline().strip().split()
            if len(line) != 3:
                continue
            node1, node2, weight = line[0], line[1], int(line[2])
            
            # Check for negative weights
            if weight < 0:
                messagebox.showerror("File Error", f"Edge encountered as negative.")
                raise ValueError(f"Negative weight detected: {node1} -> {node2} with weight {weight}")
            
            if node1 not in graph:
                graph[node1] = {}
            if node2 not in graph:  # Ensure all nodes exist in the graph
                graph[node2] = {}
            graph[node1][node2] = weight

    return graph, num_nodes, num_edges

def log_execution_details(file_name, source_node, num_nodes, num_edges, execution_time, end_node=None, path=None):
    log_file = "dijkstra.txt"
    with open(log_file, "a") as file:
        file.write(f"Graph File: {file_name}\n")
        file.write(f"Source Node: {source_node}\n")
        if end_node:
            file.write(f"End Node: {end_node}\n")
        file.write(f"Number of Nodes: {num_nodes}\n")
        file.write(f"Number of Edges: {num_edges}\n")
        file.write(f"Execution Time: {execution_time:.6f} seconds\n")
        if path:
            file.write(f"Path: {path}\n")
        file.write("-" * 50 + "\n")


def dijkstra(graph, start):
    priority_queue = [(0, start)]
    shortest_paths = {start: (None, 0)}
    visited = set()

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        if current_node in visited:
            continue

        visited.add(current_node)

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if neighbor not in shortest_paths or distance < shortest_paths[neighbor][1]:
                shortest_paths[neighbor] = (current_node, distance)
                heapq.heappush(priority_queue, (distance, neighbor))

    return shortest_paths


def reconstruct_path(shortest_paths, start, end):
    path = []
    current_node = end
    while current_node is not None:
        path.append(current_node)
        next_node = shortest_paths[current_node][0]
        current_node = next_node
    path = path[::-1]
    if path[0] == start:
        return path
    else:
        return []

def process_graph(file_path, start_node, end_node):
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        return None, None, None
    
    graph, num_nodes, num_edges = read_graph_from_file(file_path)
    
    if start_node not in graph or end_node not in graph:
        print(f"Start node ({start_node}) or end node ({end_node}) not in graph.")
        return None, None, None  # Return None when nodes are not in the graph

    start_time = time.perf_counter()  # Start measuring time
    shortest_paths = dijkstra(graph, start_node)
    end_time = time.perf_counter()  # End measuring time

    execution_time = (end_time - start_time) * 1000  # Convert to milliseconds

    if end_node in shortest_paths:
        path = reconstruct_path(shortest_paths, start_node, end_node)
        return path, shortest_paths[end_node][1], execution_time
    else:
        print(f"No path found from {start_node} to {end_node}")
        return None, None, execution_time  # Return None for no path found


class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Shortest Path Finder")

        # Create a frame for the input section
        input_frame = tk.Frame(root)
        input_frame.pack(pady=10)

        # Load graph file button
        self.load_button = tk.Button(input_frame, text="Load Graph File", command=self.load_file)
        self.load_button.grid(row=0, column=4, padx=5)

        # Start node input field
        self.start_label = tk.Label(input_frame, text="Start Node:")
        self.start_label.grid(row=0, column=0, padx=5)
        self.start_entry = tk.Entry(input_frame)
        self.start_entry.grid(row=0, column=1, padx=5)

        # End node input field
        self.end_label = tk.Label(input_frame, text="End Node:")
        self.end_label.grid(row=0, column=2, padx=5)
        self.end_entry = tk.Entry(input_frame)
        self.end_entry.grid(row=0, column=3, padx=5)

        # Find shortest path button
        self.find_button = tk.Button(input_frame, text="Find Shortest Path", command=self.find_shortest_path)
        self.find_button.grid(row=0, column=5, padx=5)

        # Result label for displaying the shortest path and execution time
        self.result_label = tk.Label(root, text="Find Shortest Path\nExecution time: 0.0 ms")
        self.result_label.pack(pady=10)

        # Create a canvas for the graph
        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(self.canvas_frame, height=1)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.graph_file = None

    def load_file(self):
        self.graph_file = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if self.graph_file:
            messagebox.showinfo("File Loaded", f"Graph file loaded: {self.graph_file}")

    def find_shortest_path(self):
        start_node = self.start_entry.get()
        end_node = self.end_entry.get()

        if not self.graph_file or not start_node or not end_node:
            messagebox.showerror("Input Error", "Please load a graph file and specify start and end nodes.")
            return

        # Read the graph from the file
        graph, num_nodes, num_edges = read_graph_from_file(self.graph_file)

        # Check if the start and end nodes exist in the graph
        if start_node not in graph:
            messagebox.showerror("Node Error", f"Start node '{start_node}' does not exist in the graph.")
            return
        if end_node not in graph:
            messagebox.showerror("Node Error", f"End node '{end_node}' does not exist in the graph.")
            return

        # Process the graph if both nodes exist
        path, distance, execution_time = process_graph(self.graph_file, start_node, end_node)

        if path is None:
            self.result_label.config(text=f"No path found.\nExecution time: {execution_time:.6f} ms")
            log_execution_details(self.graph_file, start_node, num_nodes, num_edges, execution_time)
        else:
            path_str = " -> ".join(path)
            self.result_label.config(text=f"Shortest Path: {path_str}\nDistance: {distance}\nExecution time: {execution_time:.6f} ms")
            self.display_graph(path)

            # Log the details including the end node and path
            log_execution_details(self.graph_file, start_node, num_nodes, num_edges, execution_time, end_node, path_str)



    def display_graph(self, path=None):
        # Clear the previous graph from the canvas (ensures no overlapping content)
        self.canvas.delete("all")  # Clears everything on the canvas
        
        # Clear the current matplotlib figure before creating a new one
        plt.clf()  # Clears the current figure
        
        # Read the graph from the file
        graph, _, _ = read_graph_from_file(self.graph_file)

        # Create a NetworkX graph
        G = nx.DiGraph()
        for node, neighbors in graph.items():
            for neighbor, weight in neighbors.items():
                G.add_edge(node, neighbor, weight=weight)

        # Use Kamada-Kawai layout for better spacing
        pos = nx.kamada_kawai_layout(G)

        # Draw the graph
        nx.draw(G, pos, with_labels=True, node_size=400, node_color='lavender', font_size=6, font_weight='bold', width=1)

        if path:
            edges_in_path = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
            nx.draw_networkx_edges(G, pos, edgelist=edges_in_path, edge_color='purple', width=3, arrows=True)

        # Draw edge labels
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

        # Embed the plot into the canvas
        self.fig = plt.gcf()  # Get the current figure (matplotlib figure)

        # Check if the canvas widget exists and destroy the old one before creating a new one
        if hasattr(self, 'canvas_widget'):
            self.canvas_widget.get_tk_widget().destroy()  # Destroy the old canvas widget

        # Create a new FigureCanvasTkAgg widget
        self.canvas_widget = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        self.canvas_widget.draw()
        self.canvas_widget.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()
