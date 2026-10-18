import subprocess,sys,math
from colgen import solve
from fractions import Fraction as F
c=int(sys.argv[1]); N=int(sys.argv[2])
T=[None]+list(map(int,subprocess.check_output(['./model2',str(c),str(N)]).split()))
bad=[]
for n in range(c+1,N+1):
    f=solve(n,c)[0]; L=F(f).limit_denominator(1000)
    if math.ceil(L)!=T[n]: bad.append((n,str(L),T[n]))
print(c,'ceil(LP)!=T at',bad)
