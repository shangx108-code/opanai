# Role Assignments

Last updated: 2026-04-29

| Role | Current task | Input | Deliverable | Completion standard |
| --- | --- | --- | --- | --- |
| 统筹者 | 把“补齐所有数据”维持为唯一最高优先级，并把新 coupled baseline、SGF 最小包、BTK 最小包转成下轮单一主瓶颈和执行顺序 | 用户最新优先级、现有 evidence ledger、memory 状态文件、2026-04-29 coupled baseline 与最小包结果 | 每轮状态判断、主瓶颈判断、待同步队列 | 每轮都只保留一个主瓶颈，且把新增数据写入索引 |
| 技术状态检查者 | 核查 normal-state、SGF、BTK/robustness 三条线哪些数据已经真实生成，哪些仍缺数组、对照或统计，并明确区分 baseline、exclusion datasets、current faithful coupled baseline、SGF proxy、BTK proxy | SI、source data、重建脚本输出、全部扫描结果、SGF/BTK 最小包结果 | 已验证 / 部分验证 / 未验证的数据清单 | 不把脚本草稿或未落盘结果包装成完整数据包 |
| 环境配置负责人 | 维护本地运行链路与云端存储链路，记录 Python 依赖可用性、Google Drive 权限状态、源 workbook 缺失状态、fallback 数据源、当前 persistent project-space 运行链，以及稿件源文件缺失状态 | 本地 workspace、Python 工具链、Google Drive connector 状态、memory source mirror | 环境可运行记录、云端权限检查记录、源数据来源说明 | 明确区分“原始 workbook 可用”“fallback 镜像可用”“共享 pipeline 可直接回退”“云端已存档”“稿件源是否存在” |
| 理论与数值负责人 A | 继续补齐 normal-state 数据链，以新的 `8.367 meV` coupled path-plus-hopping 候选为 baseline，并把已完成的 short-range + `sqrt(7)` full exact-`Gamma` 联合层视为当前已排空分支，转去测试下一个未扫描 coupled valley-specific 自由度 | Tuo SI、memory source mirror、Track-1 持久脚本、全部 exclusion datasets、current coupled baseline、full 6960-candidate joint ledger | hopping 表、band 对比、残差表、规则排除记录 | true Tuo TB 在全路径无歧义闭合，或至少形成更完整且不重复的 coupled exclusion 谱系 |
| 理论与数值负责人 B | 在持久项目空间里把 SGF 最小包从 finite-ribbon edge proxy 迭代到 manuscript-grade semi-infinite benchmark | current coupled Track-1 baseline、edge geometry、脚本 `code/generate_sgf_minimal_package.py` | SGF arrays、edge-spectrum maps、方法说明 | 至少形成可运行、可保存、可索引的 SGF 数据骨架，并逐步摆脱 proxy 状态 |
| 理论与数值负责人 C | 在持久项目空间里把 BTK / robustness 最小包从 proxy 推进到 material-specific conductance benchmark | SGF minimal package、interface model、candidate pairings、脚本 `code/generate_btk_minimal_package.py` | conductance arrays、robustness metrics、字段说明 | 后续 BTK 结果必须天然适合保存到 memory 与 Drive，并逐步摆脱 proxy 状态 |
| 数据归档负责人 | 维护 memory 文件夹中的数据索引、待同步队列、文件用途说明，并把 Track 1、SGF、BTK 三条线的新包都纳入归档和待同步列表，特别是本轮新增的 joint coupled scan packages | 本地输出目录、drive-index、archive checklist、当前持久代码与数据目录 | 数据索引、pending-sync list、归档状态 | 每个关键数据文件都有用途、版本、位置、同步状态 |
| 稿件状态检查者 | 判断当前是否已有足够数据支持正文修改，并限制任何超出数据证据的材料特异性叙述；当前继续记录“暂无可编辑稿件源文件”这一限制 | revision notes、三轨数据进度、归档状态、workspace 搜索结果 | 稿件可修改范围判断 | 不在数据包未闭环或稿件源缺失时写过强结论，并持续把“无稿件源”与“数据仍未闭环”分开记录 |
