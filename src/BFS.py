from graph import *
from graph_io import *

def BFS(G,s):
    for v in G.vertices:
        v.label = None
    s.label = 0
    L = [s]
    k = 1
    pred = {s: None}
    while L:
        v = L[0]
        for w in v.neighbours:
            if w.label == None:
                w.label = k
                pred[w] = v
                L.append(w)
                k += 1
        L.remove(v)
    return pred

