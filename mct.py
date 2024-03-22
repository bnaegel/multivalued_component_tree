from ordering import Ordering
from node import Node_component

# class MCT 
# This class provides a generic algorithm to build a multivalued component tree (MCT) based on a modification of Salembier's algorithm for max-tree

class MCT:
    # class variables (queue status)
    ACTIVE = -1
    INQUEUE = -2

    # FUNCTION : __init__
    # DESC : constructor for Salembier
    # INPUT : none
    # OUTPUT : none
    # PRECONDITION : none
    # POSTCONDITION : none
    def __init__(self):
        # MCT variables
        self.dx = 0
        self.dy = 0
        self.I = []
        self.nb_pixels = 0
        self.hmin = 0
        self.in_queue = []
        self.processed = []
        self.status = []
        self.node_at_level = {}
        self.number_nodes = {}
        self.hq = {}
        self.index = {}
        self.xmin = 0
        self.pos = 0

	# FUNCTION : build
	# DESC : initialisation for Salembier's MCT computation algorithm
	# INPUT :
	#	- I : index image
	#	- label_root_index : index of label of the MCT root
	#	- ordering : instance of class Ordering defining an order on arbitrary labels
	#	- adj : adjacency function (see c4 and c8 functions in test.py)
	# OUTPUT :
	#	- root of the computed MCT
	# PRECONDITION :
	#	- I should be an index image
	#	- label_root_index should be a integer
	#	- ordering should be an instance of class LabelOrdering
	#	- ordering should already have called its compute_labels function
	#	- adj should be a function returning point coordinates such as ((-1,-1) (-1,1) (1,-1) (1,1))
	# POSTCONDITION : none
    def build(self, I, label_root_index, ordering: Ordering, adj)->Node_component:

        self.dx = I.shape[1]
        self.dy = I.shape[0]
        self.I = I.flatten()
        self.nb_pixels = I.size
        self.hmin = label_root_index
        self.in_queue = [False] * self.nb_pixels
        self.processed = [False] * self.nb_pixels
        self.status = [self.ACTIVE] * self.nb_pixels

        for l in range(len(ordering.labels)):
            self.node_at_level[l] = False
            self.number_nodes[l] = 0
            self.hq[l] = []
            self.index[l] = []

        # hmin represents a virtual value
        # Initialization of the flooding: we put in the queue an arbitrary image pixel (0) with value hmin 
        self.xmin=0
        self.in_queue[self.xmin] = True

        root = Node_component(self.hmin)

        self.index[self.hmin].append(root)

        self.node_at_level[self.hmin] = True

        self.hq[self.hmin].append(self.xmin)

        self.flood(self.hmin, label_root_index, ordering, adj)

        self.I = self.I.reshape((self.dy, self.dx))

        return root

	# FUNCTION : flood
	# DESC : recursive flooding function used to build the MCT - fast version
	# INPUT :
	#	- h : current index
	#	- label_root_index : index of root label
	#	- ordering : instance of class LabelOrdering (from label_ordering.py) defining an order on arbitrary labels
	#	- adj : adjacency function (see c4 and c8 functions in test.py)
	# OUTPUT : none
	# PRECONDITION :
	#	- h should be an index (integer)
	#	- label_root_index should be an integer
	#	- ordering should be an instance of class LabelOrdering
	#	- ordering should already have called its compute_labels function
	#	- adj should be a function returning point coordinates such as ((-1,-1) (-1,1) (1,-1) (1,1))
	# POSTCONDITION : none
    def flood(self, h, label_root_index, ordering, adj):

        self.pos = self.pos + 5

        while self.hq[h]:

            p = self.hq[h].pop(0)

            if self.I[p] != h:	# fictitious pixel

                if self.status[p] == self.ACTIVE:	# point has not been processed yet
                    m = self.I[p]
                    self.hq[m].append(p)
                    self.status[p] = self.INQUEUE

                    while ordering.ilt(h, m):
                        m = self.flood(m, label_root_index, ordering, adj)

            else:

                self.status[p] = self.number_nodes[h]
                if len(self.index[h]) <= self.status[p]:
                    n = Node_component(h)
                    self.index[h].append(n)

                # area incr
                # add pixel to current node at level h
                self.index[h][self.status[p]].area += 1
                self.index[h][self.status[p]].pixels.append(p)

                # 8 neighbourhood
                for (i, j) in adj:
                    (x, y) = (p % self.dx + i, p // self.dx + j)

                    if x >= 0 and x < self.dx and y >= 0 and y < self.dy:
                        q = y * self.dx + x
                        m = self.I[q]

                        if self.status[q] == self.ACTIVE:

                            if not ordering.is_comparable(h, m):
                                binf = ordering.inf(h, m)
                                self.hq[binf].append(q)

                                if len(self.index[binf]) <= self.number_nodes[binf]:
                                    n = Node_component(binf)
                                    self.index[binf].append(n)

                                self.node_at_level[binf] = True

                            else:
                                self.hq[m].append(q)
                                self.status[q] = self.INQUEUE

                                # create the node at level m is not exists
                                if len(self.index[m]) <= self.number_nodes[m]:
                                    n = Node_component(m)
                                    self.index[m].append(n)

                                self.node_at_level[m] = True

                            while ordering.ilt(h, m):
                                m = self.flood(m, label_root_index, ordering, adj)

        # retrieve predecessor of h
        m = ordering.prec_of_label(h)

        if m != h:

            while not self.node_at_level[m] and ordering.prec_of_label(m) != m:
                m = ordering.prec_of_label(m)

            # father - child relation
            if ordering.ilt(label_root_index, m):
                self.index[h][self.number_nodes[h]].father = self.index[m][self.number_nodes[m]]
                self.index[m][self.number_nodes[m]].childs.append(self.index[h][self.number_nodes[h]])
                self.index[m][self.number_nodes[m]].area += self.index[h][self.number_nodes[h]].area

            else:
                if m == label_root_index:
                    self.index[m][0].father = self.index[m][0]
                    self.index[m][self.number_nodes[m]].childs.append(self.index[h][self.number_nodes[h]])
                    self.index[m][self.number_nodes[m]].area += self.index[h][self.number_nodes[h]].area

            self.number_nodes[h] += 1
            self.node_at_level[h] = False
            self.pos = self.pos - 5

        return m

    #------------------------------------------------------------------------------
    # Post-processing: fictitious node removal (MCT)
    #------------------------------------------------------------------------------

    # FUNCTION : remove_fictitious_nodes
    # DESC : removes fictitious nodes in the MCT (nodes with an area of 0)
    # INPUT :
    #	- n : root node of MCT
    # OUTPUT : none (tree pruning)
    # PRECONDITION : 
    #	- root should be a Node_component
    # POSTCONDITION : none 
    def remove_fictitious_nodes(self, n: Node_component):

        childs = list(n.childs)

        for c in childs:

            # in case the link child --> father does not exist then it is added BN ???
            c.father = n

            self.remove_fictitious_nodes(c)

            if len(c.pixels) == 0:

                n.childs.remove(c)
                n.childs += c.childs

                # updating the new father as the current father is removed
                # the new father is the father of the current father of the node
                for cc in c.childs:
                    cc.father = n


   
    

