import graph
import graph_io
import GraphUtils

def main():
    test("/home/max/Mod7-Redo/src/torus24")

def test(path: str):
    test = None
    with open(path + ".grl") as f:
        test = graph_io.load_graph(f, graph.Graph, False)

    GraphUtils.colorRefinement(test, 0)

    with open(path + ".dot", 'w') as f:
        graph_io.write_dot(test, f, False)

    GraphUtils.countColours(test)

if __name__ == "__main__": main()
