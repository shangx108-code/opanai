# 角色任务表：self-calibrating-diffractive-ncomms

## 当前阶段
wave-optics 最小阳性对照、round3 理论补强和 round4 cross-task 验证已完成，且已有 round5/round5b 第一轮最小被动衍射处理器原型；下一步转入“增强 Figure 5 稳健性”。

## 当前唯一主瓶颈
已有 ordinary D2NN vs pilot-assisted D2NN 的真实最小原型对照，但优势太弱，且 calibration readout 没有形成一致正向结果。

## 角色任务

### 统筹者
- 当前任务：把已存在的 round5/round5b 弱原型推进到更稳健的 Figure 5 结果
- 输入：round1-round5b 结果、环境状态
- 输出：Figure 5 增强路线、完成标准、风险边界
- 完成标准：后续所有任务只围绕 processor-level 优势增强展开
- 优先级：最高

### 理论人员
- 当前任务：把 round4 tight bound 融入后续正文与补充材料理论主线
- 输入：`round1_theory_note.md`、`round2_theory_note.md`、`round3_information_bound_note.md`、`round4_tight_bound_note.md`
- 输出：从 pilot-channel information 到 task-level loss floor 的理论桥接
- 完成标准：不把 local theorem 误写成全局 blind inverse theorem
- 优先级：高

### 代码与数值计算人员
- 当前任务：增强 round5b self-calibrating D2NN，使 common-path 相比 ordinary / non-common-path / wrong-reference 的优势更清晰
- 输入：`round5_minimal_d2nn_comparison.py`、`round5b_selfcalibrating_d2nn.py`
- 输出：稳健性扫描脚本、更新后的 Figure 5 指标表与图文件
- 完成标准：processor-level gain 不再只是弱单点信号
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
- 当前任务：把 round5b 面板当作 Figure 5 原型，而不是终稿
- 输入：round5 / round5b 原始输出
- 输出：真实数据图更新版；若后续增强成功再升级图面布局
- 完成标准：Figure 5 每个条件都必须有论证职责
- 优先级：中

### 论文撰写人员
- 当前任务：把 Figure 5 从“缺失”改写为“弱原型证据”
- 输入：项目主张、round1-round5b 证据边界、目标期刊要求
- 输出：更新后的 `manuscript-v0-structure.md`
- 完成标准：Figure 5 在正文中被明确引用，但不越过证据强度
- 优先级：高

### 监督 / 审稿环节
- 当前任务：每轮检查是否把 surrogate 结果误写成 D2NN 结果
- 输入：代码、summary、状态文件
- 输出：监督意见与接收概率更新
- 完成标准：发现过度陈述立即纠偏
- 优先级：最高
