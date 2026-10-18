// exact bridge-and-torch, times 1..n, capacity c, arbitrary forward/return groups
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int n,c; 
int main(int argc,char**argv){n=atoi(argv[1]);c=atoi(argv[2]);
 int N=1<<n; int S=2*N; int *d=malloc(sizeof(int)*S); for(int i=0;i<S;i++)d[i]=1<<29;
 // state: mask = people on far side, bit side: 0 torch near, 1 far. index mask*2+side
 // Dial's algorithm buckets with max edge weight n
 int maxd=n*n*2+10; // bound
 // simple: since weights <= n, use bucket queue with circular? just use arrays of vectors
 int cap=1<<22; 
 int **bk=malloc(sizeof(int*)*(maxd+n+5)); int *bs=calloc(maxd+n+5,sizeof(int)),*bc=calloc(maxd+n+5,sizeof(int));
 #define PUSH(dd,x) do{ if(bs[dd]==bc[dd]){bc[dd]=bc[dd]?bc[dd]*2:16; bk[dd]=realloc(bc[dd]==16?NULL:bk[dd],sizeof(int)*bc[dd]);} bk[dd][bs[dd]++]=x;}while(0)
 for(int i=0;i<maxd+n+5;i++){bk[i]=NULL;}
 d[0]=0; PUSH(0,0);
 int target=(N-1)*2+1;
 for(int D=0;D<maxd;D++){
  for(int q=0;q<bs[D];q++){int st=bk[D][q]; if(d[st]!=D)continue; if(st==target){printf("%d\n",D);return 0;}
   int mask=st>>1, side=st&1; int avail= side? mask : ((N-1)&~mask);
   // enumerate subsets of avail of size 1..c
   for(int sub=avail; sub; sub=(sub-1)&avail){ if(__builtin_popcount(sub)>c)continue;
     int hi=31-__builtin_clz(sub); int w=hi+1; int nm= side? (mask&~sub):(mask|sub); int ns=nm*2+(1-side);
     if(D+w<d[ns]){d[ns]=D+w; PUSH(D+w,ns);} }
  }
 }
 printf("fail\n");}
