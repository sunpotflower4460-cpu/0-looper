# 15 — D+ repeated lineage selection results

## 目的

`docs/14-delta-inheritance-results.md` では、closure 後の split と継承を最低限実装した。  
ただし、そこでは `full_inheritance` が `pattern_only` を明確に上回るところまでは出ていなかった。

D+ では、より Claude 合流マップの意図に近い形で、**単発の子ではなく、複数世代の survival curve** を見る。

問い：

```text
pattern だけを渡す lineage は、繰り返し stress を越えられるか。
marker だけを渡す lineage は、active pattern なしで持続できるか。
pattern と marker が閉ループで渡る lineage は、世代を越えて残るか。
```

実装は `scripts/dplus_lineage_selection.py`。

## 実行

```bash
python3 scripts/dplus_lineage_selection.py --mode all --seeds 12 --generations 20
```

## モデル

これは Gray-Scott grid を毎世代回す高コスト版ではなく、D の結果を受けた **lineage-level toy**。

個体は2つの状態量を持つ。

- `p`: active pattern strength
- `m`: memory / marker strength

比較する lineage は4つ。

- `no_inheritance`: 子は弱い新規 seed から始まる
- `pattern_only`: `p` だけを渡す
- `marker_only`: `m` だけを渡す
- `full_loop`: `p` と `m` を渡し、`p` が `m` を維持し、`m` が `p` を守る

これは生物学的な遺伝ではない。  
**継承可能な状態量が、繰り返し stress の中で lineage persistence を変えるか**だけを見る。

## generation 1

| mode | alive rate | mean count | mean pattern p | mean marker m | persistence |
|---|---:|---:|---:|---:|---:|
| no_inheritance | 1.00 | 4.1 | 0.232 | 0.011 | 0.117 |
| pattern_only | 1.00 | 48.0 | 0.681 | 0.010 | 0.344 |
| marker_only | 1.00 | 38.6 | 0.410 | 0.799 | 0.369 |
| full_loop | 1.00 | 48.0 | 1.000 | 1.000 | 1.000 |

## generation 5

| mode | alive rate | mean count | mean pattern p | mean marker m | persistence |
|---|---:|---:|---:|---:|---:|
| no_inheritance | 0.00 | 0.0 | 0.000 | 0.000 | 0.000 |
| pattern_only | 0.00 | 0.0 | 0.000 | 0.000 | 0.000 |
| marker_only | 1.00 | 26.1 | 0.280 | 0.295 | 0.182 |
| full_loop | 1.00 | 200.0 | 1.000 | 1.000 | 1.000 |

## generation 10

| mode | alive rate | mean count | mean pattern p | mean marker m | persistence |
|---|---:|---:|---:|---:|---:|
| no_inheritance | 0.00 | 0.0 | 0.000 | 0.000 | 0.000 |
| pattern_only | 0.00 | 0.0 | 0.000 | 0.000 | 0.000 |
| marker_only | 0.00 | 0.0 | 0.000 | 0.000 | 0.000 |
| full_loop | 1.00 | 200.0 | 1.000 | 1.000 | 1.000 |

## generation 20

| mode | alive rate | mean count | mean pattern p | mean marker m | persistence |
|---|---:|---:|---:|---:|---:|
| no_inheritance | 0.00 | 0.0 | 0.000 | 0.000 | 0.000 |
| pattern_only | 0.00 | 0.0 | 0.000 | 0.000 | 0.000 |
| marker_only | 0.00 | 0.0 | 0.000 | 0.000 | 0.000 |
| full_loop | 1.00 | 200.0 | 1.000 | 1.000 | 1.000 |

## final comparison

| mode | alive at final gen | final count | final persistence | reading |
|---|---:|---:|---:|---|
| no_inheritance | 0.00 | 0.0 | 0.000 | fresh weak seeds die out |
| pattern_only | 0.00 | 0.0 | 0.000 | pattern alone does not survive repeated stress |
| marker_only | 0.00 | 0.0 | 0.000 | marker alone decays without active pattern |
| full_loop | 1.00 | 200.0 | 1.000 | p and m reinforce; lineage persists |

## 読み

D の単発 split では、`pattern_only` と `full_inheritance` の差が明確ではなかった。  
D+ で複数世代 stress を入れると、差がはっきり出る。

```text
pattern only: 1世代目は強いが、繰り返し stress で消える。
marker only : 数世代は残るが、active pattern がないので消える。
full loop   : pattern と marker が互いに維持し、lineage が残る。
```

ここでの重要点は、**継承される marker そのものではなく、marker と active pattern の閉ループ**。

```text
p が m を維持する
m が p を守る
その両方が子へ渡る
```

これが repeated generations で選択優位として見える。

## 正直な境界

言ってよいこと：

> repo 側でも、単発 split では弱かった marker advantage を、複数世代 stress 条件で再検証した。pattern だけ、marker だけの lineage は消え、p↔m の閉ループを継承する lineage だけが 20 世代まで残った。

まだ言わないこと：

> 遺伝を作った。
> 自然選択を証明した。
> DNA 的な情報継承を再現した。
> 生命の世代交代を作った。

これは **lineage-level toy**。  
Gray-Scott grid の full repeated generation ではなく、D の結果を圧縮した p/m 状態量モデルである。

## 次

次に進むなら2方向。

### 1. D++ full-grid repeated generations

- Gray-Scott grid を各世代で実際に split
- child を複数生成
- stress 後に survival した child だけ次世代へ
- marker-rich / marker-poor の lineage curve を再測定

### 2. 統合現在地ドキュメント

ここまでの α / β / γ / δ / D+ を1枚に整理する。

```text
α third/soc: 空間的幅・臨界性
β arrow: 低エントロピー境界から時間の矢
γ closure: A→M→A の器
δ inheritance: closure 後の split と継承
D+ lineage: p↔m 閉ループの世代持続性
```
