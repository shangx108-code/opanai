# 项目状态：self-calibrating-diffractive-ncomms

## 项目基本信息
- 项目名称：Self-calibrating diffractive optical neural operators for imaging through dynamic aberrations
- 目标期刊：Nature Communications
- 最近更新时间：2026-04-26（round2）
- 当前资料来源：
  - `/workspace/user_files/01-markdown-1-md-3`
  - `/workspace/self-calibrating-diffractive-ncomms/round1_theory_note.md`
  - `/workspace/self-calibrating-diffractive-ncomms/outputs/round1_summary.md`
  - `/workspace/self-calibrating-diffractive-ncomms/round2_theory_note.md`
  - `/workspace/self-calibrating-diffractive-ncomms/outputs/round2_summary.md`

## 当前运行规则
- 默认推进主体：自研智能体
- 自动迭代频率：每 2 小时 1 轮
- 停止条件必须同时满足：
  - 保守五审稿人接收概率均超过 70%
  - 所有需要补的 evidence 全部补齐
  - 所有正式数据图都基于真实数据
  - 理论推导详实、可靠、可检查
  - 正文与补充材料所需图表、引用和对照组全部补齐
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
- 关键对照：ordinary D2NN、pilot-assisted D2NN、非共路 reference、错误 reference、传统 Wiener / RL / blind deconvolution、电子 U-Net、理想 phase-conjugation 上限
- 正文与补充材料全套投稿级图表
- 30 篇以上已核对参考文献
- 可归档的代码、数据、图表、正文、补充材料与最终投稿包

## 当前阶段
结果生成阶段（最小 wave-optics 证据恢复子阶段）。

说明：
- 当前工作区之前没有该项目的既有命名空间记忆。
- 本轮已把上传提案正式转入项目状态，并完成第一轮最小真实数值验证。
- 现在已进一步完成 round2：真实运行基于 Zernike pupil 的 wave-optics PSF 最小证据链。
- 当前仍不是完整 D2NN，也不是投稿级证据链。

## 当前唯一主瓶颈
当前唯一主瓶颈是：还没有在同一动态像差协议下建立“真实被动衍射处理器”层面的 ordinary D2NN 与 pilot-assisted D2NN 最小阳性对照证据。

原因：
- 目前已证明“共路 pilot 降低动态退化不确定性”的最小机制，在 Gaussian surrogate 与 Zernike wave-optics PSF 两层模型上都成立。
- 但还没有证明固定被动衍射处理器在真实 coherent propagation 下也能保留这一优势。
- 若 ordinary D2NN vs pilot-assisted D2NN 在 OOD 动态退化上不能拉开可信差距，则论文主线需要重评。

## 本轮唯一最高优先级
先把更强 forward model 下的最小真实证据链跑通，再决定是否继续向被动衍射处理器训练栈扩展。

## 本轮交付物
1. round1 最小机制脚本：`/workspace/self-calibrating-diffractive-ncomms/round1_pilot_selfcalibration.py`
2. round1 理论说明：`/workspace/self-calibrating-diffractive-ncomms/round1_theory_note.md`
3. round2 wave-optics 脚本：`/workspace/self-calibrating-diffractive-ncomms/round2_zernike_waveoptics.py`
4. round2 理论说明：`/workspace/self-calibrating-diffractive-ncomms/round2_theory_note.md`
5. round2 指标表：`/workspace/self-calibrating-diffractive-ncomms/outputs/round2_metrics.csv`
6. round2 汇总 JSON：`/workspace/self-calibrating-diffractive-ncomms/outputs/round2_summary.json`
7. round2 汇总说明：`/workspace/self-calibrating-diffractive-ncomms/outputs/round2_summary.md`
8. round2 结果面板：`/workspace/self-calibrating-diffractive-ncomms/outputs/round2_zernike_waveoptics_panel.png`

## 本轮完成标准
- 已真实运行 round2 脚本并落盘结果文件
- 已把 stronger forward model 下“共路 vs 非共路 vs 无 reference”的差异写成可检查指标
- 已明确写出 round2 仍不是 D2NN 证据、仍不可包装成 submission-grade 结论

## 下一轮立即动作
1. 在当前工作区写出 ordinary D2NN 与 pilot-assisted D2NN 的最小可运行对照脚本。
2. 保留“共路、非共路、错误 reference”三组关键对照，不满足就及时止损。
3. 若最小被动衍射对照仍为阳性，再扩展到 turbulence / thin phase screen。
4. 之后才进入传统与电子 baselines、理论细化和图稿成型。

## 技术状态检查结论
- 已验证：
  - 上传提案已转为当前项目主线。
  - 最小数值证据链已真实运行并输出 CSV / JSON / Markdown / PNG。
  - OOD stronger-aberration 集上，共路 pilot 较无 reference 有明确增益。
  - Zernike defocus + astigmatism 的 wave-optics pupil forward model已真实运行。
  - 在 OOD stronger-aberration 集上，共路 pilot 相比无 reference 将平均 PSNR 从 `37.069 dB` 提升到 `38.422 dB`，非共路仅为 `37.078 dB`。
  - OOD 集上，共路 pilot 的 mean PSF MSE 为 `4.217e-06`，优于无 reference 的 `1.279e-05` 与非共路的 `1.155e-05`。
- 部分验证：
  - 共路 pilot 降低动态退化不确定性的机制，在 Gaussian surrogate 与 Zernike wave-optics PSF 两层模型上成立。
- 未验证：
  - Zernike、湍流、薄相位屏三类真实波动光学退化。
  - ordinary D2NN 与 pilot-assisted D2NN 的真实对照。
  - 传统与电子 baselines。
  - 制造误差、量化误差、错位、波长漂移和 shot noise 鲁棒性。
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
  - 若下一轮采用 D2NN 训练，需要确认是否继续使用纯 NumPy 方案，或补齐更合适的训练环境
- 是否支持进入下一步程序运行、图片生成或论文编译：
  - 支持继续做小规模数值验证和 PNG 图生成
  - 尚不支持默认按深度学习训练链直接展开

## 稿件状态检查结论
- 已满足：
  - 题目主线、核心主张、关键对照框架已有第一版方向定义
  - 现在已有两轮真实证据，而不是只有选题草案
- 部分满足：
  - 摘要雏形和主图规划已有提案，但仍是前期构想，不可视为稿件实物
  - “共路 pilot 优于非共路 / 无 reference”的核心机制已有两轮真实数据支撑，但仍未到稿件主结果标准
- 未满足：
  - 正文、补充材料、正式图、图注、引用链、参考文献库均未形成投稿级实物
- 存在错误：
  - 若将当前 surrogate 结果直接包装为“固定被动衍射网络已实现自校准恢复”，会构成过度陈述
- 待核实：
  - 目标期刊最合适的故事边界，是否更偏 Nature Communications 还是更适合 Optica / Light 级别
- 是否支持进入下一阶段：
  - 只支持进入“最小被动衍射处理器对照”阶段，不支持进入正式成稿阶段

## 当前接收概率判断
- 综合接收概率：14%–18%

依据：
- 创新构想：中到强
- 最小机制信号：中到中强
- 理论充分性：弱
- 方法与代码可靠性：中
- 数据与结果完整性：弱
- 图表质量：弱
- 写作成熟度：弱

最拖累接收概率的短板：
1. 还没有真实被动衍射处理器 + 动态像差协议下的核心对照结果
2. 还没有三类退化与强对照 baselines
3. 还没有投稿级正文、补图与参考文献链

## 最近一次重要更新摘要
- 2026-04-26：基于上传提案初始化 `self-calibrating-diffractive-ncomms` 项目命名空间。
- 2026-04-26：完成 round1 最小机制验证，使用 shared-blur Gaussian pilot surrogate 检验共路 pilot 降低动态退化不确定性的基本方向是否成立。
- 2026-04-26：OOD stronger-aberration 集上，无 reference 平均 PSNR 为 `19.669 dB`，共路 pilot 为 `21.990 dB`，非共路 pilot 为 `20.268 dB`。
- 2026-04-26：完成 round2 wave-optics 最小证据链，使用 Zernike defocus + astigmatism pupil 生成真实 PSF；OOD 集上，无 reference 平均 PSNR 为 `37.069 dB`，共路 pilot 为 `38.422 dB`，非共路 pilot 为 `37.078 dB`，且共路 pilot 的 mean PSF MSE 最低。
