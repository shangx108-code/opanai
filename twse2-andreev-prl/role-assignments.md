# Role Assignments

Last updated: 2026-04-28

| Role | Current task | Input | Deliverable | Completion standard |
| --- | --- | --- | --- | --- |
| 统筹者 | 把“补齐所有数据”维持为唯一最高优先级，并把每小时迭代结果转成可追踪的数据闭环计划 | 用户最新优先级、现有 evidence ledger、memory 状态文件 | 每小时状态判断、主瓶颈判断、待同步队列 | 每轮都只保留一个主瓶颈，且把新增数据写入索引 |
| 技术状态检查者 | 核查 normal-state、SGF、BTK/robustness 三条线哪些数据已经真实生成，哪些仍缺数组、对照或统计，并明确区分“旧 baseline”“新 `k`-path baseline”和“新 mixed-star baseline” | SI、source data、重建脚本输出、`k`-path scan 结果、mixed-star scan 结果 | 已验证 / 部分验证 / 未验证的数据清单 | 不把脚本草稿或未落盘结果包装成完整数据包 |
| 环境配置负责人 | 维护本地运行链路与云端存储链路，记录 Python 依赖可用性、Google Drive 权限状态、源 workbook 缺失状态、fallback 数据源、当前 `/workspace/twse2_tb` 运行链，以及稿件源文件缺失状态 | 本地 workspace、Python 工具链、Google Drive connector 状态、memory 镜像 source 表 | 环境可运行记录、云端权限检查记录、源数据来源说明 | 明确区分“原始 workbook 可用”“fallback 镜像可用”“云端已存档”“稿件源是否存在” |
| 理论与数值负责人 A | 继续补齐 normal-state 数据链，但从这一轮起以 `8.372 meV` 的 shared mixed-star 候选为 baseline，停止回到已排空的旧 path / 旧 `A-B` 分支，转去测试能打破 `K^B / K^T` 残差对称性的非共享 `A-C` / `B-C` mixed-star 或 valley-specific gauge 层 | Tuo SI、memory 镜像 source data、重建脚本、`A-B` exclusion scan、`k`-path mapping scan、mixed-star scan | hopping 表、band 对比、残差表、规则排除记录 | true Tuo TB 在全路径无歧义闭合，或至少形成更完整的可审计排除谱系 |
| 理论与数值负责人 B | 在 Track 1 足够稳定后，建立 SGF 最小数据包规范和输出骨架 | exact TB closure、edge geometry、pairing library | SGF arrays schema、最小基准输出清单 | 至少形成可运行、可保存、可索引的 SGF 数据骨架 |
| 理论与数值负责人 C | 在 Track 1 足够稳定后，建立 BTK / robustness 完整数据包模板与字段标准 | exact TB closure、interface model、candidate pairings | conductance arrays 规范、robustness map 字段、结果表模板 | 后续 BTK 结果必须天然适合保存到 memory 与 Drive |
| 数据归档负责人 | 维护 memory 文件夹中的数据索引、待同步队列、文件用途说明，并把新生成的 mixed-star 扫描文件、最佳候选包与新脚本纳入归档和待同步列表 | 本地输出目录、drive-index、archive checklist、新扫描输出 | 数据索引、pending-sync list、归档状态 | 每个关键数据文件都有用途、版本、位置、同步状态 |
| 稿件状态检查者 | 判断当前是否已有足够数据支持正文修改，并限制任何超出数据证据的材料特异性叙述；当前先记录“暂无可编辑稿件源文件”这一限制 | revision notes、三轨数据进度、归档状态、workspace 搜索结果 | 稿件可修改范围判断 | 不在数据包未闭环或稿件源缺失时写过强结论 |
