import sympy as sp
c,t=sp.symbols('c t',integer=True)
phi=lambda j: sp.Rational((j-4)**2-7,2)
def famcost(k,tt,a,n):
    # returns symbolic cost given k, partial t (symbolic or 0), counts a[j], n (symbolic in c,t)
    tot=sp.Rational(7-(k-4)**2,2); pos=k; E=0
    if tt!=0:
        pos=pos+tt; tot+=pos+phi(k); E+=k-1
    for j in range(k,0,-1):
        for _ in range(a.get(j,0)):
            pos=pos+(c-j); tot+=pos+phi(j); E+=j-1
    P=sp.simplify((n-pos)/c)
    assert P.is_integer or P.free_symbols==set(), P
    # pure blocks leaders: n, n-c, ..., n-(P-1)c
    i=sp.symbols('i',integer=True)
    tot+=sp.summation(n-i*c,(i,0,P-1))+P*phi(0); E-=P
    D=sp.simplify(k-1-E)
    # nomadic: k=2 -> D N2 trips each eff 1/2 ; k=3 -> N3 free, one N2 if D odd
    if k==2: tot+=D*sp.Rational(1,2)
    else:
        assert D.is_number
        tot+=sp.Rational(1,2)*(D%2)
    return sp.expand(tot),P,D
def F(n):
    # closed formula pieces: n+3 = g c + d
    pass
cases=[('e=-5',2,c-3,{1:0,2:2},5*c-5),('e=-4',2,0,{2:3},5*c-4),('e in[-3,c-6]',2,t,{1:1,2:2},5*c+t-3),
       ('e=c-5',2,0,{1:1,2:3},6*c-5),('e=c-4',2,0,{2:3},6*c-4),('e in[c-3,2c-7]',3,t,{1:1,2:1,3:1},6*c-3+t),('e=2c-6',3,0,{1:1,2:1,3:2},7*c-6)]
for name,k,tt,a,n in cases:
    C,P,D=famcost(k,tt,a,n)
    print(name,'n=',n,' P=',P,' D=',D,' cost=',sp.factor(C))
