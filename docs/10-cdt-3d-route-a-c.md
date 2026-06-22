# 10 — 3D CDT route A-C checks

## 目的

Claude 同期資料②「3D CDTルート」に沿って、まず steps A-C を repo 側で再現・確認する。

この段階の目標は、まだ 3D CDT の相探索ではない。

```text
A. 3D 次元測定 machinery の検証
B. 3D 単体複体 + 汎用 bistellar move の検証
C. 葉層 3 トーラス + 葉層保存 (2,6) move の検証
```

Claude 資料でのルートは、2D では因果だけで足りたが、3D以上では Regge 作用と Monte Carlo が必要になるため、A-C を固めてから D-E-F へ進む、という整理。

## 実装

`scripts/cdt3d_route_min.py`

依存なし Python。  
元資料の JS / Node 実験に合わせて、LCG は `s = s*1664525 + 1013904223` 系を使用。

## A. 3D measurement machinery

### 目的

平らな 2+1 積層が、直径スケーリングとスペクトル次元で `d≈3` と読めるか。  
さらに近道を入れるとスモールワールド方向へ潰れるか。

### 結果

| side | vertices | diameter | ball dim | spectral dim | avg degree |
|---:|---:|---:|---:|---:|---:|
| 6 | 216 | 7 | 1.96 | 2.82 | 8.00 |
| 8 | 512 | 9 | 2.36 | 3.10 | 8.00 |
| 10 | 1000 | 11 | 2.43 | 3.13 | 8.00 |
| 14 | 2744 | 16 | 2.62 | 3.13 | 8.00 |

```text
diameter_slope = 0.324
diameter_dimension = 3.08
```

読み：直径スケーリングとスペクトル次元は 3 付近。ball growth は小さい 3D では中域べき窓が狭く、低めに出る。Claude 資料の注意と一致。

### 近道 null

| rewiring f | vertices | diameter | ball dim | spectral dim |
|---:|---:|---:|---:|---:|
| 0.00 | 2744 | 16 | 2.62 | 3.13 |
| 0.05 | 2744 | 8 | 4.02 | 3.65 |
| 0.15 | 2744 | 7 | NaN | 4.29 |
| 0.30 | 2744 | 6 | NaN | 5.18 |

読み：近道注入で直径が急縮小し、スペクトル次元が上がる。3Dでも近道はスモールワールド化を起こす。

## B. Simplex complex + generic bistellar move

### 目的

最小の `S^3` である `∂Δ4` から始め、(1,4) と (4,1) が必要な閉3多様体条件を保つか。

見る条件：

- 全三角形がちょうど2テトラに共有される
- `F = 2T`
- `χ = V - E + F - T = 0`

### 結果

| step | move | V | E | F | T | chi | F=2T | pseudo | bad faces |
|---:|---|---:|---:|---:|---:|---:|---|---|---:|
| 0 | initial boundary Δ4 | 5 | 10 | 10 | 5 | 0 | True | True | 0 |
| 1 | (1,4) | 6 | 14 | 16 | 8 | 0 | True | True | 0 |
| 2 | (1,4) | 7 | 18 | 22 | 11 | 0 | True | True | 0 |
| 3 | (1,4) | 8 | 22 | 28 | 14 | 0 | True | True | 0 |
| 4 | (1,4) | 9 | 26 | 34 | 17 | 0 | True | True | 0 |
| 5 | (1,4) | 10 | 30 | 40 | 20 | 0 | True | True | 0 |

逆の (4,1) でも巻き戻し可能。  
この段階では葉層なしの汎用 bistellar scaffold。

## C. Foliated 3-torus + leaf-preserving (2,6)

### 目的

時間ラベル付きの葉層 3 トーラスを作り、テトラを `(3,1)/(2,2)/(1,3)` に分類し、葉層保存 move `(2,6)` が多様体条件と葉層条件を保つか。

設定：`L=3, T=4`

期待初期値：

```text
V = 36
Tets = 216
(3,1)/(2,2)/(1,3) = 72/72/72
spacelike triangles = 2 L^2 T = 72
```

### 結果

| step | V | E | F | Tets | chi | F=2T | pseudo | (3,1) | (2,2) | (1,3) | invalid | spacelike | foliation ok |
|---:|---:|---:|---:|---:|---:|---|---|---:|---:|---:|---:|---:|---|
| 0 | 36 | 252 | 432 | 216 | 0 | True | True | 72 | 72 | 72 | 0 | 72 | True |
| 1 | 37 | 257 | 440 | 220 | 0 | True | True | 74 | 72 | 74 | 0 | 74 | True |
| 2 | 38 | 262 | 448 | 224 | 0 | True | True | 76 | 72 | 76 | 0 | 76 | True |
| 3 | 39 | 267 | 456 | 228 | 0 | True | True | 78 | 72 | 78 | 0 | 78 | True |
| 4 | 40 | 272 | 464 | 232 | 0 | True | True | 80 | 72 | 80 | 0 | 80 | True |
| 5 | 41 | 277 | 472 | 236 | 0 | True | True | 82 | 72 | 82 | 0 | 82 | True |

読み：Claude 側の期待通り、`72/72/72 → 74/72/74 → ...` と動き、`χ=0`, `F=2T`, `pseudo`, `foliation ok` が維持された。

## 正直な境界

言ってよいこと：

> 3D CDT へ進む前段として、測定 machinery、汎用単体 move、葉層3トーラス、葉層保存 (2,6) move の検証を repo 側でも再現した。

まだ言わないこと：

> 3D CDT の extended 相を出した。
> Regge 作用を入れた。
> Monte Carlo で相探索した。
> 3D空間、または4D時空を創発させた。

## 次

Claude 資料の step D に進む。

- `(4,4)` move：spacelike edge 周りの flip
- `(2,3)/(3,2)` move：timelike triangle / timelike edge 周りの Pachner move
- moveごとの valid 条件
- move後の `F=2T`, `χ=0`, pseudo, foliation, link check

D が固まったら、E の Regge action + Metropolis へ進む。
