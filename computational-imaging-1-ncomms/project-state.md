# 项目状态：计算成像1

## 项目基本信息
- 项目名称：计算成像1
- 目标期刊：Nature Communications
- 最近更新时间：2026-04-25
- 当前资料来源：`/workspace/user_files/01-1-.txt`

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
- 同时，第一版理论笔记与 30+ 工作文献表已经补上。
- 但当前仍是“最小证据链”，还不是 Nature Communications 级别的完整研究证据。

## 当前唯一主瓶颈
虽然线性任务已经从 hand-crafted prior、低秩 prior、前馈式 autoencoder prior 推进到 measurement-consistent 的 latent inverse baseline，但 unsupported region / bridge intensity 仍只是经验指标，还没有被形式化成统一、可计算、可写入理论部分的判据，因此当前结果仍停留在“现象成立”而不是“论证闭环”。

具体表现：
- 线性任务已新增 latent inverse solver，但 bridge intensity 与 unsupported-region error 还没有升格为正式定义。
- 当前 measurement-consistent baseline 仍是线性 benchmark 下的一类 learned decoder prior，不等同于 DIP / diffusion / Bayesian posterior 全景证据。
- 相位恢复任务已经证明 measurement ambiguity，但还没有展示 learned prior 或 posterior sampling 在该歧义上的实际失效模式。
- DSI / PDR / HCI 仍未完成完整推导和可计算实现。
- 正文与补充材料仍无投稿级图表体系。

## 本轮唯一最高优先级
把当前线性 benchmark 中已经跑通的 zero-fill、PCA prior、autoencoder projection 与 measurement-consistent latent inverse 结果，写成第一版统一可计算判据：明确 observed region、unsupported region、bridge region 以及对应误差/强度指标的数学定义和可执行计算口径。

## 本轮交付物
1. measurement-consistent learned prior 脚本：`/workspace/computational-imaging-1-ncomms/round4_linear_measurement_consistent_prior.py`
2. 真实输出目录：`/workspace/computational-imaging-1-ncomms/round4_outputs/`
3. 代表性结果图：`round4_linear_measurement_consistent_panel.png`
4. 观测 mask 图：`round4_linear_measurement_mask.png`
5. 指标文件：`round4_summary.json` 与 `round4_case_metrics.csv`
6. 第一版理论笔记：`/workspace/computational-imaging-1-ncomms/theory_round2_note.md`
7. 30+ 工作文献表：`/workspace/computational-imaging-1-ncomms/reference_map_round2.md`

## 完成标准
下一轮完成标准：
- 不是只给口头定义，而是给出正式符号、区域定义、计算式和适用边界
- 定义能无歧义对应到当前 round4 结果文件中的真实字段与像素区域
- 明确哪些量已可计算，哪些仍只是启发式量
- 已据此更新项目状态与下一轮优先级

## 下一轮立即动作
1. 固定 round4 的观测掩膜、目标集合与 bridge 区域定义。
2. 把 unsupported region、bridge region、observed region error、unsupported-region error、bridge intensity 写成统一数学表达。
3. 将这些定义回填到当前线性 benchmark 的汇总脚本与结果叙述中。
4. 再进入相位恢复 iterative / posterior baseline，而不是提前铺开显微任务。

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

## 已部分完成但仍缺关键环节
- 文献：已补到 30+，并形成按主题分类的工作文献表；但尚未整理成最终 BibTeX 并逐条嵌入正文/补充材料。
- 理论：已有第一版可检查理论链，但仍缺一般压缩成像、一般非线性相位恢复和 calibrated HCI 的完整推导。
- 任务设计：压缩成像/incomplete measurement 与相位恢复已形成最小真实运行结果；线性任务已有训练型低秩 prior、前馈式非线性 autoencoder prior 与 measurement-consistent latent inverse prior，但仍缺相位恢复的 learned prior / posterior 版本以及投稿级 benchmark。
- 图表：已有第 1 轮结果图，但仍属于内部实验图，不是投稿定稿图。
- 归档：本轮在当前工作区未找到历史 round1 / round2 脚本与输出文件，说明历史结果记录已存在于 memory，但原始工件仍需补回归档。

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
- 综合接收概率：14%–20%

依据：
- 创新构想：中到强
- 理论充分性：弱
- 方法与代码可靠性：弱到中
- 数据与结果完整性：弱
- 图表质量：弱
- 写作成熟度：弱
- 期刊匹配度：中

当前最拖累接收概率的短板：
1. 没有闭合的理论推导与正式可计算指标定义
2. 结果仍停留在线性 toy benchmark 与最小相位恢复证据，跨任务主结果链尚未形成
3. 图表体系、正文、补充材料和多任务结果矩阵仍远未补齐

## 最近一次重要更新摘要
2026-04-25：根据上传项目草案完成项目初始化，确立“先建立并跑通最小双任务证据链”为当前唯一最高优先级，并启用独立项目记忆文件集。
2026-04-25：完成第 1 轮最小双任务基准运行。线性任务中 prior library selection 选择了 `connected_vertical_bar`，其未观测区域误差高于观测区域误差；相位恢复任务中 prior library selection 选择了 `reversed_ambiguity_mode`，且该分支相对 reversed mode 的误差为 0，measurement identity error 为 `4.20e-26`。
2026-04-25：在线性任务上完成训练型低秩 PCA prior 初测。PCA prior 残差为 `7.28e-02`，观测区误差为 `5.29e-03`，未观测区误差为 `4.49e-02`，表明 learned prior 同样更容易在 unsupported region 引入结构。
2026-04-25：在线性任务上完成非线性 autoencoder prior 初测。基于 256 个 connected-bar 训练样本训练小型自编码器，并在 6 个断裂目标上真实运行；autoencoder prior 的平均观测区 MAE 为 `0.0000`，未观测区 MAE 为 `0.2356`，bridge mean intensity 为 `0.3417`，说明 learned prior 会在 measurement mask 未覆盖区域补出连接结构。
2026-04-25：在线性任务上补做 measurement-consistent learned prior 逆问题基线。已在当前工作区真实运行 `round4_linear_measurement_consistent_prior.py`，并输出 `round4_summary.json`、`round4_case_metrics.csv`、`round4_linear_measurement_consistent_panel.png` 与 `round4_linear_measurement_mask.png`；结果显示 latent inverse 在观测区 MAE 为 `0.0000` 的同时，未观测区 MAE 为 `0.4891`，bridge mean intensity 为 `0.4964`，说明 measurement-consistent 求解并未消除 unsupported bridge hallucination。
2026-04-25：完成第一版理论笔记与工作文献表。理论上已把 masked-identity 下的 DSI/PDR 和 Fourier magnitude 下的 ambiguity branch 写成可检查形式；文献已扩展到 42 条并按主题分类。
