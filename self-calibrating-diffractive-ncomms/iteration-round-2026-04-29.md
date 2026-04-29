# 2026-04-29 研究迭代轮

## 当前阶段
- 从“已停止自动迭代”切换为“强化研究迭代模式”。

## 当前主瓶颈
- 尚未获得 ordinary D2NN 与 pilot-assisted D2NN 在统一动态像差协议下的最小器件级阳性对照。

## 本轮最高优先级
- 恢复研究迭代，并把后续每轮推进改成可追溯、可检查、可审计的执行模式。

## 本轮新增规则
1. 每轮必须只围绕一个主瓶颈推进。
2. 每轮必须产出可检查交付物或明确阻塞点。
3. 每轮必须写入 `iteration-log.md`。
4. 若无新结果，不得制造“已在运行”的假象。

## 当前真实状态
- 已验证的 strongest evidence 仍停留在 surrogate、wave-optics 和 cross-task 层。
- 器件级主结果仍未完成。
- 自动排程是否正在外部持续触发，当前没有可检查日志证明。

## 下一轮立即动作
- 以最小 NumPy 方案设计 passive diffractive processor 对照脚本接口、控制组和输出格式。

## 本轮新增执行结果
- 已在活动工作区新增并运行 `/workspace/self-calibrating-diffractive-ncomms/round5c_passive_processor_seed_pilot_scan.py`。
- 已产出：
  - `/workspace/self-calibrating-diffractive-ncomms/outputs/round5c_passive_processor_seed_scan_detail.csv`
  - `/workspace/self-calibrating-diffractive-ncomms/outputs/round5c_passive_processor_seed_scan_summary.csv`
  - `/workspace/self-calibrating-diffractive-ncomms/outputs/round5c_passive_processor_seed_scan_summary.json`
  - `/workspace/self-calibrating-diffractive-ncomms/outputs/round5c_passive_processor_seed_scan_summary.md`
  - `/workspace/self-calibrating-diffractive-ncomms/outputs/round5c_passive_processor_seed_scan_panel.png`

## 本轮结果判断
- 这轮真实恢复了 processor-level 链路的工作区可跑性。
- 当前最佳 pilot 幅度窗口出现在 `0.35`。
- 该窗口下 common-path 相比 ordinary 的平均 OOD object-zone PSNR 仅 `+0.061 dB`。
- 同一窗口下 common-path 相比 non-common-path 仍为 `-0.046 dB`，因此还不能把它视为清晰稳健的 Figure 5 阳性结果。
- 这轮的主要价值是恢复可执行链并给出诚实弱结果，而不是完成主结果闭环。
