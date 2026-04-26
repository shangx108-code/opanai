# 审稿历史：self-calibrating-diffractive-ncomms

## Round 1 内部严格审稿

### 检查范围
- 机制主张与当前证据是否一致
- 当前结果是否足以支持 Nature Communications 级叙述

### 主要意见
1. 当前结果只验证了一个 Gaussian surrogate 机制，不支持把“pilot-assisted diffractive neural operator”当成已验证事实。
2. 论文成败关键对照仍缺失：ordinary D2NN vs pilot-assisted D2NN，且必须在 OOD 动态退化下成立。
3. 非共路 reference 的对照虽然已有最小 surrogate 结果，但尚未在 wave-optics 下验证。
4. 目前没有 30+ 可核对参考文献链，也没有正文/补充材料实物。

### 审稿判断
- 当前不具备投稿条件。
- 当前仅支持继续投入下一轮真实证据生成。

### 接收概率变化依据
- 从“无项目状态”提升到“有最小真实机制验证”，因此项目从不可判断提升到 `8%–12%` 的非常早期水平。
- 该提升不来自写作，而来自实际运行结果。

## Round 2 内部严格审稿

### 检查范围
- round2 是否比 round1 真正更接近论文主张
- 当前结果是否足以支撑更强 claims

### 主要意见
1. round2 是实质性前进，因为 forward model 已从 Gaussian surrogate 升到 Zernike wave-optics pupil。
2. 共路 pilot 的图像恢复优势在 OOD stronger-aberration 集上仍然存在，因此主线继续成立。
3. 不能把 coefficient L1 error 写成 round2 的主亮点；更稳妥的状态量是 PSF 匹配误差和重建质量。
4. 当前仍然缺 ordinary D2NN vs pilot-assisted D2NN 的最小真实 processor 对照，这仍是下一轮唯一主瓶颈。

### 审稿判断
- 当前仍不具备投稿条件。
- 但项目已从“是否值得继续做”提升到“值得投入下一轮器件级最小对照”。

### 接收概率变化依据
- round2 提供了比 round1 更接近论文主张的真实物理 forward model，因此将接收概率谨慎上调到 `14%–18%`。

## Round 3 内部严格审稿

### 检查范围
- FNO baseline、实验验证与信息论补强是否真实落地

### 主要意见
1. FNO baseline 已经加上，但当前只是最小 FNO-style spectral operator，不是完整深 FNO。
2. 更重要的是，这个 baseline 没有显示 common-path pilot 优于 observation-only，因此不能把它写成正向支持证据。
3. CRLB / information-bound 层是真正的理论增强，能支撑“pilot channel carries finite Fisher information”这一有边界的表述。
4. 实验部分当前只能写成可执行方案，不能写成已完成验证。

### 审稿判断
- 本轮提升了理论说服力，但没有显著提升 ML 说服力。
- 项目仍不具备投稿条件。

### 接收概率变化依据
- 因理论层变强、实验路径更清楚，接收概率谨慎上调到 `16%–20%`；但由于 ML baseline 没有正向结果，上调幅度必须克制。

## Scope Adjustment Note

### 审稿判断
- 在用户明确限定为纯理论与仿真研究后，实验缺失不再作为当前回合的直接执行缺口。
- 但如果目标期刊最终对实验支撑高度敏感，这仍可能在后期变成期刊匹配风险，而不是当前执行风险。
