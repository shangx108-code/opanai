# 项目状态：计算成像2

## 项目基本信息
- 项目名称：计算成像2
- 目标期刊：Nature Communications
- 最近更新时间：2026-04-26
- 当前资料来源：当前项目命名空间状态文件 + `/workspace/computational-imaging-2-ncomms/linear_gaussian_round3_robust.py` 及其真实输出文件

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
结果生成阶段。

说明：
- 本轮已真实建立并跑通最小线性高斯鲁棒容量脚本，得到 reconstruction / task / robust 三类指标的同轮数据。
- 当前工作区中未找到此前记忆中记录的 round1 / round2 脚本与结果文件，因此这些旧条目暂不能继续按“已真实完成”计数。
- 现在真正可追溯的证据起点，是本轮已跑通并落盘的 round3 robust 最小平台。

## 当前唯一主瓶颈
虽然本轮已经真实得到“理想任务最优不等于鲁棒最优”的最小信号，但还没有把这条信号推进成 Nature Communications 级别可接受的完整证据链。

具体表现：
- `RCR` 目前只有第一版操作性定义与真实计算结果，尚未写成可检查推导链。
- reconstruction / task / robust 三者的排序关系只在当前最小线性高斯 surrogate 上验证。
- Figure 5 所需的鲁棒面板数据虽然已有接口，但还没有投稿级正文图与补充图。
- 参考文献仍明显不足，且当前工作区内没有可核对的 30+ 文献链。

## 本轮唯一最高优先级
建立并真实跑通第三轮最小鲁棒容量实验。

本轮只聚焦一件事：
- 给出 ideal reconstruction、ideal task 与 robust retention 的同轮对照结果
- 确认真正发生的是“理想任务最优”和“鲁棒最优”的排序分离
- 为下一轮 `RCR` 推导文稿和 Figure 5 数据映射提供真实输入

## 本轮交付物
1. 第三轮最小鲁棒容量真实计算脚本
2. 第三轮结果表、总结文件、运行日志与矢量总览图
3. 更新后的阶段判定、瓶颈与下一轮动作
4. 对旧记忆中“找不到实际文件”的已完成条目进行纠偏

## 完成标准
本轮仅在以下内容全部满足时视为完成：
- 已真实跑通第三轮最小鲁棒容量线性高斯脚本
- 已生成结果表、总结文件、运行日志和矢量总览图
- 已确认 ideal task-optimal 与 robustness-optimal 排序分离
- 已将本轮真实产出写入项目状态文件

## 项目停止条件
只有在以下条件同时满足后，项目才允许停止自动推进：
1. Nature Communications 五位审稿人的接收概率判断都大于 70%
2. 所有需要补的 evidence 均已补齐
3. 所有正文图和补充材料图均已补齐，其中数据图全部来自真实数据
4. 所有关键理论推导均已补齐并通过可检查性要求
5. 参考文献已补齐到 30 篇以上并完成核对

## 下一轮立即动作
1. 写出本轮 `RCR` 的第一版详细推导文稿，并明确其与 `task_mi`、mismatched risk 的关系
2. 把本轮真实结果整理成 Figure 5 的正式面板字段与图注框架
3. 扩展扰动模型，补做 task variable 敏感性与参数稳健性扫描
4. 开始系统扩充参考文献到 20 篇以上的中间里程碑
5. 为后续 PSF / depth 平台准备统一符号和任务映射

## 已真实完成
- 已识别目标期刊为 Nature Communications。
- 已完成项目初始化编排与持续迭代框架设计。
- 已在 `/workspace/computational-imaging-2-ncomms/linear_gaussian_round3_robust.py` 建立第三轮最小鲁棒容量真实计算脚本。
- 已真实生成第三轮结果文件：
  - `linear_gaussian_round3_robust_results.csv`
  - `linear_gaussian_round3_robust_summary.json`
  - `linear_gaussian_round3_robust_summary.md`
  - `linear_gaussian_round3_robust_overview.svg`
  - `linear_gaussian_round3_robust_run.log`
- 已得到第三轮关键结果：
  - `identity` 在 reconstruction MI 上最优，`recon_mi = 4.3228 nats`
  - `task_matched_diag` 在 ideal task MI 上最优，`task_mi = 2.8652 nats`
  - `hadamard_like` 在 `RCR` 上最优，`RCR = 0.9979`
  - `hadamard_like` 的 robust mismatched task risk 最低，`robust_task_risk_mean = 0.1300`
  - 因此已真实观察到 ideal task-optimal 与 robustness-optimal 的排序分离

## 已部分完成但仍缺关键环节
- 文献：30+ 已核对参考文献仍未建立。
- 理论：本轮 `RCR` 已有第一版操作性定义和真实计算，但详细推导仍未完成。
- 图表：已有一张基于真实结果的 round3 SVG 总览图，但离投稿级正文图和补充材料图仍有距离。
- 可复核性：此前记忆中记录的 round1 / round2 文件当前工作区未找到，因此这些条目只能算“待重建”，不能继续算已完成。

## 尚未开始
- 全套理论推导文稿
- 已验证的 round1 / round2 复现实验链
- PSF / depth 平台真实计算
- 正文和补充材料正式图生成
- 五位审稿人并行评审循环
- 最终投稿归档包

## 参考文献状态
- 当前已核对参考文献数：0
- 目标下限：30
- 当前判断：明显不足，尚不能支撑 Nature Communications 级别的引言、讨论和补充材料文献链

## 当前接收概率判断
- 综合接收概率：18%–26%

依据：
- 创新构想：强
- 理论充分性：弱到中
- 方法与代码可靠性：中
- 数据与结果完整性：弱到中
- 图表质量：弱到中
- 写作成熟度：弱
- 期刊匹配度：中到强

当前最拖累接收概率的短板：
1. `RCR` 只有操作性结果，缺少可检查推导与正文级理论叙述链
2. 当前只有 round3 最小平台真实可追溯，round1 / round2 仍需重建或复现
3. 参考文献、补充材料与跨平台验证远未补齐

## 最近一次重要更新摘要
2026-04-26：已真实跑通第三轮最小鲁棒容量线性高斯脚本，首次在当前可追溯工作区内观察到 ideal task-optimal 与 robustness-optimal 的排序分离。同时发现此前记忆中的 round1 / round2 文件当前工作区未找到，因此这些旧条目已从“已真实完成”中剔除，下一轮将转向 `RCR` 推导固化与 Figure 5 数据映射。
