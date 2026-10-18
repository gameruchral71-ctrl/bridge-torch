# Explicit optimal bags (forward trips) for the base window 5c-5 <= n <= 7c-6, c >= 8,
# a schedule realizer, and verification against the closed formula.
import sys
from formula import Tf
from functools import lru_cache
def family(n,c):
    e=n-5*c
    if e==-5: k,t,a=2,c-3,{1:0,2:2}
    elif e==-4: k,t,a=2,0,{1:0,2:3}
    elif -3<=e<=c-6: k,t,a=2,e+3,{1:1,2:2}
    elif e==c-5: k,t,a=2,0,{1:1,2:3}
    elif e==c-4: k,t,a=2,0,{1:0,2:3}
    elif c-3<=e<=2*c-7: k,t,a=3,e-c+3,{1:1,2:1,3:1}
    elif e==2*c-6: k,t,a=3,0,{1:1,2:1,3:2}
    else: raise ValueError
    return k,t,a
def build_bag(n,c,k,t,a):
    trips=[]; pos=k
    if t>0:
        trips.append(tuple(range(1,k+1))+tuple(range(pos+1,pos+t+1))); pos+=t
    for j in range(k,0,-1):
        for _ in range(a.get(j,0)):
            s=c-j; trips.append(tuple(range(1,j+1))+tuple(range(pos+1,pos+s+1))); pos+=s
    rem=n-pos; assert rem>=0 and rem%c==0, (n,c,k,t,a,rem)
    P=rem//c
    for _ in range(P):
        trips.append(tuple(range(pos+1,pos+c+1))); pos+=c
    # nomadic trips to satisfy |F| = sum r + 1  <=>  sum_T (j_T-1) = k-1
    E=sum(sum(1 for x in T if x<=k)-1 for T in trips)
    D=k-1-E; assert D>=0,(n,c,D)
    if k==2: trips+= [(1,2)]*D
    else:
        trips+= [(1,2,3)]*(D//2) + ([(1,2)] if D%2 else [])
    return trips
def cost(bag,n):
    f=[0]*(n+1)
    for T in bag:
        for x in T: f[x]+=1
    assert all(f[i]>=1 for i in range(1,n+1))
    assert sum(len(T)-1 for T in bag)==n-1
    return sum(max(T) for T in bag)+sum(i*(f[i]-1) for i in range(1,n+1))
def realize(bag,n):
    # DFS for an actual crossing sequence using exactly these forward trips, single-person returns.
    from collections import Counter
    bag=Counter(bag)
    need={i:0 for i in range(1,n+1)}
    for T,m in bag.items():
        for x in T: need[x]+=m
    far=set(); seq=[]
    sys.setrecursionlimit(100000)
    seen=set()
    def key(): return (frozenset(far),tuple(sorted(bag.items())))
    def dfs():
        if sum(bag.values())==0: return len(far)==n
        kk=key()
        if kk in seen: return False
        # forward step: pick a trip all of whose members are near
        for T in sorted([T for T,m in bag.items() if m>0], key=lambda T:(-sum(1 for x in T if need[x]>1),max(T))):
            if any(x in far for x in T): continue
            bag[T]-=1
            for x in T: far.add(x); need[x]-=1
            seq.append(('F',T))
            if sum(bag.values())==0:
                if len(far)==n: return True
            else:
                # return step: someone on far side with remaining forward trips
                for r in sorted(x for x in far if need[x]>0):
                    far.discard(r); seq.append(('R',(r,)))
                    if dfs(): return True
                    far.add(r); seq.pop()
            seq.pop()
            for x in T: far.discard(x); need[x]+=1
            bag[T]+=1
        seen.add(kk)
        return False
    ok=dfs()
    return seq if ok else None
def seq_cost(seq,n,c):
    near=set(range(1,n+1)); far=set(); tot=0; side=0
    for typ,G in seq:
        assert 1<=len(G)<=c
        if typ=='F':
            assert side==0 and all(x in near for x in G); near-=set(G); far|=set(G); side=1
        else:
            assert side==1 and all(x in far for x in G); far-=set(G); near|=set(G); side=0
        tot+=max(G)
    assert not near and side==1
    return tot
if __name__=='__main__':
    c0,c1=int(sys.argv[1]),int(sys.argv[2]); real=len(sys.argv)>3
    for c in range(c0,c1+1):
        for n in range(5*c-5,7*c-5):
            k,t,a=family(n,c); bag=build_bag(n,c,k,t,a)
            assert all(2<=len(T)<=c for T in bag)
            C=cost(bag,n)
            assert C==Tf(n,c),(c,n,C,Tf(n,c))
            if real:
                s=realize(bag,n); assert s is not None,(c,n)
                assert seq_cost(s,n,c)==C
        print('c',c,'base window OK'+(' (sequences realized)' if real else ''),flush=True)
