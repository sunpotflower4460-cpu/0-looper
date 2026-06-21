# 05 — Root principle check

## 問い

この repo は、いま話している「関係性を軸に、宇宙そのものと同じ根本原理・条件へ近づける」という目的を押さえているか。

## 暫定回答

**半分は押さえている。だが、まだ根本原理そのものではない。**

現在の `relation-lab-v3.html` が押さえているのは、次の部分である。

```text
0 / white
↓
event
↓
relation
↓
causal order
↓
width / chain / comparable ratio を後から読む
```

これは、「空間を先に置かず、関係と因果順序から幾何らしさを読む」という方向には合っている。

## 押さえている点

### 1. 空間を最初に置かない

v3 では、表示座標は後付け。  
ノードの親選択は、x/y座標ではなく、関係上の条件で決まる。

これは重要。

> 座標があるから近いのではなく、関係があるから後から距離らしさを読む。

### 2. event が先にある

世界を「点の集合」として固定するのではなく、発生した event の履歴として見る。

### 3. 因果順序を持つ

parent → child の向きを持つ。  
この向きがあることで、単なる関係網ではなく、順序を持つ構造になる。

### 4. 失敗条件を持つ

- chain collapse：全順序へ潰れる
- hairball collapse：全結合の毛玉になる
- weak growth：幅や鎖が育たない

これらを失敗として明示しているのは、研究上かなり大事。

## まだ足りない点

### 1. ルールがまだ外から与えられている

現在の `compatibility`、`frontier`、`balance` は、実験者が与えた条件である。  
これは「宇宙そのものの根本原理」ではなく、「根本原理候補を探すための足場」。

次は、これらのパラメータをより少ない保存則・対称性・変分原理から出したい。

### 2. metric recovery がまだ弱い

現在は、width、longest chain、comparable ratio を見ている。  
これは幾何らしさの入口だが、距離そのものを復元してはいない。

次に必要なのは、関係グラフだけから近傍・距離・層を再構成すること。

### 3. dimension validation がまだ簡易

`d_hint` はあくまで簡易指標。  
次は event 数を変えたスケーリング、Myrheim-Meyer 的な比較、chain scaling を分けて測る。

### 4. 0 / white から event が自然発生しているわけではない

relation-lab は event を増やす成長モデル。  
0-prism は差の発生を見る補助実験。  
まだ、この2つは完全には統合されていない。

本当に根本原理に近づけるなら、次は：

```text
0 / white の場
↓
差が立つ
↓
event が生まれる
↓
relation / causal order が生まれる
↓
geometry を読む
```

まで一本化する必要がある。

## 現在の正しい位置づけ

言ってよいこと：

> 関係と因果順序だけを成長させる toy model で、鎖崩壊と毛玉崩壊を避け、幅と深さが共存する条件を探している。

まだ言わないこと：

> 宇宙と同じ原理を実装した。
> 時空を無から作った。
> 重力を導いた。
> 0から本物の宇宙が生まれた。

## 次の本命ステップ

### Phase R1：表示を安定させる

force layout ではなく、因果層表示を使う。  
これが `relation-lab-v3.html`。

### Phase R2：距離を後から読む

関係グラフだけから、次を測る。

- shortest path distance
- ancestor overlap distance
- local neighborhood
- layer width
- causal interval size

### Phase R3：0-prism と relation-lab をつなぐ

0-prism で発生した event を relation-lab の causal graph に流し込む。

### Phase R4：最小原理へ圧縮する

`compatibility / frontier / balance` を、より根本的な言葉に置き換える。

候補：

- bounded influence
- causal consistency
- non-collapse
- balance / conservation
- no preferred coordinate
- local closure

## 現時点の結論

この repo は、根本原理の**入口**は押さえている。

特に、

> 空間を先に置かず、関係と因果順序から後で幾何を読む

という方向は合っている。

ただし、まだ「根本原理そのもの」ではなく、**根本原理を探すための実験台**である。

次にやるべきことは、見た目をきれいにすることではなく、

> 関係だけから距離を読めるか
> 0からeventが立ち、eventからrelationが立つ流れを一本化できるか

である。
