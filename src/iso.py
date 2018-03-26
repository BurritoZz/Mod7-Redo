from graph import *
from basicpermutationgroup import *
from permv2 import *
from graph_io import *
from AHU_trees import *

def color(G):
    if not G.vertices:
        return dict()
    coloring = dict()
    inQueue = dict()
    queue = []
    maxColor = 0
    if (not hasattr(G.vertices[0],'color')):
        for v in G.vertices:
            v.color = len(v.neighbours)
            if (v.color > maxColor):
                maxColor = v.color
            coloring.setdefault(v.color,[]).append(v)
    else:
        for v in G.vertices:
            coloring.setdefault(v.color,[]).append(v)
            if (v.color > maxColor):
                maxColor = v.color
    ci = maxColor+1 #color index, this means that when we add a new color that this is the index of the new color. Then after the color has been added the collor index is increased by 1.

    #append all colors except the biggest to the queue
    maxLength = 0
    maxLengthColor = None
    for ck,color in coloring.items(): #key: color key, color: value
        if (len(color) > maxLength):
            maxLength = len(color)
            maxLengthColor = color
    for ck,color in coloring.items():
        if (color != maxLengthColor):
            queue.append(ck)
            inQueue[ck] = True
        else:
            inQueue[ck] = False

    while (queue): 
        #take the first  element of the queue
        ck = queue.pop(0)
        color = coloring[ck]
        inQueue[ck] = False
        if (not color):
            continue
        #new colors to be added to the dictionary
        newcolors = dict()
        #count for each neighbours how many neighbours it has in the current color.
        colorNeighbours = dict()
        for v in color:
            for n in v.neighbours:
                if (n.color != v.color):
                    if n in colorNeighbours:
                        colorNeighbours[n] += 1
                    else:
                        colorNeighbours[n] = 1
        #for each color store how big it is. That is, how many neighbours it has in the current color
        colorSize = dict()
        for n,neighboursNum in colorNeighbours.items():
            #add every neighbour to a new color. Neighbours belong to the same color if they have the same number of neighbours in the current color and the same n.color.
            newcolors.setdefault(n.color,dict()).setdefault(neighboursNum,[]).append(n)
            currentSize = colorSize.get(n.color)
            if (currentSize == None):
                currentSize = 0
            colorSize[n.color] = currentSize + 1

        for colorNum,splits in newcolors.items():
            toQueue = []
            #keep track of the biggest split. That is, the number of neighbours in the current color that occurres most often.
            biggest = None
            biggestLen = 0
            totalLen = colorSize[colorNum]

            skip= False #set to True if all vertices in a color change color, then one color has to remain.
            zeroNeighbours = False #no nodes with 0 neighbours
            if (totalLen == len(coloring[colorNum])):
                skip = True
            else:
                zeroNeighbours = True #there are nodes in this color that have no neighbours in the current color.
                #set it to biggest.
                biggest = colorNum
                biggestLen = len(coloring[colorNum]) - totalLen

            for neighboursNum,split in splits.items():
                #keep track of the biggest split.
                if (len(split) > biggestLen):
                    biggest = split
                    biggestLen = len(split)
                #skip the first one if skip is true.
                if (skip):
                    skip = False
                    continue
                coloring[ci] = split
                inQueue[ci] = False
                #change the color of each n in newcolor
                for n in split:
                    coloring[n.color].remove(n)
                    n.color = ci
                #remove the old color if it is empty.
                #TODO can probs be removed
                #if (not coloring[n.color]):
                    #coloring.pop(n.color,None)
                #increase color index.
                ci += 1
                toQueue.append(split[0].color)

            #if there are nodes with no neighbours in the current color. And it is not the biggest. Add it to the queue
            if (zeroNeighbours and biggest != colorNum):
                toQueue.append(colorNum)

            #add every color that is not the biggest to the queue.
            for newcolor in toQueue:
                if (newcolor != biggest):
                    if (not inQueue[newcolor]):
                        queue.append(newcolor)
                        inQueue[newcolor] = True
    return coloring,ci

def isIsomorph(G1,G2,G=None,count=False):
    if (len(G1.vertices) != len(G2.vertices) or len(G2.edges) != len(G1.edges)):
        return 0
    if (len(G1.edges) == len(G1.vertices) -1 and is_connected(G1) and is_connected(G2)):
        #it is a tree
        return ahu_tree_isomorphism(G1,G2,count)
    if (not G):
        G = Graph(False)
        for v in G1.vertices + G2.vertices:
            v._graph = G
            G.add_vertex(v)
        for e in G1.edges + G2.edges:
            G.add_edge(e)
    coloring,ci = color(G)
    for g in [G1,G2]:
        for v in g:
            v._graph = g
    num=isIsomorphColored(coloring)
    if (num == "?"):
        for ck,c in coloring.items():
            if (len(c) >= 4):
                break
        x = c[0]
        num = 0
        for y in c:
            if (y._graph != x._graph):
                prevC = getColorArray(G)
                x.color = ci
                y.color = ci
                #print("x: %d, y: %d" % (x.label,y.label))
                num = num+isIsomorph(G1,G2,G,count)
                if (not count and num):
                    return num
                restoreColors(G,prevC)
    return num

def countIsomorph(G1,G2,count=False):
    if (len(G1.vertices) != len(G2.vertices) or len(G2.edges) != len(G1.edges)):
        return []

    if (len(G1.edges) == len(G1.vertices) -1 and is_connected(G1) and is_connected(G2)):
        #it is a tree
        return ahu_tree_isomorphism(G1,G2,count)
    #check for cube
    G = Graph(False)
    for v in G1.vertices + G2.vertices:
        v._graph = G
        G.add_vertex(v)
    for e in G1.edges + G2.edges:
        G.add_edge(e)

    myX=[]
    num = generatePerms(G1,G2,G,count,X=myX)
    if not count:
        return num
    else:
        return order(myX)

def generatePerms(G1,G2,G=None,count=False,X=[],trivial=True):
    coloring,ci = color(G)
    for g in [G1,G2]:
        for v in g:
            v._graph = g
    num=isIsomorphColored(coloring)
    if (num == 1):
        perm = [0]*len(G1.vertices)
        for ck,c in coloring.items():
            perm[c[0].label] = c[1].label
        perm = permutation(len(perm),mapping=perm)
        if (not member(X,perm)):
            X.append(perm)

    elif (num == "?"):
        for ck,c in coloring.items():
            if (len(c) >= 4):
                break
        x = c[0]
        nexttrivial = trivial
        for y in c:
            if (y._graph != x._graph):
                prevC = getColorArray(G)
                x.color = ci
                y.color = ci
                #indent = ""
                #for i in range(0,layer):
                    #indent += "\t"
                #string = indent + "x: %d, y: %d, trivial: %r" % (x.label,y.label,nexttrivial)
                #print(string)
                num = generatePerms(G1,G2,G,count,X,nexttrivial)
                #if num:
                    #print(indent + "num: %d" % (num))
                if ((num and not trivial) or not count):
                    return num
                restoreColors(G,prevC)
                nexttrivial = False
    return num

def getColorArray(G):
    colors = []
    for v in G.vertices:
        colors.append(v.color)
    return colors

def restoreColors(G,colors):
    i = 0
    for v in G.vertices:
        v.color = colors[i]
        i += 1

def isIsomorphColored(coloring):
    bijection = 1
    for ck,color in coloring.items():
        graph1 = color[0]._graph
        g1 = 0
        g2 = 0
        for v in color:
            if v._graph == graph1:
                g1 += 1
            else:
                g2 += 1
        if (g1 != g2):
            return 0
        elif (g1 != 1):
            bijection = 0
    if (not bijection):
        return "?"
    else:
        return 1

def printGraph(G):
    print("graph")
    for v in G:
        if (not hasattr(v,'color')):
            color = 0
        else:
            color = v.color
        print("label: %s, color: %d" % (v.label,color))

def isoSets(Gs,count=False):
    setsI = [[0]]
    sets = [[Gs[0]]]
    for i in range(1,len(Gs)):
        added = False
        for j in range(0,len(sets)):
            mySet = sets[j]
            if (isIsomorph(Gs[i],mySet[0].deepcopy(),count=False)):
                mySet.append(Gs[i])
                setsI[j].append(i)
                added = True
                break
        if (not added):
            sets.append([Gs[i]])
            setsI.append([i])
    for i in range(0,len(setsI)):
        string = "["
        for graphI in setsI[i]:
            string += "%d," % (graphI)
        string = string[:len(string)-1]
        if count:
            G1 = sets[i][0]
            G2 = G1.deepcopy()
            aut = countIsomorph(G1,G2,count=True)
            string += "] \t#auts: %d" % aut
        else:
            string += "]"
        print(string)

def member(H,f):
    a = FindNonTrivialOrbit(H)
    if (a == None):
        return False
    if f in H or f.istrivial():
        return True
    orbit,tvs = Orbit(H,a,returntransversal=True)
    b = f[a]
    if not b in orbit:
        return False
    comp = -tvs[orbit.index(b)] * f
    stab = Stabilizer(H,a)
    return member(stab,comp)

def order(H):
    a = FindNonTrivialOrbit(H)
    if a == None:
        return 1
    orbit = Orbit(H,a)
    stab = Stabilizer(H,a)
    return len(orbit)*order(stab)

def is_connected(G):
    for v in G.vertices:
        v.label = None
    BFS(G, G.vertices[0])
    for v in G.vertices:
        if v.label == None:
            return False
    return True
