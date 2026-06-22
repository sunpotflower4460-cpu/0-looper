# 0-looper

**0 は無ではない。**  
このリポジトリは、AeternaGenesis の根本仮説を最小の形で試すための実験場です。

> 白は空間ではなく、未分化の存在である。  
> 0 は何も無いことではなく、まだ差が立っていない基底状態である。  
> そこにルール・ゆらぎ・不安定性があると、差、関係、順序、因果、次元が読み出される。

## 目的

最初から「生命」「トーラス」「宇宙」「重力」を描きません。  
最初に置くのは、次の最小材料だけです。

1. **0 / white** — 差が立つ前の基底状態
2. **rule** — 次が今にどう依存するか
3. **event** — 差が観測可能な出来事になること
4. **relation** — event 同士が互いに条件になること
5. **causal order** — 関係に向きが生まれること
6. **observation** — 後から距離・因果・次元を読む測定器

## 現在の八本柱

### 1. `one-flow-lab.html`

0-prism と relation-lab を分けず、一本の流れとして見る統合ラボ。

```text
0 / white
↓
局所ルールで差が立つ
↓
閾値を超えた変化が event になる
↓
recent + local dependency から relation を張る
↓
parent → child が causal order になる
↓
width / longest chain / comparable ratio / d hint を後から読む
```

第一推奨テンプレートは **balanced-oneflow**。

### 2. `scripts/async_causal_origin.py`

Claude 側の「時間←変化」に対応する headless 実験。

- 大域時計を入れない
- 局所的な非同期更新だけを記録する
- 読んだ近傍セルの直前 event を parent にする
- DAG / causal layers / dimension scaling / CTC injection を測る

### 3. `scripts/cdt_2d_toy.py`

Claude 側の「空間←因果」に対応する 2D CDT toy。

- 時間スライスごとの 1D 空間リング
- 隣接スライス間の causal up/down triangles
- diameter scaling / ball growth / spectral dimension を測る
- rewiring で因果を壊したときのスモールワールド化を見る

### 4. `scripts/cdt3d_route_min.py`

Claude 側の「3D CDT ルート」に対応する steps A-C の検証。

- A: 平らな 2+1 積層で、直径スケーリングとスペクトル次元が `d≈3` を読むか
- B: `∂Δ4` から汎用 `(1,4)/(4,1)` move が閉3多様体条件を保つか
- C: 葉層 3 トーラスと葉層保存 `(2,6)` move が多様体＋葉層を保つか

まだ Regge 作用、Metropolis、相探索は入れていない。

### 5. `scripts/alpha_space_map.py`

Claude 合流マップの **α third / α soc** に対応する独立再現。

- width scaling: 幅指数 `β` と有効次元 `d≈1/(1-β)` の sanity check
- branching / balance: 素朴分岐と密度フィードバックの比較
- third: 辺 vs 三角形 × 順序なし vs 因果順序
- soc: 2D BTW sandpile の avalanche 分布

### 6. `scripts/beta_arrow.py`

Claude 合流マップの **β arrow** に対応する独立再現。

- Kac ring: 低エントロピー初期では矢が立ち、高エントロピー初期では弱い
- asymmetry scan: 51/49 でも faint な矢があり、閾値なし
- complexity window: 混合の中間で複雑さが最大
- two-arrow: 低エントロピー境界から前後両方向へエントロピーが増える

### 7. `scripts/gamma_closure.py`

Claude 合流マップの **γ closure / 器** に対応する独立再現。

- self-repair: 反応拡散 seed が半分破壊後に回復するか
- memory: memory/confinement proxy が元の構造への戻りやすさを上げるか
- closure: `A→M` と `M→A` の両アームが揃う時だけ持続性が上がるか

### 8. `scripts/delta_inheritance.py`

Claude 合流マップの **δ inheritance / 継承マーク** に対応する独立再現。

- split: closed parent を左右に分け、child に pattern / marker を渡す
- marker inheritance: memory/marker proxy が子へ残るかを見る
- selection bias: pattern-bearing child と marker-only child の survival を比較する

## 補助実験

### `relation-lab-v3.html`

field から event を発生させず、event と relation の成長だけを見るラボ。  
関係性だけを切り出して確認したいときに使う。

### `zero-prism.html`

0 / white が局所ルールでどの波長モードへ分かれるかを見る補助ラボ。

## 自動検証

### one-flow sweep

```bash
python3 scripts/one_flow_sweep.py --mode presets --seeds 20
python3 scripts/one_flow_sweep.py --mode grid --seeds 3 --top 12
```

### async causal origin

```bash
python3 scripts/async_causal_origin.py --mode summary --cells 32 --sweeps 32 --seeds 5
python3 scripts/async_causal_origin.py --mode ctc --cells 32 --sweeps 32 --seeds 5
python3 scripts/async_causal_origin.py --mode scaling --seeds 3
```

### 2D CDT toy

```bash
python3 scripts/cdt_2d_toy.py --mode sizes --sources 6
python3 scripts/cdt_2d_toy.py --mode rewire --sources 6
python3 scripts/cdt_2d_toy.py --mode fluct --sources 6
```

### 3D CDT route A-C

```bash
python3 scripts/cdt3d_route_min.py --mode A
python3 scripts/cdt3d_route_min.py --mode B --moves 5
python3 scripts/cdt3d_route_min.py --mode C --L 3 --T 4 --moves 5
```

### alpha space map

```bash
python3 scripts/alpha_space_map.py --mode third --seed 0
python3 scripts/alpha_space_map.py --mode balance --seed 0
python3 scripts/alpha_space_map.py --mode soc --seed 0
```

### beta arrow

```bash
python3 scripts/beta_arrow.py --mode kac
python3 scripts/beta_arrow.py --mode asym
python3 scripts/beta_arrow.py --mode complexity
python3 scripts/beta_arrow.py --mode twoarrow
```

### gamma closure

```bash
python3 scripts/gamma_closure.py --mode self-repair --seeds 3
python3 scripts/gamma_closure.py --mode memory --seeds 3
python3 scripts/gamma_closure.py --mode closure --seeds 3
```

### delta inheritance

```bash
python3 scripts/delta_inheritance.py --mode split --seeds 3
python3 scripts/delta_inheritance.py --mode selection --seeds 3
```

### relation-only sweep

```bash
python3 scripts/relation_sweep.py --mode presets --seeds 30
python3 scripts/relation_sweep.py --mode scaling --seeds 12
python3 scripts/relation_sweep.py --mode grid --seeds 4 --top 12
```

GitHub Actions でも push / PR / 手動実行時に sweep が走ります。

## docs

- `docs/00-philosophy.md` — 0、白、無音、プリズム比喩の整理
- `docs/01-protocol.md` — 最初の 0-looper toy の測定プロトコル
- `docs/02-relation-first-universe-hypothesis.md` — 関係性を軸にした宇宙条件の仮説
- `docs/03-automated-sweep-results.md` — 初回 relation sweep 結果
- `docs/04-expanded-sweep-results.md` — 追加 relation sweep / scaling / grid 結果
- `docs/05-root-principle-check.md` — 根本原理として何が足りないか
- `docs/06-one-flow-sweep-results.md` — 一本化 one-flow sweep 結果
- `docs/07-claude-sync-needed-info.md` — Claude 側と同期するための情報テンプレ
- `docs/08-async-causal-origin-plan.md` — 非同期更新から時間を読む実験
- `docs/09-cdt-2d-toy-results.md` — 2D CDT toy の再測定結果
- `docs/10-cdt-3d-route-a-c.md` — 3D CDT ルート A-C の再現・検証
- `docs/11-alpha-space-map-results.md` — α third / α soc の独立再現
- `docs/12-beta-arrow-results.md` — β arrow の独立再現
- `docs/13-gamma-closure-results.md` — γ closure / 器 の独立再現
- `docs/14-delta-inheritance-results.md` — δ inheritance / 継承マーク の独立再現

## Claim tiers

- **measured**: このコードで直接測ったこと
- **observed**: 可視化上そう見えること
- **interpretive**: 既存物理概念への読み替え
- **analogy**: 音楽・神聖幾何学・生命への比喩
- **frontier**: まだ未検証の前線

## 現在の合言葉

> 無音は、音楽の不在ではない。  
> それは、まだ鳴っていない音楽を受け止める基底である。
