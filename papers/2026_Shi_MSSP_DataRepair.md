# Shi et al. 2026 — A method for discontinuous data repair and precise health monitoring of rolling bearings integrating particle filtering and digital twin

- 期刊：**Mechanical Systems and Signal Processing**, 250, 114136
- DOI：https://doi.org/10.1016/j.ymssp.2026.114136
- 阅读状态：**B**
- 官方代码：**未发现**

## 研究问题

高速/冲击环境下传感器可能发生 intermittent failure，形成 discontinuous measurements。缺失数据会破坏 health feature extraction 和状态判断。

## 方法主线

论文组合：

1. high-fidelity bearing dynamics model：描述 life-cycle evolution；
2. **Particle Filter Model (PFM)**：在观测缺失时，利用 historical state + available observations 预测 defect propagation；
3. **TCW-GAN** digital-twin framework：建立 measured 与 virtual data domain 的动态映射。

目标是：

- 修复 missing / discontinuous state/data；
- 保持 physical continuity；
- 让 DT 在不连续观测条件下继续 health monitoring。

## 对我们的启发

它代表真正的 **online/update-oriented Twin**，与我们“分类 Teacher”主线不同。

但可以用于论文中说明：

- 完整 DT 的难点包括 online state estimation；
- 我们有意把研究范围限制为 diagnosis Teacher，而不是声称构建全功能 online Twin。
