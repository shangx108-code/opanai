# 项目状态：self-calibrating-diffractive-ncomms

## 项目基本信息
- 项目名称：Self-calibrating diffractive optical neural operators for imaging through dynamic aberrations
- 目标期刊：Nature Communications
- 最近更新时间：2026-04-29（round19-tail-metrics）

## 当前运行规则
- 默认推进主体：自研智能体
- 自动迭代频率：每 1 小时 1 轮
- 每轮必须写入：`iteration-log.md`
- 停止条件必须同时满足：
  - 所有需要补充的判据全部补齐
  - 五个审稿人的接收概率均超过 80%
  - 所有正式数据图都基于真实数据
  - 理论推导详实、可靠、可检查
  - 正文与补充材料所需图表、引用和对照组全部补齐

## 研究边界
- 当前项目按纯理论与纯仿真路线推进
- 不把实验设备、实验数据或 benchtop 验证作为当前阶段硬依赖
- 正式结果图必须来自真实计算或真实实验数据
- 未完成真实运行的代码、结果图和 benchmark 不得记为已完成

## 研究总目标
围绕“固定被动衍射处理器如何在动态像差/弱散射环境中通过共路 reference 实现自校准成像恢复”建立一条可投稿到 Nature Communications 的完整证据链，最终形成：
- 主体理论：共路 pilot 如何降低瞬时退化不确定性，以及该机制在 diffractive optical neural operator 中的成立条件、边界和失效模式
- 真实可复现的仿真链：至少覆盖 Zernike 动态像差、Kolmogorov 湍流、薄相位屏散射三类退化
- 关键对照：ordinary D2NN、pilot-assisted D2NN、非共路 reference、错误 reference、传统 Wiener / RL / blind deconvolution、电子 U-Net、理想 phase-conjugation 上限
- 正文与补充材料全套投稿级图表
- 30 篇以上已核对参考文献

## 当前阶段
最小器件级参数扫描阶段。

说明：
- round1-round4 的 surrogate、wave-optics、information-bound 和 cross-task 证据已建立。
- round5 / round5b 已有第一轮器件级 prototype 结果，但强度不足以封闭主结论。
- strict manuscript 已形成，但 Figure 5 仍然不够强。
- round6 已在当前活动工作区恢复出最小 NumPy 可复跑链。
- round7 已在当前活动工作区完成完整轻量参数扫描并生成全部数据资产。

## 当前唯一主瓶颈
当前唯一主瓶颈是：round18 已证明当前 Figure 5 口径不能外推到更广 OOD 集，而 round19 进一步表明失败并非单一来源，而是同时包含“common-path 自身离开稳定窗口”的 thin/fragmented shape failure 与“wrong-reference 过度跟踪对象支撑”的 decoy-tracking failure。

原因：
- round5 / round5b 的第一轮器件级原型仍然较弱。
- round6 的最小 NumPy 重建结果显示 common-path 相比 ordinary 仍为负向。
- round7 虽然把结果推进到了正向配置区间，但 ranking 最优配置对 wrong-reference 的分离仍不够强。
- round18 表明结构性改写的正向 paired exclusion 目前仍局限于窄风险样本子集，新增 OOD 形状如 `zigzag`、`half_ring`、`triple_bars` 与 `offcenter_disk` 会重新拉出明显负尾部。
- round19 表明 `zigzag` 与 `triple_bars` 主要是 thin/fragmented geometry 让 common-path 自身掉出 ordinary-stable window；`offcenter_disk`、`half_ring`、以及较轻的 `disk` 更接近 wrong-reference decoy 仍能通过 `occupancy_guarded` 编码跟住对象支撑。
- 网络代理限制使 `matplotlib`、`scipy`、`torch` 无法在线安装，因此后续仍需按轻量环境组织扫描。

## 本轮唯一最高优先级
停止把 Figure 5 继续朝“更强排他性”升级；下一步应优先围绕扩展 OOD 中暴露出的新失败样本做结构诊断与风险度量升级，而不是继续单纯增加重复数。

## 当前已验证结果
- round1：Gaussian surrogate 上 common-path pilot 相比 no-reference 有明确增益
- round2：Zernike wave-optics PSF 模型上，OOD 集 common-path 平均 PSNR `38.422 dB`，高于 no-reference `37.069 dB` 与 non-common-path `37.078 dB`
- round3：最小 FNO-style baseline 为中性偏负；CRLB / information-bound 已建立
- round4：cross-task surrogate 上 reconstruction、classification residual、inverse-design surrogate 出现第一轮正向信号
- round5：两层 pure-reconstruction D2NN 为中性偏负；common-path 相比 ordinary `-0.191 dB`
- round5b：三层 self-calibrating D2NN 给出第一轮弱正向 reconstruction 信号；OOD 下 common-path object-zone PSNR `11.559 dB`，ordinary `11.356 dB`，non-common-path `11.505 dB`，wrong-reference `11.350 dB`
- round6：当前活动工作区的最小 NumPy 可复跑链已恢复；OOD 下 ordinary `11.884 dB`，common-path `10.754 dB`，non-common-path `10.690 dB`，wrong-reference `10.831 dB`
- round7：参数扫描已真实完成 `45` 组配置；ranking 最优配置为 `num_layers=1, reference_weight=0.20, phase_mix=0.15`，其中 `common minus ordinary = +0.630 dB`

## 当前环境状态
- 可用：
  - Python 3.12
  - `numpy 2.3.5`
  - `Pillow 12.2.0`
  - 本地文件写入、JSON 输出、PNG 输出
  - 最小 D2NN 对照脚本真实运行与结果落盘
- 不可用：
  - `matplotlib`
  - `scipy`
  - `torch` / `torchvision`
- 当前判断：
  - 现阶段应采用 `numpy + Pillow` 路线继续补数据

## 本轮交付物
- `manuscript-v1-strict.md`
- `review-round-manuscript-v1-strict.md`
- `iteration-log.md`
- `iteration-round-2026-04-29.md`
- `/workspace/output/sc-don-drive-sync-manifest-2026-04-29.csv`
- `/workspace/self-calibrating-diffractive-ncomms/scripts/environment_smoke_test.py`
- `/workspace/self-calibrating-diffractive-ncomms/scripts/minimal_passive_d2nn_protocol.md`
- `/workspace/self-calibrating-diffractive-ncomms/scripts/round6_numpy_passive_d2nn.py`
- `/workspace/self-calibrating-diffractive-ncomms/scripts/round7_parameter_scan.py`
- round6 与 round7 全部输出资产

## 下一轮立即动作
1. 围绕 `reference_weight = 0.20` 做更细局部扫描，优先增强 `common minus wrong-reference`
2. 保留“共路、非共路、错误 reference”三组关键对照
3. 继续补真实运行数据而不是等待外部依赖
4. 每轮结束强制写入 `iteration-log.md`

## 当前稿件状态判断
- 已满足：
  - 四段式引言
  - Methods / Results / Discussion / Summary 主文结构
  - 每张图在正文中被明确引用并承担论证职责
  - 30+ 参考文献底稿
- 未满足：
  - Figure 5 仍不足以承担主文核心论点
  - 所有缺失标准未补齐
  - 五位审稿人接收概率未全部超过 80%

## 当前接收概率判断
- 综合接收概率：26%–33%
- 五审稿人最近一轮严格评估：
  - Reviewer A：36%
  - Reviewer B：18%
  - Reviewer C：23%
  - Reviewer D：41%
  - Reviewer E：17%

## 最近一次重要更新摘要
- 2026-04-27：完成 round5 两层 pure-reconstruction phase-only D2NN 对照，结果中性偏负
- 2026-04-27：完成 round5b 三层 self-calibrating phase-only D2NN 原型，得到第一轮弱正向 reconstruction 信号
- 2026-04-27：进入 strict manuscript mode，形成 `manuscript-v1-strict.md`
- 2026-04-27：完成五审稿人严格评估，接收概率仍显著低于停止标准
- 2026-04-29：恢复研究迭代并建立独立迭代日志
- 2026-04-29：完成本地环境打通
- 2026-04-29：完成 `round6_numpy_passive_d2nn.py` 的真实运行，恢复最小 ordinary / common-path / non-common-path / wrong-reference 对照数据链；结果显示 common-path 相比 ordinary 仍为负向 `-1.131 dB`
- 2026-04-29：完成 `round7_parameter_scan.py` 的真实运行，扫描 `45` 组轻量配置，并生成完整数据资产；当前已出现一批 `common-path > ordinary` 的正向配置，但对 `wrong-reference` 的分离仍偏弱
- 2026-04-29：已在 Google Drive 中确认两张现成但为空的 `SC-DON NatComm Iteration Ledger` 表，并生成本地同步清单 `sc-don-drive-sync-manifest-2026-04-29.csv`；当前真实阻塞是 Drive 写入入口缺失，而不是本地归档包缺失
- 2026-04-29：已把 neural-operator formalism 明确写入 `manuscript-v1-strict.md`，并把 Figure 4 从“cross-task”升级为“cross-domain demonstration”的论文表述；同时生成 `cross_domain_demonstration_summary.csv` 与更新后的 Supplementary PDF 资产
- 2026-04-29：完成 `round8_narrow_processor_scan.py` 的真实运行，在 round7 最优窗口附近完成 `60` 组局部配置、每组 `4` 次重复的 processor-level 扫描；当前最优稳健配置为 `num_layers=1, reference_weight=0.16, phase_mix=0.15`，其 `common minus ordinary` 均值为 `+0.438 dB`，但 `common minus wrong-reference` 均值仅 `+0.062 dB`，最差重复仍为 `-0.307 dB`
- 2026-04-29：完成 `round9_wrong_reference_targeted_scan.py` 的真实运行，固定 `num_layers=1` 与 `reference_weight=0.16` 后，对 `30` 组 targeted wrong-reference 配置做了每组 `4` 次重复；当前最佳排他性配置为 `wrongref_mode=anti_phase, phase_mix=0.20`，其 `common minus ordinary` 均值为 `+0.654 dB`，最差重复仍为 `+0.556 dB`，同时 `common minus wrong-reference` 均值为 `+0.141 dB`，最差重复仍为 `+0.027 dB`
- 2026-04-29：完成 `round10_antiphase_confirmation_scan.py` 的真实运行，对 `anti_phase` wrong-reference 在 `phase_mix=0.18-0.22` 上做了 `9` 点超窄扫描、每点 `10` 次重复；最佳确认点为 `phase_mix=0.18`，其 `common minus ordinary` 均值为 `+0.409 dB`，但 `common minus wrong-reference` 均值仅 `+0.067 dB`，最差重复回落到 `-0.103 dB`，因此 round9 出现的排他性窗口未能在更高重复数下稳定确认
- 2026-04-29：已把 Figure 5 与相关图注口径统一下调为“ordinary-baseline advantage repeat-stable, wrong-reference exclusion unresolved”，避免主张强于 round10 证据
- 2026-04-29：已新增 `wrong-reference-design-v2.md` 与 `scripts/wrong_reference_designs_v2.py` 对应的设计说明，作为下一轮 focused scan 的未验证设计输入
- 2026-04-29：已重写 Supplementary PDF 文案并重生成补充材料，使其与 round8-round10 processor 结果、Figure 5 图注口径和当前设计边界保持一致
- 2026-04-29：完成 `round11_wrongref_v2_focused_scan.py` 的真实运行，固定 `num_layers=1`、`reference_weight=0.16` 与 `phase_mix=0.14-0.18`，仅测试 `task_matched_decoy` 与 `anti_phase_plus_decoy` 两个 wrong-reference v2 候选，共 `10` 个 focused 配置、每个 `8` 次重复；当前最佳配置为 `anti_phase_plus_decoy` at `phase_mix=0.17`，其 `common minus ordinary` 均值为 `+0.491 dB`、最差重复为 `+0.346 dB`，但 `common minus wrong-reference` 均值仅 `+0.101 dB`、最差重复仍为 `-0.013 dB`，因此仍不能把 wrong-reference 排他性写成稳定成立
- 2026-04-29：完成 `round12_margin_diagnostics.py` 的真实运行，不重训任何 processor，仅复用 round11 最优配置做 sample-level 与 repeat-level margin 诊断；结果显示 `common minus wrong-reference` 在 repeat 级为 `6/8` 正、最差重复仅 `-0.013 dB`，sample-repeat 对的正率为 `0.708`、q10 为 `-0.054 dB`，最常见最差样本为 `frame`（`5/8` 次），其次为 `two_spots`（`3/8` 次），因此当前更接近“近阈值不稳”而非“全面不可分”
- 2026-04-29：完成 `round13_risk_sample_mechanism.py` 的真实运行，专门分析 round11 最优配置下 `frame` 与 `two_spots` 的 per-sample 失稳机制；结果显示 `frame` 的 `common minus wrong-reference` 均值仅 `+0.034 dB`、中位数为 `-0.017 dB`，且 `wrong-reference` 有 `4/8` 次超过 common，说明主要是 edge-dominated ambiguity；`two_spots` 的 `common minus ordinary` 仍强（均值 `+0.772 dB`），但 `wrong-reference` 也有 `3/8` 次超过 common，说明 sparse-spot geometry 会被 wrong-reference 偶发跟住；据此已准备 Figure 5 的候选新判据包：sample-pair positive fraction `0.708`、sample-pair q10 `-0.054 dB`、risk-sample positive fraction `0.5625`、risk worst-repeat margin min `-0.158 dB`
- 2026-04-29：完成 `round14_figure5_visual_panel.py` 的真实运行，生成新版 Figure 5 四联视觉面板 `figure5_paired_diagnostic_panel.png/pdf`；当前 panel 结构已改为 protocol-and-preview、stable ordinary window、paired diagnostics、以及 `frame/two_spots` risk-sample breakdown，与新的 Figure 5 正文和图注口径保持一致
- 2026-04-29：完成 `round15_risk_targeted_rescan.py` 的真实运行，仅针对 `frame` 与 `two_spots` 扫描 `phase_mix`、`reference_weight` 与 `input_phase coupling`，固定 `wrongref_mode=anti_phase_plus_decoy`，共 `48` 个 focused 配置、每个 `8` 次重复；最佳配置为 `phase_mix=0.16`、`reference_weight=0.16`、`input_phase_coupling=0.90`，其 risk-sample q10 仍为 `-0.131 dB`，risk-pair positive fraction 为 `0.5625`，但 `common minus ordinary` 均值仍保留在 `+0.482 dB`；本轮没有任何配置达到 `q10 >= 0`
- 2026-04-29：完成 `wrong_reference_designs_v3.py` 与 `round16_structural_modes_scan.py` 的真实运行，用 3 个新的结构性 wrong-reference 机制和 4 个输入编码模式替代连续微调扫描；共测试 `12` 个结构组合、每个 `6` 次重复。最佳组合为 `sparse_tracker_decoy + occupancy_guarded`，其 risk-sample q10 首次达到 `+0.015 dB`，risk-pair positive fraction 提升到 `0.9167`，同时 `common minus ordinary` 均值为 `+0.649 dB`、最差重复仍为 `+0.571 dB`；次优组合 `sparse_tracker_decoy + hybrid_guarded` 也达到 `q10 = +0.020 dB`，但 ordinary 优势明显更弱，因此当前最值得保留的是 `sparse_tracker_decoy + occupancy_guarded`
- 2026-04-29：完成 `round17_structural_confirmation.py` 的真实运行，只对 `sparse_tracker_decoy + occupancy_guarded` 做高重复确认，共 `14` 次重复；确认结果为 `risk-sample q10 = +0.090 dB`，risk-pair positive fraction = `0.9643`，`common minus ordinary` 均值为 `+0.638 dB`、最差重复仍为 `+0.413 dB`，且 `common minus wrong-reference` 的重复均值为 `+0.278 dB`、最差重复仍为 `+0.047 dB`；但按 risk-sample 最小值统计，仍存在单次负尾部 `-0.025 dB`，因此当前最诚实的升级口径应是“structural redesign makes q10 positive under higher-repeat confirmation”，而不是“all worst-case failures removed”
- 2026-04-29：已把 round17 的确认结果同步写入 `manuscript-v1-strict.md`、`figure5_caption_package.md`、`round14_figure5_visual_panel.py` 与 `generate_supplementary_pdf.py`，并重生成 Figure 5 四联面板与 `/workspace/output/self-calibrating-diffractive-ncomms-supplementary.pdf`；当前统一口径为“ordinary-baseline advantage repeat-stable, structurally improved paired exclusion with one remaining negative tail event”
- 2026-04-29：完成 `round18_expanded_ood_confirmation.py` 的真实运行，在不改变 `sparse_tracker_decoy + occupancy_guarded` 结构和 `14` 次重复的前提下，把 OOD 集从原始 `3` 个样本扩展到 `9` 个未见形状；结果显示 expanded-pair q10 回落到 `-0.366 dB`，最差样本达到 `-1.204 dB`，positive fraction 仅 `0.611`。最差新增样本是 `zigzag`，其次是 `offcenter_disk`、`half_ring` 与 `triple_bars`，说明 round17 的升级口径不能直接外推到更完整 OOD 集
- 2026-04-29：完成 `round19_tail_mechanism_risk_metrics.py` 的真实运行，不增加任何重复实验，只对 round18 的失败尾部做机制拆解与新风险度量计算；结果显示 `transfer penalty q10 = -0.457 dB`、`tail CVaR20 = -0.444 dB`、`negative mass = 0.107 dB`、`sample failure breadth = 0.333`、`ordinary-window retention = 0.677`。机制上，`zigzag` 与 `triple_bars` 主要属于 thin/fragmented shape 导致 common-path 本身失稳，而 `offcenter_disk`、`half_ring`、`disk` 更接近 wrong-reference decoy 在 `occupancy_guarded` 编码下过度贴近对象支撑
