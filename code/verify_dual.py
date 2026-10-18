# Exhaustive check (exact arithmetic, doubled) that weights u are dual-feasible:
# for every set T of 1..c people: sum_T u <= max T + 9/2 (forward trips)
# and for every set R: sum_R u - (9/2)|R| + (9/2)(|R|-1) >= -max R, i.e. sum_R u >= 9/2 - max R (return trips).
import sys
from fractions import Fraction as F
def weights(c,n):
    u=[None,F(7,2),F(5,2),F(3,2)]
    g=1
    while len(u)<=n:
        u+= [F(g)]*(c-3) + [F(2*g+1,2)]*min(g-1,3)
        g+=1
    return u[:n+1]
def check(c,n):
    u=weights(c,n)
    for M in range(1,n+1):
        below=sorted(u[1:M],reverse=True)
        acc=u[M]
        if acc>M+F(9,2): return ('F',M,1)
        for s in range(2,min(c,M)+1):
            acc+=below[s-2]
            if acc>M+F(9,2): return ('F',M,s)
        acc=u[M]
        if acc< F(9,2)-M: return ('R',M,1)
        asc=below[::-1]
        for s in range(2,min(c,M)+1):
            acc+=asc[s-2]
            if acc< F(9,2)-M: return ('R',M,s)
    return None
if __name__=='__main__':
    for c in range(3,int(sys.argv[1])+1):
        r=check(c,int(sys.argv[2])*c)
        print(c,'feasible' if r is None else r)
