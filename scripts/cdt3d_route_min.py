#!/usr/bin/env python3
from collections import Counter, defaultdict, deque
import argparse, math

class LCG:
    def __init__(self, seed): self.s = seed & 0xffffffff
    def rnd(self): self.s=(self.s*1664525+1013904223)&0xffffffff; return self.s/4294967296.0

def add(A,a,b):
    if a!=b: A[a].add(b); A[b].add(a)

def slope(xs,ys):
    X=[math.log(x) for x in xs]; Y=[math.log(y) for y in ys]; n=len(X)
    sx=sum(X); sy=sum(Y); sxx=sum(x*x for x in X); sxy=sum(x*y for x,y in zip(X,Y))
    return (n*sxy-sx*sy)/(n*sxx-sx*sx)

# A: flat 2+1 measurement machinery

def flat_graph(L):
    N=L*L*L; A=[set() for _ in range(N)]
    def vid(x,y,t): return ((t%L)*L+(y%L))*L+(x%L)
    for t in range(L):
        for y in range(L):
            for x in range(L):
                a=vid(x,y,t)
                for dx,dy,dt in [(1,0,0),(0,1,0),(1,-1,0),(0,0,1)]: add(A,a,vid(x+dx,y+dy,t+dt))
    return [list(s) for s in A]

def rewire(A,f,seed):
    r=LCG(seed); N=len(A); B=[set(x) for x in A]
    for u in range(N):
        for v in list(B[u]):
            if v>u and r.rnd()<f:
                B[u].discard(v); B[v].discard(u); w=u
                while w==u or w in B[u]: w=int(r.rnd()*N)
                add(B,u,w)
    return [list(s) for s in B]

def bfs(A,s):
    d=[-1]*len(A); d[s]=0; q=deque([s])
    while q:
        u=q.popleft()
        for v in A[u]:
            if d[v]<0: d[v]=d[u]+1; q.append(v)
    return d

def diam(A,seed=1):
    r=LCG(seed); d=bfs(A,int(r.rnd()*len(A))); a=max(range(len(A)),key=lambda i:d[i]); return max(bfs(A,a))

def spec(A,seed=1,nsrc=4,t1=6,t2=30):
    r=LCG(seed); N=len(A); vals=[]
    for _ in range(nsrc):
        src=int(r.rnd()*N); p=[0.0]*N; p[src]=1.0; P=[]
        for _t in range(t2+1):
            P.append(p[src]); np=[0.0]*N
            for i,pi in enumerate(p):
                if pi==0: continue
                np[i]+=0.5*pi; mv=0.5*pi/(len(A[i]) or 1)
                for k in A[i]: np[k]+=mv
            p=np
        vals.append(-2*(math.log(P[t2])-math.log(P[t1]))/(math.log(t2)-math.log(t1)))
    return sum(vals)/len(vals)

def ball(A,seed=1,nsrc=6):
    r=LCG(seed); N=len(A); acc=[]
    for _ in range(nsrc):
        d=bfs(A,int(r.rnd()*N)); c=[0]*(max(d)+1)
        for x in d: c[x]+=1
        cum=[]; s=0
        for x in c: s+=x; cum.append(s)
        if len(acc)<len(cum): acc += [acc[-1] if acc else 0]*(len(cum)-len(acc))
        for i in range(len(acc)): acc[i]+=cum[i] if i<len(cum) else cum[-1]
    acc=[x/nsrc for x in acc]; lo=N*.03; hi=N*.30; r1=r2=-1
    for i in range(1,len(acc)):
        if acc[i]>=lo and r1<0: r1=i
        if acc[i]<=hi: r2=i
    return float('nan') if r1<1 or r2<=r1 else (math.log(acc[r2])-math.log(acc[r1]))/(math.log(r2)-math.log(r1))

# B/C: tetra complex helpers

def tet(x): return tuple(sorted(x))
def faces(t):
    a,b,c,d=t; return [tet(x)[:3] for x in [(a,b,c),(a,b,d),(a,c,d),(b,c,d)]]
def edges(t):
    a,b,c,d=t; return [tuple(sorted(x)) for x in [(a,b),(a,c),(a,d),(b,c),(b,d),(c,d)]]
def validate(ts):
    tr=Counter(); ed=set(); vs=set()
    for t in ts: vs.update(t); tr.update(faces(t)); ed.update(edges(t))
    V,E,F,T=len(vs),len(ed),len(tr),len(ts); bad=sum(1 for c in tr.values() if c!=2)
    return V,E,F,T,V-E+F-T,F==2*T,bad==0,bad

def boundary4():
    v=[0,1,2,3,4]; return [tet(x for x in v if x!=omit) for omit in v]
def move14(ts,idx,v):
    a,b,c,d=ts[idx]; return ts[:idx]+ts[idx+1:]+[tet(x) for x in [(v,b,c,d),(a,v,c,d),(a,b,v,d),(a,b,c,v)]]
def move41(ts,v):
    cont=[t for t in ts if v in t]
    if len(cont)!=4: return None
    oth=set(x for t in cont for x in t if x!=v)
    if len(oth)!=4: return None
    return [t for t in ts if v not in t]+[tet(oth)]

def spatial_tris(L):
    def sid(x,y): return (y%L)*L+(x%L)
    out=[]
    for y in range(L):
        for x in range(L):
            a=sid(x,y); b=sid(x+1,y); c=sid(x,y+1); d=sid(x+1,y+1)
            out += [tet((a,b,c))[:3], tet((b,d,c))[:3]]
    return out

def foliated(L,T):
    time={}
    def vid(s,t):
        v=(t%T)*L*L+s; time[v]=t%T; return v
    ts=[]
    for t0 in range(T):
        u=(t0+1)%T
        for a,b,c in spatial_tris(L):
            ts += [tet((vid(a,t0),vid(b,t0),vid(c,t0),vid(c,u))), tet((vid(a,t0),vid(b,t0),vid(b,u),vid(c,u))), tet((vid(a,t0),vid(a,u),vid(b,u),vid(c,u)))]
    return ts,time

def classify(t,time,T):
    ss=sorted(set(time[v] for v in t))
    if len(ss)!=2: return None
    if ss[1]-ss[0]==1: lo,hi=ss
    elif ss[1]-ss[0]==T-1: lo,hi=ss[1],ss[0]
    else: return None
    return (sum(time[v]==lo for v in t), sum(time[v]==hi for v in t), lo, hi)

def fol_check(ts,time,T,L):
    cnt=Counter(); bad=0; own=defaultdict(list)
    for i,t in enumerate(ts):
        c=classify(t,time,T)
        if c and c[:2] in [(3,1),(2,2),(1,3)]: cnt[c[:2]]+=1
        else: bad+=1
        for f in faces(t): own[f].append(i)
    sp=ok=spbad=0
    for f,ids in own.items():
        if len({time[v] for v in f})==1:
            sp+=1; cc=Counter(classify(ts[i],time,T)[:2] for i in ids if classify(ts[i],time,T))
            if cc==Counter({(3,1):1,(1,3):1}): ok+=1
            else: spbad+=1
    return cnt,bad,sp,ok,spbad,(bad==0 and sp==2*L*L*T and spbad==0 and cnt[(3,1)]==cnt[(1,3)])

def move26(ts,time,T):
    own=defaultdict(list)
    for i,t in enumerate(ts):
        for f in faces(t): own[f].append(i)
    newv=max(time)+1
    for f,ids in own.items():
        if len({time[v] for v in f})!=1 or len(ids)!=2: continue
        data=[(classify(ts[i],time,T),i) for i in ids]
        if Counter(c[:2] for c,i in data if c)!=Counter({(3,1):1,(1,3):1}): continue
        a,b,c=f; up=next(i for c0,i in data if c0[:2]==(3,1)); dn=next(i for c0,i in data if c0[:2]==(1,3))
        p=next(v for v in ts[up] if v not in f); q=next(v for v in ts[dn] if v not in f); time[newv]=time[a]
        keep=[t for i,t in enumerate(ts) if i not in (up,dn)]
        return keep+[tet(x) for x in [(a,b,newv,p),(b,c,newv,p),(a,c,newv,p),(a,b,newv,q),(b,c,newv,q),(a,c,newv,q)]],time
    raise RuntimeError('no move26 site')

def runA():
    print('## A flat 2+1')
    print('| side | V | diam | ball | spectral | degree |'); print('|---:|---:|---:|---:|---:|---:|')
    Ns=[]; Ds=[]
    for s in [6,8,10,14]:
        A=flat_graph(s); N=len(A); d=diam(A,s); Ns.append(N); Ds.append(d)
        print(f'| {s} | {N} | {d} | {ball(A,s):.2f} | {spec(A,s):.2f} | {sum(map(len,A))/N:.2f} |')
    sl=slope(Ns,Ds); print(f'\ndiameter_slope={sl:.3f}\ndiameter_dimension={1/sl:.2f}\n')
    print('| rewire | V | diam | ball | spectral |'); print('|---:|---:|---:|---:|---:|')
    base=flat_graph(14)
    for f in [0,.05,.15,.30]:
        A=base if f==0 else rewire(base,f,12345)
        print(f'| {f:.2f} | {len(A)} | {diam(A,9)} | {ball(A,10):.2f} | {spec(A,11):.2f} |')

def runB(m=5):
    print('## B bistellar')
    print('| step | move | V | E | F | T | chi | F2T | pseudo | bad |'); print('|---:|---|---:|---:|---:|---:|---:|---|---|---:|')
    ts=boundary4(); ins=[]
    def row(k,mv):
        V,E,F,T,chi,F2T,p,b=validate(ts); print(f'| {k} | {mv} | {V} | {E} | {F} | {T} | {chi} | {F2T} | {p} | {b} |')
    row(0,'initial')
    for k in range(m):
        v=max(max(t) for t in ts)+1; ts=move14(ts,0,v); ins.append(v); row(k+1,f'(1,4) {v}')
    for k,v in enumerate(reversed(ins),1):
        nt=move41(ts,v)
        if nt is not None: ts=nt
        row(f'rollback {k}',f'(4,1) {v}')

def runC(L=3,T=4,m=5):
    print('## C foliated 3-torus')
    print('| step | V | E | F | Tets | chi | F2T | pseudo | 3,1 | 2,2 | 1,3 | invalid | spacelike | foliation |'); print('|---:|---:|---:|---:|---:|---:|---|---|---:|---:|---:|---:|---:|---|')
    ts,time=foliated(L,T)
    for k in range(m+1):
        V,E,F,Tn,chi,F2T,p,b=validate(ts); cnt,bad,sp,ok,spbad,fol=fol_check(ts,time,T,L)
        print(f'| {k} | {V} | {E} | {F} | {Tn} | {chi} | {F2T} | {p} | {cnt[(3,1)]} | {cnt[(2,2)]} | {cnt[(1,3)]} | {bad} | {sp} | {fol} |')
        if k<m: ts,time=move26(ts,time,T)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--mode',choices=['A','B','C','all'],default='all'); ap.add_argument('--moves',type=int,default=5); ap.add_argument('--L',type=int,default=3); ap.add_argument('--T',type=int,default=4); a=ap.parse_args()
    if a.mode in ['A','all']: runA(); print()
    if a.mode in ['B','all']: runB(a.moves); print()
    if a.mode in ['C','all']: runC(a.L,a.T,a.moves)
if __name__=='__main__': main()
