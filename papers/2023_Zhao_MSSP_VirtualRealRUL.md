# Zhao et al. 2023 — Research on rolling bearing virtual-real fusion life prediction with digital twin

- Journal: **Mechanical Systems and Signal Processing**, 198, 110434
- DOI: https://doi.org/10.1016/j.ymssp.2023.110434
- Reading status: **B+**
- Official code: **未发现**
- Accepted manuscript: University of Huddersfield research portal lists an accepted manuscript.

## 研究问题

全寿命真实故障样本少，导致 RUL 模型难训练。作者利用 DT 生成独立的 virtual life-cycle data，再把虚拟域映射到真实域。

## 核心 pipeline

[
life-cycle simulation
ightarrow x_{virtual}
ightarrow Modified CycleGAN + Wasserstein
ightarrow x_{physical-like}
ightarrow RUL
]

关键点不是简单 augmentation，而是**virtual-real distribution mapping**。

## 创新点

1. DT 生成大规模全寿命 simulation samples；
2. 修改 CycleGAN 并引入 Wasserstein distance，减少 simulation/measurement discrepancy；
3. 把融合后的大量样本用于多个 RUL predictor，以解决 small-sample life prediction。

## 对我们的启发

这是非常典型的 **“让虚拟信号越来越像真实信号”** 路线，可以作为我们 Signal-faithful Twin 的代表。

它也提出我们要验证的反问题：

> 若目标从 RUL 换成 unseen-bearing fault classification，virtual-to-real mapping 是否会把 machine/background style 一并注入？

## 复现难点

主要不是 GAN，而是 life-cycle physical simulator 的可信性与训练数据配对/非配对设计。我们当前分类工作不建议先从这条路线起步。
