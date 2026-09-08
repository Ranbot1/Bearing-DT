# Shi et al. 2026 — A method for discontinuous data repair and precise health monitoring of rolling bearings integrating particle filtering and digital twin

- Journal: **Mechanical Systems and Signal Processing**, 250, 114136
- DOI: https://doi.org/10.1016/j.ymssp.2026.114136
- Reading status: **B**
- Official code: **未发现**

## 问题

高速/冲击环境下传感器可能 intermittent failure，形成 discontinuous measurements。缺数据会破坏 health feature extraction 和状态判断。

## 方法主线

论文组合：

1. high-fidelity bearing dynamics model，描述 life-cycle evolution；
2. **Particle Filter Model (PFM)**：在观测缺失时利用 historical state + available observations 预测 defect propagation；
3. **TCW-GAN** digital-twin framework：建立 measured 与 virtual data domain 的动态映射。

目标是：
- repair missing/discontinuous state/data；
- 保持 physical continuity；
- 让 DT 在不连续观测条件下继续 health monitoring。

## 对我们的启发

它代表真正的 **online/update-oriented twin**，与我们“分类 teacher”主线不同。

但可以用于论文里说明：
- 完整 DT 的难点包括 online state estimation；
- 我们有意把研究范围限制为 diagnosis teacher，而不是声称构建全功能 online twin。
