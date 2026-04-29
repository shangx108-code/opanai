# 2026-04-29 研究迭代轮

## 当前阶段
- 最小 runnable chain 稳定后的 Figure 5 局部增强阶段。

## 当前主瓶颈
- common-path 仍未在 processor level 上稳健优于 ordinary D2NN。

## 本轮最高优先级
- 先把环境 readiness 从阻塞项降级为已解决项，再用真实运行结果判断 Figure 5 是否存在可用局部窗口。

## 本轮新增执行结果
- 已创建并验证：
  - `/workspace/self-calibrating-diffractive-ncomms/scripts/environment_smoke_test.py`
  - `/workspace/self-calibrating-diffractive-ncomms/scripts/minimal_passive_d2nn_protocol.md`
  - `/workspace/self-calibrating-diffractive-ncomms/scripts/round6_numpy_passive_d2nn.py`
- 已产出：
  - `/workspace/self-calibrating-diffractive-ncomms/outputs/environment_smoke_test.md`
  - `/workspace/self-calibrating-diffractive-ncomms/outputs/environment_smoke_test.json`
  - `/workspace/self-calibrating-diffractive-ncomms/outputs/environment_smoke_test.png`
  - `/workspace/self-calibrating-diffractive-ncomms/outputs/round6_numpy_passive_d2nn_metrics.csv`
  - `/workspace/self-calibrating-diffractive-ncomms/outputs/round6_numpy_passive_d2nn_summary.md`
  - `/workspace/self-calibrating-diffractive-ncomms/outputs/round6_numpy_passive_d2nn_summary.json`
  - `/workspace/self-calibrating-diffractive-ncomms/outputs/round6_numpy_passive_d2nn_panel.png`
  - `/workspace/self-calibrating-diffractive-ncomms/outputs/round6_numpy_passive_d2nn_training_history.json`

## 本轮结果判断
- 环境已稳定到足以支持后续持续补 Figure 5 数据。
- best common-path 与 best ordinary 在当前最优点上近似持平，不支持“common-path 已稳健领先 ordinary”。
- common-path 在 matched 配置下出现了 `+0.214 dB` 的 local common-vs-noncommon 优势，这说明共路信息并未消失，但仍不足以封闭主文结论。

## 下一轮立即动作
- 固定低 pilot 幅度窗口，继续做 matched 局部扫描，优先验证 common-path 是否能稳定跨过 ordinary。
