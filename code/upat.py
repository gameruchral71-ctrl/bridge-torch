import sys
from fractions import Fraction as F
from ucheck import Useq
def upat(c,N):
    u=[]
    g=1
    while len(u)<N:
        u+= [F(g)]*(c-3) + [F(2*g+1,2)]*min(g-1,3)
        g+=1
    return u[:N]
if __name__=="__main__":
  for c in range(3,61):
    N=15*c; U=Useq(c,N); u=[U[i]-U[i-1] for i in range(4,N+1)]
    p=upat(c,len(u))
    if u!=p: print('c',c,'MISMATCH at', next(i+4 for i in range(len(u)) if u[i]!=p[i]))
  print('done')
