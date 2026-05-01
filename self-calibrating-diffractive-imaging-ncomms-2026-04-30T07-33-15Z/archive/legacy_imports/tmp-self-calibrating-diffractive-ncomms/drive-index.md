# 云端资料索引：self-calibrating-diffractive-ncomms

## 当前状态
- 已在 Google Drive 中发现两张现成迭代表，但目前均为空表：
  - `SC-DON NatComm Iteration Ledger`
  - `SC-DON NatComm Iteration Ledger 2026-04-28`
- 两张表都位于“我的云端硬盘”根目录下，当前尚未发现该项目的稳定文件夹结构。
- 当前可用接口已验证到“可读”，但本轮没有可用的 Drive 写入 / 上传入口，因此仍未完成真正归档。

## 待建立的目录建议
- `01-project-admin`
- `02-literature`
- `03-theory`
- `04-data`
- `05-figures`
- `06-manuscript`
- `07-code`
- `08-review-and-supervision`
- `09-archive`

## 已发现的 Drive 落点
- 迭代表 1：`https://docs.google.com/spreadsheets/d/1g9siXbReO87RJ_MoVqIVV3U2kha56J0IbMNPomPNdq8/edit`
- 迭代表 2：`https://docs.google.com/spreadsheets/d/1Obxm2TZxgmlYDOGXnHKEGx9NvtH9XcDBSZquEVLpTgI/edit`
- 两表当前结构：`Sheet1`，26 列，1000 行，`A1:Z20` 为空

## 本轮待同步清单
- 已生成本地 manifest：`/workspace/output/sc-don-drive-sync-manifest-2026-04-29.csv`
- 该 manifest 已覆盖：
  - round6 / round7 活动工作区代码
  - round6 / round7 全部真实输出资产
  - manuscript / review / reference ledger 三份记忆区文档
  - round5 / round5b 当前活动工作区缺失项

## 2026-04-29 长期空间核查结论
- 当前本地长期空间不是空缺，而是“近期结果完整、历史归档与索引滞后”的状态
- 已确认活动工作区输出资产连续覆盖 round6-round19
- 已确认以下长期空间缺口仍存在：
  - Drive manifest 仍未覆盖 round8-round19 的新增资产
  - Drive 正式目录结构尚未真正建立到可写状态
  - Memory 中仍残留一批失效路径引用，主要包括：
    - round5 / round5b 缺失项 `5` 条
    - round5c 旧引用 `4` 条
- 因此“数据齐全性”的当前判断应分开写：
  - 近期活动数据：基本齐全
  - 长期云端归档：未完成
  - 历史全链证据：未齐

## 当前待执行动作
- 当前唯一阻塞：没有可用的 Drive 写入入口，因此不能把 manifest 中的本地文件真正写入 Drive。
- 一旦具备可写入口或用户提供目标文件夹 URL，优先动作如下：
  - 先在现有 Drive 结构中确定项目主目录或使用现有迭代表作为主索引
  - 先刷新 manifest，使其覆盖 round8-round19 新增资产后，再将 `local-ready` 项逐条写入
  - 将缺失项单独标记为 `missing-from-active-workspace`，不伪装为已归档
- 后续写入时优先归档：
  - `/workspace/self-calibrating-diffractive-ncomms/scripts/round6_numpy_passive_d2nn.py`
  - `/workspace/self-calibrating-diffractive-ncomms/scripts/round7_parameter_scan.py`
  - `/workspace/self-calibrating-diffractive-ncomms/outputs/round7_parameter_scan_detail.csv`
  - `/workspace/self-calibrating-diffractive-ncomms/outputs/round7_parameter_scan_summary.csv`
  - `/workspace/self-calibrating-diffractive-ncomms/outputs/round7_best_config_panel.png`
  - `/workspace/memory/self-calibrating-diffractive-ncomms/manuscript-v1-strict.md`
  - `/workspace/memory/self-calibrating-diffractive-ncomms/review-round-manuscript-v1-strict.md`

<!-- auto-drive-sync:start -->
## 自动同步状态
- 最近刷新时间（UTC）：`2026-04-29T02-08-24Z`
- 本地已就绪待同步资产：`28`
- 当前缺失历史资产：`5`
- 最新 manifest：`/workspace/output/sc-don-drive-sync-manifest-latest.csv`
- 最新状态 JSON：`/workspace/output/sc-don-drive-sync-status.json`
- 默认目标文件夹：`SC-DON-NatComm-data` -> `https://drive.google.com/drive/folders/1k09jiRUUyA2hRrynpoJgak0d4-5O4gSe`
- 当前云端写入状态：受限。现有工作流已能自动整理同步包和长期索引，但仍需可写 Drive 入口才能完成真正上云。
- 当前附加问题：manifest 与索引正文尚未吸收 round8-round19 新资产，Memory 内另有 `9` 条失效路径引用待清理
- 已发现的 Drive 台账：
  - `SC-DON NatComm Iteration Ledger`: `https://docs.google.com/spreadsheets/d/1g9siXbReO87RJ_MoVqIVV3U2kha56J0IbMNPomPNdq8/edit`
  - `SC-DON NatComm Iteration Ledger 2026-04-28`: `https://docs.google.com/spreadsheets/d/1Obxm2TZxgmlYDOGXnHKEGx9NvtH9XcDBSZquEVLpTgI/edit`
<!-- auto-drive-sync:end -->
