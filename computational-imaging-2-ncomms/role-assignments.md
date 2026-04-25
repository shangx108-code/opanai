# 角色任务表：计算成像2

## 统筹者
- 当前任务：维护项目阶段判断、唯一主瓶颈、唯一最高优先级，并纠正“记忆记录”和“工作区真实文件”之间的差异
- 输入：Nature Communications 门槛、当前命名空间状态文件、本轮真实计算输出
- 输出：每轮状态更新、优先级调整、已完成/未完成重新判定
- 最近完成产出：已确认 round3 robust 是当前工作区内首个可完整追溯的真实证据点
- 下一步交付物：更新后的阶段判断与 Figure 5 推进路线
- 完成标准：任何时刻都能明确当前阶段、当前主瓶颈、本轮最高优先级、交付物和下一轮动作
- 依赖：全部角色的真实完成状态
- 优先级：最高

## 理论人员
- 当前任务：把本轮 `RCR` 的操作性定义写成可检查推导链
- 输入：`linear_gaussian_round3_robust.py` 中的 forward model、任务映射、扰动模型、真实结果表
- 输出：
  - `RCR` 第一版详细推导文稿
  - `task_mi`、mismatched task risk 与 `RCR` 的关系说明
  - 明确哪些步骤是定义、哪些步骤是推导、哪些是假设
- 最近完成产出：`RCR = robust_task_mi_mean / ideal_task_mi` 的第一版操作性计算路径已固定
- 下一步交付物：可检查的 `RCR` 推导说明
- 完成标准：每个关键结论都有连续推导，而不是概念口号
- 依赖：本轮 round3 真实结果
- 优先级：P1

## 代码与数值计算人员
- 当前任务：在 round3 最小平台基础上补做敏感性与参数扫描
- 输入：本轮真实脚本、当前扰动模型、任务变量定义
- 输出：
  - round3 参数敏感性扩展结果
  - task variable 改动下的排序稳定性记录
  - 更新后的运行日志
- 最近完成产出：
  - `/workspace/computational-imaging-2-ncomms/linear_gaussian_round3_robust.py`
  - `linear_gaussian_round3_robust_results.csv`
  - `linear_gaussian_round3_robust_summary.json`
  - `linear_gaussian_round3_robust_summary.md`
  - `linear_gaussian_round3_robust_overview.svg`
  - `linear_gaussian_round3_robust_run.log`
- 下一步交付物：参数扫描后的 round3 扩展结果表
- 完成标准：不只是“已有鲁棒脚本”，而是“已真实运行并留下扩展结果”
- 依赖：理论人员固定下一轮需要对齐的判据
- 优先级：P1

## 数据分析人员
- 当前任务：把本轮同轮 reconstruction / task / robust 结果整理成可写入 Results 的判读记录
- 输入：round3 结果表和总结文件
- 输出：
  - ideal vs robust 排序翻转判读表
  - `RCR` 与 robust task risk 的一致性检查表
  - 需要追加的对照分析清单
- 最近完成产出：已确认 `task_matched_diag` 为 ideal task-optimal，而 `hadamard_like` 为 robustness-optimal
- 下一步交付物：Figure 5 的数据解释提纲
- 完成标准：能明确说明本轮结果支持什么，不支持什么
- 依赖：round3 真实结果
- 优先级：P2

## 画图人员
- 当前任务：把本轮 round3 数据推进到 Figure 5 的正式字段规范
- 输入：round3 CSV、summary、SVG、统一变量命名
- 输出：
  - Figure 5 面板字段映射表
  - 图注所需定量句子草案
  - 补充图中参数扫描面板的预留字段
- 最近完成产出：已有 round3 overview SVG，可作为 Figure 5 的临时数据底稿
- 下一步交付物：Figure 5 数据映射表
- 完成标准：所有数据图都能追溯到真实结果文件，不把当前 overview 图直接当投稿图
- 依赖：数据分析人员完成判读
- 优先级：P2

## 论文撰写人员
- 当前任务：把 round3 结果接入 Results 和 Methods 的最小写作骨架
- 输入：round3 真实结果、理论推导草案、Figure 5 字段映射
- 输出：
  - Results 中“robust capacity minimal benchmark”段落骨架
  - Methods 中扰动模型与 `RCR` 计算段落骨架
  - 每段主张对应的证据需求表
- 最近完成产出：写作入口条件已从“只有路线图”提升为“已有真实 round3 数据”
- 下一步交付物：Results/Methods 双段骨架
- 完成标准：所有主张都明确标记其所需证据，不提前包装普适结论
- 依赖：理论人员与画图人员
- 优先级：P3

## 监督人员
- 当前任务：检查是否把本轮 round3 结果过度推广，并监督旧记忆条目的纠偏
- 输入：全部角色产出
- 输出：
  - 阶段性质检意见
  - 对“找不到实际文件”的旧条目做降级处理
  - 下一轮风险提醒
- 最近完成产出：已确认此前记忆中 round1 / round2 文件当前工作区未找到，不能继续计入已完成
- 下一步交付物：监督轮次 3 的正式记录
- 完成标准：所有不满足 First Principle 的内容都不计入完成项
- 依赖：全部角色
- 优先级：最高

## 严格审稿人
- 当前任务：继续维持预审入口条件，不启动正式五审稿人循环
- 输入：阶段性结果、图表、推导、文稿
- 输出：是否具备进入严格审稿循环的判定
- 最近完成产出：更新预审门槛，要求 round1 / round2 复现链也必须补齐
- 下一步交付物：下一次阶段性接收概率更新
- 完成标准：只有当正文、图表、推导、文献链和可复核性都形成后，才进入正式五审稿人评估
- 依赖：理论、结果、图表、写作均形成可审材料
- 优先级：后置

## 当前依赖主链
1. 理论人员写出 `RCR` 第一版详细推导
2. 数据分析人员固定 round3 的排序解释与限制条件
3. 画图人员整理 Figure 5 字段映射
4. 代码与数值计算人员补跑参数扫描
5. 撰写人员将 round3 结果写入 Results / Methods 骨架
6. 监督人员检查是否仍有未校正的“记忆代替证据”问题

## 本轮唯一最高优先级任务拆解
- 任务名称：第三轮鲁棒容量最小实验
- 负责人：统筹者 + 代码与数值计算人员
- 实际完成情况：已完成
- 已输出：
  - 第三轮误差模型参数化脚本
  - reconstruction / task / `RCR` 对照结果表
  - ideal 与 robust 排序变化记录
  - 运行日志与总览 SVG
- 完成标准核对：
  - 第三轮脚本已真实跑通
  - 已留下可检查结果文件
  - 已证明当前最小模型里 ideal task-optimal 与 robustness-optimal 不一致
