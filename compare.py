import matplotlib.pyplot as plt
import os

def parse_file(file_path):
    """
    Parses a file containing multiple records separated by dotted lines.
    Extracts the number of nodes, edges, and execution time for each graph.

    Args:
        file_path (str): Path to the file.

    Returns:
        list: A list of dictionaries containing data for each graph.
    """
    results = []
    with open(file_path, 'r') as file:
        graph_data = {}
        for line in file:
            line = line.strip()
            if line.startswith("Number of Nodes:"):
                graph_data['num_nodes'] = int(line.split(":")[1].strip())
            elif line.startswith("Number of Edges:"):
                graph_data['num_edges'] = int(line.split(":")[1].strip())
            elif line.startswith("Execution Time:"):
                graph_data['execution_time'] = float(line.split(":")[1].strip().split()[0])
            elif line.startswith("----"):  # Delimiter indicates end of one record
                if graph_data:  # Save completed graph data
                    results.append(graph_data)
                    graph_data = {}  # Reset for the next record
        if graph_data:  # Append the last record if no trailing delimiter
            results.append(graph_data)
    return results

def plot_comparative_graphs(data1, data2, labels):
    """
    Plots comparative graphs for execution time vs. number of nodes and edges for two datasets.

    Args:
        data1 (list): First dataset (list of dictionaries).
        data2 (list): Second dataset (list of dictionaries).
        labels (list): Labels for the datasets (e.g., ["Bellman-Ford", "Dijkstra"]).
    """
    num_nodes1 = [entry['num_nodes'] for entry in data1]
    num_edges1 = [entry['num_edges'] for entry in data1]
    execution_times1 = [entry['execution_time'] for entry in data1]

    num_nodes2 = [entry['num_nodes'] for entry in data2]
    num_edges2 = [entry['num_edges'] for entry in data2]
    execution_times2 = [entry['execution_time'] for entry in data2]

    # Plot Execution Time vs. Number of Nodes
    plt.figure(figsize=(10, 6))
    plt.plot(num_nodes1, execution_times1, marker='o', linestyle='-', label=f"{labels[0]} Execution Time")
    plt.plot(num_nodes2, execution_times2, marker='o', linestyle='--', label=f"{labels[1]} Execution Time")
    plt.title("Execution Time vs. Number of Nodes")
    plt.xlabel("Number of Nodes")
    plt.ylabel("Execution Time (seconds)")
    plt.grid()
    plt.legend()
    plt.tight_layout()
    plt.savefig("comparative_execution_time_vs_nodes.png")

    # Plot Execution Time vs. Number of Edges
    plt.figure(figsize=(10, 6))
    plt.plot(num_edges1, execution_times1, marker='o', linestyle='-', label=f"{labels[0]} Execution Time")
    plt.plot(num_edges2, execution_times2, marker='o', linestyle='--', label=f"{labels[1]} Execution Time")
    plt.title("Execution Time vs. Number of Edges")
    plt.xlabel("Number of Edges")
    plt.ylabel("Execution Time (seconds)")
    plt.grid()
    plt.legend()
    plt.tight_layout()
    plt.savefig("comparative_execution_time_vs_edges.png")

    # Display all figures at once
    plt.show()

def main():
    """
    Main function to parse Bellman-Ford and Dijkstra files, extract graph data, and plot comparative graphs.
    """
    file_path1 = "bellman.txt"
    file_path2 = "dijkstra.txt"

    # Verify file existence
    if not os.path.isfile(file_path1):
        print(f"Error: File '{file_path1}' does not exist.")
        return
    if not os.path.isfile(file_path2):
        print(f"Error: File '{file_path2}' does not exist.")
        return

    # Parse the files and extract data
    try:
        data1 = parse_file(file_path1)
        data2 = parse_file(file_path2)

        if not data1 or not data2:
            print("Error: One or both files contain no valid data.")
            return

        # Plot comparative graphs
        plot_comparative_graphs(data1, data2, labels=["Bellman-Ford", "Dijkstra"])
        print("Comparative plots have been saved and displayed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
