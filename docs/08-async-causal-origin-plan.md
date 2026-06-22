# 08 — Async causal origin plan

## 目的

Claude 側の「最深 — 因果・時間はどこから来るのか」に対応する repo 側の再実装。

問い：

> 大域時計を入れず、局所的な非同期変化だけを記録したとき、依存構造から時間・葉層・同時面・次元ヒントが読めるか。

## 実装

`scripts/async_causal_origin.py`

### 入れるもの

- 1D ring のセル
- ランダムに1セルを選ぶ非同期 micro update
- 更新時に読む近傍セル `{i-1, i, i+1}`
- 各セルの直前更新 event を parent として記録

### 入れないもの

- 共有された synchronous clock
- 最初からの時間スライス
- global layer assignment
- 未来依存
- 幾何座標による測定

ただし、1D ring は与えている。  
したがってこれは「空間なし」ではなく、**空間所与で、時間/因果順序を変化から読む実験**。

## 測るもの

- DAG rate
- topological sort count
- depth = causal layer count
- width = layer width
- comparable ratio
- dimension scaling
- CTC injection collapse

## sanity check

手元の小さい確認では、次の挙動を確認した。

### summary example

```text
N = 32
sweeps = 32
events = 1024
DAG = true
topological sort count = 1024
depth ≈ 128
width ≈ 12
comparable ratio ≈ 0.65
```

### CTC injection example

```text
future -> past edge を1本追加
topological sort count が 1024 -> 約224 に低下
DAG = false
```

### scaling example

`sweeps = N` として、N = 16, 24, 32, 48, 64 を確認。

```text
events: 256, 576, 1024, 2304, 4096
depth : 64, 95, 130, 191, 258
slope ≈ 0.503
dimension_hint ≈ 1.99
```

読み：1D carrier + causal depth で、約2次元の時空的スケーリングが出る。

## Claude PDF との対応

Claude 側の文書では、大域時計なしの非同期局所更新から DAG、トポロジカル順序、時間の葉層、関係的な同時、因果集合の次元 `d_s≈1.94` が出たと整理されている。

repo 側では、まずこの結果の最小再現として `async_causal_origin.py` を置く。

## 正直な境界

言ってよいこと：

> 大域時計を明示的に使わない非同期更新から、event の依存DAG、因果層、時間らしい深さ、約2次元のスケーリングが読める toy model を再実装した。

まだ言わないこと：

> 時間の向きを完全に導いた。
> 空間も同時に無から創発した。
> 現実宇宙の時間の起源を証明した。

## 次

1. Claude 側の正確なパラメータと比較する
2. `radius`, `sweeps`, `N` の sweep を追加する
3. entropy gradient / arrow direction を別トラックとして測る
4. 2D CDT toy を repo に実装し、空間創発側と並べる
5. one-flow と async-causal を統合し、0/white -> field change -> async event -> causal layers まで一本化する
