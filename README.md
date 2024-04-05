# Multivalued component-trees

This repository contains the code for the paper "New algorithms for multivalued component-trees" by Nicolas Passat, Romain Perrin, Jimmy Francy Randrianasoa, Camille Kurtz, and Benoît Naegel. The paper is available at ...

## Installation

The code is written in Python and requires the following libraries:
- numpy
- scipy
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



