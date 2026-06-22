# 09 — 2D CDT toy results

## 目的

Claude 同期資料の実験2 `cdt_2d` を Python に移植し、repo 側で再測定する。

問い：

> 関係だけでは潰れる。時間で葉層化した因果的ランダム三角形分割なら、広がった2D空間が出るか。因果を壊すと潰れるか。

## 実装

`scripts/cdt_2d_toy.py`

Claude 側の Node.js 実装を、依存なし Python に移植した。

### 入れるもの

- 時間スライス `T`
- 各スライスの 1D 空間リング
- 隣接スライス間の causal up/down triangles
- 周期境界
- 空間体積のゆらぎ `fluct`

### 入れないもの

- 3D / 4D Regge 作用
- Monte Carlo action sampling
- 現実宇宙の時空主張

2D では Einstein-Hilbert 作用がトポロジー項なので、この toy は「因果葉層だけで2Dの広がりが出るか」を見る。

## 実行コマンド

```bash
python3 scripts/cdt_2d_toy.py --mode all --sources 6
```

## 再測定結果

### diameter / ball / spectral scaling

| side | vertices | diameter | ball dim | spectral dim | avg degree |
|---:|---:|---:|---:|---:|---:|
| 14 | 219 | 8 | 1.63 | 1.81 | 6.00 |
| 20 | 418 | 11 | 2.11 | 1.99 | 6.00 |
| 28 | 755 | 15 | 2.22 | 2.18 | 6.00 |
| 40 | 1612 | 21 | 2.19 | 2.10 | 6.00 |

```text
diameter_slope = 0.486
diameter_dimension = 2.06
```

読み：直径スケーリング、ball growth、spectral dimension がだいたい2付近に揃う。小さい side=14 は有限サイズ効果で低め。

### causality-breaking rewiring

| rewiring f | vertices | diameter | ball dim | spectral dim | avg degree |
|---:|---:|---:|---:|---:|---:|
| 0.00 | 1633 | 22 | 1.94 | 2.01 | 6.00 |
| 0.05 | 1633 | 10 | 3.47 | 2.60 | 6.00 |
| 0.15 | 1633 | 8 | 4.26 | 3.28 | 6.00 |
| 0.30 | 1633 | 7 | NaN | 4.42 | 6.00 |

読み：因果的な近傍を壊して遠距離リンクを注入すると、直径が急に縮み、次元推定が上がる。30% では ball growth の中域推定が壊れるほどスモールワールド寄りになる。

### fluctuation robustness

| fluct | vertices | diameter | ball dim | spectral dim | avg degree |
|---:|---:|---:|---:|---:|---:|
| 2 | 1633 | 22 | 1.94 | 2.01 | 6.00 |
| 5 | 1939 | 23 | 2.22 | 2.09 | 6.00 |
| 8 | 876 | 20 | 1.93 | 1.89 | 6.00 |
| 12 | 2476 | 21 | 2.15 | 2.20 | 6.00 |

読み：体積ゆらぎを強めても、推定次元はだいたい2付近に残る。seed と有限サイズの影響はあるが、方向は Claude 側の結果と一致。

## Claude 同期資料との一致点

Claude 側の代表出力は、因果ありで直径スケーリング `d≈2.07`、ball成長 `d≈2.12`、spectral `d_s≈2.11`。repo 側の再測定でも、diameter dimension `2.06`、side 20〜40 の ball/spectral が概ね2付近に出た。

Claude 側の null では、因果を壊す rewiring で直径が縮み、ball/spectral 次元が上がる。repo 側でも 5%, 15%, 30% rewiring で同じ崩れ方を確認した。

## 正直な境界

言ってよいこと：

> 2D CDT toy を Python に移植し、因果葉層があると2D的な広がりが出て、遠距離 rewiring でスモールワールド方向へ潰れることを再測定した。

まだ言わないこと：

> 空間を無から生成した。
> 現実宇宙の空間次元を導いた。
> 3D/4D重力を実装した。

これは **空間←因果** の toy reproduction。  
因果葉層は所与であり、2D限定では作用がトポロジーなので因果のみで試せる、という位置づけ。

## 次

1. `scripts/cdt_2d_toy.py` を CI に入れて継続テスト
2. 複数 seed 平均の summary mode を追加
3. 2D CDT の簡易ブラウザ可視化を追加
4. 3D scaffold に進む前に、2D の null / finite-size 効果をもう少し固める
5. one-flow / async causal / cdt_2d を README 上で三本柱として整理する
