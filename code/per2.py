import subprocess,sys
for c in range(int(sys.argv[1]),int(sys.argv[2])+1):
    N=int(sys.argv[3])*c
    T=[None]+list(map(int,subprocess.check_output(['./model2',str(c),str(N)]).split()))
    bad=[n for n in range(2*c+1,N+1) if T[n]!=T[n-2*c]+2*n+9-c]
    n0=(max(bad)+1) if bad else 2*c+1
    print(c,'recurrence T(n)=T(n-2c)+2n+9-c holds for',n0,'<=n<=',N,' i.e. closed form from n>=',n0-2*c,' (5c-5=%d)'%(5*c-5),flush=True)
