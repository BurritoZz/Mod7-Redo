import graph
from collections import Counter
import sys

def printTable(data: list):
    for i, d in enumerate(data):
        line = '|'.join(str(x).ljust(12) for x in d)
        print(line)
        if i == 0:
            print('-' * len(line))

def colorRefinement(L: list, color: int=0):  # color is the highest color already assigned, if 0, it will assign initial colors
    # Initialize list that, for every vertex, contains the colors of its neighbours
    neighbourColors = [None]*len(L)
    # If no color has already been assigned, give everything an initial coloring
    if color == 0:
        for v in L:
            v.colornum = v.degree
            if v.colornum > color:
                color = v.colornum

    # Fill in the neighbour color list
    for v in L:
        neighbourColors[v.label] = Counter([n.colornum for n in v.neighbours])  # Van alle punten slaat die de samenstelling van de buren op

    # Execute this loop until the previous iteration did not change the color of any vertex
    for i in range(3):
        # Compare every vertex against every other vertex
        for v in L:
            for u in L:
                # If the vertices are the same, or if their colors are different, no changes are needed
                if u is v or u.colornum != v.colornum:
                    continue

                # If the colors of their neigbours are different, a change is needed
                if neighbourColors[v.label] != neighbourColors[u.label]:
                    color += 1
                    toDo = []
                    # Create the list of vertices which need a new color
                    for i in L:
                        colors = Counter([n.colornum for n in i.neighbours])
                        if colors == neighbourColors[u.label] and i.colornum == u.colornum:
                            toDo.append(i)

                    # Assign them their new color
                    for i in toDo:
                        i.colornum = color
                    # For the neigbours of these vertices, update the list of colors of their neighbours

                    for i in toDo:
                        for n in i.neighbours:
                            neighbourColors[n.label] = Counter([x.colornum for x in n.neighbours])
    return color

def countColours(L: list):
    data = [['colour', 'amount']]
    keys = []
    amount = []
    dict = {}
    for v in L:
        if v.colornum not in dict:
            dict[v.colornum] = 1
        else:
            dict[v.colornum] = dict[v.colornum] + 1
    for k in sorted(dict.keys()):
        keys.append(k)
        amount.append(dict[k])
    data = data + list(zip(keys, amount))
    printTable(data)
