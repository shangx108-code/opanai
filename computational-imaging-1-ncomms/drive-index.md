# 资料索引：计算成像1

## 最近更新时间
- 日期：2026-04-26
- 更新类型：自动迭代状态核查后的资料位置纠偏

## 当前索引结论
- 当前项目的长期资料索引尚未闭合。
- 本地工作区当前未找到 `/workspace/computational-imaging-1-ncomms/` 项目目录。
- 当前命名空间内已现场读取到的文件只有：
  - `project-state.md`
  - `role-assignments.md`
  - `supervision-log.md`
  - `review-history.md`
  - `journal-criteria.md`
  - `archive-checklist.md`
  - `phase-ambiguity-metrics-round6.md`
- 项目状态与归档清单中登记的 round7-10 脚本、输出表和图片目前都属于“记忆中有记录，但本轮未在本地找到原始工件”。

## 本地工作区状态
### 已验证存在
- `/workspace/memory/computational-imaging-1-ncomms/phase-ambiguity-metrics-round6.md`
- `/workspace/memory/computational-imaging-1-ncomms/` 下的项目状态文件集合

### 未在当前工作区找到
- `/workspace/computational-imaging-1-ncomms/round7_phase_pca_solver_rebuild.py`
- `/workspace/computational-imaging-1-ncomms/round8_phase_branch_robustness_scan.py`
- `/workspace/computational-imaging-1-ncomms/round9_phase_orientation_ratio_scan.py`
- `/workspace/computational-imaging-1-ncomms/round10_phase_debiased_exact_pair.py`
- 以及这些脚本对应的输出目录、CSV、JSON、PNG、Markdown 说明文件

## 云端资料状态
- 本轮尝试检索 Google Drive 失败，返回权限不足错误。
- 因此当前无法确认：
  - 是否已有对应项目文件夹
  - 是否已有 round7-10 原始脚本或结果包
  - 是否存在正文、补充材料、图表或代码归档版本

## 当前阻塞
1. 本地可运行工件缺失，导致下一轮 solver 级 symmetry-enforced 实验没有真实起点。
2. 云端资料暂时无法检索，导致无法判断原始工件是否可直接回填。
3. 索引与实体文件不同步，当前不能把归档清单中的旧路径继续算作“已现场复核”。

## 下一轮索引动作
1. 先恢复本地 `/workspace/computational-imaging-1-ncomms/` 最小目录，至少补回 round7 或 round10 的一套脚本与输出。
2. 若本地无法直接恢复，则优先解决 Google Drive 权限并重新检索项目资料。
3. 一旦找到真实工件，立即在本文件中补记：
  - 文件名称
  - 内容类型
  - 用途
  - 版本状态
  - 所在位置
