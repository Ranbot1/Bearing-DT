# 生成产物留存策略

复现结论必须能够通过仓库中的实际产物进行审计，不能只依赖 Markdown 摘要。

对于每一个已经通过的物理或信号处理里程碑，**生成脚本**必须产出：

- 精确的 config 快照和运行时覆盖参数；
- 完整生成的 Twin 数组（NPZ）；
- 便于文本直接检查的紧凑信号导出；
- 支撑所报告数值的频谱/特征表；
- 由信号处理代码生成的 SVG 和 PNG 图；
- 各类别指标；
- provenance manifest 与 SHA-256。

对于**固定 Git 快照**，需要保留足够的文本和可视化证据，保证能够直接检查，同时控制仓库历史体积。完整二进制 NPZ 可以保持“可再生成”而不在每次提交中版本化，但必须记录生成端对应的哈希。

当前固定快照：

- [20260909_6203_r1r2](audit_snapshots/20260909_6203_r1r2/README.md)
- [20260909_dual_impulse_r2](audit_snapshots/20260909_dual_impulse_r2/README.md)

对应生成脚本：

- [scripts/06_build_audit_snapshot.py](../scripts/06_build_audit_snapshot.py)
- [scripts/07_validate_dual_impulse.py](../scripts/07_validate_dual_impulse.py)
