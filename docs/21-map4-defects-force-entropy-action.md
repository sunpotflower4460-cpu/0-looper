# 21 — Map 4 merge: defects, force, metric curvature, entropy/action frontier

## 目的

Claude 側の A 系列メモを repo 側へ合流する。

今回の主題は、空間創発の次に来る「物質 / 欠陥 / 力 / 曲率 / 作用」の橋。

中心の鎖：

```text
差
→ 欠陥 / 物質
→ 欠陥同士の力
→ 欠陥が空間を曲げる
→ 空間の計量が力を媒介する
→ 残る本丸 = 幾何の作用そのものはどこから来るか
```

## 追加 scripts

```text
scripts/defect_metric_curvature.py
scripts/vortex_metric_force.py
scripts/entropy_action_frontier.py
```

これらは Claude sandbox の A3/A4/A5 を repo 側で追うための lightweight reproducer。  
A1/A1b/A2 は Claude sandbox measured として合流し、repo 側では今後必要なら追加する。

## A3 — 計量こそが力を生む

`scripts/vortex_metric_force.py`

XY field 上に `+/-` vortex pair を置き、separation を変えたときの field energy を測る。

場のエネルギー：

```text
E = Σ_edges (1 - cos(Δθ))
```

比較：

```text
field / metricあり     : energy depends on separation
combinatorial local cost: defect cost q²+q² only, separation independent
```

読み：

> 計量のある場では、欠陥間の距離がエネルギーに入る。  
> つまり、エネルギー勾配として力が読める。  
> 一方、局所的な組み合わせコストだけでは、欠陥が離れても同じなので、力がない。

claim tier:

```text
measured toy check + interpretive
```

まだ言わないこと：

```text
実在の重力や電磁気を導いた。
```

## A4 — 欠陥 / 物質が graph metric を曲げる

`scripts/defect_metric_curvature.py`

三角形格子の cone toy を作る。

```text
sectors = 6 : flat triangular lattice
sectors = 5 : missing wedge / positive defect / positive curvature
sectors = 7 : extra wedge / negative defect / negative curvature
```

外から Euclidean metric を入れず、中心欠陥からの graph distance だけで見る。

見るもの：

```text
sphere circumference at graph radius r
ball area within graph radius r
```

典型的な読み：

```text
positive defect: circumference and area are smaller than flat
flat          : circumference ~ 6r
negative defect: circumference and area are larger than flat
```

これは、欠陥が周囲の graph metric を変えるという reduced mechanism check。

重要：

> 欠陥＝曲率を角度として外から割り当てるだけでなく、関係と graph distance から円周/面積の変化として読める。

claim tier:

```text
measured in conical graph toy
```

## A5a — 力はエントロピー / 数えることから出る

`scripts/entropy_action_frontier.py --mode spring`

1D random-walk chain の endpoint count を厳密に数える。

全ての walk configuration は同じ重み。  
つまり、課したエネルギーはゼロ。

しかし endpoint displacement `R` が大きいほど、対応する configuration 数が減る。

```text
F(R) = -ln P(R)
F(R) - F(0) ~ R² / (2N)
```

読み：

> 純粋に数えることだけから、戻す力 = entropic spring が出る。  
> 力はエントロピーから創発しうる。

claim tier:

```text
measured / known Gaussian-chain elasticity / analogy to entropic force
```

## A5b — しかし平らさの作用は、素朴なエントロピーからは出ない

`scripts/entropy_action_frontier.py --mode flips`

`triangulation_flip.py` の torus triangulation に対して、flatness action を使わず、可能な Pachner 2-2 flips をランダムに受け入れる。

見るもの：

```text
degree variance = curvature fluctuation
average graph distance = crumpling / shortcut tendency
```

読み：

> 純粋な entropy-only random flips は、平らさを選ばない。  
> むしろ degree variance が増え、距離が縮み、crumpling へ寄る。

これが A5 の重要な二段結論。

```text
A5a: 力は数えることから出る。
A5b: しかし幾何を平らに保つ作用は、素朴な数の最大化だけでは出ない。
```

つまり、#4 の本丸は残る。

claim tier:

```text
measured toy check
```

## A 系列の整理

Claude sandbox での A 系列の全体像：

| track | 何を示したか | claim |
|---|---|---|
| A1 | 一規則で `+/-` は引き合い対消滅、`+/+` は反発 | measured in XY/GL sandbox, analogy |
| A1b | quench で欠陥が生まれ、正味巻き数が釣り合う | measured, topology |
| A2 | metric なしの組み合わせでは欠陥は引き合わず凍る | measured |
| A3 | metric field では pair energy が距離依存 = 力 | measured + interpretive |
| A4 | defect が graph metric を曲げる | measured |
| A5a | entropic spring = force from counting | measured / known physics analogy |
| A5b | entropy-only geometry crumples; flatness action does not emerge naively | measured |

repo 側で今回追加したのは A3/A4/A5 の lightweight checks。

## 三つのビジョンへの対応

### 1. 最初の差から強制展開

物質の toy level では強くなってきた。

```text
差
→ 欠陥
→ 正味ゼロ / topological balance
→ attraction / repulsion / annihilation
→ order restoration
```

ただし、場のエネルギー規則そのものはまだ置いている。

### 2. 完全な平らは要件ではない、欠陥が世界

平らな空間だけでは空っぽ。  
欠陥があることで、物質・曲率・力が現れる。

```text
defect = matter-like excitation
matter-like defect bends metric
metric mediates force
```

### 3. 物質と空間は幾何を介して一つに結ばれる

A4 と A3 を合わせると、GR 的な型が見える。

```text
matter / defect -> curvature / changed graph metric
metric geometry -> force between defects
```

ただしこれは GR の導出ではなく、GR 型の toy correspondence。

## まだ課しているもの

最深の残りはここ。

```text
場 / エネルギー / 落ち着け規則 / 幾何の作用
```

A5a で、力が entropy から出る例は確認した。  
A5b で、幾何の flatness action は素朴な entropy からは出ず、むしろ crumple へ行くことも確認した。

したがって、正直な frontier は：

```text
幾何の作用そのものが、より深い entropy / thermodynamics / causal restriction から出るか。
```

CDT は因果制限によって潰れを避ける既知の道。  
Jacobson / Verlinde 的な horizon thermodynamics は、より深い未解決の道。

## 次の攻め口

### A6 — 物質は空間の動力学に反作用するか

A4 は静的に、欠陥周りの metric が曲がることを見た。  
次は動的に見る。

```text
move defect
→ update local triangulation / metric
→ circumference / area profile follows defect?
```

### A7 — #4 の本丸に正面から

A5b と CDT をつなぐ。

```text
entropy-only flips crumple
causal restriction avoids crumple
```

問い：

```text
causal restriction は、作用を entropy から出す一形態か。
```

### A8 — 空間と物質を一つの動力学で動かす

一番重要。

```text
triangulation / metric
+ field / defects
+ coupled update
```

Regge-calculus 的に、metric が matter に応じて曲がり、matter が metric に沿って動くかを見る。

ここが「関係の反応、それだけ」に最も近い。

## 現在地の合言葉

> 欠陥は空間の上に乗るだけではない。  
> 欠陥は graph metric を曲げ、metric は欠陥同士の力を媒介する。  
> しかし、その metric を平らに保つ作用そのものは、まだ最後の本丸として残る。
