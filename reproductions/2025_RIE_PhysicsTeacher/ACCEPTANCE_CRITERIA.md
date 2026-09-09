# 验收标准

复现按阶段验收，禁止用“最终准确率接近”掩盖前面的物理模型或协议错误。

---

## 生成产物留存规则

每一个被判定为通过的复现阶段，都必须保留足够的生成证据，便于独立审计：

- 生成的信号数据，或具有代表性的原始数据快照；
- 支撑所报告峰值/指标的精确信号处理表；
- 由代码生成的图；
- config 与运行时参数快照；
- 文件哈希与来源信息（provenance）。

**仅有 Markdown 文字结论不足以作为阶段验收证据。**

---

## R0 — 仓库与可复现性规范

必须全部通过：

- [ ] `pip install -e ".[dev]"` 可安装。
- [ ] `pytest -q` 通过。
- [ ] 所有运行参数来自 config，不写死在训练脚本中。
- [ ] random seed 可固定。
- [ ] raw data 不提交 Git。
- [ ] results 按 run directory 保存 config + metrics。
- [ ] CONFIRMED / INFERRED 参数可追踪。

**R0 不通过，不进入论文结果对齐。**

---

## R1 — 物理模拟器基本合理性

### R1.1 轴承特征频率

由同一组 bearing geometry 和 shaft speed 计算：

\[
BPFI,\ BPFO,\ BSF,\ FTF
\]

必须满足标准运动学公式，单元测试误差 < \(10^{-9}\)（代码计算一致性）。

### R1.2 数值稳定性

对 normal / inner / outer 三种状态：

- solver 正常结束；
- 所有 state / acceleration 为 finite；
- 不出现 NaN/Inf；
- 接触力非负；
- 给定随机种子后结果可重复。

### R1.3 机制级频谱验收

对论文对应的 6203 配置：

- 论文 Eq. (6) / Fig. 5 给出的 inner-race reference 为 **123.24 Hz**；
- 我们根据 config 中的 geometry / speed 独立计算 theoretical BPFI；
- 两者应首先在 rounding / geometry precision 范围内一致；
- inner fault 的主要故障周期证据应落在理论 BPFI 邻域；
- outer fault 的主要故障周期证据应落在理论 BPFO 邻域；
- 第一阶段允许误差：**±2%**；
- 分析优先使用 envelope spectrum，而不是强行要求 raw FFT 最大峰等于故障频率。

### R1.4 故障频率与转速一致性

改变 shaft speed 时：

\[
f_{fault}\propto f_r
\]

归一化到 order 后，主要机制位置应保持一致。

---

## R2 — 论文图级模拟器复现

目标：至少复现论文一组 6203 simulated fault signal 的核心物理现象。

验收：

- [x] 使用论文确认的 6203 geometry。
- [x] 明确列出所有 INFERRED 动力学参数。
- [x] 输出 waveform + spectrum/envelope。
- [x] 给出理论频率与模拟频率的定量对照表。
- [x] 不以“视觉相似”代替物理一致性。
- [x] dual-impulse DITS error <= 5%。
- [x] exit/entry high-frequency peak ratio median >= 1.2。
- [x] exit/entry high-frequency RMS ratio median >= 1.1。
- [x] 禁用 trailing-edge collision 后，exit/entry ratio 必须下降。
- [x] 若无法复现论文幅值/共振形态，必须明确记录为 unresolved gap。

**R2 机制级关口：PASS。**

幅值与共振结构的物理标定明确不属于当前已经通过的证据等级。

---

## R3 — Teacher 预训练

验收：

- [ ] simulation dataset 生成脚本固定 config/hash。
- [ ] Teacher 输入预处理可复现。
- [ ] simulated-domain train/val/test 独立。
- [ ] Teacher 在 simulated held-out set 上达到稳定分类性能。
- [ ] 至少 3 个 seeds，报告 mean ± std。
- [ ] 不能只报告 training accuracy。

阶段目标不是强制达到某个百分比，而是先证明 Teacher 确实能从 simulation 中学习到可重复的分类表示。

---

## R4 — Paderborn 迁移复现

验收：

- [ ] 数据来源和文件列表固定。
- [ ] source/target condition 按论文定义。
- [ ] segmentation 与 normalization 全部记录。
- [ ] normalization statistics 只来自允许的 training data。
- [ ] 实现 global + class-wise adversarial alignment。
- [ ] 实现论文确认的 MK-MMD physics-guided knowledge loss。
- [ ] Feature extractor 满足已确认的 4 Conv + BN + CBAM + 128-d representation。
- [ ] SGD=1e-4、batch=16、iterations=100、λm/λt/λk=1.0/0.05/10.0 作为 paper-faithful 默认配置。
- [ ] 至少 3 个 seeds。
- [ ] 与 ERM / DANN / MADA 等合理 baseline 在同一协议下比较。

### 论文级目标

论文报告该数据集相关 transfer tasks 的平均结果约 **88.15%**。

第一轮接受区间：

\[
|Acc_{repro}-Acc_{paper}|\le 3\ \text{percentage points}
\]

若超出，不允许只继续调参；必须先检查：

- preprocessing；
- task definition；
- exact architecture；
- loss weights；
- paper ambiguity。

---

## R5 — HUST 迁移复现

同 R4。

论文报告相关任务平均结果约 **96.74%**。

第一轮接受区间：

\[
|Acc_{repro}-Acc_{paper}|\le 3\ \text{percentage points}
\]

---

## R6 — 复现完整性

最终至少提供：

- [ ] 模拟器验收报告
- [ ] 精确 config 文件
- [ ] 环境锁定信息 / 依赖版本
- [ ] 数据集 manifest
- [ ] Teacher 指标
- [ ] transfer 指标
- [ ] ablation
- [ ] 论文结果与复现结果对比表
- [ ] 尚未解决的差异
- [ ] 可复现命令清单

只有 R0–R6 主要项完成，才标记：

`REPRODUCED`

否则使用更准确的状态：

- `SKELETON`
- `PARTIAL`
- `PHYSICS_REPRODUCED`
- `METHOD_REPRODUCED`
