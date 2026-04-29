# 项目状态：self-calibrating-diffractive-ncomms

## 项目基本信息
- 项目名称：Self-calibrating diffractive optical neural operators for imaging through dynamic aberrations
- 目标期刊：Nature Communications
- 最近更新时间：2026-04-29（environment-bringup）

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
- 机制示意图可用 AI 起草，但正式结果图必须来自真实计算或真实实验数据
- 未完成真实运行的代码、结果图和 benchmark 不得记为已完成

## 研究总目标
围绕“固定被动衍射处理器如何在动态像差/弱散射环境中通过共路 reference 实现自校准成像恢复”建立一条可投稿到 Nature Communications 的完整证据链，最终形成：
- 主体理论：共路 pilot 如何降低瞬时退化不确定性，以及该机制在 diffractive optical neural operator 中的成立条件、边界和失效模式
- 真实可复现的仿真链：至少覆盖 Zernike 动态像差、Kolmogorov 湍流、薄相位屏散射三类退化
- 关键对照：ordinary D2NN、pilot-assisted D2NN、非共路 reference、错误 reference、传统 Wiener / RL / blind deconvolution、电子 U-Net、理想 phase-conjugation 上限
- 正文与补充材料全套投稿级图表
- 30 篇以上已核对参考文献

## 当前阶段
环境配置与数据补全优先阶段。

说明：
- round1-round4 的 surrogate、wave-optics、information-bound 和 cross-task 证据已建立。
- round5 / round5b 已有第一轮器件级 prototype 结果，但强度不足以封闭主结论。
- strict manuscript 已形成，但 Figure 5 仍然不够强。
- 当前活动工作区缺少 round1-round5b 的底层脚本与输出文件，因此本轮先把“可持续运行环境 + 数据补全链路”补稳。

## 当前唯一主瓶颈
当前唯一主瓶颈是：Figure 5 相关数据补全缺少稳定可复跑环境与连续证据链。

原因：
- 当前已有 round5 / round5b 的第一轮弱原型结果，但 common-path 优势过弱。
- 活动工作区缺少底层 round1-round5b 文件，限制了立即复跑和连续补数据。
- 网络代理限制使 `matplotlib`、`scipy`、`torch` 无法在线安装，因此不能把重依赖环境当作默认可用条件。

## 本轮唯一最高优先级
配置可持续运行环境，以运行代码并补全数据；这是当前最高优先级。

## 当前已验证结果
- round1：Gaussian surrogate 上 common-path pilot 相比 no-reference 有明确增益
- round2：Zernike wave-optics PSF 模型上，OOD 集 common-path 平均 PSNR `38.422 dB`，高于 no-reference `37.069 dB` 与 non-common-path `37.078 dB`
- round3：最小 FNO-style baseline 为中性偏负；CRLB / information-bound 已建立
- round4：cross-task surrogate 上 reconstruction、classification residual、inverse-design surrogate 出现第一轮正向信号
- round5：两层 pure-reconstruction D2NN 为中性偏负；common-path 相比 ordinary `-0.191 dB`
- round5b：三层 self-calibrating D2NN 给出第一轮弱正向 reconstruction 信号；OOD 下 common-path object-zone PSNR `11.559 dB`，ordinary `11.356 dB`，non-common-path `11.505 dB`，wrong-reference `11.350 dB`

## 当前环境状态
- 可用：
  - Python 3.12
  - `numpy 2.3.5`
  - `Pillow 12.2.0`
  - 本地文件写入、JSON 输出、PNG 输出
- 不可用：
  - `matplotlib`
  - `scipy`
  - `torch` / `torchvision`
- 已验证：
  - `/workspace/self-calibrating-diffractive-ncomms/` 工作目录已建立
  - `scripts/outputs/logs` 子目录已建立
  - `environment_smoke_test.py` 已真实运行
  - `environment_smoke_test.md/json/png` 已落盘
- 当前判断：
  - 现阶段应采用 `numpy + Pillow` 路线继续补数据

## 本轮交付物
- `manuscript-v1-strict.md`
- `review-round-manuscript-v1-strict.md`
- `iteration-log.md`
- `iteration-round-2026-04-29.md`
- `/workspace/self-calibrating-diffractive-ncomms/scripts/environment_smoke_test.py`
- `/workspace/self-calibrating-diffractive-ncomms/scripts/minimal_passive_d2nn_protocol.md`
- `/workspace/self-calibrating-diffractive-ncomms/outputs/environment_smoke_test.md`
- `/workspace/self-calibrating-diffractive-ncomms/outputs/environment_smoke_test.json`
- `/workspace/self-calibrating-diffractive-ncomms/outputs/environment_smoke_test.png`

## 下一轮立即动作
1. 以 `numpy + Pillow` 恢复或补出 round5 / round5b 的最小可复跑脚本与数据输出链
2. 保留“共路、非共路、错误 reference”三组关键对照
3. 继续增强 Figure 5，优先补真实运行数据而不是等待外部依赖
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
- 综合接收概率：24%–30%
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
- 2026-04-29：根据用户新指令，将“配置运行环境、运行代码、补全数据”设为当前最高优先级，并完成本地环境打通
