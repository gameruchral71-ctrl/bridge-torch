// Fast exact T_c(n) for all n<=N via ordered nested bags (Backhouse-Truong structure), doubled costs.
#include <bits/stdc++.h>
using namespace std;
typedef long long ll; const ll INF=LLONG_MAX/4;
int c,N;
ll H2(int j){return (ll)(j-4)*(j-4)-7;} // 2*phi(j)
// min doubled nomadic cost for excess D>=0 with need N_k trips >= need
ll nomcost(int k,ll D,int need){
  if(k==1) return (D==0&&need==0)?0:INF;
  ll best=INF;
  for(ll a=need;a*(k-1)<=D && a<=need+3;a++){
    ll r=D-a*(k-1); ll cr;
    if(k==2) cr=r; // each N2 costs 1 (doubled .5)
    else cr=(r%2)?1:0; // N3 free, one N2 if odd
    best=min(best,a*(ll)(k-3)*(k-3)+cr);
  }
  return best;
}
int main(int argc,char**argv){
  c=atoi(argv[1]);N=atoi(argv[2]);
  vector<ll> ans(N+1,INF);
  for(int n=1;n<=min(N,c);n++) ans[n]=n;
  for(int k=1;k<=c;k++){
    int S=N-k; if(S<1) break;
    bool clamp=(k>=3);
    int Emin = clamp? -(2*k+2) : -(S+2);
    int Emax = 2*N+5; // E can rise via mixed blocks; bound
    if(clamp) Emax = (k-1)*(S+1); // rough
    // E range large when many mixed blocks with j>=2; cap Emax for memory: mixed blocks count <= S
    int Er = Emax-Emin+1;
    // to limit memory, store per pos a map? use vector sized (k+1)*Er*3 per pos, roll? need all pos. Use hashmap per pos.
    vector<unordered_map<ll,ll>> dp(S+1);
    auto key=[&](int lj,int E,int ck){return ((ll)lj*10000019LL+(E+2000000))*3+ck;};
    dp[0][key(k,0,0)]=0;
    for(int p=0;p<=S;p++){
      for(auto &kv: dp[p]){
        ll kk=kv.first; ll v=kv.second; int ck=kk%3; ll rest=kk/3; int E=(int)(rest%10000019LL)-2000000; int lj=(int)(rest/10000019LL);
        // finalize
        if(p>=1 || true){
          int n=k+p;
          if(p>=1){ ll D=(ll)k-1-E; if(D>=0){ int need=max(0,2-ck); ll nc=nomcost(k,D,need); if(nc<INF){ ll tot=v+nc+7-(ll)(k-4)*(k-4); ll T=(tot+1)/2; // ceil of tot/2 (tot may be negative? no)
                if(T<ans[n]) ans[n]=T; } } }
        }
        if(p==S) continue;
        for(int j=0;j<=lj;j++){
          for(int s=(j==0?c:1); s<=c-j && p+s<=S; s++){
            int ell=k+p+s; int ne=E+(j-1);
            if(clamp && ne<Emin) ne+=2*((Emin-ne+1)/2);
            if(ne > k-1 + (S-(p+s))/c) continue;
            int nck=min(2,ck+(j==k?1:0));
            ll nv=v+2LL*ell+H2(j);
            ll q=key(j,ne,nck);
            auto it=dp[p+s].find(q);
            if(it==dp[p+s].end()||nv<it->second) dp[p+s][q]=nv;
          }
        }
      }
      dp[p].clear(); dp[p].rehash(0);
    }
  }
  for(int n=1;n<=N;n++) printf("%lld ",ans[n]); printf("\n");
}
