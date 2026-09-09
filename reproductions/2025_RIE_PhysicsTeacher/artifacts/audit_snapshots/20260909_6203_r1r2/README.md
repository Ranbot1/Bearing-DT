# 6203 Twin 信号审计快照 — 2026-09-09

本目录保存用于 R1/R2 物理验收的**代码生成并实际留存**的审计产物。

## Git 中实际保留了什么

### 生成的 Twin 数据

- `data/signals_1khz/part_01.csv ... part_07.csv`
  - 完整保留 0.05 s 到 0.35 s 的稳定区间；
  - 包含 normal / inner / outer 三类信号；
  - 从原始 64 kHz 模拟信号经过抗混叠降采样到 1 kHz；
  - 足以独立检查 BPFO/BPFI 尺度的周期性证据。
- `data/signals_64khz_excerpt_1ms.csv`
  - 保留原始 **64 kHz** 采样网格上的 1 ms 片段；
  - 用于直接检查未降采样的原始模拟波形数值。

### 信号处理数据

- `tables/characteristic_frequencies.csv`
  - 理论 shaft / BPFI / BPFO / BSF / FTF 频率。
- `tables/class_metrics.csv`
  - 波形统计量、raw-spectrum 目标峰、envelope-spectrum 目标峰以及故障频带能量。
- `tables/spectra_fault_band_60_140hz.csv`
  - 同时覆盖 BPFO 与 BPFI 邻域的精确 raw/envelope 频谱数值。

### 代码生成的图

- `figures/inner_time_domain.svg`
- `figures/inner_raw_spectrum.svg`
- `figures/inner_envelope_spectrum.svg`
- `figures/class_envelope_comparison.svg`

这些 SVG 均由同一次留存的模拟运行通过代码生成，不是外部额外制作的图片。

## 固定快照中的关键审计数值

| 指标 | 数值 |
|---|---:|
| 理论 BPFI | 123.6842 Hz |
| inner raw-spectrum 局部峰 | 125.4680 Hz |
| inner raw 误差 | 1.442% |
| inner envelope 峰 | 123.7564 Hz |
| inner envelope 误差 | **0.058%** |
| 理论 BPFO | 76.3158 Hz |
| outer raw-spectrum 局部峰 | 76.6760 Hz |
| outer raw 误差 | 0.472% |
| outer envelope 峰 | 76.2874 Hz |
| outer envelope 误差 | **0.037%** |

这个固定快照比主 R1/R2 长时验收运行更短，因此频率分辨率更粗，inner raw-spectrum 的峰值误差也更大；但 envelope-spectrum 的机制检查仍然与理论值高度一致。

## 来源与可追溯性

- `config_snapshot.yaml`：复制到快照中的 simulator 配置。
- `audit_runtime_overrides.json`：短时审计运行的覆盖参数。
- `manifest.json`：留存文件的 SHA-256，以及同一运行中生成的全分辨率 NPZ 文件哈希。

完整 64 kHz NPZ 数组由 `scripts/06_build_audit_snapshot.py` 在本地重新生成。Git 中保留完整 0.30 s、1 kHz 的机制频带信号以及 64 kHz 原始片段，使仓库可以直接审计，同时避免把 Git 历史变成大体积二进制数据仓库。

## 局限

等效质量、刚度、阻尼、Hertz coefficient、clearance 和 defect dimensions 仍然属于 `INFERRED`。

因此该快照验证的是**机制级信号行为**，不是与真实物理试验台进行 high-fidelity waveform matching。
