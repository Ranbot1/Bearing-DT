# 轴承数字孪生建模路线矩阵

| 路线 | 典型论文 | 物理层 | 校准层 | Twin 输出 | 下游用途 | 建模难度 |
|---|---|---|---|---|---|---|
| 多学科/高保真试验台 DT | Ma 2023 MSSP | FE + bearing/contact + support/transmission | modal test + parameter ID + FE updating | 模拟振动 | few-shot EMTL | ★★★★★ |
| 缺陷演化 DT | Shi 2023 MSSP; Li 2023 TIM | defect growth/evolution dynamics | sensor-driven update / calibration | defect size/state | health mapping | ★★★★☆ |
| 虚实融合寿命 DT | Zhao 2023 MSSP | life-cycle simulation | CycleGAN + Wasserstein | real-like degradation samples | RUL | ★★★★☆ |
| inverse-PINN calibrated DT | Qin 2024 KBS | bearing dynamic model | inverse PINN + spectrum discrepancy | calibrated fault samples | imbalance diagnosis | ★★★★☆ |
| Multibody Sim2Real DT | Fang 2025 MSSP | CRB + support housing，Augmented Lagrange + Hertz | same-condition virtual/physical validation | pedestal acceleration | domain adaptation | ★★★★★ |
| Physics Teacher | Cui 2025 RIE | 4-DOF + time-varying contact stiffness + Hertz | 不追求波形完全一致 | mechanism-rich simulated vibration / Teacher feature | KD + DA | ★★★☆☆ |
| Dynamic + causal Teacher | Ding 2026 TASE | bearing dynamics prior | causal prior 抑制 confounding | Teacher representation | interpretable KD | ★★★★☆ |
| DT-guided denoising | Qiao 2026 MSSP | physical-parameter bearing DT | physical-virtual fusion | clean/high-fidelity labeled signal | early fault detection | ★★★★☆ |
| DT + open-set | Ming 2026 MSSP | 5-DOF dynamic model（论文路线） | virtual-real enhancement | augmented known-fault data | unknown rejection | ★★★★☆ |
| PF online state repair DT | Shi 2026 MSSP | life-cycle high-fidelity dynamics | particle filter + TCW-GAN | repaired state/data | health monitoring | ★★★★★ |

## 对我们最重要的分层

### C — Mechanism-only

仅允许 Fault + Geometry + necessary RPM/Load。目标不是拟合完整真实波形，而是生成可靠的 fault evidence。

### B — Full-physics-like

在 C 基础上加入 housing / support / transfer path / sensor response，研究更多 machine-specific information 是否提高或损害 transferability。

### A — Signal-faithful

进一步用真实数据校准参数，使 PSD / envelope / statistical distributions 更接近实测。

这里要警惕：**越接近真实信号，也越可能把 nuisance cue 一起编码进去。**

建议开发顺序：**C → B → A**，而不是一开始追求高保真。
