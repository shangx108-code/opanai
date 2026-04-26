# 监督日志：计算成像1

## 监督轮次 10
- 日期：2026-04-26
- 节点性质：round10 rebuilt de-biased exact-pair 检验监督

## 当前版本总体评价
这一轮真正把“对称先验下 residual bias 会不会自动消失”从猜测变成了可复核结果。当前工作区已经有一套新的 rebuilt de-biased exact-pair 工件，并且继续把 `x_hat` 限制在 exact ambiguity pair 上，因此 `recovered_measurement_error` 仍在机器精度量级。结果说明：随机 `0.5` 取向训练并不会自动把 residual bias 压到近零，但显式 mirror-averaged posterior 可以。这是有效新进展，但仍不是机制闭环，因为这一步还停留在 rebuilt branch scorer，而不是低误差 learned solver。

## 本轮已真实完成
- 已在当前工作区新建并运行 `/workspace/computational-imaging-1-ncomms/round10_phase_debiased_exact_pair.py`。
- 已生成 `/workspace/computational-imaging-1-ncomms/round10_phase_debiased_exact_pair_outputs/round10_phase_summary.json`。
- 已生成 `/workspace/computational-imaging-1-ncomms/round10_phase_debiased_exact_pair_outputs/round10_phase_case_metrics.csv` 与 `round10_phase_seed_metrics.csv`。
- 已生成 `/workspace/computational-imaging-1-ncomms/round10_phase_debiased_exact_pair_outputs/round10_phase_panel.png` 与 `round10_phase_notes.md`。
- `balanced_density_prior` 共完成 `1024` 次 exact-pair evaluation，平均 exact ambiguity quantity `1.04e-16`，平均 `recovered_measurement_error = 4.79e-17`，平均 `branch_bias = 0.0962`，平均 normalized branch bias `0.0820`，`choose_true_ratio = 0.541`，二项检验 `p = 0.00946`。
- `mirror_averaged_posterior` 共完成 `1024` 次 control evaluation，平均 exact ambiguity quantity `1.04e-16`，平均 `recovered_measurement_error = 5.13e-17`，平均 `branch_bias = 0.0041`，平均 normalized branch bias `0.0039`，`choose_true_ratio = 0.502`，二项检验 `p = 0.925`。

## 本轮未达标部分
- 当前 round10 是 rebuilt exact-pair branch scorer，不是 solver 级 learned prior / posterior / diffusion baseline。
- 当前只能说明显式 symmetry-enforced averaging 在这个 controlled benchmark 中有效，不能直接外推到一般 phase retrieval。
- DSI / PDR / HCI 仍未完成论文级推导。
- 图表、正文、补充材料与五审稿人循环仍未启动。

## 新增风险提醒
- 如果下一轮不把 symmetry-enforced 机制接入真实低误差 solver，项目会停留在“评分器层面的机制演示”，还不足以支撑方法学主张。
- 当前 `balanced_density_prior` 的 residual bias 虽小于强偏置条件，但统计上仍不应包装成“自动无偏”。
- `mirror_averaged_posterior` 的近零 residual bias 目前是受控 benchmark 结论，不等于真实应用任务中 branch bias 已被完全解决。

## 必须纠正项
1. 下一轮必须优先把 symmetry-enforced averaging 或 mirror-consistency 约束接入低 measurement-error solver。
2. 不得把 round10 写成“对称训练已经证明无偏”；当前更准确的结论是“显式 symmetry enforcement 有效，而 balanced sampling 仍可能留下 residual bias”。
3. 在 solver 级对照完成前，不得把当前 phase 结论外推成 Nature Communications 级方法学闭环。

## 是否允许进入下一阶段
允许继续停留在“理论强化与最小结果生成阶段”，但仍不允许进入“图表完善完成”或“成稿”阶段。

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
- 已增加第一版理论笔记和 42 条工作文献表，项目不再停留在“只有实验碎片”的状态。

## 新的监督判断
- 文献数量门槛已跨过，但仍未形成最终引用体系。
- 理论链已从口号进入可检查状态，但距离正文 / Methods 可直接使用还差一步。
- 下一轮最应该继续推进的是：把真实 deep prior / diffusion / Bayesian baseline 接进现有双任务框架。

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

## 监督轮次 9
- 日期：2026-04-26
- 节点性质：round9 orientation-ratio 连续扫参监督

## 当前版本总体评价
这一轮真正把“prior family 会不会翻转 branch sign”进一步压缩成了一个更干净的机制问题。当前工作区已经有一套可现场复核的 round9 连续扫参工件，而且本轮把 `x_hat` 直接限制在 exact ambiguity pair 上，使 `recovered_measurement_error` 下降到机器精度量级。结果说明：branch sign 的变化不只是三档 family 的离散现象，而是会随 training orientation ratio 连续跨零移动。这是有效新进展，但仍不是机制闭环，因为对称先验下 residual bias 是否消失还没有被真实检验。

## 本轮已真实完成
- 已在当前工作区新建并运行 `/workspace/computational-imaging-1-ncomms/round9_phase_orientation_ratio_scan.py`。
- 已生成 `/workspace/computational-imaging-1-ncomms/round9_phase_orientation_ratio_outputs/round9_phase_summary.json`。
- 已生成 `/workspace/computational-imaging-1-ncomms/round9_phase_orientation_ratio_outputs/round9_phase_case_metrics.csv`。
- 已生成 `/workspace/computational-imaging-1-ncomms/round9_phase_orientation_ratio_outputs/round9_phase_panel.png` 与 `round9_phase_notes.md`。
- 本轮共完成 `1056` 次 exact-ambiguity branch evaluation，平均 exact ambiguity quantity 为 `1.39e-16`，平均 `recovered_measurement_error = 7.11e-17`。
- 平均 `branch_bias` 随 training true-orientation ratio 从 `0.0` 的 `-0.6078` 连续移动到 `1.0` 的 `0.4125`，并在 `0.5`–`0.6` 附近跨零；对应正偏向比例从 `0.188` 升到 `0.729`。

## 本轮未达标部分
- 当前 round9 仍是 controlled exact-ambiguity benchmark，不是 posterior / diffusion / Bayesian baseline。
- 当前只证明了 orientation bias 足以驱动 branch sign 连续变化，还没有证明对称先验下 residual bias 会自动消失。
- DSI / PDR / HCI 仍未完成论文级推导。
- 图表、正文、补充材料与五审稿人循环仍未启动。

## 新增风险提醒
- 如果下一轮不直接做去偏置 baseline，项目会继续停留在“偏置足以解释一部分现象”而不是“机制来源已分离清楚”。
- 当前 `ratio = 0.5` 条件下平均 `branch_bias = -0.0894`、正偏向比例 `0.479`，已经接近对称，但还不能据此声称 residual bias 为零。
- round9 的 `recovered_measurement_error` 接近零，说明这一步更适合写成“solver failure 已基本剥离”，但不能反过来包装成“一般 phase retrieval 已解决”。

## 必须纠正项
1. 下一轮必须优先补去偏置或后验平均型 baseline，直接检查 residual branch bias 是否收敛到接近零。
2. 不得把 round9 的连续 crossing 写成“branch selection 的统一规律已经确立”；当前它只说明 orientation bias 是充分驱动因素。
3. 在去偏置检验完成前，不得把当前 phase 结论外推成 Nature Communications 级方法学主张。

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

## 监督轮次 4
- 日期：2026-04-26
- 节点性质：运行规则收紧与迭代节奏调整

## 当前版本总体评价
项目推进规则已经从“尽快推进”收紧为“证据闭环优先”。这是必要调整，因为目标不只是把接收概率抬高，还要真正补全 evidence、数据、图和推导。

## 本轮已真实完成
- 已把项目自动推进节奏更新为每 2 小时 1 轮。
- 已把停止标准明确收紧为“接收概率门槛”和“证据链门槛”同时成立。
- 已把画图规则明确拆分为：
  - 示意图可用 GPT-imag-2.0 起稿；
  - 除示意图外，其余图必须全部来自真实数据。
- 已把理论标准明确收紧为“详实、可靠、可检查”。

## 当前监督判断
- 这次调整提高了项目的真实性门槛，能减少后续把不完整内容包装成“可投稿”的风险。
- 但规则收紧不会自动带来结果，真正的瓶颈仍然是：理论判据闭环和跨任务真实结果矩阵。

## 必须继续坚持的事项
1. 不得因为示意图可用 GPT-imag-2.0 起稿，就放松真实数据图标准。
2. 不得因为参考文献数量已过 30，就忽略正文嵌入、引用角色和补充材料衔接。
3. 不得把未完成详细推导的量写成论文主结论。

## 监督轮次 5
- 日期：2026-04-26
- 节点性质：线性 benchmark 区域定义与指标正式化监督

## 当前版本总体评价
本轮终于把“unsupported region / bridge intensity 只是经验说法”的问题往前推进了一步。当前工作区已经有了真实运行的重现实验脚本、可复核输出和正式定义文档，因此线性 benchmark 不再只是现象图，而是具备了第一版 Methods/Results 可写入口径。

## 本轮已真实完成
- 已在当前工作区新建并运行 `/workspace/computational-imaging-1-ncomms/round4_region_formalization_repro.py`。
- 已生成 `/workspace/computational-imaging-1-ncomms/round4_region_formalization_outputs/round4_reproduced_summary.json`。
- 已生成 `/workspace/computational-imaging-1-ncomms/round4_region_formalization_outputs/round4_reproduced_case_metrics.csv`。
- 已生成 `/workspace/computational-imaging-1-ncomms/round4_region_formalization_outputs/round4_reproduced_panel.png` 与 `round4_reproduced_mask.png`。
- 已新增 `/workspace/computational-imaging-1-ncomms/theory_round3_region_formalization.md`，把 observed region、unsupported region、bridge region 以及四个指标的口径固定下来。
- 重现实验聚合结果显示：zero-fill 的 bridge mean intensity 为 `0.0000`，PCA prior 为 `0.5756`，autoencoder projection 为 `0.9077`，latent inverse 为 `0.9959`；同时四个方法的 observed-region MAE 都为 `0.0000`。

## 本轮未达标部分
- 当前正式化只覆盖 linear masked-identity benchmark，不等于一般 hallucination 理论已经完成。
- 相位恢复仍缺 learned prior / posterior baseline。
- DSI / PDR / HCI 仍缺完整论文级推导。
- 图表仍属于内部研究图，不是正文和补充材料定稿图。

## 新增风险提醒
- 当前工作区未找到记忆中登记的旧 round4 实体路径，因此不能把旧 round4 文件包装成“已现场复核”；本轮真正新增的是一套新的可复核重现实验工件。
- 当前断裂 bar benchmark 的 ground truth 在未观测 bridge 区域为零，因此 bridge intensity 与 bridge L1 error 在当前脚本中数值重合；后续写作不能把这种重合误写成一般结论。

## 必须纠正项
1. 下一轮必须把相位恢复任务补到 learned prior / ambiguity selection 级真实结果。
2. 不得把当前线性 benchmark 的区域定义直接外推成所有 forward model 的普适定理。
3. 不得把内部研究图直接当作 Figure 2 / Figure 3 定稿图。

## 是否允许进入下一阶段
允许继续停留在“理论强化与最小结果生成阶段”，但仍不允许进入“图表完善完成”或“成稿”阶段。

## 监督轮次 6
- 日期：2026-04-26
- 节点性质：相位恢复 learned-prior / ambiguity selection 初证据监督

## 当前版本总体评价
这一轮确实补上了之前最缺的一块：相位恢复不再只有 true / reversed 的等测量存在性，而是已经出现一版真实运行的 learned-prior branch-selection 结果。项目因此第一次具备了“线性任务有 learned prior unsupported structure，非线性任务也有 learned prior branch bias”的跨 forward model 初证据。但这仍然只是第一版经验结果，还不是强 solver 结果，更不是统一理论闭环。

## 本轮已真实完成
- 已在当前工作区新建并运行 `/workspace/computational-imaging-1-ncomms/round5_phase_retrieval_learned_prior.py`。
- 已训练一版长度为 64 的非线性 autoencoder decoder prior，并在 4 个 held-out 相位恢复样例上仅通过 Fourier magnitude 测量做 latent 优化。
- 已生成 `/workspace/computational-imaging-1-ncomms/round5_phase_retrieval_outputs/round5_phase_summary.json`。
- 已生成 `/workspace/computational-imaging-1-ncomms/round5_phase_retrieval_outputs/round5_phase_case_metrics.csv`。
- 已生成 `/workspace/computational-imaging-1-ncomms/round5_phase_retrieval_outputs/round5_phase_panel.png` 与 `round5_phase_ambiguity_notes.md`。
- 聚合结果显示：true / reversed 分支的 measurement error 为 `1.26e-16` 量级；learned prior 输出到 true branch 的平均距离为 `0.4380`，到 reversed branch 的平均距离为 `1.2072`，mean branch bias 为 `0.7692`，且 4 / 4 个样例均为正偏向。

## 本轮未达标部分
- 当前 learned prior 仍是 orientation-biased decoder prior，不是 posterior / diffusion / Bayesian baseline。
- 当前平均 recovered measurement error 仍为 `2.52e-01`，说明它还不是低误差强求解器。
- 当前相位恢复指标说明仍未正式接入 DSI / PDR / HCI 推导链。
- 图表、正文、补充材料与五审稿人循环仍未启动。

## 监督轮次 7
- 日期：2026-04-26
- 节点性质：phase ambiguity 指标边界 formalization 监督

## 当前版本总体评价
本轮没有新增真实数值实验，但完成了一项必要的理论与口径清障：把 round5 相位恢复中的 exact ambiguity、empirical measurement consistency 和 empirical branch selection 明确拆开。这一步是有效推进，因为它直接降低了把经验偏向误写成理论结论的风险。

## 本轮已真实完成
- 已新增 `/workspace/memory/computational-imaging-1-ncomms/phase-ambiguity-metrics-round6.md`。
- 已把 round5 已登记字段 `true_reversed_measurement_error`、`recovered_measurement_error`、`distance_to_true`、`distance_to_reversed`、`branch_bias` 固定为三层量。
- 已明确 `branch_bias = distance_to_reversed - distance_to_true`，并根据已登记聚合值验证出 `1.2072 - 0.4380 = 0.7692`。
- 已完成下一轮优先级判定：先补强 phase solver 的 measurement consistency，再讨论统一理论接口。

## 本轮未达标部分
- 当前工作区仍未找到 round5 原始脚本和原始输出文件，因此本轮不构成对 round5 工件的二次现场复核。
- 当前仍没有新的低 measurement-error phase baseline。
- DSI / PDR / HCI 仍未完成论文级推导。
- 正文、补充材料和投稿级图表仍未形成。

## 新增风险提醒

## 监督轮次 8
- 日期：2026-04-26
- 节点性质：低误差 phase branch-bias 稳健性扫描监督

## 当前版本总体评价
这一轮不是停留在“猜测 branch bias 不稳”，而是把它真实跑成了一个受控稳健性扫描。当前环境中已经有一套新的可复核脚本和 `144` 次 phase solve 输出，因此项目对 phase 分支问题的认识明显更扎实了。但结果同样更严格地削弱了旧的强主张空间：branch selection 在低误差条件下会随 prior orientation bias 系统性翻转，当前不能再把它写成稳定、统一的 prior-induced branch preference。

## 本轮已真实完成
- 已在当前环境中新建并运行 `/workspace/computational-imaging-1-ncomms/round8_phase_branch_robustness_scan.py`。
- 已生成 `/workspace/computational-imaging-1-ncomms/round8_phase_branch_robustness_outputs/round8_phase_summary.json`。
- 已生成 `/workspace/computational-imaging-1-ncomms/round8_phase_branch_robustness_outputs/round8_phase_case_metrics.csv`。
- 已生成 `/workspace/computational-imaging-1-ncomms/round8_phase_branch_robustness_outputs/round8_phase_panel.png` 与 `round8_phase_notes.md`。
- 已在 `3` 个 prior family、`3` 个训练随机种子、`4` 个初始化种子和 `4` 个 held-out 样例上完成 `144` 次真实 solve。
- 聚合结果显示：mean exact ambiguity quantity `1.08e-16`，mean recovered measurement error `1.20e-02`，median recovered measurement error `6.79e-03`，mean branch bias `0.0105`。
- 分组结果显示：
  - `true_biased` 下平均 `branch_bias = 0.6893`，正偏向比例 `1.000`
  - `balanced` 下平均 `branch_bias = 0.0752`，正偏向比例 `0.604`
  - `reversed_biased` 下平均 `branch_bias = -0.7330`，正偏向比例 `0.000`

## 本轮未达标部分
- 当前 phase baseline 仍是 synthetic PCA prior，不是 posterior / diffusion / Bayesian baseline。
- 当前稳健性扫描已证明“branch bias 不稳定”，但还没有给出 orientation bias 的连续响应曲线。
- DSI / PDR / HCI 仍未完成论文级详细推导。
- 正文、补充材料与投稿级图表仍未形成。

## 新增风险提醒
- 现在最大的写作风险已经从“把高 solver-error 现象误写成 branch selection”变成“把 orientation-biased prior 的翻转现象误写成普适 prior effect”。
- 当前 round8 是 synthetic controlled benchmark，不等于真实高应用价值任务已经补齐。
- 即使 mean recovered measurement error 已在 `1e-2` 量级，也不能直接宣称 phase 机制闭环成立，因为 branch sign 仍受 prior family 强烈控制。

## 必须纠正项
1. 下一轮必须优先补 training orientation 比例连续扫参，量化 branch bias 对先验偏置的响应曲线。
2. 不得把 `true_biased` 条件下的全正偏向写成“相位恢复普遍偏向 true branch”；它只对当前有偏训练分布成立。
3. 不得把当前稳健性扫描当作 phase 任务已经完成；它只是把主瓶颈从“是否稳定”进一步缩到“为何翻转”。

## 是否允许进入下一阶段
允许继续停留在“理论强化与最小结果生成阶段”，但仍不允许进入“图表完善完成”或“成稿”阶段。
- 如果下一轮直接把当前 round5 结果接成统一理论接口，会把 solver failure 与 prior-induced branch preference 混写。
- 如果后续恢复 round5 原始工件，仍需再做一次现场核验，不能用本轮口径说明替代原始归档。

## 必须纠正项
1. 下一轮必须优先降低 phase baseline 的 `recovered_measurement_error`。
2. 不得把 `branch_bias > 0` 写成 phase retrieval 中的一般理论定理。
3. 在原始 round5 工件补回前，不得声称本轮完成了对该脚本实现细节的重新核验。

## 是否允许进入下一阶段
允许继续停留在“理论强化与最小结果生成阶段”，但不允许进入“图表完善完成”或“成稿”阶段。

## 监督轮次 8
- 日期：2026-04-26
- 节点性质：round7 rebuilt low-error phase solver 监督

## 当前版本总体评价
这一轮真正推进了上一轮的首要瓶颈：当前工作区已经有一套可现场复核的 rebuilt phase baseline，并把平均 `recovered_measurement_error` 压到 `9.54e-03`。这说明“先把 solver 跑强一点”不是空话，现场已经做成了。但结果也更严格地暴露出新的主问题：当 solver error 不再高企时，branch bias 并没有稳定保留，当前 phase 证据仍不足以支撑论文级机制主张。

## 本轮已真实完成
- 已在当前工作区新建并运行 `/workspace/computational-imaging-1-ncomms/round7_phase_pca_solver_rebuild.py`。
- 已生成 `/workspace/computational-imaging-1-ncomms/round7_phase_pca_solver_outputs/round7_phase_summary.json`。
- 已生成 `/workspace/computational-imaging-1-ncomms/round7_phase_pca_solver_outputs/round7_phase_case_metrics.csv`。
- 已生成 `/workspace/computational-imaging-1-ncomms/round7_phase_pca_solver_outputs/round7_phase_panel.png` 与 `round7_phase_notes.md`。
- rebuilt PCA prior baseline 在 4 个 held-out 样例上的聚合结果为：true / reversed 精确 branch 的 measurement error `1.39e-16`，平均 recovered measurement error `9.54e-03`，平均 distance to true `0.9250`，平均 distance to reversed `0.7775`，mean branch bias `-0.1475`，仅 `1 / 4` 个样例为正 branch bias。

## 本轮未达标部分
- 当前 rebuilt phase baseline 仍只是一类 PCA decoder prior，不是 posterior / diffusion / Bayesian baseline。
- 当前 branch bias 在低 measurement-error 条件下并不稳定，因此 phase 结果还不能接成“稳定 prior-induced selection”主结论。
- DSI / PDR / HCI 仍未完成论文级推导。
- 图表、正文、补充材料与五审稿人循环仍未启动。

## 新增风险提醒
- 若继续只引用已登记 round5 的正 branch bias，而忽略 round7 的 sign flip 与波动，就会把不稳健结果包装成机制结论。
- 当前 round7 是 rebuilt on-site benchmark，不是对缺失的 round5 原始工件做逐项复核；两者不能混写成同一实验轮次。
- 如果后续不做 prior family / seed / initialization 的受控扫描，phase 结果仍可能停留在“单次实验偶然性”层面。

## 必须纠正项
1. 下一轮必须优先做 round7 低误差 phase baseline 的稳健性统计，而不是立刻扩写理论主结论。
2. 不得把本轮 `mean branch_bias = -0.1475` 解读成“reversed branch 一般更优”；当前它只说明 branch selection 还不稳定。
3. 在稳健性扫描完成前，不得把 round5 或 round7 任一单轮 branch preference 写成统一规律。

## 是否允许进入下一阶段
允许继续停留在“理论强化与最小结果生成阶段”，但仍不允许进入“图表完善完成”或“成稿”阶段。

## 新增风险提醒
- 不能把 `x_true` 与 `x_rev` 的精确测量等价，与 `x_hat` 对 true branch 的经验偏向混写成同一种“已证明结论”。
- 当前 round5 的 branch bias 强，但 measurement error 仍不低；如果写作时忽略这一点，会把“branch preference”误包装成“高质量 reconstruction”。
- 当前 phase 结果只覆盖一类 orientation-biased toy family，不能直接外推为一般 phase retrieval learned prior 定理。

## 必须纠正项
1. 下一轮必须把 phase ambiguity 的 exact quantity 与 empirical quantity 写成统一、可检查的说明。
2. 不得把 round5 结果写成“phase retrieval 深度先验已经证明理论成立”。
3. 在 measurement error 口径与适用边界未写清前，不得把当前 panel 直接升级成正文定稿图。

## 是否允许进入下一阶段
允许继续停留在“理论强化与最小结果生成阶段”，但仍不允许进入“图表完善完成”或“成稿”阶段。
