# 12 — β arrow results

## 目的

Claude 合流マップの優先順位 2 にある **β arrow** を repo 側で独立再現する。

合流マップ上の主張は次。

```text
時間の向きは法則そのものではなく、低エントロピー境界条件から立つ。
低エントロピー初期 → S増大 → 矢が立つ。
高エントロピー初期 → 矢なし。
51/49 の微小非対称でも faint な矢があり、閾値はない。
複雑さは、秩序と無秩序の中間で最大になる。
低エントロピー境界を t=0 に置くと、前後両方向へ S が増える。
```

実装は `scripts/beta_arrow.py`。

## 実行

```bash
python3 scripts/beta_arrow.py --mode all
```

## Kac ring: arrow + recurrence

| initial | S(0) | max S | S(N/4) | S(N/2) | S(N) | S(2N) | reading |
|---|---:|---:|---:|---:|---:|---:|---|
| low entropy all + | 0.000 | 1.000 | 1.000 | 0.999 | 0.000 | 0.000 | arrow + recurrence |
| high entropy random 50/50 | 1.000 | 1.000 | 0.993 | 1.000 | 1.000 | 1.000 | no strong arrow |

読み：低エントロピー初期ではエントロピーが増え、有限系なので回帰する。高エントロピー初期では、最初からほぼ最大で、明確な矢は立ちにくい。

## asymmetry scan

| initial plus fraction | S(0) | max S | ΔS=max-S0 | reading |
|---:|---:|---:|---:|---|
| 0.50 | 1.00000 | 1.00000 | 0.00000 | equilibrium/no arrow |
| 0.51 | 0.99971 | 1.00000 | 0.00029 | continuous, no threshold |
| 0.53 | 0.99740 | 1.00000 | 0.00260 | continuous, no threshold |
| 0.55 | 0.99277 | 1.00000 | 0.00723 | continuous, no threshold |
| 0.60 | 0.97095 | 1.00000 | 0.02905 | continuous, no threshold |
| 0.70 | 0.88129 | 1.00000 | 0.11871 | continuous, no threshold |
| 0.90 | 0.46900 | 1.00000 | 0.53100 | continuous, no threshold |
| 1.00 | 0.00000 | 1.00000 | 1.00000 | continuous, no threshold |

読み：初期非対称が 51/49 でも、非常に小さいが `ΔS>0`。矢の強さは連続的で、明確な閾値はない。

## complexity window

| point | step | coarse entropy | gzip bytes | reading |
|---|---:|---:|---:|---|
| start | 0 | 0.402 | 73 | ordered / simple |
| complexity peak | 8 | 1.348 | 714 | filamented middle |
| final | 80 | 0.000 | 28 | coarse mixed / simple again |

読み：秩序だった初期状態は単純。混合の途中でフィラメント状になり、gzip complexity が最大化する。粗視的に混ざり切ると、再び単純になる。これは「構造・生命・今は秩序と無秩序の中間に宿る」という合流マップの読みと対応する。

注：ここでは cat map + 弱い粗視混合を使っている。完全な可逆ミクロ状態そのものではなく、粗視観測上の complexity window を見る toy。

## two-arrow

| |t| | S(-t) | S(0) | S(+t) | reading |
|---:|---:|---:|---:|---|
| 0 | 0.000 | 0.000 | 0.000 | entropy rises away from low-entropy boundary |
| 25 | 0.943 | 0.000 | 0.943 | entropy rises away from low-entropy boundary |
| 50 | 1.000 | 0.000 | 1.000 | entropy rises away from low-entropy boundary |
| 100 | 0.999 | 0.000 | 0.999 | entropy rises away from low-entropy boundary |

読み：低エントロピー状態を `t=0` に置くと、前後どちらへ走らせてもエントロピーが増える。矢の向きは、低エントロピー境界がどこに置かれているかで決まる。

## 正直な境界

言ってよいこと：

> repo 側でも、Kac ring で低エントロピー初期から矢が立ち、高エントロピー初期では矢が弱いこと、微小非対称でも連続的な faint arrow があること、低エントロピー境界から前後両方向にエントロピーが増えることを再現した。

まだ言わないこと：

> なぜ我々の宇宙の始まりが低エントロピーだったかを説明した。
> 時間の矢を法則だけから導いた。
> 量子重力の過去仮説を解いた。

## 次

現在地への合流順では、次は **器 closure**。

- self_repair: Gray-Scott seed から自己組織化し、半分破壊後に回復するか
- memory: ずらし後、記憶あり/なしで元の構造へ戻る差を見る
- closure: A→M と M→閉じ込めの両アームが揃う時だけ持続するか
