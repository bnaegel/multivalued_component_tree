import numpy as np


# class Ordering
# This provides an interface for label comparisons in O(1) time

class Ordering:

	# FUNCTION : __init__
	# DESC : constructor for Ordering
	# INPUT : none
	# OUTPUT : none
	# PRECONDITION : none
	# POSTCONDITION : none
	def __init__(self, label_root,labels):
		
		self.root=label_root
		self.labels=labels
		self.values = None	# values
		self.order = None	# contains all ordering relations on labels in the form of an adjacency matrix

		# init parent array
		self.parent = np.full(len(self.labels),0)

		for i in labels:
			self.parent[i.label]=i.father.label


	def __repr__(self):
		res= "Values : " + str(self.values) + "\nOrder : " + str(self.order)
		return res

	# FUNCTION : ilt
	# DESC : Provides an O(1) comparison between two labels (criterion is <)
	# INPUT :
	#	- a b : labels to compare
	# OUTPUT :
	#	- True is a < b; false otherwise
	# PRECONDITION :
	#	- a and b should be label indices
	# POSTCONDITION : none
	def ilt(self, a, b):

		if self.order[a][b] == 1:

			return True
		else:
			return False

	# FUNCTION : prec_of_label
	# DESC : Finds the predecessor of a given label
	# INPUT :
	# 	- h : label
	# OUTPUT :
	#	- a label predecessor of h
	# PRECONDITION :
	#	- h should be a label (integer in that case)
	# POSTCONDITION : none
	# returns the predecessor of a label h (in the real space not the restricted number of nodes created)
	def prec_of_label(self, h):

		return self.parent[h]




	# FUNCTION : is_comparable
	# DESC : Indicates whether two labels are comparable
	# INPUT :
	# 	- a b : labels
	# OUTPUT :
	# 	- True if the two given labels are comparable; false otherwise
	# PRECONDITION :
	#	- a and b should be labels
	# POSTCONDITION : none
	def is_comparable(self, a, b):

		return a == b or self.ilt(a, b) or self.ilt(b, a)

	# FUNCTION : inf
	# DESC : Returns the lower bound of a and b (closest common ancestor)
	# INPUT : 
	#	- a b : labels
	# OUTPUT : 
	#	- a label being the closest common ancestor to both a and b
	# PRECONDITION :
	#	- a and b should be labels
	# POSTCONDITION : none
	def inf(self, a, b):

		if self.ilt(a, b):

			return a

		elif self.ilt(b, a):
			
			return b

		while not self.ilt(a, b):

			a = self.parent[a]

		return a



	# FUNCTION 	: trans_closure
	# DESC : computes the transitive closure of the order relation on labels
	# INPUT :
	#	- label_root : label used for root of tree 
	# OUTPUT : none
	# PRECONDITION :
	#	- label_root should be a Label_component 
	# POSTCONDITION : none
	# def trans_closure(self):
		
	# 	# number of labels
	# 	nb_labels=self.parent.size

	# 	# adjacency matrix order
	# 	self.order = np.zeros([nb_labels,nb_labels], np.int32)
		
	# 	label_root=nb_labels-1
	# 	for p in range(len(self.parent)) :

	# 		self.order[label_root][p]=1
	# 		self.order[p][label_root]=-1

	# 		par=p
	# 		# propagate through the root
		
	# 		while self.parent[par] != par:
	# 			par=self.parent[par]
	# 			self.order[par][p]=1
	# 			self.order[p][par]=-1				

	def trans_closure(self):

		# transitive closure of the label graph
		# each label is identified with its index
		self.order = []
		self.order = [[0] * len(self.labels) for i in range(0, len(self.labels))]

		self.compute_succ(self.root)

		for l in self.labels:
			for c in l.succ:
				# print l.index,' ',c.index
				self.order[l.label][c.label] = 1
				self.order[c.label][l.label] = -1



	# FUNCTION : compute_succ
	# DESC : recursive function used to compute all the successors of the current node
	# INPUT :
	#	- n : array order (self contained in class)
	# OUTPUT :
	#	- array order
	# PRECONDITION : none
	# POSTCONDITION : none
	def compute_succ(self, n):

		n.succ += n.childs

		for c in n.childs:
			n.succ += self.compute_succ(c)

		return n.succ

