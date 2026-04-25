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
- 线性 incomplete measurement 任务已新增一轮真实可运行的非线性学习型 prior 实验。
- 但当前结果仍是“最小证据链”，还不是 Nature Communications 级别的完整研究证据。

## 当前唯一主瓶颈
虽然线性任务已经从 hand-crafted prior 与低秩 prior 推进到非线性学习型 prior，但当前 learned prior 仍是前馈式 inpainting surrogate，而不是 measurement-consistent 的 inverse solver / posterior 方法，因此还不能把“学习型先验导致 unsupported hallucination”提升为更强的论文主张。

具体表现：
- 线性任务虽已有 PCA prior 与非线性 autoencoder prior，但两者都还不是优化式深度先验或 posterior baseline。
- 当前 autoencoder prior 采用“零填充测量 -> 网络补全 -> 观测区投影”的流程，证明了 learned prior 会在未观测区补结构，但还不能等同于 DIP / diffusion / Bayesian inverse solver。
- 相位恢复任务已经证明 measurement ambiguity，但还没有展示 learned prior 或 posterior sampling 在该歧义上的实际失效模式。
- DSI / PDR / HCI 仍未完成详细推导和可计算实现。
- 正文与补充材料仍无投稿级图表体系。

## 本轮唯一最高优先级
在线性 incomplete measurement 任务上，把当前前馈式 autoencoder prior 升级为 measurement-consistent 的优化式 learned prior baseline，并与现有 zero-fill、PCA prior、autoencoder prior 做同任务对照。

## 本轮交付物
1. 非线性学习型 prior 脚本：`/workspace/computational-imaging-1-ncomms/round3_linear_autoencoder_prior.py`
2. 真实输出目录：`/workspace/computational-imaging-1-ncomms/round3_outputs/`
3. 代表性结果图：`round3_linear_autoencoder_panel.png`
4. 观测 mask 图：`round3_linear_measurement_mask.png`
5. 指标文件：`round3_summary.json` 与 `round3_case_metrics.csv`

## 完成标准
本轮已完成，满足以下条件：
- 线性任务脚本已真实运行
- 已产出实际结果文件
- 已在多个断裂目标上给出 learned prior 在 unsupported region 补出连接结构的真实量化结果
- 已据真实结果更新项目状态与下一轮优先级

## 下一轮立即动作
1. 在线性任务上实现 measurement-consistent 的优化式 learned prior baseline，而不再停留在前馈补全。
2. 用同一观测 mask 与目标集合，对 zero-fill、PCA prior、autoencoder prior、优化式 prior 做统一误差表。
3. 在不扩展任务面的前提下，把 unsupported region 与 bridge intensity 写成线性任务的第一版可计算定义。
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

## 已部分完成但仍缺关键环节
- 文献：已有 12 篇种子参考文献，但未补足到 30+，且尚未完成统一核对与主题归类。
- 理论：已有概念框架与指标定义草案，但详细推导尚未完成。
- 任务设计：压缩成像/incomplete measurement 与相位恢复已形成最小真实运行结果；线性任务已有训练型低秩 prior 与非线性 autoencoder prior，但仍缺 measurement-consistent 深度先验 / diffusion / Bayesian 版本和投稿级 benchmark。
- 图表：已有第 1 轮结果图，但仍属于内部实验图，不是投稿定稿图。
- 归档：本轮在当前工作区未找到历史 round1 / round2 脚本与输出文件，说明历史结果记录已存在于 memory，但原始工件仍需补回归档。

## 尚未开始
- DSI / PDR / HCI 的详细推导文稿
- 正文与补充材料图的正式生成
- 5 位审稿人并行审稿循环
- 最终投稿归档包

## 参考文献状态
- 当前已提取种子文献数：12
- 目标下限：30
- 当前判断：明显不足，不能支撑 Nature Communications 级别的引言、相关工作与讨论部分

## 当前接收概率判断
- 综合接收概率：12%–18%

依据：
- 创新构想：中到强
- 理论充分性：弱
- 方法与代码可靠性：弱到中
- 数据与结果完整性：弱
- 图表质量：弱
- 写作成熟度：弱
- 期刊匹配度：中

当前最拖累接收概率的短板：
1. 结果仍停留在线性 toy benchmark，尚未接入 measurement-consistent 深度先验 / posterior 方法
2. 没有闭合的理论推导与物理可辨识性证明
3. 参考文献与补充证据链远未补齐

## 最近一次重要更新摘要
2026-04-25：根据上传项目草案完成项目初始化，确立“先建立并跑通最小双任务证据链”为当前唯一最高优先级，并启用独立项目记忆文件集。
2026-04-25：完成第 1 轮最小双任务基准运行。线性任务中 prior library selection 选择了 `connected_vertical_bar`，其未观测区域误差高于观测区域误差；相位恢复任务中 prior library selection 选择了 `reversed_ambiguity_mode`，且该分支相对 reversed mode 的误差为 0，measurement identity error 为 `4.20e-26`。
2026-04-25：在线性任务上完成训练型低秩 PCA prior 初测。PCA prior 残差为 `7.28e-02`，观测区误差为 `5.29e-03`，未观测区误差为 `4.49e-02`，表明 learned prior 同样更容易在 unsupported region 引入结构。
2026-04-25：在线性任务上完成非线性 autoencoder prior 初测。基于 256 个 connected-bar 训练样本训练小型自编码器，并在 6 个断裂目标上真实运行；autoencoder prior 的平均观测区 MAE 为 `0.0000`，未观测区 MAE 为 `0.2356`，bridge mean intensity 为 `0.3417`，说明 learned prior 会在 measurement mask 未覆盖区域补出连接结构。
