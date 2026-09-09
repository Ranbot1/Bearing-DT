# 复现契约

## 1. 复现目标

本目录目标是复现论文：

> Failure mechanism-driven multi-adversarial domain transfer learning for rolling bearing fault diagnosis

而不是提前实现任何后续研究想法。

## 2. 三种证据等级

所有实现决策必须属于以下之一：

### CONFIRMED

可从论文正文或官方页面直接核实。

### REFERENCED

论文明确引用前人方法，但当前实现根据被引用方法进行重建；必须记录来源。

### INFERRED

论文没有提供足够信息，只能采用合理工程假设。

**禁止将 INFERRED 参数写成“论文参数（paper parameter）”。**

## 3. 允许的复现偏差

只有以下情况允许偏差：

- 原文没有给出参数；
- 原文描述存在歧义；
- 软件或数据不可获得；
- 为完成 smoke test 使用最小可运行默认值。

任何偏差都必须写入：
`EVIDENCE_LEDGER.md`

## 4. 禁止行为

- 不为了接近论文 accuracy 偷调 test set。
- 不使用 target test labels 选择超参数。
- 不把随机窗口泄漏当作正常复现细节。
- 不把我们自己的严格 bearing-isolated protocol 混入 paper-faithful baseline。
- 不使用未经确认的第三方代码并声称为官方实现。
- 不上传受版权保护的 PDF 或不可再分发数据。

## 5. 复现与扩展隔离

未来任何如下工作：

- bearing-ID audit
- unseen-bearing split
- mechanism-only teacher
- signal-faithful vs mechanism-faithful comparison
- shortcut intervention

都必须另放：

```text
extensions/
```

复现目录本身保持论文基线。
