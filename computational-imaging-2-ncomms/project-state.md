# 项目状态：计算成像2

## 项目基本信息
- 项目名称：计算成像2
- 目标期刊：Nature Communications
- 最近更新时间：2026-04-26
- 当前资料来源：`/workspace/user_files/01-1-.txt`

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
- 第一轮真实计算已经建立了 reconstruction-oriented baseline。
- 第二轮真实计算已经在同一线性高斯框架下引入 task variable，并得到 reconstruction-optimal 与 task-optimal 排序分离的首个真实例子。
- 但这条证据链仍局限于当前 surrogate 模型，尚未扩展到更强的理论推导、鲁棒容量、PSF 平台和投稿级图表体系。

## 当前唯一主瓶颈
虽然第二轮已经得到“重建最优不等于任务最优”的真实信号，但还没有把这一信号推进成 Nature Communications 级别可接受的完整证据链。

具体表现：
- TIG 已有第一版可计算定义，但推导文稿尚未写成可检查链条。
- 任务最优与重建最优的分离目前只在一个线性 surrogate 任务上验证。
- RCR 与鲁棒误差链尚未启动。
- 图表仍停留在首版总览图，离正文 Figure 2 / Figure 4 和补充材料图还有距离。
- 参考文献仍只有 12 篇种子文献。

## 本轮唯一最高优先级
把第二轮排序分离结果推进成“可写入论文 Results 的最小理论-数值闭环”。

本轮只聚焦一件事：
- 固定 OIG、PIE、TIG 的第一版数学定义
- 把第二轮 task-weighted 结果整理成 Figure 2 / Figure 4 的正式数据接口
- 为下一轮鲁棒容量实验设计最小误差模型

## 本轮交付物
1. 第二轮 task-weighted 真实计算脚本
2. 第二轮结果表、总结文件与矢量总览图
3. 更新后的阶段判定、瓶颈与下一轮动作
4. 已持续运行的小时级自动迭代安排

## 完成标准
本轮仅在以下内容全部满足时视为完成：
- 已真实跑通第二轮 task-weighted 线性高斯计算脚本
- 已生成结果表、总结文件和矢量总览图
- 已确认 reconstruction-optimal 与 task-optimal 排序分离
- 已将本轮真实产出写入项目状态文件

## 下一轮立即动作
1. 写出 OIG、PIE、TIG 的第一版推导文稿
2. 从第二轮结果中整理 Figure 2 和 Figure 4 的正式面板字段
3. 启动第三轮鲁棒容量最小实验，加入 calibration / throughput / mismatch 扰动
4. 开始扩充参考文献到 20 篇以上的中间里程碑
5. 为后续 PSF / depth 平台准备统一符号和任务映射

## 已真实完成
- 已从上传材料中抽取项目名称、英文标题、研究主线、图表规划、实施方案与 12 篇种子参考文献。
- 已识别目标期刊为 Nature Communications。
- 已完成项目初始化编排与持续迭代框架设计。
- 已在 `/workspace/computational-imaging-2-ncomms/linear_gaussian_round1.py` 建立第一轮线性高斯真实计算脚本。
- 已在 `/workspace/computational-imaging-2-ncomms/linear_gaussian_round2_task.py` 建立第二轮 task-weighted 真实计算脚本。
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
- 已得到第二轮关键结果：
  - `identity` 仍在 reconstruction MI 上最优，`recon_mi = 26.5029`
  - `task_matched_diag` 在 task MI 上最优，`task_mi = 9.3260`
  - `task_matched_diag` 相对 `identity` 的 `TIG = +7.5241 nats`
  - `task_matched_diag` 的 `task_risk_per_dim = 0.0068`，显著优于 `identity` 的 `0.0444`
  - 因此已真实观察到 reconstruction-optimal 与 task-optimal 的排序分离

## 已部分完成但仍缺关键环节
- 文献：已有 12 篇种子文献，但未补足到 30+，且尚未完成主题分组与逐条核对。
- 理论：OIG、PIE、TIG 已进入第一版可计算状态，但详细推导和 RCR 仍未完成。
- 图表：已有两张基于真实结果的 SVG 总览图，但离投稿级正文图和补充材料图仍有距离。
- 任务规划：线性验证线已推进到第二轮，其余 PSF、任务容量跨平台验证、鲁棒容量 3 条验证线尚未真实运行。

## 尚未开始
- 全套理论推导文稿
- 第三轮鲁棒容量真实计算
- PSF / depth 平台真实计算
- 正文和补充材料正式图生成
- 五位审稿人并行评审循环
- 最终投稿归档包

## 参考文献状态
- 当前已提取种子文献数：12
- 目标下限：30
- 当前判断：明显不足，尚不能支撑 Nature Communications 级别的引言、讨论和补充材料文献链

## 当前接收概率判断
- 综合接收概率：16%–24%

依据：
- 创新构想：强
- 理论充分性：中
- 方法与代码可靠性：中到强
- 数据与结果完整性：弱到中
- 图表质量：中
- 写作成熟度：弱
- 期刊匹配度：中到强

当前最拖累接收概率的短板：
1. 还没有鲁棒容量与跨平台验证，核心命题支撑面仍偏窄
2. 没有闭合的理论推导与正文级叙述链
3. 参考文献、补充材料与后续验证线远未补齐

## 最近一次重要更新摘要
2026-04-26：第二轮 task-weighted 线性高斯脚本已真实跑通，首次观察到 reconstruction-optimal 与 task-optimal 的排序分离。下一轮将转向指标推导固化与鲁棒容量最小实验。
