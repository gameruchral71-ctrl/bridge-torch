from fractions import Fraction as F
import sys
def ut(c,i):  # periodic extension
    # group g occupies [(g-1)c-2, gc-3]; value g on first c-3, g+1/2 on last 3
    g=(i+2)//c+1
    off=i-((g-1)*c-2)
    return F(g) if off<c-3 else F(2*g+1,2)
def u(c,i):
    if i<=3: return F(0)
    if i<=c: return F(1)
    if i<=2*c-3: return F(2)
    if i==2*c-2: return F(5,2)
    if i<=3*c-5: return F(3)
    if i<=3*c-3: return F(7,2)
    return ut(c,i)
SIG={1:F(7,2),2:F(6),3:F(15,2)}
def Q(c,j,a):
    return sum(ut(c,i) for i in range(a,a+j))+sum(ut(c,i)-u(c,i) for i in range(a+j,a+c))
def check(c):
    # sanity: u equals pattern used in verify_dual for i>=4
    from verify_dual import weights
    w=weights(c,6*c)
    assert all(w[i]==u(c,i) for i in range(4,6*c+1))
    assert all(ut(c,i)-u(c,i)>=0 for i in range(5-c,6*c))
    mins={}
    for j in (1,2,3):
        vals=[(a,Q(c,j,a)-SIG[j]) for a in range(5-c,4*c)]
        mins[j]=min(v for a,v in vals)
        if mins[j]<0: return False,mins
    return True,mins
if __name__=='__main__':
    for c in range(int(sys.argv[1]),int(sys.argv[2])+1):
        ok,m=check(c)
        if not ok or c%25==0 or c<12: print(c,ok,{j:str(v) for j,v in m.items()})
