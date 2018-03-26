from BFS import BFS

from graph_io import *
from time import time
from math import factorial

def find_center(G):  # Input is graph
    V = G.vertices
    for v in V:
        v.label = v.degree
    while len(V) > 2:
        D = []
        for v in V:
            if v.label == 1:
                D.append(v)
                V.remove(v)  # 'remove' vertex
                v.label = -1
        for d in D:
            for n in d.neighbours:
                if n.degree != -1:
                    n.label -= 1
    return V


def find_center2(G):
    v = G.vertices[0]
    BFS(G,v)
    v1 = v
    for w in G.vertices:
        if w.label > v1.label:
            v1 = w
    pred = BFS(G,v1)
    v2 = v1
    for w in G.vertices:
        if w.label > v2.label:
            v2 = w
    current = pred[v2]
    L = [v2]
    while current:
        L.append(current)
        current = pred[current]
    i = len(L) // 2
    if len(L)%2 == 0:
        return [L[i-1],L[i]]
    else:
        return [L[i]]




def rooted_tree(G,c):   # Input is Graph and a vertex c which is the center
    levels = {c: 0}
    k = 1
    A = {c}
    Done = {c}
    while len(levels) < len(G.vertices):
        B = set()
        for i in A:
            B = B | set(i.neighbours)
            Done = Done | {i}
            levels[i] = k
        A = B-Done
        k +=1
    return levels


def assign_canonical_names(v, label):  # Input is vertex and labels of vertices
    if v.degree == 1:
        v.label = '10'
    else:
        A = [a for a in v.neighbours if label[a] > label[v]]
        for a in A:
            assign_canonical_names(a,label)
        L = [a.label for a in A]
        L.sort()
        temp = ''
        for i in L:
            temp += str(i)
        v.label = '1' + temp + '0'


def ahu_tree_isomorphism(G1, G2,count=False):
    c1 = find_center2(G1)
    c2 = find_center2(G2)
    if len(c1) != len(c2):
        return 0
    if len(c1) == 1 and len(c2) == 1:
        assign_canonical_names(c1[0] , rooted_tree(G1,c1[0]))
        assign_canonical_names(c2[0], rooted_tree(G2, c2[0]))
        n1 = c1[0].label
        n2 = c2[0].label
        if n1 == n2:
            if count:
                return count_sub_auto(G1,c1[0])
            else:
                return 1
        else:
            return 0
    else:
        c2 = c2[0]
        c11 = c1[0]
        c12 = c1[1]
        assign_canonical_names(c2, rooted_tree(G2, c2))
        n2 = c2.label
        assign_canonical_names(c11, rooted_tree(G1, c11))
        n11 = c11.label
        assign_canonical_names(c12, rooted_tree(G1, c12))
        n12 = c12.label
        automorphisms = 0
        if n2 == n11:
            if count:
                automorphisms += count_sub_auto(G1,c11)
            else:
                return 1
        if n2 == n12:
            if count:
                automorphisms += count_sub_auto(G1,c12)
            else:
                return 1
        return automorphisms

def tree_isomorphisms(G):
    L = list(range(len(G)))
    Iso = [[0]]
    L.remove(0)
    while L:
        a = L[0]
        Isomorphic = False
        for i in Iso:
            if ahu_tree_isomorphism(G[i[0]], G[a]):
                Isomorphic = True
                i.append(a)
                L.remove(a)
        if not Isomorphic:
            Iso.append([a])
            L.remove(a)
    return Iso


def automorphisms(G):
    c = find_center2(G)
    c = c[0]
    assign_canonical_names(c, rooted_tree(G, c))
    return count_sub_auto(G,c)

def count_sub_auto(G,v):
    Children = {}
    for w in v.neighbours:
        if len(w.label) < len(v.label):
            Children.setdefault(w.label,[]).append(w)

    if not Children:
        return 1
    else:
        count = 1
        for k,v in Children.items():
            count *= factorial(len(v))
            count *= count_sub_auto(G,v[0])**len(v)
        return count
