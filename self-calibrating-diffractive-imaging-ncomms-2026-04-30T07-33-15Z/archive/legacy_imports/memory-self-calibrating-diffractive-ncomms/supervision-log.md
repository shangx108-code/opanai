# 监督记录：self-calibrating-diffractive-ncomms

## 2026-04-26 Round 1
- 已确认：
  - 最小 Gaussian surrogate 已真实运行并落盘
  - common-path 高于 no-reference 与 non-common-path
- 当前问题：
  - 仍不是 D2NN 证据
  - 仍不能进入正式成稿

## 2026-04-26 Round 2
- 已确认：
  - Zernike wave-optics 脚本已真实运行
  - common-path OOD PSNR `38.422 dB`，高于 no-reference `37.069 dB` 与 non-common-path `37.078 dB`
- 当前问题：
  - coefficient error 未同步改善
  - 仍缺 processor-level 结果

## 2026-04-26 Round 3
- 已确认：
  - 最小 FNO-style baseline 与 CRLB 脚本已真实运行
- 当前问题：
  - ML baseline 为中性偏负
  - 不能把 round3 写成 ML 侧正向闭环

## 2026-04-27 Round 4
- 已确认：
  - task-level tight bound note 与 cross-task surrogate 已落盘
- 当前问题：
  - reconstruction 外的任务信号仍偏弱
  - 不能把 cross-task 结果扩写成普适器件级结论

## 2026-04-27 Round 5 / 5b
- 已确认：
  - 第一轮 processor-level prototype 已存在
  - round5 为中性偏负
  - round5b 为弱正向 reconstruction 信号
- 当前问题：
  - 与 ordinary、non-common-path 的差值太小
  - calibration readout 没有同步增强

## 2026-04-27 Strict Manuscript Mode
- 已确认：
  - 主文保持四段式 Introduction 与 Methods / Results / Discussion / Summary 结构
  - Figure 1-5 均有明确论证职责
- 当前问题：
  - Figure 5 仍然不足以承担主结果图职责

## 2026-04-29 Round 6 Stable NumPy Chain

### 当前检查范围
- 活动工作区是否已恢复最小可持续运行链
- Figure 5 是否在当前 NumPy-only 协议下出现新的可用局部窗口
- 是否存在把环境恢复误写成主结果增强的风险

### 已确认正确的部分
- `/workspace/self-calibrating-diffractive-ncomms/` 工作目录已建立并可写入。
- `environment_smoke_test.py` 已真实运行，证明 `numpy + Pillow` 的 FFT / JSON / PNG 链路可用。
- `round6_numpy_passive_d2nn.py` 已真实运行，并生成 metrics、summary、panel 与 training history。
- best common-path OOD mean PSNR 与 best ordinary 近似持平：`20.421 dB` vs `20.421 dB`，差值仅 `+0.000116 dB`。
- matched 配置下出现 `+0.214 dB` 的 common-path 相对 non-common-path 局部优势。

### 当前存在的问题或错误
- 当前 best non-common-path `20.473 dB` 仍高于 best common-path `20.421 dB`。
- common-path 对 ordinary 的优势仍未达到可称为稳健正结果的程度。
- 因此不能把本轮写成“Figure 5 已被增强到投稿级”。

### 对当前阶段真实状态的判断
- 环境 readiness 已从主阻塞项转为已解决项。
- Figure 5 已从“缺最小运行链”推进到“有真实可复跑基线和局部 matched common-path 窗口”。
- 但当前仍应把 Figure 5 记为边界型证据，而不是主结论闭环。

### 是否支持进入下一阶段
- 支持继续围绕低 pilot 幅度和少量层数做窄窗 matched 扫描。
- 不支持切换到更宽的新主线。
- 不支持升级稿件为 submission-ready。
