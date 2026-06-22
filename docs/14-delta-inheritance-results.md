# 14 — δ inheritance / marker results

## 目的

Claude 合流マップの優先順位 4 にある **D 継承マーク** を repo 側で独立再現する。

合流マップ上の問いは次。

```text
closure / 器 のあと、構造は分かれても何かを渡せるか。
split after closure で、親の pattern / marker が子に残るか。
marker inheritance は、子の回復・持続性に効くか。
selection bias は出るか。
```

実装は `scripts/delta_inheritance.py`。

## 実行

```bash
python3 scripts/delta_inheritance.py --mode all --seeds 3
```

## モデル

γ closure と同じく、Gray-Scott 風の反応拡散 seed を使う。

- `v`: activator / pattern
- `m`: memory / marker proxy
- parent は closed-loop 条件で settle させる
- parent を左右に split し、各半分を child の中央に移植する
- child に stress を与え、recover 後の similarity / survival を測る

これは生物学的な遺伝ではない。  
ここでは、**親のパターンや記憶マーカーが、分割後の子の持続性に影響するか**だけを見る。

## split inheritance

| mode | child similarity | marker similarity | mass ratio | survival | persistence index |
|---|---:|---:|---:|---:|---:|
| no_inheritance | 0.720 | 0.735 | 0.00 | 0.00 | 0.000 |
| pattern_only | 0.522 | 0.546 | 1.07 | 1.00 | 0.403 |
| marker_only | 0.703 | 0.913 | 0.00 | 0.00 | 0.000 |
| full_inheritance | 0.507 | 0.541 | 2.53 | 1.00 | 0.391 |

## selection bias

| class | survival | persistence index | reading |
|---|---:|---:|---|
| weak/no transmitted activator | 0.00 | 0.000 | marker alone is not enough |
| transmitted active pattern | 1.00 | 0.397 | pattern-bearing children survive stress |

## 読み

今回の toy では、**marker だけでは子は生き残らない**。  
`marker_only` は marker similarity は高いが、activator mass が戻らず survival は 0 だった。

一方で、`pattern_only` と `full_inheritance` は survival 1.00 になった。  
つまり、この段階で継承に必要なのは、まず **動いている pattern / activator を渡すこと**。

ただし、γ closure では closed loop が破壊後の構造類似度を大きく上げていた。  
今回の D では、split 後の toy 条件では `full_inheritance` が `pattern_only` を明確に上回るところまでは出ていない。ここは正直に **未確定** とする。

暫定的な結論：

```text
closure → split → inheritance の最小鎖は成立。
marker は渡る。
しかし marker だけでは足りない。
子の持続には active pattern の継承が必要。
marker が選択優位をどこまで作るかは、stress 条件と marker dynamics の追加検証が必要。
```

## 正直な境界

言ってよいこと：

> repo 側でも、closed parent を split し、pattern / marker の継承有無で child persistence が変わる toy を実装した。active pattern を渡した子は stress 後も survival し、marker だけでは survival しなかった。

まだ言わないこと：

> 遺伝を作った。
> DNA のような継承を再現した。
> marker が明確な選択優位を作ると証明した。
> 生命の世代交代を再現した。

## 次

D は最低限追いついた。  
次にやるなら、2つの方向がある。

### D+ 改良

- marker dynamics を強める
- split 後の child environment を変える
- repeated generations を回す
- marker-rich lineage / marker-poor lineage の survival curve を比較する

### 合流まとめ

ここまでの α / β / γ / δ を、1枚の現在地ドキュメントにまとめる。

```text
α third/soc: 空間的幅・臨界性
β arrow: 低エントロピー境界から時間の矢
γ closure: A→M→A の器
δ inheritance: closure 後の split と継承
```
