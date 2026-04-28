# Role Assignments

Last updated: 2026-04-29

| Role | Current task | Input | Deliverable | Completion standard |
| --- | --- | --- | --- | --- |
| 统筹者 | 把“补齐所有数据”维持为唯一最高优先级，并把每小时迭代结果转成可追踪的数据闭环计划 | 用户最新优先级、现有 evidence ledger、memory 状态文件 | 每小时状态判断、主瓶颈判断、待同步队列 | 每轮都只保留一个主瓶颈，且把新增数据写入索引 |
| 技术状态检查者 | 核查 normal-state、SGF、BTK/robustness 三条线哪些数据已经真实生成，哪些仍缺数组、对照或统计 | SI、source data、重建脚本输出、后续数值结果 | 已验证 / 部分验证 / 未验证的数据清单 | 不把脚本草稿或未落盘结果包装成完整数据包 |
| 环境配置负责人 | 维护本地运行链路与云端存储链路，特别是记录 Google Drive 权限状态和待同步阻塞 | 本地 workspace、Python 工具链、Google Drive connector 状态 | 环境可运行记录、云端权限检查记录 | 明确区分“本地可运行”与“云端已存档” |
| 理论与数值负责人 A | 先补齐 normal-state 数据链，优先推进 exact `K^B / K^T` closure，同时把每次 accepted candidate 的表格和残差文件落盘 | Tuo SI、Fig. 1c source data、重建脚本 | hopping 表、band 对比、残差表、规则排除记录 | true Tuo TB 在全路径无歧义闭合，或至少形成可审计的数据排除谱系 |
| 理论与数值负责人 B | 在 Track 1 足够稳定后，建立 SGF 最小数据包规范和输出骨架 | exact TB closure、edge geometry、pairing library | SGF arrays schema、最小基准输出清单 | 至少形成可运行、可保存、可索引的 SGF 数据骨架 |
| 理论与数值负责人 C | 在 Track 1 足够稳定后，建立 BTK / robustness 完整数据包模板与字段标准 | exact TB closure、interface model、candidate pairings | conductance arrays 规范、robustness map 字段、结果表模板 | 后续 BTK 结果必须天然适合保存到 memory 与 Drive |
| 数据归档负责人 | 维护 memory 文件夹中的数据索引、待同步队列、文件用途说明，并在权限恢复后推动云盘同步 | 本地输出目录、drive-index、archive checklist | 数据索引、pending-sync list、归档状态 | 每个关键数据文件都有用途、版本、位置、同步状态 |
| 稿件状态检查者 | 判断当前是否已有足够数据支持正文修改，并限制任何超出数据证据的材料特异性叙述 | revision notes、三轨数据进度、归档状态 | 稿件可修改范围判断 | 不在数据包未闭环时写过强结论 |
