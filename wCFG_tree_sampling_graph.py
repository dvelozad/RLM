import numpy as np
from igraph import *

p = 0.5

tree = [(1,0)]
tree_index = np.array([[0,0,0]])
weight_index = np.array([])


shell = 1
tree_index = np.append(tree_index,[[shell,1,0]],axis=0)


N_no_term=1
N_term=0

N_term_MAX = 2000

N_no_term_temp=0
N_term_temp=0

node_number=0
node_number_temp=-1

tree_graph = []

while N_no_term != 0:
    N_no_term_temp=0
    shell+=1
    print tree
    
    tree_temp = []
    weight_index = np.array([])
    
    for i in tree:
        node_number_temp+=1
        if i[0] == 1:
            if np.random.uniform() < (1.-p):
                node_number+=1

                N_no_term_temp+=2
                tree_temp.append((1,node_number))
                tree_temp.append((1,node_number+1))

                tree_graph.append((node_number_temp,node_number))
                tree_graph.append((node_number_temp,node_number+1))

                weight_index = np.append(weight_index,['M'])
                node_number+=1
            else:
                node_number+=1
                N_term_temp+=1
                tree_temp.append((0,node_number))
                tree_graph.append((node_number_temp,node_number))
                weight_index = np.append(weight_index,['O'])
        else:
            node_number+=1
            tree_temp.append((0,node_number))
            weight_index = np.append(weight_index,['O'])

    #print weight_index

    N_no_term=N_no_term_temp
    N_term=N_term_temp
    tree_index=np.append(tree_index,[[shell,N_no_term,N_term]],axis=0)

    tree=tree_temp

    if N_no_term == 0:
        print tree
    if N_term >= N_term_MAX:
        break

print '_______________________________________________________________________'
print tree_index
print '_______________________________________________________________________'
print tree_graph
#print tree_index

g = Graph(edges=tree_graph)
plot(g,layout=g.layout('rt',root=[0]),bbox=(5000,4000))