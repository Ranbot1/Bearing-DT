# 代码开源审计

审计日期：2026-09-09。

## 核心论文

| 论文 | 官方代码 | 数据/补充材料 | 备注 |
|---|---|---|---|
| Ma 2023 MSSP, EMTL | **未发现** | 自建试验台 | 通过标题/DOI/作者/GitHub 检索均未发现作者仓库 |
| Shi 2023 MSSP, defect extension DT | **未发现** | XJTU-SY 公开数据 | 未发现官方实现 |
| Zhao 2023 MSSP, virtual-real RUL | **未发现** | PRONOSTIA/实验数据路线 | Huddersfield 有 accepted manuscript（已接受稿），但未发现代码 |
| Li 2023 IEEE TIM, multiscale evolution | **未发现** | — | 未发现官方实现 |
| Qin 2024 KBS, inverse PINN | **未发现** | 论文称真实数据参与参数辨识 | 未发现官方实现 |
| Li 2024 Information Fusion, DTa-DT | **未发现** | 两个公开 bearing datasets | 通过标题/方法名/作者/GitHub 检索未发现可确认官方仓库 |
| Fang 2025 MSSP, DTDA | **未发现** | 自建试验台/模拟数据 | 作者主页列有论文，但未链接代码 |
| Cui 2025 RIE, mechanism-driven transfer | **未发现** | 论文数据可用性：需向作者申请 | 开放全文未提供 GitHub 链接 |
| Ding 2026 IEEE TASE, dynamic+causal KD | **未发现** | — | 未发现官方仓库 |
| Qiao 2026 MSSP, DT-guided denoising | **未发现** | XJTU-SY 等 | 未发现官方仓库 |
| Ming 2026 MSSP, open-set DT | **未发现** | 自建/实机验证 | 未发现官方仓库 |
| Shi 2026 MSSP, PF+DT data repair | **未发现** | XJTU-SY + 自建 | 未发现官方仓库 |

## 相关开源项目（不是上述论文官方代码）

这些仓库只作为实现参考，**不能当作论文复现**：

- https://github.com/akshatverma1602/UKF-based-Digital-Twin-for-Rotor-Bearing  
  2-DOF Jeffcott rotor-bearing + UKF 在线估计 bearing stiffness/damping，适合理解“物理参数在线更新”的 DT。
- https://github.com/Avibest/digital_twin_project  
  NASA IMS + health indicators + Random Forest/Streamlit；更偏 data-driven monitoring，不是高保真 bearing dynamics DT。
- https://github.com/ruiliapt/traction-twin  
  含 bearing degradation 注入和 CWRU 接入的工程型 Twin demo；适合软件架构参考，不对应核心论文。

## 后续动作

若发现官方代码：

1. 先确认 GitHub owner 与作者/实验室身份；
2. 记录 commit/tag；
3. 在对应论文笔记增加“代码结构 → 论文模块”的映射；
4. 单独审查数据划分和潜在 leakage。
