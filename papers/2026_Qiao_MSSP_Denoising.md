# Qiao et al. 2026 — A digital twin guided physical-virtual denoising method for early fault detection of rolling element bearings

- 期刊：**Mechanical Systems and Signal Processing**, 249, 114108
- DOI：https://doi.org/10.1016/j.ymssp.2026.114108
- 阅读状态：**B**
- 官方代码：**未发现**

## 研究问题

早期 bearing fault signals 很弱、噪声强，普通 denoising 容易把真正的 fault impulses 一起去掉。

## 方法

论文建立 bearing digital twin model，用 physical parameters 生成 high-fidelity labeled simulated signals。

再设计 **DeWGAN-GP** 融合：

- simulated / virtual fault signal；
- measured noisy signal。

目的不是单纯分类，而是借助物理虚拟信号提供“故障应该长什么样”的干净物理参考，进行 physical-virtual denoising。

## 对我们的启发

这与 mechanism-only Teacher 的思想非常接近：

> virtual signal 可以充当“故障应该呈现什么证据”的物理参考。

但该论文目标是 early-fault denoising，而不是：

- unseen-bearing classification；
- shortcut suppression；
- Teacher-information boundary。

这篇应作为“physics reference signal”相关工作重点引用。
