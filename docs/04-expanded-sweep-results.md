# 04 — Expanded relation sweep results

## 実行内容

関係性方面の自動検証を追加で広げた。

今回見たのは、**宇宙そのものの再現**ではなく、以下の中間領域が安定して出るかである。

> 鎖がある。  
> 幅がある。  
> しかし全順序の鎖にも、全結合の毛玉にも潰れない。

これは、関係＋因果順序から幾何らしさを読むための最初の条件として扱う。

## 追加した検証モード

`scripts/relation_sweep.py` に3つのモードを追加した。

```bash
python3 scripts/relation_sweep.py --mode presets --seeds 30
python3 scripts/relation_sweep.py --mode scaling --seeds 12
python3 scripts/relation_sweep.py --mode grid --seeds 4 --top 12
```

GitHub Actions でも、push / PR / 手動実行時にこの3種類を回す。

## Preset sweep / 30 seeds / maxn=260

| template | avg degree | longest chain | width | comparable r | d hint | 読み |
|---|---:|---:|---:|---:|---:|---|
| woven-width-v2 | 4.94 | 42.9 | 21.0 | 0.227 | 1.48 | 第一推奨 |
| woven-width-v1 | 4.94 | 42.7 | 20.7 | 0.227 | 1.48 | 旧推奨。v2とほぼ同等 |
| thin-causal-v2 | 4.95 | 78.5 | 11.6 | 0.425 | 1.28 | 因果鎖強め |
| wide-frontier-v2 | 4.92 | 29.3 | 29.5 | 0.157 | 1.65 | 空間幅強め |
| sparse-spacious-v2 | 3.97 | 29.7 | 26.1 | 0.144 | 1.65 | 低密度・広がり強め |
| low-degree-web | 2.98 | 35.0 | 20.4 | 0.175 | 1.57 | 低次数の関係網 |

## Compact grid sweep / 756 patterns / 4 seeds / maxn=220

大まかなグリッド探索では、以下が上位に来た。

| rank | birth | frontier | parents | comp | balance | avg degree | chain | width | comparable r | d hint |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1 | 32 | 4 | 0.50 | 0.55 | 5.04 | 39.3 | 23.5 | 0.247 | 1.47 |
| 2 | 2 | 32 | 4 | 0.50 | 0.55 | 5.04 | 39.3 | 23.5 | 0.247 | 1.47 |
| 3 | 3 | 32 | 4 | 0.50 | 0.55 | 5.04 | 39.3 | 23.5 | 0.247 | 1.47 |
| 4 | 1 | 32 | 4 | 0.50 | 0.85 | 5.04 | 39.0 | 23.5 | 0.247 | 1.47 |
| 5 | 2 | 32 | 4 | 0.50 | 0.85 | 5.04 | 39.0 | 23.5 | 0.247 | 1.47 |

注：birth は最終的な graph 構造よりもアニメーション速度に効く。最終 event 数を固定すると、同じ親選択ルールでは graph 指標がほぼ一致する。

## Scaling sweep / sizes 120, 180, 260, 380, 520

### woven-width-v2

| maxn | avg degree | longest chain | width | comparable r | d hint |
|---:|---:|---:|---:|---:|---:|
| 120 | 4.97 | 23.0 | 19.2 | 0.272 | 1.53 |
| 180 | 4.98 | 32.6 | 20.8 | 0.251 | 1.49 |
| 260 | 4.98 | 44.4 | 21.3 | 0.239 | 1.47 |
| 380 | 5.01 | 61.9 | 21.9 | 0.226 | 1.44 |
| 520 | 5.03 | 84.3 | 23.1 | 0.220 | 1.41 |

読み：平均次数は安定し、comparable r は 0.22 前後へ寄る。鎖は伸びるが、幅も消えない。現時点で一番バランスが良い。

### thin-causal-v2

| maxn | avg degree | longest chain | width | comparable r | d hint |
|---:|---:|---:|---:|---:|---:|
| 120 | 4.91 | 38.5 | 11.3 | 0.461 | 1.31 |
| 180 | 4.94 | 55.3 | 11.5 | 0.443 | 1.29 |
| 260 | 5.00 | 79.9 | 12.0 | 0.433 | 1.27 |
| 380 | 5.00 | 116.0 | 12.9 | 0.430 | 1.25 |
| 520 | 4.98 | 158.3 | 12.9 | 0.426 | 1.24 |

読み：因果鎖が強い。幅は残るが細め。時間列・旋律性を見るテンプレート。

### wide-frontier-v2

| maxn | avg degree | longest chain | width | comparable r | d hint |
|---:|---:|---:|---:|---:|---:|
| 120 | 4.87 | 16.0 | 25.2 | 0.203 | 1.74 |
| 180 | 4.90 | 21.7 | 25.9 | 0.176 | 1.70 |
| 260 | 4.89 | 28.8 | 29.3 | 0.159 | 1.66 |
| 380 | 4.90 | 40.2 | 30.9 | 0.147 | 1.61 |
| 520 | 4.93 | 52.5 | 31.4 | 0.139 | 1.58 |

読み：幅がかなり強い。空間的な広がりを見るときの候補。

### sparse-spacious-v2

| maxn | avg degree | longest chain | width | comparable r | d hint |
|---:|---:|---:|---:|---:|---:|
| 120 | 3.87 | 16.0 | 20.9 | 0.168 | 1.74 |
| 180 | 3.93 | 22.4 | 22.5 | 0.155 | 1.67 |
| 260 | 3.96 | 30.3 | 24.7 | 0.146 | 1.64 |
| 380 | 3.97 | 44.0 | 26.1 | 0.141 | 1.58 |
| 520 | 4.00 | 57.1 | 30.5 | 0.137 | 1.55 |

読み：低密度で幅が残る。毛玉にはなりにくいが、因果的な深さは woven-width より弱め。

### low-degree-web

| maxn | avg degree | longest chain | width | comparable r | d hint |
|---:|---:|---:|---:|---:|---:|
| 120 | 2.93 | 17.5 | 16.9 | 0.193 | 1.71 |
| 180 | 2.96 | 26.3 | 18.3 | 0.181 | 1.61 |
| 260 | 2.98 | 35.1 | 20.5 | 0.176 | 1.57 |
| 380 | 2.98 | 49.2 | 22.5 | 0.170 | 1.53 |
| 520 | 2.98 | 63.3 | 24.3 | 0.166 | 1.51 |

読み：平均次数が約3でかなり軽い。関係が少ないのに幅と鎖が残るため、今後の「最小関係条件」探索に向く。

## 現時点のおすすめ順

### 1. woven-width-v2

最初に見るならこれ。

```text
birth = 2
frontier = 32
parents = 4
compatibility = 0.50
balance = 0.55
max events = 260
```

選定理由：鎖・幅・次数・comparable r のバランスが一番良い。

### 2. thin-causal-v2

「関係が旋律になる」方向を見たいとき。

```text
birth = 2
frontier = 16
parents = 4
compatibility = 0.50
balance = 0.55
max events = 260
```

### 3. wide-frontier-v2

空間的な幅、同時面っぽさを見たいとき。

```text
birth = 2
frontier = 60
parents = 4
compatibility = 0.50
balance = 0.55
max events = 260
```

### 4. sparse-spacious-v2

低密度で広がる関係網を見たいとき。

```text
birth = 1
frontier = 44
parents = 3
compatibility = 0.75
balance = 0.45
max events = 260
```

### 5. low-degree-web

最小関係でどこまで幾何らしさが残るかを見る候補。

```text
birth = 2
frontier = 80
parents = 2
compatibility = 0.75
balance = 0.20
max events = 260
```

## 今回の暫定結論

現時点の主役テンプレートは **woven-width-v2**。

> 関係の密度を平均次数約5に抑えながら、因果的な深さと空間的な幅が同時に残る。

この結果はまだ「時空の創発」ではない。  
しかし、関係性方向の次の手動観察では、woven-width-v2 を第一候補にする価値がある。

## 次に見るポイント

手動観察では、次を見る。

1. ノードが一直線に潰れていないか
2. 線が濃すぎて毛玉になっていないか
3. 層・枝・束のような構造が見えるか
4. width と longest chain が同時に残るか
5. comparable r が 0.15〜0.35 くらいに保たれるか
6. average degree が 3〜6 くらいに保たれるか

この条件を満たすなら、次は relation graph から距離推定、層検出、局所近傍の再構成へ進む。
