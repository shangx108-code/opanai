# 项目状态：计算成像2

## 项目基本信息
- 项目名称：计算成像2
- 目标期刊：Nature Communications
- 最近更新时间：2026-04-26（scheduled round 3）
- 当前资料来源：当前项目命名空间状态文件 + 本轮对 `/workspace` 的最小范围证据核查结果

## 当前推进规则
- 之后默认使用“自研智能体”持续推进本项目。
- 自动迭代频率调整为每 2 小时 1 轮。
- 停止条件不只是接收概率超过 70%，还要求所有应补证据链全部补齐。
- 所有数据图必须基于真实数据生成，不允许用示意数据替代。
- 仅机制示意图、结构示意图和概念图可使用 GPT-imag-2.0 生成初稿，且仍需后续人工校正后才可进入正文或补充材料。
- 理论推导必须详实、连续、可检查；未完成详细推导的结论不得计为已完成证据。

## 研究总目标
围绕“计算成像中光学编码的信息容量、任务容量与鲁棒容量理论”建立一条可投稿到 Nature Communications 的完整证据链，最终形成：
- 主体理论：统一 forward model、Shannon 信息容量、Fisher 信息、任务容量、鲁棒容量及其相互关系
- 真实可复现实验链：至少覆盖线性压缩成像、PSF/depth 参数估计、任务导向快照成像、鲁棒误差分析 4 条主验证线
- 正文与补充材料全套投稿级图表
- 30 篇以上已核对参考文献
- 可归档的代码、数据、图表、正文、补充材料与最终投稿包

## 当前阶段
结果生成阶段（证据恢复子阶段，round2 已恢复，当前切换到 round3 robust 恢复）。

说明：
- 本轮已在当前工作区新建并真实运行 `/workspace/computational-imaging-2-ncomms/linear_gaussian_round2_task_weighted.py`。
- 已真实生成当前工作区可追溯的 round2 最小结果包：CSV、JSON、Markdown summary、SVG overview 和运行日志。
- 当前 round2 结果表明：在规范 task-matched 场景 `gamma = 0.0` 下，`identity_top4` 为 reconstruction-optimal，`task_matched_diag` 为 task-optimal；继续增大 task nuisance coupling 后，task-optimal 会在 `gamma = 0.8` 左右转向 `hadamard_like`。
- 当前工作区仍未找到可打开的 round3 robust 结果文件，因此 reconstruction-task-robust 三线最小闭环仍未完成。

## 当前唯一主瓶颈
当前工作区仍缺少 round3 robust 真实结果链，导致 reconstruction-task-robust 三线最小证据链无法闭合。

具体表现：
- 现在已有一条 round2 task-weighted 真实结果链，但鲁棒容量链仍不存在当前工作区实物文件。
- 只凭 round2 不能支撑 robustness 相关核心主张，也不能合法推进 Figure 5 联合对照。
- `RCR` 仍没有与当前工作区真实鲁棒结果逐项对照的详细推导输入。
- 参考文献、正文图、补充图、正文和补充材料仍远未补齐。

## 本轮唯一最高优先级
重建并真实跑通当前工作区中的最小 round3 robust 证据链。

本轮只聚焦一件事：
- 在 `/workspace/computational-imaging-2-ncomms/` 下恢复 round3 最小 robust 平台脚本
- 真实运行并落盘 CSV、summary、log 和图文件
- 用当前工作区真实输出重新建立 robust-capacity 证据基座，并与已恢复的 round2 最小链形成最小对照

## 本轮交付物
1. `/workspace/computational-imaging-2-ncomms/` 下的 round3 robust 最小平台脚本
2. round3 结果 CSV
3. round3 summary JSON
4. round3 summary Markdown
5. round3 对照图文件
6. round3 运行日志

## 本轮完成标准
- 已在当前工作区真实写出并运行 round3 脚本
- 已真实生成 round3 的 CSV、JSON、Markdown、图文件和运行日志
- 已能把 round3 结果与当前 round2 最小链进行逐项对照
- 未把任何未在当前工作区找到的旧文件继续记为已完成

## 下一轮立即动作
1. 在当前工作区真实跑通 round3 robust 最小平台并落盘实物文件
2. 基于 round2 / round3 双链结果起草 `TIG` / `RCR` 对照推导骨架
3. 决定 round1 reconstruction baseline 与 Figure 5 数据映射的先后顺序
4. 恢复参考文献核对链，先建立 10 篇可核对种子文献
5. 继续维持“无实物文件不算完成”的监督规则

## 已真实完成
- 已识别目标期刊为 Nature Communications。
- 已完成项目初始化编排与持续迭代框架设计。
- 已完成当前工作区证据核查，并确认此前记忆中声称存在的结果目录需要用当前工作区实物文件重新核对。
- 已在本轮于当前工作区真实重建并跑通 round2 最小 task-weighted surrogate。
- 已生成当前工作区可追溯的 round2 脚本、结果 CSV、summary JSON、summary Markdown、SVG overview 和运行日志。
- 已真实观察到在 `gamma = 0.0` 时 `identity_top4` 为 reconstruction-optimal、`task_matched_diag` 为 task-optimal。
- 已真实观察到 task-optimal 设计会在 `gamma = 0.8` 左右从 `task_matched_diag` 转向 `hadamard_like`。
- 已完成 scheduled round 3 的状态纠偏：当前唯一主瓶颈与唯一最高优先级已统一切换到 round3 robust 真实恢复。

## 已部分完成但仍缺关键环节
- 文献：30+ 已核对参考文献仍未建立。
- 理论：`TIG`、`RCR` 仍只有操作性数值链，尚无与当前真实结果逐项对齐的详细推导稿。
- 可复核性：目前只有 round2 最小链已恢复，round1 / round3 仍缺少当前工作区实物文件。
- 写作：虽然已有一条真实 round2 结果链，但正文和补充材料仍缺 round3 / round1、理论推导和参考文献支撑，不能进入正式写作。

## 尚未开始
- 当前工作区内可追溯的 round1 reconstruction 真实计算链
- 当前工作区内可追溯的 round3 robust 真实计算链
- 全套理论推导文稿
- PSF / depth 平台真实计算
- 正文和补充材料正式图生成
- 五位审稿人并行评审循环
- 最终投稿归档包

## 参考文献状态
- 当前已核对参考文献数：0
- 目标下限：30
- 当前判断：明显不足，尚不能支撑 Nature Communications 级别的引言、讨论和补充材料文献链

## 当前接收概率判断
- 综合接收概率：14%–20%

依据：
- 创新构想：强
- 理论充分性：弱到中
- 方法与代码可靠性：中
- 数据与结果完整性：弱到中
- 图表质量：弱
- 写作成熟度：弱
- 期刊匹配度：中到强

当前最拖累接收概率的短板：
1. reconstruction-task-robust 三线真实证据链仍未闭合，当前工作区缺少 round3 / round1 文件
2. `TIG` / `RCR` 仍没有详细推导，当前 round2 结果还只是最小 surrogate
3. 参考文献、补充材料与投稿级图表远未补齐

## 最近一次重要更新摘要
2026-04-26：scheduled round 3 未新增实验或理论证据，但已完成状态纠偏，将当前唯一主瓶颈与唯一最高优先级从已完成的 round2 恢复任务正式切换到 round3 robust 真实恢复。项目仍停留在证据恢复子阶段，因为 round3 / round1 尚未恢复，详细推导、图表和参考文献链也尚未完成。

## 项目停止条件
只有在以下条件同时满足后，项目才允许停止自动推进：
1. Nature Communications 五位审稿人的接收概率判断都大于 70%
2. 所有需要补的 evidence 均已补齐
3. 所有正文图和补充材料图均已补齐，其中数据图全部来自真实数据
4. 所有关键理论推导均已补齐并通过可检查性要求
5. 参考文献已补齐到 30 篇以上并完成核对
