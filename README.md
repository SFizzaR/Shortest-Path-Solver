# Shortest-Path Solver: Bellman-Ford vs. Dijkstra

## Introduction
This project implements a shortest-path solver that compares the **Bellman-Ford** and **Dijkstra’s** algorithms, analyzing their execution times under different graph scenarios.

## Technologies Used
- **Programming Language**: Python  
- **GUI Framework**: Tkinter  
- **Graph Processing**: NetworkX (optional for visualization)  

## Features
- **Graph Input**: Users can define graphs through a GUI.  
- **Algorithm Selection**: Choose between Bellman-Ford and Dijkstra’s algorithms.  
- **Execution Time Analysis**: Compare their performances on different graph types.  
- **Visualization**: Display the computed shortest paths.  

## Installation & Setup
1. Clone the repository:  
   ```sh
   git clone <repository-url>
   cd shortest-path-solver
   
2. Run the program (first the algorithms, then compare.py):
   ```sh
   python <filename>.py

##  Usage
- Open the GUI and enter the graph details.
- Select the algorithm to run (Bellman-Ford or Dijkstra).
- View the computed shortest path and execution time analysis.

## Performance Analysis
- **Bellman-Ford**: Suitable for graphs with negative weights but runs in O(VE) time.
- **Dijkstra**: Faster on graphs with non-negative weights, using O(V log V) (with a priority queue).
The program compares _execution times_ for different graph sizes and structures.

## Possible Future Enhancements
- Add support for more graph algorithms (e.g., A*).
- Improve visualization with Matplotlib/NetworkX.
- Allow importing graphs from files.

## Conclusion
This project provides an interactive way to compare shortest-path algorithms, offering insights into their efficiency in various scenarios.

