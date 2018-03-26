import sys
from graph_io import *
from iso import *

if len(sys.argv) < 2:
    print("Take as input a single graph or a list of graphs")
    print("usage: %s <filename> <count=[true|false]>" % sys.argv[0])
    sys.exit()
myCount = sys.argv[2]
filename = sys.argv[1]
List = False
if ".grl" in filename:
    List = True

with open(filename) as f:
    G = load_graph(f,read_list=List)
    if List:
        isoSets(G[0],count=myCount)
    else:
        print(isIsomorph(G,G.deepcopy(),count=myCount))
