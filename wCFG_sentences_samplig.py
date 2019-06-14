import numpy as np
import os

#grammar_sample = 80
#tree_sample = 60
ed = 10000000
N = 10
T = 27
p = 0.52

Num_grammars = 80
Num_trees = 50

same_tree = 0
print_tree = False

for grammar_sample in range(Num_grammars):
    sigma = []
    o_ = []
    for tree_sample in range(Num_trees):
        tree = np.load('samples/trees/tree_samples_p.'+str(p)+'_grammar.'+str((1-same_tree)*grammar_sample)+'/tree_No.'+str(tree_sample)+'.npy')
        rules = np.load('samples/trees/tree_samples_p.'+str(p)+'_grammar.'+str((1-same_tree)*grammar_sample)+'/tree_No.'+str(tree_sample)+'.npy')

        M = np.load('samples/grammars/grammar_samples_N.'+str(N)+'_T.'+str(T)+'_ed.'+str(ed)+'/wCFG_N.'+str(N)+'_T.'+str(T)+'_ed.'+str(ed)+'_sample.'+str(grammar_sample)+'_M.npy')
        O = np.load('samples/grammars/grammar_samples_N.'+str(N)+'_T.'+str(T)+'_ed.'+str(ed)+'/wCFG_N.'+str(N)+'_T.'+str(T)+'_ed.'+str(ed)+'_sample.'+str(grammar_sample)+'_O.npy')

        if print_tree == True:
            for i in range(len(tree)):
                print tree[i]

        S_0 = 0

        index = []
        index_temp= []

        for n in range(len(tree)):
            shell = tree[n]
            pseudo_node = 0
            for node in range(len(shell)):
                if shell[node] == 'M':
                    if n == 0:
                        a = S_0
                    else:
                        a = index[pseudo_node]
                        pseudo_node+=1
                    b = np.random.randint(0,N)
                    c = np.random.randint(0,N)
                    random = np.amax(M[a,:,:])*np.random.rand()
                    for k in range(100000):
                        #if M[a][b][c] > np.random.uniform(0.,1./(N**2.)):
                        if (1**2.)*M[a][b][c] >= random:
                            rules[n][node]=(a,b,c)
                            index_temp.append(b)
                            index_temp.append(c)
                            break
                        else:
                            b = np.random.randint(0,N)
                            c = np.random.randint(0,N)
                elif shell[node] == 'O':
                    if n == 0:
                        d = S_0
                    else:
                        d = index[pseudo_node]
                        pseudo_node+=1
                    B = np.random.randint(0,T)
                    random = np.amax(O[d,:])*np.random.rand()
                    for k in range(100000):
                        #if O[d][B] > np.random.uniform(0.,1./(T)):
                        if (1)*O[d][B] >= random:
                            rules[n][node]=(d,B+N) #se le suma +10 para distinguir los puntos terminales(27) de los no terminales(10)
                            break
                        else:
                            B = np.random.randint(0,T)
            index = index_temp
            index_temp=[]

        if print_tree == True:
            for i in range(len(tree)):
                print rules[i]

        #Repeticion de las reglas M, O y de los {sigmas} y {o's}
        N = len(M)
        T = len(O[0,:])

        pi = np.zeros((N,N,N))
        rho = np.zeros((N,T))

        for shell in rules:
            for node in shell:
                if len(node) == 3:
                    sigma.append(node[0])
                    pi[node[0]][node[1]][node[2]]+=1
                elif len(node) == 2:
                    sigma.append(node[0])
                    o_.append(node[1])
                    rho[node[0]][node[1]-N]+=1

        directory = 'samples/sentences/sentence_samples_ed.'+str(ed)+'/sentence_samples_N.'+str(N)
        if not os.path.exists('samples'):
            os.makedirs('samples')
        if not os.path.exists('samples/sentences'):
            os.makedirs('samples/sentences')
        if not os.path.exists(directory):
            os.makedirs(directory)

        repeat_sigma = np.zeros(N)
        repeat_o_ = np.zeros(T)

        for i in sigma:
            repeat_sigma[i] += 1
        for j in o_:
            repeat_o_[j-N] += 1
    
        #np.save(directory+'/pi_sentence_tree.'+str(tree_sample),pi)
        #np.save(directory+'/rho_sentence_tree.'+str(tree_sample),rho)
        #np.save(directory+'/sigma_sentence_tree.'+str(tree_sample),np.unique(np.array(sigma)))
        #np.save(directory+'/os_sentence_tree.'+str(tree_sample),np.unique(np.array(o_)))
    np.save(directory+'/repeat_sigma_sentence_grammar.'+str(grammar_sample),np.array(repeat_sigma))
    np.save(directory+'/repeat_os_sentence_grammar.'+str(grammar_sample),np.array(repeat_o_))
    np.save(directory+'/lenght_sigma_o_grammar.'+str(grammar_sample),np.array((len(sigma),len(o_))))
    #print np.sum(repeat_sigma)
    print grammar_sample