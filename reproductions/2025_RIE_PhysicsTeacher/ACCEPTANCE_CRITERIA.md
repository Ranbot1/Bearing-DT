# 验收标准

复现按阶段验收，禁止用“最终准确率接近”掩盖前面物理模型或协议错误。

---

## R0 — Repository / reproducibility hygiene

必须全部通过：

- [ ] `pip install -e ".[dev]"` 可安装。
- [ ] `pytest -q` 通过。
- [ ] 所有运行参数来自 config，不写死在训练脚本。
- [ ] random seed 可固定。
- [ ] raw data 不提交 Git。
- [ ] results 按 run directory 保存 config + metrics。
- [ ] CONFIRMED / INFERRED 参数可追踪。

**R0 不通过，不进入论文结果对齐。**

---

## R1 — Physics simulator sanity

### R1.1 Characteristic frequencies

由同一组 bearing geometry 和 shaft speed 计算：

[
BPFI, BPFO, BSF, FTF
]

必须满足标准运动学公式，单元测试误差 < (10^{-9})（代码计算一致性）。

### R1.2 Numerical stability

对 normal / inner / outer 三种状态：

- solver 正常结束；
- 所有 state / acceleration 为 finite；
- 不出现 NaN/Inf；
- 接触力非负；
- 给定随机种子结果可重复。

### R1.3 Mechanism-level spectral validation

对论文对应 6203 配置：

- inner fault 的主要故障周期证据应落在理论 BPFI 邻域；
- outer fault 的主要故障周期证据应落在理论 BPFO 邻域；
- 允许 tolerance：**±2%**（第一阶段）；
- 分析优先使用 envelope spectrum，而不是强行要求 raw FFT 最大峰等于故障频率。

### R1.4 Fault / speed consistency

改变 shaft speed 时：

[
f_{fault}propto f_r
]

归一化到 order 后，主要机制位置应保持一致。

---

## R2 — Paper figure-level simulator reproduction

目标：至少复现论文一组 6203 simulated fault signal 的核心物理现象。

验收：

- [ ] 使用论文确认的 6203 geometry。
- [ ] 明确列出所有 INFERRED 动力学参数。
- [ ] 输出 waveform + spectrum/envelope。
- [ ] 理论频率与模拟频率定量对照表。
- [ ] 不以“视觉相似”代替物理一致性。
- [ ] 若无法复现论文幅值/共振形态，必须记录为 unresolved gap。

---

## R3 — Teacher pretraining

验收：

- [ ] simulation dataset 生成脚本固定 config/hash。
- [ ] Teacher 输入预处理可复现。
- [ ] simulated-domain train/val/test 独立。
- [ ] Teacher 在 simulated held-out set 上达到稳定分类性能。
- [ ] 至少 3 seeds，报告 mean ± std。
- [ ] 不能仅报告 training accuracy。

阶段目标不是强制某个百分比，而是先证明 Teacher 真正从 simulation 学到可重复分类表示。

---

## R4 — Paderborn transfer reproduction

验收：

- [ ] 数据来源/文件列表固定。
- [ ] source/target condition 按论文定义。
- [ ] segmentation 与 normalization 全部记录。
- [ ] normalization statistics 只来自允许的 training data。
- [ ] 实现 global + class-wise adversarial alignment。
- [ ] 实现 physics-guided knowledge loss。
- [ ] 至少 3 seeds。
- [ ] 与 ERM / DANN / MADA 等合理 baseline 同协议比较。

### Paper-level target

论文报告该数据集相关 transfer tasks 的平均结果约 **88.15%**。

第一轮接受区间：

[
|Acc_{repro}-Acc_{paper}|le 3 	ext{percentage points}
]

若超出，不允许只继续调参；必须先查：
- preprocessing；
- task definition；
- exact architecture；
- loss weights；
- paper ambiguity。

---

## R5 — HUST transfer reproduction

同 R4。

论文报告相关任务平均结果约 **96.74%**。

第一轮接受区间：

[
|Acc_{repro}-Acc_{paper}|le 3 	ext{percentage points}
]

---

## R6 — Reproduction completeness

最终至少提供：

- [ ] simulator validation report
- [ ] exact config files
- [ ] environment lock / dependency versions
- [ ] dataset manifest
- [ ] teacher metrics
- [ ] transfer metrics
- [ ] ablation
- [ ] paper-vs-reproduction comparison table
- [ ] unresolved differences
- [ ] reproducible command list

只有 R0–R6 主要项完成，才标记：

`REPRODUCED`

否则使用：

- `SKELETON`
- `PARTIAL`
- `PHYSICS_REPRODUCED`
- `METHOD_REPRODUCED`

等更准确状态。
