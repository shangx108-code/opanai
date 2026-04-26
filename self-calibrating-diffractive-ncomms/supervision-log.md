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
