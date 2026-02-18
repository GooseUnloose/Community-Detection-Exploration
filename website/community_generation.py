import sys,json,pandas

#sys.path.append('../../Community-Detection-Exploration')

from flask import render_template,request,Blueprint

from community_detection.community_detection import *
from community_detection.fetch_data import *


bp = Blueprint('community_generation',__name__)


@bp.route('/')
def home():
   return render_template('index.html')


   
@bp.route('/louvain')
def run_louvain():
   input_cities = request.args.get('cities_list').split(',')
   
   with open("data/city_graph.json", 'r') as file:
        cities_dict = json.load(file)
        
   cities_dict = load_graph_data()
   
   coordinate_df = pandas.read_csv('data/area_locations.csv')
   
   
   
   
   
   city_nodes = [Node(input_cities[x]) for x in range(0,len(input_cities))]
   
   city_coordinates = {}
   
   
   graph = Graph(city_nodes)
   graph.set_weight_cutoff(3600)
    
   for i in range(0,len(input_cities)):
      
      #Fetches the longitude and latitude from csv
      city_coordinates.update({input_cities[i] : {
         'lon' : coordinate_df['lon'].loc[coordinate_df['area'] == input_cities[i]].item(),
         'lat' : coordinate_df['lat'].loc[coordinate_df['area'] == input_cities[i]].item() }})
      
      for j in range(0,len(input_cities)):
         graph.alter_edge_weight([input_cities[i],input_cities[j]],(get_city_distances(input_cities[i],input_cities[j],cities_dict)))


   output = louvain(graph)

   output.drop_empty_communities()
   
   #return json of communities
   partition_dict = {'graph' : {x: [str(y) for y in output.partition[x]] for x in range(0,len(output.partition))},
                     'coordinates' : city_coordinates}
   
   rtn_partition = json.dumps(partition_dict)
   return rtn_partition