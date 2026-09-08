# Bearing-DT

轴承数字孪生（Digital Twin, DT）故障诊断论文知识库。

本仓库服务于后续 **bearing fault diagnosis × physics/digital twin × sim-to-real × knowledge distillation** 研究，不上传受版权保护的论文 PDF；保存 DOI/官方页面、结构化深读笔记、建模方法、代码开源状态和对后续研究的启发。

## 当前关注问题

我们特别关心一个区别：

- **Signal-faithful twin**：尽量让模拟信号接近真实信号；
- **Full-physics twin**：显式建模轴承、支撑、壳体、传递路径等；
- **Mechanism-only twin / physics teacher**：只保留故障机理及必要 causal context，尽量不引入 bearing ID / machine ID / sensor / transfer-path 等 nuisance cues。

核心科学问题：

> Which information in a digital twin should be transferred to a bearing diagnostic model?

## 核心论文索引

> 期刊分区会随年份/学科变化；这里优先收录 MSSP、KBS、IEEE TASE/TIM、Measurement 等高水平期刊，并额外保留与“physics teacher”高度相关的工作。

| 年份 | 论文 | 期刊 | DT 主线 | 代码状态 | 深读 |
|---|---|---|---|---|---|
| 2022 | [Digital Twin for rolling bearings: A review of current simulation and PHM techniques](papers/2022_Peng_Measurement_Review.md) | Measurement | 综述：检测/建模/PHM | 未发现官方代码 | B |
| 2023 | [Digital twin-assisted enhanced meta-transfer learning for rolling bearing fault diagnosis](papers/2023_Ma_MSSP_EMTL.md) | MSSP | FE/多学科试验台 DT + EMTL | 未发现官方代码 | **A** |
| 2023 | [A novel digital twin model for dynamical updating and real-time mapping of local defect extension](papers/2023_Shi_MSSP_DefectExtension.md) | MSSP | 缺陷扩展 + 动态更新 | 未发现官方代码 | B |
| 2023 | [Research on rolling bearing virtual-real fusion life prediction with digital twin](papers/2023_Zhao_MSSP_VirtualRealRUL.md) | MSSP | 全寿命模拟 + CycleGAN | 未发现官方代码 | B+ |
| 2023 | [A Digital Twin Model of Life-Cycle Rolling Bearing With Multiscale Fault Evolution](papers/2023_Li_TIM_MultiscaleEvolution.md) | IEEE TIM | 微观裂纹→剥落→宏观缺陷 | 未发现官方代码 | B |
| 2024 | [Inverse physics-informed neural networks for digital twin-based bearing fault diagnosis under imbalanced samples](papers/2024_Qin_KBS_InversePINN.md) | Knowledge-Based Systems | inverse PINN 参数辨识 + 数据生成 | 未发现官方代码 | B+ |
| 2024 | [Digital twin-assisted dual transfer: A novel information-model adaptation method for rolling bearing fault diagnosis](deep_readings/03_2024_Li_InformationFusion_Dual_Transfer.md) | Information Fusion | DT 信息迁移 + 模型迁移 | 未发现官方代码 | **精读** |
| 2025 | [A digital twin-enabled domain adaptation network for cross-space fault diagnosis of roller bearings](papers/2025_Fang_MSSP_DTDA.md) | MSSP | 多体动力学 + Sim2Real DA | 未发现官方代码 | B+ |
| 2025 | [Failure mechanism-driven multi-adversarial domain transfer learning for rolling bearing fault diagnosis](papers/2025_Cui_RIE_PhysicsTeacher.md) | Results in Engineering | **4-DOF physics teacher + KD** | 未发现官方代码 | **A** |
| 2026 | [Elevating Interpretability in Bearing Fault Diagnosis: A Knowledge Distillation Framework Integrating Dynamic and Causal a Priori](papers/2026_Ding_TASE_DynamicCausalKD.md) | IEEE TASE | **dynamic prior + causal prior + KD** | 未发现官方代码 | B |
| 2026 | [A digital twin guided physical-virtual denoising method for early fault detection](papers/2026_Qiao_MSSP_Denoising.md) | MSSP | DT 高保真模拟 + DeWGAN-GP | 未发现官方代码 | B |
| 2026 | [Digital twin-enhanced framework for rolling bearings fault diagnosis under imbalanced and open-set conditions](papers/2026_Ming_MSSP_OpenSet.md) | MSSP | DT augmentation + open-set | 未发现官方代码 | B |
| 2026 | [A method for discontinuous data repair and precise health monitoring integrating particle filtering and digital twin](papers/2026_Shi_MSSP_DataRepair.md) | MSSP | 动力学 + PF + TCW-GAN | 未发现官方代码 | B |

### 深读等级

- **A**：已获得可检索的正文级方法信息，能够记录方程/参数/实验/损失或完整 pipeline。
- **B+**：官方摘要、方法段/机构 manuscript 信息足以还原主要技术路线，但仍有细节需要全文再次核查。
- **B**：已核对官方摘要、highlights、论文元数据和相关作者/机构页面；暂不把无法核实的细节写成事实。

## 精读入口

- [第一批高优先级论文精读](deep_readings/README.md)

## 横向资料

- [DT 建模路线矩阵](docs/MODELING_MATRIX.md)
- [代码开源审计](docs/CODE_AVAILABILITY.md)
- [阅读与证据标准](docs/READING_POLICY.md)
- [与 Mechanism-only Teacher 的关系](docs/MECHANISM_ONLY_TEACHER.md)

## 仓库原则

1. 不把“模拟数据生成”自动等同于高保真数字孪生。
2. 明确区分 **mechanism fidelity**、**signal fidelity** 与 **diagnostic transferability**。
3. 对每篇论文记录：物理模型、参数来源、缺陷建模、Twin 输出、虚实校准、下游网络、实验协议、局限。
4. 代码只有在确认是作者/官方团队仓库时才标记为“官方开源”；第三方实现单独列出。
5. 后续若实现论文模型，新增 `implementations/`，不直接修改论文笔记中的事实记录。
