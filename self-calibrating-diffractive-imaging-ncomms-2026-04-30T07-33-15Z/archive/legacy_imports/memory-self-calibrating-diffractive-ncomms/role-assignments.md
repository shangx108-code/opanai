# 角色任务表：self-calibrating-diffractive-ncomms

## 当前阶段
最小 runnable chain 稳定后的 Figure 5 局部增强阶段。

## 当前唯一主瓶颈
Figure 5 仍缺少相对 ordinary D2NN 的稳健 common-path 优势。

## 角色任务

### 统筹者
- 当前任务：保持最小可复跑链稳定，并把推进重心压到 common-path vs ordinary 的局部增强
- 输入：round1-round5b 已记录结果、环境状态、活动工作区可见文件
- 输出：环境就绪结论、Figure 5 增强路线、风险边界
- 完成标准：后续任务都围绕“窄窗补数据 + processor-level 优势增强”展开
- 优先级：最高

### 理论人员
- 当前任务：继续维护 round4 tight bound 到正文与补充材料的理论桥接
- 输入：`round1_theory_note.md`、`round2_theory_note.md`、`round3_information_bound_note.md`、`round4_tight_bound_note.md`
- 输出：从 pilot-channel information 到 task-level loss floor 的理论桥接
- 完成标准：不把 local theorem 误写成全局 blind inverse theorem
- 优先级：高

### 代码与数值计算人员
- 当前任务：沿当前 `numpy + Pillow` 管线继续做低 pilot 幅度、少量层数的 matched 局部扫描
- 输入：round5 / round5b 已记录指标、最小协议说明、当前工作区环境
- 输出：可复跑脚本、CSV、summary、图文件、运行日志
- 完成标准：最小链保持稳定，且 common-path 相对 ordinary 的增益不再只是近似持平或弱单点信号
- 优先级：最高

### 数据分析人员
- 当前任务：把已有 round4 与 round5 / round5b 结果分成“正向主证据”“弱信号”“边界证据”
- 输入：`round4_cross_task_summary.md` 及 round5 / round5b 已记录指标
- 输出：主文可用指标表与边界说明
- 完成标准：不把弱信号写成强结论

### ML 基线人员
- 当前任务：继续把 round3 FNO-style 负结果记录为真实风险
- 输入：`round3_fno_style_summary.md`
- 输出：后续更强数字基线需求说明
- 完成标准：明确当前最小 spectral baseline 不足以支撑 ML 说服力

### 实验负责人
- 当前任务：仅保留实验边界说明，不作为当前主线推进角色
- 输入：`round3_experiment_feasibility_note.md`
- 输出：边界说明与未来可选路径
- 完成标准：不虚构任何实验验证
- 优先级：高

### 画图人员
- 当前任务：把 round6 NumPy 面板当作最新 Figure 5 基线，并明确标注其局部窗口与证据边界
- 输入：round5 / round5b 已记录输出与后续新数据
- 输出：真实数据图更新版
- 完成标准：Figure 5 每个条件都必须有论证职责
- 优先级：中

### 论文撰写人员
- 当前任务：维护 `manuscript-v1-strict.md` 的证据边界，把 Figure 5 更新为“可复跑基线 + 局部窗口”而不是“稳健优势”
- 输入：项目主张、round1-round5b 证据边界、目标期刊要求
- 输出：更新后的主文结构或正文
- 完成标准：Figure 5 被明确引用，但不越过证据强度
- 优先级：高

### 监督 / 审稿环节
- 当前任务：每轮检查是否把 surrogate 结果误写成 D2NN 结果，并同时检查底层文件是否在活动工作区可访问、该轮是否留下独立日志
- 输入：代码、summary、状态文件、活动工作区文件
- 输出：监督意见与接收概率更新
- 完成标准：发现过度陈述立即纠偏；无日志则该轮不算有效推进
- 优先级：最高
