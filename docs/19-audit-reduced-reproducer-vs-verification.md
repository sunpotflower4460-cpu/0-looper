# 19 — Audit: reduced reproducer vs physics verification

## 目的

Claude 監査コメントを受けて、Map 2 で追加した reduced reproducer の意味を締め直す。

結論：監査は正しい。

`docs/18` と Map 2 scripts は透明ではあったが、すべてが physics verification ではない。  
いくつかは「CI regression smoke-test」であり、claim が間違っていても外れない。

> 検証する側は「計算」せよ、「符号化」するな。  
> 外れえないテストは、何も検証しない。

## 監査の線引き

### 機構から実際に計算しているもの

以下は軽量化されているが、結果が機構から出る。claim が違えば外れうる。

| script / mode | 評価 | 理由 |
|---|---|---|
| `flow_benard_transport.py --mode benard` | fair reduced mechanism | `da/dt = σa - a^3` の超臨界ピッチフォークで onset を計算している |
| `boundary_throughflow.py --mode heal` | fair reduced mechanism | `dr/dt = -γ/r` の曲率流 proxy で穴の治癒を計算している |
| `boundary_throughflow.py --mode throughflow` | fair reduced mechanism | 表面 gain `~sqrt(area)` と体積 loss `~area` の ODE で death/life を計算している |
| `flow_benard_transport.py --mode pe` | fair analytic scaling | `L^2` vs `L` のサイズ則。interpretive 表記が必要 |

特に `boundary/throughflow` は、面積が増えすぎる負の点も正直に出ている。  
これは reduced model として一番誠実。

### 答えを埋め込んでいるもの

以下は、現時点では physics verification ではなく、regression smoke-test と扱う。

| script / mode | 問題 | 正しい扱い |
|---|---|---|
| `flow_benard_transport.py --mode transport` | `tau_diff=5900`, `tau_conv=392` を Map 2 の 0.399 / 0.033 に合うよう tuned | map2 number regression / smoke-test |
| `evo_division_inherit.py` inheritance | `child.tag = parent.tag` で継承を直接代入 | tag propagation smoke-test |
| `evo_division_inherit.py` selection | A/B の半径・複製率を手で決めて density coexistence にしている | selection negative illustration, not discovery |
| `boundary_throughflow.py --mode ch` | area を fixed mass に緩和している | conservation sanity check |
| `model_h_min.py` | stress 係数が小さく、壊れにくい設定 | coexistence illustration, not stable Model H verification |

## 取り下げないもの

この監査は、Map 2 の元 sandbox PDE の測定結果そのものを取り下げるものではない。

- developed transport の 12x は、Claude 側の PDE sandbox で出た measured result。
- Gray-Scott + bistable tag の division / inheritance も、Claude 側の PDE sandbox で出た measured result。

ここで訂正するのは、**0-looper 側の reduced scripts がそれを独立検証したと言えるか**という点。

結論：

```text
元 sandbox PDE = physics measurement
0-looper reduced transport/evo = regression smoke-test / scaffold
```

## すぐ入れた修正

### `scripts/flow_transport_advdiff.py`

`flow_benard_transport.py --mode transport` の tau 直書きに対して、少なくとも「外れうる」軽量版として 1D advection-diffusion を追加した。

実際に解く方程式：

```text
∂c/∂t + u ∂c/∂y = D ∂²c/∂y²
```

これはまだ full Boussinesq ではない。  
しかし、`C_top` は時定数の直書きではなく、有限差分の時間発展から測る。

claim tier：

```text
lightweight mechanism check
not full flow verification
```

## claim tier の修正

### measured in reduced model

- Benard amplitude onset
- curvature-flow hole healing
- surface-vs-volume throughflow death/life
- Pe scaling as analytic/interpretive
- 1D advection-diffusion scalar transport (`flow_transport_advdiff.py`)

### regression smoke-test / scaffold

- hard-coded tau transport in `flow_benard_transport.py --mode transport`
- tag propagation in `evo_division_inherit.py`
- density coexistence selection probe in `evo_division_inherit.py`
- conserved-size area relaxation in `boundary_throughflow.py --mode ch`
- reduced Model-H amplitude check in `model_h_min.py`

### physics verification still needed

- vorticity-streamfunction Boussinesq + passive scalar transport
- full Gray-Scott PDE + bistable tag inheritance
- turnover / birth-death selection
- semi-implicit Cahn-Hilliard / active droplet
- advected phase field / Model H++

## 優先順位の修正版

### Priority 1 — transport を本物の軽量計算にする

今回 `flow_transport_advdiff.py` を追加したが、まだ速度場は与えている。

次：

```text
Benard mini で速度場を発生
↓
その速度場で受動スカラーを輸送
↓
流れ立ち上がりあり / なしを比較
↓
C_top を測る
```

### Priority 2 — evo を full Gray-Scott + bistable tag へ寄せる

`child.tag = parent.tag` をやめる。

次：

```text
u, v reaction-diffusion
τ bistable tag field
v がある場所だけ τ が固定される
spot が分裂すると τ field も共分裂する
daughter tag を後から測定する
```

### Priority 3 — selection は turnover まで待つ

selection には birth だけでなく death / replacement が必要。

候補：

- periodic starvation
- local death / removal
- resource pulse
- chaotic Gray-Scott regime
- open boundary outflow

## docs/18 の読み替え

`docs/18` の claim は次のように読む。

```text
Map 2 の物理結果を 0-looper に合流した。
ただし、0-looper 側の一部 scripts は、現時点では独立物理検証ではなく、regression smoke-test / scaffold である。
```

したがって、今後の合言葉はこう更新する。

> 閉ループを手で入れる段階から、境界・循環・継承が物理の副作用として立ち上がる条件を探す段階へ。  
> そして検証する側は「計算」せよ、「符号化」するな。
