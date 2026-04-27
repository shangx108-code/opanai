# 监督记录：self-calibrating-diffractive-ncomms

## 2026-04-26 Round 1

### 当前检查范围
- 上传提案是否已转化为单一项目主线
- 本轮是否真正完成了一个可检查的数值闭环
- 输出是否存在夸大

### 已确认正确的部分
- 已新建项目命名空间并保存项目状态。
- 已真实运行最小数值脚本，并生成 CSV、JSON、Markdown 和 PNG。
- 当前 summary 明确承认：这是 Gaussian dynamic-defocus surrogate，不是完整 D2NN 结果。
- OOD stronger-aberration 集上，共路 pilot 的平均 PSNR 高于无 reference 与非共路 reference。

### 当前存在的问题或错误
- 证据仍然过弱，只能支持“继续推进”而不能支持“论文主张已成立”。
- 还没有 ordinary D2NN vs pilot-assisted D2NN 的真实对照。
- 还没有 Zernike / turbulence / scattering 三类真实退化结果。

### 尚未验证或待核实的部分
- 参考文献准确性与目标期刊匹配度
- 真实 wave-optics 下的正结果是否仍成立
- 后续训练环境是否需要额外依赖

### 对当前阶段真实状态的判断
- 当前处于“机制是否值得继续扩展”的前置证据阶段。
- 不支持进入正式成稿。

### 是否支持进入下一阶段
- 支持进入 round2 wave-optics 真实对照构建。
- 不支持跳过对照直接写稿或画定稿图。

### 自动化迭代任务判断
- 当前只应保留这一轮每 2 小时 1 次的项目迭代。
- 尚未发现同项目重复迭代任务，但后续若新增任务，需检查是否冲突。

## 2026-04-26 Round 2

### 当前检查范围
- round2 是否真正把 forward model 升级为 wave-optics pupil
- 结果是否仍支持共路 pilot 主线
- 是否出现过度陈述

### 已确认正确的部分
- 已真实运行 `round2_zernike_waveoptics.py` 并输出 CSV、JSON、Markdown 和 PNG。
- round2 forward model 使用了基于 Zernike defocus + astigmatism 的 pupil 来生成 PSF。
- OOD 集上，共路 pilot 的平均 PSNR 为 `38.422 dB`，优于无 reference 的 `37.069 dB` 与非共路的 `37.078 dB`。
- OOD 集上，共路 pilot 的 mean PSF MSE 为 `4.217e-06`，优于无 reference 与非共路。

### 当前存在的问题或错误
- 仍然没有真实 passive diffractive processor 层面的对照。
- round2 的 coefficient L1 error 没有优于无 reference，因此不应把“参数恢复更准”写成主结论。

### 尚未验证或待核实的部分
- passive diffractive processor 是否保留相同优势
- turbulence / thin phase screen 是否仍为阳性
- 参考文献链与期刊匹配度

### 对当前阶段真实状态的判断
- 当前已经越过“纯 idea / 纯 surrogate”阶段，进入“有两轮真实机制证据，但仍未触及核心器件证据”的状态。

### 是否支持进入下一阶段
- 支持进入 round3 最小被动衍射处理器对照。
- 不支持进入正式成稿。

### 自动化迭代任务判断
- 继续保留每 2 小时 1 次的单项目迭代。

## 2026-04-26 Round 3

### 当前检查范围
- FNO baseline 是否真实运行
- 实验验证是否存在过度陈述
- CRLB 是否形成真实理论补强

### 已确认正确的部分
- 已真实运行 `round3_fno_style_baseline.py`。
- 已真实运行 `round3_information_bound.py` 并输出 CRLB 数据与图。
- 已写出实验可行性说明，并明确当前没有硬件和原始数据。

### 当前存在的问题或错误
- 最小 FNO-style spectral baseline 没有显示 common-path pilot 优于 observation-only baseline。
- 因此 ML 说服力并未因本轮而正向闭合。

### 尚未验证或待核实的部分
- 完整深 FNO / U-Net / 条件神经算子是否会恢复 pilot 优势
- 真实实验数据
- 被动衍射处理器层面对照

### 对当前阶段真实状态的判断
- 当前理论层比前两轮更强，但 ML 侧 baseline 暂时给出的是中性偏负信号。

### 是否支持进入下一阶段
- 支持继续推进被动衍射处理器核心对照。
- 不支持把 round3 的 ML baseline 写成正向亮点。

### 自动化迭代任务判断
- 继续保留每 2 小时 1 次的单项目迭代。

## 2026-04-26 Scope Update

### 当前检查范围
- 用户是否已明确限定项目为纯理论与纯仿真路线

### 已确认正确的部分
- 用户已明确说明当前没有实验设备，仅做理论和仿真相关研究。

### 当前存在的问题或错误
- 无。

### 对当前阶段真实状态的判断
- 实验验证从“若条件允许可补充”调整为“当前不作为主线依赖”。

### 是否支持进入下一阶段
- 支持继续推进理论、仿真、ML baseline、被动衍射处理器对照与投稿级图稿。
- 不再把实验数据缺失视为当前主瓶颈。

## 2026-04-27 Round 4

### 当前检查范围
- tight bound / theorem 是否已形成可检查文本
- cross-task 泛化是否真正运行并落盘

### 已确认正确的部分
- 已新增 `round4_tight_bound_note.md`，把 CRLB 推进到任务级 loss sandwich 与 local floor。
- 已真实运行 `round4_cross_task_generalization.py` 并生成 CSV、JSON、Markdown 和 PNG。
- OOD 集上，common-path 在 reconstruction、classification true-class residual 和 inverse-design surrogate 上都优于 no-reference。

### 当前存在的问题或错误
- classification accuracy 本身在当前原型任务上已饱和，因此不能把“accuracy 未提升”误读成机制无效。
- inverse-design surrogate 的改进幅度仍然较小，当前只能写成“弱正向信号”。

### 尚未验证或待核实的部分
- task-level theorem 的数值 tightness 常数 `alpha_T / beta_T`
- 更难 classification 任务或训练型 classifier 下是否仍然成立
- 被动衍射处理器层面的 cross-task 对照

### 对当前阶段真实状态的判断
- 理论与 task-level 叙事已明显加强，但最核心的器件级主证据仍未到位。

### 是否支持进入下一阶段
- 支持进入被动衍射处理器最小对照构建。
- 支持把 round4 theorem 与 cross-task 结果作为后续文稿骨架的一部分。

## 2026-04-27 Writing Launch

### 当前检查范围
- 是否可以在不夸大现有证据的前提下启动严格论文写作流程
- 写作结构是否已经与当前真实证据边界对齐

### 已确认正确的部分
- 已建立四段式引言、Methods / Results / Discussion / Summary 主文结构。
- 已建立 figure-to-text argument map，明确每张图在正文中的论证职责。
- 已建立超过 30 篇的参考文献初始账本，并把关键论断与引用做了第一轮映射。

### 当前存在的问题或错误
- 写作启动并不等于稿件成熟；最关键的 passive processor 对照仍未完成。
- 部分新增参考文献属于候选扩展文献，还不能全部直接进入最终参考文献表。

### 尚未验证或待核实的部分
- ordinary D2NN vs pilot-assisted D2NN 的统一协议结果
- Figure 5 主结果包
- 部分 2026 年候选文献的最终卷期页码与是否进入主文

### 对当前阶段真实状态的判断
- 当前支持进入“严格写作 + 继续补主证据”的并行推进阶段。
- 当前仍不支持宣布可投稿。

## 2026-04-27 Round 5 / 5b

### 当前检查范围
- 最小 phase-only D2NN 器件级对照是否已真实运行
- common-path 优势是否在 processor level 上出现
- Figure 5 是否可从占位项升级为真实原型

### 已确认正确的部分
- 已真实运行 `round5_minimal_d2nn_comparison.py` 并生成 CSV、JSON、Markdown、PNG、NPZ。
- 已真实运行 `round5b_selfcalibrating_d2nn.py` 并生成 CSV、JSON、Markdown、PNG、NPZ。
- round5b 在 OOD 集上给出第一轮弱正向 reconstruction 信号：common-path object-zone PSNR 为 `11.559 dB`，ordinary 为 `11.356 dB`，wrong-reference 为 `11.350 dB`。
- Figure 5 现在已有真实原型图，不再是纯占位。

### 当前存在的问题或错误
- round5 的最小两层重建型 D2NN 是中性偏负结果，说明当前器件级主线并不天然稳健。
- round5b 的 common-path 相比 non-common-path 仅 `+0.054 dB`，增益太弱。
- round5b 的 coefficient readout MAE 未优于 ordinary，因此不能把它写成“已经实现清晰自校准”。

### 尚未验证或待核实的部分
- seed 稳定性
- pilot amplitude / layer count 的局部鲁棒性窗口
- turbulence / thin phase screen 下是否仍保留相同方向
- 更强数字基线与器件级对照的最终关系

### 对当前阶段真实状态的判断
- 当前已从“缺失 processor-level 结果”进入“已有 processor-level 弱原型，但仍不足以封闭主文结论”的阶段。

### 是否支持进入下一阶段
- 支持进入 Figure 5 稳健性增强阶段。
- 不支持宣称所有缺失标准已满足。
