# 研究迭代日志：self-calibrating-diffractive-ncomms

## 2026-04-29 09:11 CST Round 6 Stable NumPy Chain
- 当前阶段：最小 runnable chain 稳定后进入 Figure 5 局部增强
- 当前唯一主瓶颈：common-path 仍未形成相对 ordinary 的稳健 processor-level 优势
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
  - best ordinary OOD mean PSNR：`20.421 dB`
  - best common-path OOD mean PSNR：`20.421 dB`
  - best non-common-path OOD mean PSNR：`20.473 dB`
  - best wrong-reference OOD mean PSNR：`20.382 dB`
  - matched 配置下的最佳 common-path minus non-common-path 为 `+0.214 dB`

## 2026-05-01 Manuscript Package Build
- 当前阶段：full draft assembly under strict evidence boundary
- 当前唯一主瓶颈：缺少可编译、可归档、符合 Nature Communications 当前投稿节奏的主稿与附录包
- 本轮真实完成：
  - 建立 `/workspace/self-calibrating-diffractive-ncomms/` 论文工程目录
  - 新增 `manuscript/main.tex` 与 `supplement/supplement.tex`
  - 新增 `scripts/render_figures.py`
  - 新增 `data/fig2_mechanism_waveoptics.csv`
  - 新增 `data/fig3_information_transfer.csv`
  - 新增 `data/fig4_processor_boundary.csv`
  - 新增 `data/method_fairness_table.csv`
  - 新增 `source_data/source_data_index.csv`
  - 生成 `figures/figure1_schematic.png`
  - 生成 `figures/figure2_mechanism_waveoptics.png`
  - 生成 `figures/figure3_information_transfer.png`
  - 生成 `figures/figure4_processor_boundary.png`
  - 编译 `manuscript/main.pdf`
  - 编译 `supplement/supplement.pdf`
- 本轮关键判断：
  - 当前主稿已经切换到 NC 兼容节奏：Title / Abstract / Introduction / Results / Discussion / Methods / Data Availability / Code Availability / References。
  - 引言已严格保持四段式。
  - 除示意图外，其余图全部由已有项目账本数值直接生成。
  - 该包解决了“没有可提交稿件工程”的问题，但没有伪装成“全部原始数据已恢复”。
