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
