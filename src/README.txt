The file iso.py contains the isomorphism related functions. 
The most important functions are:

- isIsomorphism(G1,G2,count) => returns the if G1 and G2 are isomorphic. If count = True it returns the number of isomorphisms.
- countIsomorphism(G1,G1.deepcopy(),count) => returns the number of automorphisms of G1. This algorithm uses the faster permutations implementation. If count = 0 it returns after the first isomorphism.
- The function isoSets(G,count) => returns the isomorphism sets in graph list G. If count = True, also the number of automorphisms per group are given.

The file AHU_trees.py contains tree related functions. These are called from the functions in iso.py if the graph is a tree.

You can run a test using the program run.py. This program takes a graph, or graph list and a variable count which can be true or false. 
Example:

python run.py Graph1.gr True

or

python run.py Graphs.grl False
