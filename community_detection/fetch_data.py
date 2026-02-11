import json,os


def load_graph_data():
    with open("../data/city_graph.json", 'r') as file:
        cities_dict = json.load(file)
    
    return cities_dict

def get_city_distances(root_city:str, target_city:str,graph_dict:dict):
    return graph_dict[root_city][target_city][1]


def fetch_city_edges():
    None
