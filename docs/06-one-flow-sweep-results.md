# 06 — One-flow sweep results

## 目的

今回の目的は、0-prism と relation-lab を分けず、一本の流れとして扱うこと。

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

これはまだ宇宙生成ではない。  
ただし、「0から差、差からevent、eventから関係、関係から因果、因果から幾何らしさ」という一本の実験台になっている。

## 追加したもの

- `one-flow-lab.html`：ブラウザで見る統合ラボ
- `scripts/one_flow_sweep.py`：headless 自動検証

## 初回 preset sweep

ローカルで各テンプレート 20 seeds を確認した初期結果。

| template | events | avg degree | chain | width | comparable r | d hint | 読み |
|---|---:|---:|---:|---:|---:|---:|---|
| balanced-oneflow | 95.1 | 2.44 | 8.9 | 34.9 | 0.049 | 2.12 | 第一推奨 |
| quiet-crystallize | 93.7 | 2.73 | 9.8 | 31.5 | 0.059 | 2.01 | 静かに整う |
| active-web | 96.2 | 3.16 | 10.8 | 27.3 | 0.078 | 1.94 | 関係が活発 |
| wide-memory | 95.1 | 4.33 | 12.4 | 21.8 | 0.110 | 1.82 | 因果鎖強め |
| sparse-events | 75.2 | 2.50 | 8.8 | 26.8 | 0.059 | 2.03 | event少なめ |
| hairball-null | 96.4 | 16.03 | 21.4 | 8.9 | 0.469 | 1.50 | 失敗例：濃すぎる |
| weak-link-null | 54.3 | 0.08 | 1.9 | 52.2 | 0.002 | 5.49 | 失敗例：関係が弱すぎる |

## 現時点のおすすめ順

### 1. balanced-oneflow

```text
mu = 0.90
D = 0.22
eta = 0.012
threshold = 0.60
causal radius = 3
memory = 8
birth cap = 6
```

第一推奨。  
差がeventに変わり、event間のrelationもほどよく生まれる。  
`d hint` が 2 付近に寄り、1D carrier + time という toy として自然な読みになりやすい。

### 2. quiet-crystallize

```text
mu = 0.75
D = 0.26
eta = 0.008
threshold = 0.55
causal radius = 3
memory = 10
birth cap = 4
```

静かに整うテンプレート。  
ゆらぎを抑え、にじみを少し強める。  
eventは十分出るが、関係は暴れにくい。

### 3. active-web

```text
mu = 1.10
D = 0.16
eta = 0.016
threshold = 0.62
causal radius = 4
memory = 8
birth cap = 8
```

関係が活発。  
差→event→relation の流れが見やすい。  
ただし濃くなりすぎる方向へ近いので、hairballに注意。

### 4. wide-memory

```text
mu = 0.90
D = 0.22
eta = 0.012
threshold = 0.60
causal radius = 4
memory = 14
birth cap = 6
```

記憶を広くして、因果鎖を強める。  
時間列・旋律性を見るテンプレート。

### 5. sparse-events

```text
mu = 0.80
D = 0.26
eta = 0.008
threshold = 0.70
causal radius = 3
memory = 8
birth cap = 3
```

eventを絞る比較用。  
静かだが、relation が弱くなりすぎない範囲を探せる。

## 今回の判断

一本の流れとして一番良い入口は **balanced-oneflow**。

理由：

> 0/white から差が立ち、その差が event になり、event 間の relation から causal order が読める。しかも、relation が濃すぎる毛玉にも、弱すぎる断片にも潰れていない。

ただし、根本原理としてはまだ足りない。

- carrier が固定されている
- event 閾値は外から与えている
- relation は recent + local dependency で読んでいる
- 距離復元はまだ行っていない

## 次に必要な検証

1. `balanced-oneflow` 周辺の grid sweep
2. event 数を増やした scaling
3. relation graph だけから距離を復元する
4. carrier を弱め、関係から近傍を再構成する
5. 2D carrier 版で d hint が 3 付近に寄るか見る

## claim discipline

言ってよいこと：

> 0/white から差・event・relation・causal order を一本で生成する toy model を作り、幅と因果鎖が共存するテンプレートを見つけた。

まだ言わないこと：

> 宇宙そのものを作った。
> 空間を無から生成した。
> 重力を導いた。
> 現実宇宙と同じ原理を証明した。
