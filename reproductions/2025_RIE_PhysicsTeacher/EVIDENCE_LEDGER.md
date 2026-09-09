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
- exact optimizer / LR / batch size
- all loss weights

这些参数当前只用于让代码结构可运行。

## D. 方程实现注意

论文官方页面的 Eq. (5) 网页抓取存在排版异常：部分 y/x 方程的二阶导符号在 HTML 抽取中可能丢失。

因此代码采用**物理一致的二阶 4-DOF ODE**：

[
Mddot q + Cdot q + Kq = F_{contact}+F_{external}
]

而不是机械复制网页中可能损坏的 HTML 文本。

状态：**REFERENCED / physically reconstructed**。

## E. 下一步证据补齐

优先继续核对：

1. Eq. (6–8) 接触变形与 localized defect 的精确写法；
2. 论文 simulator 参数表；
3. network layer table；
4. knowledge loss exact equation；
5. Paderborn transfer task definitions；
6. HUST task definitions；
7. optimizer / loss weights。

任何补齐后必须把本文件对应项从 INFERRED 改为 CONFIRMED，并记录来源。
