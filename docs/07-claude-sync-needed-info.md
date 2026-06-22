# 07 — Claude sync: 欲しい共有情報

Claude 側が独自の `index` やローカル実験で進んでいる場合、GPT 側の repo 実験と揃えるために欲しい情報。

全部なくてもよい。最小は **コード / パラメータ / 出力 / 主張の線引き**。

## 最小セット

### 1. 実験の名前

例：

```text
async causal origin
2D CDT toy
3D Regge trial
one-flow zero -> event -> relation
```

### 2. 何を入れたか

最初から与えたものを明記する。

```text
空間: 1D ring / 2D triangulation / none / relation graph
時間: global clockあり / micro update orderのみ / causal layersのみ
因果: 入れた / 依存から読んだ / 壊した比較あり
更新: synchronous / asynchronous / Monte Carlo
境界: periodic / open / fixed
```

### 3. 何を測ったか

```text
DAG成立率
topological sort count
longest chain / depth
width / layer size
comparable ratio
Myrheim-Meyer dimension
diameter scaling
ball growth dimension
spectral dimension
CTC injection result
rewire null result
```

### 4. 代表パラメータ

```text
N / number of cells / vertices
sweeps / events / steps
seed count
update radius
noise / fluctuation
threshold
Monte Carlo moves
acceptance rule
```

### 5. 代表出力

例：

```text
events = 2624
DAG = true
depth = ...
width = ...
d_s = 1.94
CTC injected -> topo ordered count = ...
```

### 6. null / 破壊テスト

何を壊したら崩れたか。

```text
future -> past edge injected
causal order removed
random rewiring 5/15/30%
all-to-all relation
chain-only relation
```

### 7. claim tier

```text
measured:
observed:
interpretive:
analogy:
frontier:
```

## こちら側で合わせるときの変換表

### Claude 側：非同期局所更新

GPT repo 側では `scripts/async_causal_origin.py` に対応。

見るもの：

- DAG rate
- topological sort count
- depth / width
- comparable ratio
- dimension scaling
- CTC injection

### Claude 側：CDT / 空間創発

GPT repo 側では次に `scripts/cdt_2d_toy.py` として入れる予定。

見るもの：

- graph diameter scaling
- ball growth
- spectral dimension
- random rewiring null

### Claude 側：one-flow / 0からevent

GPT repo 側では `one-flow-lab.html` と `scripts/one_flow_sweep.py` に対応。

見るもの：

- 0/white field
- threshold event
- inferred relation
- causal order
- width / chain / d hint

## 理想の共有フォーマット

```text
実験名:
目的:
入れたもの:
入れていないもの:
更新ルール:
親/因果の定義:
パラメータ:
seed数:
測定指標:
結果:
壊した比較:
正直な境界:
次にやること:
コード全文または主要関数:
```

## こちら側の方針

Claude 側の実験をそのまま信じて文章化するのではなく、repo に落とせるものは再実装して、headless で再測定する。

合言葉：

> 同じ言葉に見えるものを、同じ測定で確かめる。
