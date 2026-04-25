# 归档清单：计算成像1

## 项目基础状态
- [x] 已建立项目独立命名空间
- [x] 已建立项目状态文件
- [x] 已建立角色任务文件
- [x] 已建立监督日志
- [x] 已建立审稿历史文件
- [x] 已建立期刊标准文件
- [x] 已建立归档清单

## 理论材料
- [ ] 统一符号表
- [ ] hallucination 形式化定义
- [x] DSI 第一版推导
- [x] PDR 第一版推导
- [ ] HCI 详细推导
- [ ] 线性情形可证明结论
- [ ] 非线性相位恢复近似推导
- [x] round6 phase ambiguity 指标边界说明

## 代码与计算
- [x] 压缩成像最小基准代码
- [x] 相位恢复最小基准代码
- [ ] classical baselines 跑通
- [ ] deep prior baselines 跑通
- [x] 非线性 autoencoder prior 初测
- [x] ambiguity case 生成脚本
- [x] 失败案例记录
- [ ] OOD / model mismatch 实验
- [ ] calibration / abstention 实验

## 数据与结果
- [x] 第一批真实结果数据
- [ ] 主结果矩阵
- [ ] 消融结果
- [ ] 稳健性分析
- [ ] 统计显著性或重复性检查

## 图表
- [ ] Figure 1 概念图定稿
- [ ] Figure 2 理论图定稿
- [ ] Figure 3 压缩成像结果图
- [ ] Figure 4 相位恢复结果图
- [ ] Figure 5 显微任务结果图
- [ ] Figure 6 跨任务总结图
- [ ] Supplementary 全部图表

## 写作
- [ ] manuscript v1
- [ ] supplement v1
- [ ] cover letter 草案
- [ ] rebuttal risk note
- [ ] 最终投稿版正文 PDF
- [ ] 最终投稿版补充材料 PDF

## 参考文献
- [x] 种子文献整理
- [x] 主题分类完成
- [x] 30 篇以上核对完成
- [ ] Bib 文件或文献主表完成

## 审稿循环
- [ ] 五位审稿人第 1 轮
- [ ] 第 1 轮修订
- [ ] 五位审稿人第 2 轮
- [ ] 所有审稿人接收概率 > 70%

## 最终归档包
- [ ] 代码归档
- [ ] 原始数据归档
- [ ] 处理后数据归档
- [ ] 图源文件归档
- [ ] 正文源文件归档
- [ ] 补充材料源文件归档
- [ ] 最终 ZIP 归档包

## 当前归档备注
- round3 当前已落地的实体文件：
  - `/workspace/computational-imaging-1-ncomms/round3_linear_autoencoder_prior.py`
  - `/workspace/computational-imaging-1-ncomms/round3_outputs/round3_summary.json`
  - `/workspace/computational-imaging-1-ncomms/round3_outputs/round3_case_metrics.csv`
  - `/workspace/computational-imaging-1-ncomms/round3_outputs/round3_linear_autoencoder_panel.png`
- round4 当前已落地的实体文件：
  - `/workspace/computational-imaging-1-ncomms/round4_linear_measurement_consistent_prior.py`
  - `/workspace/computational-imaging-1-ncomms/round4_outputs/round4_summary.json`
  - `/workspace/computational-imaging-1-ncomms/round4_outputs/round4_case_metrics.csv`
  - `/workspace/computational-imaging-1-ncomms/round4_outputs/round4_linear_measurement_consistent_panel.png`
  - `/workspace/computational-imaging-1-ncomms/round4_outputs/round4_linear_measurement_mask.png`
- round4 区域定义重现实验当前已落地的实体文件：
  - `/workspace/computational-imaging-1-ncomms/round4_region_formalization_repro.py`
  - `/workspace/computational-imaging-1-ncomms/theory_round3_region_formalization.md`
  - `/workspace/computational-imaging-1-ncomms/round4_region_formalization_outputs/round4_reproduced_summary.json`
  - `/workspace/computational-imaging-1-ncomms/round4_region_formalization_outputs/round4_reproduced_case_metrics.csv`
  - `/workspace/computational-imaging-1-ncomms/round4_region_formalization_outputs/round4_reproduced_panel.png`
  - `/workspace/computational-imaging-1-ncomms/round4_region_formalization_outputs/round4_reproduced_mask.png`
  - `/workspace/computational-imaging-1-ncomms/round4_region_formalization_outputs/round4_region_metadata.json`
- round5 相位恢复 learned-prior 当前已落地的实体文件：
  - `/workspace/computational-imaging-1-ncomms/round5_phase_retrieval_learned_prior.py`
  - `/workspace/computational-imaging-1-ncomms/round5_phase_retrieval_outputs/round5_phase_summary.json`
  - `/workspace/computational-imaging-1-ncomms/round5_phase_retrieval_outputs/round5_phase_case_metrics.csv`
  - `/workspace/computational-imaging-1-ncomms/round5_phase_retrieval_outputs/round5_phase_panel.png`
  - `/workspace/computational-imaging-1-ncomms/round5_phase_retrieval_outputs/round5_phase_ambiguity_notes.md`
- round6 当前已落地的实体文件：
  - `/workspace/memory/computational-imaging-1-ncomms/phase-ambiguity-metrics-round6.md`
- 当前工作区未见历史 round1 / round2 实体脚本与输出文件，说明历史结果记录已保存在项目状态中，但原始归档仍需后续补齐。
- 当前工作区也未见记忆中登记的旧 round4 实体脚本与输出文件，因此旧 round4 工件仍不能视为已现场复核归档；本轮新增的是一套新的可复核重现实验归档。
- 当前工作区同样未见记忆中登记的 round5 原始脚本与输出文件，因此 round5 工件仍需后续补回现场归档；本轮新增的是一份基于已登记状态的指标 formalization 文档，而不是 round5 原始工件的二次现场复核。
