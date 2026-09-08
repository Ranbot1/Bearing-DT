# 轴承数字孪生故障诊断论文：写作框架

> **用途**：本目录只总结“这类论文通常怎么写、每一节承担什么论证任务、图表与实验如何组织”。  
> **不包含**：任何特定论文选题、个人研究方案、创新点设计、实验结论预设。

本框架主要从仓库中的 MSSP、Information Fusion、Knowledge-Based Systems、IEEE TASE/TIM、Measurement 等轴承数字孪生研究中抽取共同写作结构。

---

## 一条总原则

轴承数字孪生故障诊断论文通常存在两条需要同时成立的证据链：

### 证据链 A：Twin 本身可信

\[
Physical/Mechanism\ Assumptions
\rightarrow
Dynamic\ Model
\rightarrow
Virtual\ Response
\rightarrow
Twin\ Validation
\]

需要回答：

> 为什么这个数字模型产生的数据值得相信？

### 证据链 B：Twin 对诊断有用

\[
Validated\ Twin
\rightarrow
Virtual/Physical\ Interaction
\rightarrow
Diagnostic\ Model
\rightarrow
Experimental\ Evidence
\]

需要回答：

> 为什么引入这个 Twin 后，诊断问题得到了解决？

一篇完整论文不能只证明其中一条。

### 图表如何嵌入这两条证据链

从高优先级精读样本中可以进一步蒸馏出一个稳定规律：

[
oxed{
正文提出问题
ightarrow
Figure 给直观结构/现象
ightarrow
Table 给精确参数/数值
ightarrow
正文解释其意义
ightarrow
进入下一论证问题
}
]

因此图表不是独立的“结果附件”，而是正文论证的一部分。

- **结构/框架类 Figure**：回答“系统是什么、信息怎么流、故障怎么进入模型”；
- **数据/参数类 Table**：回答“模型和实验到底用了什么”；
- **Twin validation Figure/Table**：回答“虚拟模型为什么可信”；
- **diagnosis Figure/Table**：回答“方法是否有效、哪里有效、为什么有效”。

目前能完整核对正文编号的三篇代表论文中：
- Ma 2023 MSSP：21 Figures + 9 Tables；
- Li 2024 Information Fusion：22 Figures + 8 Tables；
- Zhang 2025 Results in Engineering：23 Figures + 13 Tables。

这些数字只反映**高物理建模密度论文的证据量感**，不是推荐配额。真正应遵循的是：每一个重要 claim 都有职责匹配的图表证据，而不是机械追求图表数量。

---

## 推荐的完整论文结构

1. **Title**
2. **Abstract**
3. **Keywords**
4. **1. Introduction**
5. **2. Related Work / Theoretical Background**
6. **3. Digital Twin Modeling**
7. **4. Digital-Twin-Assisted Diagnostic Method**
8. **5. Experimental Setup**
9. **6. Results and Analysis**
10. **7. Discussion**
11. **8. Conclusions**
12. **Data / Code Availability**
13. **References**

具体可根据期刊篇幅把第 2 节并入 Introduction，或把第 5、6 节合并为 Experiments and Results。

---

## 本目录

- [01 — 全文骨架与章节功能](01_FULL_MANUSCRIPT_STRUCTURE.md)
- [02 — Introduction 与 Related Work 写法](02_INTRODUCTION_AND_RELATED_WORK.md)
- [03 — DT 建模与诊断方法章节写法](03_METHOD_SECTION_STRUCTURE.md)
- [04 — 实验、结果与 Discussion 写法](04_EXPERIMENT_RESULTS_DISCUSSION.md)
- [05 — 图表规划与论文叙事顺序](05_FIGURE_TABLE_AND_NARRATIVE_PLAN.md)
- [06 — 写作检查清单](06_WRITING_CHECKLIST.md)

---

## 推荐实际写作顺序

论文最终呈现顺序和作者真正动笔顺序最好分开。

推荐：

\[
Method
\rightarrow
Experimental\ Setup
\rightarrow
Results
\rightarrow
Discussion
\rightarrow
Introduction
\rightarrow
Related\ Work
\rightarrow
Conclusion
\rightarrow
Abstract
\]

原因是 Introduction 和 Abstract 必须与最终完成的实验事实严格一致，不宜在实验尚未稳定时提前写死。

---

## 最常见的结构性问题

1. **DT 建模写得很长，但没有独立 Twin validation。**
2. **只有分类准确率，没有证明模拟数据为什么可信。**
3. **Twin 与诊断网络之间的接口没有解释清楚。**
4. **Related Work 按年份罗列，没有形成技术分类。**
5. **Introduction 中 method details 过多，导致问题链条不清楚。**
6. **Results 只报最高 accuracy，没有解释 improvement 来自哪里。**
7. **Discussion 与 Results 重复，没有讨论适用边界和失败条件。**
8. **把“virtual model”“simulation”“digital twin”三个概念混用而不定义。**

写作时应始终保持：

\[
Problem
\rightarrow
Why\ DT
\rightarrow
How\ Twin\ is\ built
\rightarrow
Why\ Twin\ is\ credible
\rightarrow
How\ Twin\ enters\ diagnosis
\rightarrow
Does\ it\ work
\]

这一条主线不断裂。
