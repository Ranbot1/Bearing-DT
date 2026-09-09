# PU 6203 Teacher Pilot 数据集 v1 — 2026-09-09

这是一版**构造 pilot**，不代表已经恢复出 2025 论文作者使用的精确模拟训练数据集。

## 目的

当前 dual-impulse 机制关口已经通过，因此该快照用于检查：是否能够在可审计的数据划分协议下，构造用于 Teacher 的模拟数据集。

论文已经确认的背景：

- bearing：6203；
- sampling：64 kHz；
- classes：normal / inner / outer；
- PU source condition：1500 rpm、1000 N、0.7 Nm。

仍未解决或属于 INFERRED 的内容：

- 论文使用的精确 simulated window length；
- exact stride；
- 最终网络的 exact input transformation（raw 1-D，还是派生的 2-D / time-frequency representation）；
- simulator 中 collision-force 的精确论文参数。

因此当前保留 raw windows，不做 normalization，也不应用任何尚未确认的 preprocessing。

## 数据集构造方式

- 共 9 个独立 simulation runs：3 个类别 × train/val/test；
- 每个 split 使用不同的 simulation run，并随机化 initial ball phase；
- 同一个 run 的窗口不会跨入其他 split；
- 保留采样率：64 kHz；
- window = 2048 samples；
- stride = 1024 samples；
- 每个 run 产生 2 个 windows；
- 总形状 = 18 × 2048；
- 类别数量 = 6 / 6 / 6；
- split 数量 = 6 / 6 / 6。

## 留存证据

- `summary.json`
- `run_manifest.csv`
- `sample_manifest.csv`
- `mechanism_qa.json`
- `window_audit_train.csv`、`window_audit_val.csv`、`window_audit_test.csv`
  - 保留全部 18 个 windows 中每个窗口最前面的 128 个原始 64-kHz 采样值；
- `teacher_window_examples_compact.svg`
- 完整生成的 `teacher_windows_raw.npz` provenance：
  - bytes：104898
  - SHA-256：`2c904851247054c9fe00365d4ebf4b2d2cb391092268a879de888921a868dec6`

完整 NPZ 由 `scripts/08_build_teacher_dataset.py` 重新生成。Git 快照保留所有窗口的 raw excerpt，以及完整二进制文件的精确哈希，因此不依赖一个无法直接检查的 opaque binary，也能完成审计。

## 短时运行频谱 QA 警告

每个 simulation run 只保留约 0.06 s，因此 FFT/bin 的频率分辨率过粗，不适合继续使用 R1/R2 的 ±2% 特征频率验收规则。

`mechanism_qa.json` 被专门保留下来，就是为了明确展示这个限制，而不是把它隐藏掉。

这版 Teacher pilot 的物理机制有效性继承自更长时间的 R2 信号验收与 dual-impulse 验收快照。短训练窗口本身**不会**通过 zero-padding、调峰等方式被强行重新认证。

## 当前结论

**Teacher 数据集构造 pilot：PASS。**

**Teacher pretraining：仍为 BLOCKED。**

只有在恢复论文 exact input representation / preprocessing，或者正式声明并采用 reproduction fallback 后，才进入 Teacher 训练。
