# Dual-Impulse R2 审计 — 2026-09-09

该快照用于在构造 Teacher 数据集之前，对 localized-spall 的 dual-impulse 机制进行验收。

## 文献目标

2025 复现论文明确采用 Luo et al. 的 localized-spall 动力学路线，并描述了 dual-impulse 行为。其参考机制区分两类事件：

1. rolling element 进入 spall → 较低频的 step response；
2. rolling element 离开时撞击 trailing edge → 较高频的 transient impulse。

当前可访问文献支持平滑的 spall-displacement profile，以及显式的 trailing-edge collision term。但 2025 论文中使用的精确碰撞力常数无法从当前可访问正文中恢复。

因此：

- `half_cosine` spall profile 属于 REFERENCED reconstruction；
- `exit_impact_force_n=500 N` 与 `exit_impact_duration_s=80 us` 属于 INFERRED；
- 不宣称这两个数值就是论文作者使用的原始参数。

## 定量验收

| 指标 | 重建模型 | 去除 exit-impact 的负对照 |
|---|---:|---:|
| 理论 DITS | 1.078014 ms | 1.078014 ms |
| 检测 DITS 中位数 | 1.093750 ms | 1.046875 ms |
| DITS 误差 | **1.460%** | 2.889% |
| exit/entry 高频峰值比中位数 | **1.785** | 0.870 |
| exit/entry 高频 RMS 比中位数 | **1.310** | 0.876 |
| exit 峰值 > entry 的比例 | 0.571 | 0.286 |
| 理论 BPFI | 123.6842 Hz | 123.6842 Hz |
| envelope BPFI 峰值 | **123.3852 Hz** | 116.3070 Hz |
| BPFI 误差 | **0.242%** | 5.965% |

验收标准：

- DITS error <= 5%；
- median exit/entry HF peak >= 1.2；
- median exit/entry HF RMS >= 1.1；
- BPFI error <= 2%；
- 禁用 trailing-edge impact 后，exit/entry HF ratio 必须下降。

**结论：PASS（R2 机制级 dual-impulse 关口）。**

## 留存证据

- `dual_impulse_metrics.json`：汇总指标与负对照结果。
- `event_metrics.csv`：用于验收的 7 次完整 defect passage。
- `strongest_passage.csv`：最强 passage 周围的 raw / high-pass / low-pass 数值。
- `dual_impulse_compact.svg`：由代码生成的该 passage 可视化。

## 结果解释

之前的 rectangular-clearance 模型能够复现 entry/exit 的时间间隔，但无法复现 dual-impulse 的形态差异：exit 高频冲击并不比 entry 更强。

当前重建模型通过把平滑 spall displacement 与瞬态 trailing-edge collision 分开建模，恢复了这一机制差异。

这属于**机制级重建**，并不代表已经完成 Paderborn 真实物理试验台的 high-fidelity 标定。
