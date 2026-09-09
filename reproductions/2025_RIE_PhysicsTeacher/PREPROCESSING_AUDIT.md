# 输入与预处理审计 — 2026-09-09

论文：**Failure mechanism-driven multi-adversarial domain transfer learning for rolling bearing fault diagnosis**  
DOI：10.1016/j.rineng.2025.106165

## 开放全文中已经确认的信息

- 预训练模型是使用**模拟轴承振动数据**训练的深度 CNN。
- 预训练特征提取器与迁移网络的特征提取器有意保持相似。
- 所提出的共享特征提取器包含 **4 个卷积层 + BN + CBAM**。
- 论文与一个名为 **CNN2d** 的 baseline 进行比较。
- 论文给出了训练超参数，包括 SGD、学习率、batch size、iterations 和 loss weights。

## 当前可访问全文中没有找到的信息

开放正文**没有**给出以下内容的可复现规格：

- 模拟信号的精确 window length；
- overlap / stride；
- normalization 公式；
- 所提网络是否直接接收 raw 1-D vibration；
- 是否将振动信号 reshape 成 2-D array；
- 是否使用 STFT / CWT / envelope / time-frequency image；
- Conv1 之前 input tensor 的精确维度。

论文引言只是在一般性背景中说明，深度网络可以从 raw vibration signals **或简单变换**中学习，这不能作为本文具体方法的 preprocessing specification。

同样，存在一个名为 CNN2d 的对比 baseline，也不足以证明所提方法采用了哪一种精确输入变换。

## 复现决策

在获得更强证据之前：

1. 保留 raw 64-kHz simulated windows，作为 Teacher pilot 的规范数据；
2. 不把任何 1-D / 2-D transformation 标记为 PAPER-CONFIRMED；
3. 对 **paper-faithful** 路线继续阻止 Teacher pretraining；
4. 如果后续确实需要 fallback，则必须放在名称明确的 reproduction fallback config 中，并比较不同方案，不能静默选择某一种预处理。

当前状态：**UNRESOLVED，但边界已明确记录。**
