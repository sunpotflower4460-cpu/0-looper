# 0-looper

**0 は無ではない。**  
このリポジトリは、AeternaGenesis の根本仮説を最小の形で試すための実験場です。

> 白は空間ではなく、未分化の存在である。  
> 0 は何も無いことではなく、まだ差が立っていない基底状態である。  
> そこにルール・ゆらぎ・不安定性があると、差、関係、順序、因果、次元が読み出される。

## 目的

最初から「生命」「トーラス」「宇宙」「重力」を描きません。  
最初に置くのは、次の最小材料だけです。

1. **0 / white** — 差が立つ前の基底状態
2. **rule** — 次が今にどう依存するか
3. **event** — 差が観測可能な出来事になること
4. **relation** — event 同士が互いに条件になること
5. **causal order** — 関係に向きが生まれること
6. **observation** — 後から距離・因果・次元を読む測定器

## 現在の本命実験

### `one-flow-lab.html`

0-prism と relation-lab を分けず、一本の流れとして見る統合ラボ。

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

第一推奨テンプレートは **balanced-oneflow**。

> 0から差が立ち、eventとrelationがほどよく生まれ、d hintが2付近に寄りやすい。

## 補助実験

### `relation-lab-v3.html`

field から event を発生させず、event と relation の成長だけを見るラボ。  
関係性だけを切り出して確認したいときに使う。

### `zero-prism.html`

0 / white が局所ルールでどの波長モードへ分かれるかを見る補助ラボ。

## 自動検証

### one-flow sweep

```bash
python3 scripts/one_flow_sweep.py --mode presets --seeds 20
python3 scripts/one_flow_sweep.py --mode grid --seeds 3 --top 12
```

現時点の推奨順：

1. **balanced-oneflow** — 一本化の第一推奨
2. **quiet-crystallize** — 静かに整う
3. **active-web** — 関係が活発
4. **wide-memory** — 因果鎖・記憶を強める
5. **sparse-events** — event少なめの比較用

### relation-only sweep

```bash
python3 scripts/relation_sweep.py --mode presets --seeds 30
python3 scripts/relation_sweep.py --mode scaling --seeds 12
python3 scripts/relation_sweep.py --mode grid --seeds 4 --top 12
```

GitHub Actions でも push / PR / 手動実行時に sweep が走ります。

## docs

- `docs/00-philosophy.md` — 0、白、無音、プリズム比喩の整理
- `docs/01-protocol.md` — 最初の 0-looper toy の測定プロトコル
- `docs/02-relation-first-universe-hypothesis.md` — 関係性を軸にした宇宙条件の仮説
- `docs/03-automated-sweep-results.md` — 初回 relation sweep 結果
- `docs/04-expanded-sweep-results.md` — 追加 relation sweep / scaling / grid 結果
- `docs/05-root-principle-check.md` — 根本原理として何が足りないか
- `docs/06-one-flow-sweep-results.md` — 一本化 one-flow sweep 結果

## Claim tiers

- **measured**: このコードで直接測ったこと
- **observed**: 可視化上そう見えること
- **interpretive**: 既存物理概念への読み替え
- **analogy**: 音楽・神聖幾何学・生命への比喩
- **frontier**: まだ未検証の前線

## 現在の合言葉

> 無音は、音楽の不在ではない。  
> それは、まだ鳴っていない音楽を受け止める基底である。
