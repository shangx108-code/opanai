# 角色任务表：self-calibrating-diffractive-ncomms

## 当前阶段
wave-optics 最小阳性对照、round3 理论补强和 round4 cross-task 验证已完成，下一步继续进入最小被动衍射处理器对照构建。

## 当前唯一主瓶颈
缺少 ordinary D2NN vs pilot-assisted D2NN 的真实被动衍射处理器对照结果。

## 角色任务

### 统筹者
- 当前任务：把已验证的 wave-optics 机制推进到被动衍射处理器层面的最小阳性对照
- 输入：上传提案、round1/round2 结果、环境状态
- 输出：round3 唯一目标、完成标准、风险边界
- 完成标准：后续所有任务只围绕最小 ordinary vs pilot-assisted 被动衍射处理器对照推进
- 优先级：最高

### 理论人员
- 当前任务：把 round4 tight bound 融入后续正文与补充材料理论主线
- 输入：`round1_theory_note.md`、`round2_theory_note.md`、`round3_information_bound_note.md`、`round4_tight_bound_note.md`
- 输出：从 pilot-channel information 到 task-level loss floor 的理论桥接
- 完成标准：不把 local theorem 误写成全局 blind inverse theorem
- 优先级：高

### 代码与数值计算人员
- 当前任务：实现最小 passive diffractive processor + dynamic aberration + ordinary / pilot-assisted 对照
- 输入：上传提案中的 Result 1 / Result 2 框架，round1/round2 结果
- 输出：round3 脚本、CSV、summary、图文件、运行日志
- 完成标准：至少得到一轮真实可复核的 ordinary vs pilot-assisted OOD 对照
- 优先级：最高

### 数据分析人员
- 当前任务：把 round4 cross-task 结果整理成可写入主文或补充材料的任务级证据
- 输入：`round4_cross_task_summary.md`
- 输出：哪些指标可作为正向 cross-task 结果，哪些只能作为边界说明
- 完成标准：不把弱信号写成强结论

### ML 基线人员
- 当前任务：把 round3 的最小 FNO-style 负结果记录为真实风险，而不是包装成加分项
- 输入：`round3_fno_style_summary.md`
- 输出：完整深 FNO / 条件神经算子的后续需求说明
- 完成标准：明确当前最小 spectral baseline 不足以支撑 ML 说服力

### 实验负责人
- 当前任务：仅保留实验边界说明，不作为当前主线推进角色
- 输入：`round3_experiment_feasibility_note.md`
- 输出：边界说明与未来可选路径
- 完成标准：不虚构任何实验验证，也不把实验列为当前必须完成项
- 优先级：高

### 画图人员
- 当前任务：维持“所有正式数据图必须来自真实计算”的约束
- 输入：round2 原始输出
- 输出：只生成真实数据图；概念示意图若需要可后续由 GPT-imag-2.0 起草
- 完成标准：不提前制造装饰性定稿图
- 优先级：中

### 论文撰写人员
- 当前任务：推进严格写作流程，先完成四段式引言、正文结构、图文映射和 reference ledger 初稿
- 输入：项目主张、round1-round4 证据边界、目标期刊要求
- 输出：`manuscript-v0-structure.md` 与 `reference-ledger-v1.md`
- 完成标准：写作结构可直接承接后续真实结果；不出现结论强于证据
- 优先级：高

### 监督 / 审稿环节
- 当前任务：每轮检查是否把 surrogate 结果误写成 D2NN 结果
- 输入：代码、summary、状态文件
- 输出：监督意见与接收概率更新
- 完成标准：发现过度陈述立即纠偏
- 优先级：最高
