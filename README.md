# Multivalued component-trees

This repository contains the code for the paper *New algorithms for multivalued component-trees* by Nicolas Passat, Romain Perrin, Jimmy Francy Randrianasoa, Camille Kurtz, and Benoît Naegel. 

## Installation

The code is written in Python and requires the following libraries:
- numpy
- pydot 

## Usage

The command :
```bash
python3 main.py 
```
will run the code on the image of depicted on Figure 1 of the paper and output the multivalued component-tree in dot format in the file `output.dot`.
The tree can be visualized using for example the command:
```bash
dot -Tpdf output.dot -o output.pdf
```
which produces a graphical representation of the tree in pdf format.
or using any tiers software that can read dot files.

<img src="figs/Fig1.png"  />

(a) the hierarchical ordering of labels, (b) the adjacency graph, and (c) the input image F

<img src="figs/Fig2.png"  />
(a) the threshold sets of F, (b) the multivalued component-tree of F

<img src="figs/mct_fig1.png"  />
The produced MCT using the proposed algorithm.
Each node is described by:

- l: the unique identifier of the node
- a: the area (number of pixels) of the node
- g: the value of the  node

