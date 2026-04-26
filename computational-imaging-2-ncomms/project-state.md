# 项目状态：计算成像2

## 项目基本信息
- 项目名称：计算成像2
- 目标期刊：Nature Communications
- 最近更新时间：2026-04-26
- 当前资料来源：`/workspace/user_files/01-1-.txt`

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
理论强化与结果生成已启动阶段。

说明：
- 第一轮真实计算已经建立 reconstruction-oriented baseline。
- 第二轮真实计算已经得到 reconstruction-optimal 与 task-optimal 排序分离的首个真实例子。
- 第三轮真实计算已经给出第一版 robust surrogate 结果与 RCR 初稿。
- 第四轮真实计算已经完成更强扰动族扫描，并给出“到当前扫描上限仍未出现 robust ranking flip”的边界条件。

## 当前唯一主瓶颈
当前最限制投稿质量提升的瓶颈，已经从“有没有鲁棒结果”转成“如何把未翻转边界条件与 RCR 推导组织成有说服力的理论结论”，同时还需要跨平台证据来避免整篇文章过度依赖线性 surrogate。

具体表现：
- 第四轮把 severity 扫描到 2.5 后，`task_matched_diag` 仍保持 best robust code，说明当前并未观察到 robust ranking flip。
- 当前结果更像“边界图谱”而不是“翻转证据”，需要理论解释为什么会这样。
- OIG、PIE、TIG、RCR 仍未写成连续推导文稿。
- 图表仍停留在总览图级别，正文 Figure 2 / Figure 4 / Figure 5 尚未正式成图。
- 参考文献仍只有 12 篇种子文献。

## 本轮唯一最高优先级
把第四轮“未翻转边界条件”推进成可写入论文的鲁棒性结果，并同步启动理论推导文稿。

本轮只聚焦一件事：
- 固定 RCR 与 robust score 的第一版数学定义
- 把第四轮 stronger-perturbation 扫描整理成 Figure 5 的正式数据接口
- 写出为什么当前没有出现 robust flip 的边界解释

## 本轮交付物
1. 第四轮更强扰动族扫描真实计算脚本
2. 第四轮结果表、总结文件与矢量总览图
3. 更新后的阶段判定、瓶颈与下一轮动作
4. 已持续运行的每 2 小时自动迭代安排

## 完成标准
本轮仅在以下内容全部满足时视为完成：
- 已真实跑通第四轮更强扰动族扫描脚本
- 已生成结果表、总结文件和矢量总览图
- 已明确记录“扫描到 severity 2.5 仍未观察到 robust flip”的边界条件
- 已将本轮真实产出写入项目状态文件

## 项目停止条件
只有在以下条件同时满足后，项目才允许停止自动推进：
1. Nature Communications 五位审稿人的接收概率判断都大于 70%
2. 所有需要补的 evidence 均已补齐
3. 所有正文图和补充材料图均已补齐，其中数据图全部来自真实数据
4. 所有关键理论推导均已补齐并通过可检查性要求
5. 参考文献已补齐到 30 篇以上并完成核对

## 下一轮立即动作
1. 写出 OIG、PIE、TIG、RCR 的第一版推导文稿
2. 从前四轮结果中整理 Figure 2、Figure 4、Figure 5 的正式面板字段
3. 启动第五轮任务定义与扰动结构联合扫描，测试是否存在真正的 robust flip 区域
4. 开始扩充参考文献到 20 篇以上的中间里程碑
5. 为后续 PSF / depth 平台准备统一符号和任务映射

## 已真实完成
- 已从上传材料中抽取项目名称、英文标题、研究主线、图表规划、实施方案与 12 篇种子参考文献。
- 已识别目标期刊为 Nature Communications。
- 已完成项目初始化编排与持续迭代框架设计。
- 已在 `/workspace/computational-imaging-2-ncomms/linear_gaussian_round1.py` 建立第一轮线性高斯真实计算脚本。
- 已在 `/workspace/computational-imaging-2-ncomms/linear_gaussian_round2_task.py` 建立第二轮 task-weighted 真实计算脚本。
- 已在 `/workspace/computational-imaging-2-ncomms/linear_gaussian_round3_robust.py` 建立第三轮 robust surrogate 真实计算脚本。
- 已在 `/workspace/computational-imaging-2-ncomms/linear_gaussian_round4_stress_scan.py` 建立第四轮更强扰动族扫描脚本。
- 已真实生成第一轮结果文件：
  - `linear_gaussian_round1_results.csv`
  - `linear_gaussian_round1_summary.json`
  - `linear_gaussian_round1_summary.md`
  - `linear_gaussian_round1_overview.svg`
- 已真实生成第二轮结果文件：
  - `linear_gaussian_round2_task_results.csv`
  - `linear_gaussian_round2_task_summary.json`
  - `linear_gaussian_round2_task_summary.md`
  - `linear_gaussian_round2_task_overview.svg`
- 已真实生成第三轮结果文件：
  - `linear_gaussian_round3_robust_results.csv`
  - `linear_gaussian_round3_robust_summary.json`
  - `linear_gaussian_round3_robust_summary.md`
  - `linear_gaussian_round3_robust_overview.svg`
- 已真实生成第四轮结果文件：
  - `linear_gaussian_round4_stress_scan_results.csv`
  - `linear_gaussian_round4_stress_scan_summary.json`
  - `linear_gaussian_round4_stress_scan_summary.md`
  - `linear_gaussian_round4_stress_scan_overview.svg`
- 已得到第二轮关键结果：
  - `identity` 仍在 reconstruction MI 上最优，`recon_mi = 26.5029`
  - `task_matched_diag` 在 task MI 上最优，`task_mi = 9.3260`
  - `task_matched_diag` 相对 `identity` 的 `TIG = +7.5241 nats`
  - `task_matched_diag` 的 `task_risk_per_dim = 0.0068`，显著优于 `identity` 的 `0.0444`
  - 因此已真实观察到 reconstruction-optimal 与 task-optimal 的排序分离
- 已得到第三轮关键结果：
  - `task_matched_diag` 仍是 ideal best task code
  - `task_matched_diag` 仍是 best robust score code，说明本轮未出现 robust ranking flip
  - `task_matched_diag` 的 `robust_task_mi_mean = 9.0110`
  - `task_matched_diag` 的 `RCR = 0.9662`
  - `identity` 的 `RCR = 1.0044`，说明 direct baseline 保留率更稳，但绝对任务信息仍远低于 task-matched 设计
- 已得到第四轮关键结果：
  - severity 从 `0.5` 扫描到 `2.5`，best robust code 始终为 `task_matched_diag`
  - 当前扫描范围内未观察到 robust ranking flip
  - `task_matched_diag` 的 robust score 从 `8.2681` 随 severity 下降到 `4.1075`
  - `identity` 的 robust score 从 `1.7429` 下降到 `1.5387`
  - 当前结果给出了“到 severity 2.5 仍未翻转”的边界条件

## 已部分完成但仍缺关键环节
- 文献：已有 12 篇种子文献，但未补足到 30+，且尚未完成主题分组与逐条核对。
- 理论：OIG、PIE、TIG、RCR 已进入第一版可计算状态，但详细推导仍未完成。
- 图表：已有四张基于真实结果的 SVG 总览图，但离投稿级正文图和补充材料图仍有距离。
- 任务规划：线性验证线已推进到第四轮，其余 PSF、跨平台任务容量验证、扩展鲁棒容量 3 条验证线尚未真实运行。

## 尚未开始
- 全套理论推导文稿
- 第五轮任务定义与扰动结构联合扫描
- PSF / depth 平台真实计算
- 正文和补充材料正式图生成
- 五位审稿人并行评审循环
- 最终投稿归档包

## 参考文献状态
- 当前已提取种子文献数：12
- 目标下限：30
- 当前判断：明显不足，尚不能支撑 Nature Communications 级别的引言、讨论和补充材料文献链

## 当前接收概率判断
- 综合接收概率：23%–31%

依据：
- 创新构想：强
- 理论充分性：中
- 方法与代码可靠性：强
- 数据与结果完整性：中
- 图表质量：中
- 写作成熟度：弱
- 期刊匹配度：中到强

当前最拖累接收概率的短板：
1. 鲁棒容量目前只有“未翻转边界条件”，还缺更强证据与理论解释
2. 没有闭合的理论推导与正文级叙述链
3. 参考文献、补充材料与跨平台验证线远未补齐

## 最近一次重要更新摘要
2026-04-26：第四轮更强扰动族扫描已真实跑通，结果显示在当前扫描到的 severity 2.5 范围内仍未出现 robust ranking flip。下一轮将转向理论推导文稿与更高维联合扫描。
