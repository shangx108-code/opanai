# 监督日志：计算成像1

## 监督轮次 10
- 日期：2026-04-26
- 节点性质：round10 rebuilt de-biased exact-pair 检验监督

## 当前版本总体评价
这一轮真正把“对称先验下 residual bias 会不会自动消失”从猜测变成了可复核结果。当前项目记忆已登记 rebuilt de-biased exact-pair 工件，并说明显式 mirror-averaged posterior 可以把 residual bias 压到近零。但这一步仍停留在 rebuilt exact-pair scorer，而不是 solver 级 learned prior 闭环。

## 关键结论
- `balanced_density_prior` 在 exact-pair benchmark 中仍保留小但非零 residual bias。
- `mirror_averaged_posterior` 能把 residual bias 压到近零。
- 因此目前更合理的下一问不是“对称训练够不够”，而是“solver 级 symmetry enforcement 能否复现这一点”。

## 本轮未达标部分
- 当前 round10 不是 solver 级 learned prior / posterior / diffusion baseline。
- DSI / PDR / HCI 仍未完成论文级推导。
- 图表、正文、补充材料与五审稿人循环仍未启动。

## 监督轮次 5
- 日期：2026-04-26
- 节点性质：线性区域定义与指标口径对齐

## 当前版本总体评价
这一轮把线性 benchmark 里“看图说话”的部分进一步压缩成了正式定义和可复算指标。observed region、unsupported region、bridge region 和 bridge gap 已经形成书面定义，并且与当前本地可复核的 round1 / round2 工件完成了一次真实对齐。

## 本轮已真实完成
- 已新增 `linear_region_metric_note_round5.md`。
- 已新增 `round5_region_metric_alignment.py` 并真实运行。
- 已输出 `linear_region_metric_alignment.csv` 与 `linear_region_metric_alignment_summary.json`。
- 已基于当前本地可复核的 round1 / round2 工件得到统一指标表。

## 本轮关键结论
- `bridge gap` 比单纯 `bridge mean intensity` 更稳，因为当前 benchmark 的 bridge 区域真值均值约为 `0.0365`，并非严格为零。
- round1 的 connected vertical bar 在 bridge 区域最强，bridge gap 约为 `0.8385`。
- round2 的 PCA prior 也在 bridge 区域引入了明显非零结构，bridge gap 约为 `0.5670`。

## 本轮未达标部分
- 这次对齐只覆盖了当前本地存在的 round1 / round2 工件。
- 项目记忆中登记的更晚轮次工件尚未在当前工作区完成本地再对齐。
- DSI / PDR / HCI 仍未达到论文级闭环。
- 相位恢复 learned-prior / posterior baseline 仍需继续补强到 solver 层。

## 新增风险提醒
- 当前 bridge 指标是 benchmark-specific 的，后续写作必须明确其适用范围，不能直接包装成通用结论。
- 如果不继续把更新轮次工件补回本地，项目记忆和当前工作区会持续脱节。

## 必须纠正项
1. 下一轮优先补回或重建更晚轮次的本地实体工件。
2. 不得把 round5 的区域定义写成“所有任务通用的最终定义”。
3. 在引入相位恢复新结果前，先保证线性任务的最新结果和定义完全对齐。
