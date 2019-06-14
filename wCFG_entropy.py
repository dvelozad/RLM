import numpy as np
from scipy.special import digamma, factorial
from scipy.misc import derivative

entropy_sigma = []
entropy_os = []
ed = 100000000

N = 10
T = 27

Num_grammars = 80

for grammar in range(Num_grammars):
        directory = 'samples/sentences/sentence_samples_ed.'+str(ed)+'/sentence_samples_N.'+str(N)

        N_sigma = np.load(directory+'/repeat_sigma_sentence_grammar.'+str(grammar)+'.npy')
        N_o_ = np.load(directory+'/repeat_os_sentence_grammar.'+str(grammar)+'.npy')
        lenght_sg_o = np.load(directory+'/lenght_sigma_o_grammar.'+str(grammar)+'.npy')

        sum_sigma = 0.
        for i in range(N):
                n_i = N_sigma[i]
                N_sig = np.sum(N_sigma)
                if N_sigma[i] != 0:
                        sum_sigma += (n_i/N_sig)*(np.log(N_sig) - digamma(n_i) - (1./((n_i)*(n_i+1)))*(-1.)**(n_i))
        entropy_sigma.append(sum_sigma / np.log(N))
        sum_os = 0.
        for i in range(T):
                n_i = N_o_[i]
                N_o = np.sum(N_o_)
                if N_o_[i] != 0:
                        sum_os += (n_i/N_o)*(np.log(N_o) - digamma(n_i) - (1./((n_i)*(n_i+1)))*(-1.)**(n_i))
        entropy_os.append(sum_os / np.log(T))

#print np.mean(np.array(entropy_sigma))
#print np.mean(np.array(entropy_os))

entropy_sigma = np.sort(np.array(entropy_sigma))
entropy_os = np.sort(np.array(entropy_os))

#entropy_sigma = np.unique(entropy_sigma)
#entropy_os = np.unique(entropy_os)

#print entropy_sigma[int(len(entropy_sigma)/2.)]
#print '__________________________________________'
#print entropy_os[int(len(entropy_os)/2.)]

sigma_20 = 0
sigma_80 = 0
os_20 = 0
os_80 = 0

for i in range(len(entropy_sigma)):
        if i == int(len(entropy_sigma)*0.2):
                sigma_20 = entropy_sigma[i]
        elif i == int(len(entropy_sigma)*0.8):
                sigma_80 = entropy_sigma[i]
                #print entropy_sigma[i]
print np.mean(entropy_sigma)
print sigma_80 - sigma_20
print '__________________________________________'

for i in range(len(entropy_os)):
        if i == int(len(entropy_os)*0.2):
                os_20 = entropy_os[i]
        elif i == int(len(entropy_os)*0.8):
                os_80 = entropy_os[i]
print np.mean(entropy_os)
print os_80 - os_20
 