# 项目状态：self-calibrating-diffractive-ncomms

## 项目基本信息
- 项目名称：Self-calibrating diffractive optical neural operators for imaging through dynamic aberrations
- 目标期刊：Nature Communications
- 最近更新时间：2026-04-27（writing-launch）
- 当前资料来源：
  - `/workspace/user_files/01-markdown-1-md-3`
  - `/workspace/self-calibrating-diffractive-ncomms/round1_theory_note.md`
  - `/workspace/self-calibrating-diffractive-ncomms/outputs/round1_summary.md`
  - `/workspace/self-calibrating-diffractive-ncomms/round2_theory_note.md`
  - `/workspace/self-calibrating-diffractive-ncomms/outputs/round2_summary.md`
  - `/workspace/self-calibrating-diffractive-ncomms/outputs/round3_fno_style_summary.md`
  - `/workspace/self-calibrating-diffractive-ncomms/round3_information_bound_note.md`
  - `/workspace/self-calibrating-diffractive-ncomms/outputs/round3_crlb_summary.md`
  - `/workspace/self-calibrating-diffractive-ncomms/round3_experiment_feasibility_note.md`
  - `/workspace/self-calibrating-diffractive-ncomms/round4_tight_bound_note.md`
  - `/workspace/self-calibrating-diffractive-ncomms/outputs/round4_cross_task_summary.md`

## 当前运行规则
- 默认推进主体：自研智能体
- 自动迭代频率：每 1 小时 1 轮
- 停止条件必须同时满足：
  - 保守五审稿人接收概率均超过 70%
  - 所有需要补的 evidence 全部补齐
  - 所有正式数据图都基于真实数据
  - 理论推导详实、可靠、可检查
  - 正文与补充材料所需图表、引用和对照组全部补齐
- 研究边界：
  - 当前项目按纯理论与纯仿真路线推进
  - 不把实验设备、实验数据或 benchtop 验证作为当前阶段硬依赖
  - 允许在论文中讨论 future experimental pathway，但不得把实验验证写成当前待补的必做证据，除非后续条件发生变化
- 图表规则：
  - 机制示意图、结构示意图、概念图可用 GPT-imag-2.0 生成初稿
  - 除示意图外，所有图必须来自真实计算或真实实验数据
  - AI 示意图不得直接视为定稿
- 理论规则：
  - 未完成详细推导的结论不得写成已证明
  - 未完成真实运行的代码、结果图与 benchmark 不得记为已完成

## 研究总目标
围绕“固定被动衍射处理器如何在动态像差/弱散射环境中通过共路 reference 实现自校准成像恢复”建立一条可投稿到 Nature Communications 的完整证据链，最终形成：
- 主体理论：共路 pilot 如何降低瞬时退化不确定性，以及该机制在 diffractive optical neural operator 中的成立条件、边界和失效模式
- 真实可复现实验链：至少覆盖 Zernike 动态像差、Kolmogorov 湍流、薄相位屏散射三类退化
- 真实可复现实验链：
  - 当前版本限定为真实可复现的理论推导、数值计算、仿真数据与仿真图表
  - 至少覆盖 Zernike 动态像差、Kolmogorov 湍流、薄相位屏散射三类退化
- 关键对照：ordinary D2NN、pilot-assisted D2NN、非共路 reference、错误 reference、传统 Wiener / RL / blind deconvolution、电子 U-Net、理想 phase-conjugation 上限
- 正文与补充材料全套投稿级图表
- 30 篇以上已核对参考文献
- 可归档的代码、数据、图表、正文、补充材料与最终投稿包

## 当前阶段
严格写作与器件级主结果校准并行阶段（已得到第一轮最小 D2NN 原型对照，但强度不足以封闭主结论）。

说明：
- 当前工作区之前没有该项目的既有命名空间记忆。
- 本轮已把上传提案正式转入项目状态，并完成第一轮最小真实数值验证。
- 现在已进一步完成 round2：真实运行基于 Zernike pupil 的 wave-optics PSF 最小证据链。
- 现在已进一步完成 round3：加入最小 FNO-style spectral baseline、CRLB 扫描，以及实验边界澄清。
- 现在已进一步完成 round4：加入 task-level tight bound / theorem，以及 classification / inverse-design surrogate 的 cross-task 泛化仿真。
- 本轮已新增第一轮真实器件级 prototype：先做了纯重建型两层 D2NN，对 common-path pilot 给出中性偏负结果；随后升级为带 calibration readout 区的三层相位型 D2NN，得到弱正向 reconstruction 信号。
- 当前仍不是完整 submission-grade D2NN 主结果，也不是投稿级证据链。
- 写作骨架仍有效，但 Figure 5 不再是“完全缺失”，而是“已有第一轮弱原型，不足以承担主文 pivot”。

## 当前唯一主瓶颈
当前唯一主瓶颈是：虽然已经得到同一动态像差协议下的第一轮 ordinary D2NN 与 pilot-assisted D2NN 最小原型对照，但 common-path 优势过弱，且 calibration readout 没有形成一致正向证据，因此 Figure 5 仍不足以支撑主文核心论点。

原因：
- 目前已证明“共路 pilot 降低动态退化不确定性”的最小机制，在 Gaussian surrogate 与 Zernike wave-optics PSF 两层模型上都成立。
- 当前新增的最小 FNO-style spectral baseline没有自动恢复出这一优势，因此“ML 说服力”仍未闭环。
- 尽管 round4 已在任务层面看到正向 cross-task 信号，但这一点仍然建立在 aberration-aware inverse / surrogate task maps 上，不是被动衍射处理器本身的器件级证据。
- 当前 round5b 只显示 object-zone PSNR 的弱提升：common-path 相比 ordinary 为 `+0.204 dB`，相比 non-common-path 为 `+0.054 dB`，相比 wrong-reference 为 `+0.209 dB`；这还不是足够稳健的主结果。
- 同一 round5b 中 coefficient readout MAE 没有变好，说明“自校准”还没有在器件级被清晰读出。
- 若后续仍不能把 processor-level common-path 优势从“弱、可疑、架构相关”提升到“清晰、稳健、可解释”，论文主线需要重评。

## 本轮唯一最高优先级
用真实最小 phase-only D2NN 原型把 Figure 5 从“完全缺失”推进到“已有第一轮可审查结果”，并据此重写稿件边界与下一轮任务，而不是继续把该缺口当作纯占位项。

## 本轮交付物
1. round1 最小机制脚本：`/workspace/self-calibrating-diffractive-ncomms/round1_pilot_selfcalibration.py`
2. round1 理论说明：`/workspace/self-calibrating-diffractive-ncomms/round1_theory_note.md`
3. round2 wave-optics 脚本：`/workspace/self-calibrating-diffractive-ncomms/round2_zernike_waveoptics.py`
4. round2 理论说明：`/workspace/self-calibrating-diffractive-ncomms/round2_theory_note.md`
5. round2 指标表：`/workspace/self-calibrating-diffractive-ncomms/outputs/round2_metrics.csv`
6. round2 汇总 JSON：`/workspace/self-calibrating-diffractive-ncomms/outputs/round2_summary.json`
7. round2 汇总说明：`/workspace/self-calibrating-diffractive-ncomms/outputs/round2_summary.md`
8. round2 结果面板：`/workspace/self-calibrating-diffractive-ncomms/outputs/round2_zernike_waveoptics_panel.png`
9. round3 FNO-style baseline：`/workspace/self-calibrating-diffractive-ncomms/round3_fno_style_baseline.py`
10. round3 FNO-style 汇总：`/workspace/self-calibrating-diffractive-ncomms/outputs/round3_fno_style_summary.md`
11. round3 CRLB 脚本：`/workspace/self-calibrating-diffractive-ncomms/round3_information_bound.py`
12. round3 理论说明：`/workspace/self-calibrating-diffractive-ncomms/round3_information_bound_note.md`
13. round3 CRLB 汇总：`/workspace/self-calibrating-diffractive-ncomms/outputs/round3_crlb_summary.md`
14. round3 实验可行性说明：`/workspace/self-calibrating-diffractive-ncomms/round3_experiment_feasibility_note.md`
15. round4 cross-task 脚本：`/workspace/self-calibrating-diffractive-ncomms/round4_cross_task_generalization.py`
16. round4 cross-task 汇总：`/workspace/self-calibrating-diffractive-ncomms/outputs/round4_cross_task_summary.md`
17. round4 tight bound note：`/workspace/self-calibrating-diffractive-ncomms/round4_tight_bound_note.md`
18. 写作启动记录：`/workspace/memory/self-calibrating-diffractive-ncomms/manuscript-writing-launch-2026-04-27.md`
19. 主文骨架：`/workspace/memory/self-calibrating-diffractive-ncomms/manuscript-v0-structure.md`
20. reference ledger：`/workspace/memory/self-calibrating-diffractive-ncomms/reference-ledger-v1.md`
21. round5 两层重建型 D2NN 脚本：`/workspace/self-calibrating-diffractive-ncomms/round5_minimal_d2nn_comparison.py`
22. round5 指标表：`/workspace/self-calibrating-diffractive-ncomms/outputs/round5_minimal_d2nn_metrics.csv`
23. round5 汇总：`/workspace/self-calibrating-diffractive-ncomms/outputs/round5_minimal_d2nn_summary.md`
24. round5 面板：`/workspace/self-calibrating-diffractive-ncomms/outputs/round5_minimal_d2nn_panel.png`
25. round5b 自校准 D2NN 脚本：`/workspace/self-calibrating-diffractive-ncomms/round5b_selfcalibrating_d2nn.py`
26. round5b 指标表：`/workspace/self-calibrating-diffractive-ncomms/outputs/round5b_selfcalibrating_d2nn_metrics.csv`
27. round5b 汇总：`/workspace/self-calibrating-diffractive-ncomms/outputs/round5b_selfcalibrating_d2nn_summary.md`
28. round5b 面板：`/workspace/self-calibrating-diffractive-ncomms/outputs/round5b_selfcalibrating_d2nn_panel.png`

## 本轮完成标准
- 已真实运行 round2 脚本并落盘结果文件
- 已把 stronger forward model 下“共路 vs 非共路 vs 无 reference”的差异写成可检查指标
- 已明确写出 round2 仍不是 D2NN 证据、仍不可包装成 submission-grade 结论
- 已真实运行 round3 FNO-style baseline 与 CRLB 扫描
- 已把简单实验验证诚实降级为“当前缺硬件与原始数据，只能先给出最小实验方案”
- 已真实运行 round4 cross-task 泛化仿真并落盘结果
- 已写出 round4 task-level tight bound / theorem note
- 已建立四段式引言、正文结构、图文映射和 30+ reference ledger 初稿
- 已真实运行 round5 两层 phase-only D2NN 最小对照，并记录其对 common-path pilot 的中性偏负结果
- 已真实运行 round5b 带 calibration readout 的三层 phase-only D2NN，并得到第一轮弱正向 processor-level reconstruction 信号
- 已把 Figure 5 从“缺失”更新为“已有第一轮原型，但仍不足以作为最终主结果”

## 下一轮立即动作
1. 围绕 round5b 继续增强 Figure 5：优先把 common-path 相比 ordinary / non-common-path / wrong-reference 的优势从弱信号抬升到稳健信号。
2. 明确拆分“reconstruction gain”和“calibration readout gain”，避免把前者误写成后者。
3. 在不引入新主线的前提下做最小稳健性检查，例如 seed / pilot amplitude / layer count 的局部扫描。
4. 若 processor-level 优势变强，再扩展到 turbulence / thin phase screen；若仍弱，则考虑收缩期刊目标或重写主张边界。

## 技术状态检查结论
- 已验证：
  - 上传提案已转为当前项目主线。
  - 最小数值证据链已真实运行并输出 CSV / JSON / Markdown / PNG。
  - OOD stronger-aberration 集上，共路 pilot 较无 reference 有明确增益。
  - Zernike defocus + astigmatism 的 wave-optics pupil forward model已真实运行。
  - 在 OOD stronger-aberration 集上，共路 pilot 相比无 reference 将平均 PSNR 从 `37.069 dB` 提升到 `38.422 dB`，非共路仅为 `37.078 dB`。
  - OOD 集上，共路 pilot 的 mean PSF MSE 为 `4.217e-06`，优于无 reference 的 `1.279e-05` 与非共路的 `1.155e-05`。
  - round3 已真实加入最小 FNO-style spectral baseline 与 CRLB 扫描。
  - round4 已真实加入 cross-task 泛化仿真与 task-level tight bound note。
  - round5 两层 pure-reconstruction D2NN 已真实运行；结果为 common-path 相比 ordinary `-0.191 dB`，相比分别 non-common-path 与 wrong-reference 为 `+0.031 dB` 与 `+0.227 dB`，属于中性偏负证据。
  - round5b 三层 self-calibrating D2NN 已真实运行；OOD 下 common-path object-zone PSNR 为 `11.559 dB`，ordinary 为 `11.356 dB`，non-common-path 为 `11.505 dB`，wrong-reference 为 `11.350 dB`。
- 部分验证：
  - 共路 pilot 降低动态退化不确定性的机制，在 Gaussian surrogate 与 Zernike wave-optics PSF 两层模型上成立。
  - 该机制在 cross-task surrogate 上已有第一轮任务级正向信号：OOD 下 common-path 相比 no-reference 将 reconstruction PSNR 从 `34.837 dB` 提升到 `36.782 dB`，将 classification true-class residual 从 `0.035464` 降到 `0.034616`，并小幅改善 inverse-design target MSE。
  - 固定被动衍射处理器层面现在已有第一轮最小原型信号，但强度很弱，且 calibration readout MAE 未优于 ordinary，因此只能记为部分验证。
- 未验证：
  - Zernike、湍流、薄相位屏三类真实波动光学退化。
  - stronger processor-level robustness：包括 seed 稳定性、pilot 强度窗口、层数 / aperture 缩放后的趋势。
  - 强 ML baseline（完整深 FNO / U-Net / 其他现代神经算子）的正面对照。
  - 制造误差、量化误差、错位、波长漂移和 shot noise 鲁棒性。
  - 真实实验数据（当前已从主线依赖中移除，不作为本阶段硬门槛）。
- 存在错误：
  - 无。
- 待核实：
  - 上传提案给出的部分参考文献是否全部准确、可用且与主张一致。

## 环境配置负责人结论
- 当前环境检查范围：Python 3.12、NumPy、Pillow、本地文件写入、PNG 导出
- 已验证可运行链路：
  - Python + NumPy 数值模拟
  - CSV / JSON / Markdown / PNG 输出
  - Zernike pupil PSF 生成与 wave-optics-informed 数据链
- 已验证可生成的图片链路：
  - Pillow 可生成结果 panel PNG
- 已验证可编译的 PDF 链路：
  - 本轮未测试 PDF 编译，当前记为待验证
- 当前存在的环境问题：
  - `matplotlib` 不可用
  - `scipy` 不可用
  - `torch` / `torchvision` 不可用
- 待安装、待修复或待核实项：
  - 若下一轮采用 D2NN / FNO 训练，需要确认是否继续使用纯 NumPy 方案，或补齐更合适的训练环境
- 是否支持进入下一步程序运行、图片生成或论文编译：
  - 支持继续做小规模数值验证和 PNG 图生成
  - 尚不支持默认按深度学习训练链直接展开

## 稿件状态检查结论
- 已满足：
  - 题目主线、核心主张、关键对照框架已有第一版方向定义
  - 现在已有两轮真实证据，而不是只有选题草案
  - 已启动严格写作流程，并建立四段式引言、正文结构、图文映射与 30+ reference ledger 初稿
  - Figure 5 已不再是空占位，已有第一轮 processor-level prototype 可供审稿式判断
- 部分满足：
  - 摘要雏形和主图规划已有提案，但仍是前期构想，不可视为稿件实物
  - “共路 pilot 优于非共路 / 无 reference”的核心机制已有两轮真实数据支撑，但仍未到稿件主结果标准
  - 现在已有一轮 task-level theorem、一轮 cross-task 泛化结果和一轮最小器件级 prototype，但仍需要更强、更稳健的器件级主证据
- 存在新的负面或中性证据：
  - 最小 FNO-style spectral baseline 未显示 common-path pilot 优于 observation-only baseline，说明 ML 说服力仍未闭环
  - 最小两层 pure-reconstruction D2NN 给出中性偏负结果，说明“只加 pilot 不显式自校准”并不会自然形成优势
  - round5b 的 processor-level gain 仍然很弱，且 calibration readout MAE 未改善
- 未满足：
  - 正文、补充材料、正式图、图注、引用链、参考文献库均未形成投稿级实物
  - 尽管已启动主文骨架且 Figure 5 有了原型，但仍未达到 submission-ready manuscript
- 存在错误：
  - 若将当前 surrogate 结果直接包装为“固定被动衍射网络已实现自校准恢复”，会构成过度陈述
- 待核实：
  - 目标期刊最合适的故事边界，是否更偏 Nature Communications 还是更适合 Optica / Light 级别
- 是否支持进入下一阶段：
  - 支持进入“增强 Figure 5 稳健性”的阶段，不支持进入正式成稿阶段

## 当前接收概率判断
- 综合接收概率：24%–30%

依据：
- 创新构想：中到强
- 最小机制信号：中到中强
- 理论层强度：中
- cross-task 任务级说服力：中
- 理论充分性：中偏弱
- 方法与代码可靠性：中
- 数据与结果完整性：弱到中偏弱
- 图表质量：弱
- 写作成熟度：弱

最拖累接收概率的短板：
1. 真实被动衍射处理器 + 动态像差协议下虽已有第一轮对照，但优势太弱，仍不足以支撑主故事
2. 强 ML baseline 目前没有形成正向加分证据
3. 还没有三类退化、投稿级正文/补图/参考文献链，以及更强鲁棒性验证

## 最近一次重要更新摘要
- 2026-04-26：基于上传提案初始化 `self-calibrating-diffractive-ncomms` 项目命名空间。
- 2026-04-26：完成 round1 最小机制验证，使用 shared-blur Gaussian pilot surrogate 检验共路 pilot 降低动态退化不确定性的基本方向是否成立。
- 2026-04-26：OOD stronger-aberration 集上，无 reference 平均 PSNR 为 `19.669 dB`，共路 pilot 为 `21.990 dB`，非共路 pilot 为 `20.268 dB`。
- 2026-04-26：完成 round2 wave-optics 最小证据链，使用 Zernike defocus + astigmatism pupil 生成真实 PSF；OOD 集上，无 reference 平均 PSNR 为 `37.069 dB`，共路 pilot 为 `38.422 dB`，非共路 pilot 为 `37.078 dB`，且共路 pilot 的 mean PSF MSE 最低。
- 2026-04-26：完成 round3 最小 FNO-style spectral baseline。当前结果为中性偏负：OOD 集上 observation-only 为 `37.286 dB`，common-path pilot 为 `37.224 dB`，说明最小线性 spectral baseline 还没有自动学会利用 pilot。
- 2026-04-26：完成 round3 information bound / CRLB 扫描。当前 pilot-channel CRLB 在 train 与 OOD 区域的中位数 trace 分别为 `6.452e-04` 与 `1.736e-04`，说明该 pilot observation model 在大部分区域内确实携带有限 Fisher 信息。
- 2026-04-26：根据用户最新约束，项目正式收敛为“仅理论与仿真研究”；后续不再把实验验证作为当前阶段硬依赖。
- 2026-04-27：完成 round4 tight bound / theorem note，将 pilot-channel covariance 与下游任务损失通过局部曲率 sandwich 和 CRLB-limited floor 联系起来。
- 2026-04-27：完成 round4 cross-task 泛化仿真。OOD 下 common-path 相比 no-reference 将 reconstruction PSNR 从 `34.837 dB` 提升到 `36.782 dB`，将 classification true-class residual 从 `0.035464` 降到 `0.034616`，并将 inverse-design target MSE 从 `0.002317` 小幅降到 `0.002315`。
- 2026-04-27：正式启动严格写作流程，新增主文骨架、图文映射和 30+ reference ledger 初稿；同时保留“普通 D2NN vs pilot-assisted D2NN 器件级阳性对照尚未完成”的明确边界。
- 2026-04-27：完成 round5 两层 pure-reconstruction phase-only D2NN 对照。OOD 下 common-path 相比 ordinary 为 `-0.191 dB`，给出中性偏负结果。
- 2026-04-27：完成 round5b 三层 self-calibrating phase-only D2NN 原型。OOD 下 common-path object-zone PSNR 相比 ordinary 提升 `+0.204 dB`，但相对 non-common-path 仅 `+0.054 dB`，且 coefficient readout MAE 未改善，因此 Figure 5 只获得了第一轮弱原型证据。
