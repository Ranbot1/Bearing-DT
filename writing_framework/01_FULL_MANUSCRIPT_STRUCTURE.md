# 01 — 全文骨架与章节功能

本文件给出轴承数字孪生故障诊断研究论文的**标准章节骨架**。章节编号可以调整，但每一个“论证功能”最好保留。

---

# Title

标题通常包含三个元素：

\[
Application + Digital\ Twin\ Role + Core\ Task/Method
\]

常见结构：

- Digital twin-assisted ... for rolling bearing fault diagnosis
- Digital twin-enabled ... for cross-space bearing diagnosis
- ... digital twin for bearing fault diagnosis under ...
- Physics-/mechanism-guided ... with digital twin ...

标题应避免同时塞入过多模块名。

---

# Abstract

建议按 **6 个信息单元**写。

### A1 — 背景问题

1–2 句说明现实诊断困难。

回答：

> 为什么这个问题值得解决？

### A2 — 现有方法不足

1 句指出现有 data-driven / simulation-based / transfer method 的关键限制。

回答：

> 为什么已有方法还不够？

### A3 — 本文总体方案

1–2 句给出 digital twin 与 diagnosis 的总体关系。

只讲主链，不进入小模块细节。

### A4 — DT 核心建模

1 句交代 Twin 基于什么物理/动力学建模，以及 virtual data/state 怎么得到。

### A5 — 关键实验结果

给最关键的定量结果：

- 数据集/试验台数量；
- 主要诊断指标；
- 相对强 baseline 的提升；
- 必要时给 Twin validation 指标。

### A6 — 结论意义

最后 1 句回答：

> 结果说明这种 DT 辅助方式解决了什么问题？

---

# 1. Introduction

Introduction 的任务不是介绍全部方法，而是建立：

\[
Real\ Problem
\rightarrow
Existing\ Limitation
\rightarrow
Why\ DT
\rightarrow
Unresolved\ Gap
\rightarrow
Paper\ Objective
\]

推荐五段式，详见：
[02_INTRODUCTION_AND_RELATED_WORK.md](02_INTRODUCTION_AND_RELATED_WORK.md)

最后通常列出 2–4 条 contributions，然后给论文组织结构。

---

# 2. Related Work / Background

不要按：

> A 做了什么，B 做了什么，C 又做了什么。

而应形成分类。

推荐三条主线：

## 2.1 Bearing fault dynamics / physical modeling

介绍故障动力学、接触模型、缺陷模型、振动响应建模。

## 2.2 Digital twin for bearing monitoring and diagnosis

介绍：
- high-fidelity twin；
- dynamic updating；
- virtual-real fusion；
- simulation data generation。

## 2.3 Digital-to-physical diagnostic transfer

介绍：
- transfer learning；
- domain adaptation；
- knowledge distillation；
- physics-informed / causal guided diagnosis。

最后一段统一总结：

> 现有三条路线分别解决了什么，但仍留下什么研究缺口。

---

# 3. Digital Twin Modeling

这一节回答：

\[
\boxed{\text{Twin 是怎么建立出来的？}}
\]

推荐：

## 3.1 Physical object and modeling assumptions

说明：
- 被建模对象；
- 坐标系；
- 自由度；
- 基本假设；
- 输入、状态、输出。

## 3.2 Bearing dynamic model

写：
- 运动方程；
- 接触力；
- Hertz contact；
- stiffness / damping；
- cage/roller kinematics；
- load。

## 3.3 Fault modeling

分别说明：
- inner-race fault；
- outer-race fault；
- rolling-element fault；
- 其他结构故障（若有）。

重点回答：

> 故障如何进入动力学方程？

## 3.4 Digital-twin parameterization / updating

参数来自：
- design specification；
- measurement；
- parameter identification；
- inverse learning；
- FE updating；
- optimization。

要明确区分：
- known parameters；
- identified parameters；
- tuned parameters。

## 3.5 Virtual signal/state generation

说明：
- solver；
- sampling；
- simulation duration；
- virtual conditions；
- 输出变量。

## 3.6 Twin validation

这是独立小节，不建议省略。

详见：
[03_METHOD_SECTION_STRUCTURE.md](03_METHOD_SECTION_STRUCTURE.md)

---

# 4. Digital-Twin-Assisted Diagnostic Method

这一节回答：

\[
\boxed{\text{Twin 怎么真正进入诊断器？}}
\]

建议先放一张总体框架图。

## 4.1 Overall architecture

先画清楚：

\[
Digital\ Space
\leftrightarrow
Physical\ Space
\rightarrow
Diagnosis
\]

不要上来直接讲网络层数。

## 4.2 Data / representation construction

说明：
- virtual samples；
- measured samples；
- preprocessing；
- segmentation；
- normalization；
- input representation。

## 4.3 Diagnostic backbone

只写必要结构。

如果网络本身不是核心，避免花过多篇幅逐层介绍 CNN。

## 4.4 Virtual–physical interaction

这一部分通常是全文方法核心。

可能是：
- data augmentation；
- information fusion；
- transfer learning；
- domain adaptation；
- teacher–student；
- parameter updating；
- virtual-real mapping。

## 4.5 Objective function

统一给总损失：

\[
\mathcal L =
\sum_k \lambda_k \mathcal L_k
\]

随后逐项解释：
- 每一项约束什么；
- 哪些网络参数被更新；
- 优化方向。

## 4.6 Training / inference procedure

最好给：
- Algorithm 1；
- pseudo-code；
- flow chart。

区分训练阶段与部署/测试阶段。

---

# 5. Experimental Setup

这一节只写**实验事实和协议**，不要提前解释结果。

## 5.1 Dataset / test rig

记录：
- bearing；
- sensor；
- sampling rate；
- speed；
- load；
- fault type；
- fault size/severity；
- train/val/test unit。

## 5.2 DT simulation settings

单独给 parameter table。

## 5.3 Data preprocessing and split

必须交代：
- window length；
- overlap；
- normalization；
- split unit；
- sample counts。

## 5.4 Baselines

按类别组织：
- purely data-driven；
- transfer/domain adaptation；
- physics-informed；
- DT-based。

## 5.5 Implementation details

包括：
- backbone；
- optimizer；
- learning rate；
- batch size；
- epochs；
- hardware；
- random seeds；
- repeats。

## 5.6 Evaluation metrics

根据任务列：
- Accuracy；
- Macro-F1；
- Precision / Recall；
- AUROC；
- unknown detection metrics；
- RUL metrics。

---

# 6. Results and Analysis

推荐结果顺序：

## 6.1 Twin fidelity / physical validity

先回答：

> Twin 本身靠谱吗？

## 6.2 Overall diagnostic comparison

再回答：

> 完整方法有没有用？

## 6.3 Ablation

回答：

> 到底是哪部分产生作用？

## 6.4 Robustness / sensitivity

回答：
- 噪声变化？
- 工况变化？
- 参数变化？
- 样本减少？

## 6.5 Feature / representation analysis

可用：
- t-SNE/UMAP；
- confusion matrix；
- spectrum/envelope；
- attention/feature visualization。

注意：可视化只能辅助解释，不能替代定量证据。

---

# 7. Discussion

Discussion 不要复制 Results。

它应该回答四个问题：

1. **Why did it work?**
2. **When does it work?**
3. **When may it fail?**
4. **What does the result imply for DT-based diagnosis?**

可以讨论：
- Twin fidelity 与 diagnosis 的关系；
- simulation-to-real gap；
- model complexity；
- parameter dependence；
- online feasibility；
- computational cost；
- generalization limits。

---

# 8. Conclusions

推荐四段信息：

1. 再次简述研究问题；
2. 简述方法主链；
3. 总结最关键实验事实；
4. 给出局限与未来工作。

不要在 Conclusion 引入正文没有验证的新理论。

---

# 全文章节与图表职责的联动

论文结构不应只按章节排列，还要让每一节承担对应的视觉/定量证据。

| 正文阶段 | 正文回答的问题 | Figure 的主要职责 | Table 的主要职责 |
|---|---|---|---|
| Introduction / Related Work | 为什么需要这项研究？现有路线是什么？ | 必要时用概念图/技术路线图 | 文献比较表，可选 |
| DT Modeling | Twin 建了什么？故障如何进入模型？ | 物理对象、坐标、接触、fault geometry、总体 DT 结构 | bearing / Twin 参数及来源 |
| Twin Validation | Twin 是否可信？ | waveform、spectrum、envelope、time-frequency、sim-real distribution | characteristic-frequency error、MMD、modal/statistical error |
| Diagnostic Method | Twin 如何进入诊断器？ | network / transfer / KD / DA 流程 | loss、network setting，必要时 |
| Experimental Setup | 数据从哪来？协议是什么？ | test rig、sensor location、复杂 split protocol | speed/load/fault/sample counts、hyperparameters |
| Main Results | 方法有没有用？ | confusion matrix / feature visualization | Accuracy / F1 / mean±std 主比较 |
| Ablation / Robustness | 为什么有效？是否稳定？ | sensitivity curves、representation change | ablation / robustness 定量结果 |
| Discussion | 结果意味着什么？适用边界在哪？ | 通常不新增主证据图 | 通常不新增主结果表 |

由此形成一种自然的正文节奏：

[
System
ightarrow
Physics
ightarrow
Twin Credibility
ightarrow
Diagnostic Interface
ightarrow
Protocol
ightarrow
Performance
ightarrow
Mechanism/Robustness
]

不要出现“前半篇只讲网络、最后才补 Twin 验证”的倒序叙事。

---

# Data / Code Availability

DT 论文尤其建议明确：

- raw measured data 是否公开；
- virtual data 是否可生成；
- simulator code 是否公开；
- trained model 是否公开；
- parameter table 是否完整。

这直接影响论文的可复现性。
