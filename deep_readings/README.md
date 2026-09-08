# 轴承数字孪生论文精读

本目录只放**对当前研究路线最重要、值得反复回看的精读文件**。与 \`papers/\` 的区别：

- \`papers/\`：全库结构化论文卡片，覆盖面优先；
- \`deep_readings/\`：正文级拆方法、实验和可复现风险，强调“我们后续怎么用”。

## 第一批优先级

| 优先级 | 论文 | 为什么先读 |
|---|---|---|
| P0 | [Ding et al., 2026, IEEE TASE](01_2026_Ding_TASE_Dynamic_Causal_KD.md) | 与“physics teacher + 抑制混杂”最直接竞争 |
| P0 | [Zhang et al., 2025, Results in Engineering](02_2025_Zhang_RIE_Physics_Teacher.md) | 已明确做“动力学仿真 → Teacher → Student KD” |
| P0 | [Li et al., 2024, Information Fusion](03_2024_Li_InformationFusion_Dual_Transfer.md) | 顶刊，直接研究“DT 信息迁移 + 模型迁移” |
| P1 | [Fang et al., 2025, MSSP](04_2025_Fang_MSSP_CrossSpace_DTDA.md) | 代表高质量 multibody DT → physical Sim2Real |
| P1 | [Ma et al., 2023, MSSP](05_2023_Ma_MSSP_HighFidelity_EMTL.md) | 代表“高保真试验台 Twin”的建模上限 |

## 当前研究判断

第一批精读后，已经可以明确：

1. **“物理模型生成故障信号作为 Teacher”不是空白。**
2. **“用因果先验减少 confounder”也已经有人明确提出。**
3. 仍值得研究的是：  
   **Teacher 本身应该被允许知道哪些信息？提高 twin fidelity 是否一定提高 unseen-bearing / cross-machine generalization？**
4. 需要把问题从“有没有 physics teacher”改成：
   > **Does increasing digital-twin fidelity improve transferable fault knowledge, or transfer more machine-specific shortcuts?**

## 证据规则

每篇精读文件都区分：
- 论文正文/官方页面已确认；
- 公开 preview 能确认；
- 由同团队专利/前置工作辅助重建但尚未从论文全文逐字核实。

不把后两类写成“论文原文事实”。
