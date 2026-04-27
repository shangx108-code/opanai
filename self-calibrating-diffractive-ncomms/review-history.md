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

## Round 4 内部严格审稿

### 检查范围
- tighter theorem 与 cross-task 泛化是否真正增强说服力

### 主要意见
1. round4 的 tight bound note 比 round3 的纯 CRLB 说明更接近正文可用理论，因为它把 state estimation covariance 与 downstream task loss 连接起来了。
2. cross-task 结果是正向的，但强度不均匀：reconstruction 明显最强，classification residual 次之，inverse-design surrogate 目前只是小幅改善。
3. 当前 prototype-based classification accuracy 已饱和，因此应当优先引用 residual / score-level量，而不是只盯准确率。
4. round4 仍不能替代最关键的器件级 ordinary vs pilot-assisted 对照。

### 审稿判断
- 项目说服力有实质提升，但仍未达到可投稿状态。

### 接收概率变化依据
- 因理论层从 estimation-bound 提升到 task-level theorem，且 cross-task 结果出现第一轮正向信号，接收概率谨慎上调到 `20%–25%`。

## Writing Launch 内部严格审稿

### 检查范围
- 严格写作流程是否真实启动
- 新的写作工作是否保持了证据边界

### 主要意见
1. 启动四段式引言和主文骨架是必要前进，因为它把后续结果、图和引用的接口固定下来了。
2. 这一步的价值在于减少后续返工，而不是提升主结果强度。
3. 当前稿件仍不能越过 passive diffractive processor 核心对照的缺口。
4. reference ledger 已超过 30 条，但仍需在成稿前做一轮最终核查，尤其是部分 2026 年条目。

### 审稿判断
- 该步骤是真正推进，但属于“写作系统搭建”，不是“主证据闭环”。
- 项目仍不具备投稿条件。

### 接收概率变化依据
- 因写作结构、图文映射和引用链得到规范化，稿件执行效率会提高，但主证据没有新增，因此综合接收概率暂维持 `20%–25%`。

## Round 5 / 5b 内部严格审稿

### 检查范围
- ordinary D2NN vs pilot-assisted D2NN 的最小 phase-only 器件级对照是否已真实运行
- Figure 5 是否已经从占位项变成真实可审查结果
- 新结果是否足以显著提升投稿成熟度

### 主要意见
1. round5 的两层 pure-reconstruction D2NN 给出的是中性偏负结果：common-path 相比 ordinary 为 `-0.191 dB`，说明“把 pilot 加进输入”本身不会自动形成器件级优势。
2. round5b 升级为带 calibration readout 区的三层 self-calibrating D2NN 后，processor-level OOD reconstruction 出现第一轮弱正向信号：common-path 相比 ordinary 为 `+0.204 dB`，相对 wrong-reference 为 `+0.209 dB`。
3. 但相对 non-common-path 仅 `+0.054 dB`，而 coefficient readout MAE 反而没有优于 ordinary，因此“自校准已被器件级清晰读出”仍不能成立。
4. Figure 5 已经不再缺失，但它现在只能作为“第一轮弱原型”，不能承担 Nature Communications 主文 pivot。

### 审稿判断
- 项目有真实推进，因为最核心缺口已从“无结果”变为“有弱结果”。
- 但项目仍不具备投稿条件。

### 五审稿人接收概率
- Reviewer A（机制与理论链）: `31%`
- Reviewer B（器件级证据）: `22%`
- Reviewer C（计算成像与基线）: `24%`
- Reviewer D（图文与叙事完整性）: `29%`
- Reviewer E（期刊门槛与总体成熟度）: `21%`

### 接收概率变化依据
- 由于 Figure 5 已有第一轮真实 prototype，综合接收概率可谨慎上调到 `24%–30%`。
- 但所有五位审稿人的接收概率都远未超过 `80%`，停止条件明确未满足。
