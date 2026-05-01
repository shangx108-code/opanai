# 项目状态：self-calibrating-diffractive-ncomms

## 项目基本信息
- 项目名称：Self-calibrating diffractive optical neural operators for imaging through dynamic aberrations
- 目标期刊：Nature Communications
- 最近更新时间：2026-04-29（round6-stable-numpy-chain）
- 当前活动资料来源：
  - `/workspace/memory/self-calibrating-diffractive-ncomms/manuscript-v1-strict.md`
  - `/workspace/memory/self-calibrating-diffractive-ncomms/review-round-manuscript-v1-strict.md`
  - `/workspace/self-calibrating-diffractive-ncomms/scripts/environment_smoke_test.py`
  - `/workspace/self-calibrating-diffractive-ncomms/scripts/minimal_passive_d2nn_protocol.md`
  - `/workspace/self-calibrating-diffractive-ncomms/scripts/round6_numpy_passive_d2nn.py`
  - `/workspace/self-calibrating-diffractive-ncomms/outputs/environment_smoke_test.md`
  - `/workspace/self-calibrating-diffractive-ncomms/outputs/round6_numpy_passive_d2nn_summary.md`
  - `/workspace/self-calibrating-diffractive-ncomms/outputs/round6_numpy_passive_d2nn_summary.json`

## 当前运行规则
- 默认推进主体：强化研究迭代模式
- 当前主线优先级：
  1. 保持最小可运行代码链稳定
  2. 用真实运行结果继续增强 Figure 5
  3. 维持主文证据边界，不把局部窗口包装成稳健主结论
- 当前项目按纯理论与纯仿真路线推进
- 除示意图外，正式图必须来自真实计算或真实实验数据
- 只要本轮有真实推进，必须更新项目记忆与 `iteration-log.md`

## 当前阶段
最小可复跑链稳定后的 Figure 5 局部增强阶段。

## 当前唯一主瓶颈
当前唯一主瓶颈是：Figure 5 仍缺少对 ordinary D2NN 的稳健、可重复、幅度足够的 common-path 优势。

## 当前已验证结果
- round1：Gaussian surrogate 上 common-path pilot 相比 no-reference 与 non-common-path 有明确增益。[verified]
- round2：Zernike wave-optics 模型上，OOD 集 common-path 平均 PSNR `38.422 dB`，高于 no-reference `37.069 dB` 与 non-common-path `37.078 dB`。[verified]
- round3：最小 FNO-style baseline 为中性偏负；CRLB / information-bound 已建立。[verified]
- round4：cross-task surrogate 上 reconstruction、classification residual、inverse-design surrogate 出现第一轮正向信号。[verified/partially verified]
- round5：两层 pure-reconstruction D2NN 为中性偏负；common-path 相比 ordinary `-0.191 dB`。[verified]
- round5b：三层 self-calibrating D2NN 给出第一轮弱正向 reconstruction 信号；OOD 下 common-path `11.559 dB`，ordinary `11.356 dB`，non-common-path `11.505 dB`，wrong-reference `11.350 dB`。[partially verified]
- round6：当前活动工作区的最小 NumPy pipeline 已真实运行。
  - best ordinary OOD mean PSNR：`20.421 dB`
  - best common-path OOD mean PSNR：`20.421 dB`
  - best non-common-path OOD mean PSNR：`20.473 dB`
  - best wrong-reference OOD mean PSNR：`20.382 dB`
  - 在 matched 配置下，最佳 common-path 相比 matched non-common-path 的局部优势为 `+0.214 dB`

## 2026-05-01 manuscript-package update
- 已把严格边界版主稿重构为 Nature Communications 风格 LaTeX 主稿与独立 Supplementary Information。
- 引言保持严格四段式。
- Figure 1 已生成示意图；Figures 2-4 仅由已有账本数值渲染为数据图。
- 主稿与附录均已真实编译成 PDF。
- 当前包是“submission-style manuscript package”，不是“full raw archive restored”。
