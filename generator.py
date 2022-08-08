import itertools
from timeit import repeat
from pysat.solvers import Solver
from pysat.formula import CNF
from random import randint

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

def create_solver(k,ksquare):
    s=Solver()
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
    return s

def get_full_sud(k,ksquare):
    s = create_solver(k,ksquare)
    s.solve()
    pos=[]
    for i in s.get_model():
        if i>0:
            pos.append(i)
    s.delete()
    return pos

def create_hole(pos, neg):
    i = pos.pop(randint(0,len(pos)-1))
    neg.append(i)
    return pos,neg

def single_sol_check(pos,neg,k,ksquare):
    s = create_solver(k,ksquare)
    s.add_clause([-1*i for i in neg])
    r = s.solve(assumptions=pos)
    s.delete()
    return not r

k = int(input())
ksquare = k*k
pos = get_full_sud(k,ksquare)
pos,neg = create_hole(pos,[])
while single_sol_check(pos,neg,k,ksquare):
    pos1 = pos
    pos,neg = create_hole(pos,neg)

out = "output"+str(k)+".csv"
f = open(out,'w')
sud = [get_num(i) for i in pos1]
sud1 = [[],[]]
for i in range(ksquare):
    sud1[0].append([0 for j in range(ksquare)])
    sud1[1].append([0 for j in range(ksquare)])
for i in sud:
    sud1[i[2]-1][i[0]-1][i[1]-1] = i[3]
lst1 = str(k)+"\n"
for i in sud1:
    for line in i:
        for word in line:
            lst1+=str(word)+","
        lst1 = lst1[:-1]+"\n"
f.write(lst1)
f.close()