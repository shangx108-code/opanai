# 项目状态：计算成像1

## 项目基本信息
- 项目名称：计算成像1
- 目标期刊：Nature Communications
- 最近更新时间：2026-04-26
- 当前资料来源：`/workspace/user_files/01-1-.txt`

## 当前运行规则
- 默认推进主体：自研智能体
- 自动迭代频率：每 2 小时 1 轮
- 停止条件必须同时满足：
  - Nature Communications 五位审稿人接收概率均大于 70%
  - 所有需要补的 evidence 全部补齐
  - 所有需要的数据全部补齐
  - 正文与补充材料所需图全部补齐
  - 参考文献补齐并稳定高于 30 篇
- 图表规则：
  - 机制示意图、结构示意图、概念图可用 GPT-imag-2.0 生成初稿
  - 除示意图外，所有数据图必须基于真实数据正式成图
  - 任何 AI 生成示意图都不得直接视为定稿，仍需后续人工校正标签、结构逻辑、比例关系与期刊风格
- 理论规则：
  - 理论推导必须详实、可靠、可检查
  - 未完成详细推导的部分不得写成已证明结论

## 研究总目标
围绕“深度先验计算成像的幻觉边界与可校准不确定性理论”建立一条可投稿到 Nature Communications 的完整证据链，最终形成：
- 主体理论：hallucination 的物理定义、DSI、PDR、HCI 与 calibrated abstention
- 真实可复现实验链：至少覆盖压缩成像、相位恢复、显微去卷积/SIM 三类任务
- 正文与补充材料全套投稿级图表
- 30 篇以上已核对参考文献
- 可归档的代码、数据、图表、正文、补充材料与最终投稿包

## 当前阶段
理论强化与最小结果生成阶段。

说明：
- 选题主线、论文定位、潜在创新点、候选任务和阶段路线图已有较完整草案。
- 线性 incomplete measurement 任务已从 hand-crafted prior 推进到低秩 PCA prior、autoencoder prior 和 measurement-consistent latent inverse 基线。
- 同时，线性 masked-identity benchmark 的 observed / unsupported / bridge 三类区域定义已经补成第一版可复算口径。
- 但当前仍是“最小证据链”，还不是 Nature Communications 级别的完整研究证据。

## 当前唯一主瓶颈
round7 已在当前工作区重建并真实运行一个更强的 learned-prior phase baseline，把平均 `recovered_measurement_error` 从已登记 round5 的 `2.52e-01` 压到 `9.54e-03`。因此上一轮“phase solver measurement consistency 偏弱”的首要问题已被推进。当前新的唯一主瓶颈变成：在更低 solver error 下，phase branch bias 不再稳定，甚至多数样例更接近 reversed branch，说明现有 phase 证据仍不足以支撑“稳定 prior-induced branch selection”这一论文级主张。

具体表现：
- round7 的 exact ambiguity quantity 仍保持机器精度量级，但 empirical branch-selection quantity 出现明显翻转和样例间波动。
- round7 的 4 个样例中仅 `1 / 4` 为正 branch bias，平均 `branch_bias = -0.1475`，与已登记 round5 的 `0.7692` 正偏向不一致。
- 这意味着此前 branch preference 至少部分依赖 solver / benchmark / prior family 细节，而不是已站稳的统一现象。
- DSI / PDR / HCI 仍未完成完整推导、完整适用边界说明和可计算实现。
- 正文与补充材料仍无投稿级图表体系。

## 本轮唯一最高优先级
在 round6 指标边界已固定的前提下，本轮唯一最高优先级是：重建并真实运行一个更强的 learned-prior phase solver，优先把 `recovered_measurement_error` 明显降下来，再检查低误差条件下 branch bias 是否仍稳定存在。

## 本轮交付物
1. 当前工作区可现场复核的 round7 phase solver 重建脚本
2. round7 相位恢复输出目录与真实结果文件
3. 新的 `recovered_measurement_error`、`distance_to_true`、`distance_to_reversed`、`branch_bias` 对照表
4. “低 solver error 下 branch bias 仍不稳定”的优先级判定
5. 更新后的项目状态与监督结论

## 完成标准
- 当前工作区已真实跑出一个更低 `recovered_measurement_error` 的新 phase baseline
- 新 baseline 的输出字段仍与 round6 的 exact / empirical 三层量兼容
- 已据新结果判断低误差下 branch bias 是否仍稳定
- 已据此更新项目状态与监督结论

## 下一轮立即动作
1. 在 round7 低 measurement-error 重建基线上做受控稳健性扫描，优先检查 branch bias 对 prior family、训练集取向偏置和随机初始化的敏感性。
2. 真实运行该稳健性扫描，并形成 branch sign / magnitude 的重复性统计，而不是只看单次均值。
3. 只有在低误差条件下 branch selection 仍可重复稳定出现，才考虑把 phase 结果接到 DSI / PDR / HCI 的统一理论接口。

## 已真实完成
- 已从上传材料中抽取项目名称、论文主线、实施方案、候选任务、图表规划与首批参考文献。
- 已识别目标期刊为 Nature Communications。
- 已完成项目初始化编排与持续迭代框架设计。
- 已编写并运行最小双任务基准脚本。
- 已获得线性 incomplete measurement 任务中的 unsupported connector 现象。
- 已获得 phase retrieval 中 true object 与 reversed mode 的等测量证据，measurement identity error 为 `4.20e-26` 量级。
- 已生成第 1 轮结果文件：
  - `linear_round1_panel.png`
  - `linear_measurement_mask.png`
  - `phase_round1_panel.png`
  - `round1_summary.json`
  - `round1_metrics.csv`
- 已在同一线性任务上接入训练型低秩 PCA prior，并真实运行 `round2_linear_pca_prior.py`。
- 训练型 PCA prior 在观测区误差为 `5.29e-03`，未观测区误差为 `4.49e-02`，说明其在观测约束较弱处更容易引入额外结构。
- 已新建并真实运行 `round3_linear_autoencoder_prior.py`，在 6 个断裂目标上评估 zero-fill、PCA prior 与非线性 autoencoder prior。
- round3 聚合结果显示：
  - zero-fill：观测区 MAE `0.0000`，未观测区 MAE `0.0729`，bridge mean intensity `0.0000`
  - PCA prior：观测区 MAE `0.0352`，未观测区 MAE `0.1107`，bridge mean intensity `0.5276`
  - autoencoder prior：观测区 MAE `0.0000`，未观测区 MAE `0.2356`，bridge mean intensity `0.3417`
- 代表性样例显示，autoencoder prior 在保持观测区一致的同时，会在缺失中段补出连续亮结构。
- 已在当前工作区新建并真实运行 `round4_linear_measurement_consistent_prior.py`。
- 已在同一线性 benchmark 上形成 zero-fill、PCA prior、autoencoder projection 与 measurement-consistent latent inverse 四方对照。
- round4 聚合结果显示：
  - zero-fill：观测区 MAE `0.0000`，未观测区 MAE `0.0000`，bridge mean intensity `0.0000`
  - PCA prior：观测区 MAE `0.0000`，未观测区 MAE `0.1887`，bridge mean intensity `0.8264`
  - autoencoder projection：观测区 MAE `0.0000`，未观测区 MAE `0.4900`，bridge mean intensity `0.4968`
  - latent inverse：观测区 MAE `0.0000`，未观测区 MAE `0.4891`，bridge mean intensity `0.4964`
- round4 结果说明：在当前断裂目标 benchmark 中，measurement-consistent 的 latent inverse 基线即使保持观测区精确一致，仍会在未观测 bridge 区域生成非零连接结构。
- 已完成第一版可检查理论链：
  - 线性 masked-identity 模型下，未观测像素的 DSI = 0、PDR = 1 为精确结论。
  - Fourier magnitude phase retrieval 下，true object 与 reversed mode 的测量等价为精确结论。
- 已完成 30+ 工作文献表，当前工作文献数为 42。
- 已在当前工作区重新落地并真实运行线性 round4 重现实验脚本：`/workspace/computational-imaging-1-ncomms/round4_region_formalization_repro.py`。
- 已生成当前工作区可复核的新输出目录：`/workspace/computational-imaging-1-ncomms/round4_region_formalization_outputs/`。
- 已生成新的正式定义对齐文件：`/workspace/computational-imaging-1-ncomms/theory_round3_region_formalization.md`。
- 已在当前工作区新建并真实运行相位恢复 learned-prior 基线脚本：`/workspace/computational-imaging-1-ncomms/round5_phase_retrieval_learned_prior.py`。
- 已生成新的相位恢复输出目录：`/workspace/computational-imaging-1-ncomms/round5_phase_retrieval_outputs/`。
- 已生成 round5 结果文件：
  - `round5_phase_summary.json`
  - `round5_phase_case_metrics.csv`
  - `round5_phase_panel.png`
  - `round5_phase_ambiguity_notes.md`
- round5 在 4 个 held-out 相位恢复样例上的聚合结果为：
  - true / reversed 精确 branch 的 measurement error：`1.26e-16`
  - learned prior 输出的平均 measurement error：`2.52e-01`
  - learned prior 输出到 true branch 的平均距离：`0.4380`
  - learned prior 输出到 reversed branch 的平均距离：`1.2072`
  - mean branch bias：`0.7692`
  - 4 / 4 个样例均表现为对 true branch 的正偏向
- 当前重现实验在 6 个断裂目标上的聚合结果为：
  - zero-fill：观测区 MAE `0.0000`，未支撑区 MAE `0.0000`，bridge mean intensity `0.0000`
  - PCA prior：观测区 MAE `0.0000`，未支撑区 MAE `0.1186`，bridge mean intensity `0.5756`
  - autoencoder projection：观测区 MAE `0.0000`，未支撑区 MAE `0.1012`，bridge mean intensity `0.9077`
  - latent inverse：观测区 MAE `0.0000`，未支撑区 MAE `0.1674`，bridge mean intensity `0.9959`
- 这一步已经把 observed region、unsupported region、bridge region 以及对应的 observed-region MAE、unsupported-region MAE、bridge mean intensity、bridge L1 error 固定为可复算字段。
- 已确认一个关键归档事实：记忆中登记的旧 round4 实体路径当前不在工作区，因此本轮新增的是“可复核重现实验工件”，不能把旧路径直接算作已现场复核完成。
- 已新增 `/workspace/memory/computational-imaging-1-ncomms/phase-ambiguity-metrics-round6.md`，把 round5 中 `true_reversed_measurement_error`、`recovered_measurement_error`、`distance_to_true`、`distance_to_reversed` 与 `branch_bias` 固定为三层量：
  - exact ambiguity quantity
  - empirical measurement-consistency quantity
  - empirical branch-selection quantity
- 已在该说明中明确：`branch_bias = distance_to_reversed - distance_to_true`，按登记聚合值计算为 `1.2072 - 0.4380 = 0.7692`。
- 已据此完成本轮优先级判定：下一轮应先补强 phase solver 的 measurement consistency，而不是直接把当前 round5 结果接成统一理论主结论。
- 已确认一个新的现场限制：当前工作区未找到 round5 的原始脚本与原始输出文件，因此本轮 formalization 是基于已登记项目状态完成的理论/口径推进，不构成对 round5 原始工件的二次现场复核。
- 已在当前工作区新建并真实运行 ` /workspace/computational-imaging-1-ncomms/round7_phase_pca_solver_rebuild.py`，重建一个可现场复核的 learned-prior phase benchmark。
- 已生成新的输出目录：`/workspace/computational-imaging-1-ncomms/round7_phase_pca_solver_outputs/`。
- 已生成 round7 结果文件：
  - `round7_phase_summary.json`
  - `round7_phase_case_metrics.csv`
  - `round7_phase_panel.png`
  - `round7_phase_notes.md`
- round7 在 4 个 held-out 相位恢复样例上的聚合结果为：
  - true / reversed 精确 branch 的 measurement error：`1.39e-16`
  - rebuilt learned prior 输出的平均 measurement error：`9.54e-03`
  - rebuilt learned prior 输出到 true branch 的平均距离：`0.9250`
  - rebuilt learned prior 输出到 reversed branch 的平均距离：`0.7775`
  - mean branch bias：`-0.1475`
  - 仅 `1 / 4` 个样例为正 branch bias
- 这一步真实推进了“先降 solver error”的瓶颈，但同时暴露出一个更关键的新事实：当 measurement consistency 显著改善后，branch bias 并没有稳定保持为对 true branch 的正偏向，因此当前 phase 结果仍不足以直接支撑统一理论接口。

## 已部分完成但仍缺关键环节
- 文献：已补到 30+，并形成按主题分类的工作文献表；但尚未整理成最终 BibTeX 并逐条嵌入正文/补充材料。
- 理论：已有第一版可检查理论链，并补上了线性 benchmark 的区域与指标正式定义；但仍缺一般压缩成像、一般非线性相位恢复和 calibrated HCI 的完整推导。
- 任务设计：压缩成像/incomplete measurement 与相位恢复已形成最小真实运行结果；线性任务已有训练型低秩 prior、前馈式非线性 autoencoder prior、measurement-consistent latent inverse prior 以及统一区域指标；相位恢复除已登记 round5 结果外，现又补出 round7 的低 measurement-error 重建基线，但仍缺 posterior / diffusion / Bayesian 版本、branch bias 稳健性统计以及投稿级 benchmark。
- 图表：已有第 1 轮结果图，但仍属于内部实验图，不是投稿定稿图。
- 归档：当前工作区已新增 round4 重现实验工件；但历史 round1 / round2 以及记忆中登记的旧 round4 工件仍未在现场找到，原始归档仍需后续补回。

## 尚未开始
- DSI / PDR / HCI 的完整论文级推导文稿
- 正文与补充材料图的正式生成
- 5 位审稿人并行审稿循环
- 最终投稿归档包

## 参考文献状态
- 当前工作文献数：42
- 目标下限：30
- 当前判断：数量门槛已跨过，但还未完成 BibTeX 统一、正文嵌入和引用角色精修

## 当前接收概率判断
- 综合接收概率：19%–25%

依据：
- 创新构想：中到强
- 理论充分性：弱
- 方法与代码可靠性：弱到中
- 数据与结果完整性：弱
- 图表质量：弱
- 写作成熟度：弱
- 期刊匹配度：中

当前最拖累接收概率的短板：
1. 低 measurement-error 条件下的 phase branch bias 仍不稳定，尚未形成可重复的机制证据
2. DSI / PDR / HCI 仍没有完整论文级推导与适用边界说明
3. 图表体系、正文、补充材料和多任务结果矩阵仍远未补齐

## 最近一次重要更新摘要
2026-04-25：根据上传项目草案完成项目初始化，确立“先建立并跑通最小双任务证据链”为当前唯一最高优先级，并启用独立项目记忆文件集。
2026-04-25：完成第 1 轮最小双任务基准运行。线性任务中 prior library selection 选择了 `connected_vertical_bar`，其未观测区域误差高于观测区域误差；相位恢复任务中 prior library selection 选择了 `reversed_ambiguity_mode`，且该分支相对 reversed mode 的误差为 0，measurement identity error 为 `4.20e-26`。
2026-04-25：在线性任务上完成训练型低秩 PCA prior 初测。PCA prior 残差为 `7.28e-02`，观测区误差为 `5.29e-03`，未观测区误差为 `4.49e-02`，表明 learned prior 同样更容易在 unsupported region 引入结构。
2026-04-25：在线性任务上完成非线性 autoencoder prior 初测。基于 256 个 connected-bar 训练样本训练小型自编码器，并在 6 个断裂目标上真实运行；autoencoder prior 的平均观测区 MAE 为 `0.0000`，未观测区 MAE 为 `0.2356`，bridge mean intensity 为 `0.3417`，说明 learned prior 会在 measurement mask 未覆盖区域补出连接结构。
2026-04-25：在线性任务上补做 measurement-consistent learned prior 逆问题基线。已在当前工作区真实运行 `round4_linear_measurement_consistent_prior.py`，并输出 `round4_summary.json`、`round4_case_metrics.csv`、`round4_linear_measurement_consistent_panel.png` 与 `round4_linear_measurement_mask.png`；结果显示 latent inverse 在观测区 MAE 为 `0.0000` 的同时，未观测区 MAE 为 `0.4891`，bridge mean intensity 为 `0.4964`，说明 measurement-consistent 求解并未消除 unsupported bridge hallucination。
2026-04-25：完成第一版理论笔记与工作文献表。理论上已把 masked-identity 下的 DSI/PDR 和 Fourier magnitude 下的 ambiguity branch 写成可检查形式；文献已扩展到 42 条并按主题分类。
2026-04-26：更新项目运行规则。后续由自研智能体按每 2 小时 1 轮推进；停止标准收紧为“接收概率 >70%”与“evidence / 数据 / 图 / 参考文献全部补齐”同时成立；示意图允许用 GPT-imag-2.0 起稿，但非示意图必须全部使用真实数据，理论推导必须详实可靠。
2026-04-26：在当前工作区重新落地并真实运行 `round4_region_formalization_repro.py`，生成 `round4_reproduced_summary.json`、`round4_reproduced_case_metrics.csv`、`round4_reproduced_panel.png`、`round4_reproduced_mask.png` 与 `round4_region_metadata.json`；同时新增 `theory_round3_region_formalization.md`，把 observed / unsupported / bridge 三类区域及其指标定义固定为可复算口径。此举补上了线性 benchmark 的第一版正式判据，但尚未补齐相位恢复 learned prior / posterior 结果链。
2026-04-26：在当前工作区新建并真实运行 `round5_phase_retrieval_learned_prior.py`，训练长度为 64 的一维非对称对象 autoencoder decoder prior，并在 4 个 held-out 样例上仅通过 Fourier magnitude 测量做 latent 优化。生成 `round5_phase_summary.json`、`round5_phase_case_metrics.csv`、`round5_phase_panel.png` 与 `round5_phase_ambiguity_notes.md`。结果显示 true / reversed 分支的精确 measurement error 为 `1.26e-16` 量级，而 learned prior 输出的 mean branch bias 为 `0.7692`，且 4 / 4 个样例均更接近 true branch；但其平均 measurement error 仍为 `2.52e-01`，因此当前只能算“第一版经验性 branch-selection 证据”，不能包装成强求解器或一般理论结论。
2026-04-26：新增 `/workspace/memory/computational-imaging-1-ncomms/phase-ambiguity-metrics-round6.md`。本轮未新增真实数值实验，而是把 round5 已登记字段正式拆分为 exact ambiguity quantity、empirical measurement-consistency quantity 与 empirical branch-selection quantity，并明确 `branch_bias = distance_to_reversed - distance_to_true`。基于这一步，项目当前唯一主瓶颈已从“指标边界不清”切换为“phase solver 的 measurement consistency 仍偏弱”，因此下一轮唯一最高优先级改为先补强 phase baseline，而不是直接推进统一理论主接口。
2026-04-26：在当前工作区新建并真实运行 `round7_phase_pca_solver_rebuild.py`，重建了一个可现场复核的 learned-prior phase retrieval benchmark，并生成 `/workspace/computational-imaging-1-ncomms/round7_phase_pca_solver_outputs/`。该 rebuilt PCA prior baseline 在 4 个 held-out 样例上的平均 `recovered_measurement_error` 为 `9.54e-03`，显著低于已登记 round5 的 `2.52e-01`；但其平均 `branch_bias = -0.1475`，且只有 `1 / 4` 个样例为正偏向，说明一旦 solver error 降低，当前 phase branch preference 并不稳定。由此，项目当前唯一主瓶颈已从“先降 measurement error”切换为“验证低误差 phase branch bias 的稳健性与机制来源”，统一理论接口仍不能提前闭合。
