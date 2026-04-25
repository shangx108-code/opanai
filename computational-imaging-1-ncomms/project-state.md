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
- 第 1 轮已真实跑通一个最小双任务基准，并产出第一批结果图、指标文件和可复现实验脚本。
- 但当前结果仍是“最小证据链”，还不是 Nature Communications 级别的完整研究证据。

## 当前唯一主瓶颈
虽然最小证据链已经建立，但它仍停留在“候选库先验”层面，尚未进入真正的深度先验 / Bayesian / diffusion 级别验证，因此还不能支撑目标论文的核心主张强度。

具体表现：
- 线性任务和相位恢复任务只有最小 toy benchmark，尚无 DIP / PnP / diffusion / Bayesian baseline。
- 线性任务中的“先验幻觉”目前来自候选库选择，而不是深度先验优化。
- 相位恢复任务已经证明 measurement ambiguity，但还没有展示 learned prior 或 posterior sampling 在该歧义上的实际失效模式。
- DSI / PDR / HCI 仍未完成详细推导和可计算实现。
- 正文与补充材料仍无投稿级图表体系。

## 本轮唯一最高优先级
把第 1 轮最小双任务基准升级到“可支持深度先验验证”的版本，优先从线性 incomplete measurement 任务切入，接入一个真实可运行的学习型先验或低秩训练型先验，并开始把 toy 现象转成更接近论文主张的结果链。

## 本轮交付物
1. 第 1 轮最小双任务基准脚本：`/workspace/computational-imaging-1-ncomms/round1_minimal_benchmark.py`
2. 真实输出目录：`/workspace/computational-imaging-1-ncomms/round1_outputs/`
3. 线性任务结果图与 measurement mask 图
4. 相位恢复歧义图
5. 指标文件：`round1_summary.json` 与 `round1_metrics.csv`

## 完成标准
第 1 轮已完成，满足以下条件：
- 双任务脚本已真实运行
- 已产出实际结果文件
- 已证明至少一个线性 unsupported-structure 案例和一个非线性 exact ambiguity 案例
- 已据真实结果更新项目状态与下一轮优先级

## 下一轮立即动作
1. 在线性 incomplete measurement 任务上接入真实训练型先验，而不再停留在手工候选库。
2. 为相位恢复任务加入可运行的 iterative baseline，并比较其与 prior branch selection 的差别。
3. 基于当前观测 mask 和 phase ambiguity，写出 DSI 与 ambiguity branch 的第一版形式化说明。
4. 把参考文献从 12 篇扩充到至少 20 篇，并按主题分类。
5. 开始整理正文 Figure 1 和 Figure 2 的正式数据字段与图注逻辑。

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

## 已部分完成但仍缺关键环节
- 文献：已有 12 篇种子参考文献，但未补足到 30+，且尚未完成统一核对与主题归类。
- 理论：已有概念框架与指标定义草案，但详细推导尚未完成。
- 任务设计：压缩成像/incomplete measurement 与相位恢复已形成最小真实运行结果；线性任务已有训练型低秩 prior 版本，但仍缺真实 deep prior / diffusion / Bayesian 版本和投稿级 benchmark。
- 图表：已有第 1 轮结果图，但仍属于内部实验图，不是投稿定稿图。

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
- 综合接收概率：10%–15%

依据：
- 创新构想：中到强
- 理论充分性：弱
- 方法与代码可靠性：弱
- 数据与结果完整性：弱
- 图表质量：弱
- 写作成熟度：弱
- 期刊匹配度：中

当前最拖累接收概率的短板：
1. 结果仍停留在 toy benchmark，尚未接入真实深度先验方法
2. 没有闭合的理论推导与物理可辨识性证明
3. 参考文献与补充证据链远未补齐

## 最近一次重要更新摘要
2026-04-25：根据上传项目草案完成项目初始化，确立“先建立并跑通最小双任务证据链”为当前唯一最高优先级，并启用独立项目记忆文件集。
2026-04-25：完成第 1 轮最小双任务基准运行。线性任务中 prior library selection 选择了 `connected_vertical_bar`，其未观测区域误差高于观测区域误差；相位恢复任务中 prior library selection 选择了 `reversed_ambiguity_mode`，且该分支相对 reversed mode 的误差为 0，measurement identity error 为 `4.20e-26`。
2026-04-25：在线性任务上完成训练型低秩 PCA prior 初测。PCA prior 残差为 `7.28e-02`，观测区误差为 `5.29e-03`，未观测区误差为 `4.49e-02`，表明 learned prior 同样更容易在 unsupported region 引入结构。
