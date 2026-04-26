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
- [x] 线性 benchmark 区域定义说明
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
- [x] 第一版区域指标对齐结果
- [x] rebuilt round3 本地结果
- [x] rebuilt round4 本地结果
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
- 当前工作区已确认存在：
  - `/workspace/computational-imaging-1-ncomms/round1_minimal_benchmark.py`
  - `/workspace/computational-imaging-1-ncomms/round2_linear_pca_prior.py`
  - `/workspace/computational-imaging-1-ncomms/round3_linear_autoencoder_prior.py`
  - `/workspace/computational-imaging-1-ncomms/round4_linear_measurement_consistent_prior.py`
  - `/workspace/computational-imaging-1-ncomms/round1_outputs/`
  - `/workspace/computational-imaging-1-ncomms/round2_outputs/`
  - `/workspace/computational-imaging-1-ncomms/round3_outputs/`
  - `/workspace/computational-imaging-1-ncomms/round4_outputs/`
  - `/workspace/computational-imaging-1-ncomms/linear_region_metric_note_round5.md`
  - `/workspace/computational-imaging-1-ncomms/round5_region_metric_alignment.py`
  - `/workspace/computational-imaging-1-ncomms/round5_outputs/`
- 2026-04-26 新增说明：
  - round3 / round4 现已在当前工作区以 rebuild 形式补回，可作为本地可复核起点。
  - 这些 rebuild 工件不等于历史原始工件的逐字恢复，后续写作必须如实区分。
- 项目记忆中还登记有更晚轮次的 phase 工件与 rebuilt benchmark 进展，但它们当前仍需继续补回或重建为本地可复核工件。
