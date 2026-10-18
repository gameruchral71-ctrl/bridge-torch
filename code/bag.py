import itertools, sys, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds, linprog
from scipy.sparse import lil_matrix
def build(n,c,multiret=True):
    P=range(1,n+1)
    Ts=[T for k in range(1,c+1) for T in itertools.combinations(P,k)]
    Rs=Ts if multiret else [(i,) for i in P]
    V=len(Ts)+len(Rs)
    cost=np.array([max(T) for T in Ts]+[max(R) for R in Rs],float)
    A=lil_matrix((n+1,V))
    for j,T in enumerate(Ts):
        for i in T: A[i-1,j]=1
        A[n,j]=1
    for j,R in enumerate(Rs):
        for i in R: A[i-1,len(Ts)+j]-=1
        A[n,len(Ts)+j]=-1
    return Ts,Rs,cost,A.tocsr()
def B(n,c,relax=False,multiret=True):
    Ts,Rs,cost,A=build(n,c,multiret)
    b=np.ones(n+1)
    if relax:
        r=linprog(cost,A_eq=A,b_eq=b,bounds=(0,None),method='highs'); return r.fun
    r=milp(cost,constraints=LinearConstraint(A,b,b),integrality=np.ones(len(cost)),bounds=Bounds(0,np.inf))
    return r.fun
if __name__=='__main__':
    c=int(sys.argv[1])
    for n in range(int(sys.argv[2]),int(sys.argv[3])+1):
        print(n,round(B(n,c)),B(n,c,relax=True),flush=True)
