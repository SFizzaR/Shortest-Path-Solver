import tkinter as tk
from tkinter import filedialog, messagebox
import networkx as nx
import matplotlib.pyplot as plt
import cv2
import os
import time

# Function to save and display graphs
def save_and_display_graphs(graph_files_folder):
    images = []
    for file_name in sorted(os.listdir(graph_files_folder)):
        if file_name.endswith(".png"):
            img = cv2.imread(os.path.join(graph_files_folder, file_name))
            images.append(img)

    for img in images:
        cv2.imshow("Graph Visualization", img)
        key = cv2.waitKey(0)  # Wait for user input to show the next graph
        if key == 27:  # Press ESC to exit early
            break

    cv2.destroyAllWindows()

# Function to read a graph from a file
def read_graph_from_file(file_name):
    graph = nx.DiGraph()
    with open(file_name, 'r') as file:
        n_nodes = int(file.readline().strip())  # Number of nodes
        n_edges = int(file.readline().strip())  # Number of edges
        for _ in range(n_edges):
            line = file.readline().strip()
            if not line:  # Skip empty lines
                continue
            try:
                u, v, w = line.split()
                w = int(w)  # Convert weight to integer
                graph.add_edge(u, v, weight=w)
            except ValueError:
                print(f"Skipping invalid line: {line}")
                continue  # Skip invalid lines
    return graph, n_nodes, n_edges


# Bellman-Ford with visualization and saving graphs
def bellman_ford_with_visualization(graph, source, destination, output_folder):
    distances = {node: float('inf') for node in graph.nodes}
    distances[source] = 0
    predecessors = {node: None for node in graph.nodes}  # Track predecessors

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    plt.figure(figsize=(10, 6))  # Adjust the figure size for better compactness
    pos = nx.spring_layout(graph, seed=42, k=0.15)  # Reduce the k-value to pull nodes closer together

    # Shift the nodes upward by adjusting their y-coordinates
    for node in pos:
        pos[node] = (pos[node][0], pos[node][1] + 0.1)  # Increase the y-coordinate by 0.1

    nx.draw(graph, pos, with_labels=True, node_color='lavender', node_size=400, font_size=8, font_weight='bold', edge_color='black')
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=8)
    plt.title(f"Initial Graph (Source: {source})", fontsize=12)
    plt.tight_layout(pad=1)  # Adjust padding to make sure everything fits
    plt.savefig(os.path.join(output_folder, "graph_0.png"))
    plt.close()

    for i in range(len(graph.nodes) - 1):
        updated = False
        for u, v, weight in graph.edges(data='weight'):
            if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                distances[v] = distances[u] + weight
                predecessors[v] = u
                updated = True

                plt.figure(figsize=(10, 6))  # Adjust the figure size again for compactness
                nx.draw(graph, pos, with_labels=True, node_color='lavender', node_size=400, font_size=8, font_weight='bold', edge_color='black')
                nx.draw_networkx_edges(graph, pos, edgelist=[(u, v)], edge_color='green', width=2)
                edge_labels = nx.get_edge_attributes(graph, 'weight')
                nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=8)
                annotation_text = f"Relaxed Edge ({u}, {v})\nNew Dist: {distances[v]}"
                plt.annotate(annotation_text, xy=pos[v], xytext=(pos[v][0] + 0.03, pos[v][1] + 0.05),  # Adjusted offsets
                             arrowprops=dict(arrowstyle="->", lw=1.5), fontsize=8, fontweight='bold', color='red')
                plt.title(f"Iteration {i + 1}: Relaxed Edge ({u}, {v})", fontsize=12)
                plt.tight_layout(pad=1)
                plt.savefig(os.path.join(output_folder, f"graph_{i + 1}_{u}_{v}.png"))
                plt.close()

        if not updated:
            break

    # Final visualization with shortest path
    path = []
    current_node = destination
    while current_node is not None:
        path.insert(0, current_node)
        current_node = predecessors.get(current_node)

    if distances[destination] != float('inf'):
        shortest_path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]

        plt.figure(figsize=(10, 6))
        nx.draw(graph, pos, with_labels=True, node_color='lavender', node_size=400, font_size=8, font_weight='bold', edge_color='black')
        nx.draw_networkx_edges(graph, pos, edgelist=shortest_path_edges, edge_color='purple', width=5)
        edge_labels = nx.get_edge_attributes(graph, 'weight')
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=8)
        for node, dist in distances.items():
            if dist != float('inf'):
                plt.annotate(f"Dist: {dist}", xy=pos[node], xytext=(pos[node][0] + 0.03, pos[node][1] + 0.05),  # Adjusted offsets
                             fontsize=8, fontweight='bold', color='blue')
        plt.title(f"Final Graph with Shortest Path from {source} to {destination}", fontsize=12)
        plt.tight_layout(pad=1)
        plt.savefig(os.path.join(output_folder, "graph_final_with_shortest_path.png"))
        plt.close()

    plt.figure(figsize=(10, 6))
    nx.draw(graph, pos, with_labels=True, node_color='lavender', node_size=400, font_size=8, font_weight='bold', edge_color='black')
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=8)
    for node, dist in distances.items():
        if dist != float('inf'):
            plt.annotate(f"Dist: {dist}", xy=pos[node], xytext=(pos[node][0] + 0.03, pos[node][1] + 0.05),  # Adjusted offsets
                         fontsize=8, fontweight='bold', color='blue')
    plt.title("Final Graph with Shortest Path Distances", fontsize=12)
    plt.tight_layout(pad=1)
    plt.savefig(os.path.join(output_folder, "graph_final.png"))
    plt.close()

    if destination not in distances or distances[destination] == float('inf'):
        return None, distances, None
    return distances[destination], distances, path


# Function to log execution details
def log_execution_details(file_name, source_node, num_nodes, num_edges, execution_time, end_node=None, path=None):
    log_file = "bellman.txt"
    with open(log_file, "a") as file:
        file.write(f"Graph File: {file_name}\n")
        file.write(f"Source Node: {source_node}\n")
        if end_node:
            file.write(f"End Node: {end_node}\n")
        file.write(f"Number of Nodes: {num_nodes}\n")
        file.write(f"Number of Edges: {num_edges}\n")
        file.write(f"Execution Time: {execution_time:.6f} seconds\n")
        if path:
            file.write(f"Path: {' -> '.join(path)}\n")
        file.write("-" * 50 + "\n")

# GUI Application
def main_gui():
    def select_file():
        file_path = filedialog.askopenfilename(title="Select Graph File", filetypes=[("Text Files", "*.txt")])
        if file_path:
            file_label.config(text=f"Selected File: {os.path.basename(file_path)}")
            file_label.file_path = file_path

    def run_algorithm():
        if not hasattr(file_label, 'file_path'):
            messagebox.showerror("Error", "Please select a graph file first!")
            return

        source_node = source_entry.get()
        destination_node = destination_entry.get()

        if not source_node or not destination_node:
            messagebox.showerror("Error", "Please enter both source and destination nodes!")
            return

        graph, num_nodes, num_edges = read_graph_from_file(file_label.file_path)

        if source_node not in graph.nodes:
            messagebox.showerror("Error", f"Source node '{source_node}' is not in the graph!")
            return
        if destination_node not in graph.nodes:
            messagebox.showerror("Error", f"Destination node '{destination_node}' is not in the graph!")
            return

        output_folder = "graph_outputs"

        start_time = time.perf_counter()
        shortest_distance, distances, path = bellman_ford_with_visualization(graph, source_node, destination_node, output_folder)
        end_time = time.perf_counter()

        if shortest_distance is not None:
            messagebox.showinfo("Result", f"Shortest distance from {source_node} to {destination_node}: {shortest_distance}\nPath: {' -> '.join(path)}")
        else:
            messagebox.showinfo("Result", f"Destination node {destination_node} is unreachable from source node {source_node}.")

        log_execution_details(file_label.file_path, source_node, num_nodes, num_edges, end_time - start_time, destination_node, path)
        save_and_display_graphs(output_folder)

    root = tk.Tk()
    root.title("Bellman-Ford Algorithm with Visualization")

    tk.Label(root, text="Bellman-Ford Algorithm", font=("Helvetica", 16, "bold")).pack(pady=10)
    tk.Button(root, text="Select Graph File", command=select_file, font=("Helvetica", 12)).pack(pady=5)
    file_label = tk.Label(root, text="No file selected", font=("Helvetica", 10))
    file_label.pack(pady=5)

    tk.Label(root, text="Enter Source Node:", font=("Helvetica", 12)).pack(pady=5)
    source_entry = tk.Entry(root, font=("Helvetica", 12))
    source_entry.pack(pady=5)

    tk.Label(root, text="Enter Destination Node:", font=("Helvetica", 12)).pack(pady=5)
    destination_entry = tk.Entry(root, font=("Helvetica", 12))
    destination_entry.pack(pady=5)

    tk.Button(root, text="Run Algorithm", command=run_algorithm, font=("Helvetica", 12), bg="lightgreen").pack(pady=10)
    root.mainloop()

if __name__ == "__main__":
    main_gui()
