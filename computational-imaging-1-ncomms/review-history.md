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

## 预审备注（状态核查与资料索引纠偏后）
- 本轮未新增新的理论推导、数值结果或正式图表，因此仍不具备进入正式五审稿人并行评审的条件。
- 新增的是一次真实性核查：当前工作区未找到项目状态中登记的 `/workspace/computational-imaging-1-ncomms/` round7-10 工件，当前命名空间内现场可读的技术文件只有 `phase-ambiguity-metrics-round6.md`。
- 环境方面，Python、`numpy`、`pandas`、`PIL`、PNG 生成和 `latexmk` PDF 编译链路已验证可用；但 `matplotlib` 缺失，Google Drive 检索权限不足，因此旧绘图脚本和长期资料归档都仍待恢复。
- 这意味着当前项目的预审主风险已从“solver 级去偏置实验还没做”进一步前移为“当前可运行工件与资料索引脱节”。在恢复本地或云端原始工件前，任何把 round7-10 写成“当前可现场复核”的表述都不成立。
- 因此，下一轮预审入口应优先检查：是否已恢复至少一套可运行 phase 工件，然后才讨论 solver 级 symmetry-enforced 机制闭环。

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

## 预审备注（round6 phase ambiguity 指标 formalization 后）
- 本轮未新增正式审稿材料，也未新增新的 phase 数值结果，因此仍不具备进入正式五审稿人并行评审的条件。
- 本轮新增的是一份指标边界说明：把 round5 的 `true_reversed_measurement_error` 定义为 exact ambiguity quantity，把 `recovered_measurement_error` 定义为 empirical measurement-consistency quantity，把 `distance_to_true`、`distance_to_reversed` 与 `branch_bias` 定义为 empirical branch-selection quantities。
- 该说明进一步明确：当前 `branch_bias = 0.7692` 只能写成“toy learned prior 的经验性 true-branch preference”，不能写成 phase retrieval ambiguity 的一般结论。
- 基于这一预审更新，下一轮更合理的推进路线是先把 phase baseline 变成更强、误差更低的 solver，再决定是否启动统一理论接口或更靠近正式审稿门槛。

## 预审备注（round7 rebuilt low-error phase solver 后）
- 当前工作区已新增一套可复核的 round7 rebuilt phase solver 工件，并首次在明显更低 measurement error 的条件下重新检查 branch selection。
- round7 在 4 个 held-out 样例上的聚合结果为：true / reversed 的 measurement error `1.39e-16` 量级，rebuilt learned prior 输出的平均 measurement error `9.54e-03`，到 true branch 的平均距离 `0.9250`，到 reversed branch 的平均距离 `0.7775`，mean branch bias `-0.1475`，且仅 `1 / 4` 个样例为正偏向。
- 该结果说明：phase retrieval 中“先把 solver error 降下来”这一任务已被真实推进，但 branch preference 并未在低误差条件下稳定保持。
- 因此，当前 phase 结果更接近“branch selection 对 solver / prior / benchmark 细节敏感”的预审结论，而不是“稳定 prior-induced branch bias 已成立”。
- 正式五审稿人循环仍不能启动，因为理论推导、稳健性统计、正文与补图仍未形成可审材料。

## 预审备注（round8 branch-bias 稳健性扫描后）
- 当前环境已新增一套可复核的 round8 稳健性扫描工件，并在低 measurement-error 条件下系统比较了 prior family、训练随机种子和初始化对 branch bias 的影响。
- round8 共完成 `144` 次真实 phase solve，整体聚合结果为：mean exact ambiguity quantity `1.08e-16`，mean recovered measurement error `1.20e-02`，mean branch bias `0.0105`，正偏向比例 `0.535`，负偏向比例 `0.465`。
- 更关键的是，分组后出现了系统性翻转：`true_biased` 条件下 `48 / 48` 次为正偏向，平均 `branch_bias = 0.6893`；`reversed_biased` 条件下 `48 / 48` 次为负偏向，平均 `branch_bias = -0.7330`；`balanced` 条件下仅轻微偏正，平均 `branch_bias = 0.0752`。
- 该结果说明：当前 phase retrieval 中的 branch selection 至少在这个 controlled benchmark 里高度依赖 prior orientation bias，而不是稳定的统一现象。
- 因此，正式五审稿人循环仍不能启动；下一步必须先补机制分离实验，而不是把当前 branch sign 写成论文主结论。

## 预审备注（round9 orientation-ratio 连续扫参后）
- 当前工作区已新增一套可复核的 round9 连续扫参工件，并把 branch selection 限制在 exact ambiguity pair 上，从而把 solver failure 与 prior-induced selection 进一步分离。
- round9 共完成 `1056` 次真实 branch evaluation，聚合结果为：mean exact ambiguity quantity `1.39e-16`，mean recovered measurement error `7.11e-17`，overall mean branch bias `-0.0280`，overall 正偏向比例 `0.495`。
- 更关键的是，平均 `branch_bias` 会随 training true-orientation ratio 连续变化：`ratio=0.0` 时为 `-0.6078`，`ratio=0.5` 时为 `-0.0894`，`ratio=0.6` 时转为 `0.1951`，`ratio=1.0` 时为 `0.4125`。
- 该结果说明：orientation bias 本身已足以在几乎零 measurement-error 的条件下驱动 branch sign 跨零翻转，因此当前 phase 预审结论已从“对 prior family 敏感”进一步收紧为“对 training orientation bias 连续敏感”。
- 但正式五审稿人循环仍不能启动，因为去偏置 baseline、理论推导、正文与补图仍未形成可审材料；下一步必须优先检查对称先验下 residual branch bias 是否归零。

## 预审备注（round10 rebuilt de-biased exact-pair 检验后）
- 当前工作区已新增一套可复核的 round10 去偏置工件，并继续把 branch selection 限制在 exact ambiguity pair 上，因此没有把 solver failure 重新混进 residual bias 判断。
- `balanced_density_prior` 在 `1024` 次 evaluation 中的聚合结果为：mean exact ambiguity quantity `1.04e-16`，mean recovered measurement error `4.79e-17`，mean branch bias `0.0962`，mean normalized branch bias `0.0820`，`choose_true_ratio = 0.541`，二项检验 `p = 0.00946`。
- `mirror_averaged_posterior` 在 `1024` 次 evaluation 中的聚合结果为：mean exact ambiguity quantity `1.04e-16`，mean recovered measurement error `5.13e-17`，mean branch bias `0.0041`，mean normalized branch bias `0.0039`，`choose_true_ratio = 0.502`，二项检验 `p = 0.925`。
- 该结果说明：当前更准确的 phase 预审结论已经从“对称先验下 residual bias 可能会自然归零”收紧为“balanced sampling 仍可能留下 residual bias，而显式 symmetry-enforced posterior averaging 才能在 rebuilt exact-pair benchmark 中把它压到近零”。
- 但正式五审稿人循环仍不能启动，因为这一点还没有推进到真实低误差 learned solver，理论推导、正文与补图也仍未形成可审材料；下一步必须优先做 solver 级 symmetry-enforced 对照。
