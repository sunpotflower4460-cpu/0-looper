# 17 — Audit response and revised priorities

## 目的

Claude 側からの監査コメントを受けて、`δ inheritance` と `D+ lineage` の claim を締め直し、次の優先順位を更新する。

結論から言うと、監査は正しい。

`docs/16-current-location-synthesis.md` の規律は維持できているが、特に γ/δ/D+ については、さらに明確に次の線を引く必要がある。

> γ/δ/D+ は「相互維持の結合があるなら持続する」ことを確認した toy。  
> まだ「相互維持の結合そのものが創発した」ことを示していない。

## 監査コメントの要点

### 良い点

- `docs/16` は、言ってよいこと / まだ言わないこと / 弱点を明記していて、claim discipline がある。
- α third の `d≈1.85`、2D CDT の `d≈2.06` など、Claude 側と GPT 側の別実装で近い数字が出ている。
- 「関係には制約が要る」「第三が幅を生む」「器は形でなく閉ループ」「継承は marker 単体ではなく閉ループ」という気づきは、ここまでの測定に合っている。
- 神聖幾何学を物理法則そのものではなく、交点・三角形・局所閉包のモチーフとして扱う線は健全。

### 重要な指摘

δ と D+ は、結果がコードにかなり入っている。

- δ では、`m` が `k_eff` と `d_v_eff` を下げる。さらに stress の damage も下げる。
- D+ では、`m が p を守り、p が m を養う` が update rule に直接書かれている。
- `marker_only` は、active pattern を弱くする設計なので、死にやすい。
- D+ の `full_loop` が `persistence = 1.000` に張り付くのは、天井に貼り付く設計の徴候。

したがって、D+ の読みは次に限定する。

```text
誤: p↔m 閉ループが自然に創発した。
正: p↔m 閉ループを dynamics に仮定すると、repeated stress の中で lineage advantage が積み上がる。
```

## 改訂 claim tier

### measured

- α third: edge/pair だけでは string / crumpled に寄り、triangle/third + causal order では 2D-like width が出た。
- 2D CDT: causal layering があると 2D-like scaling が出て、rewiring で small-world 化した。
- β arrow: low-entropy boundary から entropy arrow が立った。
- γ closure: 手で入れた `A→M` と `M→A` の coupling があると、damage 後の structural similarity が上がった。
- δ/D+: 手で入れた `p↔m` coupling があると、単発/複数世代で persistence advantage が出る。

### conditional / by-construction

- γ/δ/D+ の closed loop advantage は、現時点では **by construction**。
- つまり、相互維持を仮定した場合の帰結を見ている。
- 「相互維持が必要そうだ」という地図にはなるが、「相互維持が創発した」という証明ではない。

### frontier

- one-flow から closure が立つか。
- `m が p を守る` を手で書かず、reaction product / local obstruction / permeability の結果として出せるか。
- scar と regenerative boundary を分けられるか。
- marker-rich lineage が full-grid repeated generations で本当に残るか。

## 優先順位の更新

監査前の優先順位では D++ full-grid repeated generations が最上位だった。  
監査後は、順番を少し変える。

## Priority 1 — one-flow → closure 接続

もっとも根に近い次の一歩。

いまの closure 系は、Gray-Scott 風の反応拡散を別に用意している。  
次は、`0 → 差 → event → relation → causal order` の one-flow から、局所的な閉ループ field を立ち上げる。

目標：

```text
0 / white
↓
event
↓
relation / causal loop
↓
local production field
↓
boundary-like memory
↓
vessel-like persistence
```

言ってよい claim：

> event/relation/causal loop から、closure field の候補を生成する toy を試す。

まだ言わない claim：

> 器が自然発生した。
> 細胞膜ができた。

## Priority 2 — coupling emergence

`m が p を守る` を直接書かない。

現在の問題：

```text
m が diffusion / decay / damage を下げるように手で設定している。
```

次の方向：

```text
p が副産物 b を出す
b は局所に溜まる
b は物理的に空き容量 / permeability を変える
その結果として p の流出が変わる
```

重要なのは、`m protects p` を目的関数として入れないこと。  
保護に見える効果は、局所的な obstruction / permeability / crowding から後で読む。

必要な ablation：

- no product
- inert product: 溜まるが permeability に効かない
- obstructive product: 溜まりすぎると流れを塞ぐ
- regenerative product: 壊れても再生成される
- scar product: 壊れた後に固まって再生を邪魔する

見たいもの：

- protection が出るか
- scar 化するか
- regeneration と obstruction の窓があるか
- closed loop が自動で持続する範囲があるか

## Priority 3 — D++ full-grid repeated generations

D++ は価値がある。  
ただし claim は絞る。

誤：

```text
marker を持つ系列が創発した。
```

正：

```text
marker advantage を dynamics に入れた場合、full-grid repeated generations でも選択で積み上がるかを調べる。
```

D++ は、Priority 2 の coupling emergence を少し進めてからの方が価値が高い。  
少なくとも、direct damage reduction だけは避ける。

## Priority 4 — 3D CDT step D

CDT 側は引き続き重要。

次は：

- `(4,4)` move
- `(2,3)/(3,2)` move
- validity check
- foliation check
- link condition

その後に Regge action + Metropolis へ進む。

## docs/16 の読み替え

`docs/16` の中心仮説は維持する。

```text
空間らしさには、関係だけでなく、因果と第三が必要。
時間の矢には、低エントロピー境界が必要。
器には、形ではなく A→M→A の閉ループが必要。
継承には、marker 単体ではなく p↔m の閉ループが必要。
```

ただし後半2つは、次の注釈つきで読む。

```text
器には A→M→A の閉ループが有効である。
ただし、現実装ではその結合は手で入れている。

継承には p↔m の閉ループが有効である。
ただし、現実装では p↔m の相互維持を手で入れている。
```

## 次に作るべきもの

### 1. `scripts/one_flow_closure.py`

one-flow から closure field を作る headless 実験。

最小仕様：

```text
field difference
→ threshold event
→ causal relation
→ loop / local recurrence score
→ product field b
→ boundary-like concentration
→ persistence under perturbation
```

### 2. `scripts/coupling_emergence.py`

反応副産物が permeability / obstruction を変えるだけで、保護らしさが出るかを見る。

禁止：

```text
m directly reduces damage
m directly reduces decay as a designed protection term
```

許可：

```text
local crowding changes diffusion coefficients through physical occupancy
reaction product accumulates and decays
permeability is computed from occupancy, not from survival goal
```

## 現在地の修正版結論

`0-looper` は、かなり良い場所まで来ている。  
特に α/β/CDT は、別実装でも数字が近く、強い足場になっている。

一方で、γ/δ/D+ は、次の壁に当たった。

> 閉ループを入れれば持続する。  
> しかし、閉ループがどこから来るかはまだ示していない。

これは失敗ではなく、むしろ前線が明確になったということ。

次の合言葉：

> 仮定した閉ループを測る段階から、閉ループが立ち上がる条件を探す段階へ。
