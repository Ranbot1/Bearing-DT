# 论文复现区

本目录只用于**论文复现（reproduction）**，与后续原创研究严格分离。

## 目录规范

每篇论文建立独立目录：

```
reproductions/
  YYYY_JOURNAL_SHORTNAME/
    README.md
    REPRODUCTION_CONTRACT.md
    ACCEPTANCE_CRITERIA.md
    EVIDENCE_LEDGER.md
    configs/
    src/
    scripts/
    tests/
    results/
```

## 复现原则

1. **Paper-faithful first**：先复现论文方法，再做任何改造。
2. **Confirmed / Inferred 分离**：论文未明确给出的参数不能伪装成原文参数。
3. **No silent tuning**：为得到更好结果而调整参数，必须记录。
4. **No data leakage**：数据划分、标准化、窗口重叠都必须可审计。
5. **Reproduction ≠ extension**：任何纠错、改进、严格协议都放到后续 `extensions/`。
6. **可执行优先**：每篇复现都应有 smoke test、配置文件、固定随机种子和结果目录。
