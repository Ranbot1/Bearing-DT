# 04 — 实验、结果与讨论写法

DT 诊断论文的实验最好按**论证问题**排，而不是按“我做了哪些图”排。

推荐证据顺序：

\[
Twin\ 可信性
\rightarrow
诊断有效性
\rightarrow
模块必要性
\rightarrow
稳健性
\rightarrow
适用边界
\]

---

# 1. 实验设置（Experimental Setup）

这一部分只描述 protocol，不提前解释优劣。

## 1.1 数据集 / 试验台说明

推荐表格：

| 数据集/试验台 | 轴承 | 故障 | 转速 | 载荷 | 采样率 | 传感器 |
|---|---|---|---|---|---|---|

正文只解释：

- 为什么选这些工况；
- 哪些是 source / target；
- 哪些用于 Twin calibration；
- 哪些完全保留给 test。

---

## 1.2 数据划分

必须明确 split unit：

\[
sample/window
\]

还是：

\[
record,
\quad
bearing,
\quad
machine
\]

报告：

- physical recordings 数量；
- generated windows 数量；
- train / validation / test counts；
- overlap。

特别是 vibration segmentation，不能只写“80/20 random split”。

---

## 1.3 仿真参数设置

单独给：

| 参数 | 数值/范围 | 来源 |
|---|---|---|

并区分：

- fixed；
- randomized；
- optimized。

---

## 1.4 对比方法（Baselines）

不要把所有 baseline 混成一列。

建议分类：

### 纯数据驱动
CNN / ResNet / Transformer 等。

### 迁移 / 域适配
DANN / MMD / CDAN 等。

### 物理引导
physics regularization / PINN / feature prior。

### 数字孪生方法
与本文属于同类型的 DT 方法。

这样主结果表的意义更清晰。

---

## 1.5 实现细节

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

# 2. 结果：推荐五层证据

## R1. Twin 验证

这一部分应当**先于最终分类准确率**。

### 机制证据

展示：

- theoretical characteristic frequency；
- virtual spectrum；
- measured spectrum。

### 信号证据

若有 high-fidelity claim，展示：

- PSD；
- envelope；
- time-frequency；
- statistic/distribution metric。

结果文字回答：

> 哪些物理特征被正确复现？哪些仍存在差异？

不要只写“曲线高度相似”后就结束。

---

## R2. 主诊断结果

这是主 comparison table。

推荐：

| 方法 | Task 1 | Task 2 | Task 3 | 平均值 | Macro-F1 |
|---|---:|---:|---:|---:|---:|

主文只强调：

- overall ranking；
- difficult tasks；
- statistical consistency。

不要逐单元格朗读表格。

---

## R3. 消融实验（Ablation Study）

Ablation 的目标是：

\[
\boxed{\text{证明模块必要性}}
\]

不是简单删三个 module 后再报 accuracy。

推荐：

| 变体 | Twin | Transfer | Physics/KD | Accuracy | F1 |
|---|---|---|---|---:|---:|

同时解释：

> 去掉该模块后，改变的是哪条机制？

例如：

- gap increases；
- feature separation worsens；
- noise robustness decreases。

---

## R4. 稳健性 / 敏感性

DT 论文尤其适合做：

### 噪声
\[
SNR=...
\]

### 转速 / 载荷变化
不同 operating condition。

### 样本稀缺
真实 labeled data percentage：

\[
1\%,5\%,10\%,...
\]

### 参数不确定性
Twin parameters 扰动：

\[
\theta(1\pm\epsilon)
\]

### 超参数敏感性
只分析真正重要的 \(\lambda\)，不要把所有学习率都画一遍。

---

## R5. 表示与物理解释

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

# 3. 结果中的正文—Figure—Table 标准联动

高质量结果小节不是“先放图表，再补两句描述”，而是按论证问题组织。

推荐：

\[
问题
\rightarrow
设置
\rightarrow
Figure
\rightarrow
Table
\rightarrow
解释
\rightarrow
过渡
\]

并不是每个实验都必须同时有 Figure 和 Table；只有当二者承担不同职责时才成对出现。

### 典型配对 1 — Twin validation

**Figure**：让读者看见 simulated / measured waveform、spectrum、time-frequency 的对应关系。  
**Table**：给 characteristic-frequency error、MMD、modal error、statistical distance 等精确值。

正文依次回答：为什么现在需要验证 Twin？哪个物理现象被复现？这种一致性在数值上有多大？这些 virtual data 是否足以进入后续诊断阶段？

### 典型配对 2 — 主结果比较

**Table**：主 accuracy / F1 / mean±std。  
**Figure**：confusion matrix、t-SNE/UMAP 或代表性 feature/spectrum。

Table 回答“提升了多少”，Figure 回答“改善具体发生在哪些类别或表示结构”。

### 典型配对 3 — Ablation / Robustness

**Table**：删除模块或改变条件后，性能下降多少。  
**Figure**：feature separability、sensitivity curve、noise/condition 下 representation 如何变化。

Table 支持“该模块有效”，Figure 帮助解释“为什么可能有效”。

---

# 4. Results 的标准段落结构

每个实验小节推荐四句逻辑：

1. **问题句**：该实验用于验证什么；
2. **设置句**：在什么条件下比较；
3. **结果句**：给 1–3 个最重要数字；
4. **解释句**：说明结果支持哪个机制判断。

若同时包含 Figure 与 Table，可以扩展为“目的 → 设置 → Figure 观察 → Table 定量 → 解释 → 过渡”。

---

# 5. 讨论（Discussion）

Discussion 与 Results 的区别：

- Results 回答：**发生了什么？**
- Discussion 回答：**为什么发生？意味着什么？**

## D1. 结果解释

讨论：physics prior 为什么有效、virtual data 为什么能 transfer、model alignment 为什么成功/失败、Twin fidelity 如何影响 downstream diagnosis。

## D2. 与现有范式比较

不是重复 accuracy table，而是讨论与纯 data-driven、conventional simulation、domain adaptation、high-fidelity DT 的本质差异。

## D3. 适用性

明确：需要哪些传感器、是否需要 bearing parameters、是否需要 target data、是否需要在线更新、是否只适用于 fixed speed、computational demand 如何。

## D4. 局限

建议至少写 2–4 条真实限制，例如 simplified dynamics、unknown true parameters、only localized defects、closed-set assumption、single sensor、limited machines、real-time performance 未验证。

---

# 6. 结论（Conclusions）

推荐顺序：

1. 研究问题；
2. 总体方案；
3. Twin validation 与 diagnosis 最关键结论；
4. 适用边界与下一步。

最终应该回答：

> 这篇论文除了得到一个 accuracy 数字之外，增加了什么可复用知识？
