# 角色任务表：计算成像1

## 统筹者
- 当前任务：维护项目阶段判断、主瓶颈、每轮唯一最高优先级和跨模块依赖关系
- 输入：上传项目草案、期刊门槛、各角色最新真实产出
- 输出：每轮状态更新、优先级调整、里程碑判定
- 完成标准：任何时刻都能明确当前阶段、当前主瓶颈、本轮最高优先级、交付物和下一轮动作
- 依赖：全部角色的真实完成状态
- 优先级：最高

## 理论人员
- 当前任务：把线性 observation mask 下的 zero-fill / PCA / autoencoder / latent inverse 差异转写成第一版可计算判据
- 输入：统一 forward model、线性与非线性任务定义、likelihood / prior 形式
- 输出：
  - 统一数学符号表
  - 线性 incomplete measurement 下的 data-supported / unsupported 区域判据
  - bridge intensity、unsupported-region error 与 observed-region error 的定义草案
  - 相位恢复 reversed ambiguity 的测量等价说明
  - DSI / ambiguity branch 的第一版数学说明
- 完成标准：
  - 每个关键结论都有连续推导，而不是概念口号
  - 清楚区分已证明结果、近似结果和待验证命题
- 依赖：forward model 设定与实验场景固定
- 优先级：P1

## 代码与数值计算人员
- 当前任务：维护 round4 线性 benchmark 结果可复核性，并为下一轮指标公式化提供一致的数据接口
- 输入：任务定义、噪声模型、baseline 清单
- 输出：
  - 已完成的 autoencoder prior 与 latent inverse prior 脚本及结果文件
  - 下一轮统一指标计算接口
  - iterative phase-retrieval baseline
  - 运行日志与失败案例表
- 完成标准：
  - 当前线性任务基础上已经产出 measurement-consistent learned prior 真实结果
  - round4 结果字段与像素区域能够无歧义映射到理论定义
  - 至少一组结果能展示“相同或近似相同测量对应不同结构”的案例
- 依赖：理论人员给出统一评价指标
- 优先级：P1

## 数据分析人员
- 当前任务：对 zero-fill、PCA prior、autoencoder projection 与 latent inverse 的差异做结构性判读，特别是区分观测区与未观测区误差
- 输入：baseline 输出、误差图、数据一致性指标、posterior variance 或 sample spread
- 输出：
  - observed / unsupported 区域误差对照表
  - bridge intensity 指标表
  - round4 四方法对照解读
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
- 输出：是否具备进入严格审稿循环的判定
- 完成标准：
  - 只有当至少形成一版可审稿稿件与核心图表后，才进入正式五审稿人评估
- 依赖：理论、结果、图表、写作均形成可审材料
- 优先级：后置

## 当前依赖主链
1. 统筹者锁定“从 toy prior 走向学习型 prior”的升级路线
2. 代码与数值计算人员在第 1 轮脚本基础上接入真实 prior
3. 理论人员把 observation mask 和 phase ambiguity 结果写成判据
4. 数据分析人员建立 observed / unsupported 区域误差表
5. 画图人员定义 Figure 1 / Figure 2 的正式面板结构
6. 撰写人员再写结果段与方法段

## 本轮唯一最高优先级任务拆解
- 任务名称：把 round4 线性四方法结果写成统一可计算判据
- 负责人：统筹者 + 理论人员 + 代码与数值计算人员
- 预期输出：
  - observed / unsupported / bridge 三类区域的正式定义
  - 与 round4 数据字段一一对应的指标计算式
  - 能直接接到结果段与方法段的定义说明
- 完成标准：
  - 不是“想好怎么写”，而是“给出可检查公式并和真实结果文件对齐”
