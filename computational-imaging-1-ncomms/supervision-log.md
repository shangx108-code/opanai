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

## 监督轮次 6
- 日期：2026-04-26
- 节点性质：线性 round3 / round4 本地 rebuild 工件恢复

## 当前版本总体评价
这一轮解决的是一个很实际的问题：项目记忆里写过 round3 / round4，但当前工作区并没有本地脚本和输出。现在这两轮至少重新在本地落地了，虽然它们是 rebuild 版本，不是历史原件的逐字恢复，但已经足以作为下一轮继续统一线性指标和衔接 phase 链的现场起点。

## 本轮已真实完成
- 已新增并运行 `round3_linear_autoencoder_prior.py`。
- 已生成 `round3_outputs/round3_summary.json`、`round3_case_metrics.csv` 和 `round3_linear_autoencoder_panel.png`。
- 已新增并运行 `round4_linear_measurement_consistent_prior.py`。
- 已生成 `round4_outputs/round4_summary.json`、`round4_case_metrics.csv`、`round4_linear_measurement_consistent_panel.png` 和 `round4_linear_measurement_mask.png`。

## 本轮关键结论
- rebuilt round3 的 autoencoder projection 在 6 个样例上平均 `bridge_mean_intensity = 0.7947`，说明 nonlinear learned prior 在当前 benchmark 中仍会明显填充未观测桥接区。
- rebuilt round4 的 latent inverse 平均 `bridge_mean_intensity = 0.7102`，说明 measurement-consistent latent optimization 也没有自动消除桥接结构。
- 但这些数值和记忆里早先登记的版本并不一致，因此必须明确区分“本地 rebuild 工件”和“历史原始工件”。

## 本轮未达标部分
- round3 / round4 目前只是 rebuild 工件，尚未和历史原始结果完成一一校核。
- phase 链仍缺当前工作区可复核的 solver 级 symmetry-enforced baseline。
- DSI / PDR / HCI 仍未达到论文级闭环。

## 必须纠正项
1. 下一轮先把 round5 的区域定义正式映射到 rebuilt round3 / round4 汇总结果。
2. 不得把 rebuilt round3 / round4 写成“原始工件已完全找回”。
3. 线性链补稳后，再把最高优先级切回 phase solver 级 symmetry-enforced 基线。
