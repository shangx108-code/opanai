# 审稿历史：计算成像1

## 当前状态
- 正式五位审稿人并行评审：尚未启动
- 原因：
  - 尚无可审稿的正文稿件
  - 尚无正式核心图与补充图
  - 尚无闭合理论推导与真实结果矩阵

## 预设审稿维度
未来正式审稿循环默认覆盖以下五类审稿视角：
1. 创新性与期刊匹配
2. 理论严谨性与机制解释
3. 方法、代码与数值流程可靠性
4. 结果充分性、图表质量与证据支撑
5. 写作质量、叙事逻辑与说服力

## 当前预审判断
- 不具备进入正式五审稿人评审的条件
- 当前综合状态更接近“研究提案 + 执行路线图”

## 进入正式审稿循环前的硬门槛
1. 至少一版完整 manuscript 草稿
2. 至少一版 supplementary 草稿
3. 正文和补充材料中的全部图完成到可审稿状态
4. 关键理论推导可检查
5. 关键代码路径真实跑通并可复核
6. 参考文献达到 30 篇以上

## 接收概率追踪规则
只有在正式五审稿人循环启动后，才记录每位审稿人的：
- 一句话总评
- 主要拒稿理由
- 必须修改项
- 可选增强项
- 接收概率区间
- 最终建议

## 当前结论
当前接收概率不能通过“审稿轮次”上调；在真实结果、图表和推导补齐前，任何乐观判断都不成立。

## 预审备注（第 1 轮结果后）
- 线性任务已有第一批 unsupported-structure 案例。
- 相位恢复已有严格的 measurement ambiguity 证据。
- 但由于当前 prior 仍是手工候选库而非真实深度先验，正式五审稿人循环仍不能启动。

## 预审备注（round3 学习型 prior 后）
- 线性任务已新增真实非线性学习型 autoencoder prior 结果，并形成 zero-fill / PCA / autoencoder 三方对照。
- autoencoder prior 在 6 个断裂目标上保持观测区误差为 0，但未观测区平均 MAE 上升到 `0.2356`，bridge mean intensity 为 `0.3417`，说明 learned prior 的 unsupported hallucination 现象确已进入训练型模型层面。
- 但该结果仍不等同于 DIP、diffusion prior、PnP 或 Bayesian posterior baseline，因此正式五审稿人循环仍不能启动。
- 当前最近的预审判断仍为：不具备进入正式五审稿人并行评审的条件。

## 预审备注（round4 measurement-consistent latent inverse 后）
- 线性任务已新增一类 measurement-consistent learned prior 逆问题基线，并形成 zero-fill / PCA / autoencoder projection / latent inverse 四方对照。
- latent inverse 在 6 个断裂目标上的聚合结果为：观测区 MAE `0.0000`，未观测区 MAE `0.4891`，bridge mean intensity `0.4964`。
- 该结果表明：即使在观测区严格一致的条件下，learned prior 仍可能在 bridge 区域生成 unsupported structure。
- 但由于当前指标尚未形式化、相位恢复 learned prior 尚未补齐、正文与补图体系仍缺失，正式五审稿人循环仍不能启动。
- 当前最近的预审判断仍为：不具备进入正式五审稿人并行评审的条件。

## 预审备注（线性区域定义与指标正式化后）
- 当前工作区已新增一套可复核的 round4 重现实验工件，并把 observed / unsupported / bridge 三类区域及其指标写成正式定义。
- 新重现实验在 6 个断裂目标上的聚合结果为：PCA prior 的 bridge mean intensity `0.5756`，autoencoder projection `0.9077`，latent inverse `0.9959`，而 zero-fill 为 `0.0000`；四个方法的 observed-region MAE 均为 `0.0000`。
- 该结果使线性 benchmark 首次具备“measurement consistency 与 unsupported bridge hallucination 可同时成立”的统一口径。
- 但由于相位恢复 learned prior / posterior baseline 仍缺失、DSI/PDR/HCI 仍未完成完整推导、正文与补图仍缺失，正式五审稿人循环仍不能启动。
- 当前最近的预审判断仍为：不具备进入正式五审稿人并行评审的条件。

## 预审备注（round5 相位恢复 learned-prior branch bias 后）
- 当前工作区已新增一套可复核的 round5 相位恢复工件，并首次把 true / reversed 精确 ambiguity 与 learned-prior branch selection 放到同一 measurement-error 口径下比较。
- round5 在 4 个 held-out 样例上的聚合结果为：true / reversed 的 measurement error `1.26e-16` 量级，learned prior 输出的平均 measurement error `2.52e-01`，到 true branch 的平均距离 `0.4380`，到 reversed branch 的平均距离 `1.2072`，mean branch bias `0.7692`，且 4 / 4 个样例均为正偏向。
- 该结果说明：相位恢复中的 learned prior branch selection 已从“纯存在性”推进到“真实经验结果”。
- 但由于当前 baseline 仍是 toy decoder prior、measurement error 仍不低、统一理论指标接口仍未完成、正文与补图仍缺失，正式五审稿人循环仍不能启动。
- 当前最近的预审判断仍为：不具备进入正式五审稿人并行评审的条件。
