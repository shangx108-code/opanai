# 研究迭代日志：self-calibrating-diffractive-ncomms

## 2026-04-29 Iteration Resume
- 当前阶段：恢复强化研究迭代模式
- 当前唯一主瓶颈：缺少 ordinary D2NN vs pilot-assisted D2NN 的真实器件级最小对照
- 本轮最高优先级：恢复可追踪执行，而不是假装自动链已经稳定
- 本轮交付物：
  - `iteration-log.md`
  - `iteration-round-2026-04-29.md`
  - 更新后的 `project-state.md`
  - 更新后的 `role-assignments.md`
  - 更新后的 `supervision-log.md`

## 2026-04-29 Environment Bring-up
- 当前阶段：环境配置与数据补全优先
- 当前唯一主瓶颈：Figure 5 缺少稳定可复跑环境与连续证据链
- 本轮真实结果：
  - 已建立 `/workspace/self-calibrating-diffractive-ncomms/`
  - 已确认 `numpy + Pillow` 可用
  - 已确认在线安装重依赖不可作为默认路径
- 当前判断：
  - 当前默认路线应为 `numpy + Pillow`

## 2026-04-29 09:11 CST Round 6 Stable NumPy Chain
- 当前阶段：最小 runnable chain 稳定后进入 Figure 5 局部增强
- 当前唯一主瓶颈：common-path 仍未形成相对 ordinary 的稳健 processor-level 优势
- 本轮唯一最高优先级：先把最小可运行链真正落盘，再用真实数据查清 Figure 5 是否存在局部正窗口
- 本轮真实完成：
  - 新增并运行 `scripts/environment_smoke_test.py`
  - 新增并运行 `scripts/round6_numpy_passive_d2nn.py`
  - 新增 `scripts/minimal_passive_d2nn_protocol.md`
  - 生成 `environment_smoke_test.md/json/png`
  - 生成 `round6_numpy_passive_d2nn_metrics.csv`
  - 生成 `round6_numpy_passive_d2nn_summary.md/json`
  - 生成 `round6_numpy_passive_d2nn_panel.png`
  - 生成 `round6_numpy_passive_d2nn_training_history.json`
- 本轮关键结果：
  - 环境 readiness 已解决；当前稳定链路为 `numpy 2.3.5 + Pillow 12.2.0`
  - best ordinary OOD mean PSNR：`20.421 dB`
  - best common-path OOD mean PSNR：`20.421 dB`，与 best ordinary 近似持平，差值 `+0.000116 dB`
  - best non-common-path OOD mean PSNR：`20.473 dB`
  - best wrong-reference OOD mean PSNR：`20.382 dB`
  - matched 配置下的最佳 common-path minus non-common-path 为 `+0.214 dB`，出现在 4 layers、pilot amplitude `0.25`
- 当前判断：
  - 本轮真正完成的是“最小可复跑链稳定 + Figure 5 局部窗口识别”
  - 当前仍不能把 Figure 5 写成 common-path 稳健优于 ordinary 的器件级主证据
- 下一轮立即动作：
  1. 围绕低 pilot 幅度和少量层数做更窄的 matched 局部扫描
  2. 检查能否把“近似持平 ordinary”推进到“稳定优于 ordinary”
  3. 若不能，则进一步收紧 Figure 5 的正文表述
