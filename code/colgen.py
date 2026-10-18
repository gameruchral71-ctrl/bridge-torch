import sys,numpy as np, itertools
from scipy.optimize import linprog
from scipy.sparse import csc_matrix
def solve(n,c,verbose=False):
    # columns: forward trips (sets), single returns
    cols=set()
    for i in range(1,n+1): cols.add((i,))
    for M in range(1,n+1):
        for s in range(2,c+1):
            if M-s+1>=1: cols.add(tuple(range(M-s+1,M+1)))
            if s-1<M: cols.add(tuple(list(range(1,s))+[M]))
    cols=set(cols)
    while True:
        Ts=sorted(cols)
        rows=[];colsidx=[];vals=[]
        for j,T in enumerate(Ts):
            for i in T: rows.append(i-1);colsidx.append(j);vals.append(1)
            rows.append(n);colsidx.append(j);vals.append(1)
        m=len(Ts)
        for i in range(1,n+1):
            rows+= [i-1,n]; colsidx+=[m+i-1]*2; vals+=[-1,-1]
        A=csc_matrix((vals,(rows,colsidx)),shape=(n+1,m+n))
        cost=np.array([max(T) for T in Ts]+list(range(1,n+1)),float)
        r=linprog(cost,A_eq=A,b_eq=np.ones(n+1),bounds=(0,None),method='highs')
        u=r.eqlin.marginals; mu=u[n]; v=u[:n]+mu; lam=-mu
        # pricing: forward T: sum v + lam(|T|-1) <= max T
        added=0
        for M in range(1,n+1):
            prev=sorted(v[:M-1],reverse=True); idx=np.argsort(-v[:M-1])
            acc=v[M-1]
            for s in range(2,c+1):
                if s-1>M-1: break
                acc+=prev[s-2]
                if acc+lam*(s-1)>M+1e-9:
                    T=tuple(sorted([M]+[int(k)+1 for k in idx[:s-1]]))
                    if T not in cols: cols.add(T); added+=1
        # multi returns: sum_R v + lam(|R|-1) >= -max R  -> check min
        viol=0
        for M in range(1,n+1):
            prev=sorted(v[:M-1]); acc=v[M-1]
            for s in range(2,c+1):
                if s-1>M-1: break
                acc+=prev[s-2]
                if acc+lam*(s-1)< -M-1e-9: viol+=1
        if added==0:
            return r.fun,v,lam,viol,Ts,r.x
if __name__=='__main__':
    c=int(sys.argv[1])
    from fractions import Fraction
    for n in range(int(sys.argv[2]),int(sys.argv[3])+1):
        f,v,lam,viol,_,_=solve(n,c)
        print(n,Fraction(f).limit_denominator(1000),lam,viol,flush=True)
