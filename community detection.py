class Node:
    '''Nodes as an object contain their unique identifer and their density representative of how many addresses reside within the Node'''
    def __init__(self,indentifier, density=0):
        self.identifier = indentifier
        self.density = density
        
    def __repr__(self):
        return self.identifier
    

class Graph:
    '''graphs contain a list of vertices and initalise an adjacency matrix for all edges of the graph, as we are dealing with a complete, weighted graph'''
    def __init__(self,vertices:list[Node]):
        self.vertices = vertices
        self.edges = [[0 for i in range(0,len(vertices))] for j in range(0,len(vertices))]
        self.partition = []
        self.partition_edges = [[0 for i in range(0,len(self.partition))] for j in range(0,len(self.partition))]
        
        
    def visualise_edges(self):
        for i in range(0,len(self.edges)):
            print(self.edges[i])
        
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

    def add_community(self,node_list:list[Node]):
        '''creates a community based off of a list of Nodes and ads this to the graph parition'''
        self.partition.append(node_list)
        
        '''creates a new  column and row for the adjacency matrix to hold all edge weights'''
        self.partition_edges.append([0])

        if len(self.partition_edges) > 1:
            for column in self.partition_edges:
                column.append(0)
            
            
    def drop_community(self,community_id:int):
        
        self.partition.pop(community_id)
        
        self.partition_edges[community_id]
        for i in range(0,len(self.partition_edges)):
            self.partition_edges[i][community_id]
        
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
                
        sum_edges
                
        
test1 = Node('Birmingham')
test2 = Node('Bath')
test3 = Node('Nottingham')
test_graph = Graph([test1,test2,test3])

test_graph.alter_edge_weight([test1,test2],5)
test_graph.alter_edge_weight([test1,test3],5)
test_graph.alter_edge_weight([test2,test3],5)
test_graph.alter_edge_weight([test2,test1],10)
test_graph.visualise_edges()

test_graph.add_community([test1])
test_graph.partition_edges
test_graph.add_community([test2,test3])
test_graph.add_community_edge(0,1)

test_graph.partition
test_graph.partition_edges
test_graph.edges

