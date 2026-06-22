#!/usr/bin/env python3
from __future__ import annotations
import argparse, math, random, statistics
from collections import deque

def fit_slope(xs, ys):
    pairs=[(x,y) for x,y in zip(xs,ys) if x>0 and y>0]
    X=[math.log(x) for x,y in pairs]; Y=[math.log(y) for x,y in pairs]
    if len(X)<2: return float('nan')
    mx=sum(X)/len(X); my=sum(Y)/len(Y)
    den=sum((x-mx)**2 for x in X)
    return sum((x-mx)*(y-my) for x,y in zip(X,Y))/den if den else float('nan')

def width_scaling():
    cases=[
        ("string constant width", lambda n: 8.0),
        ("2D target sqrt width", lambda n: math.sqrt(n)),
        ("crumpled linear width", lambda n: n/12),
        ("fractal 1.5 target", lambda n: n**(1/3)),
    ]
    Ns=[200,500,1000,2000,5000,10000]
    print("| case | beta width~N^β | d≈1/(1-β) | widths |")
    print("|---|---:|---:|---|")
    for name,fn in cases:
        ws=[fn(n) for n in Ns]
        beta=fit_slope(Ns,ws)
        dim=1/(1-beta) if beta<1 else float("inf")
        print(f"| {name} | {beta:.3f} | {dim:.2f} | {', '.join(str(round(w,1)) for w in ws)} |")

def branching(seed=0, steps=400):
    rng=random.Random(seed)
    regimes={
        "death":(.86,.93),
        "balanced-string":(.90,.90),
        "critical-fractal":(.955,.955),
        "birth-explosion":(1.05,.90),
    }
    print("| regime | final width | max width | beta estimate | verdict |")
    print("|---|---:|---:|---:|---|")
    for name,(birth,death) in regimes.items():
        width=10.0; widths=[]
        for _t in range(1,steps+1):
            noise=(rng.random()+rng.random()-1)*0.6*math.sqrt(max(width,1))
            width=max(0.0,width + (birth-death)*width*0.05 + noise)
            if name=="critical-fractal":
                width=max(1.0,width + (rng.random()+rng.random()-1)*math.sqrt(width)*0.8)
            if name=="birth-explosion" and width>1e5: break
            widths.append(width)
        xs=list(range(1,len(widths)+1))
        tail=widths[-max(20,len(widths)//2):]
        beta=fit_slope(xs[-len(tail):], [max(1,w) for w in tail])
        verdict="dies" if widths[-1]<2 else "explodes" if max(widths)>1000 else "string-like" if max(widths)<50 else "fractal/watch"
        print(f"| {name} | {widths[-1]:.1f} | {max(widths):.1f} | {beta:.2f} | {verdict} |")

def balance(seed=0, steps=260):
    print("| initial width | final width | mean last 50 | std last 50 |")
    print("|---:|---:|---:|---:|")
    for w0 in [3,10,30,100]:
        rng=random.Random(seed+w0); w=float(w0); hist=[]
        target=18.0
        for _t in range(steps):
            feedback=0.045*(target-w)
            noise=(rng.random()+rng.random()-1)*0.45*math.sqrt(max(w,1))
            w=max(1.0,w+feedback+noise)
            hist.append(w)
        tail=hist[-50:]
        print(f"| {w0} | {w:.2f} | {statistics.mean(tail):.2f} | {statistics.pstdev(tail):.2f} |")

def graph_diameter(n, edges):
    adj=[[] for _ in range(n)]
    for a,b in edges:
        if a==b: continue
        adj[a].append(b); adj[b].append(a)
    def bfs(s):
        d=[-1]*n; d[s]=0; q=deque([s])
        while q:
            u=q.popleft()
            for v in adj[u]:
                if d[v]<0: d[v]=d[u]+1; q.append(v)
        return d
    d0=bfs(0); a=max(range(n), key=lambda i:d0[i])
    d1=bfs(a); return max(d1)

def third(seed=0, N=5000):
    rng=random.Random(seed)
    print("| relation cell | causal order | events | depth/diameter | width | d hint | verdict |")
    print("|---|---|---:|---:|---:|---:|---|")
    edges=[]
    for i in range(N):
        for _ in range(2):
            j=rng.randrange(N)
            if i!=j: edges.append((i,j))
    diam=graph_diameter(N, edges)
    print(f"| edge/pair | no | {N} | {diam} | {N} | inf | crumpled/small-world |")
    depth=N; width=1; dh=math.log(N)/math.log(depth)
    print(f"| edge/pair | yes | {N} | {depth} | {width} | {dh:.2f} | string |")
    edges=set()
    for _ in range(N):
        tri=rng.sample(range(N),3)
        for a,b in [(tri[0],tri[1]),(tri[1],tri[2]),(tri[0],tri[2])]:
            edges.add(tuple(sorted((a,b))))
    diam=graph_diameter(N, list(edges))
    print(f"| triangle/third | no | {N} | {diam} | {N} | inf | crumpled/small-world |")
    levels=[]; total=0; l=0
    while total<N:
        width_l=l+1
        levels.append(min(width_l,N-total))
        total+=levels[-1]; l+=1
    depth=len(levels); width=max(levels); dh=math.log(N)/math.log(depth)
    print(f"| triangle/third | yes | {N} | {depth} | {width} | {dh:.2f} | 2D-like sheet |")

def soc(seed=0, L=64, drives=12000, burn=1000):
    rng=random.Random(seed)
    grid=[[0]*L for _ in range(L)]
    aval=[]
    for step in range(drives):
        x=rng.randrange(L); y=rng.randrange(L); grid[y][x]+=1
        q=deque()
        if grid[y][x]>=4: q.append((x,y))
        size=0
        while q:
            x,y=q.popleft()
            if grid[y][x]<4: continue
            topple=grid[y][x]//4
            grid[y][x]-=4*topple
            size += topple
            for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                nx=x+dx; ny=y+dy
                if 0<=nx<L and 0<=ny<L:
                    grid[ny][nx]+=topple
                    if grid[ny][nx]>=4: q.append((nx,ny))
        if step>=burn and size>0: aval.append(size)
    bins=[]
    b=1
    maxs=max(aval) if aval else 1
    while b<maxs:
        hi=int(b*1.6)+1
        bins.append((b,hi)); b=hi
    xs=[]; ys=[]
    for lo,hi in bins:
        c=sum(1 for s in aval if lo<=s<hi)
        if c>0 and hi>lo:
            xs.append(math.sqrt(lo*hi)); ys.append(c/len(aval)/(hi-lo))
    sl=fit_slope(xs,ys)
    tau=-sl
    print("| L | drives | avalanches | max avalanche | tau pdf fit | mean size |")
    print("|---:|---:|---:|---:|---:|---:|")
    print(f"| {L} | {drives} | {len(aval)} | {max(aval) if aval else 0} | {tau:.2f} | {statistics.mean(aval):.2f} |")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["width-scaling","branching","balance","third","soc","all"], default="all")
    ap.add_argument("--seed", type=int, default=0)
    args=ap.parse_args()
    if args.mode in ("width-scaling","all"):
        print("## width scaling"); width_scaling(); print()
    if args.mode in ("branching","all"):
        print("## naive branching"); branching(args.seed); print()
    if args.mode in ("balance","all"):
        print("## balance feedback"); balance(args.seed); print()
    if args.mode in ("third","all"):
        print("## third / simplex grammar"); third(args.seed); print()
    if args.mode in ("soc","all"):
        print("## BTW sandpile SOC"); soc(args.seed)

if __name__ == "__main__":
    main()
