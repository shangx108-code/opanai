# 监督日志：计算成像1

## 监督轮次 0
- 日期：2026-04-25
- 节点性质：项目初始化监督

## 当前版本总体评价
项目构想强，论文定位有潜力，但当前仍是高质量 proposal，不是可投稿研究成果。

## 与 Nature Communications 标准的差距
1. 缺少真实运行结果，尚无证据证明现象、指标和结论成立。
2. 缺少闭合理论推导，当前主要是框架性表述。
3. 缺少正式图表，图 1-6 仅为规划。
4. 参考文献远未补足，相关工作链条不完整。
5. 尚无正文和补充材料草稿可供严格审稿。

## 已达标部分
- 研究问题具有明确性和潜在普适性。
- 期刊定位基本合理。
- 主线从“更强网络”转向“可信性边界与校准理论”，方向判断较好。

## 未达标部分
- 理论严谨性
- 代码与数值结果
- 数据完整性
- 图表成熟度
- 写作完成度
- 审稿准备度

## 核心质量风险
最大风险是项目长期停留在“概念很强、证据很弱”的状态，导致后续任何写作都变成包装，而不是研究推进。

## 证据链缺口
- 幻觉定义缺乏严格可计算判据
- 双任务最小 benchmark 未跑通
- 尚未证明 DSI / PDR / HCI 优于普通 uncertainty variance
- 尚未建立 OOD、model mismatch、calibration 的真实分析结果

## 必须纠正项
1. 立即停止把路线图当成果表述。
2. 先做最小基准，不同时铺开四个任务。
3. 在出现第一批真实结果前，不进入正式写作和正式审稿循环。
4. 将参考文献扩充到 30 篇以上，并完成主题分类。

## 优先级调整建议
保持“先双任务最小证据链，后扩展应用任务”的路线，不提前展开显微、散射、封面图或大规模写作。

## 是否允许进入下一阶段
暂不允许进入“结果生成完成”或“成稿”阶段。

允许进入的下一步仅为：
- 基础平台搭建
- 第一批真实结果生成
- 理论推导细化

## 下一轮监督重点
1. 学习型 prior 是否已接入线性任务
2. 第 1 轮 toy prior 现象是否能被更真实的 prior 复现
3. DSI / PDR / HCI 是否开始从口号变为可计算对象
4. 文献扩充是否开始有系统推进

## 监督轮次 1
- 日期：2026-04-25
- 节点性质：第 1 轮最小真实结果监督

## 当前版本总体评价
项目已经脱离纯 proposal 状态，开始有可核查的真实结果，但这些结果仍然只是最小证据链，不应被包装成论文主结果。

## 本轮已真实完成
- 已运行最小双任务脚本。
- 线性任务中，prior library selection 选中了 `connected_vertical_bar`，在仅观测上下两段亮块的条件下，引入了未被测量支持的连接结构。
- 相位恢复任务中，prior library selection 选中了 `reversed_ambiguity_mode`，其相对 reversed mode 的误差为 0，且 measurement identity error 为 `4.20e-26` 量级，证明该歧义是测量层面的真实等价。

## 本轮未达标部分
- 没有真实深度先验或 Bayesian baseline。
- 没有 formal DSI / PDR / HCI 推导。
- 图还只是内部说明图。
- 还没有正文 / 补充材料组织方式。

## 新增进展备注
- 线性任务已增加训练型低秩 PCA prior，说明 unsupported-region error 升高并不只来自手工候选库；该现象已经开始从 hand-crafted prior 过渡到 learned prior。

## 核心质量风险
如果接下来不尽快把 toy prior 升级为真实学习型 prior，项目会卡在“概念演示”层，无法提升到目标期刊标准。

## 必须纠正项
1. 下一轮必须把至少一个任务切换到真实学习型 prior。
2. 不得把当前候选库选择结果写成“深度先验已经验证”。
3. 必须把 observed 与 unsupported 区域的差异做成更标准的量化表。

## 是否允许进入下一阶段
允许从“启动前”进入“最小结果生成”阶段，但不允许进入“成稿”阶段。

## 监督轮次 2
- 日期：2026-04-25
- 节点性质：线性非线性学习型 prior 初测监督

## 当前版本总体评价
项目已不再只有 hand-crafted prior 与低秩 prior，线性任务中已经出现一轮真实非线性学习型 prior 结果。这是有效进展，但仍然只是“学习型补全器会在未观测区补结构”的初证据，不足以替代真正的 inverse-solver 级深度先验验证。

## 本轮已真实完成
- 已在当前工作区新建并运行 `round3_linear_autoencoder_prior.py`。
- 已用 256 个 connected-bar 训练样本训练小型非线性 autoencoder prior。
- 已在 6 个断裂目标上输出 `round3_case_metrics.csv` 与 `round3_summary.json`。
- 已得到聚合结果：autoencoder prior 的观测区 MAE 为 `0.0000`，未观测区 MAE 为 `0.2356`，bridge mean intensity 为 `0.3417`。
- 已得到对照结果：PCA prior 的 bridge mean intensity 为 `0.5276`，zero-fill 为 `0.0000`。

## 本轮未达标部分
- 当前 autoencoder prior 仍是前馈式补全，不是 measurement-consistent inverse solver。
- 相位恢复仍无 iterative / posterior learned-prior baseline。
- DSI / PDR / HCI 仍无详细推导。
- 图表仍属于内部实验图，不是正文和补充材料定稿图。

## 新增风险提醒
- 当前工作区未见历史 round1 / round2 实体脚本与结果文件，本轮不能把这些旧路径视为已现场复核归档完成。
- 如果下一轮不把 learned prior 推到优化式逆问题求解层，项目仍会卡在“toy learned completion”层。

## 必须纠正项
1. 下一轮必须把线性 learned prior 改为 measurement-consistent 求解，而不是继续堆更多前馈变体。
2. 不得把本轮 autoencoder 结果写成“深度先验 / diffusion / Bayesian 已验证”。
3. 必须把 unsupported region 与 bridge intensity 转成统一指标定义，避免只看图说话。

## 是否允许进入下一阶段
允许继续停留在“理论强化与最小结果生成阶段”，但仍不允许进入“图表完善完成”或“成稿”阶段。

## 监督轮次 3
- 日期：2026-04-25
- 节点性质：measurement-consistent learned prior 基线监督

## 当前版本总体评价
项目在线性 benchmark 上终于补上了一类真正按测量约束做求解的 learned prior 逆问题基线。这是有效补强，但目前提升的是“现象可靠性”，还不是“理论闭环完成”。

## 本轮已真实完成
- 已在当前工作区新建并运行 `round4_linear_measurement_consistent_prior.py`。
- 已在 6 个断裂目标上统一对照 zero-fill、PCA prior、autoencoder projection 与 measurement-consistent latent inverse。
- 已生成 `round4_summary.json`、`round4_case_metrics.csv`、`round4_linear_measurement_consistent_panel.png` 与 `round4_linear_measurement_mask.png`。
- latent inverse 的聚合结果为：观测区 MAE `0.0000`，未观测区 MAE `0.4891`，bridge mean intensity `0.4964`。

## 本轮未达标部分
- unsupported region / bridge intensity 仍只是经验性指标，没有正式定义。
- latent inverse 仍只在线性 benchmark 上成立，未扩展到相位恢复 learned prior / posterior baseline。
- DSI / PDR / HCI 仍无详细推导。
- 正文与补充材料图仍未成体系。

## 新增风险提醒
- 当前 zero-fill 的未观测区 MAE 为 `0.0000`，因为 benchmark 的 ground truth 本身就是断裂目标；这意味着后续写作必须明确区分“重建误差最小”和“unsupported bridge hallucination 最强”不是同一个命题。
- 如果下一轮不把区域定义与指标公式化，round4 结果仍只能作为现象图，不能进入理论主张。

## 必须纠正项
1. 下一轮必须把 observed / unsupported / bridge 三类区域的定义固定下来。
2. 不得把 round4 结果直接写成“measurement-consistent 深度先验已经证明理论成立”。
3. 必须在结果叙述中明确 benchmark 的 ground truth 是断裂目标，因此 bridge intensity 才是当前 hallucination 现象的关键量之一。

## 是否允许进入下一阶段
允许继续停留在“理论强化与最小结果生成阶段”，仍不允许进入“图表完善完成”或“成稿”阶段。
