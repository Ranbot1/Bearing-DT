# Peng et al. 2022 — Digital Twin for rolling bearings: A review of current simulation and PHM techniques

- 期刊：**Measurement**, 201, 111728
- DOI：https://doi.org/10.1016/j.measurement.2022.111728
- 类型：综述
- 阅读状态：**B**
- 官方代码：**未发现 / 不适用（综述）**

## 论文在 DT 文献中的位置

这是较早系统讨论“rolling bearing digital twin”的综述之一。作者把轴承 DT 的基础拆成三大技术块：

1. **检测/感知（Detection / sensing）**：物理轴承状态如何被观测；
2. **建模/仿真（Modeling / simulation）**：虚拟实体如何构造；
3. **PHM**：虚拟与实测信息如何用于诊断、预测和寿命管理。

## 对建模的核心启示

真正的轴承 DT 不是单一深度网络，而是至少包含：

\[
Physical\ bearing \leftrightarrow sensing \leftrightarrow virtual\ model \rightarrow PHM
\]

对我们最重要的是，它明确指出轴承动力学建模、状态检测和 PHM 可以分层讨论。因此我们可以把 **mechanism simulator** 与后续 Student diagnosis 分开设计，而不是强迫一个网络同时完成所有任务。

## 对后续研究的价值

- 用它做术语和技术历史入口；
- 用它追踪早期 bearing dynamics / defect modeling 文献；
- 论文写 Related Work 时，可用于解释“digital model / digital shadow / digital twin”的边界。

## 局限

综述早于 2025–2026 年大量 sim-to-real、open-set、physics-teacher 工作，不足以覆盖当前的 Teacher / causal prior / open-set DT 路线。
