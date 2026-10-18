# Enumerate "ordered bag" configurations for large n: nomads 1..k (k=3 or 4),
# from bottom: optional partial block (j=k) of t settlers, then full blocks with j=k, k-1, ..., 1, then pure blocks.
import sys, itertools
from fractions import Fraction as F
def hh(j): return F((j-3)**2,2)-j
def cost_conf(n,c,k,t,a):   # a[j] = number of full blocks with j nomads, j=1..k ; returns exact cost or None
    pos=k   # last settler covered so far
    tot=F(0); E=0; cntk=0
    blocks=[]
    if t>0:
        if t>=c-k: return None
        pos+=t; tot+=pos+hh(k); E+=k-1; cntk+=1
    for j in range(k,0,-1):
        for _ in range(a[j]):
            pos+=c-j; tot+=pos+hh(j); E+=j-1; cntk+= (j==k)
    rem=n-pos
    if rem<0 or rem%c: return None
    P=rem//c
    tot+=sum(n-i*c for i in range(P))+P*hh(0); E-=P
    D=k-1-E
    if D<0: return None
    # nomadic: free N3 if k>=3; parity cost .5
    nom=F(1,2) if D%2 else F(0)
    if k==2:
        nom=F(D,2)
        if cntk+D<2: return None
    if k==3 and cntk+D//2<2: return None
    if k==5:
        need=max(0,2-cntk); best=None
        for x in range(need,need+3):
            r=D-4*x
            if r<0: continue
            v=x*F(2)+(F(1,2) if r%2 else 0)
            best=v if best is None or v<best else best
        if best is None: return None
        nom=best
    if k==4:
        # need f_4>=2: trips with j=4; N4 cost .5 each, N4 excess 3
        need=max(0,2-cntk)
        # choose nomadic trips: x N4 (>=need), rest N3/N2 to make D
        best=None
        for x in range(need,need+3):
            r=D-3*x
            if r<0: continue
            v=F(x,2)+(F(1,2) if r%2 else 0)
            best=v if best is None or v<best else best
        if best is None: return None
        nom=best
    return tot+nom+F(7,2)-F((k-4)**2,2)
def best(n,c,R=4):
    b=None;arg=None
    for k in (2,3,4,5):
        if k>=c: continue
        for t in range(0,c-k):
            for a in itertools.product(range(R),repeat=k):
                aa=[0]+list(a)
                v=cost_conf(n,c,k,t,aa)
                if v is not None:
                    import math
                    v2=math.ceil(v)
                    if b is None or v2<b: b=v2;arg=(k,t,tuple(a),v)
    return b,arg
if __name__=='__main__':
    c=int(sys.argv[1])
    for n in range(int(sys.argv[2]),int(sys.argv[3])+1):
        print(n,*best(n,c))
