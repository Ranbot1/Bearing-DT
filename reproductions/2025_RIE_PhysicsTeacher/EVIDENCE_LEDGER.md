# Evidence Ledger

审计日期：2026-09-09。

## A. 已确认（CONFIRMED）

来自论文官方开放页面/正文：

| Item | Status | Notes |
|---|---|---|
| 4-DOF ball-bearing dynamic model | CONFIRMED | 论文 Sec. 3.1 |
| Hertzian contact theory | CONFIRMED | 论文 Sec. 3.1 |
| Time-varying contact stiffness route | CONFIRMED | adapted from Luo et al. |
| Inner/outer ring x-y dynamics | CONFIRMED | (x_i,y_i,x_o,y_o) |
| Support mass/stiffness/damping terms | CONFIRMED | Eq. (5) description |
| Radial force, eccentricity, speed, gravity | CONFIRMED | Eq. (5) description |
| Simulation pretraining | CONFIRMED | simulated vibration → pretrained network |
| Physics-guided knowledge loss | CONFIRMED | proposed method |
| Global + fine-grained class-level alignment | CONFIRMED | proposed multi-adversarial framework |
| Paderborn + HUST public datasets | CONFIRMED | experiments |
| Paper averages ≈ 88.15%, 96.74% | CONFIRMED | abstract |
| Inner-race simulation characteristic frequency 123.24 Hz | CONFIRMED | Eq. (6) / Fig. 5 discussion |
| Feature extractor = 4 convolutional layers + BN + CBAM | CONFIRMED | Sec. 3.5 / Table 9 |
| Feature dimension = 128 | CONFIRMED | Table 9 |
| Label predictor = 128→3 (PU), 128→7 (HUST) | CONFIRMED | Table 9 |
| Discriminator = 128→64→1 | CONFIRMED | Table 9 |
| Conv activation = Leaky ReLU | CONFIRMED | Table 9 |
| Optimizer = SGD, learning rate 1e-4 | CONFIRMED | Table 9 |
| Batch size = 16, iterations = 100 | CONFIRMED | Table 9 |
| Loss weights λm/λt/λk = 1.0/0.05/10.0 | CONFIRMED | Table 9 |
| Repetitions = 10 | CONFIRMED | Table 9 |
| Knowledge loss uses MK-MMD | CONFIRMED | Sec. 3.2–3.4 |
| PU Setting 0/1/2/3 conditions | CONFIRMED | Table 3 / Table 8 |
| No confirmed official GitHub | CONFIRMED AS SEARCH STATUS | repository audit |

## B. 6203 geometry（正文级已记录）

| Parameter | Value | Status |
|---|---:|---|
| outer diameter | 40 mm | CONFIRMED |
| inner diameter | 17 mm | CONFIRMED |
| width | 12 mm | CONFIRMED |
| ball diameter | 6.75 mm | CONFIRMED |
| pitch diameter | 28.5 mm | CONFIRMED |
| ball count | 8 | CONFIRMED |
| contact angle | 0 deg | CONFIRMED |

## C. 当前未完全核实，因此只能 INFERRED

以下值**不能**宣称为论文原值：

- inner/outer ring effective mass
- support stiffness (k_{ix},k_{iy},k_{ox},k_{oy})
- support damping
- Hertz coefficient numerical value
- bearing clearance exact numerical value
- eccentricity exact numerical value
- defect depth / angular width
- numerical integrator and tolerances（若正文后续未核到）
- exact sample window length
- exact convolution channel counts / kernel sizes shown only graphically in Fig. 7/9
- exact input representation dimensionality used by the final network
- MK-MMD kernel bandwidths

这些参数当前只用于让代码结构可运行。

## D. 方程实现注意

论文官方页面的 Eq. (5) 网页抓取存在排版异常：部分 y/x 方程的二阶导符号在 HTML 抽取中可能丢失。

因此代码采用**物理一致的二阶 4-DOF ODE**：

[
Mddot q + Cdot q + Kq = F_{contact}+F_{external}
]

而不是机械复制网页中可能损坏的 HTML 文本。

状态：**REFERENCED / physically reconstructed**。

## E. 已发现的原文歧义

Table 1 中 6203 的 “Bearing Speed” 与 Eq. (6)/PU Setting 0 的约 1500 rpm 语境存在单位或录入层面的不一致。当前：
- characteristic-frequency validation 以 Eq. (6) 的 **123.24 Hz** 为 paper reference；
- PU transfer condition 以 Table 3 的 **1500 rpm** 为准；
- 不用 Table 1 的 speed 字段覆盖实验工况。

## F. Reproduction-derived evidence

以下不是论文事实，而是当前代码的验收结果：

- 当前 6203 + 1500 rpm config 独立计算 BPFI = **123.6842 Hz**；
- 论文 Fig.5 reference = **123.24 Hz**，二者差约 0.36%；
- 当前 inner simulation raw-spectrum interpolated peak = **123.561 Hz**；
- envelope audit peak = **123.650 Hz**；
- 900 rpm 时 envelope peak = **74.200 Hz**，与 1500 rpm 峰值比约 0.60008；
- 初始 outer angle 270 deg 落在当前坐标系非承载区，outer simulation 与 normal 相同；
- outer angle 90 deg（INFERRED loaded-zone center）后，envelope peak = **76.304 Hz**，接近理论 BPFO 76.3158 Hz；
- integration max step 从 1/(4fs) 放宽到 1/fs 时，0.1 s inner waveform correlation = **0.9999999988**，relative RMSE/std = **4.93e-5**。

详见：
[reports/R1_R2_SIGNAL_VALIDATION_20260909.md](reports/R1_R2_SIGNAL_VALIDATION_20260909.md)

## G. Dual-impulse reconstruction evidence

The 2025 paper attributes the localized-spall response to the Luo et al. dynamics line. The accessible referenced literature distinguishes:
- entry into the spall: lower-frequency step-type response;
- collision with the trailing edge: higher-frequency transient response.

Reproduction result with half-cosine spall displacement + explicit exit collision:
- theoretical DITS = 1.078014 ms;
- detected median DITS = 1.093750 ms;
- DITS error = 1.460%;
- median exit/entry HF peak ratio = 1.785;
- median exit/entry HF RMS ratio = 1.310;
- envelope BPFI error = 0.242%;
- disabling the exit collision reduces median HF peak ratio to 0.870.

The numerical collision amplitude/duration remain INFERRED and are not claimed as paper parameters.

Audit:
[artifacts/audit_snapshots/20260909_dual_impulse_r2/README.md](artifacts/audit_snapshots/20260909_dual_impulse_r2/README.md)

## H. Input preprocessing audit

Open-full-text review confirms simulated vibration data + CNN pretraining, but does not provide a reproducible specification of window length, stride, normalization, raw-1D/reshaped-2D/time-frequency input, or input tensor dimensions.

See:
[PREPROCESSING_AUDIT.md](PREPROCESSING_AUDIT.md)

## I. 下一步证据补齐

优先继续核对：

1. localized spall “dual-impulse” 的精确几何/接触函数；
2. 论文未公开的有效质量、支承刚度/阻尼、Hertz coefficient 等 simulator 数值；
3. Fig. 7/9 中卷积核与通道数；
4. exact input representation / preprocessing；
5. Paderborn Table 6 的具体 bearing IDs；
6. HUST Table 7 的具体 source/target sample composition。

任何补齐后必须把本文件对应项从 INFERRED 改为 CONFIRMED，并记录来源。
