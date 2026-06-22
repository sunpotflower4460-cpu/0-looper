# 13 — γ closure / vessel results

## 目的

Claude 合流マップの優先順位 3 にある **器 closure** を repo 側で独立再現する。

合流マップ上の主張は次。

```text
器は、単に形が閉じていることではない。
自己組織化したパターンが、破壊後にも回復するか。
記憶場があることで、元の構造に戻りやすくなるか。
A→M と M→A の閉ループが揃うと、持続性が上がるか。
```

実装は `scripts/gamma_closure.py`。

## 実行

```bash
python3 scripts/gamma_closure.py --mode all --seeds 3
```

## モデル

Gray-Scott 風の反応拡散 seed を、自己組織化パターンの最小 proxy として使う。

- `u`: substrate / nutrient
- `v`: activator / pattern
- `m`: memory / membrane proxy

`m` は本物の膜ではない。  
ここでは「パターンが自分の痕跡を残し、その痕跡が次のパターン維持に影響するか」を見る。

破壊テストとして、settle 後に左半分の activator `v` を消し、memory `m` も弱める。

## self-repair

| config | pre mass | post damage | final mass | recovery | similarity | persistence | final membrane |
|---|---:|---:|---:|---:|---:|---:|---:|
| gray_scott_seed | 177.80 | 88.78 | 203.52 | 1.29 | 0.516 | 0.591 | 0.00 |

読み：Gray-Scott seed は、半分破壊後にも activator mass を回復する。  
ただし structural similarity は 0.516 で、元の形そのものに戻ったというより、同じ regime が再成長したと読むのが安全。

## memory

| config | pre mass | post damage | final mass | recovery | similarity | persistence | final membrane |
|---|---:|---:|---:|---:|---:|---:|---:|
| no_memory | 177.80 | 88.78 | 203.52 | 1.29 | 0.516 | 0.591 | 0.00 |
| memory_closed_loop | 369.33 | 184.59 | 378.03 | 1.05 | 0.890 | 0.911 | 351.75 |

読み：memory + confinement を入れると、半分破壊後の structural similarity が 0.516 → 0.890 に上がる。  
単に量が戻るだけでなく、「元の構造へ戻りやすい」方向が出た。

## closure arms

| config | pre mass | post damage | final mass | recovery | similarity | persistence | final membrane |
|---|---:|---:|---:|---:|---:|---:|---:|
| no_closure | 177.80 | 88.78 | 203.52 | 1.29 | 0.516 | 0.591 | 0.00 |
| A_to_M_only | 177.80 | 88.78 | 203.52 | 1.29 | 0.516 | 0.591 | 185.40 |
| M_to_A_only | 198.42 | 99.04 | 216.52 | 1.18 | 0.536 | 0.585 | 0.00 |
| closed_loop | 369.33 | 184.59 | 378.03 | 1.05 | 0.890 | 0.911 | 351.75 |

読み：

- `A_to_M_only`: activator が memory を作るだけでは、pattern には戻りやすくならない。
- `M_to_A_only`: 外から与えた memory/confinement だけでは、効果は弱い。
- `closed_loop`: activator が memory を作り、その memory が activator を守ると、structural similarity と persistence が大きく上がる。

つまり、器らしさは「形」ではなく、

```text
A が M を作る
M が A を守る
```

という閉ループで強くなる。

## 正直な境界

言ってよいこと：

> repo 側でも、反応拡散パターンに memory/confinement proxy を結合すると、破壊後の構造類似度と持続性が上がる toy を再現した。A→M と M→A の両方が揃う closed loop が最も強かった。

まだ言わないこと：

> 生命を作った。
> 本物の細胞膜を再現した。
> 自己修復生命の原理を証明した。
> トーラスや器が自然発生した。

## 次

現在地への合流順では、次は **D 継承マーク**。

- split after closure
- marker inheritance
- parent/child similarity
- selection / survival bias

ただし、Dに進む前に `gamma_closure.py` の browser visualization を作ると、器の直感はかなり見やすくなる。
