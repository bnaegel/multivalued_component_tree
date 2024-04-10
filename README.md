# Multivalued component-trees (MCT)

This repository contains the code for the paper *New algorithms for multivalued component-trees* by Nicolas Passat, Romain Perrin, Jimmy Francky Randrianasoa, Camille Kurtz, and Benoît Naegel. 

## Installation

The code is written in Python and requires the following libraries:
- numpy
- pydot

## MCT from the image of Figure 1

### Usage

The command :
```bash
python3 mct_fig1.py 
```
will run the code on the image of depicted on <b>Figure 1</b> of the paper and output the multivalued component-tree in dot format in the file `mct_fig1.dot`.
The tree can be visualized using for example the command:
```bash
dot -Tpdf mct_fig1.dot -o mct_fig1.pdf
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
- g: the value of the  node, represented by an integer index based on the following mapping :
    - 0: <font style="color: white; background-color: blue; padding: 3px"> a </font>
    - 1: <font style="color: white; background-color: red; padding: 3px"> b </font>
    - 2: <font style="color: black; background-color: #00FF40; padding: 3px"> c </font>
    - 3: <font style="color: black; background-color: yellow; padding: 3px"> d </font>
    - 4: <font style="color: white; background-color: #318CE7; padding: 3px"> e </font>
    - 5: <font style="color: white; background-color: #C21E56; padding: 5px"> f </font>
    - 6: <font style="color: black; background-color: orange; padding: 3px"> g </font>
    - 7: <font style="color: black; background-color: #FBCEB1; padding: 3px"> h </font>
    - 8: <font style="color: white; background-color: #C04000; padding: 5px"> i </font>

## MCT from the image of Figure 6

### Usage

The command :
```bash
python3 mct_fig6.py 
```
will run the code on the image of depicted on <b>Figure 6</b> of the paper and output the multivalued component-tree in dot format in the file `mct_fig6.dot`.

This example requires a hierarchical order on an enriched set of values. The `bpt_labels_fig6.dot` has been built as described in the <b>Section 5.2: Ordering the enriched value set</b> of the paper. The code is available at <a href="https://github.com/jimmy-randrianasoa/Example_BinaryPartitionTree_ValueSet.git">Example_BinaryPartitionTree_ValueSet</a>.

The MCT can be visualized using for example the command:
```bash
dot -Tpdf mct_fig6.dot -o mct_fig6.pdf
```
which produces a graphical representation of the tree in pdf format.
or using any tiers software that can read dot files.

<img src="figs/Fig6.png"  />

(a) Top: the image. Bottom: set of 9 values. (b) Top: the co-occurrence matrix of the image. Bottom: the set is endowed with an adjacency. (c) Binary partition tree as a hierarchical order on an enriched set of values.

<img src="figs/mct_fig6.png"  />

The produced MCT using the proposed algorithm.
Each node is described by:

- l: the unique identifier of the node
- a: the area (number of pixels) of the node
- g: the value of the  node, represented by an integer index based on the following mapping :
    -  &nbsp; 0: 9
    -  &nbsp; 1: <font style="color: white; background-color: blue; padding: 3px"> 0 </font>
    -  &nbsp; 2: <font style="color: white; background-color: gray; padding: 3px"> 4 </font>
    -  &nbsp; 3:       10
    -  &nbsp; 4: <font style="color: black; background-color: cyan; padding: 3px"> 5 </font>
    -  &nbsp; 5: <font style="color: black; background-color: yellow; padding: 3px"> 8 </font>
    -  &nbsp; 6:       11
    -  &nbsp; 7:       12
    -  &nbsp; 8: <font style="color: white; background-color: green; padding: 3px"> 2 </font>
    -  &nbsp; 9:       13
    - 10: <font style="color: white; background-color: fuchsia; padding: 3px"> 3 </font>
    - 11:       14
    - 12: <font style="color: white; background-color: #318CE7; padding: 3px"> 1 </font>
    - 13:       15
    - 14:<font style="black: white; background-color: orange; padding: 3px"> 7 </font>
    - 15:       16
    - 16: <font style="color: white; background-color: red; padding: 3px"> 6 </font>