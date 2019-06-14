import numpy as np
import os

def alpha_PG(M,O,M_,O_,ed):
    N=len(M[:,0,0])
    T=len(O[0,:])
    M_prom=1./(N**2.)
    O_prom=1./T

    sd=(1./(N**3.))*(np.sum(np.log(M/M_prom)**2.))
    ss=(1./(N*T))*(np.sum(np.log(O/O_prom)**2.))
    J = np.exp(-np.sum(np.log(M_))-np.sum(np.log(O_))+np.sum(np.log(M))+np.sum(np.log(O)))
    #ed=(N**3.)/(2.*sd)
    #es=N*T/(2.*ss)
    es=(N*T)*0.01

    sd_=(1./(N**3.))*(np.sum(np.log(M_/M_prom)**2.))
    ss_=(1./(N*T))*(np.sum(np.log(O_/O_prom)**2.))
    #ed_=(N**3.)/(2.*sd_)
    #es_=N*T/(2.*ss_)
    ed_=ed
    es_=(N*T)*0.01
    return J*np.exp((-es_*ss_-ed_*sd_+es*ss+ed*sd))

N=10
T=27
ed=10000000

N_metropolis=2000
N_samples=120

M = np.ones((N,N,N))
O = np.ones((N,T))
#Normalization
for i in range(N):
        M[i,:,:]/=np.sum(M,axis=(1,2))[i]
for i in range(N):
        O[i,:]/=np.sum(O,axis=1)[i]
M_new = np.copy(M)
O_new = np.copy(O)
#//
#M=np.random.normal(0,1,(N,N,N))
#M = np.abs(M)
#Normalization
#for i in range(N):
#        M[i,:,:]/=np.sum(M,axis=(1,2))[i]

#O=np.random.normal(0,1,(N,T))
#O = np.abs(O)
#Normalization
#for i in range(N):
#        O[i,:]/=np.sum(O,axis=1)[i]



#for i in range(N):
#        for j in range(N):
#                for k in range(N):
#                        M_new[i][j][k] = np.random.normal(M[i][j][k],1.)
#M_new = np.abs(M_new)
#Normalization
#for i in range(N):
#        M_new[i,:,:]/=np.sum(M_new,axis=(1,2))[i]

#for i in range(N):
#        for j in range(T):
#                O_new[i][j] = np.random.normal(O[i][j],1.)
#O_new = np.abs(O_new)
#Normalization
#for i in range(N):
#        O_new[i,:]/=np.sum(O_new,axis=1)[i]

counter = 0

directory = 'samples/grammars/grammar_samples_N.'+str(N)+'_T.'+str(T)+'_ed.'+str(ed)
if not os.path.exists('samples'):
    os.makedirs('samples')
if not os.path.exists('samples/grammars'):
    os.makedirs('samples/grammars')
if not os.path.exists(directory):
    os.makedirs(directory)

for n_step in range(N_metropolis):
        for i in range(N):
                for j in range(N):
                        for k in range(N):
                                M_temp = np.copy(M)
                                m_new_ijk = np.random.normal(M[i][j][k],1.)
                                m_new_ijk = np.abs(m_new_ijk)
                                M_temp[i][j][k] = m_new_ijk
                                if np.random.rand() < alpha_PG(M,O,M_temp,O,ed):
                                        M_new[i][j][k]=m_new_ijk
        for i in range(N):
                for j in range(T):
                        O_temp = np.copy(O)
                        o_new_ijk = np.random.normal(O[i][j],1.)
                        o_new_ijk = np.abs(o_new_ijk)
                        O_temp[i][j] = o_new_ijk

                        if np.random.rand() < alpha_PG(M,O,M,O_temp,ed):
                                O_new[i][j]=o_new_ijk
        #Normalization
        for i in range(N):
                M_new[i,:,:]/=np.sum(M_new,axis=(1,2))[i]
        #Normalization
        for i in range(N):
                O_new[i,:]/=np.sum(O_new,axis=1)[i]

        M = np.copy(M_new)
        O = np.copy(O_new)

        if n_step >= N_metropolis-500:
                np.save(directory+'/wCFG_N.'+str(N)+'_T.'+str(T)+'_ed.'+str(ed)+'_sample.'+str(counter)+'_M',M)
                np.save(directory+'/wCFG_N.'+str(N)+'_T.'+str(T)+'_ed.'+str(ed)+'_sample.'+str(counter)+'_O',O)
                counter += 1
        if counter == N_samples:
                break
        print n_step
#Fill the missing samples
if counter != N_samples:
        print 'Filling...'
        for i in range(counter,N_samples):
                        np.save(directory+'/wCFG_N.'+str(N)+'_T.'+str(T)+'_ed.'+str(ed)+'_sample.'+str(counter)+'_M',M)
                        np.save(directory+'/wCFG_N.'+str(N)+'_T.'+str(T)+'_ed.'+str(ed)+'_sample.'+str(counter)+'_O',O)
                        counter += 1
