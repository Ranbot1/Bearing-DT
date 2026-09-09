# 06 — 写作检查清单

在投稿前逐项检查。

---

# A. 题目与摘要（Title / Abstract）

- [ ] 标题能看出 bearing + DT role + diagnosis task。
- [ ] 摘要有明确现实问题。
- [ ] 摘要明确说明 Twin 做什么。
- [ ] 摘要没有堆 5 个以上模块缩写。
- [ ] 摘要有定量实验结果。
- [ ] 摘要中的 claims 全部在正文得到验证。

---

# B. 引言（Introduction）

- [ ] 第 1 段建立现实诊断问题。
- [ ] 第 2 段指出 data-driven / current method 的具体限制。
- [ ] DT 是由问题自然引出的，不是突然出现。
- [ ] 明确指出 DT 本身也存在 simulation-real gap / fidelity 等挑战。
- [ ] 文献综述按路线分类，而不是年份流水账。
- [ ] 最后一段有明确 research objective。
- [ ] Contributions 不与 existing work 重复。
- [ ] Contributions 中没有写实验尚未证明的结论。

---

# C. 数字孪生建模（Digital Twin Modeling）

- [ ] 建模对象和物理边界明确。
- [ ] 坐标系明确。
- [ ] DOF 明确。
- [ ] bearing geometry 明确。
- [ ] contact model 明确。
- [ ] fault geometry / excitation 明确。
- [ ] speed/load 如何进入模型明确。
- [ ] 每个关键参数有来源。
- [ ] 明确哪些参数是 measured / known / identified / assumed。
- [ ] numerical solver 可复现。
- [ ] sampling / simulation duration 可复现。
- [ ] Twin 输出变量明确。
- [ ] 没有把 simulator 自动称为 high-fidelity Twin。

---

# D. Twin 验证（Twin Validation）

- [ ] 有独立 Twin validation，而不是只有 diagnosis accuracy。
- [ ] characteristic frequency / mechanism 一致性得到验证。
- [ ] 若声称 high fidelity，有 waveform/statistical/distribution 证据。
- [ ] simulated vs real comparison 使用同等 preprocessing。
- [ ] 没有只靠 t-SNE 证明 virtual-real similarity。
- [ ] 讨论了 Twin 仍存在的 mismatch。

---

# E. 诊断方法（Diagnostic Method）

- [ ] Fig. 1 能说明 Twin 和 diagnosis 的接口。
- [ ] 明确 DT 是 generator / fusion source / domain / Teacher / state estimator 中哪种角色。
- [ ] 训练和测试阶段数据流清晰。
- [ ] target data 是否参与训练说清楚。
- [ ] 网络输入维度明确。
- [ ] 每个 loss 的物理/统计作用明确。
- [ ] 总损失和优化方向明确。
- [ ] 普通 backbone 没有被过度包装成主要贡献。

---

# F. 实验协议（Experimental Protocol）

- [ ] 数据集/试验台来源明确。
- [ ] bearing 型号明确。
- [ ] sensor 和 sampling rate 明确。
- [ ] speed/load 明确。
- [ ] fault type/severity 明确。
- [ ] split unit 明确。
- [ ] window overlap 明确。
- [ ] train/val/test sample count 明确。
- [ ] normalization 没有使用 test statistics。
- [ ] 没有 obvious train-test leakage。
- [ ] baseline 足够强。
- [ ] hyperparameter selection protocol 明确。
- [ ] 至少多次重复或说明 random seed。

---

# G. 结果（Results）

- [ ] 先证明 Twin，再证明 diagnosis。
- [ ] 主结果报告 mean ± std（若可行）。
- [ ] 不只报告 Accuracy。
- [ ] 有 ablation。
- [ ] Ablation 能对应方法机制。
- [ ] 有 robustness / sensitivity。
- [ ] 可视化与 quantitative result 一致。
- [ ] 没有 cherry-pick 只展示最好 task。
- [ ] improvement 与 strongest relevant baseline 比较。

---

# H. 讨论（Discussion）

- [ ] 解释为什么有效，而不是重复准确率。
- [ ] 明确哪些信息来自 physics，哪些来自 data。
- [ ] 讨论 sim-real gap。
- [ ] 讨论 parameter uncertainty。
- [ ] 讨论 computational cost。
- [ ] 讨论适用条件。
- [ ] 讨论失败场景。
- [ ] 局限是真实局限，不是礼貌性一句话。

---

# I. 结论（Conclusion）

- [ ] 不引入新实验。
- [ ] 不引入正文没定义的新概念。
- [ ] 不夸大 industrial applicability。
- [ ] 结论和实验协议相匹配。
- [ ] Future work 针对已识别局限。

---

# J. 图—表—正文联动（Figure / Table / Text Coupling）

- [ ] 每张 Figure/Table 都对应一个明确 claim 或必要 protocol 信息。
- [ ] 结构图用于解释系统/流程，而不是承担性能证明。
- [ ] 参数表明确数值、单位和来源，不让正文反复列参数。
- [ ] Twin validation 既有直观 Figure，也有适当定量指标（若 claim 需要）。
- [ ] 主结果优先用 Table 给精确数值，不靠柱状图代替可比较数字。
- [ ] Confusion matrix / t-SNE 等 Figure 用来解释主结果，而不是替代主结果。
- [ ] Ablation 的 Table 与解释性 Figure 不重复同一信息。
- [ ] 图表出现前，正文已经说明“为什么需要看它”。
- [ ] 图表之后，正文至少包含“观察 + 含义”，而不是只写“Fig. X shows ...”。
- [ ] 正文没有逐行/逐列朗读 Table。
- [ ] 每个结果小节结尾能自然过渡到下一论证问题。
- [ ] 没有为了“看起来像顶刊”机械堆 20 张以上图。
- [ ] Supplementary Material 承担次要图表，主文只保留核心证据链。

---

# K. 可复现性（Reproducibility）

- [ ] DOI / dataset links 准确。
- [ ] parameter table 足以重建 simulator。
- [ ] preprocessing 可复现。
- [ ] split 可复现。
- [ ] network/training setting 可复现。
- [ ] code availability 如实说明。
- [ ] data availability 如实说明。
- [ ] third-party implementation 没有误标成 official code。

---

# 最后一项：一句话审稿测试

投稿前尝试用一句话回答以下五个问题：

### Q1
这篇论文研究的具体 bearing diagnosis problem 是什么？

### Q2
为什么需要 Digital Twin？

### Q3
Twin 为什么可信？

### Q4
Twin 通过什么机制改善 diagnosis？

### Q5
哪组实验分别支持 Q3 和 Q4？

如果其中任意一项无法在 1–2 句话内回答，说明论文主线仍可能过于分散。
