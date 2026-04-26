# 角色任务表：计算成像1

## 统筹者
- 当前任务：维护项目阶段判断、主瓶颈、每轮唯一最高优先级和跨模块依赖关系
- 输入：上传项目草案、期刊门槛、各角色最新真实产出
- 输出：每轮状态更新、优先级调整、里程碑判定
- 完成标准：任何时刻都能明确当前阶段、当前主瓶颈、本轮最高优先级、交付物和下一轮动作
- 依赖：全部角色的真实完成状态
- 优先级：最高
- 最近完成产出：完成 round9 连续扫参后的阶段重判，确认当前唯一主瓶颈已从“orientation bias 是否驱动翻转”收缩为“去偏置后 residual bias 是否归零”
- 下一步交付物：去偏置或后验平均型 baseline 的唯一最高优先级重排

## 理论人员
- 当前任务：在 round9 已确认 orientation ratio 可连续驱动 branch sign 跨零的基础上，继续维护 exact / empirical 边界，并把下一轮检验收缩为“对称先验下 residual bias 是否仍非零”
- 输入：统一 forward model、线性与非线性任务定义、likelihood / prior 形式
- 输出：
  - round6 指标说明维护版
  - exact ambiguity pair 下仍适用的 exact / empirical 判据
  - symmetric prior 下 residual branch bias 的理论检查项
- 完成标准：
  - 所有新 phase 结果都必须落入 round6 定义的三层量中
  - 不把经验 branch bias 写成精确 ambiguity 定理
  - 不把 orientation-biased prior 的分支偏向写成可推广结论
- 依赖：round6 指标说明已形成
- 优先级：P2

## 代码与数值计算人员
- 当前任务：以 round6 指标说明为约束，在 round9 已确认连续 crossing 的基础上，优先补去偏置或后验平均型 baseline
- 输入：任务定义、噪声模型、baseline 清单
- 输出：
  - 去偏置或后验平均型新 baseline
  - symmetric prior 下的 `recovered_measurement_error` 与 `branch_bias`
  - residual bias 是否接近零的直接证据
- 完成标准：
  - 新输出字段直接继承 round6 定义
  - 能判断去偏置后 residual branch bias 是否收敛到接近零
- 依赖：理论人员给出 round6 统一评价指标
- 优先级：P1

## 数据分析人员
- 当前任务：比较 round5、round7、round8 与 round9，重点判断 branch sign 是否已被 orientation bias 解释，以及 residual bias 是否还需额外机制
- 输入：baseline 输出、误差图、数据一致性指标、posterior variance 或 sample spread
- 输出：
  - branch distance 对照表
  - measurement consistency 与 branch selection 对照表
  - solver failure、prior family 与 orientation ratio 的分离分析
  - residual bias 是否仍显著的判断
- 完成标准：
  - 能区分普通 solver failure 与可重复的 branch preference
  - 能指出对称先验下是否还需要继续排查 architecture / optimizer 隐式偏置
- 依赖：新的 phase baseline 结果
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
- 最近完成产出：确认 round8 与 round9 都属于真实新进展，但当前只能写成“branch sign 对 prior family 与 orientation ratio 敏感”，不能写成稳定或普适分支规律
- 下一步交付物：下一轮继续盯住是否把 orientation-driven crossing 误写成已完成机制闭环

## 严格审稿人
- 当前任务：暂不启动正式五审稿人循环，只维护预审入口条件
- 输入：阶段性结果、图表、推导、文稿
- 输出：是否具备进入正式五审稿人评估的判定
- 完成标准：
  - 只有当至少形成一版可审稿稿件与核心图表后，才进入正式五审稿人评估
- 依赖：理论、结果、图表、写作均形成可审材料
- 优先级：后置

## 当前依赖主链
1. 统筹者锁定“先分清 exact ambiguity 与 empirical branch bias，再强化 solver”的路线
2. 线性 benchmark 已形成可复核区域定义与指标输出
3. round6 已把 phase ambiguity 的三个层级量固定下来
4. 代码与数值计算人员已据此完成 round7 的低 measurement-error rebuilt solver
5. 代码与数值计算人员已继续完成 round8 的 prior-family / seed / init 稳健性扫描
6. 代码与数值计算人员已进一步完成 round9 的 orientation-ratio 连续扫参
7. 数据分析人员据此判断 branch sign 会在 `ratio=0.5` 附近跨零，而不仅是三档 family 之间跳变
8. 后续再由画图人员定义 Figure 4 的正式面板结构，并由撰写人员改写 Results/Methods 入口

## 本轮唯一最高优先级任务拆解
- 任务名称：对称先验下的 residual branch-bias 检验
- 负责人：统筹者 + 代码与数值计算人员
- 预期输出：
  - 去偏置或后验平均型新 baseline
  - 在 round6 判据下可直接比较的新 branch 指标
  - residual branch bias 是否接近零的判断依据
- 完成标准：
  - 已在当前环境真实完成对称先验检验
  - 已确认去偏置后 residual branch bias 是接近零还是仍显著非零
