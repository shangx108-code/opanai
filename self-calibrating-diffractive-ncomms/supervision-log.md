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
