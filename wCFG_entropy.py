import numpy as np
from scipy.special import digamma, factorial
from scipy.misc import derivative
import matplotlib.pyplot as plt

ed_=[1e-7,1e-6,1e-5,1e-4,1e-3,1e-2,1e-1,1,100,1000,10000,100000,1000000,10000000,100000000,1000000000,10000000000,100000000000]
#ed_=[1e-7,1e-6,1e-5,1e-4,10000,100000,1000000,10000000]
#N = 20
T = 27

Num_grammars = 80

counter = 0
for N in [10,20]:
        Hs_k1 = []
        Hd_k1 = []
        Hs_bar_k1 = []
        Hd_bar_k1 = []
        Hs_k2 = []
        Hd_k2 = []
        Hs_bar_k2 = []
        Hd_bar_k2 = []
        for ed in ed_:
                entropy_sigma_k1 = []
                entropy_os_k1 = []
                entropy_sigma_k2 = []
                entropy_os_k2 = []        
                #k = 1
                for grammar in range(Num_grammars):
                        directory = 'samples/sentences/sentence_samples_ed.'+str(ed)+'/sentence_samples_N.'+str(N)

                        N_sigma = np.load(directory+'/repeat_sigma_k.1_sentence_grammar.'+str(grammar)+'.npy')
                        N_o_ = np.load(directory+'/repeat_os_k.1_sentence_grammar.'+str(grammar)+'.npy')
                        #lenght_sg_o = np.load(directory+'/lenght_sigma_o_grammar.'+str(grammar)+'.npy')

                        sum_sigma = 0.
                        for i in range(N):
                                n_i = N_sigma[i]
                                N_sig = np.sum(N_sigma)
                                if N_sigma[i] != 0:
                                        sum_sigma += (n_i/N_sig)*(np.log(N_sig) - digamma(n_i) - (1./((n_i)*(n_i+1)))*(-1.)**(n_i))
                        entropy_sigma_k1.append(sum_sigma / np.log(N))
                        sum_os = 0.
                        for i in range(T):
                                n_i = N_o_[i]
                                N_o = np.sum(N_o_)
                                if N_o_[i] != 0:
                                        sum_os += (n_i/N_o)*(np.log(N_o) - digamma(n_i) - (1./((n_i)*(n_i+1)))*(-1.)**(n_i))
                        entropy_os_k1.append(sum_os / np.log(T))
                #k = 2
                for grammar in range(Num_grammars):
                        N_test = np.load(directory+'/repeat_sigma_k.1_sentence_grammar.'+str(grammar)+'.npy')
                        directory = 'samples/sentences/sentence_samples_ed.'+str(ed)+'/sentence_samples_N.'+str(N)
                        N_sigma = np.load(directory+'/repeat_sigma_k.2_sentence_grammar.'+str(grammar)+'.npy')
                        N_o_ = np.load(directory+'/repeat_os_k.2_sentence_grammar.'+str(grammar)+'.npy')
                        #lenght_sg_o = np.load(directory+'/lenght_sigma_o_grammar.'+str(grammar)+'.npy')

                        sum_sigma = 0.
                        for i in range(N):
                                for j in range(N):
                                        n_i = N_sigma[i][j]
                                        N_sig = np.sum(N_sigma) +1.
                                        #N_sig = np.sum(N_test)
                                        if N_sigma[i][j] != 0:
                                                sum_sigma += (n_i/N_sig)*(np.log(N_sig) - digamma(n_i) - (1./((n_i)*(n_i+1)))*(-1.)**(n_i))
                        entropy_sigma_k2.append(0.5*sum_sigma / np.log(N))
                        sum_os = 0.
                        for i in range(T):
                                for j in range(T):
                                        n_i = N_o_[i][j]
                                        N_o = np.sum(N_o_) + 1.
                                        if N_o_[i][j] != 0:
                                                sum_os += (n_i/N_o)*(np.log(N_o) - digamma(n_i) - (1./((n_i)*(n_i+1)))*(-1.)**(n_i))
                        entropy_os_k2.append(0.5*sum_os / np.log(T))

                #print np.mean(np.array(entropy_sigma))
                #print np.mean(np.array(entropy_os))

                entropy_sigma_k1 = np.unique(np.sort(np.array(entropy_sigma_k1)))
                entropy_os_k1 = np.unique(np.sort(np.array(entropy_os_k1)))
                entropy_sigma_k2 = np.unique(np.sort(np.array(entropy_sigma_k2)))
                entropy_os_k2 = np.unique(np.sort(np.array(entropy_os_k2)))
                
                #entropy_sigma = np.unique(entropy_sigma)
                #entropy_os = np.unique(entropy_os)

                #print entropy_sigma[int(len(entropy_sigma)/2.)]
                #print '__________________________________________'
                #print entropy_os[int(len(entropy_os)/2.)]

                sigma_20 = 0
                sigma_80 = 0
                os_20 = 0
                os_80 = 0

                Hs_prom_k1 = np.mean(entropy_sigma_k1)
                Hd_prom_k1 = np.mean(entropy_os_k1)

                Hs_prom_k2 = np.mean(entropy_sigma_k2)
                Hd_prom_k2 = np.mean(entropy_os_k2)


                for i in range(len(entropy_sigma_k1)):
                        if i == int(len(entropy_sigma_k1)*0.3):
                                sigma_20 = entropy_sigma_k1[i]
                        elif i == int(len(entropy_sigma_k1)*0.7):
                                sigma_80 = entropy_sigma_k1[i]
                                #print entropy_sigma[i]
                print np.mean(entropy_sigma_k1)
                print sigma_80 - sigma_20
                print '__________________________________________'

                for i in range(len(entropy_os_k1)):
                        if i == int(len(entropy_os_k1)*0.3):
                                os_20 = entropy_os_k1[i]
                        elif i == int(len(entropy_os_k1)*0.7):
                                os_80 = entropy_os_k1[i]
                #print np.mean(entropy_os_k1)
                #print os_80 - os_20

                Hs_k1.append(Hs_prom_k1)
                Hd_k1.append(Hd_prom_k1)
                Hs_bar_k1.append(sigma_80 - sigma_20)
                Hd_bar_k1.append(os_80 - os_20)



                for i in range(len(entropy_sigma_k2)):
                        if i == int(len(entropy_sigma_k2)*0.3):
                                sigma_20 = entropy_sigma_k2[i]
                        elif i == int(len(entropy_sigma_k2)*0.7):
                                sigma_80 = entropy_sigma_k2[i]

                print np.mean(entropy_sigma_k2)
                print sigma_80 - sigma_20
                print '----------------------------------------------'

                for i in range(len(entropy_os_k2)):
                        if i == int(len(entropy_os_k2)*0.3):
                                os_20 = entropy_os_k2[i]
                        elif i == int(len(entropy_os_k2)*0.7):
                                os_80 = entropy_os_k2[i]

                Hs_k2.append(Hs_prom_k2)
                Hd_k2.append(Hd_prom_k2)
                Hs_bar_k2.append(sigma_80 - sigma_20)
                Hd_bar_k2.append(os_80 - os_20)

        ed_d=np.array(ed_)

        s1= open("data_"+str(N)+"_Hs_k1.txt","w+")
        for i in range(len(ed_)):
                s1.write(str((ed_[i]+counter*0.5*ed_d[i])*((np.log(N))**2.)/((N)**3.))+'\t'+str(Hs_k1[i])+'\t'+str(Hs_bar_k1[i])+'\n')
        s2= open("data_"+str(N)+"_Hs_k2.txt","w+")
        for i in range(len(ed_)):
                s2.write(str((ed_[i]+counter*0.5*ed_d[i])*((np.log(N))**2.)/((N)**3.))+'\t'+str(Hs_k2[i])+'\t'+str(Hs_bar_k2[i])+'\n')
        d1= open("data_"+str(N)+"_Hd_k1.txt","w+")
        for i in range(len(ed_)):
                d1.write(str((ed_[i]+counter*0.5*ed_d[i])*((np.log(N))**2.)/((N)**3.))+'\t'+str(Hd_k1[i])+'\t'+str(Hd_bar_k1[i])+'\n')
        d2= open("data_"+str(N)+"_Hd_k2.txt","w+")
        for i in range(len(ed_)):
                d2.write(str((ed_[i]+counter*0.5*ed_d[i])*((np.log(N))**2.)/((N)**3.))+'\t'+str(Hd_k2[i])+'\t'+str(Hd_bar_k2[i])+'\n')
        s1.close()
        s2.close()
        d1.close()
        d2.close()

        plt.errorbar(ed_+counter*0.5*ed_d,Hd_k1,yerr=Hd_bar_k1)
        plt.xscale('log')
        plt.errorbar(ed_+counter*0.5*ed_d,Hd_k2,yerr=Hd_bar_k2)
        plt.xscale('log')
        counter += 1

plt.show()