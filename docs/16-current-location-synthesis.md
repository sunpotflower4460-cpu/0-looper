# 16 — Current location synthesis

## 目的

ここまでの `0-looper` の現在地を、単なる作業ログではなく、**何が見えたのか / 何を言ってよいのか / 次に何を試すべきか**として整理する。

このドキュメントは、Claude 側の合流マップと GPT 側の repo 実装をつなぐための現在地ノートである。

## いまの一文

> 0 は無ではなく、差が立つ前の基底である。  
> 差が event になり、event が relation を持ち、relation に causal order が入ると、幅・時間・器・継承のような構造を、後から測定できる。

ただし、これはまだ宇宙や生命を作ったという話ではない。  
現在地は、**宇宙や生命を語る前に必要な構造条件を toy model で分解している段階**である。

## 全体マップ

```text
0 / white
  ↓
差・ゆらぎ・event
  ↓
relation / causal order
  ↓
geometry hint / width / dimension
  ↓
entropy boundary / arrow
  ↓
closure / vessel
  ↓
inheritance / lineage
```

これまでに repo 側で確認した系列は以下。

```text
one-flow        : 0 → 差 → event → relation → causal order
async causal    : 時間 ← 局所変化
cdt_2d          : 空間的広がり ← 因果葉層
cdt3d route     : 3D CDT へ進むための A-C 検証
α third/soc     : 空間的幅・臨界性
β arrow         : 低エントロピー境界から時間の矢
γ closure       : A→M→A の器
δ inheritance   : closure 後の split と継承
D+ lineage      : p↔m 閉ループの世代持続性
```

## 1. one-flow: 0 から event / relation へ

`one-flow-lab.html` と `scripts/one_flow_sweep.py` では、0-prism と relation-lab を分けず、一本の流れとして扱った。

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

初期の推奨テンプレートは `balanced-oneflow`。

読み：

- 0/white から直接「宇宙」が出たわけではない。
- しかし、**差が event になり、event が causal graph になる最小パイプライン**はできた。
- ここは全体の入口として残す価値がある。

気づいたこと：

> 「白」は空間というより、差が立つ前の基底として扱う方が自然。  
> 空間は最初から置くものではなく、event と relation から後で読むものとして扱う方が筋がよい。

## 2. async causal: 時間は変化の依存から読める

`scripts/async_causal_origin.py` では、大域時計を入れず、局所的な非同期更新だけを記録した。

見たもの：

- event dependency DAG
- topological sort
- causal depth / layer
- width
- dimension scaling
- CTC injection

確認したこと：

- 非同期局所更新から DAG と causal layers が読める。
- `sweeps = N` の scaling では、1D carrier + causal depth として、およそ 2D 的な scaling が出る。
- future → past edge を1本入れると、topological sort が壊れ、DAG が崩れる。

気づいたこと：

> 時間は「外から流れるもの」として入れるより、event の依存順序として読む方が、この研究の方向に合う。  
> ただし、carrier はまだ与えている。空間まで無から出したとは言わない。

## 3. cdt_2d: 因果を保つと広がり、壊すとスモールワールド化する

`scripts/cdt_2d_toy.py` では、2D CDT toy を再測定した。

見たもの：

- diameter scaling
- ball growth dimension
- spectral dimension
- rewiring null
- volume fluctuation robustness

主な結果：

```text
diameter_dimension ≈ 2.06
```

因果を保った場合、ball dim / spectral dim もだいたい 2 付近に揃った。  
一方で、遠距離 rewiring を入れると、diameter が急に縮み、次元推定が上がり、small-world / crumpled 方向へ崩れた。

気づいたこと：

> 関係を増やせば空間になるわけではない。  
> むしろ遠距離関係を入れすぎると、距離が消えてクシャっと潰れる。  
> 空間らしさには、因果的な制限・近傍性・葉層が必要。

## 4. cdt3d route: 3D へ進む前の足場

`scripts/cdt3d_route_min.py` では、3D CDT へ進むための A-C を確認した。

A: 平らな 2+1 積層で、測定器が d≈3 を読むか  
B: `∂Δ4` から `(1,4)/(4,1)` move が閉3多様体条件を保つか  
C: 葉層3トーラスと `(2,6)` move が foliation を保つか

確認したこと：

- A では diameter dimension が約 3 に出る。
- B では `χ=0`, `F=2T`, pseudo-manifold 条件が保たれる。
- C では `(3,1)/(2,2)/(1,3)` の分類と foliation ok が維持される。

気づいたこと：

> 3D 以上では、2D のように「因果だけ」で済ませるのは危険。  
> Regge action / Metropolis / phase scan に進む前に、move validity と不変量チェックを固める必要がある。

## 5. α third/soc: 第三と臨界性

`scripts/alpha_space_map.py` では、Claude 合流マップの α を再現した。

### third

比較：

```text
edge/pair + no causal order      → small-world / crumpled
edge/pair + causal order         → string / d≈1
triangle/third + no causal order → small-world / crumpled
triangle/third + causal order    → 2D-like sheet / d≈1.85
```

重要な気づき：

> 辺だけに順序を入れると紐になる。  
> 三角形、つまり「第三」を持つ関係セルに順序を入れると、幅が出る。

これは、この研究全体でかなり重要な気づき。

言い換えると、

```text
二者関係だけでは、距離か鎖に潰れやすい。
第三があると、面・幅・局所閉包が生まれる。
```

### SOC

2D BTW sandpile では、ゆっくり駆動 + 保存 + しきい値から avalanche 分布が出た。

気づいたこと：

> 構造は、完全な安定でも完全な乱雑でもなく、しきい値とゆっくり駆動の間に現れやすい。  
> これは後の closure / lineage にもつながる。

## 6. β arrow: 時間の矢は低エントロピー境界から立つ

`scripts/beta_arrow.py` では、Kac ring / asymmetry / complexity window / two-arrow を確認した。

見えたこと：

- 低エントロピー初期では `S=0 → S≈1` へ増え、矢が立つ。
- 高エントロピー初期では最初から `S≈1` で、強い矢は立たない。
- 51/49 の微小非対称でも faint arrow があり、閾値はない。
- 複雑さは、秩序と混合の中間で最大になる。
- 低エントロピー境界を `t=0` に置くと、前後両方向へエントロピーが増える。

気づいたこと：

> 時間の矢は、法則そのものに最初から刻まれているというより、境界条件から立つ。  
> そして「構造が宿る場所」は、低エントロピーそのものでも熱的平衡でもなく、その間の混合途中にある。

これは「無音から音楽が始まる」比喩ともつながる。  
完全な無音でも完全な白色雑音でもなく、展開しつつある途中に旋律が見える。

## 7. γ closure: 器は形ではなく閉ループ

`scripts/gamma_closure.py` では、反応拡散 pattern に memory / membrane proxy を結合した。

比較：

```text
no_closure
A_to_M_only
M_to_A_only
closed_loop
```

結果：

- `A_to_M_only`: activator が memory を作るだけでは弱い。
- `M_to_A_only`: 外から memory/confinement があるだけでも弱い。
- `closed_loop`: A が M を作り、M が A を守ると、破壊後の structural similarity と persistence が上がる。

重要な気づき：

> 器らしさは、単に境界の形が閉じていることではない。  
> A が M を作り、M が A を守るという、自己維持の閉ループが器らしさを作る。

ここで「トーラス」や「膜」を直接描くより、

```text
内側の活動が境界を作る
境界が内側の活動を守る
```

という条件を先に置く方が、作為的でない。

## 8. δ inheritance: marker だけでは足りない

`scripts/delta_inheritance.py` では、closed parent を split し、pattern / marker を child に渡した。

結果：

- `marker_only` は marker similarity は高いが、survival は 0。
- `pattern_only` と `full_inheritance` は survival 1.00。
- ただし単発 split では、`full_inheritance` が `pattern_only` を明確に上回るところまでは出なかった。

気づいたこと：

> 継承には marker だけでは足りない。  
> active pattern を渡すことがまず必要。  
> marker の価値は、単発ではなく、繰り返し stress と世代の中で見える可能性がある。

## 9. D+ lineage: p↔m closed loop が世代を越えて残る

`scripts/dplus_lineage_selection.py` では、D の結果を圧縮した lineage-level toy を作った。

個体は2つの状態量を持つ。

```text
p: active pattern strength
m: memory / marker strength
```

比較：

```text
no_inheritance
pattern_only
marker_only
full_loop
```

結果：

- `pattern_only`: 1世代目は強いが、繰り返し stress で消える。
- `marker_only`: 数世代は残るが、active pattern がないので消える。
- `full_loop`: p と m が互いに維持し、lineage が残る。

重要な気づき：

```text
p が m を維持する
m が p を守る
その両方が子へ渡る
```

これが repeated generations で選択優位として見える。

ただしこれは **lineage-level toy** であり、Gray-Scott grid を毎世代 full で回しているわけではない。

## 現在地までに見えた大きなこと

### 1. 関係だけでは足りない

単なる関係網は、small-world / crumpled に潰れやすい。  
必要なのは、関係そのものではなく、**制約された関係**。

候補：

- causal order
- local dependency
- third / triangle
- foliation
- bounded influence

### 2. 因果は空間を守る

因果を壊して遠距離 rewiring すると、距離が消えてしまう。  
これは 2D CDT でも 3D 測定器でも同じ方向。

> 空間は「たくさんつながること」ではなく、「つながりすぎないこと」にも支えられている。

### 3. 第三が幅を生む

二者関係だけだと、紐か毛玉に寄りやすい。  
第三、三角形、局所閉包があると、面・幅・局所性が出る。

これは、神聖幾何学的な「円と円の交点」「三角形」「フラワーオブライフ」を物理視点に翻訳するときの、かなり健全な接点になる。

ただし、神聖幾何学がそのまま物理法則という意味ではない。  
言えるのは、**交点・三角形・局所閉包は、関係が空間的幅を持つための自然なモチーフとして現れる**ということ。

### 4. 時間の矢は境界条件に依存する

低エントロピー境界があると、そこから離れる方向に矢が立つ。  
これは「法則が時間非対称だから矢がある」というより、初期/境界条件の役割が大きい。

### 5. 器は形ではなく閉ループ

器は、単に丸い・閉じている・膜がある、では弱い。  
器らしさは、

```text
内側の活動が境界を作る
境界が内側の活動を守る
```

という閉ループで強くなる。

### 6. 継承は marker 単体ではなく、閉ループの継承

marker だけでは足りない。  
pattern だけでも長期には弱い。  
世代を越えるには、pattern と marker の相互維持が必要になる。

つまり、継承されるべきものは「物質」だけでも「情報」だけでもなく、**相互維持する関係の型**である可能性がある。

## 研究コピーとして強い言い方

安全に言える強い表現：

> 0-looper は、0 から宇宙を作る装置ではない。  
> 0 を「差が立つ前の基底」として扱い、差・関係・因果・幅・時間の矢・器・継承が成立するための条件を、toy model で分解する実験場である。

もう少し詩的に言うなら：

> 種とは、完成形の設計図ではなく、展開の偏りである。  
> そして器とは、形ではなく、内と外が互いを保つ閉ループである。

## 言ってよいこと / まだ言わないこと

### 言ってよいこと

- 0/white から差・event・relation・causal order を一本で生成する toy pipeline を作った。
- 大域時計なしの非同期局所更新から、causal layer と時間らしさを読める toy を作った。
- 2D CDT toy では、因果葉層があると 2D 的広がりが出て、rewiring で崩れることを再測定した。
- 3D CDT route では、A-C の測定器・move・葉層保存チェックを再現した。
- α では、三角形 + 因果順序が 2D 的幅を出す toy を確認した。
- β では、低エントロピー境界から時間の矢が立つ toy を確認した。
- γ では、A→M→A の閉ループが破壊後の構造類似度を上げる toy を確認した。
- δ / D+ では、p↔m closed loop を継承する lineage が repeated stress で残る toy を確認した。

### まだ言わないこと

- 宇宙を作った。
- 空間を完全に無から生成した。
- 重力を導いた。
- 生命を作った。
- 本物の細胞膜や DNA 的遺伝を再現した。
- 神聖幾何学が物理法則そのものだと示した。

## いまの弱点

### 1. toy 間がまだ完全には統合されていない

one-flow、async causal、CDT、closure、inheritance はそれぞれ意味がある。  
しかし、まだ全部が1つの model に統合されているわけではない。

今は「分解して条件を見ている段階」。

### 2. D+ は圧縮モデル

D+ lineage は Gray-Scott grid を毎世代 full に回したものではなく、`p/m` 状態量に圧縮した lineage-level toy。  
結果は示唆的だが、次は full-grid repeated generations が必要。

### 3. 3D CDT はまだ相探索前

3D route は A-C の scaffold。  
Regge action、Metropolis、phase scan はまだ入っていない。

### 4. 「第三」はまだ導出されていない

三角形/第三を入れると幅が出ることは見えた。  
しかし、第三そのものが 0 から自然に出ることまでは示していない。

## 次の優先順位

### Priority 1: D++ full-grid repeated generations

D+ の圧縮モデルを、Gray-Scott grid の full repeated generation で検証する。

```text
closed parent
↓
split into children
↓
stress
↓
survivors only reproduce
↓
marker-rich / marker-poor lineage curve
```

見るもの：

- survival curve
- parent-child similarity
- marker inheritance
- lineage persistence
- marker advantage under repeated stress

### Priority 2: α→γ→δ 統合ブラウザビュー

手動で見やすくするため、ブラウザ上で以下を一続きに見る。

```text
third / width
↓
closure
↓
split / inheritance
```

### Priority 3: 3D CDT step D

`(4,4)`, `(2,3)/(3,2)` move を追加し、validity checks を固める。

その後に Regge action + Metropolis へ進む。

### Priority 4: one-flow と closure の接続

0/white から立った event/relation が、直接 closure field を作る方向へつなぐ。

```text
0/white
↓
event/relation
↓
local closed loop
↓
vessel
↓
split/inheritance
```

## 現在地の結論

いま見えている中心仮説は、かなりはっきりしてきた。

```text
空間らしさには、関係だけでなく、因果と第三が必要。
時間の矢には、低エントロピー境界が必要。
器には、形ではなく A→M→A の閉ループが必要。
継承には、marker 単体ではなく p↔m の閉ループが必要。
```

つまり、ここまでの `0-looper` は、

> 0 から何かが突然完成する話ではなく、  
> 差が立ち、関係が制約され、因果が幅を守り、境界が内側を守り、閉ループが世代を越える条件を探している。

という現在地にいる。

これはかなり良い。  
なぜなら、「宇宙」や「生命」を直接作ろうとしているのではなく、**それらを語る前に必要な条件を一段ずつ分解して測っている**からである。
