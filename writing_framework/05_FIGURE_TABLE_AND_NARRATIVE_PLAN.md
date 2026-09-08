# 05 — 图表规划与论文叙事顺序

图表不是“结果装饰”，而应承担论文的主要证据。

轴承 DT 诊断论文可以按下面的图表顺序规划。

---

# Figure 1 — Overall problem / framework

第一张图通常是整篇最重要的图。

应该能看到：

\[
Physical\ Space
\leftrightarrow
Digital\ Space
\rightarrow
Diagnostic\ Space
\]

包括：
- physical data；
- dynamics/twin；
- virtual output；
- virtual-real interaction；
- final diagnosis。

读者只看 Fig. 1 应该理解 70% 的论文逻辑。

---

# Figure 2 — Bearing / test-rig physical model

用途：

> 告诉读者 Twin 到底建了什么。

可以包含：
- bearing geometry；
- coordinate system；
- force；
- support；
- sensor；
- defect location。

若为 multibody/FE，可分：
- physical object；
- digital model。

---

# Figure 3 — Local defect modeling

单独展示：
- inner-race defect；
- outer-race defect；
- rolling-element defect；
- contact deformation。

用途：

\[
Defect\ Geometry
\rightarrow
Dynamic\ Excitation
\]

如果这一步很简单，可以与 Figure 2 合并。

---

# Figure 4 — Twin validation

应当是第一张“证据型”结果图。

可组合：

### (a)
real vs simulated waveform

### (b)
spectrum / envelope

### (c)
time-frequency map

### (d)
distribution / characteristic-frequency error

重点不是多，而是能证明：

\[
Twin\ captures\ intended\ behavior
\]

---

# Figure 5 — Diagnostic network / transfer mechanism

只画真正需要解释的模块。

避免把普通：
Conv → BN → ReLU
全部画得巨大。

重点显示：
- virtual branch；
- physical branch；
- transfer；
- teacher；
- fusion；
- discriminator；
- loss direction。

---

# Figure 6 — Experimental protocol

如果实验设计复杂，单独画：
- source；
- target；
- train；
- validation；
- test；
- operating conditions。

这张图对跨域/跨工况论文尤其有价值。

---

# Figure 7 — Main representation evidence

可以选：
- t-SNE；
- UMAP；
- confusion matrix；
- feature spectrum。

只保留最有解释力的 1–2 种。

---

# Figure 8 — Robustness / sensitivity

例如：
- SNR；
- sample ratio；
- parameter error；
- speed/load change。

---

# Table 1 — Literature comparison

如果 Related Work 中方法差异复杂，可以给：

| Ref. | Physical Model | Calibration | DT Output | Virtual-real Method | Diagnosis Task |

这比纯文字更容易说明研究脉络。

---

# Table 2 — Bearing / Twin parameters

必须完整。

推荐：

| Parameter | Symbol | Value | Unit | Source |

---

# Table 3 — Dataset / test rig

| Condition | Speed | Load | Fault | Severity | Samples |

---

# Table 4 — Baseline comparison

主结果表。

建议同时包含：
- Accuracy；
- Macro-F1；
- mean ± std。

---

# Table 5 — Ablation

单独放，不要和 main comparison 混。

---

# Table 6 — Complexity

若方法较复杂，推荐：
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
System
\rightarrow
Physics
\rightarrow
Twin\ Credibility
\rightarrow
Algorithm
\rightarrow
Protocol
\rightarrow
Performance
}
\]

而不是：

\[
Network
\rightarrow
Accuracy
\rightarrow
最后才解释 Twin
\]

---

# 图注写法

Figure caption 不应只是：

> The proposed framework.

更好的 caption 需要说明：
- 图展示什么；
- 各分支的含义；
- 必要缩写。

读者只看 caption + figure 应该基本能理解图。

---

# Results 中引用图表

不要写：

> Figure 7 shows the results.

而应写：

> Figure 7 shows that the simulated outer-race response preserves the expected fault-related spectral pattern across the tested operating conditions.

也就是：

\[
Figure\ reference + Observation + Meaning
\]

---

# 图表数量控制

一篇普通 10–15 页研究论文，主文可参考：

- Figures: 6–9
- Tables: 4–6

不是硬性规定。

如果一个结果不能服务核心 claim，宁可放 Supplementary Material，也不要让主线失焦。
