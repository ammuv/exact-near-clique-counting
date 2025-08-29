import os
import re
import copy
import numpy as np
import random

##### This is the main graph class. It contains the methods for creating and 
##### minor manipulations of graphs. The creation and edge insertion process creates 
##### undirected graphs, though one can easily adapt the representation for directed
##### graphs. Indeed, we later define the DAG (directed acyclic graph) class by
##### inheriting the methods of this class.
##### 
##### 
##### The graph is stored as an adjacency list. This is represented by a dict() structure,
##### where the keys are vertices and the values are sets with the corresponding neighborhood lists. 
##### 
##### C. Seshadhri, Jan 2015 

class graph(object):

#### Initializing empty graph
####

    def __init__(self):
        self.adj_list = dict()   # Initial adjacency list is empty dictionary 
        self.vertices = set()    # Vertices are stored in a set   
        self.degrees = dict()    # Degrees stored as dictionary
        self.colors = dict()     # Colors assigned to each node in the graph

#### Checks if (node1, node2) is edge of graph. Output is 1 (yes) or 0 (no).
####

    def isEdge(self, node1, node2):
        if node1 in self.vertices:               # Check if node1 is vertex
            if node2 in self.adj_list[node1]:    # Then check if node2 is neighbor of node1
                return 1                         # Edge is present!

        if node2 in self.vertices:               # Check if node2 is vertex
            if node1 in self.adj_list[node2]:    # Then check if node1 is neighbor of node2 
                return 1                         # Edge is present!

        return 0                # Edge not present!

#### Add undirected, simple edge (node1, node2)
####
    
    def Add_und_edge(self, node1, node2):

        if node1 == node2:            # Self loop, so do nothing
            return
        if node1 in self.vertices:        # Check if node1 is vertex
            nbrs = self.adj_list[node1]   # nbrs is neighbor list of node1
            if node2 not in nbrs:         # Check if node2 already neighbor of node1
                nbrs.add(node2)           # Add node2 to this list
                self.degrees[node1] = self.degrees[node1] + 1    # Increment degree of node1

        else:                    # So node1 is not vertex
            self.vertices.add(node1)        # Add node1 to vertices
            self.adj_list[node1] = {node2}  # Initialize node1's list to have node2
            self.degrees[node1] = 1         # Set degree of node1 to be 1

        if node2 in self.vertices:        # Check if node2 is vertex
            nbrs = self.adj_list[node2]   # nbrs is neighbor list of node2
            if node1 not in nbrs:         # Check if node1 already neighbor of node2
                nbrs.add(node1)            # Add node1 to this list
                self.degrees[node2] = self.degrees[node2] + 1    # Increment degree of node2

        else:                    # So node2 is not vertex
            self.vertices.add(node2)        # Add node2 to vertices
            self.adj_list[node2] = {node1}  # Initialize node2's list to have node1
            self.degrees[node2] = 1         # Set degree of node2 to be 1


#### Read a graph from a file with list of edges. Arguments are fname (file name),
#### dirname (directory name), sep (separator). Looks for file dirname/fname.
#### Assumes that line looks like:
#### 
#### node1 sep node2 sep <anything else>
#### 
#### If sep is not set, then it is just whitespace.
####
 
    def Read_edges(self, fname, sep=None):
        num_edges = 0
        with open(fname, 'r') as f_input: # Open file
            for line in f_input: # Read line by line. This is more memory efficient, but might be slower
                line = line.strip() # Remove whitespace from edge
                if not line.startswith('#'): # Skip comments
                    tokens = re.split(sep or r'\s+', line.strip())
                    if len(tokens) >= 2:
                        self.Add_und_edge(tokens[0], tokens[1])
                        num_edges += 1
        print('raw edges =', num_edges)    # Print number of lines in file


#### Give the size of the graph. Outputs [vertices (sum of degrees) wedges]
#### Note that sum of degrees is twice the number of edges in the undirected case 
####

    def Size(self):
        n = len(self.vertices)            # Number of vertices

        m = 0                    # Initialize edges/wedges = 0
        wedge = 0
        for node in self.vertices:        # Loop over nodes
            deg = self.degrees[node]      # Get degree of node
            m = m + deg                   # Add degree to current edge count
            wedge = wedge + deg * (deg - 1) / 2   # Add wedges centered at node to wedge count
        return [n, m, wedge]              # Return size info

#### Print the adjacency list of the graph. Output is written in dirname/fname. 
####
 
    def Output(self, fname, dirname):
        os.chdir(dirname)
        f_output = open(fname, 'w')    # Opening file

        for node1 in list(self.adj_list.keys()):   # Looping over nodes
            f_output.write(str(node1) + ': ')        # Writing node
            for node2 in (self.adj_list)[node1]:   # Looping over neighbors of node1
                f_output.write(str(node2) + ' ')     # Writing out neighbor
            f_output.write('\n')
        f_output.write('------------------\n')     # Ending with dashes
        f_output.close()

#### Compute the degree distribution of graph. Note that the degree is the size of the neighbor list, and is hence the *out*-degree if graph is directed. 
#### Output is a list, where the ith entry is the number of nodes of degree i.
#### If argument fname is provided, then list is written to this file. (This is convenient for plotting.)
####
 
    def Deg_dist(self, fname=''):
        degs = list((self.degrees).values())    # List of degrees
        dd = np.bincount(degs)                  # Doing bincount, so dd[i] is number of entries of value i in degs
        if fname != '':                         # If file name is actually given
            f_input = open(fname, 'w')
            for count in dd:                    # Write out each count in separate line
                f_input.write(str(count) + '\n')
            f_input.close()
        return dd 

    def DegreeOrder(self):
        '''Creates a DAG by imposing an order of vertices based on their degree.'''
        debug = False
        core_G = DAG()
        core_G.top_order = sorted(self.degrees, key=lambda el: self.degrees[el])
        if debug:
            print(core_G.top_order)
        for source in core_G.top_order:
            if debug:
                print(f"{source}: ", end='')
            core_G.vertices.add(source)
            core_G.adj_list[source] = set()
            core_G.degrees[source] = 0
            for node in self.adj_list[source]:
                if debug:
                    print(f"{node}", end=' ')
                if node in core_G.vertices:  # Average case O(1), worse case O(n) 
                    # We already accounted for this edge
                    # (node has higher order than source, so don't add add from higher to lower)
                    if debug:
                        print("(skipping), ", end='')
                    continue
                else:
                    if debug:
                        print(", ", end='')
                core_G.adj_list[source].add(copy.deepcopy(node))
                core_G.degrees[source] += 1
            if debug:
                print()
        return core_G

    def RandomOrder(self):
        '''Creates a DAG by imposing a random order to the vertices of the graph.'''
        debug = False
        core_G = DAG()
        # Makes a copy of the set of vertices and turns them into a list
        core_G.top_order = list(self.vertices)
        random.shuffle(core_G.top_order)
        for source in core_G.top_order:
            if debug:
                print(f"{source}: ", end='')
            core_G.vertices.add(source)
            core_G.adj_list[source] = set()
            core_G.degrees[source] = 0
            for node in self.adj_list[source]:
                if debug:
                    print(f"{node}", end=' ')
                if node in core_G.vertices:  # Average case O(1), worse case O(n) 
                    # We already accounted for this edge
                    # (node has higher order than source, so don't add add from higher to lower)
                    if debug:
                        print("(skipping), ", end='')
                    continue
                else:
                    if debug:
                        print(", ", end='')
                core_G.adj_list[source].add(copy.deepcopy(node))
                core_G.degrees[source] += 1
            if debug:
                print()
        return core_G


#### Simple function to generate random undirected graphs. Arguments are n (number of vertices)
#### and p (probability of edge). It adds every edge (node1, node2) with probability p.
#### 

    def Rand_graph(self, n, p):
        self.adj_list = dict()   # Initial adjacency list is empty dictionary 
        self.vertices = set()    # Vertices are stored in a set   
        self.degrees = dict()    # Degrees stored as dictionary

        for i in range(n):            # Looping over all vertex pairs
            for j in range(i):        # Generate edge (i, j)
                r = np.random.uniform(0,1)    # Generate random number
                if r <= p:                    # Compare to probability
                    self.Add_und_edge(i, j)   # Add edge


##### End of graph class



class DAG(graph):
    def __init__(self):
        super(DAG, self).__init__()
        self.top_order = [] # Store the order of the vertices

    def TopologicalOrder(self):
        '''Computes a topological ordering of a DAG'''
        in_degrees = {u: 0 for u in self.vertices}  # Initialization
        for u in self.vertices:
            for v in self.adj_list[u]:
                in_degrees[v] += 1
        queue = [u for u in self.vertices if in_degrees[u] == 0]  # Nodes with no incoming edges
        top_order = []
        while queue:
            u = queue.pop(0)
            top_order.append(u)
            for v in self.adj_list[u]:
                in_degrees[v] -= 1
                if in_degrees[v] == 0:
                    queue.append(v)
        if len(top_order) != len(self.vertices):
            print("The graph is not acyclic!")
            return None
        self.top_order = top_order
        return top_order

    def LongestPath(self, s, t):
        '''Computes longest path in a DAG from s to t'''
        self.TopologicalOrder()
        distances = {u: float('-inf') for u in self.vertices}
        distances[s] = 0
        for u in self.top_order:
            for v in self.adj_list[u]:
                if distances[u] != float('-inf'):
                    distances[v] = max(distances[v], distances[u] + 1)
        return distances[t]

