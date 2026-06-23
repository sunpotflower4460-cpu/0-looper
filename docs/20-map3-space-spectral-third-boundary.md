# 20 — Map 3 merge: space emergence, spectral toolbox, third, boundary/entropy bridge

## 目的

`0-looper 合流マップ3：空間創発の深掘り（スペクトル道具箱・第三・開閉バランス・境界/エントロピー橋）` を repo 側へ合流する。

今回の核は2つ。

```text
1. 第三は irreducible。
   関係/辺だけでは、多様体にならず、弦か潰れに落ちやすい。

2. 開と閉の両方が要る。
   閉 = 曲率制御 / 多様体条件 / 作用。
   開 = 揺らぎ / エントロピー / 動き。
   2Dは「閉が支配 + 少し開く」の針の穴。
```

この repo 合流では、PDFの §1-3 と §5-1 を優先して実装した。

## 追加 scripts

```text
scripts/spectral_coord.py
scripts/weyl_dim.py
scripts/remesh_loop.py
scripts/triangulation_flip.py
scripts/boundary_scaling.py
```

## 1. spectral_coord — 座標 = 最低固有モード = 巻く位相

`scripts/spectral_coord.py`

### ring modes

リング上の Laplacian 固有モードは、`k` 回巻く位相として読める。

```text
k = 0 : 定数モード / 巻かない / 0=white
k = 1 : 最初の巻き / 最初の座標軸
k = 2,4,8 : 巻き数2倍 / octave
```

読み：座標とは、線というより「最も低い巻く位相」。  
サイマティクス模様は、同じ空間のより高い固有モード。

### 2D grid coordinates

2D open grid の Laplacian を小さな Jacobi 固有分解で解き、低い非自明固有ベクトルと真の `x/y` 座標の相関を見る。

典型出力：

```text
v2: corr x ≈ 0.99
v3: corr y ≈ 0.99
```

claim tier:

```text
measured in small graph eigensolver
```

注意：

```text
これは小グラフ用の座標抽出。
エンタングルメント・エントロピーには使わない。
```

## 2. weyl_dim — スペクトル次元メーター

`scripts/weyl_dim.py`

Weyl則：

```text
λ_k ~ k^(2/d)
log λ_k vs log k の slope = 2/d
```

repo 側では、1D/2D/3D grid の解析的 Laplacian eigenvalues で検証する。

典型出力：

| graph | d≈2/slope | reading |
|---|---:|---|
| 1D path | ~1.0 | baseline |
| 2D grid | ~1.9-2.0 | baseline |
| 3D grid | ~3.0 | baseline |

shortcut anomaly は、Laplacian spectrum ではなく ball-growth proxy として入れた。  
小世界ショートカットを入れると、clean 2D から外れる。

claim tier:

```text
Weyl baseline = measured / analytic eigenvalues
shortcut anomaly = graph-growth proxy, not strict spectrum
```

## 3. remesh_loop — graph↔coordinate の自己無撞着ループ

`scripts/remesh_loop.py`

鶏卵問題：

```text
graph -> spectral coordinates -> geometric kNN graph -> repeat
```

これは悪循環ではなく、自己無撞着方程式 `X = F(X)` として解く対象。

repo 側では、ランダムグラフから始めて次を比較する。

```text
naive remesh      : 改善後に fragment/collapse しうる
connected remesh  : 安定するが、often string-like fixed point
```

読み：

> ループは閉じるだけでは足りない。  
> 安定化が要る。  
> しかし安定化しても、2Dではなく弦に落ちることがある。

claim tier:

```text
measured in small self-consistent remesh loop
```

## 4. triangulation_flip — 第三を足すと多様体が保たれる

`scripts/triangulation_flip.py`

設定：

```text
flat torus triangulation
Pachner 2-2 edge flips
flatness action E = Σ_v (deg(v)-6)^2
Metropolis temperature T
```

見るもの：

- degree variance = curvature fluctuation
- average graph distance
- manifold condition: every edge has exactly two triangle faces

典型出力：

| case | degree variance | average distance | manifold |
|---|---:|---:|---|
| seed flat | 0.00 | high/flat | True |
| low open T=5 | moderate | slightly shorter | True |
| high open T=20 | larger | shorter/crumpled tendency | True |

重要：

```text
辺だけの graph dynamics では、多様体条件がないので弦/潰れ/分断に落ちやすい。
面=第三を構造として保つと、各辺ちょうど2三角形の2-多様体条件が維持される。
```

claim tier:

```text
measured in combinatorial torus triangulation
absolute spectral dimension is not claimed here
```

## 5. boundary_scaling — 境界/エントロピー橋

`scripts/boundary_scaling.py`

自由場エンタングルメント自体の計算は、PDF側で Jacobi solver bug が見つかったため、repo ではまだ入れない。  
先に、エントロピー面積則に直結する graph boundary scaling を入れた。

局所 d 次元なら、

```text
|boundary A| ~ |A|^((d-1)/d)
```

2Dなら exponent = 1/2。

典型出力：

| graph | exponent B~A^α | reading |
|---|---:|---|
| 2D grid torus | ~0.50 | area-law boundary, d≈2 |
| 2D grid + shortcuts | >0.5 | nonlocal boundary / abnormal |
| random degree graph | much larger | bulk-like boundary, no local geometry |

claim tier:

```text
boundary scaling = measured
entanglement entropy itself = frontier / needs correct solver
```

## 6. 方法論: 計算と関係の区別

PDFの重要な反省：二種類の「計算」を区別する。

```text
(a) 局所的な関係の反応を走らせる
    Gray-Scott, field, vortex, vessel
    = 物理のプロセスに忠実

(b) 大域量を計算で測る
    eigen-decomposition, entropy diagonalization
    = 僕らの顕微鏡
```

今回の spectral toolbox は `(b) 顕微鏡`。  
物理プロセスそのものではない。

そのため、claim はこう締める。

```text
固有モードは空間を読む顕微鏡である。
固有分解そのものが、空間の物理生成過程だとは言わない。
```

## 7. 正直な frontier

### 裸の局所規則からの多様体

未解決。

```text
裸の規則だけでは、弦か潰れに落ちやすい。
2D整数次元多様体には、第三 + 曲率制御 が irreducible に見える。
```

### 作用のエントロピー起源

未解決。

境界 scaling は見えた。  
しかし、自由場エンタングルメント・エントロピーそのものは、正しい固有値ソルバーで再実装が必要。

次の候補：

```text
numpy/scipy 環境で free scalar Gaussian entropy を実装
pure state checks: S_total=0, S_A=S_Abar
2D grid: S ~ sqrt(|A|)
random graph: S ~ |A| 方向
```

ただしこれは Codex / Python dependency あり案件。  
現 repo の dependency-free CI とは分ける。

## 8. 次の優先順位

### Priority 1 — triangulation_flip の seed / T sweep を厚くする

第三 + 曲率制御の核なので、seed / T / L を増やす。

### Priority 2 — boundary_scaling を次元メーターとして強化

1D/2D/3D grid, small-world, random で有限サイズ scaling を見る。

### Priority 3 — entanglement entropy は別環境で正しく実装

依存ありでよいので、正しい eigen solver を使う。

### Priority 4 — third emergence の方向へ戻る

現在の triangulation は第三を入れている。  
次は、第三がどこから来るか。

```text
edge dynamics
→ loop closure
→ triangle birth
→ face stabilization
→ curvature control
```

ここが本丸。

## 現在地の合言葉

> 座標は線ではなく、最も低い巻く位相である。  
> しかし、位相を読む顕微鏡だけでは多様体は生まれない。  
> 多様体には、第三と曲率制御が要る。
