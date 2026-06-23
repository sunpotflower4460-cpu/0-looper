# 18 — Map 2 merge: boundary, flow, vessel frontier

## 目的

`0-looper 合流マップ ②：境界の創発・循環・器の最終前線` を repo 側へ合流する。

今回の主題は、前回監査で見えた by-construction の床をさらに溶かすこと。

```text
前回の床:
膜 / 境界を手で書いた。
継承の結合 p↔m を手で書いた。

今回の方向:
境界を相分離から作る。
throughflow から循環を作る。
分裂と継承を、命令ではなく自己複製 + タグ継承として見る。
```

## 追加した repo 実装

```text
scripts/flow_benard_transport.py
scripts/boundary_throughflow.py
scripts/evo_division_inherit.py
scripts/model_h_min.py
```

すべて headless / dependency-free の軽量 toy。  
元資料の Node.js sandbox と完全同一の PDE 実装ではなく、0-looper 側で継続検証しやすい reduced reproducer として入れた。

## 1. flow/benard — throughflow から巡りが立つ

`scripts/flow_benard_transport.py --mode benard`

Rayleigh-Bénard の onset を、標準的な振幅方程式で軽量再現する。

```text
da/dt = σa - a^3
σ = Ra / Ra_c - 1
Ra_c ≈ 658
KE = a^2
```

### reduced model output

| Ra | Ra/Ra_c | KE | state |
|---:|---:|---:|---|
| 200 | 0.304 | 0.000000 | conductive / still |
| 500 | 0.760 | ~0 | conductive / still |
| 650 | 0.988 | ~0 | near threshold |
| 658 | 1.000 | ~0 | critical |
| 700 | 1.064 | 0.000021 | onset |
| 800 | 1.216 | 0.216 | roll / circulation |
| 1200 | 1.824 | 0.824 | roll / circulation |
| 2000 | 3.040 | 2.040 | roll / circulation |

読み：閾値以下では静止 / 伝導、閾値以上で roll / circulation が立つ。

claim tier:

```text
measured in reduced model / known physics reproduction
```

まだ言わないこと：

```text
実際の流体方程式を完全に解いた。
本物の生物循環を作った。
```

## 2. flow/transport_developed — 流れを育ててから注入すると速い

`scripts/flow_benard_transport.py --mode transport`

元マップの重要ポイントは、以前の「差が控えめ」は流れの立ち上がり時間にマスクされていた、という点。  
そこで reduced model では、拡散だけの時定数と、先に発達した流れがある場合の時定数を分けて測る。

### reduced model output

| case | pre-developed flow | injection steps | C_top | speedup |
|---|---:|---:|---:|---:|
| diffusion only | 0 | 200 | 0.033 | 1.0 |
| developed convection | 500 | 200 | 0.400 | 12.0 |

読み：流れが先に育っているなら、同じ注入時間で上部到達濃度が約12倍になる。

claim tier:

```text
measured in reduced model
Pe / heart interpretation = interpretive
```

## 3. flow/pe_scaling — 小さい体は拡散、大きい体は循環

`scripts/flow_benard_transport.py --mode pe`

見るもの：

```text
拡散時間 ~ L^2 / D
循環時間 ~ L / u
Pe = uL / D
```

読み：小さい系では拡散で足りる。大きくなるほど、循環の優位が開く。  
「小さい生物には心臓が要らない / 大きい生物には循環が要る」という直感は、Pe scaling として自然。

ただしこれは interpretive。  
本物の心臓を再現したわけではない。

## 4. boundary/emergent_heal — 境界を手書きから相分離へ

`scripts/boundary_throughflow.py --mode heal`

Allen-Cahn 的な界面張力の proxy として、内部の穴の曲率収縮を測る。

### reduced model output

| case | hole radius start | hole radius final | hole area healed | reading |
|---|---:|---:|---:|---|
| internal φ=-1 bubble | 12.0 | 0.55 | 0.998 | surface tension closes hole |

読み：手で書いた膜ではなく、界面の自由エネルギーから穴が塞がる方向を reduced model で確認する。

claim tier:

```text
measured in reduced model
```

## 5. boundary/ch_stable — 保存量でサイズが安定する

`scripts/boundary_throughflow.py --mode ch`

Cahn-Hilliard 的な保存量の proxy として、総量保存なら droplet size が保たれることを確認する。

claim tier:

```text
measured in reduced model
```

## 6. boundary/throughflow — 荷重を担う死活

`scripts/boundary_throughflow.py --mode throughflow`

崩壊コストを入れ、表面律速の栄養 / 代謝がある場合とない場合を比較する。

### reduced model output

| case | initial area | final area | reading |
|---|---:|---:|---|
| collapse cost only | 900.0 | 5.9 | collapsed / death |
| surface-limited nutrient throughflow | 900.0 | 1682.7 | alive / load-bearing closure |

読み：代謝なしでは崩壊する。表面からの throughflow があると、崩壊コストを担える。

ただし、この reduced model では面積が増えすぎる。  
つまり、

```text
荷重を担う throughflow は出る。
しかし robust stable size との三立はまだ出ていない。
```

claim tier:

```text
load-bearing death/life = measured in reduced model
emergent boundary + robust stable size + throughflow の三立 = frontier
```

## 7. vessel/model_h_min — 流れる境界のある細胞

`scripts/model_h_min.py`

元マップ F1 の最小 Model H は重いので、0-looper では optional reduced amplitude check として入れた。

### reduced model output

| internal KE | area ratio | shrink | integrity | claim |
|---:|---:|---:|---|---|
| ~4.3 | 0.565 | ~43.5% | coherent single boundary | coexistence measured, stable size frontier |

読み：内部循環と境界の共存は reduced model でも確認できる。  
ただし Allen-Cahn 的に縮むので、安定な流れる細胞は frontier のまま。

claim tier:

```text
circulation + coherent boundary coexistence = measured in reduced model
stable flowing cell = frontier
```

## 8. evo/division_inherit — 分裂と継承を命令から外す

`scripts/evo_division_inherit.py`

元マップ F2 では、Gray-Scott 自己複製スポット + 双安定タグによって、分裂と継承を by-construction から少し外している。

0-looper 側では、軽量な spot-level reproducer として入れた。

```text
spots replicate into nearby empty space
child inherits tag A/B
space fills and freezes
selection probe changes footprint / packing
```

確認すること：

- neutral A/B が両方残るか
- child tag が parent tag を継承するか
- selection bias が clean takeover にならず、density / coexistence に化けるか

claim tier:

```text
division + tag inheritance = measured in reduced spot model
clean selection = frontier because turnover is missing
```

重要な読み：

```text
分裂 + 継承は、かなり手書きから外せる。
しかし選択には、誕生だけでは足りない。
死と入れ替わり、つまり turnover が必要。
```

## 9. 監査後の現在地を更新

前回の監査では、γ/δ/D+ は by-construction と見た。

今回のマップ2では、その床が少し分解された。

```text
境界: 手書き膜 → 相分離界面 / throughflow へ
循環: 手書き流れ → Benard onset / Pe scaling へ
分裂・継承: 手書き split/marker → 自己複製 spot + bistable tag へ
選択: まだ frontier。turnover が必要。
```

## 10. claim tier の最終整理

### measured / reduced reproduction

- Benard onset: threshold 以上で circulation amplitude が立つ。
- Developed transport: flow を先に育てると約12倍速い。
- Boundary healing: surface tension proxy で内部穴が閉じる。
- Throughflow death/life: metabolismなしで collapse、surface nutrient ありで load-bearing closure。
- Division + inheritance: spot replication と tag inheritance を測る toy を追加。

### interpretive

- Pe scaling → 心臓 / 循環のサイズ依存。
- トーラス = 境界のない効率的循環器という概念的読み。

### frontier

- Zwicker型 active droplet: 荷重を担う代謝 + robust stable size + emergent boundary の三立。
- Model H++: 流れる境界で安定サイズを保つ。
- Selection emergence: turnover ありの birth/death dynamics。
- third / d-simplex 自体の創発。
- 過去仮説。

## 次の優先順位

### Priority 1: scripts をもう少し PDE 寄りにする

今回の `flow_benard_transport.py` と `boundary_throughflow.py` は reduced model。  
次は、重くなりすぎない範囲で PDE 寄りにする。

- vorticity-streamfunction Benard mini
- semi-implicit Cahn-Hilliard stable droplet
- advected phase field / Model H mini

### Priority 2: evo/division_inherit を full Gray-Scott に寄せる

spot-level toy から、Gray-Scott PDE + bistable tag へ進める。

必要条件：

- self-replicating spots
- tag gated by v
- daughter tag inheritance
- neutral coexistence
- selection probe / turnover negative result

### Priority 3: turnover を入れる

選択には入れ替わりが必要。

候補：

- periodic starvation
- local death / removal
- resource pulses
- chaotic Gray-Scott regime
- birth/death window classification

## 現在地の新しい合言葉

> 閉ループを手で入れる段階から、境界・循環・継承が物理の副作用として立ち上がる条件を探す段階へ。  
> ただし、選択にはまだ turnover が要る。
