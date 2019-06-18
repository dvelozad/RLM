import numpy as np
import os

grammar_sample = 80
tree_sample = 60
ed = 0.01
N = 10
T = 27
p = 0.4842

print_tree = True

tree = np.load('samples/trees/tree_samples_P.'+str(p)+'/tree_p.'+str(p)+'_No.'+str(tree_sample)+'.npy')
rules = np.load('samples/trees/tree_samples_P.'+str(p)+'/tree_p.'+str(p)+'_No.'+str(tree_sample)+'.npy')

M = np.load('samples/grammars/grammar_samples_N.'+str(N)+'_T.'+str(T)+'_ed.'+str(ed)+'/wCFG_N.'+str(N)+'_T.'+str(T)+'_ed.'+str(ed)+'_sample.'+str(grammar_sample)+'_M.npy')
O = np.load('samples/grammars/grammar_samples_N.'+str(N)+'_T.'+str(T)+'_ed.'+str(ed)+'/wCFG_N.'+str(N)+'_T.'+str(T)+'_ed.'+str(ed)+'_sample.'+str(grammar_sample)+'_O.npy')

if print_tree == True:
    for i in range(len(tree)):
        print tree[i]

S_0 = np.random.randint(0,9)

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
            b = np .random.randint(0,9)
            c = np.random.randint(0,9)
            for k in range(1000):
                if M[a][b][c] > (np.random.uniform())/(10.*10.):
                    rules[n][node]=(a,b,c)
                    index_temp.append(b)
                    index_temp.append(c)
                    break
                else:
                    b = np.random.randint(0,9)
                    c = np.random.randint(0,9)
        elif shell[node] == 'O':
            if n == 0:
                d = S_0
            else:
                d = index[pseudo_node]
                pseudo_node+=1
            B = np.random.randint(0,26)
            for k in range(1000):
                if O[d][B] > (np.random.uniform())/(10.*27.):
                    rules[n][node]=(d,B+10) #se le suma +10 para distinguir los puntos terminales(27) de los no terminales(10)
                    break
                else:
                    B = np.random.randint(0,26)
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

sigma = []
o_ = []

for shell in rules:
    for node in shell:
        if len(node) == 3:
            sigma.append(node[0])
            pi[node[0]][node[1]][node[2]]+=1
        elif len(node) == 2:
            sigma.append(node[0])
            o_.append(node[1])
            rho[node[0]][node[1]-N]+=1

directory = 'samples/sentences/sentence_samples_grammar.'+str(grammar_sample)
if not os.path.exists('samples'):
    os.makedirs('samples')
if not os.path.exists('samples/sentences'):
    os.makedirs('samples/sentences')
if not os.path.exists(directory):
    os.makedirs(directory)

np.save(directory+'/pi_sentence_tree.'+str(tree_sample),pi)
np.save(directory+'/rho_sentence_tree.'+str(tree_sample),rho)
np.save(directory+'/sigma_sentence_tree.'+str(tree_sample),np.unique(np.array(sigma)))
np.save(directory+'/os_sentence_tree.'+str(tree_sample),np.unique(np.array(o_)))