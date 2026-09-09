# R1/R2 信号验收报告 — 2026-09-09

## 1. 目标范围

当前目标不是训练 Teacher，而是先验证现有 4-DOF simulator 是否能够生成论文 Fig. 5 所强调的故障运动学证据。

论文对 6203 inner-race simulation 的核心检查是：

\[
f_{BPFI}^{paper}=123.24\ \text{Hz}
\]

论文指出 simulation 的 frequency-domain graph 在该位置附近出现明显 spike。

因此本报告采用相同的 **time-domain + frequency-domain** 逻辑评估当前复现代码。Envelope spectrum 仅作为额外审计手段。

---

## 2. 当前配置

已经确认的 geometry：

- ball count：8
- ball diameter：6.75 mm
- pitch diameter：28.5 mm
- contact angle：0 deg
- 本复现使用的 PU Setting-0 speed：1500 rpm
- sampling rate：64 kHz

当前 mass / stiffness / damping / Hertz coefficient / clearance / defect dimensions 仍然属于 **INFERRED**。

因此本报告只验收 mechanism-level consistency，不验收 waveform amplitude fidelity。

---

## 3. 独立理论检查

由当前 config 中的几何参数和 1500 rpm 计算：

\[
f_{BPFI}^{config}=123.6842\ \text{Hz}
\]

论文 Fig. 5 reference：

\[
f_{BPFI}^{paper}=123.24\ \text{Hz}
\]

二者相差约 **0.36%**。

判断：**PASS，但保留并记录该差异。**

不修改公式去强行得到论文数值。

---

## 4. 内圈故障生成信号

使用当前 4-DOF + Hertz + localized inner defect 模型生成 64 kHz virtual acceleration。

较长稳定段的频谱结果：

| 指标 | 数值 |
|---|---:|
| config 理论 BPFI | 123.684 Hz |
| 论文 Fig. 5 BPFI | 123.240 Hz |
| raw-spectrum 插值峰值 | **123.561 Hz** |
| 相对 config 理论误差 | **0.100%** |
| 相对论文 Fig. 5 误差 | **0.260%** |
| envelope-spectrum 插值峰值 | **123.650 Hz** |
| envelope 相对 config 理论误差 | **0.028%** |
| envelope 相对论文 Fig. 5 误差 | **0.333%** |

### 解释

**R1.3 PASS。**

当前 simulator 能够在论文关注的 BPFI 邻域生成明确频域证据。

从“故障运动学是否被保留”这一层看，inner-race Twin 数据可以用于后续机制级研究。

---

## 5. Normal 与 Inner 对照审计

为了排除“123 Hz 只是 normal 模型自身谐波”的可能，在完全相同的 dynamics 与 speed 下比较 normal 与 inner。

在 BPFI 邻域：

- inner raw-spectrum target-band power 相对 normal 增强约 **83.6 dB**；
- inner envelope target-band power 相对 normal 增强约 **111.4 dB**。

判断：

> BPFI 证据主要来自 localized inner defect intervention，而不是 normal baseline 自带的固定谱峰。

---

## 6. 转速缩放验收

将 shaft speed 从 1500 rpm 改为 900 rpm，其余模型参数保持不变。

理论：

\[
f_{BPFI}=74.2105\ \text{Hz}
\]

检测结果：

| 指标 | 数值 |
|---|---:|
| 900 rpm 理论 BPFI | 74.211 Hz |
| raw-spectrum 插值峰值 | 73.932 Hz |
| envelope 插值峰值 | 74.200 Hz |
| envelope 峰值比例（900/1500） | **0.60008** |
| shaft-speed 比例 | **0.60000** |

判断：**R1.4 PASS。**

故障频率随 shaft speed 成比例移动，order-domain mechanism consistency 成立。

---

## 7. 发现 Outer-race 配置错误

初始 config 使用 270 deg 作为 outer fault angle。

实际运行发现 outer-fault waveform 与 normal **完全相同**。

原因不是 solver 失败，而是当前 radial-load / coordinate convention 下，270 deg 位于非承载区；rolling elements 在该位置没有有效 Hertz contact，因此 defect clearance intervention 没有进入接触力。

这是一个真实的复现配置错误，不能忽略。

### 修正审计

将 outer fault 放到当前承载区中心附近 90 deg，得到：

\[
f_{BPFO}^{theory}=76.3158\ \text{Hz}
\]

检测结果：

| 指标 | 数值 |
|---|---:|
| raw-spectrum peak | 76.651 Hz |
| raw 相对 BPFO 误差 | 0.439% |
| envelope peak | 76.304 Hz |
| envelope 相对 BPFO 误差 | **0.015%** |

判断：

- 原 270 deg config：**FAIL**
- loaded-zone 90 deg config：**PASS mechanism sanity**

由于论文没有明确给出 outer fault angular position，因此 90 deg 仍然必须标记为 **INFERRED / coordinate-dependent**，不能称为 paper parameter。

---

## 8. 数值积分审计

原 config 的 max step：

\[
3.90625\times10^{-6}s
\]

即 64 kHz sample interval 的 1/4。

对 0.1 s inner signal，将 max step 放宽到一个 sample interval：

\[
1/64000=1.5625\times10^{-5}s
\]

与原严格积分比较：

- waveform correlation：**0.9999999988**
- relative RMSE / signal std：**4.93e-5**
- runtime 明显下降

因此后续 R1/R2 可以使用 sample-interval max step，提高批量数据生成效率。

该值仍属于 numerical setting，不是论文确认参数。

---

## 9. 当前关口结论

### R1

- characteristic-frequency formulas：PASS
- numerical stability：PASS（已测试 normal / inner / outer-loaded-zone）
- inner BPFI evidence：PASS
- speed scaling：PASS
- outer 初始 config：FAIL → 已修正并记录

### R2

本报告最初阶段已经复现 Fig. 5 最核心的：

> inner-race frequency-domain spike near theoretical BPFI

后续 dual-impulse 专项审计已经进一步完成，当前 R2 机制级关口的最终状态见：

[Dual-impulse R2 审计](../artifacts/audit_snapshots/20260909_dual_impulse_r2/README.md)

因此当前总体状态为：

**PHYSICS_REPRODUCED（机制级）**

但这不等于已经完成 paper-level high-fidelity simulator calibration。

---

## 10. 留存的可核验产物

本报告背后的生成信号证据已经保存在：

[artifacts/audit_snapshots/20260909_6203_r1r2](../artifacts/audit_snapshots/20260909_6203_r1r2/README.md)

其中包含：

- 生成的 normal / inner / outer 信号检查点；
- 从 64 kHz 生成信号计算得到的完整 0–500 Hz raw/envelope 频谱表；
- 各类别指标；
- 理论轴承特征频率；
- 代码生成的 SVG 故障频率图；
- config 与 SHA-256 provenance；
- 同一次运行中生成的全分辨率 NPZ 数组哈希。

该目录的目的就是让上述数值结论可以被独立审计，而不需要只相信 Markdown 中的汇报。

---

## 11. 后续关口

后续工作已经推进到：

1. normal / inner / outer virtual-data generator：已完成；
2. PU 6203 三类 virtual dataset + manifest：pilot 已完成；
3. spectrum / envelope / speed-scaling QA：已完成机制级验收；
4. localized-spall dual-impulse：已通过专项 R2 审计；
5. Teacher pretraining：仍因 exact input preprocessing 未完全核实而保持 BLOCKED。

详见：
[PREPROCESSING_AUDIT.md](../PREPROCESSING_AUDIT.md)
