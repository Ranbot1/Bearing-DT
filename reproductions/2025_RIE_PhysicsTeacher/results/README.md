# 结果目录

本目录只保存**可再生成的小型结果与报告**。

大文件、模型权重和原始数据默认不直接提交 Git；需要长期留存的可核验数据应进入 `artifacts/`，并配套 manifest 与 SHA-256。

建议每次运行采用如下结构：

```text
results/
  YYYYMMDD_HHMM_<stage>/
    config.yaml
    metrics.json
    figures/
    notes.md
```

任何用于论文级比较的 run 都必须保存：

- 精确 config；
- Git commit SHA；
- random seed；
- dataset manifest hash；
- metrics；
- 尚未解决的 warning / difference。
