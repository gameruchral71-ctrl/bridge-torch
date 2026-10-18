import subprocess,sys
def Tf(n,c):
    g,d=divmod(n+3,c)
    x=3*g+max(0,d-c+3)
    return c*g*(g+1)//2+(g+1)*d-10+(x+1)//2
if __name__=='__main__':
    for c in range(3,int(sys.argv[1])+1):
        N=20*c
        T=[None]+list(map(int,subprocess.check_output(['./model2',str(c),str(N)]).split()))
        bad=[n for n in range(1,N+1) if Tf(n,c)!=T[n]]
        print(c,'formula fails at n<=',max(bad) if bad else None,'; 5c-5 =',5*c-5, '; all n>=%d ok'%(max(bad)+1))
