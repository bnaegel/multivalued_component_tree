from mct import *
from ordering import *
from node import *
import pydot
import numpy as np



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




# compute the MCT on the image of the figure 1 of the paper
def test_fig1():

    # define hierarchical ordering of labels
    a=Node_label('a')
    b=Node_label('b')
    c=Node_label('c')
    d=Node_label('d')
    e=Node_label('e')
    f=Node_label('f')
    g=Node_label('g')
    h=Node_label('h')
    i=Node_label('i')

    labels=[]
    labels.append(a)
    labels.append(b)
    labels.append(c)
    labels.append(d)
    labels.append(e)
    labels.append(f)
    labels.append(g)
    labels.append(h)
    labels.append(i)

    a.add_child(b)
    a.add_child(c)
    b.add_child(d)
    b.add_child(e)
    b.add_child(f)
    c.add_child(g)
    g.add_child(h)
    g.add_child(i)

    # compute ordering 
    ordering=Ordering(a, labels)

    # compute transitive closure
    ordering.trans_closure()

    # write label graph in dot format
    gg = pydot.Dot(graph_type='digraph')
    write_graph(gg, a)
    gg.write("labels_fig1.dot")

    # define image
    F=np.array([[h.label, h.label, h.label, a.label, h.label, h.label],
               [e.label, h.label, a.label, a.label, i.label, h.label],
               [e.label, e.label, e.label, i.label, i.label, i.label],
               [d.label, d.label, a.label, b.label, i.label, c.label],
               [a.label, a.label, d.label, d.label, c.label, c.label],
               [b.label, b.label, b.label, b.label, d.label, c.label]], 
               dtype='uint8')
	
    # define adjacency
    adj = c4

    # build MCT
    mct = MCT()
    root = mct.build(F, a.label, ordering, adj)

    # write MCT in dot format
    gg = pydot.Dot(graph_type='digraph')
    write_graph(gg, root)
    gg.write("mct_fig1.dot")


test_fig1()