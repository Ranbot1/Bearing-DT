# 2025 Results in Engineering — Physics-Teacher 复现

## 论文

**Failure mechanism-driven multi-adversarial domain transfer learning for rolling bearing fault diagnosis**

- 期刊：Results in Engineering, 27 (2025), 106165
- DOI：https://doi.org/10.1016/j.rineng.2025.106165
- 官方代码：**截至 2026-09-09 未发现**
- 当前复现状态：**PHYSICS_REPRODUCED — R1/R2 机制级关口已通过；Teacher 数据集 pilot 已通过**

## 为什么第一篇复现它

这篇与当前轴承 DT 研究库中“动力学仿真数据作为 physics teacher，指导真实诊断模型”的路线最直接相关，同时工程门槛明显低于 FE / ADAMS / multibody high-fidelity twin。

论文主链：

```text
4-DOF 轴承动力学
        ↓
模拟故障振动
        ↓
预训练 physics teacher
        ↓
知识约束
        +
多对抗域迁移
        ↓
真实轴承故障诊断
```

## 当前复现范围

### 已实现

- [x] 标准化复现目录
- [x] 论文证据台账
- [x] 验收标准
- [x] 4-DOF ball-bearing dynamics 基础实现
- [x] Hertz nonlinear contact
- [x] inner / outer localized defect geometry hook
- [x] bearing characteristic frequencies
- [x] simulator smoke tests
- [x] normal / inner / outer 虚拟数据生成器
- [x] 面向论文 Fig. 5 的时域/频域评估器
- [x] R1 inner BPFI + speed-scaling validation
- [x] 发现并修正 outer load-zone 配置错误
- [x] dual-impulse DITS + trailing-edge collision mechanism validation
- [x] no-exit-impact negative control
- [x] run-isolated PU Teacher pilot 数据集构造
- [x] train / val / test raw-window 审计数据留存
- [x] Teacher / domain-transfer 网络接口骨架

### 尚未宣称完成

- [x] Fig. 5 核心 inner-race frequency-domain mechanism evidence
- [x] R2 dual-impulse mechanism gate
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

## 目录结构

```text
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
  06_build_audit_snapshot.py
  07_validate_dual_impulse.py
  08_build_teacher_dataset.py

tests/
  test_characteristic_frequencies.py
  test_simulator_smoke.py
  test_dual_impulse_kinematics.py

reports/
  R1_R2_SIGNAL_VALIDATION_20260909.md

results/
  README.md
```

## 最重要的约束

当前版本中，**论文没有公开或尚未核实的动力学参数一律标记为 INFERRED**。因此当前 simulator 首先是“方程结构复现 + 物理 sanity check”，不是已经验收的 paper-level numerical reproduction。

当前 R1/R2 报告与审计入口：

- [R1/R2 信号验收报告](reports/R1_R2_SIGNAL_VALIDATION_20260909.md)
- [Dual-impulse R2 审计](artifacts/audit_snapshots/20260909_dual_impulse_r2/README.md)
- [PU Teacher pilot v1](artifacts/teacher_pilots/pu_6203_teacher_pilot_v1/README.md)
- [输入与预处理审计](PREPROCESSING_AUDIT.md)

可直接核验的代码生成产物：

- [20260909_6203_r1r2 审计快照](artifacts/audit_snapshots/20260909_6203_r1r2/README.md)
  - 生成的信号检查点；
  - 完整 0–500 Hz 频谱表；
  - 各类别指标；
  - 代码生成 SVG 图；
  - config + SHA-256 provenance。

相关规范：

- [复现契约](REPRODUCTION_CONTRACT.md)
- [验收标准](ACCEPTANCE_CRITERIA.md)
- [证据台账](EVIDENCE_LEDGER.md)
