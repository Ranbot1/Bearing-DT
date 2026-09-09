# Mechanism-only Teacher：与现有 DT 论文的差异

## 已经被做过的部分

“动力学模型生成故障信号 → 预训练 Teacher → 通过知识蒸馏辅助真实诊断 Student”已经存在。

最直接的竞争工作：

- Cui et al., 2025, Results in Engineering；
- Ding et al., 2026, IEEE TASE。

因此不能把 **physics teacher / simulated-data teacher** 本身当作核心创新。

## 仍值得研究的问题

我们希望约束 Teacher 的信息边界：

\[
T = T(Y, C)
\]

其中：

- \(Y\)：fault type / severity；
- \(C\)：necessary causal context，例如 geometry、RPM、必要 load。

明确不希望 Teacher 获得：

- bearing ID；
- machine ID；
- dataset ID；
- sensor ID；
- arbitrary transfer path；
- recording/background fingerprint。

目标不是声称 Teacher “天然只有故障信息”，而是**通过受控 simulator 层级和干预实验，验证 Teacher 到底编码了什么**。

## 可证伪假设

随着 Twin fidelity 增加：

- in-domain / random-window accuracy 可能上升；
- unseen-bearing / cross-machine generalization 不一定上升；
- machine/path calibration 可能把 nuisance cues 一起传给 Student。

论文问题可以表述为：

> 提高数字孪生的信号保真度，究竟是在改善诊断知识迁移，还是只是在增强机器特定捷径信息的迁移？
