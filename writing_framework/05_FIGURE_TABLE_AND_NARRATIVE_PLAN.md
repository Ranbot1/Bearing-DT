# 05 — 图表规划与论文叙事顺序

图表不是“结果装饰”，而应承担论文的主要证据。

轴承 DT 诊断论文可以按下面的图表顺序规划。

---

# 先区分四类图表职责

不要只分“方法图”和“结果图”。从精读论文中更稳定的分类是：

| 类型 | 典型内容 | 核心职责 |
|---|---|---|
| **A. 框架/结构 Figure** | overall framework、bearing/test rig、fault geometry、network/KD/DA flow | 解释“是什么、怎么连” |
| **B. 数据源/配置 Figure & Table** | test rig、sensor、bearing geometry、speed/load、parameter table、network setting | 交代“数据和参数从哪来” |
| **C. Twin 可信性 Figure & Table** | simulated/real waveform、spectrum、TF map、modal comparison、MMD/error | 证明“Twin 为什么可信” |
| **D. 诊断结果 Figure & Table** | comparison table、confusion matrix、t-SNE、ablation、robustness | 证明“诊断是否有效、哪里有效、为何有效” |

其中 B 与 C 都含“数据”，但含义不同：

- **B 是输入/元数据/实验配置**；
- **C 是运行 Twin 后产生的验证证据**。

---

# 从五篇精读论文看到的图表量感

目前可以完整核对正文 Figure/Table 编号的三篇代表作。

对应精读：

- [Ma 2023 MSSP](../deep_readings/05_2023_Ma_MSSP_HighFidelity_EMTL.md)
- [Li 2024 Information Fusion](../deep_readings/03_2024_Li_InformationFusion_Dual_Transfer.md)
- [Zhang 2025 Results in Engineering](../deep_readings/02_2025_Zhang_RIE_Physics_Teacher.md)
- [Fang 2025 MSSP](../deep_readings/04_2025_Fang_MSSP_CrossSpace_DTDA.md)
- [Ding 2026 IEEE TASE](../deep_readings/01_2026_Ding_TASE_Dynamic_Causal_KD.md)

| 论文 | Figures | Tables | 图表组织特点 |
|---|---:|---:|---|
| Ma 2023 MSSP | 21 | 9 | 大量图用于试验台建模、参数辨识、模型更新和 Twin validation，最后才进入诊断 |
| Li 2024 Information Fusion | 22 | 8 | 前半篇结构/信息迁移，后半篇数据分布、敏感性和最终诊断 |
| Zhang 2025 Results in Engineering | 23 | 13 | 表格大量承担参数、工况、baseline、ablation 设置；结果常用 Table + confusion/t-SNE 成对解释 |

Fang 2025 MSSP 与 Ding 2026 TASE 当前公开正文不足以负责任地统计最终图表编号，因此不填猜测数值。

这些数量说明：

> 高水平 DT 论文往往需要多轮“结构说明 → 参数交代 → Twin 证据 → 诊断证据”，因此图表自然较多。

但它们不是推荐配额。图表数量应由 claim 数量和证据需要决定。

---

# Figure 1 — 总体问题 / 总体框架

第一张图通常是整篇最重要的图。

应该能看到：

\[
物理空间
\leftrightarrow
数字空间
\rightarrow
诊断空间
\]

包括：

- physical data；
- dynamics/Twin；
- virtual output；
- virtual-real interaction；
- final diagnosis。

读者只看 Fig. 1 应该理解 70% 的论文逻辑。

---

# Figure 2 — 轴承 / 试验台物理模型

用途：

> 告诉读者 Twin 到底建了什么。

可以包含：

- bearing geometry；
- coordinate system；
- force；
- support；
- sensor；
- defect location。

若为 multibody / FE，可以区分 physical object 与 digital model。

---

# Figure 3 — 局部缺陷建模

单独展示：

- inner-race defect；
- outer-race defect；
- rolling-element defect；
- contact deformation。

用途：

\[
缺陷几何
\rightarrow
动力学激励
\]

如果这一步很简单，可以与 Figure 2 合并。

---

# Figure 4 — Twin 验证

应当是第一张“证据型”结果图。

可组合：

- (a) real vs simulated waveform；
- (b) spectrum / envelope；
- (c) time-frequency map；
- (d) distribution / characteristic-frequency error。

重点不是多，而是能够证明：

\[
Twin\ 捕获了预期的物理行为
\]

---

# Figure 5 — 诊断网络 / 迁移机制

只画真正需要解释的模块。

避免把普通 Conv → BN → ReLU 全部画得巨大。

重点显示：

- virtual branch；
- physical branch；
- transfer；
- Teacher；
- fusion；
- discriminator；
- loss direction。

---

# Figure 6 — 实验协议

如果实验设计复杂，单独画：

- source；
- target；
- train；
- validation；
- test；
- operating conditions。

这张图对跨域/跨工况论文尤其有价值。

---

# Figure 7 — 主要表示证据

可以选：

- t-SNE；
- UMAP；
- confusion matrix；
- feature spectrum。

只保留最有解释力的 1–2 种。

---

# Figure 8 — 稳健性 / 敏感性

例如：

- SNR；
- sample ratio；
- parameter error；
- speed/load change。

---

# Table 1 — 文献比较

如果 Related Work 中方法差异复杂，可以给：

| 文献 | 物理模型 | 校准方式 | DT 输出 | 虚实交互方式 | 诊断任务 |
|---|---|---|---|---|---|

这比纯文字更容易说明研究脉络。

---

# Table 2 — Bearing / Twin 参数

必须完整。

推荐：

| 参数 | 符号 | 数值 | 单位 | 来源 |
|---|---|---:|---|---|

---

# Table 3 — 数据集 / 试验台

| 工况 | 转速 | 载荷 | 故障 | 严重度 | 样本数 |
|---|---|---|---|---|---|

---

# Table 4 — Baseline 主结果比较

建议同时包含：

- Accuracy；
- Macro-F1；
- mean ± std。

---

# Table 5 — 消融实验

单独放，不要和 main comparison 混在一起。

---

# Table 6 — 复杂度

若方法较复杂，推荐报告：

- parameters；
- FLOPs；
- training time；
- inference time；
- Twin simulation cost。

这对 DT 论文尤其重要，因为 high-fidelity simulation 常存在计算成本。

---

# 图表叙事的推荐顺序

论文视觉叙事最好形成：

\[
\boxed{
系统
\rightarrow
物理机制
\rightarrow
Twin\ 可信性
\rightarrow
算法
\rightarrow
实验协议
\rightarrow
性能证据
}
\]

而不是：

\[
网络
\rightarrow
准确率
\rightarrow
最后才解释\ Twin
\]

---

# 图注写法

Figure caption 不应只是：

> 所提出的框架。

更好的 caption 需要说明：

- 图展示什么；
- 各分支的含义；
- 必要缩写。

读者只看 caption + figure 应该基本能理解图。

---

# Results 中如何引用图表

不要只写：

> Figure 7 展示了结果。

而应写成：

> Figure 7 表明，在所测试工况下，模拟外圈响应仍保留预期的故障相关频谱结构。

也就是：

\[
图表引用
+
观察
+
含义
\]

---

# 图表数量控制：不要机械照抄顶刊数量

Ma / Li / Zhang 三篇分别达到约 21–23 张 Figure 和 8–13 张 Table，是因为它们承担了大量：

- physical modeling；
- parameter identification；
- virtual-real validation；
- multi-task diagnosis；
- ablation / robustness。

因此不要把“20+ Figures”当成目标。

更合理的方法是先列核心 claims，再为每个 claim 配证据：

| Claim 类型 | 首选证据 |
|---|---|
| 系统/方法由哪些部分构成 | Framework Figure |
| 参数和工况是什么 | Parameter / Protocol Table |
| 故障动力学是否正确 | Spectrum / envelope / mechanism Figure |
| Twin 与 real 的一致性如何 | Comparison Figure + quantitative Table |
| 整体性能是否提升 | Main Comparison Table |
| 哪些类别得到改善 | Confusion Matrix |
| 表示是否更可分 | t-SNE/UMAP（辅助） |
| 模块是否必要 | Ablation Table |
| 方法是否稳健 | Robustness Table/Curve |

对于一般 10–15 页论文，**6–9 Figures、4–6 Tables 可以作为紧凑稿件的初始规划量感，但不是规范**。若物理建模和 Twin validation 较重，图表自然会增加。

如果一个 Figure/Table 不能回答一个明确 claim，宁可删掉或移到 Supplementary Material。

---

# 正文如何“调用”图表

图表出现前：

> 先告诉读者为什么现在需要这张图/表。

例如：

> 为了评估数字模型是否复现了预期故障动力学，Fig. X 对比了……

图表出现后不要只写：

> Fig. X 展示了结果。

而应按：

\[
引用
+
观察
+
解释
\]

例如：

> Fig. X 表明，模拟响应在不同测试工况下仍保留预期的故障相关频谱成分，而 Table Y 则定量给出了剩余差异。

然后再加一个“所以”：

> 这种一致性为后续将虚拟响应用于诊断实验提供了依据。

这样：

\[
正文
\rightarrow
Figure
\rightarrow
Table
\rightarrow
解释
\rightarrow
下一节
\]

才真正连起来。
