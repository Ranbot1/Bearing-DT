# R1/R2 Signal Validation — 2026-09-09

## Scope

目标不是训练 Teacher，而是先验证当前 4-DOF simulator 是否能生成论文 Fig.5 所强调的故障运动学证据。

论文对 6203 inner-race simulation 的核心检查是：

\[
f_{BPFI}^{paper}=123.24\ \text{Hz}
\]

并指出 simulation frequency-domain graph 在该位置附近出现明显 spike。

本报告按同样的 **time-domain + frequency-domain** 逻辑评估当前复现代码。Envelope spectrum 只作为额外审计。

---

## 1. Current configuration

Confirmed geometry:

- ball count: 8
- ball diameter: 6.75 mm
- pitch diameter: 28.5 mm
- contact angle: 0 deg
- PU Setting-0 speed used by reproduction: 1500 rpm
- sampling rate: 64 kHz

当前 mass / stiffness / damping / Hertz coefficient / clearance / defect dimensions 仍属于 **INFERRED**，因此本报告只验收 mechanism-level consistency，不验收 waveform amplitude fidelity。

---

## 2. Independent theoretical check

由当前 config 几何和 1500 rpm 计算：

\[
f_{BPFI}^{config}=123.6842\ \text{Hz}
\]

论文 Fig.5 reference：

\[
f_{BPFI}^{paper}=123.24\ \text{Hz}
\]

二者差约 **0.36%**。

判断：**PASS with documented discrepancy**。不修改公式去强行得到论文数值。

---

## 3. Inner-race generated signal

使用当前 4-DOF + Hertz + localized inner defect 模型生成 64 kHz virtual acceleration。

较长稳定段的频谱结果：

| Item | Value |
|---|---:|
| config theoretical BPFI | 123.684 Hz |
| paper Fig.5 BPFI | 123.240 Hz |
| raw-spectrum interpolated peak | **123.561 Hz** |
| error vs config theory | **0.100%** |
| error vs paper Fig.5 | **0.260%** |
| envelope-spectrum interpolated peak | **123.650 Hz** |
| envelope error vs config theory | **0.028%** |
| envelope error vs paper Fig.5 | **0.333%** |

### Interpretation

**R1.3 PASS**。

当前 simulator 能在论文关注的 BPFI 邻域生成明确频域证据；从“故障运动学是否被保留”这一层看，inner-race Twin 数据是可用的。

---

## 4. Normal-vs-inner audit

为了排除“123 Hz 只是 normal 模型本身的谐波”这一可能，使用相同 dynamics 和 speed 比较 normal 与 inner。

在 BPFI 邻域：

- inner raw-spectrum target-band power 相对 normal 增强约 **83.6 dB**；
- inner envelope target-band power 相对 normal 增强约 **111.4 dB**。

判断：

> BPFI 证据主要来自 localized inner defect intervention，而不是 normal baseline 自带的固定谱峰。

---

## 5. Speed-scaling test

把 shaft speed 从 1500 rpm 改为 900 rpm，其他模型保持不变。

理论：

\[
f_{BPFI}=74.2105\ \text{Hz}
\]

检测结果：

| Item | Value |
|---|---:|
| theoretical BPFI @ 900 rpm | 74.211 Hz |
| raw-spectrum interpolated peak | 73.932 Hz |
| envelope interpolated peak | 74.200 Hz |
| envelope peak ratio (900/1500) | **0.60008** |
| shaft-speed ratio | **0.60000** |

判断：**R1.4 PASS**。

故障频率随 shaft speed 成比例移动，order-domain mechanism consistency 成立。

---

## 6. Outer-race failure discovered

初始 config 使用 270 deg 作为 outer fault angle。

实际运行发现 outer-fault waveform 与 normal **完全相同**。

原因不是 solver 失败，而是当前 radial-load / coordinate convention 下，270 deg 位于非承载区，rolling elements 在该位置没有有效 Hertz contact，因此 defect clearance intervention 没有进入接触力。

这是一个真实的复现配置错误，不能忽略。

### Corrective audit

将 outer fault 放到当前承载区中心附近 90 deg，得到：

\[
f_{BPFO}^{theory}=76.3158\ \text{Hz}
\]

检测：

| Item | Value |
|---|---:|
| raw-spectrum peak | 76.651 Hz |
| raw error vs BPFO | 0.439% |
| envelope peak | 76.304 Hz |
| envelope error vs BPFO | **0.015%** |

判断：

- 原 270 deg config：**FAIL**
- loaded-zone 90 deg config：**PASS mechanism sanity**

由于论文未明确给出 outer fault angular position，90 deg 必须继续标记为 **INFERRED / coordinate-dependent**，不能称为 paper parameter。

---

## 7. Numerical integration audit

原 config max step:

\[
3.90625\times10^{-6}s
\]

即 64 kHz sample interval 的 1/4。

对 0.1 s inner signal，将 max step 放宽到一个 sample interval：

\[
1/64000=1.5625\times10^{-5}s
\]

与原严格积分比较：

- waveform correlation: **0.9999999988**
- relative RMSE / signal std: **4.93e-5**
- runtime 显著下降

因此后续 R1/R2 可以使用 sample-interval max step，提高批量数据生成效率。该值仍属于 numerical setting，不是论文确认参数。

---

## 8. Current gate decision

### R1

- characteristic-frequency formulas: PASS
- numerical stability: PASS for tested normal/inner/outer-loaded-zone
- inner BPFI evidence: PASS
- speed scaling: PASS
- outer initial config: FAIL -> corrected and documented

### R2

**PARTIAL PASS**

已经复现 Fig.5 最核心的 “inner-race frequency-domain spike near theoretical BPFI”。

尚未验收：

- paper-like time-domain morphology / dual-impulse shape
- amplitude fidelity
- resonance structure
- paper exact simulator parameters

因此状态仍应是：

**PHYSICS_REPRODUCED_PARTIAL**

还不能进入 “paper-level simulator fully reproduced”。

---

## 9. Retained verification artifacts

The generated signal evidence behind this report is retained in:

[artifacts/audit_snapshots/20260909_6203_r1r2](../artifacts/audit_snapshots/20260909_6203_r1r2/README.md)

It contains:
- generated normal / inner / outer signal checkpoints;
- the full 0–500 Hz raw/envelope spectral table from the 64 kHz generated signals;
- class metrics;
- theoretical characteristic frequencies;
- a code-generated SVG fault-frequency figure;
- config and SHA-256 provenance;
- hashes for the full-resolution NPZ arrays generated in the same run.

This artifact directory is intended to make the numerical claims independently auditable.

---

## 10. Next gate

在 Teacher pretraining 前继续做：

1. 固化 normal / inner / outer virtual-data generator；
2. 生成 PU 6203 三类 virtual dataset + manifest；
3. 对每类做 spectrum / envelope / speed-scaling QA；
4. 检查 localized-spall dual-impulse 是否与论文 Fig.4/Fig.5 一致；
5. 完成后才开放 R3 Teacher pretraining。
