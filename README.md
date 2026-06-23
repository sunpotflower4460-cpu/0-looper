# 0-looper

**0 は無ではない。**  
このリポジトリは、AeternaGenesis / 0-looper の根本仮説を、最小の toy / reduced mechanism check として積み上げる実験場です。

> 白は空間ではなく、未分化の存在である。  
> 0 は何も無いことではなく、まだ差が立っていない基底状態である。  
> そこにルール・ゆらぎ・不安定性があると、差、関係、因果、空間、物質、曲率、構造が読み出される。

## Claim discipline

- **measured**: このコードで直接測ったこと
- **observed**: 可視化上そう見えること
- **interpretive**: 既存物理概念への読み替え
- **analogy**: 音楽・神聖幾何学・生命などへの比喩
- **frontier**: まだ未検証の前線

この repo は「宇宙を作った」「本物の GR / 量子重力を導いた」とは言わない。  
やっていることは、既知物理・toy model・reduced mechanism check を通じて、**関係 + 変化 + エントロピー + 局所性 + 第三** がどこまで一貫した構造を作るかを測ること。

## 現在の大きな鎖

```text
0≠無
→ 変化
→ 因果 = 時間
→ 因果 + 関係 + 第三
→ 空間
→ 最初の差が、釣り合った物質 = 欠陥を強制
→ 一規則が物質の動力学を強制
→ 物質が空間を曲げる
→ 計量が物質の力を媒介する
→ 曲がった空間が物質・光を導く
→ co-evolution が構造を生む
→ 自己無撞着な束縛構造に閉じる
→ 残るは離散の織り目の絶対スケール / 量子重力
```

## Main tracks

### one-flow / relation / causal order

- `one-flow-lab.html` — 0/white → 差 → event → relation → causal order を一本で見るブラウザラボ
- `scripts/one_flow_sweep.py` — one-flow の headless sweep
- `scripts/async_causal_origin.py` — 大域時計なしの局所更新から causal layers を読む
- `relation-lab-v3.html` — relation-only 補助ラボ
- `zero-prism.html` — 0/white から波長モードが分かれる補助ラボ

### space / CDT / third

- `scripts/cdt_2d_toy.py` — 2D CDT toy / causal layering / rewiring null
- `scripts/cdt3d_route_min.py` — 3D CDT route A-C scaffold
- `scripts/alpha_space_map.py` — α third / SOC / width scaling
- `scripts/spectral_coord.py` — 座標 = 低い固有モード / 巻く位相
- `scripts/weyl_dim.py` — Weyl則によるスペクトル次元メーター
- `scripts/remesh_loop.py` — graph↔coordinate 自己無撞着ループ
- `scripts/triangulation_flip.py` — face/third + curvature control で2-多様体を保つ
- `scripts/boundary_scaling.py` — 境界スケーリング / 面積則に近い次元メーター

### arrow / entropy / action frontier

- `scripts/beta_arrow.py` — 低エントロピー境界から時間の矢
- `scripts/entropy_action_frontier.py` — entropic spring と entropy-only crumpling
- `scripts/causal_constraint.py` — entropy-only crumpling と causal/layered restriction の比較

### boundary / flow / vessel / lineage

- `scripts/flow_benard_transport.py` — Benard onset / transport smoke-test / Pe scaling
- `scripts/flow_transport_advdiff.py` — 1D advection-diffusion mechanism check
- `scripts/boundary_throughflow.py` — boundary healing / throughflow death-life
- `scripts/evo_division_inherit.py` — division/tag propagation smoke-test
- `scripts/model_h_min.py` — optional reduced Model-H-like vessel check
- `scripts/gamma_closure.py` — A→M→A closure / vessel toy
- `scripts/delta_inheritance.py` — split / marker inheritance toy
- `scripts/dplus_lineage_selection.py` — repeated lineage survival curve

### matter / defects / gravity

- `scripts/vortex_tdgl.py` — A1/A1b: vortex pair dynamics and random quench coarsening
- `scripts/vortex_metric_force.py` — A3: metric field makes pair energy distance-dependent
- `scripts/defect_metric_curvature.py` — A4: defect bends graph metric
- `scripts/gravity_toys.py` — A6/A10/A11: instability, weak lensing, self-gravity equilibrium

### scale / spiral / key / 3D calibration

- `scripts/efimov_dsi.py` — DSI / Efimov-style geometric ladder
- `scripts/rg_limit_cycle.py` — RG fixed point vs limit cycle / log-periodic fingerprint
- `scripts/gravity_as_key.py` — gravity as key: unscreenable, equivalence principle, universality
- `scripts/curvature_on_faces.py` — curvature lives on faces / third
- `scripts/dimensional_transmutation.py` — dimensional transmutation / generated scale
- `scripts/ball_growth_3d.py` — 3D ball-growth calibration and locality/nonlocality contrast

## Important corrections

- **等価原理**: 一様な gravitational field がゲージ、は standard GR で厳密。
- **scale itself is gauge**: standard GR ではない。conformal / scale-invariant program の frontier。
- **3D ball growth**: hand-built cubic lattice は構成上3D。小さい L の slope 2.5〜2.7 は有限サイズ抑制であり、3D創発の証明ではない。
- **reduced scripts**: 一部は physics verification ではなく regression smoke-test / scaffold。外れうる計算か、答えの符号化かを常に分ける。

## Commands

```bash
# one-flow
python3 scripts/one_flow_sweep.py --mode presets --seeds 20
python3 scripts/async_causal_origin.py --mode scaling --seeds 3

# space / third / CDT
python3 scripts/cdt_2d_toy.py --mode sizes --sources 6
python3 scripts/cdt3d_route_min.py --mode A
python3 scripts/alpha_space_map.py --mode third --seed 0
python3 scripts/spectral_coord.py --mode all
python3 scripts/weyl_dim.py --mode all
python3 scripts/triangulation_flip.py
python3 scripts/boundary_scaling.py

# arrow / entropy
python3 scripts/beta_arrow.py --mode twoarrow
python3 scripts/entropy_action_frontier.py --mode all
python3 scripts/causal_constraint.py

# boundary / flow / lineage
python3 scripts/flow_benard_transport.py --mode all
python3 scripts/flow_transport_advdiff.py
python3 scripts/boundary_throughflow.py --mode all
python3 scripts/gamma_closure.py --mode closure --seeds 3
python3 scripts/delta_inheritance.py --mode split --seeds 3
python3 scripts/dplus_lineage_selection.py --mode final --seeds 12 --generations 20

# matter / gravity
python3 scripts/vortex_tdgl.py --mode all
python3 scripts/vortex_metric_force.py
python3 scripts/defect_metric_curvature.py
python3 scripts/gravity_toys.py --mode all

# scale / spiral / key / 3D calibration
python3 scripts/efimov_dsi.py
python3 scripts/rg_limit_cycle.py
python3 scripts/gravity_as_key.py
python3 scripts/curvature_on_faces.py
python3 scripts/dimensional_transmutation.py
python3 scripts/ball_growth_3d.py
```

## Docs

- `docs/00-philosophy.md` — 0、白、無音、プリズム比喩の整理
- `docs/01-protocol.md` — 最初の 0-looper toy の測定プロトコル
- `docs/02-relation-first-universe-hypothesis.md` — 関係性を軸にした宇宙条件の仮説
- `docs/03-automated-sweep-results.md` — 初回 relation sweep 結果
- `docs/04-expanded-sweep-results.md` — 追加 relation sweep / scaling / grid 結果
- `docs/05-root-principle-check.md` — 根本原理として何が足りないか
- `docs/06-one-flow-sweep-results.md` — 一本化 one-flow sweep 結果
- `docs/07-claude-sync-needed-info.md` — Claude 側と同期するための情報テンプレ
- `docs/08-async-causal-origin-plan.md` — 非同期更新から時間を読む実験
- `docs/09-cdt-2d-toy-results.md` — 2D CDT toy の再測定結果
- `docs/10-cdt-3d-route-a-c.md` — 3D CDT ルート A-C の再現・検証
- `docs/11-alpha-space-map-results.md` — α third / α soc の独立再現
- `docs/12-beta-arrow-results.md` — β arrow の独立再現
- `docs/13-gamma-closure-results.md` — γ closure / 器 の独立再現
- `docs/14-delta-inheritance-results.md` — δ inheritance / 継承マーク の独立再現
- `docs/15-dplus-lineage-selection-results.md` — D+ lineage selection の独立再現
- `docs/16-current-location-synthesis.md` — 現在地までの統合整理と気づき
- `docs/17-audit-response-and-revised-priorities.md` — 監査コメントへの応答と優先順位の更新
- `docs/18-map2-boundary-flow-vessel-frontier.md` — 境界・循環・器の最終前線
- `docs/19-audit-reduced-reproducer-vs-verification.md` — reduced reproducer と物理検証の監査整理
- `docs/20-map3-space-spectral-third-boundary.md` — 空間創発・スペクトル・第三・境界エントロピー橋
- `docs/21-map4-defects-force-entropy-action.md` — 欠陥・力・計量曲率・エントロピー/作用
- `docs/22-map4-full-matter-gravity-unification-sync.md` — 物質・重力・空間と物質の統一
- `docs/23-scale-spiral-key-equivalence-3d-start.md` — 量子/白/螺旋/キー/等価原理/3D開始
- `docs/24-full-journey-current-frontier.md` — 0≠無から最深フロンティアまでの全旅程

## Next frontier

```text
3D causal stack toy
3D vortex line / loop toy
stronger CDT bridge
entanglement / induced gravity branch with real linear algebra dependencies
```

## 現在の合言葉

> 0≠無から、差・因果・第三・空間・物質・曲率・構造までは、かなり一本の鎖になった。  
> でも最後に残るのは、離散の織り目の絶対スケール。  
> そこが量子重力であり、次は同じ要件で 3D が試金石になる。
