# 11 — α space map results

## 目的

Claude 合流マップの優先順位 1 にある **α third / α soc** を、repo 側でまず独立再現する。

合流マップ上の主張は次。

```text
関係だけ → クシャ / small-world
裸の因果成長 → 紐 / d≈1
第三 = 三角形 + 因果順序 → 2D 的な幅 / d≈1.87
SOC = 保存 + しきい値 + ゆっくり駆動でスケールフリーななだれ
```

実装は `scripts/alpha_space_map.py`。

## 実行

```bash
python3 scripts/alpha_space_map.py --mode all --seed 0
```

## width scaling

| case | beta width~N^β | d≈1/(1-β) | 読み |
|---|---:|---:|---|
| string constant width | 0.000 | 1.00 | 幅一定 = 紐 |
| 2D target sqrt width | 0.500 | 2.00 | 幅 ~ sqrt(N) = 2D |
| crumpled linear width | 1.000 | inf | 幅 ~ N = クシャ |
| fractal 1.5 target | 0.333 | 1.50 | 中間フラクタル |

これは測定器の sanity check。  
幅スケール指数 `β` と有効次元 `d≈1/(1-β)` の読み替えを確認する。

## naive branching / balance

### naive branching

| regime | final width | max width | beta estimate | verdict |
|---|---:|---:|---:|---|
| death | 0.3 | 29.2 | -4.26 | dies |
| balanced-string | 12.5 | 25.5 | 1.34 | string-like |
| critical-fractal | 21.3 | 45.3 | 0.18 | string-like / watch |
| birth-explosion | 619.1 | 619.1 | 2.41 | explosive watch |

読み：素朴な分岐だけでは、死ぬ / 紐 / 爆発 / 不安定中間になりやすい。  
きれいな 2D 多様体相を自動で出すには弱い。

### balance feedback

| initial width | final width | mean last 50 | std last 50 |
|---:|---:|---:|---:|
| 3 | 17.22 | 18.13 | 1.43 |
| 10 | 19.42 | 19.19 | 2.05 |
| 30 | 18.51 | 21.21 | 2.56 |
| 100 | 20.19 | 20.42 | 2.39 |

読み：初期幅 3/10/30/100 が、同じ有限幅の平衡へ寄る。  
ただし、これは安定した有限幅であって、幅 ~ sqrt(N) の多様体次元そのものではない。

## third / simplex grammar

| relation cell | causal order | events | depth/diameter | width | d hint | verdict |
|---|---|---:|---:|---:|---:|---|
| edge/pair | no | 5000 | 10 | 5000 | inf | crumpled / small-world |
| edge/pair | yes | 5000 | 5000 | 1 | 1.00 | string |
| triangle/third | no | 5000 | 8 | 5000 | inf | crumpled / small-world |
| triangle/third | yes | 5000 | 100 | 99 | 1.85 | 2D-like sheet |

読み：この toy では、辺だけに因果順序を入れると紐に潰れる。  
三角形 = 第三のセルに因果順序を入れると、深さ ~ sqrt(N)、幅 ~ sqrt(N) の 2D 的な層構造になる。

合流マップの `triangle + causal order -> d≈1.87` にかなり近い結果になった。

## SOC / BTW sandpile

| L | drives | avalanches | max avalanche | tau pdf fit | mean size |
|---:|---:|---:|---:|---:|---:|
| 64 | 12000 | 2628 | 14369 | 1.46 | 195.44 |

読み：2D BTW 砂山で、ゆっくり駆動 + 保存 + しきい値から、広い avalanche size 分布が出た。  
推定 `τ≈1.46` は小さい試行・簡易フィットではあるが、合流マップの `τ≈1.36` と同じ方向。

## 正直な境界

言ってよいこと：

> repo 側でも、辺+因果が紐に潰れ、三角形+因果が 2D 的な幅を持つ toy を再現した。さらに、保存+しきい値+ゆっくり駆動で SOC 的な avalanche 分布が出ることを確認した。

まだ言わないこと：

> 空間を無から生成した。
> 第三そのものを無から導いた。
> balance だけで多様体次元を出した。
> SOC のなだれが、そのまま多様体次元を生むと示した。

## 次

現在地への合流順では、次は **β arrow**。

- Kac ring: 低エントロピー初期では矢が立ち、高エントロピー初期では矢が弱い
- asymmetry scan: 51/49 でも faint な矢、閾値なし
- complexity window: 混合過程の中間で複雑さ最大
- two-arrow: 低エントロピー境界を t=0 に置くと、前後両方向にエントロピーが増える
