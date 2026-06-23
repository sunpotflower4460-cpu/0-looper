# 23 — Scale spiral, key/equivalence, quantum-white view, and 3D start

## 目的

同期資料3 `見方から物理へ — スケール螺旋・キー・等価原理・第三、そして3D開始` と、今日の総括を repo 側へ合流する。

今回の主題は、うえきの見方を測れる物理構造に翻訳すること。

```text
直感 / 対比
→ 測れる構造
→ 物理へ当てる
→ claim tier を保つ
→ 影があるものだけ残す
```

## 今回の中心到達点

```text
関係 + 変化 + エントロピーから宇宙構造が組み上がる絵は据えた。
今回は、重力=キー、螺旋=離散スケール不変、白=最大対称性、
量子=差が可逆になめらかに動く形、等価原理=移調、曲率=第三、
そして3D開始を、測れる構造へ翻訳した。
```

## 追加 scripts

```text
scripts/efimov_dsi.py
scripts/rg_limit_cycle.py
scripts/gravity_as_key.py
scripts/curvature_on_faces.py
scripts/dimensional_transmutation.py
scripts/ball_growth_3d.py
```

これらは reduced mechanism check / known physics reproduction。  
physics verification ではなく、0-looper の CI で考え方を壊さないための軽量チェックとして扱う。

## 1. Quantum view — なぜ量子でないと成り立たないか

今回の理解：

```text
量子 = 差が、なめらかに・可逆に・安定して動ける形
```

三つの理由：

1. 安定：原子が潰れず、基底状態がある。
2. 有限：紫外発散を飛び飛び性が止める。
3. 差が動ける：0→1を純粋状態のまま連続回転できる。

claim tier:

```text
(1)(2) = known physics
(3) = interpretive but grounded
quantum reconstruction = frontier
```

ここはまだ repo script にはしていない。  
将来やるなら、Bloch sphere / reversible pure-state path の小さな可視化を追加する。

## 2. 螺旋 = 離散スケール不変 DSI

`scripts/efimov_dsi.py`

スケールフリーな構造が、条件によって等比の梯子を作る。

```text
g > 1/4:
  s0 = sqrt(g - 1/4)
  ratio = exp(2π / s0)

g <= 1/4:
  ladder absent
```

重要な読み：

```text
比は構造 g が決める。
アンカーは自由。
アンカーを動かすと梯子全体は動くが、比は変わらない。
```

claim tier:

```text
measured formula-level DSI / known mechanism
universe is spiral = frontier
```

## 3. RG fixed point vs limit cycle

`scripts/rg_limit_cycle.py`

固定点：

```text
coupling constant across ln(scale)
```

リミットサイクル：

```text
coupling rotates in ln(scale)
observable has log-periodic wave
```

今回の見方では、

```text
固定点 = 何も選ばないスケール不変
リミットサイクル = 回って戻るが一段ズレる螺旋
```

claim tier:

```text
measured toy flow
cosmic log periodicity = frontier
```

## 4. 重力 = キー / 等価原理 = 移調

`scripts/gravity_as_key.py`

三つの既知構造を測る。

### 4.1 打ち消せない

```text
mass is single sign
net source accumulates
no gravitational shielding
```

電荷は正負で打ち消せる。  
質量は基本的に単一符号なので、遮蔽できない。

### 4.2 等価原理 = 移調

```text
uniform field: relative acceleration = 0
潮汐 / 曲率: relative acceleration != 0
```

一様な場は自由落下で消える。  
潮汐は消えない。

### 4.3 普遍性

```text
a = GM / r²
```

test mass が消えるので、全部同じに落ちる。

claim tier:

```text
known physics reproduction
music/key analogy = interpretive, limited
```

正直な線：機能和声の豊かさまでは対応しない。  
一致するのは、普遍・打ち消し不可・一様場ゲージの骨格。

## 5. 曲率は第三 / 面に宿る

`scripts/curvature_on_faces.py`

三角形格子の頂点まわりで、

```text
angle deficit = 2π - deg * π/3
```

を見る。

```text
deg5: positive curvature / missing wedge
deg6: flat
deg7: negative curvature / extra wedge
```

1D の道では面を囲めないので、曲率を読めない。

重要な読み：

```text
曲率は辺だけに宿らない。
面 = 第三 = 2-cell が必要。
```

claim tier:

```text
measured combinatorial check
curvature and dimension share the third = interpretive but grounded
```

## 6. 矢はズレにあり、円にはない

今回の整理：

```text
pure rotation = reversible / no arrow
circle + drift = spiral / arrow
```

ズレには二種類ある。

```text
scale drift: RG / DSI / UV→IR
time drift : entropy / low-entropy boundary
```

言いすぎない線：

```text
時間の矢 = スケールの矢
```

とは言わない。  
同じ幾何モチーフを共有するが、別軸の現象。

## 7. スケール：ゲージか、自己生成か

`scripts/dimensional_transmutation.py`

次元的転移：

```text
dg / d ln(mu) = - b g²
Lambda / mu0 = exp(-1 / (b g0))
```

小さな dimensionless coupling から、指数的な scale hierarchy が出る。

claim tier:

```text
known mechanism reproduction / dimensional transmutation
absolute Planck scale derived = no
```

重要な訂正：

```text
等価原理: 一様な gravitational field がゲージ = standard GR
scale itself as gauge: standard GR ではない。conformal gravity 等の frontier
```

つまり、

```text
関係が一次
```

は維持できるが、

```text
スケール完全ゲージ
```

は未確定。

## 8. 白 / 観測・非観測

今回の理解：

```text
白 = 最大対称性 = 区別ゼロ = 情報ゼロ = 自分を知れない
```

最大対称性は安定というより、しばしば不安定な丘の頂点。  
最小のゆらぎで差が立つ。

観測の見方：

```text
非観測 = 重ね合わせ / 白 / 未分化
観測   = 差 / 関係 / 対称性の破れ
```

claim tier:

```text
interpretive / RQM and measurement problem are frontier
```

## 9. レシピ / 約25の純粋な数

今回の整理：

```text
なぜこのレシピか = なぜこの関係たちか
```

単位のない数は、比 = 関係。  
ワインバーグ角は、定数が幾何的な角度でありうる実例。

claim tier:

```text
known + frontier
```

## 10. 3D第一歩 — ball growth calibration

`scripts/ball_growth_3d.py`

これは創発ではなく、3D測定器の較正。

```text
hand-built cubic lattice = 3D by construction
finite size suppresses measured slope
L grows -> slope approaches 3 slowly
```

比較：

```text
clean cubic lattice      : local 3D calibration
local edge dilution      : dimension-like growth is robust
nonlocal shortcuts       : small-world / dimension breaks
```

claim tier:

```text
measured calibration + correction
3D emergence = not yet
```

重要な訂正：

```text
ball growth d≈2.56 は 3D と言い切る値ではなく、有限サイズ + 壁で抑えられた値。
```

## 11. 次の3Dフェーズ

次は、手で組んだ3D lattice ではなく、ランダムな2D slices を因果順に局所的に積む。

```text
random 2D slices
+ causal stacking
+ local gluing
→ 3D-like ball growth?

break causality / add nonlocal shortcuts
→ crumple / small-world?
```

これは 2D CDT の 3D 版の軽量最小チェック。  
完全な 3+1 CDT ではなく、0-looper で回せる reduced mechanism check から始める。

## 12. claim discipline summary

言ってよいこと：

```text
量子・螺旋・重力キー・等価原理・曲率第三・次元的転移・3D局所性の教訓を、0-looper の reduced scripts に落とした。
3Dについては測定器の較正と局所/非局所コントラストまで。
```

まだ言わないこと：

```text
宇宙が螺旋だと示した。
スケールが完全ゲージだと示した。
量子重力を解いた。
3D創発を示した。
絶対スケールを導出した。
```

## 現在地の合言葉

> 座標は低い巻く位相として読める。  
> 曲率は第三に宿る。  
> 重力はキーのように打ち消せず、一様場は移調できる。  
> そして3D性は、手で作った立体ではなく、局所性が守るかどうかで試される。
