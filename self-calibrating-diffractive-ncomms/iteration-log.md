# 研究迭代日志：self-calibrating-diffractive-ncomms

## 2026-04-29 Iteration Resume

- 当前阶段：恢复研究迭代模式
- 当前唯一主瓶颈：缺少 ordinary D2NN vs pilot-assisted D2NN 的真实被动衍射处理器最小阳性对照
- 本轮唯一最高优先级：进入器件级最小对照构建前的强化运行状态，要求后续每轮必须留下可检查日志
- 当前判断：
  - 已有 round1-round4 与 writing-launch 的项目记录
  - 当前没有独立运行日志来证明自动迭代持续执行
  - 因此本轮先补齐“强化运行”的可追踪性，而不是假装自动系统已经稳定闭环
- 本轮交付物：
  - `iteration-log.md`
  - `iteration-round-2026-04-29.md`
  - 更新后的 `project-state.md`
  - 更新后的 `role-assignments.md`
  - 更新后的 `supervision-log.md`
- 下一轮立即动作：
  1. 直接进入 ordinary D2NN vs pilot-assisted D2NN 的最小 NumPy 可运行对照脚本设计
  2. 产出统一协议、控制组、指标与预期落盘文件清单
  3. 每轮结束强制写入本日志，不再允许“只更新状态、不留迭代痕迹”

## 2026-04-29 Environment Bring-up

- 当前阶段：环境配置与数据补全优先
- 当前唯一主瓶颈：Figure 5 相关数据补全缺少稳定可复跑环境与连续证据链
- 本轮唯一最高优先级：打通最小本地运行链，而不是等待网络安装恢复
- 本轮真实结果：
  - 已创建 `/workspace/self-calibrating-diffractive-ncomms/` 工作目录
  - 已确认在线安装 `matplotlib/scipy/torch` 失败，原因为代理受限
  - 已确认当前可用执行链为 `numpy + Pillow`
- 当前可用环境：
  - `numpy 2.3.5`
  - `Pillow 12.2.0`
- 下一轮立即动作：
  1. 以 `numpy + Pillow` 实现或恢复最小 passive D2NN 对照脚本
  2. 优先补真实运行数据，不再等待外部依赖
  3. 按每小时一轮更新本日志

<<<<<<< Updated upstream
## 2026-04-29 Scheduled Execution

- 当前阶段：活动工作区 processor-level 链路恢复与弱结果复核
- 当前唯一主瓶颈：Figure 5 的器件级 common-path 优势仍弱，且活动工作区此前缺少可直接运行的底层脚本
- 本轮唯一最高优先级：先恢复一条真实可运行的 processor-level 对照链，并用最小 seed / pilot-amplitude 扫描判断它是否已经出现稳健窗口
- 本轮真实完成：
  - 新增并运行 `/workspace/self-calibrating-diffractive-ncomms/round5c_passive_processor_seed_pilot_scan.py`
  - 生成 `detail.csv`、`summary.csv`、`summary.json`、`summary.md` 与 `panel.png`
  - 清理了 `project-state.md` 中遗留的冲突标记
- 本轮关键结果：
  - 当前 rebuilt 后继链已经恢复了活动工作区的 processor-level 可跑性
  - 最佳 pilot 窗口出现在 `pilot_amplitude = 0.35`
  - 但该窗口下 common-path 相比 ordinary 仅 `+0.061 dB`，相对 non-common-path 仍为 `-0.046 dB`
  - common-path 仅在 `8/20` 个 seed-amplitude 组合中优于 ordinary，说明稳健性仍不足
- 当前判断：
  - 本轮完成的是“恢复可跑链 + 给出诚实弱结果”，不是“把 Figure 5 变强”
  - 下一轮必须继续围绕最窄窗口做局部扫描，而不是扩展新主线
=======
## 2026-04-29 Round 6 NumPy Rebuild

- 当前阶段：最小可复跑数据链恢复
- 当前唯一主瓶颈：器件级 common-path 优势仍未形成稳健正信号
- 本轮唯一最高优先级：在当前 `numpy + Pillow` 环境下恢复最小 ordinary / common-path / non-common-path / wrong-reference 对照
- 本轮真实结果：
  - 已新增 `round6_numpy_passive_d2nn.py`
  - 已真实运行并输出 `metrics.csv`、`summary.md/json`、`panel.png`、`training_history.json`
  - ordinary OOD mean PSNR：`11.884 dB`
  - common-path OOD mean PSNR：`10.754 dB`
  - non-common-path OOD mean PSNR：`10.690 dB`
  - wrong-reference OOD mean PSNR：`10.831 dB`
  - common minus ordinary：`-1.131 dB`
  - common minus non-common-path：`+0.063 dB`
- 当前判断：
  - 最小 NumPy 数据补全链已经恢复成功
  - 但这轮结果不支持把 common-path 写成优于 ordinary 的器件级主证据
- 下一轮立即动作：
  1. 保留本轮脚本与数据链作为可复跑基线
  2. 调整 reference 权重、层数或任务定义，再做小范围稳健性扫描
  3. 继续按每小时一轮记录，不把本轮负结果包装成正向亮点
>>>>>>> Stashed changes
