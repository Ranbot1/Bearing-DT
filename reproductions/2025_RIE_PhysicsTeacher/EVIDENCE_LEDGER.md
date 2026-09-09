# 证据台账

审计日期：2026-09-09。

## A. 已确认（CONFIRMED）

来自论文官方开放页面或正文：

| 项目 | 状态 | 说明 |
|---|---|---|
| 4-DOF 滚动轴承动力学模型 | CONFIRMED | 论文 Sec. 3.1 |
| Hertz 接触理论 | CONFIRMED | 论文 Sec. 3.1 |
| 时变接触刚度建模路线 | CONFIRMED | adapted from Luo et al. |
| 内外圈 x-y 动力学 | CONFIRMED | \(x_i,y_i,x_o,y_o\) |
| 支承质量/刚度/阻尼项 | CONFIRMED | Eq. (5) description |
| 径向力、偏心、转速、重力 | CONFIRMED | Eq. (5) description |
| 模拟数据预训练 | CONFIRMED | simulated vibration → pretrained network |
| 物理引导知识损失 | CONFIRMED | proposed method |
| 全局 + 细粒度类别级对齐 | CONFIRMED | proposed multi-adversarial framework |
| Paderborn + HUST 公共数据集 | CONFIRMED | experiments |
| 论文平均结果约 88.15%、96.74% | CONFIRMED | abstract |
| 内圈仿真特征频率 123.24 Hz | CONFIRMED | Eq. (6) / Fig. 5 discussion |
| 特征提取器 = 4 个卷积层 + BN + CBAM | CONFIRMED | Sec. 3.5 / Table 9 |
| 特征维度 = 128 | CONFIRMED | Table 9 |
| 标签预测器 = 128→3（PU）、128→7（HUST） | CONFIRMED | Table 9 |
| 域判别器 = 128→64→1 | CONFIRMED | Table 9 |
| 卷积激活 = Leaky ReLU | CONFIRMED | Table 9 |
| 优化器 = SGD，学习率 1e-4 | CONFIRMED | Table 9 |
| batch size = 16，iterations = 100 | CONFIRMED | Table 9 |
| 损失权重 λm/λt/λk = 1.0/0.05/10.0 | CONFIRMED | Table 9 |
| 重复次数 = 10 | CONFIRMED | Table 9 |
| 知识损失使用 MK-MMD | CONFIRMED | Sec. 3.2–3.4 |
| PU Setting 0/1/2/3 工况 | CONFIRMED | Table 3 / Table 8 |
| 尚未确认官方 GitHub | CONFIRMED AS SEARCH STATUS | repository audit |

## B. 6203 几何参数（正文级已记录）

| 参数 | 数值 | 状态 |
|---|---:|---|
| 外径 | 40 mm | CONFIRMED |
| 内径 | 17 mm | CONFIRMED |
| 宽度 | 12 mm | CONFIRMED |
| 滚动体直径 | 6.75 mm | CONFIRMED |
| 节圆直径 | 28.5 mm | CONFIRMED |
| 滚动体数量 | 8 | CONFIRMED |
| 接触角 | 0 deg | CONFIRMED |

## C. 当前未完全核实，因此只能标记为 INFERRED

以下值**不能**宣称为论文原值：

- 内圈/外圈等效质量；
- 支承刚度 \(k_{ix},k_{iy},k_{ox},k_{oy}\)；
- 支承阻尼；
- Hertz coefficient 数值；
- bearing clearance 精确数值；
- eccentricity 精确数值；
- defect depth / angular width；
- numerical integrator 与 tolerances（若正文后续仍未核到）；
- exact sample window length；
- Fig. 7/9 中仅以图示给出的卷积通道数 / kernel size；
- 最终网络 exact input representation dimensionality；
- MK-MMD kernel bandwidths。

这些参数当前只用于让代码结构可运行。

## D. 方程实现注意事项

论文官方页面的 Eq. (5) 网页抓取存在排版异常：部分 y/x 方程的二阶导符号在 HTML 抽取中可能丢失。

因此代码采用**物理一致的二阶 4-DOF ODE**：

\[
M\ddot q + C\dot q + Kq = F_{contact}+F_{external}
\]

而不是机械复制网页中可能损坏的 HTML 文本。

状态：**REFERENCED / physically reconstructed**。

## E. 已发现的原文歧义

Table 1 中 6203 的 “Bearing Speed” 与 Eq. (6) / PU Setting 0 的约 1500 rpm 语境存在单位或录入层面的不一致。当前处理方式：

- characteristic-frequency validation 以 Eq. (6) 的 **123.24 Hz** 作为 paper reference；
- PU transfer condition 以 Table 3 的 **1500 rpm** 为准；
- 不使用 Table 1 的 speed 字段覆盖实验工况。

## F. 复现代码产生的证据

以下不是论文事实，而是当前代码的验收结果：

- 当前 6203 + 1500 rpm config 独立计算 BPFI = **123.6842 Hz**；
- 论文 Fig. 5 reference = **123.24 Hz**，二者差约 0.36%；
- 当前 inner simulation raw-spectrum interpolated peak = **123.561 Hz**；
- envelope audit peak = **123.650 Hz**；
- 900 rpm 时 envelope peak = **74.200 Hz**，与 1500 rpm 峰值比约 0.60008；
- 初始 outer angle 270 deg 落在当前坐标系的非承载区，outer simulation 与 normal 相同；
- outer angle 90 deg（INFERRED loaded-zone center）后，envelope peak = **76.304 Hz**，接近理论 BPFO 76.3158 Hz；
- integration max step 从 1/(4fs) 放宽到 1/fs 时，0.1 s inner waveform correlation = **0.9999999988**，relative RMSE/std = **4.93e-5**。

详见：
[reports/R1_R2_SIGNAL_VALIDATION_20260909.md](reports/R1_R2_SIGNAL_VALIDATION_20260909.md)

## G. Dual-impulse 重建证据

2025 论文将 localized-spall 响应建立在 Luo et al. 的动力学路线之上。当前可访问的被引文献明确区分：

- rolling element 进入 spall：较低频的 step-type response；
- rolling element 离开时撞击 trailing edge：较高频的 transient response。

采用 half-cosine spall displacement + explicit exit collision 后，复现结果为：

- theoretical DITS = 1.078014 ms；
- detected median DITS = 1.093750 ms；
- DITS error = 1.460%；
- median exit/entry HF peak ratio = 1.785；
- median exit/entry HF RMS ratio = 1.310；
- envelope BPFI error = 0.242%；
- 禁用 exit collision 后，median HF peak ratio 降至 0.870。

碰撞项的数值幅值与持续时间仍然属于 INFERRED，不宣称为论文参数。

审计快照：
[artifacts/audit_snapshots/20260909_dual_impulse_r2/README.md](artifacts/audit_snapshots/20260909_dual_impulse_r2/README.md)

## H. 输入预处理审计

开放全文能够确认 simulated vibration data + CNN pretraining，但没有提供可完整复现的 window length、stride、normalization、raw-1D / reshaped-2D / time-frequency 输入形式或 input tensor dimensions。

详见：
[PREPROCESSING_AUDIT.md](PREPROCESSING_AUDIT.md)

## I. 下一步证据补齐

优先继续核对：

1. localized spall “dual-impulse” 的精确几何/接触函数；
2. 论文未公开的有效质量、支承刚度/阻尼、Hertz coefficient 等 simulator 数值；
3. Fig. 7/9 中卷积核与通道数；
4. exact input representation / preprocessing；
5. Paderborn Table 6 的具体 bearing IDs；
6. HUST Table 7 的具体 source/target sample composition。

任何补齐后都必须把本文件对应项从 INFERRED 改为 CONFIRMED，并记录来源。
