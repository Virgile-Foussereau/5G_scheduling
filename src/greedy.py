from preprocessing import *
import os
import time
from scipy import optimize as op
import numpy as np

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "../testfiles/test1.txt"
abs_file_path = os.path.join(script_dir, rel_path)
fichier=open(abs_file_path,"r")
test1=fichier.read().splitlines()
fichier.close()

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "../testfiles/test2.txt"
abs_file_path = os.path.join(script_dir, rel_path)
fichier=open(abs_file_path,"r")
test2=fichier.read().splitlines()
fichier.close()

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "../testfiles/test3.txt"
abs_file_path = os.path.join(script_dir, rel_path)
fichier=open(abs_file_path,"r")
test3=fichier.read().splitlines()
fichier.close()

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "../testfiles/test4.txt"
abs_file_path = os.path.join(script_dir, rel_path)
fichier=open(abs_file_path,"r")
test4=fichier.read().splitlines()
fichier.close()

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "../testfiles/test5.txt"
abs_file_path = os.path.join(script_dir, rel_path)
fichier=open(abs_file_path,"r")
test5=fichier.read().splitlines()
fichier.close()

testfiles=[test1,test2,test3,test4,test5]

def add(E,u):
    i=0
    while i<len(E) and E[i][0]<u[0]:
        i+=1
    return E[:i+1]+[u]+E[i+1:]

def greedyLP(L,pmax):
    E=[]
    X=[]
    p=0
    r=0
    for n in range(len(L)):
        L[n].sort(key= lambda x: x[0])
        X.append((0,1))
#X[n] contains (l,x), l the position of the triplet in L[n] and x the fraction used (which will always be 1 except for the last triplet added)
#We start with l=0 for each n because we know it is a valid solution

        p+=L[n][0][0]
        r+=L[n][0][1]
        if len(L[n])>=2:
            e=(L[n][1][1]-L[n][0][1])/(L[n][1][0]-L[n][0][0]) #computation of the incremental efficiency
            E=add(E,[e,n])
    u=E.pop()
    e,n=u[0],u[1]
    i=X[n][0]
    while len(E)>0 and p<pmax-(L[n][i+1][0]-L[n][i][0]): #we upgrade as much as we can
        X[n]=(X[n][0]+1,1)
        p+=(L[n][i+1][0]-L[n][i][0])
        r+=(L[n][i+1][1]-L[n][i][1])
        i+=1
        if i<len(L[n])-1:
            e=(L[n][i+1][1]-L[n][i][1])/(L[n][i+1][0]-L[n][i][0])
            E.append([e,n])
            E.sort(key= lambda x: x[0])
        u=E.pop()
        e,n=u[0],u[1]
        i=X[n][0]
    if len(E)==0 and p<pmax-(L[n][i+1][0]-L[n][i][0]): #we reached the end of every channel
        X[n]=(X[n][0]+1,1)
        p+=(L[n][i+1][0]-L[n][i][0])
        r+=(L[n][i+1][1]-L[n][i][1])
        return r, p, X #it is a solution to the ILP problem
    if p==pmax: #if p=pmax we have a solution to the ILP problem
        return r, p, X
    else: #if not we use our right to 2 non integer
        x=(pmax-p)/(L[n][i+1][0]-L[n][i][0])
        X[n]=(i,1-x) #we only store i and 1-x because then we know that the other triplet of the channel is associated with i+1 and x.
        r+=(L[n][i+1][1]-L[n][i][1])*x
        return r, pmax, X

def testGreedy(file):
    (N,M,K,pmax,PR)=preprocessing(file)
    start_time = time.time()
    r,p,X= greedyLP(PR,pmax)
    print("--- %s seconds ---" % (time.time() - start_time))
    print("Optimal rate : "+str(r))
    print("Used power : "+str(p))

######### LP solver for comparison

def channelSelector(current_size,KM,NKM):
    ans=[0 for i in range(NKM)]
    for i in range(KM):
        ans[current_size+i]=1
    return(ans)

def LP_parameters(L):
    N = len(L)
    NKM=count(L)
    AllChannelSelector=[0 for i in range(N)]
    current_size=0
    p_values=[]
    r_values=[]
    for n in range(N):
        KM=len(L[n])
        AllChannelSelector[n]=channelSelector(current_size,KM,NKM)
        current_size+=KM
        p_values = p_values + [L[n][i][0] for i in range(KM)]
        r_values = r_values + [L[n][i][1] for i in range(KM)]
    return(N,p_values,r_values,AllChannelSelector)

def LP_solver(N,pmax,p_values,r_values,AllChannelSelector):
    #we are going to minimize -cX in order to maximize cX
    c=np.array(r_values)
    c=-c

    #A_ubX<=B_ub
    A_ub=np.array([p_values])
    B_ub=np.array([pmax])

    #A_eqX=B_eq
    #AllChannelSelector ensures that we have only one user per channel
    A_eq=np.array(AllChannelSelector)
    B_eq=np.array([1 for n in range(N)])

    #bounds for each element of X
    bd=(0,1)

    res=op.linprog(c,A_ub,B_ub,A_eq,B_eq,bounds=bd)
    usedP=np.matmul(A_ub,res.x)[0]
    return(-res.fun,res.x,usedP)

def testLP_solver(file):
    (N,M,K,pmax,PR)=preprocessing(file)
    start_time = time.time()
    (N,p_values,r_values,AllChannelSelector)=LP_parameters(PR)
    (R,X,usedP)=LP_solver(N,pmax,p_values,r_values,AllChannelSelector)
    print("--- %s seconds ---" % (time.time() - start_time))
    print('Optimal rate : '+str(R))
    print("Used power : "+str(usedP))
