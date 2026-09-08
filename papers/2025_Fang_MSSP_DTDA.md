# Fang et al. 2025 — A digital twin-enabled domain adaptation network for cross-space fault diagnosis of roller bearings

- Journal: **Mechanical Systems and Signal Processing**, 236, 113053
- DOI: https://doi.org/10.1016/j.ymssp.2025.113053
- Author page: https://faculty.csu.edu.cn/fangcongcong/
- Reading status: **B+**
- Official code: **未发现**
- Journal note: 作者主页将该论文标为 JCR Q1。

## 问题

真实工业 CRB labeled fault data 少；digital-space simulation 有标签，但与 physical-space measured data 存在 domain discrepancy。

## DT 物理建模

数字空间建立：
- **cylindrical roller bearing (CRB)**
- **support housing**
- Augmented Lagrange multibody dynamics
- Hertzian contact theory
- localized raceway defect analytical formulation
- cage pillar fracture model

Twin 输出的是对应 fault modes 的 **bearing pedestal vibration acceleration**，而不是只输出 characteristic frequency。

## Physical space

作者实际加工 defective roller bearings，并在 bearing test rig 采集 bearing pedestal vibration。

于是形成：

[
D_s = labeled digital vibration
]

[
D_t = unlabeled physical vibration
]

## 诊断网络

提出 **DJDA (dynamic joint distributed domain adaptation)**：

- global/marginal distribution alignment；
- class-wise/conditional distribution discrimination；
- 将 digital general fault knowledge 转移到 physical space。

最终：

[
Bearing DT + DJDA Rightarrow DTDA
]

## 创新点

1. 高复杂度 CRB fault dynamics + support housing；
2. raceway defect 与 cage-pillar fracture 都可模拟；
3. 明确把任务定义为 **cross-space diagnosis**；
4. 用 DA 而不是要求 simulator 完美复制实测分布。

## 对我们的启发

它是非常好的 **Full-physics / Sim2Real baseline**。

但它仍然默认：
> digital domain 提供越丰富、越接近真实系统的 dynamics 越好。

我们的研究可以进一步问：
> 对 classification 来说，support housing / path / machine dynamics 是否是应该 transfer 的“知识”，还是可能成为 nuisance？

## 复现难度

★★★★★。需要多体动力学、CRB 几何/接触模型和实体试验台才能严格复刻。
