from community_detection.community_detection import *
from community_detection.fetch_data import *
import argparse


def main():
    cities_dict = load_graph_data()
    input_cities = args.cities_list
    
    city_nodes = [Node(input_cities[x]) for x in range(0,len(input_cities))]
    
    graph = Graph(city_nodes)
    graph.set_weight_cutoff(3600)
    
    for i in range(0,len(input_cities)):
        for j in range(0,len(input_cities)):
            graph.alter_edge_weight([input_cities[i],input_cities[j]],(get_city_distances(input_cities[i],input_cities[j],cities_dict)))


    output = louvain(graph)

    output.drop_empty_communities()

    print(output.partition)
    print(output.visualise_edges('community'))
    
    print(get_community_hypernodes(output.partition))
    

if __name__ == '__main__':
    
    
    parser = argparse.ArgumentParser(
        description='Script for performing Louvain Community Detection on a complete graph'
    )
    
    parser.add_argument('--cities-list', required= True, type= str, nargs='+')
    parser.add_argument('--distance-cutoff ',required= False, type= int)
    args = parser.parse_args()
    main()