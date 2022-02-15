from preprocessing import *
import os


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

def entier(L): #function to change every triplet values of r in p to int type
    for n in range(len(L)):
        for i in range(len(L[n])):
            for k in range(len(L[n][i])):
                L[n][i][k]=int(L[n][i][k])
    return L

def DP(L,pmax): #DP algorithm for the ILP problem
    L=entier(L)
    pmax=int(pmax)
    R0=[]
    R1=[0 for i in range(pmax+1)]
    P0=[]
    P1=R1[:]
    for P in range(pmax+1):  #for every power from 0 to pmax
        max=0
        pm=0
        for pr in L[0]:
            if pr[0]<=P and pr[1]>=max:
                max=pr[1]
                pm=pr[0]
        R0.append(max)    #keep the triplet from channel 0 with the best rate for a power <=P
        P0.append(pm)
    for n in range(1,len(L)):
        for P in range(pmax+1):
            max=0
            for pr in L[n]:
                if pr[0]<=P and R0[P-pr[0]]>0 and pr[1]+R0[P-pr[0]]>=max:
                    max=pr[1]+R0[P-pr[0]]
                    pm=pr[0]+P0[P-pr[0]]
            R1[P]=max #we use the equation to compute the max step by step
            P1[P]=pm
        R0=R1[:]
        P0=P1[:]
    return (R1[-1],P1[-1])

def DP2(L,pmax,U): #Alternative DP algorithm for the ILP problem
    L=entier(L)
    U=int(U)
    pmax=int(pmax)
    P0=[]
    for u in range(U+1):
        min=pmax+1
        for pr in L[0]:
            if pr[1]==u and pr[0]<=min:
                min=pr[0]
        if min==pmax+1:
            P0.append(0)
        else:
            P0.append(min)  #we compute the min power allocation for channel 0
    P1=P0[:]
    for n in range(1,len(L)):
        for u in range(U+1):
            min=pmax+1
            for pr in L[n]:
                if pr[1]<=u and P0[u-pr[1]]>0 and pr[0]+P0[u-pr[1]]<=min:
                    min=pr[0]+P0[u-pr[1]]
            if min==pmax+1:
                P1[u]=0
            else:
                P1[u]=min #we use the equation to compute the min step by step
        P0=P1[:]
    m=0
    for u in range(len(P1)):
        if P1[u]<=pmax and P1[u]>0:
            m=u  #we reverse to find the best rate with a power less than pmax
    return (m,P1[m])

def testDP(file):
    (N,M,K,pmax,PR)=preprocessing(file)
    start_time = time.time()
    R,P= DP(PR,pmax)
    print("--- %s seconds ---" % (time.time() - start_time))
    print("Optimal rate : "+str(R))
    print("Used power : "+str(P))

def testDP2(file,U):
    (N,M,K,pmax,PR)=preprocessing(file)
    start_time = time.time()
    R,P= DP2(PR,pmax,U)
    print("--- %s seconds ---" % (time.time() - start_time))
    print("Optimal rate : "+str(R))
    print("Used power : "+str(P))


