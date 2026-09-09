# 02 — 引言与相关工作写法

---

# 一、引言（Introduction）：五段式问题链

轴承 DT 论文的 Introduction 最重要的是**逐层收窄问题**，而不是堆叠 digital twin 的定义。

---

## 第 1 段：现实诊断需求

功能：

> 建立任务的重要性。

常见内容：

- rolling bearing 是关键旋转部件；
- failure 会导致 downtime / safety / maintenance cost；
- vibration-based intelligent diagnosis 具有实际价值。

这一段不要讲具体网络。

段末把问题落到：

\[
可靠的轴承故障诊断
\]

---

## 第 2 段：纯数据驱动诊断的限制

功能：

> 解释为什么已有深度学习还不够。

通常讨论：

- labeled fault data scarcity；
- imbalanced samples；
- variable operating conditions；
- sim-real / domain shift；
- unseen faults；
- weak/noisy early faults；
- limited interpretability。

不要把所有问题都列出来，只保留与全文后续一致的那一类。

逻辑：

\[
深度学习取得成功
\rightarrow
数据与泛化限制
\]

---

## 第 3 段：为什么数字孪生有潜力

功能：

> 从前一段的问题自然引出 DT。

介绍 Twin 能提供：

- physics-based virtual data；
- controllable fault states；
- virtual experiments；
- continuous state mapping；
- physical prior。

这一段要避免把 DT 写成万能技术。

需要立即指出：

\[
Digital\ model \neq Real\ machine
\]

因此还存在：

- modeling error；
- parameter uncertainty；
- distribution discrepancy；
- computational cost。

这样才能自然进入下一段。

---

## 第 4 段：现有 DT 诊断工作的不足

功能：

> 真正建立论文的研究缺口（research gap）。

这是 Introduction 最重要的一段。

写法应是“归类后评价”，例如：

### 路线 A — 高保真数字孪生

优点：

- physical consistency 强。

可能的不足：

- parameter identification 困难；
- test / FE calibration 成本高；
- computational burden 大。

### 路线 B — 虚实数据融合

优点：

- 减少 distribution discrepancy。

可能的不足：

- 对 real data 有依赖；
- fusion quality 难以验证。

### 路线 C — DT + 迁移/诊断网络

优点：

- 提高 virtual knowledge utilization。

可能的不足：

- downstream method 提高了 accuracy，但 Twin 的独立贡献没有被充分隔离；
- digital-space validity 与 diagnostic utility 经常混在一起验证。

这一段末尾必须收束成**一个明确的 research gap**。

---

## 第 5 段：本文做什么

功能：

> 给出论文目标和贡献。

### 先给一句总体方案

只说：

\[
问题
\rightarrow
所提框架
\rightarrow
预期作用
\]

不要在这里进入公式细节。

### 再列贡献（Contributions）

建议 2–4 条。

高质量 contribution 的组织原则：

1. **建模贡献（Modeling contribution）**
2. **方法贡献（Methodological contribution）**
3. **实验/验证贡献（Experimental / validation contribution）**

不要写：

- “大量实验表明方法有效”作为唯一贡献；
- “首次使用某某 CNN”这类弱创新；
- 与摘要结果矛盾的夸张表述。

### 最后一段

介绍 Section 2 到 Conclusion 的论文组织结构。

---

# 二、相关工作（Related Work）：不要按年份流水账

推荐按照**研究问题**分类，而不是作者年代分类。

---

## 2.1 轴承动力学建模与故障仿真

这一节回答：

> 轴承故障如何被物理建模？

可以组织为：

\[
运动学
\rightarrow
接触动力学
\rightarrow
局部缺陷
\rightarrow
振动响应
\]

常见内容：

- fault characteristic frequencies；
- Hertz contact；
- time-varying stiffness；
- multi-DOF bearing model；
- multibody dynamics；
- FE / housing / support model；
- defect evolution。

这一节结尾应指出：

> physical simulation 为 DT 提供基础，但 simulation 本身并不自动等于可信 Twin。

---

## 2.2 滚动轴承数字孪生建模

按照 Twin 深度分类：

### 类型 1 — 机制/响应模型（Mechanism/response model）

输出：

- virtual vibration；
- fault response。

### 类型 2 — 校准/高保真 Twin（Calibrated/high-fidelity twin）

增加：

- parameter identification；
- FE/modal updating；
- measured-data calibration。

### 类型 3 — 动态/状态 Twin（Dynamic/state twin）

增加：

- online updating；
- defect evolution；
- health state / RUL。

这种分类比“2022、2023、2024 分别有人做了什么”更清楚。

---

## 2.3 数字孪生辅助故障诊断

可按照 Twin 的作用分类：

### 数据生成

\[
DT\rightarrow Virtual\ Samples
\]

### 虚实融合

\[
Virtual + Real \rightarrow Fused\ Data
\]

### 迁移/域适配

\[
Digital\ Domain \rightarrow Physical\ Domain
\]

### Teacher / 先验引导

\[
Physics\ Prior \rightarrow Diagnostic\ Model
\]

### 在线监测/状态修复

\[
Twin\ State \leftrightarrow Real\ Observation
\]

这样可以把不同论文放进同一张逻辑地图。

---

# 三、Related Work 的段落模板

每个技术类别可以采用：

### 句 1 — 定义这一类在解决什么

### 句 2–4 — 选 2–4 篇代表工作

只说：

- 核心方法；
- 解决的具体问题。

### 句 5 — 总结这一类的优势

### 句 6 — 指出仍存在的共同局限

最后转入下一类。

---

# 四、Introduction 与 Related Work 的分工

不要重复。

### Introduction

回答：

> 为什么问题重要？为什么当前还没有解决？

### Related Work

回答：

> 学术界已经形成哪些技术路线？它们之间是什么关系？

如果期刊篇幅有限，可以把 Related Work 压缩成 Introduction 中 2–3 个文献段落，但逻辑分类仍应保留。

---

# 五、文献引用密度

建议：

- Introduction 前两段：引用 broad / review / benchmark；
- DT 引入段：引用 DT review + representative works；
- gap 段：引用最接近本文问题的 3–6 篇；
- Related Work：重点覆盖 representative papers，不追求机械式“引用数量”。

一段不要连续堆十几个 citation 而没有作者自己的归纳句。

---

# 六、常见失败写法

## 失败 1

用半页篇幅介绍“Digital twin 有很多优势……”的概念史。

问题：没有与 bearing diagnosis gap 建立联系。

## 失败 2

“CNN → Transformer → GAN → DT”按技术年份流水账。

问题：没有形成研究问题分类。

## 失败 3

Introduction 最后一段突然出现复杂 loss function。

问题：方法细节进入过早。

## 失败 4

Related Work 只夸已有工作，没有指出局限。

问题：无法自然导出论文必要性。

最好的目标是让读者在读到 Introduction 最后一段前，已经自然形成：

> “这个问题确实还需要一篇这样的论文。”
