from conf import best
from bags import build_bag, cost, realize, seq_cost
from formula import Tf
for c in range(3,8):
    lo=7 if c==3 else 5*c-5
    for n in range(lo,lo+2*c):
        b,arg=best(n,c,R=5)
        k,t,a,_=arg
        aa={j:a[j-1] for j in range(1,k+1)}
        bag=build_bag(n,c,k,t,aa) if k in (2,3) else None
        if bag is None: print('c',c,'n',n,'needs k',k); continue
        C=cost(bag,n); s=realize(bag,n)
        ok=(C==Tf(n,c)==b) and s is not None and seq_cost(s,n,c)==C
        print(c,n,k,t,aa,C,Tf(n,c),'OK' if ok else 'FAIL')
