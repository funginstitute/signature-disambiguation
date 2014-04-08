import numpy as np
from itertools import count
from collections import defaultdict

linked = defaultdict(set)

def get_neighbors(i,j):
    return [(i-1,j-1),(i-1,j),(i-1,j+1),
            (i,j-1),(i,j+1),
            (i+1,j-1),(i-1,j),(i+1,j+1)]

def setfind(l):
    root = min(linked[l])
    if root == l:
        return l
    else:
        return setfind(root)

def get_connectedcomponents(data):
    shape = data.shape
    # pad image with 0s on every side
    data = np.pad(data,(1,),mode='constant',constant_values=(0,))
    labels = np.zeros(data.shape,dtype=np.int)
    label = count()
    label.next()
    # first pass
    for i in range(1,shape[0]+1): # row
        for j in range(1,shape[1]+1): # column
            # is West neighbor value same as my value?
            current_pixel = data[i][j]
            if current_pixel != 0:
                neighbors = map(lambda x: data[x[0]][x[1]], get_neighbors(i,j))
                if not any(filter(lambda x: x == current_pixel, neighbors)): # if no neighbors have my current pixel value
                    next_label = label.next()
                    linked[next_label] = set([next_label])
                    labels[i][j] = next_label
                else:
                    neighbor_labels = map(lambda x: labels[x[0]][x[1]], get_neighbors(i,j))
                    nonzeros = filter(lambda x: x > 0, neighbor_labels) # TODO: do we want nonzero min?
                    min_label = min(nonzeros) if nonzeros else 0
                    if min_label == 0:
                        min_label = label.next()
                        for x in get_neighbors(i,j):
                            if data[x[0]][x[1]] == current_pixel:
                                labels[x[0]][x[1]] = min_label
                    else:
                        labels[i][j] = min_label
                        for nlabel in nonzeros:
                            linked[nlabel] = linked[nlabel].union(set(nonzeros))

    # second pass
    for i in range(1,shape[0]+1): # row
        for j in range(1,shape[1]+1): # column
            if data[i][j] != 0:
                l = labels[i][j]
                labels[i][j] = setfind(l)
    return labels[1:-1,1:-1] # remove padding

if __name__ == '__main__':
    test_im = np.array(
     [
      [0,0,0,0,1,0,0,0,0],
      [0,1,0,1,1,0,0,0,1],
      [1,0,0,1,0,0,0,0,1],
      [1,1,0,1,1,0,0,1,0],
      [0,1,1,0,1,0,0,0,0],
      [0,1,1,1,0,0,0,1,0]
      ]
    )

    print test_im
    labels = get_connectedcomponents(test_im)
    print labels
