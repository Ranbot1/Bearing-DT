# Ming et al. 2026 — Digital twin-enhanced framework for rolling bearings fault diagnosis under imbalanced and open-set conditions

- 期刊：**Mechanical Systems and Signal Processing**, 257, 114639
- DOI：https://doi.org/10.1016/j.ymssp.2026.114639
- 阅读状态：**B**
- 官方代码：**未发现**

## 研究问题

DT 可以生成 known faults，但存在两个现实问题：

1. idealized simulated signals 与 measured signals 分布不同；
2. DT 不可能事先覆盖所有 atypical / unseen fault types。

所以 closed-set DT augmentation 在 open-world 场景中会失效。

## 方法主线

论文提出 DT-enhanced framework，同时处理：

- class imbalance；
- open-set unknown faults。

公开信息显示，方法使用 bearing dynamic model 生成 known-fault virtual data，再做 virtual-real enhancement，并配合 open-set network 对 unknown class 进行拒识。

## 重要意义

这篇把 DT 诊断问题从：

\[
known\ classes\ only
\]

推进到：

\[
known\ fault\ augmentation + unknown\ rejection
\]

说明“DT 能生成什么”和“DT 不知道什么”本身已经成为研究问题。

## 对我们的启发

Mechanism-only Teacher 也必须避免暗示“physics Teacher 覆盖所有 fault reality”。

我们的 Teacher 更适合作为：

- known-fault evidence prior；
- Student regularizer；

而不是完整世界模型。
