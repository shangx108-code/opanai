# 监督记录：self-calibrating-diffractive-ncomms

## 2026-04-26 Round 1
- 已确认：Gaussian surrogate 最小机制验证已真实运行并落盘
- 结论：只支持继续推进，不支持正式成稿

## 2026-04-26 Round 2
- 已确认：wave-optics pupil 模型已真实运行，common-path 仍优于 no-reference 与 non-common-path
- 结论：进入更接近器件级主张的阶段，但仍缺真正 processor-level 对照

## 2026-04-26 Round 3
- 已确认：FNO-style baseline 与 CRLB 已真实运行
- 问题：最小 FNO-style baseline 没有显示 common-path 优势
- 结论：理论增强成立，但 ML 说服力未闭环

## 2026-04-27 Round 4
- 已确认：tight bound / theorem 与 cross-task 泛化已真实运行
- 结论：理论与任务级叙事增强，但器件级主证据仍缺失

## 2026-04-27 Writing Launch
- 已确认：四段式引言、主文结构、figure-to-text 映射、30+ reference ledger 已建立
- 结论：写作骨架已成，但不等于稿件成熟

## 2026-04-27 Round 5 / 5b
- 已确认：
  - round5 两层 pure-reconstruction D2NN 已真实运行
  - round5b 三层 self-calibrating D2NN 已真实运行
  - Figure 5 已从空占位变成第一轮真实原型
- 问题：
  - round5 为中性偏负
  - round5b 的 common-path 增益过弱
  - coefficient readout MAE 未优于 ordinary
- 结论：当前已从“缺失 processor-level 结果”进入“已有弱原型，但仍不足以封闭主文结论”的阶段

## 2026-04-27 Strict Manuscript Mode
- 已确认：
  - `manuscript-v1-strict.md` 已建立
  - 引言保持为经典四段式
  - 主文保持为 Methods / Results / Discussion / Summary
  - Figure 1-5 已在正文中被明确引用
- 新风险：
  - 当前工作区缺少项目状态中记录的 round1-round5b 底层脚本与结果文件
- 结论：严格主文已成形，但主结果和可复跑证据链都未封闭

## 2026-04-27 Iteration Stop
- 已确认：用户要求停止自动迭代
- 结论：之后仅保留手动推进，直到新指令恢复

## 2026-04-29 Iteration Resume
- 已确认：用户要求重新进入研究迭代并强化运行
- 已确认：`iteration-log.md` 与 `iteration-round-2026-04-29.md` 已建立
- 结论：恢复的是强化研究迭代模式，不是主证据闭环

## 2026-04-29 Environment Bring-up
- 已确认：
  - 用户把“配置运行环境、运行代码、补全数据”提升为当前最高优先级
  - `/workspace/self-calibrating-diffractive-ncomms/` 工作目录已建立
  - `scripts/outputs/logs` 子目录已建立
  - `environment_smoke_test.py` 已真实运行
  - `numpy + Pillow` 复数 FFT、JSON 输出、PNG 输出链路可用
- 当前问题：
  - 在线安装 `matplotlib`、`scipy`、`torch` 失败，原因是网络代理限制
  - 活动工作区仍缺少 round1-round5b 底层脚本与输出文件
- 结论：
  - 当前环境已足以支持最小 NumPy 路线继续补数据
  - 当前环境仍不足以直接展开依赖 `torch/scipy/matplotlib` 的更重训练路线

## 2026-04-29 Round 6 NumPy Rebuild
- 已确认：
  - `round6_numpy_passive_d2nn.py` 已真实运行
  - `metrics.csv`、`summary.md/json`、`panel.png`、`training_history.json` 已落盘
  - 当前活动工作区已重新具备最小器件级对照的数据生成能力
- 当前问题：
  - common-path OOD mean PSNR `10.754 dB`，低于 ordinary `11.884 dB`
  - common-path 仅略高于 non-common-path `+0.063 dB`
- 结论：
  - 本轮完成的是“可复跑基线恢复”，不是“主结果增强”
  - 当前结果不能被包装成 common-path 的正向器件级证据

## 2026-04-29 Round 7 Parameter Scan
- 已确认：
  - `round7_parameter_scan.py` 已真实运行
  - `45` 组配置已完成扫描
  - 详细表、汇总表、top10、heatmap、最佳配置面板和训练历史均已落盘
- 当前问题：
  - ranking 最优配置虽然达到 `common minus ordinary = +0.630 dB`，但 `common minus wrong-reference = -0.020 dB`
  - 说明当前 common-path 的优势还没有稳到足以排除“reference 本身形状偏置”的疑问
- 结论：
  - round7 是实质性前进，因为它把 round6 的负向单点结果推进到了正向配置区间
  - 但当前仍不能把 Figure 5 视为已经封闭

## 2026-04-29 Theory Packaging And Cross-domain Demonstration
- 已确认：
  - `manuscript-v1-strict.md` 已补入 neural-operator formalism 与 local task-map 表述
  - Figure 4 的正文角色已明确升级为 cross-domain demonstration
  - `neural-operator-formalism-note.md` 已建立
  - `cross_domain_demonstration_summary.csv` 已生成
  - Supplementary PDF 已更新以承接理论 formalism 与 cross-domain 表格
- 当前问题：
  - 这轮增强的是理论表达与论文打包，不是新增数值证据
  - Figure 5 的器件级强度瓶颈仍未解除
- 结论：
  - 当前稿件的理论桥和 Figure 4 说服力已明显增强
  - 但投稿成败的单一主瓶颈仍然是 processor-level robustness，而不是理论措辞

## 2026-04-29 Round 8 Narrow Processor Scan
- 已确认：
  - `round8_narrow_processor_scan.py` 已真实运行
  - 已完成 `60` 组局部配置、每组 `4` 次重复的局部 processor-level 扫描
  - 详细表、重复表、汇总表、top10、热图、最佳配置面板和训练历史均已落盘
- 当前问题：
  - 最优稳健配置虽然把 `common minus ordinary` 均值推进到 `+0.438 dB`，且最差重复仍保持 `+0.390 dB`
  - 但同一配置下 `common minus wrong-reference` 均值仅 `+0.062 dB`，最差重复仍降到 `-0.307 dB`
  - 全部 `60` 组局部配置中，只有 `2` 组同时满足 `common minus ordinary > 0` 与 `common minus wrong-reference > 0`
- 结论：
  - round8 是实质性前进，因为它把 round7 的单点正向窗口推进成了对 ordinary 更稳的局部配置带
  - 但 Figure 5 的单一主瓶颈没有被解除：对 wrong-reference 的分离仍然不够稳，当前还不能把 common-path 解释为清晰可靠的自校准读出

## 2026-04-29 Round 9 Wrong-reference Targeted Scan
- 已确认：
  - `round9_wrong_reference_targeted_scan.py` 已真实运行
  - 已完成 `30` 组 targeted wrong-reference 配置、每组 `4` 次重复
  - 详细表、重复表、汇总表、top10、热图、最佳面板和训练历史均已落盘
- 当前问题：
  - 当前最优排他性配置虽然已经把 `common minus wrong-reference` 稳定推到正值，但幅度仍然偏小，仅 `+0.141 dB`
  - 这仍不足以直接宣称“自校准读出已经强而稳健”
- 结论：
  - round9 是关键性前进，因为首次得到一个对 ordinary、non-common-path、wrong-reference 三者都保持正向排他的局部配置
  - Figure 5 的论证地位已明显增强，可以从“只有 ordinary 优势”升级为“出现了初步稳定的 wrong-reference 排他性窗口”，但仍需下一轮确认这个窗口不是脆弱偶然点

## 2026-04-29 Round 10 Anti-phase Confirmation Scan
- 已确认：
  - `round10_antiphase_confirmation_scan.py` 已真实运行
  - 已锁定 `wrongref_mode=anti_phase`
  - 已完成 `phase_mix=0.18-0.22` 的 `9` 点超窄扫描、每点 `10` 次重复
- 当前问题：
  - 在更高重复数下，没有任何一个 `phase_mix` 点同时满足 `common minus ordinary` 与 `common minus wrong-reference` 的最差重复都为正
  - 最佳确认点 `phase_mix=0.18` 的 `common minus wrong-reference` 均值仅 `+0.067 dB`，最差重复回落到 `-0.103 dB`
- 结论：
  - round10 对 round9 的窗口做了必要的高重复验伪
  - 当前最稳结论应回退为：common-path 相对 ordinary 的优势已有稳定窗口，但相对 wrong-reference 的排他性仍未被高重复确认
  - 因此 Figure 5 还不能升级为“稳定排他性已成立”
