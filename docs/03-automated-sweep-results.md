# 03 — Automated sweep results

## 実行内容

`relation-lab.html` の関係性ルールを、Python の headless 版 `scripts/relation_sweep.py` に移して、代表テンプレートを複数 seed で検証した。

これは「宇宙を作れた」検証ではない。  
見ているのは、関係＋因果順序の成長が、以下の悪い崩壊を避けられるかである。

- **chain collapse**：ほぼ全順序になり、幅が消える
- **hairball collapse**：関係が濃すぎて、距離が読めない毛玉になる
- **frozen / weak growth**：event が十分な鎖や幅を持たない

狙う状態は、**鎖もあり、幅もあり、しかし毛玉ではない**中間領域。

## 今回の sweep

ローカル headless sweep。各テンプレート 30 seeds。`maxn = 260`。

| template | avg degree | longest chain | width | comparable r | d hint | 判定 |
|---|---:|---:|---:|---:|---:|---|
| woven-width | 4.94 | 42.7 | 20.7 | 0.227 | 1.48 | 推奨 |
| thin-causal | 3.95 | 63.5 | 13.4 | 0.299 | 1.34 | 推奨 / 因果鎖強め |
| wide-frontier | 3.97 | 46.4 | 18.0 | 0.254 | 1.45 | 推奨 / 安定観察向き |
| sparse-spacious | 3.97 | 29.7 | 26.1 | 0.144 | 1.65 | 推奨 / 空間幅強め |
| chain-null | 1.98 | 258.0 | 3.0 | 0.985 | 1.00 | 失敗例：鎖崩壊 |
| hairball-null | 59.92 | 258.0 | 3.0 | 1.000 | 1.00 | 失敗例：毛玉崩壊 |
| random-null | 4.93 | 19.8 | 30.5 | 0.215 | 1.87 | 比較用：幅はあるが因果鎖が弱い |

## おすすめテンプレート

### 1. woven-width

現時点の第一推奨。

```text
birth = 2
frontier = 32
parents = 4
compatibility = 0.35
balance = 0.70
max events = 260
```

特徴：

- 鎖と幅が両方残る
- 平均次数が約 5 で、毛玉になりにくい
- comparable ratio が約 0.23 で、全順序に潰れていない
- 関係性から幾何らしさを読む最初の観察に向いている

### 2. thin-causal

因果鎖を強めに見るテンプレート。

```text
birth = 2
frontier = 16
parents = 3
compatibility = 0.35
balance = 0.70
max events = 260
```

特徴：

- longest chain が長い
- 幅は残るが、woven-width より時間列が強い
- 「関係が旋律になる」感覚を見るのに向いている

### 3. wide-frontier

安定観察向け。

```text
birth = 2
frontier = 60
parents = 3
compatibility = 0.55
balance = 0.20
max events = 260
```

特徴：

- 幅と鎖がほどよく共存
- balance 圧が弱く、やや自然な関係拡散に近い
- パラメータを動かす基準点に向く

### 4. sparse-spacious

空間幅を強めに見るテンプレート。

```text
birth = 1
frontier = 44
parents = 3
compatibility = 0.75
balance = 0.45
max events = 260
```

特徴：

- width が広い
- comparable ratio が低め
- 因果鎖は短めで、空間的な幅を見る比較に向いている

## 今回の結論

現時点で、関係性方向の第一テンプレートは **woven-width**。

理由：

> 全順序の鎖にも、全結合の毛玉にも潰れず、因果的な深さと空間的な幅が同時に残る。

これはまだ宇宙そのものではない。  
しかし、宇宙的条件に近づけるための toy model としては、かなり良い第一候補である。

## 次の検証

1. `maxn` を 260 → 500 → 1000 に伸ばし、longest chain と width のスケーリングを見る
2. `woven-width` の周辺だけ細かく sweep する
3. comparable ratio を Myrheim-Meyer 的な次元推定へ接続できるか調べる
4. event graph から force layout 以外の距離推定を行う
5. Gray-Scott の birth/death/split event をこの causal graph に流し込む

## claim discipline

言ってよいこと：

> 関係と因果順序だけを成長させる toy model で、鎖崩壊と毛玉崩壊を避け、幅と鎖が共存するテンプレートを見つけた。

まだ言わないこと：

> 宇宙を再現した。  
> 時空を無から作った。  
> 重力を導いた。  
> 現実宇宙と同じ原理を証明した。
