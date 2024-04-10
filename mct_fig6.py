from mct import *
from ordering import *
from node import *
import pydot
import numpy as np
import re



#------------------------------------------------------------------------------
# Neighbourhood
#------------------------------------------------------------------------------

# 8-neighbours
c8 = [(i, j) for i in [-1, 0, 1] for j in [-1, 0, 1] if (i, j) != (0, 0)]

# 4-neighbours
c4 = [(0, 1), (1, 0), (0, -1), (-1, 0)]

# FUNCTION : write_graph
# DESC : Utility function for processing all father-child relations 
# of a graph and writing it in DOT language (using pydot)
# INPUT :
#	- g : pydot graph
#	- node : root node of the graph
# OUTPUT : none
# PRECONDITION :
#	- node should be a Node (as in mct_node.py)
# POSTCONDITION : none
def write_graph(g, node):

	father = str(node)
	for c in node.childs:
		child = str(c)
		g.add_edge(pydot.Edge(father, child))
		write_graph(g, c)

# extract two nodes from an edge
def get_nodes_name_from_edge(edge):
    
	elems = re.split(" -> |;", edge.to_string()) 
	return (elems[0], elems[1])

# import a hierarchical ordering from a dot file
def get_nodes_and_labels(path):

    # preparing anf filling the list of nodes and labels and create hierarchical links
    nodes = {}
    root = None
    
    (graph, ) = pydot.graph_from_dot_file(path)
    for edge in graph.get_edges():
        (l_source, l_dest) = get_nodes_name_from_edge(edge)

        if l_source not in list(nodes.keys()):
            n1 = Node_label(l_source)
            nodes[l_source] = n1
        
        if l_dest not in list(nodes.keys()):
            n2 = Node_label(l_dest)
            nodes[l_dest] = n2

        # create the hierarchical link
        parent = nodes[l_source]
        child = nodes[l_dest]
        parent.add_child(child)

        # define root
        root = parent
        
    return (root, list(nodes.values()))

# compute the MCT on the image of the figure 6 of the paper
def test_fig6():
    
    # define hierarchical ordering of labels
    (root, labels)=get_nodes_and_labels('bpt_labels_fig6.dot')

    # 
    a_label=0 # blue
    b_label=1 # light_blue
    c_label=2 # green
    d_label=3 # fuchsia
    e_label=4 # gray
    f_label=5 # cyan
    g_label=6 # red - this label exists but not necessarily in the image
    h_label=7 # orange
    i_label=8 # yellow

    # compute ordering 
    ordering=Ordering(root, labels)

    # compute transitive closure
    ordering.trans_closure()

    # write label graph in dot format
    gg = pydot.Dot(graph_type='digraph')
    write_graph(gg, root)
    gg.write("labels_fig6.dot")

    # define image
    F=np.array([[b_label, c_label, d_label, f_label, i_label],
                [b_label, i_label, d_label, f_label, i_label],
                [a_label, i_label, a_label, e_label, f_label],
                [e_label, i_label, a_label, e_label, f_label],
                [e_label, e_label, c_label, a_label, h_label]], 
               dtype='uint8')
	
    # define adjacency
    adj = c4

    # build MCT
    mct = MCT()
    root = mct.build(F, root.label, ordering, adj)

    # write MCT in dot format
    gg = pydot.Dot(graph_type='digraph')
    write_graph(gg, root)
    gg.write("mct_fig6.dot")


test_fig6()
