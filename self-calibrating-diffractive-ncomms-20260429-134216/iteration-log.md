# 研究迭代日志：self-calibrating-diffractive-ncomms

## 2026-04-29 Iteration Resume

- 当前阶段：恢复研究迭代模式
- 当前唯一主瓶颈：缺少 ordinary D2NN vs pilot-assisted D2NN 的真实被动衍射处理器最小阳性对照
- 本轮唯一最高优先级：进入器件级最小对照构建前的强化运行状态，要求后续每轮必须留下可检查日志
- 当前判断：
  - 已有 round1-round4 与 writing-launch 的项目记录
  - 当前没有独立运行日志来证明自动迭代持续执行
  - 因此本轮先补齐“强化运行”的可追踪性，而不是假装自动系统已经稳定闭环
- 本轮交付物：
  - `iteration-log.md`
  - `iteration-round-2026-04-29.md`
  - 更新后的 `project-state.md`
  - 更新后的 `role-assignments.md`
  - 更新后的 `supervision-log.md`
- 下一轮立即动作：
  1. 直接进入 ordinary D2NN vs pilot-assisted D2NN 的最小 NumPy 可运行对照脚本设计
  2. 产出统一协议、控制组、指标与预期落盘文件清单
  3. 每轮结束强制写入本日志，不再允许“只更新状态、不留迭代痕迹”

## 2026-04-29 Environment Bring-up

- 当前阶段：环境配置与数据补全优先
- 当前唯一主瓶颈：Figure 5 相关数据补全缺少稳定可复跑环境与连续证据链
- 本轮唯一最高优先级：打通最小本地运行链，而不是等待网络安装恢复
- 本轮真实结果：
  - 已创建 `/workspace/self-calibrating-diffractive-ncomms/` 工作目录
  - 已确认在线安装 `matplotlib/scipy/torch` 失败，原因为代理受限
  - 已确认当前可用执行链为 `numpy + Pillow`
- 当前可用环境：
  - `numpy 2.3.5`
  - `Pillow 12.2.0`
- 下一轮立即动作：
  1. 以 `numpy + Pillow` 实现或恢复最小 passive D2NN 对照脚本
  2. 优先补真实运行数据，不再等待外部依赖
  3. 按每小时一轮更新本日志

## 2026-04-29 Round 6 NumPy Rebuild

- 当前阶段：最小可复跑数据链恢复
- 当前唯一主瓶颈：器件级 common-path 优势仍未形成稳健正信号
- 本轮唯一最高优先级：在当前 `numpy + Pillow` 环境下恢复最小 ordinary / common-path / non-common-path / wrong-reference 对照
- 本轮真实结果：
  - 已新增 `round6_numpy_passive_d2nn.py`
  - 已真实运行并输出 `metrics.csv`、`summary.md/json`、`panel.png`、`training_history.json`
  - ordinary OOD mean PSNR：`11.884 dB`
  - common-path OOD mean PSNR：`10.754 dB`
  - non-common-path OOD mean PSNR：`10.690 dB`
  - wrong-reference OOD mean PSNR：`10.831 dB`
  - common minus ordinary：`-1.131 dB`
  - common minus non-common-path：`+0.063 dB`
- 当前判断：
  - 最小 NumPy 数据补全链已经恢复成功
  - 但这轮结果不支持把 common-path 写成优于 ordinary 的器件级主证据
- 下一轮立即动作：
  1. 保留本轮脚本与数据链作为可复跑基线
  2. 调整 reference 权重、层数或任务定义，再做小范围稳健性扫描
  3. 继续按每小时一轮记录，不把本轮负结果包装成正向亮点

## 2026-04-29 Drive Archive Sync Prep

- 当前阶段：归档索引补全
- 当前唯一主瓶颈：Drive 侧已有空台账，但当前接口没有可用写入口，导致 round6 / round7 真实资产仍停留在本地
- 本轮唯一最高优先级：把待同步资产收口成标准 manifest，并确认 Drive 侧现成落点
- 本轮真实结果：
  - 已确认 Google Drive 中存在两张空表：
    - `SC-DON NatComm Iteration Ledger`
    - `SC-DON NatComm Iteration Ledger 2026-04-28`
  - 已确认两表位于“我的云端硬盘”根目录，`Sheet1` 当前为空
  - 已生成 `/workspace/output/sc-don-drive-sync-manifest-2026-04-29.csv`
  - 已更新 `drive-index.md`、`archive-checklist.md`、`project-state.md`
- 当前判断：
  - 本地待同步包已经足以进入 Drive 归档
  - 当前阻塞是真实的 Drive 写入入口缺失，不是本地资产缺失
- 下一轮立即动作：
  1. 一旦获得目标文件夹 URL 或可写入口，按 manifest 中 `local-ready` 项逐条写入
  2. 将 `missing-from-active-workspace` 项保留为缺失，不伪装成已归档
  3. 写入完成后再补 Memory 的正式 Drive 路径映射

<!-- auto-drive-sync:start -->
## 自动云端同步监视
- 最近刷新时间（UTC）：`2026-04-29T02-08-24Z`
- 本轮本地待同步资产数：`28`
- 当前仍缺失的历史资产数：`5`
- 最新同步清单：`/workspace/output/sc-don-drive-sync-manifest-latest.csv`
- 默认目标文件夹：`SC-DON-NatComm-data`
- 当前判断：每轮迭代后的长期保存数据已经能自动汇总到统一同步包，但还不能直接写入 Google Drive。
- 仍需恢复的代表性历史文件：
  - `/workspace/self-calibrating-diffractive-ncomms/outputs/round5_minimal_d2nn_metrics.csv`
  - `/workspace/self-calibrating-diffractive-ncomms/outputs/round5b_selfcalibrating_d2nn_metrics.csv`
  - `/workspace/self-calibrating-diffractive-ncomms/outputs/round5b_selfcalibrating_d2nn_panel.png`
<!-- auto-drive-sync:end -->

## 2026-04-29 Round 8 Narrow Processor Scan

- 当前阶段：Figure 5 局部增强扫描
- 当前唯一主瓶颈：common-path 相对 wrong-reference 的分离仍不稳定
- 本轮唯一最高优先级：围绕 round7 最优窗口做更窄、更重视 repeat 稳定性的 processor-level 扫描
- 本轮真实结果：
  - 已新增并运行 `/workspace/self-calibrating-diffractive-ncomms/scripts/round8_narrow_processor_scan.py`
  - 已完成 `60` 组局部配置、每组 `4` 次重复
  - 已生成：
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round8_narrow_scan_repeat_rows.csv`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round8_narrow_scan_detail.csv`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round8_narrow_scan_summary.csv`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round8_narrow_scan_top10.csv`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round8_narrow_scan_summary.json`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round8_narrow_scan_summary.md`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round8_narrow_scan_heatmap.png`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round8_best_local_config_panel.png`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round8_best_local_config_history.json`
- 本轮关键结果：
  - 最优稳健配置为 `num_layers=1, reference_weight=0.16, phase_mix=0.15`
  - 该配置下 `common minus ordinary` 均值为 `+0.438 dB`，最差重复仍为 `+0.390 dB`
  - 但 `common minus wrong-reference` 均值仅 `+0.062 dB`，最差重复为 `-0.307 dB`
  - 仅有 `2/60` 个局部配置同时满足 `common minus ordinary > 0` 与 `common minus wrong-reference > 0`
- 当前判断：
  - 这轮已经把 ordinary 对照上的正向窗口明显拉稳
  - 但 wrong-reference 分离仍然没有稳到足以封闭 Figure 5
- 下一轮立即动作：
  1. 固定 `num_layers=1` 与 `reference_weight=0.16`，只围绕 `phase_mix` 与 wrong-reference 结构做更针对性的局部改写
  2. 优先尝试让 wrong-reference 的参考结构更具破坏性，而不是继续盲目扩宽参数网格
  3. 若下一轮仍无法稳定拉开 wrong-reference，应考虑重写 Figure 5 的主论证目标，避免把“自校准读出”写得强于证据

## 2026-04-29 Round 9 Wrong-reference Targeted Scan

- 当前阶段：Figure 5 wrong-reference 排他性验证
- 当前唯一主瓶颈：需要确认 common-path 的优势不是 reference 形状偏置伪像
- 本轮唯一最高优先级：固定 round8 稳定窗口，只对 wrong-reference 构造做 targeted 扫描
- 本轮真实结果：
  - 已新增并运行 `/workspace/self-calibrating-diffractive-ncomms/scripts/round9_wrong_reference_targeted_scan.py`
  - 已固定 `num_layers=1` 与 `reference_weight=0.16`
  - 已完成 `30` 组 targeted wrong-reference 配置、每组 `4` 次重复
  - 已生成：
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round9_wrongref_target_repeat_rows.csv`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round9_wrongref_target_detail.csv`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round9_wrongref_target_summary.csv`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round9_wrongref_target_top10.csv`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round9_wrongref_target_summary.json`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round9_wrongref_target_summary.md`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round9_wrongref_target_heatmap.png`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round9_wrongref_target_best_panel.png`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round9_wrongref_target_best_history.json`
- 本轮关键结果：
  - 最优 targeted 配置为 `wrongref_mode=anti_phase, phase_mix=0.20`
  - 该配置下 `common minus ordinary` 均值为 `+0.654 dB`，最差重复仍为 `+0.556 dB`
  - 同时 `common minus non-common-path` 均值为 `+0.258 dB`
  - `common minus wrong-reference` 均值为 `+0.141 dB`，最差重复仍为 `+0.027 dB`
  - 本轮出现了 `2` 个严格满足 `common minus ordinary > 0`、`common minus wrong-reference > 0` 且两者最差重复都为正的 targeted 配置
- 当前判断：
  - 这轮首次拿到了对 wrong-reference 也保持全重复正向排他的局部窗口
  - Figure 5 已经不再只是“ordinary 优势较稳”，而是出现了“初步稳定的 wrong-reference 排他性”
  - 但排他性幅度仍偏小，下一轮仍需确认这个窗口是否可进一步放大
- 下一轮立即动作：
  1. 锁定 `wrongref_mode=anti_phase`，只围绕 `phase_mix=0.18-0.22` 做超窄扫描
  2. 增加重复次数，优先验证当前正向排他性窗口是否能跨更多 seed 保持
  3. 若窗口继续成立，则开始把 Figure 5 的主文措辞从“弱原型”升级为“出现初步稳定排他性窗口”

## 2026-04-29 Round 10 Anti-phase Confirmation Scan

- 当前阶段：wrong-reference 窗口高重复确认
- 当前唯一主瓶颈：需要确认 round9 的 anti-phase 排他性窗口是否能跨更多 seed 保持
- 本轮唯一最高优先级：固定 `anti_phase`，提高重复次数，对 `phase_mix=0.18-0.22` 做超窄确认扫描
- 本轮真实结果：
  - 已新增并运行 `/workspace/self-calibrating-diffractive-ncomms/scripts/round10_antiphase_confirmation_scan.py`
  - 已完成 `9` 个 `phase_mix` 点、每点 `10` 次重复
  - 已生成：
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round10_antiphase_repeat_rows.csv`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round10_antiphase_detail.csv`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round10_antiphase_summary.csv`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round10_antiphase_top.csv`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round10_antiphase_summary.json`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round10_antiphase_summary.md`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round10_antiphase_best_panel.png`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round10_antiphase_best_history.json`
- 本轮关键结果：
  - 最佳确认点为 `phase_mix=0.18`
  - 该点下 `common minus ordinary` 均值为 `+0.409 dB`，最差重复仍为 `+0.151 dB`
  - 但 `common minus wrong-reference` 均值仅 `+0.067 dB`，最差重复回落到 `-0.103 dB`
  - 全部 `9` 个确认点中，没有任何一个点满足对 wrong-reference 的最差重复也为正
- 当前判断：
  - round9 出现的 anti-phase 正向排他性窗口未能通过更高重复数确认
  - 当前能诚实保留的最强结论仍是“相对 ordinary 的正向窗口较稳”，而不是“wrong-reference 排他性已稳定成立”
- 下一轮立即动作：
  1. 停止继续在 `anti_phase` 上做同类确认扫描，避免重复消耗
  2. 回到 Figure 5 论证目标重写，把重点从“稳定 wrong-reference 排他性”下调为“ordinary 优势稳健、排他性仍待加强”
  3. 仅在出现新的 wrong-reference 构造思路时再重开这一分支

## 2026-04-29 Supplement And Wrong-reference V2 Sync

- 当前阶段：稿件口径与补充材料同步
- 当前唯一主瓶颈：正文、图注、补充材料与 next-step 设计入口需要保持同一证据边界
- 本轮唯一最高优先级：把 Figure 5 的降级口径、round8-round10 的真实结果，以及新的 wrong-reference v2 设计说明同步到可检查文档
- 本轮真实结果：
  - 已更新 `document-plan.md`
  - 已新增 `/workspace/memory/self-calibrating-diffractive-ncomms/wrong-reference-design-v2.md`
  - 已更新 `/workspace/self-calibrating-diffractive-ncomms/scripts/generate_supplementary_pdf.py`
  - 已重生成 `/workspace/output/self-calibrating-diffractive-ncomms-supplementary.pdf`
- 本轮关键判断：
  - 现在可以把 Supplementary 中 Figure 5 的最强表述稳定在“ordinary baseline advantage repeat-stable”
  - 不能把 wrong-reference 排他性写成已稳定确认
  - wrong-reference v2 家族可作为下一轮 focused scan 的设计输入，但目前仍是未验证对象
- 下一轮立即动作：
  1. 若重开 processor 分支，优先从 `anti_phase_plus_decoy` 和 `task_matched_decoy` 开始
  2. 保持正文、图注、补充材料三处对 Figure 5 的同一口径
  3. 仅在新扫描产生跨重复正向排他性后，再升级 Figure 5 的论证力度

## 2026-04-29 Round 11 Wrong-reference v2 Focused Scan

- 当前阶段：固定 ordinary-positive 窗口内的 wrong-reference v2 验证
- 当前唯一主瓶颈：需要确认更强 decoy 是否能把 `common minus wrong-reference` 跨重复稳定拉正
- 本轮唯一最高优先级：只测 `anti_phase_plus_decoy` 和 `task_matched_decoy`，不再扩展参数空间
- 本轮真实结果：
  - 已新增并运行 `/workspace/self-calibrating-diffractive-ncomms/scripts/round11_wrongref_v2_focused_scan.py`
  - 已固定 `num_layers=1` 与 `reference_weight=0.16`
  - 已完成 `10` 个 focused 配置、每个 `8` 次重复
  - 已生成：
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round11_wrongref_v2_repeat_rows.csv`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round11_wrongref_v2_detail.csv`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round11_wrongref_v2_summary.csv`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round11_wrongref_v2_top.csv`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round11_wrongref_v2_summary.json`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round11_wrongref_v2_summary.md`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round11_wrongref_v2_best_panel.png`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round11_wrongref_v2_best_history.json`
- 本轮关键结果：
  - 最优配置为 `anti_phase_plus_decoy` at `phase_mix=0.17`
  - 该配置下 `common minus ordinary` 均值为 `+0.491 dB`，最差重复仍为 `+0.346 dB`
  - 但 `common minus wrong-reference` 均值仅 `+0.101 dB`，最差重复仍为 `-0.013 dB`
  - 全部 `10` 个 focused 配置中，没有任何一个配置满足 `common minus ordinary` 与 `common minus wrong-reference` 的最差重复同时为正
- 当前判断：
  - `anti_phase_plus_decoy` 的确比先前 wrong-reference 构造更接近目标
  - 但它仍未跨重复稳定封闭排他性，因此 Figure 5 不能升级表述
  - `task_matched_decoy` 没有提供更强、更稳的排他性窗口
- 下一轮立即动作：
  1. 暂停继续横向扩 wrong-reference v2 家族，避免重复消耗
  2. 保持 Figure 5 为“ordinary 优势稳健、wrong-reference exclusion unresolved”
  3. 只有在出现新的结构性思路或新判据时，再重开 processor 排他性分支

## 2026-04-29 Round 12 Margin Diagnostics

- 当前阶段：Figure 5 判据诊断
- 当前唯一主瓶颈：需要区分“wrong-reference 排他性只是差一点”还是“现有判据本身不适合支撑排他性”
- 本轮唯一最高优先级：不重训，直接利用 round11 最优配置做 sample-level 与 repeat-level margin 诊断
- 本轮真实结果：
  - 已新增并运行 `/workspace/self-calibrating-diffractive-ncomms/scripts/round12_margin_diagnostics.py`
  - 已生成：
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round12_margin_sample_stats.csv`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round12_margin_repeat_stats.csv`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round12_margin_repeat_worst_samples.csv`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round12_margin_summary.json`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round12_margin_summary.md`
- 本轮关键结果：
  - 诊断对象为 round11 最优配置：`anti_phase_plus_decoy` at `phase_mix=0.17`
  - `common minus wrong-reference` 的 repeat 级正向次数为 `6/8`，最差重复仅 `-0.013 dB`
  - 所有 sample-repeat 对上，`common minus wrong-reference` 正率为 `0.708`，q10 为 `-0.054 dB`
  - 最常见最差样本为 `frame`，在 `8` 次重复中占 `5` 次；其次是 `two_spots`，占 `3` 次
  - `disk` 已经对 wrong-reference 保持 `8/8` 全正，说明并非所有 OOD 样本都不可分
- 当前判断：
  - Figure 5 当前更接近“近阈值不稳”而不是“整体判据完全失效”
  - 真正的局部失稳样本已经收敛到 `frame` 和 `two_spots`
  - 因此下一步更值得补的是面向风险样本的机制诊断或新判据，而不是再继续横向扩更多 decoy
- 下一轮立即动作：
  1. 围绕 `frame` 和 `two_spots` 单独做 per-sample 机制分析
  2. 尝试用分位数 / 胜率 / 最差样本判据替代单纯的均值 PSNR 排他性
  3. 在新判据真正跨重复稳定前，继续维持 Figure 5 的保守口径

## 2026-04-29 Round 13 Risk-sample Mechanism Analysis

- 当前阶段：Figure 5 风险样本机制拆解
- 当前唯一主瓶颈：需要解释为什么 `frame` 与 `two_spots` 会在 wrong-reference 下反复打平甚至反超，并把这个现象转成更诚实的 Figure 5 判据
- 本轮唯一最高优先级：只围绕 `frame` 与 `two_spots` 做 per-sample 机制分析，同时生成新的 Figure 5 候选判据包
- 本轮真实结果：
  - 已新增并运行 `/workspace/self-calibrating-diffractive-ncomms/scripts/round13_risk_sample_mechanism.py`
  - 已生成：
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round13_risk_sample_repeat_rows.csv`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round13_risk_sample_summary.csv`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round13_figure5_criteria.json`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round13_risk_mechanism_summary.md`
- 本轮关键结果：
  - `frame` 的 `common minus wrong-reference` 均值仅 `+0.034 dB`，最差为 `-0.158 dB`，中位数为 `-0.017 dB`，正率只有 `0.5`
  - `frame` 上 `wrong-reference` 有 `4/8` 次超过 common，`noncommon-path` 也有 `3/8` 次超过 common，说明主要是边缘/轮廓主导的歧义，而不是 common-path 的普遍失效
  - `two_spots` 的 `common minus ordinary` 仍很强，均值为 `+0.772 dB`，但 `wrong-reference` 也有 `3/8` 次超过 common，说明 sparse geometry 会让 wrong-reference 偶发跟住目标结构
  - 已生成 Figure 5 候选新判据：sample-pair positive fraction `0.708`、sample-pair q10 `-0.054 dB`、risk-sample positive fraction `0.5625`、risk worst-repeat margin min `-0.158 dB`
- 当前判断：
  - 现阶段不该再用“均值 PSNR 排他性”单独代表 Figure 5
  - 更诚实的写法应转为 paired distribution criterion：正率、低分位 margin、最差样本 margin 联合报告
  - `frame` 与 `two_spots` 已经足够解释为什么当前 exclusion 还不能写成稳定成立
- 下一轮立即动作：
  1. 把 Figure 5 主文与图注判据改写为“paired positive fraction + lower-quantile margin + worst-sample margin”
  2. 保留均值 PSNR 作为辅助量，不再作为唯一 exclusion 判据
  3. 若后续还要继续 processor 路线，优先针对 `frame` 与 `two_spots` 做结构性改写，而不是继续盲加 decoy 家族

## 2026-04-29 Figure 5 Text And Caption Rewrite

- 当前阶段：Figure 5 论文表述重写
- 当前唯一主瓶颈：需要把正文、图注和补充材料统一到新的 paired-diagnostic 证据口径
- 本轮唯一最高优先级：把 Figure 5 的主文段落、图注包和 Supplementary Figure 5 guidance 一次改齐
- 本轮真实结果：
  - 已更新 `/workspace/memory/self-calibrating-diffractive-ncomms/manuscript-v1-strict.md`
  - 已更新 `/workspace/memory/self-calibrating-diffractive-ncomms/figure5_caption_package.md`
  - 已更新 `/workspace/self-calibrating-diffractive-ncomms/scripts/generate_supplementary_pdf.py`
  - 已重生成 `/workspace/output/self-calibrating-diffractive-ncomms-supplementary.pdf`
- 本轮关键结果：
  - Figure 5 的正文已从“均值 PSNR 主导的 unresolved exclusion”改写为“paired positive fraction、lower-decile margin、worst-sample behavior 联合约束的 near-threshold exclusion”
  - 图注已明确写入 `sample-pair positive fraction = 0.708`、`lower-decile margin = -0.054 dB`，并点名 `frame` 与 `two_spots` 为主要风险样本
  - Supplementary 也已同步改成同一口径，避免正文和补充材料脱节
- 下一轮立即动作：
  1. 若继续修稿，优先把 Figure 5 视觉面板内容也改成与新判据一致
  2. 保持主文、图注、Supplementary 三处继续使用同一 paired-diagnostic 口径
  3. 在新数据未跨重复稳定前，不上调 Figure 5 的主张强度

## 2026-04-29 Figure 5 Visual Panel Rewrite

- 当前阶段：Figure 5 视觉面板重构
- 当前唯一主瓶颈：旧版面板结构仍偏向均值 PSNR 读法，和新的 paired-diagnostic 口径不一致
- 本轮唯一最高优先级：生成一版与正文、图注、Supplementary 同口径的新版 Figure 5 四联图
- 本轮真实结果：
  - 已新增并运行 `/workspace/self-calibrating-diffractive-ncomms/scripts/round14_figure5_visual_panel.py`
  - 已生成：
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/figure5_paired_diagnostic_panel.png`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/figure5_paired_diagnostic_panel.pdf`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/figure5_paired_diagnostic_panel_summary.md`
- 本轮关键结果：
  - panel a：protocol and preview strip tied to the best wrong-reference-v2 configuration
  - panel b：stable ordinary-baseline window metrics
  - panel c：repeat-level sign structure plus paired diagnostics
  - panel d：`frame` 与 `two_spots` 的 risk-sample breakdown
  - 当前视觉结构已和 Figure 5 的 paired positive fraction / q10 / worst-sample 口径对齐
- 下一轮立即动作：
  1. 如需继续精修，优先微调 panel 文案密度与投稿版式
  2. 若主文进入定稿阶段，可把这版 panel 直接接入正式 Figure 5 资产包
  3. 在新数据未产生跨重复稳定排他性前，不再退回旧的均值 PSNR-only 面板结构

## 2026-04-29 Round 15 Risk-sample Targeted Re-scan

- 当前阶段：风险样本定向重扫
- 当前唯一主瓶颈：需要验证仅靠 `phase_mix`、`reference_weight` 与 `input_phase coupling` 微调，是否足以把 `frame/two_spots` 的 q10 拉到非负
- 本轮唯一最高优先级：只针对风险样本做 targeted re-scan，并以 `q10 >= 0` 作为唯一成功标准
- 本轮真实结果：
  - 已新增并运行 `/workspace/self-calibrating-diffractive-ncomms/scripts/round15_risk_targeted_rescan.py`
  - 已固定 `wrongref_mode=anti_phase_plus_decoy`
  - 已完成 `48` 个 focused 配置、每个 `8` 次重复
  - 已生成：
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round15_risk_rescan_repeat_rows.csv`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round15_risk_rescan_detail.csv`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round15_risk_rescan_risk_rows.csv`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round15_risk_rescan_summary.csv`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round15_risk_rescan_top.csv`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round15_risk_rescan_summary.json`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round15_risk_rescan_summary.md`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round15_risk_rescan_best_panel.png`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round15_risk_rescan_best_history.json`
- 本轮关键结果：
  - 最优配置为 `phase_mix=0.16`、`reference_weight=0.16`、`input_phase_coupling=0.90`
  - 该配置的 risk-pair q10 仍为 `-0.131 dB`
  - risk-pair min 为 `-0.164 dB`
  - risk-pair positive fraction 为 `0.5625`
  - 同时 `common minus ordinary` 均值仍保留为 `+0.482 dB`
  - 全部 `48` 个配置中，没有任何一个达到 `q10 >= 0`
- 当前判断：
  - 仅靠这三个连续参数的局部微调，不足以把风险样本负尾部抬到非负
  - 当前 Figure 5 应继续保持 paired-diagnostic 口径，不应再期待通过同类小范围扫参把 exclusion 直接修正到稳定成立
  - 下一步若还要继续优化，必须引入结构性改变，而不是重复做同类局部 re-scan
- 下一轮立即动作：
  1. 停止同类型 risk-sample 微调扫描，避免重复消耗
  2. 保持 Figure 5 的当前图、文、图注口径不变
  3. 只有在提出新的结构性 wrong-reference / processor 机制后，再重开该分支

## 2026-04-29 Round 16 Structural Mode Scan

- 当前阶段：结构性 wrong-reference / input-encoding 改写
- 当前唯一主瓶颈：需要验证结构性改写是否真的优于连续微调，尤其是能否把 `frame/two_spots` 的 q10 拉到非负
- 本轮唯一最高优先级：用离散结构组合替代连续参数微调
- 本轮真实结果：
  - 已新增 `/workspace/self-calibrating-diffractive-ncomms/scripts/wrong_reference_designs_v3.py`
  - 已新增并运行 `/workspace/self-calibrating-diffractive-ncomms/scripts/round16_structural_modes_scan.py`
  - 已生成：
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round16_structural_scan_repeat_rows.csv`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round16_structural_scan_detail.csv`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round16_structural_scan_risk_rows.csv`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round16_structural_scan_summary.csv`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round16_structural_scan_top.csv`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round16_structural_scan_summary.json`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round16_structural_scan_summary.md`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round16_structural_scan_best_panel.png`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round16_structural_scan_best_history.json`
- 本轮关键结果：
  - 最优组合为 `sparse_tracker_decoy + occupancy_guarded`
  - 该组合的 risk-pair q10 为 `+0.015 dB`
  - risk-pair positive fraction 为 `0.9167`
  - `common minus ordinary` 均值为 `+0.649 dB`，最差重复仍为 `+0.571 dB`
  - 共有 `2` 个结构组合达到 `q10 >= 0`
  - 次优 `sparse_tracker_decoy + hybrid_guarded` 的 q10 为 `+0.020 dB`，但 ordinary 优势仅 `+0.352 dB`
- 当前判断：
  - 结构性改写确实优于连续微调扫描
  - 这轮首次把风险样本 q10 拉到了非负
  - 但最差 risk-sample margin 仍为负，因此 Figure 5 仍应保持 paired-diagnostic 口径，而不是直接上调为“稳定排他性已成立”
- 下一轮立即动作：
  1. 固定 `sparse_tracker_decoy + occupancy_guarded` 作为新的最优结构组合
  2. 只围绕这个结构组合做更高重复确认，而不是重新扩全空间
  3. Figure 5 可更新为“risk-sample q10 首次转正”，但仍不能删掉 near-threshold 与 worst-sample caveat

## 2026-04-29 Round 17 Structural Confirmation

- 当前阶段：最优结构组合高重复确认
- 当前唯一主瓶颈：需要确认 `sparse_tracker_decoy + occupancy_guarded` 的正 q10 不是低重复偶然结果
- 本轮唯一最高优先级：固定结构组合，只增加重复数
- 本轮真实结果：
  - 已新增并运行 `/workspace/self-calibrating-diffractive-ncomms/scripts/round17_structural_confirmation.py`
  - 已生成：
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round17_structural_confirm_repeat_rows.csv`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round17_structural_confirm_detail.csv`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round17_structural_confirm_risk_rows.csv`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round17_structural_confirm_summary.json`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round17_structural_confirm_summary.md`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round17_structural_confirm_best_panel.png`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round17_structural_confirm_best_history.json`
- 本轮关键结果：
  - 固定组合：`sparse_tracker_decoy + occupancy_guarded`
  - 重复数：`14`
  - `risk-sample q10 = +0.090 dB`
  - `risk-pair positive fraction = 0.9643`
  - `common minus ordinary` 均值为 `+0.638 dB`，最差重复仍为 `+0.413 dB`
  - `common minus wrong-reference` 均值为 `+0.278 dB`，最差重复仍为 `+0.047 dB`
  - 按 risk-sample 单样本最小值统计，仍保留一个小幅负尾部 `-0.025 dB`
- 当前判断：
  - 这轮已经足以确认：结构性改写不是偶然点，正 q10 在更高重复下能够保持
  - Figure 5 可以从“near-threshold q10 first turns positive”升级到“structural redesign sustains positive q10 under higher-repeat confirmation”
  - 但 worst-sample caveat 仍应保留，不宜把结论升级到“完全鲁棒排他性已建立”
- 下一轮立即动作：
  1. 更新 Figure 5 主文、图注和面板，写入高重复确认后的新数字
  2. 保留 `worst-sample tail still slightly negative` 的边界说明
  3. 如需继续推进，再决定是否做更高重复或扩大到完整 OOD 集确认

## 2026-04-29 Round 17 Figure 5 Text Sync

- 当前阶段：Figure 5 文稿与补充材料同步
- 当前唯一主瓶颈：round17 高重复确认已经拿到，但正文、图注、视觉面板和 Supplementary 仍停留在 round11 到 round16 的旧数字与旧口径
- 本轮唯一最高优先级：只做一件事，把 Figure 5 的所有公开叙述入口统一升级到 round17 证据边界
- 本轮真实结果：
  - 已更新 `/workspace/memory/self-calibrating-diffractive-ncomms/manuscript-v1-strict.md`
  - 已更新 `/workspace/memory/self-calibrating-diffractive-ncomms/figure5_caption_package.md`
  - 已更新 `/workspace/self-calibrating-diffractive-ncomms/scripts/round14_figure5_visual_panel.py`
  - 已更新 `/workspace/self-calibrating-diffractive-ncomms/scripts/generate_supplementary_pdf.py`
  - 已重生成：
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/figure5_paired_diagnostic_panel.png`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/figure5_paired_diagnostic_panel.pdf`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/figure5_paired_diagnostic_panel_summary.md`
    - `/workspace/output/self-calibrating-diffractive-ncomms-supplementary.pdf`
- 本轮关键结果：
  - Figure 5 正文已改写为 round17 口径：`common minus ordinary` 均值 `+0.638 dB`，最差重复 `+0.413 dB`
  - stricter wrong-reference 口径已改写为：`common minus wrong-reference` 均值 `+0.278 dB`，最差重复 `+0.047 dB`
  - paired risk 指标已改写为：q10 `+0.090 dB`，positive fraction `0.964`，同时保留单次负尾部 `-0.025 dB`
  - Figure 5 四联面板已从 round11/13 旧数据源切换到 round17 确认数据源
  - Supplementary 已从“near-threshold unresolved exclusion”升级为“structurally improved paired exclusion with one remaining negative tail event”
- 当前判断：
  - 这轮已经真正完成了 round17 结果的文稿落地，不再只是数据跑出但文本滞后
  - 当前最合适的 Figure 5 表述是“higher-repeat confirmed positive q10 with one remaining negative tail”
  - 在没有更多 OOD 扩展前，仍不宜写成 fully robust exclusion
- 下一轮立即动作：
  1. 决定是否继续做更高重复确认，专门压缩 `-0.025 dB` 尾部
  2. 或者把同一结构组合扩展到更完整 OOD 集，检查 Figure 5 升级口径能否维持
  3. 在新的真实结果出现前，保持正文、图注、面板和补充材料的现有统一口径

## 2026-04-29 Round 18 Expanded OOD Confirmation

- 当前阶段：Figure 5 升级口径的广义 OOD 检验
- 当前唯一主瓶颈：round17 的高重复确认只证明了窄风险样本子集上的 paired exclusion 改善，还没有证明这一改进能跨更完整 OOD 集保持
- 本轮唯一最高优先级：固定 `sparse_tracker_decoy + occupancy_guarded` 和 `14` 次重复，只扩展 OOD 样本集合，不再调整结构或参数
- 本轮真实结果：
  - 已新增并运行 `/workspace/self-calibrating-diffractive-ncomms/scripts/round18_expanded_ood_confirmation.py`
  - 已生成：
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round18_expanded_ood_repeat_rows.csv`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round18_expanded_ood_detail.csv`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round18_expanded_ood_pair_rows.csv`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round18_expanded_ood_sample_summary.csv`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round18_expanded_ood_summary.json`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round18_expanded_ood_summary.md`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round18_expanded_ood_best_panel.png`
- 本轮关键结果：
  - 扩展 OOD 集总数：`9`
  - expanded-pair q10：`-0.366 dB`
  - expanded-pair min：`-1.204 dB`
  - expanded-pair positive fraction：`0.611`
  - `common minus ordinary` 均值：`+0.432 dB`
  - `common minus wrong-reference` 均值：`+0.102 dB`
  - 最差新增失败样本是 `zigzag`，其 `common minus wrong-reference` 均值为 `-0.398 dB`，最差达到 `-1.204 dB`
  - 其他新增薄弱样本包括 `offcenter_disk`、`half_ring`、`triple_bars`
- 当前判断：
  - round17 的升级口径不能直接外推到更完整 OOD 集
  - 当前最诚实的 Figure 5 边界应回到“narrow risk-subset confirmation only”，而不是“broader OOD exclusion strengthened”
  - 继续单纯增加重复数已经不是主路径，因为当前主失败来自新增 OOD 样本族而不是原先那一个 `-0.025 dB` 尾部
- 下一轮立即动作：
  1. 针对 `zigzag`、`half_ring`、`triple_bars`、`offcenter_disk` 做逐样本机制诊断
  2. 判断这些失败是 reference 编码问题、形状稀疏性问题，还是 wrong-reference 结构仍能跟踪局部几何
  3. 在新诊断完成前，不要继续上调 Figure 5 的广义表述

## 2026-04-29 Round 19 Tail Mechanism And Risk Metrics

- 当前阶段：tail 机制可解释性与风险度量升级
- 当前唯一主瓶颈：round18 已知更完整 OOD 会重新拉出负尾部，但还不知道这些失败究竟是 common-path 自身失稳，还是 wrong-reference 仍然过度跟踪对象支撑
- 本轮唯一最高优先级：不再做更多重复实验，只基于 round17/18 现有结果做 tail 机制拆解和新风险度量设计
- 本轮真实结果：
  - 已新增并运行 `/workspace/self-calibrating-diffractive-ncomms/scripts/round19_tail_mechanism_risk_metrics.py`
  - 已生成：
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round19_tail_mechanism_summary.csv`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round19_risk_metrics.json`
    - `/workspace/self-calibrating-diffractive-ncomms/outputs/round19_tail_mechanism_summary.md`
- 本轮关键结果：
  - `transfer penalty q10 = -0.457 dB`
  - `tail CVaR20 = -0.444 dB`
  - `negative mass = 0.107 dB`
  - `sample failure breadth = 0.333`
  - `ordinary-window retention = 0.677`
  - `zigzag` 与 `triple_bars` 的主要机制更接近 thin/fragmented geometry 让 common-path 自身离开稳定窗口
  - `offcenter_disk`、`half_ring`、`disk` 的主要机制更接近 wrong-reference decoy 仍然通过 `occupancy_guarded` 编码贴近对象支撑
- 当前判断：
  - 继续增加重复数不会回答现在最关键的问题，因为当前主失败已经是外推结构失配，不是单一偶发尾部
  - Figure 5 后续若继续保留，必须明确限定为 narrow-subset confirmation
  - 风险讨论不应再只用 q10，应至少同时报告 `tail CVaR20`、`negative mass`、`sample failure breadth`
- 下一轮立即动作：
  1. 针对 common-path 自身失稳的一支，优先研究 `zigzag / triple_bars` 是否需要改变编码门控而不是仅改 wrong-reference
  2. 针对 decoy-tracking 的一支，优先研究 `offcenter_disk / half_ring` 是否需要削弱 sparse-tracker decoy 的对象支撑贴合度
  3. 在没有这两支机制修复前，不再把 Figure 5 往更强 exclusion 方向升级
