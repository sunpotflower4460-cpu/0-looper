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
3. **relation** — event 同士が互いに条件になること
4. **causal order** — 関係に向きが生まれること
5. **observation** — 後から距離・因果・次元を読む測定器

## 現在の実験

### `index.html`

固定された 1D リング上で、0 状態から差・event・cause がどう立つかを見る最初のプロトタイプ。

- 0 状態から微小ゆらぎを入れる
- 局所ルールで差が増幅される
- 閾値を超えた変化を event として拾う
- event 間の依存を cause として結ぶ
- 最長因果鎖と簡易の創発次元ヒントを表示する

これは本物の時空創発モデルではありません。  
固定された 1D リング上の toy model です。  
ただし、「無ではない 0」から、差・関係・順序がどう読み出されるかを見るための足場です。

### `relation-lab.html`

関係性を軸にした実験。  
固定格子を使わず、event と relation だけを成長させます。

- event は順番に生まれる
- parent event から child event へ causal edge を張る
- child の parent は、座標距離ではなく、関係上の compatibility と frontier から選ぶ
- 可視化の座標は force layout で後から置くだけで、力学には使わない
- longest chain / width / comparable ratio / degree / d hint を測る
- 自動 sweep で見つけた推奨テンプレートを UI からすぐ試せる

第一推奨テンプレートは **woven-width-v2**。

> 関係と因果だけで、空間らしい幅と局所性が読める条件はあるか。

## 自動検証

`scripts/relation_sweep.py` で、代表テンプレート、スケーリング、簡易グリッド探索を headless sweep できます。

```bash
python3 scripts/relation_sweep.py --mode presets --seeds 30
python3 scripts/relation_sweep.py --mode scaling --seeds 12
python3 scripts/relation_sweep.py --mode grid --seeds 4 --top 12
```

現時点の推奨順：

1. **woven-width-v2** — 第一推奨。鎖と幅が同時に残る
2. **thin-causal-v2** — 因果鎖強め
3. **wide-frontier-v2** — 空間幅強め
4. **sparse-spacious-v2** — 低密度・広がり強め
5. **low-degree-web** — 最小関係条件の探索向き

GitHub Actions でも push / PR / 手動実行時に sweep が走ります。

## docs

- `docs/00-philosophy.md` — 0、白、無音、プリズム比喩の整理
- `docs/01-protocol.md` — 最初の 0-looper toy の測定プロトコル
- `docs/02-relation-first-universe-hypothesis.md` — 関係性を軸にした宇宙条件の仮説
- `docs/03-automated-sweep-results.md` — 初回自動 sweep 結果と推奨テンプレート
- `docs/04-expanded-sweep-results.md` — 追加 sweep / scaling / grid 結果

## Claim tiers

- **measured**: このコードで直接測ったこと
- **observed**: 可視化上そう見えること
- **interpretive**: 既存物理概念への読み替え
- **analogy**: 音楽・神聖幾何学・生命への比喩
- **frontier**: まだ未検証の前線

## 現在の合言葉

> 無音は、音楽の不在ではない。  
> それは、まだ鳴っていない音楽を受け止める基底である。
