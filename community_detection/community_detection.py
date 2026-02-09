import math

class Node:
    '''Nodes as an object contain their unique identifer and their density representative of how many addresses reside within the Node'''
    def __init__(self,indentifier,hyper_node = [], density=0):
        self.identifier = indentifier
        self.density = density
        self.hyper_node = hyper_node
        
    def __repr__(self):
        return self.identifier
    

class Graph:
    '''graphs contain a list of vertices and initalise an adjacency matrix for all edges of the graph, as we are dealing with a complete, weighted graph'''
    def __init__(self,vertices:list[Node],edges:list[list[int]] = []):
        self.vertices = vertices
        if edges == []:
            self.edges = [[0 for i in range(0,len(vertices))] for j in range(0,len(vertices))]
        else:
            self.edges = edges
        self.partition = []
        self.partition_edges = [[0 for i in range(0,len(self.partition))] for j in range(0,len(self.partition))]
        
        self.cutoff_weight = math.inf
        
        
    def visualise_edges(self,edge='vertices'):
        match edge:
            case 'community':
                edge_list = self.partition_edges
                
            case 'vertices':
                edge_list = self.edges
                
            case _:
                raise Exception('Visualisation can visualise relationships of either graph vertices or communities')
                
        for i in range(0,len(edge_list)):
            print(edge_list[i])
        
        
    def alter_edge_weight(self,nodes:list[Node],weight:int):
        '''Appends the edge weight between nodes, as the graph isnt directed it is mirrored across the matrix'''
        i = self.get_Node_id(str(nodes[0]))
        j = self.get_Node_id(str(nodes[1]))
        
        if weight >= self.cutoff_weight:
            weight = 0
            
        self.edges[i][j] = weight
        self.edges[j][i] = weight
            
         
    def drop_node(self,node:Node):
        
        node_id = self.get_Node_id(str(node))
        
        self.vertices.pop(node_id)
        
        self.edges.pop(node_id)
        for i in range(0,len(self.vertices)):
            self.edges[i].pop(node_id)
        
        
    def get_Node_id(self,identifier:str):
        '''Returns the index of the column/row the Node resides on'''
        for i in range(0,len(self.vertices)):
            if str(self.vertices[i]) == identifier:
                return i


    def get_node_name(self,identifier:int):
        return self.vertices[identifier]


    def get_node_partition(self,node):
        for i in range(0,len(self.partition)):
            if node in self.partition[i]:
                return i


    def add_community(self,new_community:list[Node]):
        '''creates a community based off of a list of Nodes and ads this to the graph parition'''
        self.partition.append(new_community)
        
        '''Adds a new column and row to the adjacency matrix at the next index'''
        self.partition_edges.append([0])
        
        
        if len(self.partition) > 1:
            for x in range(0,len(self.partition)):
                while len(self.partition_edges[x]) < len(self.partition):
                    self.partition_edges[x].extend([0])
            
            
    def drop_community(self,community_id:int):
        
        self.partition.pop(community_id)
        
        self.partition_edges[community_id]
        for i in range(0,len(self.partition_edges)):
            self.partition_edges[i][community_id]
        
        
    def remove_node_from_community(self,node:Node,community:int):
        self.partition[community].remove(node)


    def add_node_to_community(self,node:Node,community:int):
        self.partition[community].append(node)
        
        
    def add_community_edge(self,i:int,j:int):
        '''Add an edge between communties determined by the sum of all edges from nodes of each community going into one another'''
        com_i = self.partition[i]
        com_j = self.partition[j]
        
        sum_edges = 0
        
        if com_i != com_j:
            for x in com_i:
                x = self.get_Node_id(str(x))
                for y in com_j:
                    y = self.get_Node_id(str(y))
                    sum_edges += self.edges[x][y]
                
        self.partition_edges[i][j] = sum_edges
        self.partition_edges[j][i] = sum_edges
                
        
    def sum_node_edge_weights(self,node:Node):
        '''returns the sum of all edges of a node within a graph'''
        node_id = self.get_Node_id(str(node))
        
        sum = 0
        
        for i in range(0,len(self.edges)):
            sum += self.edges[node_id][i]
            sum += self.edges[i][node_id]
        return sum
        
    
    def set_weight_cutoff(self,cutoff_weight):
        self.cutoff_weight = cutoff_weight
        
        
    def drop_community_edges(self,id:int):
        
        for i in range(0,len(self.partition_edges)):
            self.partition_edges[i].pop(id)
        
        self.partition_edges.pop(id)
        
    
    def drop_empty_communities(self):
        '''drops empty communities from the partition and removes edges from those communities'''

        for i in range(len(self.partition) - 1, -1, -1):
            
            if self.partition[i] == []:
                self.drop_community(i)
                self.drop_community_edges(i)
                    
            
def convert_partition_to_graph(graph:Graph):
    '''Returns a graph based on the partitions and partition edge weights of the input graph
    
    -Communities within the partition are represented as ordinally named nodes in the return graph
    '''
    
    node_list = [Node(f'{x}') for x in range(0,len(graph.partition))]
    return Graph(node_list,graph.partition_edges)
    
    
def modularity(graph:Graph,m:int = 0):
    '''returns the modularity score of a graph's current state
    
    -A value for m can be explicitly given to save time calculating
    '''
    N = len(graph.vertices)
    
    if m == 0:
        for i in range(0,len(graph.edges)):
            for j in range(0,len(graph.edges)):
                m += graph.edges[i][j]
    
    
    Q = 0
    
    if m == 0:
        return Q
                
    for community in graph.partition:
        community_ids = [graph.get_Node_id(str(x)) for x in community]
        for i in community_ids:
            for j in range(0,len(graph.vertices)):
                if j in community_ids:
                    Aij = graph.edges[i][j] + graph.edges[j][i]
                    Ki = graph.sum_node_edge_weights(str(graph.get_node_name(i)))
                    Kj = graph.sum_node_edge_weights(str(graph.get_node_name(j)))
                    
                    Q += Aij - ((Ki * Kj)/(2*m))
    
    Q = Q/(2*m)
    
    return Q                    


def partition_edge_reinitialise(graph:Graph):
    graph.partition_edges = [[0 for x in range(0,len(graph.partition))] for y in range(0,len(graph.partition))]
    for i in range(0,len(graph.partition)):
        for j in range(0,len(graph.partition)):
            graph.add_community_edge(i,j)    
    return graph


def check_community_empty(graph:Graph,id:int):
    '''Checks if a community is empty and removes it from the partition, returns the index for a replacement community'''
    if graph.partition[id] == []:
        graph.partition.pop(id)
        return [True,len(graph.partition)] # returns the length of the partition as this will be the next free index
    
    else:
        return [False,id]
    
    
def louvain_intialise(graph:Graph)->Graph:
    for node in graph.vertices:
        graph.add_community([node])
    
    for i in range(0,len(graph.vertices)):
        for j in range(0,len(graph.vertices)):
            graph.add_community_edge(i,j)   
    return graph
              
              
def louvain(graph:Graph,initialise:bool = True):
    
    if initialise == True:
        graph = louvain_intialise(graph)
    
    initial_Q = modularity(graph)
    max_Q = initial_Q
    for i in range(0,len(graph.vertices)): #for all nodes within the graph
        current_community = graph.get_node_partition(graph.vertices[i])
        potential_community = current_community
        
        for j in range(0,len(graph.vertices)): #we use an adjacency matrix and graphs are expected to be complete so increment over all other neighbouts
            if graph.edges[i][j] > 0 and graph.vertices[j] not in graph.partition[current_community]: 
                
                #current node i is,temporarily added to the community of node j and the partition edges are updated
                temp_community = graph.get_node_partition(graph.vertices[j])
                graph.remove_node_from_community(graph.vertices[i],current_community)
                
                graph.add_node_to_community(graph.vertices[i],temp_community)
                graph = partition_edge_reinitialise(graph)

                temp_Q = modularity(graph)
                
                # place current node i back into the original community, update edges again   
                graph.add_node_to_community(graph.vertices[i],current_community)
                graph.remove_node_from_community(graph.vertices[i],temp_community)
                graph = partition_edge_reinitialise(graph)
                
                if temp_Q > max_Q:
                    max_Q = temp_Q
                    potential_community = temp_community
                
        if potential_community != current_community:
            
            #print(f'{max_Q}, Hence swapped {graph.vertices[i]} from: {graph.partition[current_community]} \nto: {graph.partition[potential_community]}')
            
            graph.remove_node_from_community(graph.vertices[i],current_community)
        
            graph.add_node_to_community(graph.vertices[i],potential_community)
            graph = partition_edge_reinitialise(graph) 
              

    return graph


def get_community_hypernodes(partition: list[Node]):
    '''returns a cleaned up list of nodes based on a graph partition'''
    
    node_list = []
    for i in range(0,len(partition)):
        if partition[i] != []:
            partition_data = []
            for node in partition[i]:
                if node.hyper_node != []:
                    partition_data.append[node.hyper_node]
                else:
                    partition_data.append(node)
                    
            node_list.append(Node(f'community {i}',partition_data))
            
    return node_list
        