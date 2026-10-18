import sys, subprocess, math
from fractions import Fraction as F
PHI=[F(9,2),F(1),F(-3,2),F(-3)]
def Useq(c,N):
    U=[F(0)]*(N+1)
    for M in range(4,N+1):
        cands=[]
        for j,s in ((3,c-3),(2,c-2),(1,c-1),(0,c)):
            if s<1: continue
            cands.append(U[max(3,M-s)]+M+PHI[j])
        U[M]=min(cands)
    return U
if __name__=="__main__":
  for c in range(int(sys.argv[1]),int(sys.argv[2])+1):
      N=12*c
      U=Useq(c,N)
      u=[U[i]-U[i-1] for i in range(4,N+1)]
      mono=all(u[i]>=u[i-1] for i in range(1,len(u))) and u[0]>=F(1,2)
      T=[None]+list(map(int,subprocess.check_output(['./model2',str(c),str(N)]).split()))
      diff=[n for n in range(4,N+1) if 3+math.ceil(U[n])!=T[n]]
      print(c,'monotone' if mono else 'NOT monotone','u4=',u[0],' mismatch n:',diff[:12],'... max',max(diff) if diff else None)
