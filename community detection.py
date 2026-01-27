class Node:
    '''Nodes as an object contain their unique identifer and their density representative of how many addresses reside within the Node'''
    def __init__(self,indentifier, density=0):
        self.identifier = indentifier
        self.density = density
        
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
                
    for community in graph.partition:
        community_ids = [graph.get_Node_id(str(x)) for x in community]
        for i in community_ids:
            for j in range(0,len(graph.vertices)):
                if j not in community_ids:
                    Aij = graph.edges[i][j] + graph.edges[j][i]
                    Ki = graph.sum_node_edge_weights(str(graph.get_node_name(i)))
                    Kj = graph.sum_node_edge_weights(str(graph.get_node_name(j)))
                    
                    Q += Aij - ((Ki * Kj)/(2*m))
    
    Q = Q/(2*m)
    
    return Q                    


def reinitialise(graph:Graph):
    for i in range(0,len(graph.vertices)):
        for j in range(0,len(graph.vertices)):
            graph.add_community_edge(i,j)    
    return graph

def louvain_intialise(graph:Graph)->Graph:
    for node in graph.vertices:
        graph.add_community([node])
    
    for i in range(0,len(graph.vertices)):
        for j in range(0,len(graph.vertices)):
            graph.add_community_edge(i,j)   
    return graph

def louvain(graph:Graph,initialise:bool = True):
    '''Performs the Louvain algorithm for Community Detection of a graph
    
    -Function will keep looping until no greater improvement for modularity can be achieved
    
    -initialise is used to create a commmunity for each node in the graph, can be disabled to use a pre-existing partition
    '''
    
    if initialise == True:
        graph = louvain_intialise(graph)
    
    original_Q = modularity(graph)
    current_Q = modularity(graph)

    for i in range(0,len(graph.vertices)):
        current_community = graph.get_node_partition(graph.vertices[i])
        potential_Q = 0
        max_j = 0
        for j in range(0,len(graph.partition)):
            if current_community != graph.partition[j]:
                graph.remove_node_from_community(graph.vertices[i],current_community)
                graph.add_node_to_community(graph.vertices[i],j)
                
                mod = modularity(graph)
                
                if mod > potential_Q:
                    potential_Q = mod
                    max_j = j
                
                graph.remove_node_from_community(graph.vertices[i],j)
                graph.add_node_to_community(graph.vertices[i],current_community)
        
        if potential_Q > current_Q:
            current_Q = potential_Q
            graph.remove_node_from_community(graph.vertices[i],current_community)
            graph.add_node_to_community(graph.vertices[i],max_j)
            
            if graph.partition[current_community] == []:
                graph.drop_community(current_community)
                graph.partition_edges.pop(current_community)
                for i in graph.partition_edges:
                    i.pop(current_community)
        
    return graph,current_Q

        
                

    
    
test1 = Node('Birmingham')
test2 = Node('Bath')
test3 = Node('Nottingham')
test4 = Node('Coleshill')
test5 = Node('Lincon')
test_graph = Graph([test1,test2,test3,test4,test5])

test_graph.alter_edge_weight([test1,test2],5)
test_graph.alter_edge_weight([test1,test3],5)
test_graph.alter_edge_weight([test2,test3],5)
test_graph.alter_edge_weight([test2,test1],10)
test_graph.alter_edge_weight([test1,test4],100)
test_graph.alter_edge_weight([test3,test5],250)

a = louvain(test_graph)
a
a[0].visualise_edges('community')
a[0].visualise_edges()
a[0].partition
test_graph1 = Graph(a[0].partition,a[0].partition_edges)

test_graph1.visualise_edges()
b = louvain(test_graph1)




