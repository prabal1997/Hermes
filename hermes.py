import numpy as npy
from node import node
import heapq

class graph:

    def __init__(self, node_list=None):
        #initializer simply DECLARES the fields    
        self.__ref, self.__matrix = None, None;
        self.__visited, self.__slack = None, None;
        
        #loads data onto graph
        if (node_list):
            self.init_nodes(node_list);

    #BASIC GRAPH OPERATIONS

    def init_nodes(self, node_list):
        #check if we received a file name
        adj_list, weight_list = [], [];
        if (isinstance(node_list, str)):
            raw_input = "";
            try:
                #open file
                raw_input = open(node_list, "r");
                
                #read, clean data by stripping comments and blank lines
                #AND split input into 'data' and 'adjacency list'
                raw_input = list(raw_input);
                raw_input = [element.strip() for element in raw_input];
                raw_input = [ element.split(' ') for element in raw_input if (element and element[0]!='#') ];
                
                #store 'data', 'adjancency info.'' in their resp. lists
                ref_list = [];
                adj_list, weight_list = [], [];
                for index, element in enumerate(raw_input):
                    data = float(element[0]);
                    
                    element = element[1:];
                    edges, weights = element[0:len(element)//2], [float(weight) for weight in element[len(element)//2:]];
                    
                    adj_list.append(npy.asarray([int(num) for num in edges]));
                    weight_list.append(npy.asarray(weights));
                    
                    ref_list.append(node(data, index));
                    
                #store the lists in graph    
                self.__ref = ref_list;
                self.__matrix = npy.zeros(shape=(len(self.__ref), len(self.__ref)), dtype="float64");
            
            except:
                print("ERROR: could not open file, or the file had incorrect format");
                self.__ref, self.__matrix = None, None;
        
                return False;
                
        #check if we received a list of elements in the following format:
        #<value, [list_of_neighbours], [list_of_weights]>
        elif(isinstance(node_list, list) or isinstance(node_list, tuple)):
            try:
                self.__ref = npy.asarray([node(node_list[0][index], index) for index in range(len(node_list[0]))]);
                adj_list = [npy.asarray( node_list[1][index]) for index in range(len(node_list[1]))];
                weight_list = [npy.asarray(node_list[2][index]) for index in range(len(node_list[2]))];
                
            except:
                print("ERROR: could not process data, or the data had incorrect format");
                self.__ref = None;
                return False;
                
        else:
            print("ERROR: no input provided");
            return False;
            
        #adding edges to the adjacency matrix
        self.extend_graph([self.__ref, adj_list, weight_list], formatted=True);
        
        return True;
    
    def extend_graph(self, node_list, formatted=False):
        
        if (isinstance(node_list, list) or isinstance(node_list, tuple)):

            try:
                #check whether this function was called by the constructor
                new_ref, adj_list, weight_list = [], [], [];
                if (not formatted):
                    new_ref = npy.asarray([node(node_list[0][index], len(self.__ref)+index) for index in range(0, len(node_list[0]))]);
                    adj_list = [npy.asarray( node_list[1][index]) for index in range(len(node_list[1]))];
                    weight_list = [npy.asarray(node_list[2][index]) for index in range(len(node_list[2]))];
                    
                    new_ref = npy.hstack((self.__ref, new_ref));
                else:
                    new_ref, adj_list, weight_list = node_list[0], node_list[1], node_list[2];
    
                new_matrix = npy.zeros((len(new_ref), len(new_ref)));
                old_size = len(self.__matrix) if (self.__matrix is not None) else 0;
                new_matrix[0:old_size,0:old_size] = self.__matrix;

                #updating graph fields
                self.__ref = new_ref;
                self.__matrix = new_matrix;
                self.__visited = npy.zeros(len(self.__ref), dtype="bool_");
                
                #check whether this function was called by the constructor
                if (formatted):
                    for element, neighbours, weights in zip(self.__matrix, adj_list, weight_list):
                        if (len(neighbours)):
                            element[neighbours] = weights*(weights > 0);
                    npy.fill_diagonal(self.__matrix, 0);
                else:
                    #handle the case when we are simply adding new nodes
                    start_idx = len(self.__ref)-(len(adj_list));
                    for index in range(len(adj_list)):
                        self.__matrix[start_idx+index][adj_list[index]] = weight_list[index]*(adj_list[index] != index)*(weight_list[index] > 0);
                    
            except:
                print("ERROR: could not process data, or the data had incorrect format.");
                return False;
        else:
            print("ERROR: input provided in incorrect format");
            return False;
            
        return True;
    
    #this topologically sorts the graph and returns a list of nodes as an output
    def sort_DAG(self):
        print("sort_dag");
    
    #check if a path exists from 'node_1' to 'node_2'
    def check_path(self, node_1, node_2):
        print("DFS");
    
    #checks if the entire graph is connected (i.e. each node can be reached from a single node)
    def check_connected(self):
        print("check whether the graph is connected");
    
    #uses Kruskal's algorithm to build a MINIMUM SPANNING TREE
    #NOTE: assumes un-directed graph, or returns a random, directed DAG 
    def give_MST(self):
        #special case
        if (not self.__ref):
            return graph();
        
        #prepare a list of nodes, a list of edges
        node_list = self.__ref;
        edge_list = [];
        for index, element in enumerate(self.__matrix):
            local_edges = [ (index, num, node) for num, node in enumerate(element) if node ];
            edge_list.extend(local_edges);
        
        #sort edges by weight (in non-increasing order)
        edge_list.sort(key = lambda element: -element[2]);
        
        #initializing sets (using hash-tables)
        set_list = [{node: node_list[node]} for node in range(len(node_list))];
        
        #making the MST
        tree_edges = {};
        while(len(tree_edges) != len(node_list)-1):
            #check if edge is part of the tree
            edge = edge_list.pop();
            if (set_list[edge[0]] != set_list[edge[1]]):
                #merge the sets that contain the two nodes of the edge
                new_set = (set_list[edge[0]] if ( len(set_list[edge[1]]) > len(set_list[edge[0]]) ) else set_list[edge[1]]);
                for node_num in edge[:-1]:
                    new_set[node_num] = node_list[node_num];
                    set_list[node_num] = new_set;
                
                #incrementing counter, extending tree                
                tree_edges[edge[0]] = [ node_list[edge[0]].data(), [edge[1]], [edge[2]] ];
        
        #convert the edge list to a node list & adjacency list
        element_list = [];
        for element in range(len(node_list)):
            if (element not in tree_edges):
                tree_edges[element] = [node_list[element].data(), [], []];
            element_list.append(tree_edges[element]);
        
        final_list = [[], [], []];
        for element in element_list:
            final_list[0].append(element[0]);
            final_list[1].append(element[1]);
            final_list[2].append(element[2]);
    
        return graph(final_list);
         
    #calculates shortest path from a node to some other node
    def shortest_paths(self, node_1, node_2):
        print("ERROR: use A*");
    
    
    def add_edges(self, node_num, edge_list, edge_weight):
        #check if we are receiving a list of requests
        if (not isinstance(node_num, list)):
            node_num, edge_list, edge_weight = npy.asarray(list(node_num)), npy.asarray(list(edge_list)), npy.asarray(list(edge_weight));
        #process entire list at one go
        try:
            for index, triplet in enumerate(zip(node_num, edge_list, edge_weight)):
                node_idx, new_edges, new_weights = triplet;
                new_edges, new_weights = npy.asarray(new_edges), npy.asarray(new_weights);
                
                self.__matrix[node_idx][new_edges] = new_weights*(node_idx != new_edges)*(new_weights > 0); 
                
        except:
            print("ERROR: erroneous input provided");
            return False;
            
    def delete_node(self, node_num):
        #convert input to a numpy array
        if (isinstance(node_num, node)):
            node_num = node_num.index();
        if (isinstance(node_num, list) or isinstance(node_num, tuple)):
            node_num = npy.asarray(node_num);
        else:
            node_num = npy.array([node_num]);
            
        #bounds checking
        if ( any(node_num < 0) or any(node_num >= len(self.__ref)) ):
            print("ERROR: invalid node for deletion");
            return False;
        else:

            #fix the ref-list
            self.__ref = npy.delete(self.__ref, node_num, axis=0);
            for index, element in enumerate(self.__ref):
                element._set_index(index);
            
            #fix the adjancency matrix
            self.__matrix = npy.delete(self.__matrix, node_num, axis=0);
            self.__matrix = npy.delete(self.__matrix, node_num, axis=1);
            
    def change_data(self, input_node, new_data):
        #check data-type of the input node
        if (isinstance(input_node, int)):
            try:
                #check the data-type of the received data
                if (type(self.__ref[0].data()) == type(new_data)):
                    self.__ref[input_node]._set_data(new_data);
                else:
                    print("ERROR: incorrect input data-type.");
                    return False;
            except:
                print("ERROR: incorrect index received.");
                return False;
        elif (isinstance(input_node, node)):
            #check the data-type of the received data
            if (type(self.__ref[0].data()) == type(new_data)):
                input_node._set_data(new_data);
            else:
                print("ERROR: incorrect input data-type");
                return False;
        else:
            print("ERROR: incorrect input-node format.");
            return False;
            
    def print_graph(self, node_list=None):
        try:
            #we find the adjacency lists corresponding to specific nodes, and print them
            if (not node_list):
                node_list = npy.arange(0, len(self.__ref), 1);
            
            node_list = npy.asarray(node_list);
            new_matrix = self.__matrix[node_list][node_list];
            
            print("<<---------------------->>");
            print("Graph for nodes " + str(node_list) + ":\n");
            for index, element in enumerate(zip(node_list, new_matrix)):
                node_num, node_edges = element;
                
                out_string = ("Node "+str(node_num)+": ") + str([ str(float(edge)) + " @ "+str(index) for index, edge in enumerate(node_edges) if edge]);
                print(out_string);
            print("<<---------------------->>");
            
        except:
            print("ERROR: invalid node list provided");
            return False;
            
        return True;
            
x = graph();
x.init_nodes("source");
#x.extend_graph([[3, 2, 5], [2, 3, 1], [55, 99, 5]]);
#x.print_graph();
#x.add_edges([0, 10], [9, 9], [15, 32.234]);
#x.print_graph();
#x.delete_node([10]);
x.print_graph();
y = x.give_MST();
y.print_graph();