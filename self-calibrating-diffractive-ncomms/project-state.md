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

说明：
- round1-round4 的机制、wave-optics、information-bound 和 cross-task 证据已建立。
- round5 / round5b 已给出第一轮器件级弱原型，但不足以封闭主文结论。
- 本轮在当前活动工作区真正恢复了 `numpy + Pillow` 的最小可运行环境、脚本和输出链。
- 本轮恢复的是“可持续补数据能力 + Figure 5 局部窗口识别”，不是“器件级主结果已经闭环”。

## 当前唯一主瓶颈
当前唯一主瓶颈是：Figure 5 仍缺少对 ordinary D2NN 的稳健、可重复、幅度足够的 common-path 优势。

原因：
- 当前最强的器件级结果只达到“局部 matched non-common-path 优势”和“对 ordinary 的近似持平”，还没有形成明确领先。
- 现有 processor-level 信号仍对 pilot 幅度、层数和训练搜索细节敏感。
- 这意味着 Figure 5 还不能承担 Nature Communications 主结果图的角色，只能作为边界型证据。

## 当前已验证结果
- round1：Gaussian surrogate 上 common-path pilot 相比 no-reference 与 non-common-path 有明确增益。[verified]
- round2：Zernike wave-optics 模型上，OOD 集 common-path 平均 PSNR `38.422 dB`，高于 no-reference `37.069 dB` 与 non-common-path `37.078 dB`。[verified]
- round3：最小 FNO-style baseline 为中性偏负；CRLB / information-bound 已建立。[verified]
- round4：cross-task surrogate 上 reconstruction、classification residual、inverse-design surrogate 出现第一轮正向信号。[verified/partially verified]
- round5：两层 pure-reconstruction D2NN 为中性偏负；common-path 相比 ordinary `-0.191 dB`。[verified]
- round5b：三层 self-calibrating D2NN 给出第一轮弱正向 reconstruction 信号；OOD 下 common-path `11.559 dB`，ordinary `11.356 dB`，non-common-path `11.505 dB`，wrong-reference `11.350 dB`。[partially verified]
- round6：当前活动工作区的最小 NumPy pipeline 已真实运行。
  - best ordinary OOD mean PSNR：`20.421 dB`（3 layers）
  - best common-path OOD mean PSNR：`20.421 dB`（2 layers, pilot amplitude `0.05`），与 best ordinary 近似持平，差值仅 `+0.000116 dB`
  - best non-common-path OOD mean PSNR：`20.473 dB`
  - best wrong-reference OOD mean PSNR：`20.382 dB`
  - 在 matched 配置下，最佳 common-path 相比 matched non-common-path 的局部优势为 `+0.214 dB`，出现在 4 layers、pilot amplitude `0.25`
  - 当前不能据此声称 common-path 已稳健优于 ordinary。[partially verified]

## 当前环境状态
- 可用：
  - Python 3.12
  - `numpy 2.3.5`
  - `Pillow 12.2.0`
  - 本地文件写入、JSON 输出、PNG 输出
  - 最小 passive D2NN 对照脚本真实运行与结果落盘
- 不可用或未验证：
  - `matplotlib`
  - `scipy`
  - `torch` / `torchvision`
- 当前判断：
  - 现阶段默认沿 `numpy + Pillow` 路线继续补 Figure 5 数据
  - 不等待重依赖环境恢复后再推进

## 本轮交付物
- `/workspace/self-calibrating-diffractive-ncomms/scripts/environment_smoke_test.py`
- `/workspace/self-calibrating-diffractive-ncomms/scripts/minimal_passive_d2nn_protocol.md`
- `/workspace/self-calibrating-diffractive-ncomms/scripts/round6_numpy_passive_d2nn.py`
- `/workspace/self-calibrating-diffractive-ncomms/outputs/environment_smoke_test.md`
- `/workspace/self-calibrating-diffractive-ncomms/outputs/environment_smoke_test.json`
- `/workspace/self-calibrating-diffractive-ncomms/outputs/environment_smoke_test.png`
- `/workspace/self-calibrating-diffractive-ncomms/outputs/round6_numpy_passive_d2nn_metrics.csv`
- `/workspace/self-calibrating-diffractive-ncomms/outputs/round6_numpy_passive_d2nn_summary.md`
- `/workspace/self-calibrating-diffractive-ncomms/outputs/round6_numpy_passive_d2nn_summary.json`
- `/workspace/self-calibrating-diffractive-ncomms/outputs/round6_numpy_passive_d2nn_panel.png`
- `/workspace/self-calibrating-diffractive-ncomms/outputs/round6_numpy_passive_d2nn_training_history.json`

## 当前稳定判断
- 环境 readiness 已从阻塞项降为已解决项。[corrected]
- Figure 5 的当前状态应表述为：
  - “最小 NumPy processor-level pipeline 已恢复并可复跑”
  - “common-path 在局部 matched 配置下可优于 non-common-path”
  - “但对 ordinary 仍未建立稳健、清晰、可推广的优势”

## 下一轮唯一动作
围绕低 pilot 幅度和少量层数的 matched 配置继续做最小局部扫描，目标不是再恢复环境，而是把 common-path 相对 ordinary 的优势从“近似持平 / 局部弱信号”推进到“稳定正信号”；若做不到，就继续收紧 Figure 5 的论文角色。
