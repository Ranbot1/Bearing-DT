# 复现状态

当前状态：**PHYSICS_REPRODUCED — R1 已通过；R2 机制级关口已通过；Teacher 数据集 pilot 已通过**

最后更新：2026-09-09

## 已完成

- 仓库复现契约与约束；
- 分阶段验收标准；
- 证据台账；
- 6203 geometry config；
- PU 工况 config；
- 论文训练超参数；
- 4-DOF 二阶 ODE 实现；
- Hertz nonlinear contact；
- localized inner / outer defect hook；
- characteristic-frequency functions；
- simulator validation plotting script；
- 已确认的网络宏观结构已经编码：
  - 4 Conv；
  - BN；
  - CBAM；
  - 128-d feature；
  - 128→64→1 discriminator；
- MK-MMD loss primitive；
- smoke / unit test 源码。

## 尚未验收

- trailing-edge collision term 的论文精确数值参数；
- 与真实物理试验台对应的 high-fidelity 幅值/共振标定；
- Fig. 7/9 的 exact conv channels / kernels；
- exact preprocessing / input representation；
- Paderborn data loader + manifest；
- Teacher training；
- 完整 MADA / global + subdomain training loop；
- HUST ball-fault simulator；
- paper-level accuracy reproduction。

## 当前关口

R1 机制合理性已经通过：

- inner BPFI：PASS；
- speed scaling：PASS；
- 修正承载区角度后的 outer BPFO：PASS。

R2 机制级验收已经通过：

- Fig. 5 BPFI 频率证据：PASS；
- dual-impulse DITS：PASS；
- exit > entry 高频冲击：PASS；
- no-exit-impact negative control：PASS。

这仍然是**机制级重建**，不是已经针对真实物理试验台完成标定的 high-fidelity twin。

固定审计快照已经保存在：
`artifacts/audit_snapshots/20260909_6203_r1r2/`

其中包含生成的 Twin 数据、故障频带频谱、指标以及代码生成的 SVG 图。

该关口使用的生成证据也保存在同一目录中，因此可以独立检查信号值、频谱、图、config 和文件哈希。

Teacher 数据集构造 pilot 已通过：

- 18 个 raw windows，形状 18×2048；
- normal / inner / outer 类别平衡；
- train / val / test 数量平衡；
- simulation-run-isolated splits；
- train / val / test raw-value audit CSV 已留存；
- NPZ SHA-256 已留存；
- 代码生成的 Teacher-window SVG 已留存。

**R3 Teacher pretraining 目前仅因 paper-faithful 输入/预处理信息存在歧义而保持 BLOCKED。**

详见 [PREPROCESSING_AUDIT.md](PREPROCESSING_AUDIT.md)。

## 下一编码里程碑

1. 尽可能从更强证据中恢复 Fig. 7/9 的 input tensor 与 Conv 细节；
2. 如果仍无法恢复，则建立名称明确的 fallback 路线，并标记为非 paper-confirmed；
3. 之后再运行 Teacher pretraining，并报告 3-seed 的 simulated-domain held-out performance。
