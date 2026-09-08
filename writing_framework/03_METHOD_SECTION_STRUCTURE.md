# 03 — DT 建模与诊断方法章节写法

方法章节建议拆成两个逻辑对象：

\[
\boxed{Digital\ Twin}
\quad+\quad
\boxed{Diagnostic\ Method}
\]

不要把动力学方程、CNN、loss 和实验参数全部混在一个章节。

---

# Part A — Digital Twin Modeling

---

## A1. Modeling object and assumptions

开头用一张结构图定义：

- shaft；
- inner race；
- outer race；
- rolling elements；
- cage；
- support/housing；
- load；
- sensor location。

同时声明建模边界。

例如：

> Which components are explicitly modeled and which effects are neglected?

常见 assumptions：
- rigid rings；
- pure rolling / prescribed slip；
- constant contact angle；
- localized defect geometry；
- linear support；
- constant/variable speed。

这些假设最好集中列出，而不是散落在方程后面。

---

## A2. Coordinates and kinematics

先定义符号，再上动力学方程。

推荐顺序：

1. coordinate system；
2. rolling element angular position；
3. cage speed；
4. relative displacement；
5. contact deformation。

例如：

\[
\theta_j(t)
\]

必须在首次出现时定义。

---

## A3. Contact mechanics

解释：

\[
\delta_j
\rightarrow
F_j
\]

例如 Hertz relation：

\[
F_j = K\,[\delta_j]_+^{3/2}
\]

随后解释：
- \(K\)；
- contact condition；
- clearance；
- load distribution。

方程后必须有物理解释，不要只列公式。

---

## A4. System dynamic equations

统一给：

\[
M\ddot q+C\dot q+Kq=F(q,\dot q,t)
\]

再展开具体 DOF。

最佳写法：

### 先给 compact matrix form

让读者理解系统。

### 再给 component equations

用于复现。

如果有 10+ 个方程，可把部分推导移到 Appendix / Supplementary Material。

---

## A5. Fault excitation model

这是 DT 故障诊断论文里非常关键的一节。

必须回答：

\[
\boxed{\text{故障到底如何改变动力学系统？}}
\]

不是只给 BPFI/BPFO。

可以写成：

\[
Defect\ Geometry
\rightarrow
Contact\ Deformation
\rightarrow
Contact\ Force
\rightarrow
Dynamic\ Response
\]

分别解释：
- inner race；
- outer race；
- roller；
- cage / compound faults（若研究涉及）。

最好配一张 defect geometry 图。

---

## A6. Parameter source

单独给表：

| Parameter | Symbol | Value | Unit | Source |
|---|---|---:|---|---|
| Ball number | \(N_b\) | — | — | bearing specification |
| Pitch diameter | \(D_p\) | — | mm | manufacturer |
| Radial load | \(F_r\) | — | N | experiment |
| Contact stiffness | \(K\) | — | — | calculation / identification |
| Damping | \(c\) | — | — | identified / assumed |

“Source”这一列非常重要。

它区分：

\[
measured
,\quad
known
,\quad
identified
,\quad
assumed
\]

避免读者不知道参数是不是为了拟合结果手调出来的。

---

## A7. Numerical solution and virtual data generation

必须给：
- integration / solver；
- step size；
- sampling frequency；
- simulation length；
- transient removal；
- number of virtual runs；
- operating-condition range。

这些信息直接决定可复现性。

---

# Part B — Twin Validation

Twin validation 最好放在诊断网络之前或作为 Results 第一部分。

需要至少包含两类证据。

---

## B1. Mechanism-level validation

回答：

> 故障机理是否正确？

例如：
- BPFI；
- BPFO；
- BSF；
- harmonics；
- modulation；
- speed-dependent shift；
- defect-impact periodicity。

比较：

\[
f_{theory}
,\quad
f_{sim}
,\quad
f_{real}
\]

---

## B2. Signal/statistical validation

若论文声称 high-fidelity / real-like，才需要更进一步比较：

- waveform；
- RMS；
- kurtosis；
- PSD；
- envelope spectrum；
- time-frequency map；
- distribution distance；
- modal frequencies。

不要只给“看起来很像”的两张波形图。

---

## B3. Parameter / state validation

若研究包含 parameter identification / dynamic updating，还应验证：

\[
\theta_{estimated}
\]

或：

\[
state_{DT}
\]

是否与可测 physical state 一致。

---

# Part C — Digital-Twin-Assisted Diagnosis

---

## C1. Overall architecture first

先用一张图回答：

\[
Twin\ Output
\rightarrow
What\ Module
\rightarrow
Diagnostic\ Prediction
\]

再讲网络细节。

---

## C2. Clearly define the role of DT

Twin 常见角色只有几类：

### Source-data generator

\[
D_{DT}\rightarrow Training
\]

### Data enhancer / fusion source

\[
D_{DT}+D_{real}\rightarrow D_{fused}
\]

### Domain source

\[
D_{DT}\rightarrow Domain\ Adaptation\rightarrow D_{real}
\]

### Teacher / prior

\[
T_{DT}\rightarrow Student
\]

### State estimator

\[
DT\leftrightarrow Sensor
\]

论文必须明确属于哪一种或哪几种。

---

## C3. Diagnostic backbone

如果 backbone 是普通 CNN/ResNet：

只需要写：
- input；
- key blocks；
- feature dimension；
- classifier。

不要把十几层普通 convolution 写成主要贡献。

如果 backbone 是核心方法，则另当别论。

---

## C4. Virtual-real interaction mechanism

这里是诊断方法的重点。

建议按：

\[
Input
\rightarrow
Operation
\rightarrow
Constraint
\rightarrow
Output
\]

写每一个模块。

例如：

### Domain adaptation

Input:
\[
z_s,z_t
\]

Operation:
distribution measurement / discriminator

Constraint:
\[
D(z_s,z_t)
\]

Output:
domain-invariant representation

不要只说“we align the domains”。

---

## C5. Loss function

先列子损失：

\[
\mathcal L_{cls}
,\quad
\mathcal L_{transfer}
,\quad
\mathcal L_{physics}
,\quad
\mathcal L_{KD}
\]

再给总目标：

\[
\mathcal L_{total}
=
\lambda_1\mathcal L_{cls}
+
\lambda_2\mathcal L_{transfer}
+
\lambda_3\mathcal L_{physics}
\]

每个 \(\lambda\) 的作用要说明。

如果存在 min-max：

\[
\min_G \max_D
\]

必须明确哪个模块 minimize、哪个 maximize。

---

## C6. Training procedure

建议写成阶段：

### Stage 1
Twin simulation / Teacher pretraining

### Stage 2
Virtual-real interaction / adaptation

### Stage 3
Classifier optimization

### Stage 4
Inference

如果全部 end-to-end，也要写清楚数据在一个 iteration 中怎样流动。

---

# 方法章节最终检查

读者应该能仅靠 Method section 回答：

1. 建模对象是什么？
2. 哪些物理量被模拟？
3. 故障如何进入方程？
4. 参数从哪里来？
5. Twin 输出是什么？
6. 怎么证明 Twin 合理？
7. Twin 输出如何进入诊断算法？
8. 训练时用了哪些真实数据？
9. 测试时需要 Twin 吗？
10. 部署阶段需要 target data 吗？

如果其中任何一项答不上来，方法描述通常还不够完整。
