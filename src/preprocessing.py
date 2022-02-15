import os
import matplotlib.pyplot as plt
import copy

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

def input(file):
    N=int(float(file[0]))
    M=int(float(file[1]))
    K=int(float(file[2]))
    pmax=float(file[3])
    PR=[] #we make the choice of an array of n lists, each one represents a channel
    i=4
    for n in range(N): #first we recover all p values
        PR.append([])
        for k in range(K):
            l=file[i].split()
            i+=1
            for m in range(M):
                p=float(l[m])
                PR[n].append([p,0,m,k])  #We store the p value along the corresponding m and k
    for n in range(N):                   #Then we recover all r values
        j=0
        for k in range(K):
            l=file[i].split()
            i+=1
            for m in range(M):
                r=float(l[m])
                PR[n][j][1]=r
                j+=1
    return (N,M,K,pmax,PR)

def count(PR):          # auxiliary function to count the number of triplets.
    S=0
    for n in range(len(PR)):
        S+=len(PR[n])
    return S

def preprocessing1(input):
    (N,M,K,pmax,PR)=input
    if count(PR)==0:
        return (N,M,K,pmax,[])      #if we have no triplets we return an empty list
    LpnMin=[]           #initialization of the list of minimum p values for each channel
    S=0                 #sum of these minimum p values
    for n in range(N):
        pnMin=PR[n][0][0]
        for i in range(1,len(PR[n])):
            p=PR[n][i][0]
            if p<pnMin:
                pnMin=p         #we find the minimum for each channel
        LpnMin.append(pnMin)    #we add it to the list
        S+=pnMin                #and to the sum
    for n in range(N):
        PR[n]=[pr for pr in PR[n] if pr[0]+S-LpnMin[n]<=pmax]   #if a triplet make a solution impossible we remove it
    return (N,M,K,pmax,PR)


def preprocessing2(input):
    (N,M,K,pmax,PR)=input
    if count(PR)==0:
        return (N,M,K,pmax,[])
    for n in range(N):
        PR[n].sort(key=lambda x: (x[0],x[1]))  #list sorted on p values (and r in case of equality)
        maxR=PR[n][0][1]
        Ldelete=[]              #list of elements to delete
        for i in range(1,len(PR[n])):
            r=PR[n][i][1]
            if r <=maxR: #if we have a smaller r we delete because the list is sorted on p
                Ldelete.append(i)
            elif PR[n][i][0]==PR[n][i-1][0]: #if p are equals we delete the previous element which has a smaller r
                Ldelete.append(i-1)
                maxR=r
            else:
                maxR=r
        for i in reversed(Ldelete): #we run through Ldelete in the reverse order to not change the index of the remaining elements to delete
            del PR[n][i]
    return (N,M,K,pmax,PR)

def preprocessing3(input):
    (N,M,K,pmax,PR)=input
    if count(PR)==0:
        return (N,M,K,pmax,[])
    for n in range(N):
        PR[n].sort(key=lambda x: x[0])
        L=[PR[n][0]] #we start the concave hull
        for i in range(1,len(PR[n])):
            p,r=PR[n][i][0],PR[n][i][1]
            while len(L)>1 and (L[-1][1]-L[-2][1])*(p-L[-1][0])<=(r-L[-1][1])*(L[-1][0]-L[-2][0]):
                L.pop()  #we delete previous element not following the constraint
            L.append(PR[n][i]) #the last element of the sub-problem has to be in in the hull
        PR[n]=L
    return (N,M,K,pmax,PR)

def preprocessing3withoutSort(input): #same but we assume each L[n] is allready sorted
    (N,M,K,pmax,PR)=input
    if count(PR)==0:
        return (N,M,K,pmax,[])
    for n in range(N):
        L=[PR[n][0]] #we start the concave hull
        for i in range(1,len(PR[n])):
            p,r=PR[n][i][0],PR[n][i][1]
            while len(L)>1 and (L[-1][1]-L[-2][1])*(p-L[-1][0])<=(r-L[-1][1])*(L[-1][0]-L[-2][0]):
                L.pop()  #we delete previous element not following the constraint
            L.append(PR[n][i]) #the last element of the sub-problem has to be in in the hull
        PR[n]=L
    return (N,M,K,pmax,PR)

def preprocessing(file): #all preprocessing
    data=input(file)
    data=preprocessing1(data)
    data=preprocessing2(data)
    data=preprocessing3withoutSort(data) #allready sorted in preprocessing2
    return data

def testPreprocessing(file):
    data=input(file)
    N=str(count(data[-1]))
    print("Initial number of triplets : "+N)
    data=preprocessing1(data)
    N=str(count(data[-1]))
    print("Triplet number after first preprocessing : "+N)
    data=preprocessing2(data)
    N=str(count(data[-1]))
    print("Triplet number after second preprocessing : "+N)
    data=preprocessing3withoutSort(data)
    N=str(count(data[-1]))
    print("Triplet number after third preprocessing : "+N)

def plotPreprocessing(file):
    data=input(file)
    N=str(count(data[-1]))
    print("Nombre de données initiales : "+N)
    P0=[pr[0] for pr in data[-1][8]]
    R0=[pr[1] for pr in data[-1][8]]
    data=preprocessing1(data)
    N=str(count(data[-1]))
    print("Nombre de données après premier preprocessing : "+N)
    P1=[pr[0] for pr in data[-1][8]]
    R1=[pr[1] for pr in data[-1][8]]
    data=preprocessing2(data)
    N=str(count(data[-1]))
    print("Nombre de données après deuxième preprocessing : "+N)
    P2=[pr[0] for pr in data[-1][8]]
    R2=[pr[1] for pr in data[-1][8]]
    data=preprocessing3withoutSort(data)
    N=str(count(data[-1]))
    print("Nombre de données après troisième preprocessing : "+N)
    P3=[pr[0] for pr in data[-1][8]]
    R3=[pr[1] for pr in data[-1][8]]

    fig=plt.figure()
    ax=plt.subplot(221)
    ax.scatter(P0,R0,marker=".")
    ax.title.set_text('Initial set')
    ax.set_xlabel('Power')
    ax.set_ylabel('Rate')
    ax=plt.subplot(222)
    ax.scatter(P0,R0,marker=".")
    ax.scatter(P1,R1,marker=".",color="green")
    ax.title.set_text('Set after quick preprocessing')
    ax.set_xlabel('Power')
    ax.set_ylabel('Rate')
    ax=plt.subplot(223)
    ax.scatter(P0,R0,marker=".")
    ax.scatter(P1,R1,marker=".",color="green")
    ax.scatter(P2,R2,marker=".",color="yellow")
    ax.title.set_text('Set after removing IP dominated terms')
    ax.set_xlabel('Power')
    ax.set_ylabel('Rate')
    ax=plt.subplot(224)
    ax.scatter(P0,R0,marker=".")
    ax.scatter(P1,R1,marker=".",color="green")
    ax.scatter(P2,R2,marker=".",color="yellow")
    ax.plot(P3,R3,marker=".",color="red")
    ax.title.set_text('Set after removing LP dominated terms')
    ax.set_xlabel('Power')
    ax.set_ylabel('Rate')

    plt.tight_layout()
    plt.show()