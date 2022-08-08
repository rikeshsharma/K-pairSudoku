import itertools
from timeit import repeat
from pysat.solvers import Solver
from pysat.formula import CNF

s=Solver()

file = input()
f = open(file,'r')
k = f.readline()
k = int(k[:-1])
ksquare = k*k
mat = f.readlines()
f.close()
mat = [j.split(',') if j[-1]!="\n" else j[:-1].split(',') for j in mat]

def create_num(r,c,i,d):
    dig = ksquare+1
    return r*dig*dig*dig+c*dig*dig+i*dig+d
def get_num(num):
    dig = ksquare+1
    d = num%dig
    num //=dig
    i = num%dig
    num //=dig
    c = num%dig
    r = num//dig
    return [r,c,i,d]

pos=[]
for i in range(ksquare):
    for j in range(ksquare):
        if mat[i][j]!='0':
            pos.append(create_num(i+1,j+1,1,int(mat[i][j])))
for i in range(ksquare,2*ksquare):
    for j in range(ksquare):
        if mat[i][j]!='0':
            pos.append(create_num(i%ksquare+1,j%ksquare+1,2,int(mat[i][j])))

#atleast one number in each cell
#atmost one number in each column 
for i in range(1,3):
    for r in range(1,ksquare+1):
        for c in range(1,ksquare+1):
            s.add_clause([create_num(r, c, i,n) for n in range(1, ksquare+1)])
            for n1, n2 in itertools.combinations(range(1, ksquare+1), 2):
                s.add_clause([-1*create_num(r, c, i, n1), -1*create_num(r, c,i,n2)])

#a number appears atmost once in each row
for i in range(1,3):
    for r in range(1,ksquare+1):
        for n in range(1, ksquare+1):
            for c1,c2 in itertools.combinations(range(1, ksquare+1),2):
                s.add_clause([-1*create_num(r,c1,i,n), -1*create_num(r,c2,i,n)])

#a number appears atmost once in each column
for i in range(1,3):
    for c in range(1,ksquare+1):
        for n in range(1, ksquare+1):
            for r1,r2 in itertools.combinations(range(1, ksquare+1), 2):
                #print(int("-%d%d%d%d"%(r1,c,i,n)))
                s.add_clause([-1*create_num(r1,c,i,n), -1*create_num(r2,c,i,n)])

lst=[]
lst1=[]
for i,j in itertools.product(range(k), repeat=2):
    lst.append([i,j])
for i in range(ksquare):
    for j in range(i+1,ksquare):
        lst1.append([lst[i],lst[j]])

#a number appears atmost once in each of K*K blocks (sub-grids)
for i in range(1,3):
    for startRow, startCol in itertools.product(range(1,ksquare,k), repeat=2):
        for n in range(1, ksquare+1):
            for delta in lst1:
                s.add_clause([-1*create_num(startRow + delta[0][0], startCol + delta[0][1], i, n),
                              -1*create_num(startRow + delta[1][0], startCol + delta[1][1], i, n)])

#the two sudoku has diffrent number in corresponding cells
for r, c in itertools.product(range(1,ksquare+1), repeat=2):
    for n in range(1, ksquare+1):
        s.add_clause([-1*create_num(r,c,1,n), -1*create_num(r,c,2,n)])

def get_sud():
    sud = []
    for i in s.get_model():
        if i>0:
            sud.append(get_num(i))
    sud1 = [[],[]]
    for i in range(ksquare):
        sud1[0].append([0 for j in range(ksquare)])
        sud1[1].append([0 for j in range(ksquare)])
    for i in sud:
        sud1[i[2]-1][i[0]-1][i[1]-1] = i[3]
    lst1 = ""
    for i in sud1:
        for line in i:
            for word in line:
                lst1+=str(word)+","
            lst1 = lst1[:-1]+"\n"
    f.write(lst1)
    f.close()

out = "out_"+file.split("/")[-1]
f = open(out,'w')
if s.solve(assumptions=pos):
    get_sud()
else:
    f.write("None")
    f.close()