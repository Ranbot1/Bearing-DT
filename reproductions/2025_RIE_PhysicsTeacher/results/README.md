# Results

本目录只保存可再生成的小型结果与报告。

大文件、模型权重、原始数据不提交 Git。

建议每次运行：

```
results/
  YYYYMMDD_HHMM_<stage>/
    config.yaml
    metrics.json
    figures/
    notes.md
```

任何用于论文级比较的 run 必须保存：
- exact config
- git commit SHA
- random seed
- dataset manifest hash
- metrics
- unresolved warnings
