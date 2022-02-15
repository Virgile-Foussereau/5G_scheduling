from preprocessing import *
from DP import *
import numpy as np

def data(pmax,rmax, M, N): #give values of p and r following a uniform distribution
    d=[]
    for n in range(N):
        for m in range(M):
            p=np.random.randint(1,pmax+1)
            r=np.random.randint(1,rmax+1)
            d.append([p,r,n,r/p])
    d.sort(key= lambda x: x[3])
    return d

def online(pmax,rmax,p,M,N,K): #Online algorithm
    channels=[0 for i in range(N)] #all channels are not used at the begining
    pUser=p/K
    pcurrent=0 #power used
    r=0 #achieved rate
    L=[] #List we will build with the data to compute the offline optimal solution as comparison
    for n in range(N):
        L.append([])
    for k in range(K):
        d=data(pmax,rmax,M,N) #values for the user k+1
        i=0
        for pr in d:
            L[pr[2]].append(pr)
            if channels[pr[2]]==0 and pr[0]+pcurrent<=(k+1)*pUser: #if the channel is not used and the constraint on power is respected we can use this triplet
                channels[pr[2]]=1
                r+=pr[1]
                pcurrent+=pr[0]
    (N,M,K,pmax,L)=preprocessing1((N,M,K,pmax,L))
    (N,M,K,pmax,L)=preprocessing2((N,M,K,pmax,L))
    (N,M,K,pmax,L)=preprocessing3withoutSort((N,M,K,pmax,L))
    return (r,pcurrent,DP(L,pmax)) #return rate achieved, power used, and the result of the offline optial algorithm


def online2(pmax,rmax,p,M,N,K): #Version 2 using the average
    E=rmax/2
    for i in range(pmax):
        E+=1/(i+1)
    E=E/pmax #we have computed the average of rate/power with both following uniform distribution
    channels=[0 for i in range(N)]
    pUser=p/K
    pcurrent=0
    r=0
    L=[]
    for n in range(N):
        L.append([])
    for k in range(K):
        d=data(pmax,rmax,M,N)
        i=0
        for pr in d:
            L[pr[2]].append(pr)
            if channels[pr[2]]==0 and pr[0]+pcurrent<=(k+1)*pUser and pr[1]/pr[0]>=E:
                channels[pr[2]]=1
                r+=pr[1]
                pcurrent+=pr[0]
    (N,M,K,pmax,L)=preprocessing1((N,M,K,pmax,L))
    (N,M,K,pmax,L)=preprocessing2((N,M,K,pmax,L))
    (N,M,K,pmax,L)=preprocessing3withoutSort((N,M,K,pmax,L))
    return (r,pcurrent,DP(L,pmax)) #return rate achieved, power used, and the result of the offline optial algorithm

def testOnline(pmax=50,rmax=100,p=100,M=2,N=4,K=10):
    m1=0
    m2=0
    rm1=0
    rm2=0
    rm3=0
    pm1=0
    pm2=0
    pm3=0
    for i in range(10000): #a lot of tests, it will take a few seconds
        (r1,p1,t1)=online(pmax,rmax,p,M,N,K)
        (r2,p2,t2)=online2(pmax,rmax,p,M,N,K)
        rm1+=r1
        rm2+=r2
        rm3+=t1[0]
        m1+=r1/t1[0]
        m2+=r2/t2[0]
        pm1+=p1
        pm2+=p2
        pm3+=t1[1]
    print("Competitive ratio of online() : "+str(m1/10000))
    print("Competitive ratio of online2() : "+str(m2/10000))
    print("average rate achieved by online() : "+str(rm1/10000))
    print("average power achieved by online2() : "+str(rm2/10000))
    print("average power achieved by DP() : "+str(rm3/10000))
    print("average power used by online() : "+str(pm1/10000))
    print("average power used by online2() : "+str(pm2/10000))
    print("average power used by DP() : "+str(pm3/10000))
