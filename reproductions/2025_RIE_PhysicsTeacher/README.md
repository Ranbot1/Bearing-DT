# 2025 Results in Engineering — Physics-Teacher Reproduction

## Paper

**Failure mechanism-driven multi-adversarial domain transfer learning for rolling bearing fault diagnosis**

- Journal: Results in Engineering, 27 (2025), 106165
- DOI: https://doi.org/10.1016/j.rineng.2025.106165
- Official code: **截至 2026-09-09 未发现**
- Reproduction status: **Stage R0/R1 — repository + 4-DOF simulator implementation**

## 为什么第一篇复现它

这篇与当前轴承 DT 研究库中“动力学仿真数据作为 physics teacher，指导真实诊断模型”的路线最直接相关，同时工程门槛明显低于 FE / ADAMS / multibody high-fidelity twin。

论文主链：

```
4-DOF bearing dynamics
        ↓
simulated fault vibration
        ↓
pretrained physics teacher
        ↓
knowledge constraint
        +
multi-adversarial domain transfer
        ↓
real bearing diagnosis
```

## 当前复现范围

### 已开始实现

- [x] 标准化复现目录
- [x] 论文证据台账
- [x] 验收标准
- [x] 4-DOF ball-bearing dynamics 基础实现
- [x] Hertz nonlinear contact
- [x] inner / outer localized defect geometry hook
- [x] bearing characteristic frequencies
- [x] simulator smoke tests
- [x] normal / inner / outer virtual-data generator
- [x] paper-oriented time/frequency-domain evaluator
- [x] R1 inner BPFI + speed-scaling validation
- [x] outer load-zone configuration failure discovered and corrected
- [x] Teacher / domain-transfer 网络接口骨架

### 尚未宣称完成

- [x] Fig.5 核心 inner-race frequency-domain mechanism evidence（R2 partial）
- [ ] Paderborn transfer task 完整复现
- [ ] HUST transfer task 完整复现
- [ ] physics-teacher pretraining result
- [ ] multi-adversarial transfer result
- [ ] 88.15% / 96.74% paper-level performance reproduction

## 快速开始

```bash
cd reproductions/2025_RIE_PhysicsTeacher
python -m pip install -e ".[dev]"
pytest -q
python scripts/01_validate_simulator.py --config configs/paper_6203.yaml
```

## 目录

```
configs/
  paper_6203.yaml

src/fmdtl/
  config.py
  sim/bearing_4dof.py
  models.py
  losses.py

scripts/
  01_validate_simulator.py
  02_pretrain_teacher.py
  03_train_transfer.py
  04_generate_twin_dataset.py
  05_evaluate_paper_signal.py

tests/
  test_characteristic_frequencies.py
  test_simulator_smoke.py

reports/
  R1_R2_SIGNAL_VALIDATION_20260909.md

results/
  README.md
```

## 最重要的约束

当前版本中，**论文没有公开或尚未核实的动力学参数一律标记为 INFERRED**。因此当前 simulator 首先是“方程结构复现 + 物理 sanity check”，不是已经验收的 paper-level numerical reproduction。

当前 R1/R2 报告：
- [R1_R2_SIGNAL_VALIDATION_20260909.md](reports/R1_R2_SIGNAL_VALIDATION_20260909.md)

可直接核验的代码生成产物：
- [20260909_6203_r1r2 audit snapshot](artifacts/audit_snapshots/20260909_6203_r1r2/README.md)
  - generated signal checkpoints
  - full 0–500 Hz spectral table
  - per-class metrics
  - generated SVG figure
  - config + SHA-256 provenance

见：
- [REPRODUCTION_CONTRACT.md](REPRODUCTION_CONTRACT.md)
- [ACCEPTANCE_CRITERIA.md](ACCEPTANCE_CRITERIA.md)
- [EVIDENCE_LEDGER.md](EVIDENCE_LEDGER.md)
