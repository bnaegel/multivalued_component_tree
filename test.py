import cv2
import sys
from mct import *
from ordering import *
import pydot
import numpy as np
import scipy as sp
from scipy import ndimage
from node import *
import matplotlib.pyplot as plt



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


def rec_attribute_filter(I, node, value,area1):
    if node.area < area1:
        node.value=value
    else :
        node.value=node.original_value

    for c in node.childs:
        rec_attribute_filter(I, c, node.value,area1)
        
    for p in node.pixels:
        I[p] = node.value

	
def attribute_filter(I, root, area):
    
    If = I.flatten()
    v = root.original_value # virtual root

    # print("index value of root :  ",v)

    # for each subtree
    for c in root.childs:
        rec_attribute_filter(If, c, v, area)
        
    If = If.reshape(I.shape)
    return If

# convert the hierarchical ordering coded in a data structure "parent" into a graph based on LabelNode class
def compute_hierarchical_graph(parent):
    label_nodes=[]
    Node_label.label=0
    
    # create one node for each index / label
    for i in range(len(parent)):
        label_nodes.append(Node_label(i))
   
    # index of g_root in nodes
    # last node is the root
    root_idx=len(label_nodes)-1
    g_root=label_nodes[root_idx]

    # For each index / label
    for p in range(len(parent)): 
        # value has no parent : it is the root
        if p == parent[p]:
            print("Found root:" + str(g_root.value))
            g_root.father = g_root
        else:
            label_nodes[p].father = label_nodes[parent[p]]
            label_nodes[parent[p]].add_child(label_nodes[p])

    return g_root,root_idx,label_nodes

# reconstruction of an RGB image from a MCT
# return reconstructed image
def fill_tree(image,root, nbin):
    dx=image.shape[1]
    dy=image.shape[0]
    print(dx,dy)
    result=np.full(image.shape,0,dtype='uint8')
  #  result=result.flatten()
    fifo=[]
    fifo.append(root)
    while len(fifo)!=0:
        node=fifo.pop(0)
        for p in node.pixels:
            # check for fictitious pixel
            if p < dx*dy:
                index=node.original_value
                blue=index//(nbin*nbin)
                green=(index-blue*nbin*nbin)//nbin
                red=(index-blue*nbin*nbin-green*nbin)

                blue=blue*256/nbin
                green=green*256/nbin
                red=red*256/nbin

                x=p%dx
                y=p//dx

                result[y,x,0]=blue
                result[y,x,1]=green
                result[y,x,2]=red

        for n in node.childs:
            fifo.append(n)
           
   # result=result.reshape(image.shape)
    return result

# index image to rgb image
def index_to_value_image(index_image,nbin):
    dx=index_image.shape[1]
    dy=index_image.shape[0]
    # create rgb image
    image=np.zeros([dy,dx,3],dtype='uint8')

    for j in range(image.shape[0]):
        for i in range(image.shape[1]):
            index=index_image[i,j]
            blue=index//(nbin*nbin)
            green=(index-blue*nbin*nbin)//nbin
            red=(index-blue*nbin*nbin-green*nbin)

            blue=blue*256/nbin
            green=green*256/nbin
            red=red*256/nbin

            image[i,j,0]=blue
            image[i,j,1]=green
            image[i,j,2]=red
    return image


# filtering 3D histogram
def filter_histogram3d(h, radius):
    hist_filtered=np.empty(h.shape)
    dx=h.shape[0]
    dy=h.shape[1]
    dz=h.shape[2]

    # uniform kernel of size radius*2+1
    k=np.ones([radius*2+1,radius*2+1,radius*2+1])
    k=k/k.sum()

    h_filtered=ndimage.convolve(h, k , mode='reflect',cval=0.0)
    return h_filtered

def rgb_to_index(v):
    return v[0]*256*256+v[1]*256+v[2]

# I: RGB image
def compute_value_to_index(I: np.array)-> (dict, list):
    value_to_index={}
    index_to_value=[]
    index=0
    dx=I.shape[1]
    dy=I.shape[0]

    for x in range(dx):
        for y in range(dy):
            v=I[x,y]
            v_index=rgb_to_index(v)
            if not v_index in value_to_index:
                value_to_index[v_index]=index
                index+=1
                index_to_value.append(v)

    return value_to_index, index_to_value



# Compute a hierarchial ordering on labels based on histogram density (RGB version)
# first version: link v to the maximal value around a neighborhood d
def compute_density_based_hierarchy_RGB(h:np.ndarray, d:int)-> Ordering:

    ordering=Ordering()
    # h.size + 1 case for the root value
    par=np.full(h.size+1,-1)
    di=h.shape[0]
    dj=h.shape[1]
    dk=h.shape[2]

    for i in range(di):
        print(i)
        for j in range(dj):
            for k in range(dk):
                #print(i)
                v=h[i,j,k]
                lmax=h[i,j,k]
                imax=(i,j,k)
                for l in range(-(d+1),d+1):
                    for m in range(-(d+1),d+1):
                        for n in  range(-(d+1),d+1):
                            i1=i+l
                            j1=j+m
                            k1=k+n
                            
                            if(i1>=0  and i1 < h.shape[0] and j1>=0 and j1 < h.shape[1] and k1 >= 0  and k1 < h.shape[2]):
                                v=h[i1,j1,k1]
                                if(v > lmax):
                                    lmax=v
                                    imax=(i1,j1,k1)
                            
                # if a value has itself as parent, connect it to fictitious root
                index=i*dj*dk+j*dk+k
                imax_index=imax[0]*dj*dk+imax[1]*dk+imax[2]

                if (i,j,k)==imax:				
                    par[index]=h.size
                else :
                    par[index]=imax_index
    # the root has itself as parent
    ordering.root=h.size
    par[ordering.root]=ordering.root
    ordering.parent=par
    return ordering

# BN 2021/09/28
# Compute a hierarchial ordering on labels based on histogram density (RGB version)
# second version: link v to the least greater value around a neighborhood d
def compute_density_based_hierarchy_RGB_v2(h:np.ndarray, d:int)-> Ordering:

    ordering=Ordering()
    # h.size + 1 case for the root value
    par=np.full(h.size+1,-1)
    di=h.shape[0]
    dj=h.shape[1]
    dk=h.shape[2]

    for i in range(di):
        print(i)
        for j in range(dj):
            for k in range(dk):
                #print(i)
                v=h[i,j,k]
                vmin=100000000000
                imin=(i,j,k)
                for l in range(-(d+1),d+1):
                    for m in range(-(d+1),d+1):
                        for n in  range(-(d+1),d+1):
                            i1=i+l
                            j1=j+m
                            k1=k+n
                            
                            if(i1>=0  and i1 < h.shape[0] and j1>=0 and j1 < h.shape[1] and k1 >= 0  and k1 < h.shape[2]):
                                w=h[i1,j1,k1]
                                if(w > v and w < vmin):
                                    vmin=w
                                    imin=(i1,j1,k1)
                            
                # if a value has itself as parent, connect it to fictitious root
                index=i*dj*dk+j*dk+k
                imin_index=imin[0]*dj*dk+imin[1]*dk+imin[2]

                if (i,j,k)==imin:				
                    par[index]=h.size
                else :
                    par[index]=imin_index
    # the root has itself as parent
    ordering.root=h.size
    par[ordering.root]=ordering.root
    ordering.parent=par
    return ordering

def quantize_image(I,nbin):
    quantized_image=np.zeros((I.shape[0], I.shape[1],I.shape[2]), dtype='uint8')
    # construct index_image : each point p has an index value 
    index_image = np.zeros((I.shape[0], I.shape[1]), dtype='uint32')

    # image is quantified in nbin bins
    for i in range(I.shape[0]):
        for j in range(I.shape[1]):
            blue=I[i,j,0]
            green=I[i,j,1]
            red=I[i,j,2]
            # computation of quantized values relatively to the number of bins of histogram
            quantized_blue = int(blue*nbin / 256)
            quantized_green = int(green*nbin / 256)
            quantized_red = int(red*nbin/ 256)
            index=quantized_blue*nbin*nbin+quantized_green*nbin+quantized_red

            index_image[i,j]=index

            quantized_image[i,j,0]=quantized_blue*256/nbin
            quantized_image[i,j,1]=quantized_green*256/nbin
            quantized_image[i,j,2]=quantized_red*256/nbin
    return quantized_image,index_image


def filter_area(area):
    global J,nbin,root
    filtered_image = attribute_filter(J, root, area)
    filtered_image=index_to_value_image(filtered_image, nbin)
    cv2.imshow('image',filtered_image)
    

# check MCT computation on custom labels
def test0():
    return

# density based ordering experimentation on grey-level images
def test1_grey():
    return

J=0
nbin=0
root=0

# density based ordering experimentation on RGB images
def test2_rgb():
    global J,nbin,root

    if(len(sys.argv) != 4):
        print("Usage: ",sys.argv[0], " <image.png> (RGB image) <q> (level of quantification: q=16 for 16 bins for each color)  <area> (area filtering)\n")
        exit(0)
    filename=sys.argv[1]
    quantif=int(sys.argv[2])
    area=int(sys.argv[3])

    # read RGB image
    # warning: open CV format (BGR)
    I= cv2.imread(sys.argv[1])

    print(I.shape)

    # 1 : compute index_to_value and value_to_index
    value_to_index, index_to_value=compute_value_to_index(I)
    print("Check number of different values: ", len(value_to_index), len(index_to_value))

    # compute distribution of points (x,y,v)
    # use bins for (x,y)

    # compute histogram 
    # define bins for histogram computation
    nbin=quantif
    bins=[nbin,nbin,nbin]
    hist = cv2.calcHist([I], [0, 1, 2], None, bins, [0, 256, 0, 256, 0, 256])

    hist_b = cv2.calcHist([I], [0], None, [nbin], [0, 256])
    hist_g = cv2.calcHist([I], [1], None, [nbin], [0, 256])
    hist_r = cv2.calcHist([I], [2], None, [nbin], [0, 256])

    print(hist_b)

    plt.figure()
    plt.subplot(2,3,1)
    plt.plot(hist_b,color='b',)
    plt.subplot(2,3,2)
    plt.plot(hist_g,color='g')
    plt.subplot(2,3,3)
    plt.plot(hist_r,color='r')
    plt.show()

    # exit(1)

    di=hist.shape[0]
    dj=hist.shape[1]
    dk=hist.shape[2]

    assert(nbin==di)
    assert(nbin==dj)
    assert(nbin==dk)

    print("Check histo size: ",hist.size)
    print("Check histo sum: ", hist.sum())

    # filter histogram
    radius=8
    hist_filtered=filter_histogram3d(hist, radius)
    #hist_filtered=hist_filtered.astype('int16')
    print("Check filtered histo sum: ", hist_filtered.sum())
    # print(hist_filtered)
    
    color_coordinates=np.where(hist_filtered>0.0)
    colors=hist_filtered[color_coordinates]
    print(colors.size,colors.shape)

    # plot 3d histogram
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # ax.scatter(color_coordinates[0],color_coordinates[1],color_coordinates[2],c=colors)
    # plt.show()

    d=1 # size of 3D neighborhood in the space of values
    #compute density based hierarchy on values

    ordering=compute_density_based_hierarchy_RGB_v2(hist_filtered,d)

    # computation of transitive closure in the form of adjacency matrix  (for O(1) access) 
    ordering.trans_closure()

    # convert data structure parent into data structure NodeLabel (for visualization only)
    [g_root,root_idx,nodes]=compute_hierarchical_graph(ordering.parent)

    # save the hierarchy / tree of labels / values in dot format for graphical visualization
    gg = pydot.Dot(graph_type='digraph')
    write_graph(gg, g_root)
    gg.write("labels.dot")
    
    # index_image_utility = IndexImage()
    # index_image = index_image_utility.get_index_image_rgb(I, label_ordering.labels, label_ordering.indices, mapping, label_ordering.repr )

    quantized_image,index_image=quantize_image(I,nbin)
    print(quantized_image)
    cv2.imwrite("quantized_image.png",quantized_image)

    adj = c8
    print("Building a multivalued component tree (MCT) using modified Salembier's algorithm")
    mct = MCT()
    # take the mean as value for the root
    mean = cv2.mean(I)
    g_root.value=int(mean[0]*nbin/256)*nbin*nbin+int(mean[1]*nbin/256)*nbin+int(mean[2]*nbin/256)
    print("Label root:",g_root.label)
    print("Value of root:",g_root.value)

    root = mct.build(index_image, g_root.label, ordering, adj)
    mct.remove_fictitious_nodes(root)

    root.original_value=g_root.value

    # gg = pydot.Dot(graph_type='digraph')
    # write_graph(gg, root)
    # gg.write("mct.dot")

    # check that reconstructed image from the tree is equal to the original (or quantized) image
    test=fill_tree(I,root,nbin)

    cv2.imwrite("test.png", test)
    
    J = np.full(index_image.shape, 0,dtype='uint32')

    cv2.namedWindow('image',cv2.WINDOW_NORMAL)
    cv2.createTrackbar('area','image',0,1000,filter_area)

    filtered_image = attribute_filter(J, root, area)
    filtered_image=index_to_value_image(filtered_image, nbin)
    
    while(1):
        k = cv2.waitKey(0) & 0xFF
        if k == 27:
            break

    
    cv2.imwrite("filtered.png", filtered_image)
    # cv2.imshow("figure",filtered_image)
    # cv2.waitKey(0)
    cv2.destroyAllWindows()


test2_rgb()