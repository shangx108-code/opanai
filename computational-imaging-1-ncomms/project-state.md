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
  - 任何 AI 生成示意图都不得直接视为定稿，仍需后续人工校正
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
- 项目已经从最小双任务基准推进到线性任务的多类 learned prior、相位恢复 exact-ambiguity 分析、orientation-bias 扫描和 de-biased exact-pair benchmark。
- 同时，线性 benchmark 的 observed / unsupported / bridge 区域已经形成第一版正式定义，且本地新增了一轮区域指标对齐工件。
- 但当前仍缺 Nature Communications 级别的多任务完整结果链、论文级理论闭环、正文/补图体系与五审稿人循环。

## 当前唯一主瓶颈
线性链已经重新在当前工作区落地到 round4，但 phase 链仍然缺少当前工作区可复核的 solver 级 symmetry-enforced 低误差基线。因此当前真正限制投稿概率继续上升的，已经从“线性本地可复核性不足”转成了“phase 结果还没有在当前工作区重新站稳”。

具体表现：
- round3 / round4 现已补回本地 rebuild 工件，但还需要和 round5 的正式区域定义进一步做统一汇总。
- 项目记忆里已登记 round7-10 的 phase 进展，但当前工作区未现场复核这些工件。
- 相位恢复 learned-prior / posterior 机制仍缺当前工作区可复核的 solver 级 symmetry-enforced 低误差验证。
- DSI / PDR / HCI 仍未完成完整推导、适用边界说明和可计算实现。
- 正文与补充材料仍无投稿级图表体系。

## 本轮唯一最高优先级
补回线性 round3 / round4 的本地实体工件，并重新建立当前工作区可复核的 nonlinear prior / measurement-consistent latent inverse 起点。

## 本轮交付物
1. rebuilt round3 脚本：`/workspace/computational-imaging-1-ncomms/round3_linear_autoencoder_prior.py`
2. rebuilt round3 输出目录：`/workspace/computational-imaging-1-ncomms/round3_outputs/`
3. rebuilt round4 脚本：`/workspace/computational-imaging-1-ncomms/round4_linear_measurement_consistent_prior.py`
4. rebuilt round4 输出目录：`/workspace/computational-imaging-1-ncomms/round4_outputs/`
5. round5 区域定义说明与对齐脚本继续保留为统一口径基线

## 完成标准
- round3 / round4 已在当前工作区形成可运行脚本和真实输出文件
- 明确标注它们是 rebuild 工件，而不是对丢失原件的逐字恢复
- 新工件已经足以作为下一轮统一线性指标汇总与衔接 phase 链的本地起点
- 已据此更新项目状态与下一轮优先级

## 下一轮立即动作
1. 先把 round5 的区域定义和指标口径映射到 rebuilt round3 / round4 工件上，形成统一线性结果表。
2. 再回到相位恢复链，优先重建当前工作区可复核的 solver 级 symmetry-enforced 低误差基线。
3. 把 `bridge gap` 与 DSI / PDR 的关系推进到更正式的理论笔记。

## 已真实完成
- 已从上传材料中抽取项目名称、论文主线、实施方案、候选任务、图表规划与首批参考文献。
- 已识别目标期刊为 Nature Communications。
- 已完成项目初始化编排与持续迭代框架设计。
- 已编写并运行最小双任务基准脚本。
- 已获得线性 incomplete measurement 任务中的 unsupported connector 现象。
- 已获得 phase retrieval 中 true object 与 reversed mode 的等测量证据，measurement identity error 为 `4.20e-26` 量级。
- 已在同一线性任务上接入训练型低秩 PCA prior，并真实运行 `round2_linear_pca_prior.py`。
- 已完成第一版可检查理论链：
  - 线性 masked-identity 模型下，未观测像素的 DSI = 0、PDR = 1 为精确结论。
  - Fourier magnitude phase retrieval 下，true object 与 reversed mode 的测量等价为精确结论。
- 已完成 30+ 工作文献表，当前工作文献数为 42。
- 项目记忆中已登记后续 phase 任务推进到 rebuilt low-error solver、orientation-ratio 连续扫描和 de-biased exact-pair benchmark。
- 已完成线性 benchmark 的第一版正式区域定义说明，明确了 observed region、unsupported region、bridge region 与 peripheral unsupported region。
- 已真实运行 `round5_region_metric_alignment.py`，并用当前本地可复核的 round1 / round2 工件完成一次区域指标对齐计算。
- round5 对齐结果显示：
  - zero-fill：observed MAE `0.0000`，bridge mean `0.0000`，bridge gap `-0.0365`
  - round1 connected vertical bar：observed MAE `0.0875`，bridge mean `0.8750`，bridge gap `0.8385`
  - round2 PCA prior：observed MAE `0.0541`，bridge mean `0.6035`，bridge gap `0.5670`
- 当前 benchmark 的 bridge 区域真值均值约为 `0.0365`，因此后续写作中 `bridge gap` 比单独的 `bridge mean intensity` 更稳。
- 已在当前工作区补回并真实运行 rebuilt round3 非线性 learned-prior 工件：
  - `round3_linear_autoencoder_prior.py`
  - `round3_outputs/round3_summary.json`
  - `round3_outputs/round3_case_metrics.csv`
  - `round3_outputs/round3_linear_autoencoder_panel.png`
- rebuilt round3 聚合结果为：
  - autoencoder projection：observed MAE `0.1381`，unsupported MAE `0.1260`，bridge mean intensity `0.7947`，bridge L1 error `0.7617`
  - zero-fill：observed MAE `0.0000`，unsupported MAE `0.0246`，bridge mean intensity `0.0000`
- 已在当前工作区补回并真实运行 rebuilt round4 measurement-consistent latent-prior 工件：
  - `round4_linear_measurement_consistent_prior.py`
  - `round4_outputs/round4_summary.json`
  - `round4_outputs/round4_case_metrics.csv`
  - `round4_outputs/round4_linear_measurement_consistent_panel.png`
  - `round4_outputs/round4_linear_measurement_mask.png`
- rebuilt round4 聚合结果为：
  - zero-fill：observed MAE `0.0000`，unsupported MAE `0.0246`，bridge mean intensity `0.0000`
  - pca prior：observed MAE `0.0951`，unsupported MAE `0.1291`，bridge mean intensity `0.7121`
  - autoencoder projection：observed MAE `0.1744`，unsupported MAE `0.1223`，bridge mean intensity `0.7754`
  - latent inverse：observed MAE `0.0966`，unsupported MAE `0.1355`，bridge mean intensity `0.7102`
- 需要明确：上述 round3 / round4 是当前工作区的 rebuild 工件，用于恢复本地可复核起点，不等于历史丢失原件的逐字复刻。

## 已部分完成但仍缺关键环节
- 文献：已补到 30+，并形成按主题分类的工作文献表；但尚未整理成最终 BibTeX 并逐条嵌入正文/补充材料。
- 理论：已有第一版可检查理论链，并补上了线性 benchmark 的区域与指标正式定义；但仍缺一般压缩成像、一般非线性相位恢复和 calibrated HCI 的完整推导。
- 任务设计：压缩成像/incomplete measurement 与相位恢复已形成最小真实运行结果；线性任务现已重新具备训练型低秩 prior、前馈式非线性 autoencoder prior、measurement-consistent latent inverse prior 以及统一区域指标；相位恢复在项目记忆中已登记 round7-10 的受控 benchmark 进展，但当前工作区仍需补齐其本地可复核工件。
- 图表：已有内部研究图，但仍不是投稿定稿图。
- 归档：当前工作区已确认存在 round1、round2、rebuilt round3、rebuilt round4 与 round5 区域对齐工件；phase 更晚轮次工件仍需继续补回或重建。

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
- 综合接收概率：22%–28%

依据：
- 创新构想：中到强
- 理论充分性：弱
- 方法与代码可靠性：弱到中
- 数据与结果完整性：弱
- 图表质量：弱
- 写作成熟度：弱
- 期刊匹配度：中

当前最拖累接收概率的短板：
1. solver 级 symmetry-enforced 低误差 phase baseline 还没有形成当前工作区可复核闭环
2. DSI / PDR / HCI 仍没有完整论文级推导与适用边界说明
3. 图表体系、正文、补充材料和多任务结果矩阵仍远未补齐

## 最近一次重要更新摘要
2026-04-25：根据上传项目草案完成项目初始化，确立“先建立并跑通最小双任务证据链”为当前唯一最高优先级，并启用独立项目记忆文件集。
2026-04-25：完成第 1 轮最小双任务基准运行。线性任务中 prior library selection 选择了 `connected_vertical_bar`；相位恢复任务中 prior library selection 选择了 `reversed_ambiguity_mode`，measurement identity error 为 `4.20e-26`。
2026-04-25：在线性任务上完成训练型低秩 PCA prior 初测。
2026-04-25：完成第一版理论笔记与工作文献表。
2026-04-26：更新项目运行规则。后续由自研智能体按每 2 小时 1 轮推进；停止标准收紧为“接收概率 >70%”与“evidence / 数据 / 图 / 参考文献全部补齐”同时成立。
2026-04-26：完成 round5 线性区域定义与指标对齐。已新增 `linear_region_metric_note_round5.md` 与 `round5_region_metric_alignment.py`，并基于当前本地 round1 / round2 工件输出区域指标表；结果表明 `bridge gap` 比单独 `bridge mean intensity` 更适合作为当前 benchmark 的桥接幻觉量。
2026-04-26：补回当前工作区可复核的 rebuilt round3 / round4 线性工件。已真实运行 `round3_linear_autoencoder_prior.py` 与 `round4_linear_measurement_consistent_prior.py` 并生成对应输出目录；这一步恢复了 nonlinear prior 与 measurement-consistent latent inverse 的本地起点，但这些结果必须明确标注为 rebuild 工件，而不是历史原件的逐字复刻。
