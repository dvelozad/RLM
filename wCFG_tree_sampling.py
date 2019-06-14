import numpy as np
import os

prob = 0.52
N_trees = 200
N_term_MAX = 4000
N_grammars = 120
N_prom = 20
p = prob
for n_grammar in range(N_grammars):
    directory = 'samples/trees/tree_samples_p.'+str(p)+'_grammar.'+str(n_grammar)
    if not os.path.exists('samples'):
        os.makedirs('samples')
    if not os.path.exists('samples/trees'):
        os.makedirs('samples/trees')
    if not os.path.exists(directory):
        os.makedirs(directory)

    for N_t in range(N_trees):
        p = prob

        tree = np.array([1])
        tree_index = np.array([[0,0,0]])
        weight_index = []

        shell = 1
        tree_index = np.append(tree_index,[[shell,1,0]],axis=0)
        N_no_term=1
        N_term=0

        N_no_term_temp=0
        N_term_temp=0

        while N_no_term != 0:
            N_no_term_temp=0
            shell+=1
            
            #print tree
            tree_temp = np.array([])
            weight_temp=[]
            
            for i in tree:
                if i == 1:
                    if np.random.rand() < (1.-p):
                        N_no_term_temp+=2
                        tree_temp = np.append(tree_temp,[1,1])
                        weight_temp.append(('M'))
                    else:
                        N_term_temp+=1
                        tree_temp = np.append(tree_temp,[0])
                        weight_temp.append(('O'))
                else:
                    tree_temp = np.append(tree_temp,[0])
                    weight_temp.append(('X'))

            weight_index.append(weight_temp)

            N_no_term=N_no_term_temp
            N_term=N_term_temp
            tree_index=np.append(tree_index,[[shell,N_no_term,N_term]],axis=0)

            tree=tree_temp
            
            #print weight_temp

            if N_no_term == 0:
                True
                #print tree
            if N_term == N_prom:
                p = 0.98
            if N_term >= N_term_MAX:
                break
        np.save(directory+'/tree_No.'+str(N_t),np.array(weight_index,dtype=object))
        #print weight_index
        #print '__________________________________________-'
    print n_grammar
    