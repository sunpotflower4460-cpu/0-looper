# 22 — Map 4 full sync: matter, gravity, and space-matter unification

## 目的

アップロード資料 `0-looper 合流マップ4：物質・重力・空間と物質の統一` を repo 側へ完全合流する。

前ドキュメント `docs/21-map4-defects-force-entropy-action.md` では A3/A4/A5 を先に入れた。  
今回の full sync では、PDF の依頼どおり、特に以下を追加する。

```text
A1 / A1b : vortex dynamics and quench coarsening
A7       : causal restriction against entropy-only crumpling
A6       : gravitational instability / co-evolution
A10      : weak lensing alpha ~ 1/b
A11      : self-gravity chicken/egg equilibrium
```

## PDFの核

資料の問い：

```text
欠陥（＝物質）の動力学・引力・対消滅・重力は、僕らが命じた結果か、
一つの最小規則から強制された帰結か。
```

資料の暫定回答：

```text
多くは強制された帰結。
唯一残る「課したもの」は、作用 / 規則そのもの = #4。
```

## 追加 scripts

```text
scripts/vortex_tdgl.py
scripts/causal_constraint.py
scripts/gravity_toys.py
```

これにより、Map 4 の repo 側 scripts は以下になった。

```text
scripts/vortex_tdgl.py
scripts/vortex_metric_force.py
scripts/defect_metric_curvature.py
scripts/entropy_action_frontier.py
scripts/causal_constraint.py
scripts/gravity_toys.py
```

## A1 / A1b — 物質の動力学は強制されるか

`scripts/vortex_tdgl.py`

軽量な XY / TDGL-like phase relaxation model を入れた。

更新則：

```text
theta_t += eta * Σ_neighbors sin(theta_neighbor - theta)
```

これは full complex Ginzburg-Landau ではないが、XY energy descent と vortex charge の基本を測る。

### controlled pair

見るもの：

```text
+/- pair : attraction / annihilation tendency
++ pair  : non-annihilation / repulsion or escape tendency
energy descent
```

### quench coarsening

ランダム phase field から出発し、vortex charge を plaquette winding で数える。

見るもの：

```text
+ defects
- defects
net charge
total defects
energy
```

claim tier：

```text
measured toy check / XY analogy
```

正直な線：

```text
full GL / TDGL ではない。
実在粒子ではない。
しかし、ランダムな差から欠陥が出て、+/- がトポロジー的に釣り合い、緩和で減ることを見る足場。
```

## A2 / A3 — 物質の力は計量が媒介する

A2 は Claude sandbox measured として合流。  
repo 側では A3 を `scripts/vortex_metric_force.py` に入れている。

整理：

```text
組み合わせ / 計量なし:
  Σ(deg-6)^2 は局所的なので、欠陥間距離に依存しない。
  したがって力が読めない。

field / 計量あり:
  XY pair energy は距離に依存する。
  energy gradient が力として読める。
```

claim tier：

```text
measured toy check + interpretive
```

## A4 — 物質は空間を曲げる

`scripts/defect_metric_curvature.py`

cone graph toy により、欠陥周りの graph-distance circumference / ball area を測る。

```text
sectors=5: positive defect / missing wedge / smaller circumference
sectors=6: flat / circumference ~ 6r
sectors=7: negative defect / extra wedge / larger circumference
```

重要点：

> 外から Euclidean metric を入れず、関係と graph distance だけから曲率らしさを読む。

claim tier：

```text
measured in conical graph toy
```

## A5 / A7 — 作用はエントロピーから出るか

### A5a: entropic spring

`scripts/entropy_action_frontier.py --mode spring`

全 configuration が同じ重みの random walk chain で、endpoint count だけから

```text
F(R) = -ln P(R) ~ R² / (2N)
```

が出る。

読み：

```text
力は数えること / entropy から出うる。
```

### A5b: entropy-only flips crumple

`scripts/entropy_action_frontier.py --mode flips`

flatness action なしで Pachner flips をランダムに受け入れると、degree variance が上がり、average distance が縮む。

読み：

```text
素朴な entropy 最大化は、幾何を平らに保たず、むしろ crumple へ寄る。
```

### A7: causal restriction

`scripts/causal_constraint.py`

entropy-only random flips と、causal/layered restriction proxy を比較する。

これは full CDT Monte Carlo ではない。  
しかし、次の構図を CI で確認するための reduced mechanism check。

```text
entropy-only unconstrained flips : shortened distance / crumpling tendency
causal layered proxy             : extended distance scale remains
```

claim tier：

```text
reduced mechanism check
not full CDT action derivation
```

## A6 / A10 / A11 — 重力と構造

`scripts/gravity_toys.py`

### A6: gravitational instability

Jeans-like amplitude competition として、gravity growth と diffusion smoothing を比較する。

```text
d(delta)/dt = (G - Dk²) delta
```

読み：

```text
gravity + diffusion: contrast grows
no gravity / diffusion only: contrast is erased
```

これは full cosmological simulation ではない。  
しかし「小さな差が gravity feedback で構造になる」という最小足場。

### A10: weak lensing

点質量の Newtonian potential の transverse gradient を z 方向に積分し、GR factor 2 を入れた weak-field lensing proxy。

見るもの：

```text
alpha(b) ~ 1/b
b * alpha ≈ constant
```

claim tier：

```text
measured reduced weak-field lensing integral / analogy to GR lensing
```

### A11: self-gravity chicken/egg equilibrium

1D で次を反復する。

```text
rho ∝ exp(-phi/T)
phi'' = rho - mean(rho)
```

読み：

```text
matter distribution creates potential
potential shapes matter distribution
iteration converges to a bound self-consistent profile
```

claim tier：

```text
measured reduced self-consistency toy
```

## A系列の全体表

| track | repo status | 何を示すか | claim tier |
|---|---|---|---|
| A1 | `vortex_tdgl.py` | `+/-` と `++` の違いが energy descent から出る | measured toy / analogy |
| A1b | `vortex_tdgl.py` | random quench から欠陥が出て、正味 charge が釣り合い、減る | measured toy / topology |
| A2 | Claude sandbox measured | metric なしの組み合わせでは欠陥は引き合わず凍る | measured |
| A3 | `vortex_metric_force.py` | metric field では pair energy が距離依存 = force | measured + interpretive |
| A4 | `defect_metric_curvature.py` | defect が graph metric を曲げる | measured toy |
| A5a | `entropy_action_frontier.py` | entropic spring = force from counting | measured / known physics analogy |
| A5b | `entropy_action_frontier.py` | entropy-only geometry crumples | measured toy |
| A7 | `causal_constraint.py` | causal/layered restriction keeps extension | reduced mechanism check |
| A6 | `gravity_toys.py` | gravity feedback grows structure | reduced mechanism check |
| A10 | `gravity_toys.py` | lensing alpha ~ 1/b | reduced weak-field check |
| A11 | `gravity_toys.py` | matter↔potential self-consistency | reduced self-consistency toy |

## 三つの深い型

### 1. 正味ゼロをトポロジーが強制する

空間では Gauss-Bonnet。  
場では winding number / vortex charge。  
どちらも、対立物の釣り合いが外から命じられずに出る。

### 2. 第三と計量は irreducible

```text
空間: 関係だけでは足りない。第三 / face / curvature control が要る。
物質の力: 関係だけでは足りない。metric が要る。
```

### 3. 鶏卵 = 自己無撞着ループ

A11 の matter↔potential、DFT 的 self-consistency、オートポイエーシス、これらは同じ型。

```text
structure shapes field
field shapes structure
fixed point is not input but self-consistent solution
```

## グランドな鎖

```text
0≠無
→ 変化
→ 因果 = 時間
→ 因果 + 関係 + 第三
→ 空間
→ 最初の差が釣り合った物質 / 欠陥を強制
→ 一規則が物質の動力学を強制
→ 物質が空間を曲げる
→ 計量が物質の力を媒介する
→ 曲がった空間が物質・光を導く
→ co-evolution が構造を生む
→ 自己無撞着な束縛構造に閉じる
→ 残るは作用 / 規則そのもの = #4
```

## claim discipline

言ってよいこと：

```text
Map 4 の A 系列を repo 側に合流し、A1/A1b/A3/A4/A5/A7/A6/A10/A11 の lightweight checks を追加した。
欠陥 = 物質的 excitation、欠陥が graph metric を曲げる、metric が defect force を媒介する、という GR 型の toy correspondence が見えている。
```

まだ言わないこと：

```text
本物のGRを導いた。
重力を根本原理から完全導出した。
物質や粒子を実在レベルで作った。
幾何の作用そのものを entropy / causal restriction から完全導出した。
```

## 次の本丸

### A6 dynamic backreaction

A4 は静的 cone。次は defect を動かし、graph metric / triangulation が追随するか。

### A7 stronger CDT bridge

entropy-only crumple と causal restriction を、より CDT に近い flip system で比較する。

### A8 unified matter-geometry dynamics

```text
triangulation / metric
+ field / defects
+ coupled update
```

metric が matter に応じて曲がり、matter が metric に沿って動く。  
ここが「関係の反応、それだけ」に最も近い。

## 現在地の合言葉

> 物質は空間の上に乗るだけではない。  
> 欠陥は graph metric を曲げ、metric は欠陥同士の力を媒介する。  
> しかし、その metric を平らに保つ作用そのものは、まだ #4 の本丸として残る。
