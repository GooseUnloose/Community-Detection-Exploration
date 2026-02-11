# Community-Detection-Exploration

An exploration of identifying, locally optimal communities in dense graphs/networks. To be used in navigational services to identify geographically close communities from a list of locations

### Why?
When given a list of cities to visit over the course of a month (or any period of time), it is vital for efficiency's sake to determine if some places can be visited whilst you are already visiting another location. This cuts back on going back to areas that were already visited, and maximising the utility of trips.


### How?
For the less geographically minded, this would entail cumbersomely plotting all of the locations onto a map and checking how long it would take to get from one place to another. This takes time and is prone to human errors of judgement. This can be achieved algorithmically in a much shorter time period utilising a subsection of graph theory 'Community Detection'. This is the method of idenifying meaningfully informative commuinities within a graph partition. 

Currently this repository has the Louvain algorithm for finding an informative graph partition via maximising modularity.

With the jargon completed, it is time to cover just <i>how</i> to use this repository to group cities!

## Creating city groupings
The REPO contains both a script for command line execution and a more visual webapplication, created using Flask as a framework.

### Script method
To run the script simply cd into the project folder:
```
cd Community-Detection Exploration
```
Run the below script with parameters:
```
python louvain.py --cities-list [list of uk cities separated by a space] --distance-cutoff #max distance for a node edge

Returns [[community 1],[community 2] ,...,[community n]] #partition represented as a list of a lists of communites encompassing
                                                         #all of the cities passed as a parameter
```
### Webapp method
To run the web application cd into the website subfolder of the project:
```
cd Community-Detection Exploration/website
```
Run the below flask script to run the webapp on a local port
```
python -m flask run
```
