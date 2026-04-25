# 角色任务表：计算成像1

## 统筹者
- 当前任务：维护项目阶段判断、主瓶颈、每轮唯一最高优先级和跨模块依赖关系
- 输入：上传项目草案、期刊门槛、各角色最新真实产出
- 输出：每轮状态更新、优先级调整、里程碑判定
- 完成标准：任何时刻都能明确当前阶段、当前主瓶颈、本轮最高优先级、交付物和下一轮动作
- 依赖：全部角色的真实完成状态
- 优先级：最高

## 理论人员
- 当前任务：把 round5 相位恢复结果写成统一、可检查的 phase ambiguity 指标说明，明确 exact 结论与 empirical 结论的边界
- 输入：统一 forward model、线性与非线性任务定义、likelihood / prior 形式
- 输出：
  - phase retrieval 中 true / reversed ambiguity branch 的统一符号表
  - exact ambiguity quantity 与 empirical branch-selection quantity 的区分说明
  - `recovered_measurement_error`、`distance_to_true`、`distance_to_reversed`、`branch_bias` 的正式定义
  - 相位恢复局部指标与 DSI / ambiguity branch 的第一版接口说明
- 完成标准：
  - 每个关键结论都有连续推导，而不是概念口号
  - 清楚区分已证明结果、近似结果和待验证命题
- 依赖：round5 结果已固定
- 优先级：P1

## 代码与数值计算人员
- 当前任务：审计并补强 round5 相位恢复 learned-prior baseline 的 measurement consistency 口径，为下一轮 solver 强化做准备
- 输入：任务定义、噪声模型、baseline 清单
- 输出：
  - round5 脚本与输出字段说明
  - latent restarts / measurement error 的诊断记录
  - 是否需要下一轮优先降低 measurement error 的判断依据
- 完成标准：
  - 现有输出字段能直接映射到理论人员定义的 branch 指标
  - 明确当前 baseline 的能力边界，而不是含糊写成“已解决”
- 依赖：理论人员给出统一评价指标
- 优先级：P2

## 数据分析人员
- 当前任务：把 round5 的 branch bias 与 measurement error 组合成可写入 Results 的结构化结论
- 输入：baseline 输出、误差图、数据一致性指标、posterior variance 或 sample spread
- 输出：
  - branch distance 对照表
  - measurement consistency 与 branch selection 对照表
  - 相位恢复 learned-prior 偏向解读
  - 第一版高风险失败案例归纳
- 完成标准：
  - 能区分普通误差与疑似 hallucination
  - 能指出需要补充的对照实验
- 依赖：代码与数值计算结果
- 优先级：P2

## 画图人员
- 当前任务：把 round4 线性结果转化为 Figure 2 理论-现象联动图的字段需求，而不是提前定稿
- 输入：图 1-6 草案、统一变量命名、配色与面板逻辑
- 输出：
  - 图表风格规范
  - Figure 1 概念图需求清单
  - 真实结果图的数据字段规范
- 完成标准：
  - 图表模板与数据字段能够直接承接后续真实结果
  - 不把任何示意图误当正式结果
- 依赖：统筹者确定图表结构
- 优先级：P3

## 论文撰写人员
- 当前任务：建立“最小结果如何进入引言与结果段”的文本接口，但不提前下强结论
- 输入：论文定位、期刊标准、图表规划、理论框架
- 输出：
  - 标题候选
  - 摘要占位框架
  - 引言逻辑骨架
  - Results/Methods/Supplementary 章节骨架
  - 与 42 条工作文献对应的引用角色分配
- 完成标准：
  - 写作结构与目标期刊相匹配
  - 所有主张都明确标记其所需证据
- 依赖：统筹者与理论人员
- 优先级：P3

## 监督人员
- 当前任务：检查是否出现“把草案包装成完成成果”的倾向
- 输入：全部角色产出
- 输出：
  - 阶段性质检意见
  - 禁止提前宣称完成的条目
  - 下一轮风险提醒
- 完成标准：
  - 所有未闭合证据链都被明确标记
  - 所有不满足 First Principle 的内容都不计入完成项
- 依赖：全部角色
- 优先级：最高

## 严格审稿人
- 当前任务：暂不启动正式五审稿人循环，只维护预审入口条件
- 输入：阶段性结果、图表、推导、文稿
- 输出：是否具备进入正式五审稿人评估的判定
- 完成标准：
  - 只有当至少形成一版可审稿稿件与核心图表后，才进入正式五审稿人评估
- 依赖：理论、结果、图表、写作均形成可审材料
- 优先级：后置

## 当前依赖主链
1. 统筹者锁定“从 toy prior 走向学习型 prior”的升级路线
2. 线性 benchmark 已形成可复核区域定义与指标输出
3. 代码与数值计算人员已在 phase retrieval 最小任务上接入真实 learned decoder prior baseline，并跑出 round5 结果
4. 理论人员把 phase ambiguity 的 exact quantity 与 learned-prior branch-selection quantity 写成统一判据
5. 数据分析人员建立 branch distance 与 measurement consistency 对照表
6. 画图人员定义 Figure 2 / Figure 4 的正式面板结构
6. 撰写人员再写结果段与方法段

## 本轮唯一最高优先级任务拆解
- 任务名称：把 round5 相位恢复结果推进到统一、可检查的 phase ambiguity 指标说明
- 负责人：统筹者 + 理论人员 + 代码与数值计算人员
- 预期输出：
  - exact / empirical phase ambiguity 量的区分说明
  - 与 round5 输出字段一一对应的指标定义
  - 下一轮是否优先强化 solver 的判断依据
- 完成标准：
  - 不是“看图解释”的口头复述，而是“把 round5 的真实结果写成可检查判据”
