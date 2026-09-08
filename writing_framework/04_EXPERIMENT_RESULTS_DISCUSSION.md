# 04 — 实验、结果与 Discussion 写法

DT 诊断论文的实验最好按**论证问题**排，而不是按“我做了哪些图”排。

推荐证据顺序：

\[
Twin\ Credibility
\rightarrow
Diagnostic\ Effectiveness
\rightarrow
Component\ Necessity
\rightarrow
Robustness
\rightarrow
Boundary
\]

---

# 1. Experimental Setup

这一部分只描述 protocol，不解释优劣。

---

## 1.1 Dataset / test rig description

推荐表格：

| Dataset/Rig | Bearing | Faults | Speed | Load | Sampling | Sensor |
|---|---|---|---|---|---|---|

正文只解释：
- 为什么选这些工况；
- 哪些是 source / target；
- 哪些用于 Twin calibration；
- 哪些完全保留给 test。

---

## 1.2 Data partition

必须明确 split unit：

\[
sample/window
\]

还是：

\[
record
,\quad
bearing
,\quad
machine
\]

报告：
- number of physical recordings；
- number of generated windows；
- train / validation / test counts；
- overlap。

特别是 vibration segmentation，不能只写“80/20 random split”。

---

## 1.3 Simulation parameter setup

单独给：

| Parameter | Value/Range | Source |
|---|---|---|

并区分：
- fixed；
- randomized；
- optimized。

---

## 1.4 Baselines

不要把所有 baseline 混成一列。

建议分类：

### Data-driven

CNN / ResNet / Transformer 等。

### Transfer / adaptation

DANN / MMD / CDAN 等。

### Physics-informed

physics regularization / PINN / feature prior。

### Digital-twin based

与本文属于同类型的 DT 方法。

这样 results table 的意义更清晰。

---

## 1.5 Implementation details

需要报告：
- framework；
- GPU；
- optimizer；
- learning rate；
- batch size；
- epochs；
- early stopping；
- seeds；
- repeated runs。

结果最好给：

\[
mean\pm std
\]

而不是单次最佳结果。

---

# 2. Results：推荐五层证据

---

## R1. Twin validation

这一部分应当**先于最终分类准确率**。

### Mechanism evidence

展示：
- theoretical characteristic frequency；
- virtual spectrum；
- measured spectrum。

### Signal evidence

若有 high-fidelity claim，展示：
- PSD；
- envelope；
- time-frequency；
- statistic/distribution metric。

结果文字回答：

> 哪些物理特征被正确复现？哪些仍存在差异？

不要写成“the curves are highly similar”后就结束。

---

## R2. Main diagnostic results

这是主 comparison table。

推荐：

| Method | Task 1 | Task 2 | Task 3 | Avg. | Macro-F1 |
|---|---:|---:|---:|---:|---:|

主文只强调：
- overall ranking；
- difficult tasks；
- statistical consistency。

不要逐单元格朗读表格。

---

## R3. Ablation study

Ablation 的目标是：

\[
\boxed{\text{证明模块必要性}}
\]

不是简单删三个 module 然后再报 accuracy。

推荐：

| Variant | Twin | Transfer | Physics/KD | Accuracy | F1 |
|---|---|---|---|---:|---:|

同时解释：

> 去掉该模块后，改变的是哪条机制？

例如：
- gap increases；
- feature separation worsens；
- noise robustness decreases。

---

## R4. Robustness / sensitivity

DT 论文尤其适合做：

### Noise

\[
SNR=...
\]

### Speed/load variation

不同 operating condition。

### Sample scarcity

真实 labeled data percentage：

\[
1\%,5\%,10\%,...
\]

### Parameter uncertainty

Twin parameters 扰动：

\[
\theta(1\pm\epsilon)
\]

### Hyperparameter sensitivity

仅分析真正重要的 \(\lambda\)，不要把所有学习率都画一遍。

---

## R5. Representation / physical interpretation

可用：

- confusion matrix；
- t-SNE / UMAP；
- envelope spectra；
- learned feature spectrum；
- attention weights；
- domain distance。

但必须把图与问题绑定：

> 这张图到底验证哪个 claim？

如果图不能回答 claim，就不要放。

---

# 3. Results 的标准段落结构

每个实验小节推荐四句逻辑：

### Sentence 1 — 问题

“该实验用于验证……”

### Sentence 2 — 设置

“在……条件下比较……”

### Sentence 3 — 主要结果

给 1–3 个最重要数字。

### Sentence 4 — 解释

说明：

> 结果支持哪个机制判断？

不要把解释全部推迟到 Discussion。

---

# 4. Discussion

Discussion 与 Results 的区别：

### Results

\[
What\ happened?
\]

### Discussion

\[
Why\ did\ it\ happen?
\]

以及：

\[
What\ does\ it\ mean?
\]

---

## D1. Interpretation

解释：
- physics prior 为什么有效；
- virtual data 为什么能 transfer；
- model alignment 为什么成功/失败；
- Twin fidelity 如何影响 downstream diagnosis。

---

## D2. Comparison with existing paradigms

不是重复 accuracy table。

讨论：
- 与纯 data-driven 的差异；
- 与 conventional simulation 的差异；
- 与 domain adaptation 的差异；
- 与 high-fidelity DT 的差异。

---

## D3. Applicability

明确：
- 需要哪些传感器；
- 是否需要 bearing parameters；
- 是否需要 target data；
- 是否需要在线更新；
- 是否只适用于 fixed speed；
- computational demand。

---

## D4. Limitations

建议至少写 2–4 条真实限制。

常见：
- simplified dynamics；
- unavailable true parameters；
- only localized defects；
- closed-set assumption；
- single sensor；
- limited machines；
- real-time performance 未验证。

不要写假的 limitation，例如：

> Future work will further improve accuracy.

---

# 5. Conclusions

Conclusion 不需要再次列完整方法。

推荐顺序：

### C1
研究问题。

### C2
所采用总体方案。

### C3
Twin validation 与 diagnosis 最关键结论。

### C4
适用边界与下一步。

最终应该回答：

> 这篇论文除了得到一个 accuracy 数字之外，增加了什么可复用知识？

