# 角色任务表：self-calibrating-diffractive-ncomms

## 当前阶段
最小机制验证已完成，下一步进入 wave-optics 最小阳性对照构建。

## 当前唯一主瓶颈
缺少 ordinary D2NN vs pilot-assisted D2NN 的真实 wave-optics 对照结果。

## 角色任务

### 统筹者
- 当前任务：把 surrogate 机制验证切换成真实 coherent propagation 最小闭环
- 输入：上传提案、round1 结果、环境状态
- 输出：round2 唯一目标、完成标准、风险边界
- 完成标准：后续所有任务只围绕 Zernike 动态像差下的最小阳性对照推进
- 优先级：最高

### 理论人员
- 当前任务：把 Gaussian surrogate 的结论和边界整理成“只支持继续推进，不支持成稿”的明确理论脚手架
- 输入：`round1_theory_note.md`
- 输出：round2 wave-optics 条件下的 forward model、reference 共路/非共路定义、可检验假设
- 完成标准：ordinary vs pilot-assisted 对照的理论对象和边界写清
- 优先级：高

### 代码与数值计算人员
- 当前任务：实现最小 coherent propagation + Zernike 动态像差 + ordinary / pilot-assisted 对照
- 输入：上传提案中的 Result 1 / Result 2 框架，round1 结果
- 输出：round2 脚本、CSV、summary、图文件、运行日志
- 完成标准：至少得到一轮真实可复核的 ordinary vs pilot-assisted OOD 对照
- 优先级：最高

### 数据分析人员
- 当前任务：定义 round2 最小成功标准
- 输入：round1 指标与项目主张
- 输出：round2 指标表头、对照规则、失败判据
- 完成标准：明确哪些结果算阳性，哪些结果意味着方向需降级
- 优先级：高

### 画图人员
- 当前任务：维持“所有正式数据图必须来自真实计算”的约束
- 输入：round2 原始输出
- 输出：只生成真实数据图；概念示意图若需要可后续由 GPT-imag-2.0 起草
- 完成标准：不提前制造装饰性定稿图
- 优先级：中

### 论文撰写人员
- 当前任务：暂不写主文，先为后续引言和机制段准备边界语言
- 输入：项目主张与 round1 边界
- 输出：仅限 claim boundary 备忘，不生成过早摘要定稿
- 完成标准：不出现结论强于证据
- 优先级：中

### 监督 / 审稿环节
- 当前任务：每轮检查是否把 surrogate 结果误写成 D2NN 结果
- 输入：代码、summary、状态文件
- 输出：监督意见与接收概率更新
- 完成标准：发现过度陈述立即纠偏
- 优先级：最高
