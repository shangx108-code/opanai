# Role Assignments

Last updated: 2026-04-29

| Role | Current task | Input | Deliverable | Completion standard |
| --- | --- | --- | --- | --- |
| 统筹者 | 把“补齐所有数据”维持为唯一最高优先级，并把新的 V3 有效闭合结果转成下一轮唯一主瓶颈与执行顺序 | 用户最新优先级、现有 evidence ledger、memory 状态文件、2026-04-29 coupled baseline、V3 包与最小包结果 | 每轮状态判断、主瓶颈判断、待同步队列 | 每轮都只保留一个主瓶颈，且把新增数据写入索引 |
| 技术状态检查者 | 核查 normal-state、SGF、BTK/robustness 三条线哪些数据已经真实生成，哪些仍缺数组、对照或统计，并明确区分 faithful coupled baseline、full V3、k-space sparse V3、SGF trial proxy、BTK proxy | SI、source data、重建脚本输出、全部扫描结果、V3 包、compressed-V3 包、SGF/BTK 包结果 | 已验证 / 部分验证 / 未验证的数据清单 | 不把脚本草稿或未落盘结果包装成完整数据包 |
| 环境配置负责人 | 维护本地运行链路与云端存储链路，记录 Python 依赖可用性、Google Drive 权限状态、源 workbook 缺失状态、fallback 数据源、当前 persistent project-space 运行链，以及稿件源文件缺失状态 | 本地 workspace、Python 工具链、Google Drive connector 状态、memory source mirror | 环境可运行记录、云端权限检查记录、源数据来源说明 | 明确区分“原始 workbook 可用”“fallback 镜像可用”“云端已存档”“稿件源是否存在” |
| 理论与数值负责人 A | 继续强化现在的 k-space sparse V3 主版本，把 `3.296 meV` 再往 full V3 的 `1.503 meV` 压，而不是退回逐点 profile 或更宽盲扫 | Tuo SI、memory source mirror、Track-1 持久脚本、current coupled baseline、V3 correction profile、compressed-V3 包、k-space sparse V3 包 | 更强的 k-space sparse 模型、band 对比、残差表、参数解释 | 压缩版 V3 能更接近 full V3，同时仍保持低维可解释和 off-path 可用结构 |
| 理论与数值负责人 B | 已完成 semi-infinite SGF 验证；当前任务转为维护这条半无限基线并为 BTK 重跑提供稳定 normal-state 输入 | current coupled baseline、full V3、k-space sparse V3、edge geometry、脚本 `code/generate_sgf_minimal_package.py`、`code/run_sgf_with_kspace_sparse_v3.py` 与 `code/run_sgf_semi_infinite_with_kspace_sparse_v3.py` | 已验证的 semi-infinite SGF arrays、edge-spectrum maps、baseline-vs-compressed-V3 比较、方法说明 | SGF 数据保持无负谱重、无触顶点，并作为 BTK 的唯一活动 normal-state 输入 |
| 理论与数值负责人 C | 已完成 semi-infinite SGF 输入下的 valley-resolved generalized BTK 重跑；当前任务是比较新旧 BTK 结论并筛掉只在 finite-ribbon proxy 下成立的叙事 | SGF semi-infinite benchmark、旧 finite-ribbon BTK 包、新 semi-infinite BTK 包、脚本 `code/generate_btk_minimal_package.py` 与 `code/generate_valley_resolved_generalized_btk.py` | valley-resolved conductance arrays、robustness metrics、model-comparison summary、old-vs-new comparison note | 后续 BTK 结果必须保持 valley 分辨和 compressed-V3 锚定，并以 semi-infinite SGF 输入版本作为唯一活动主版本 |
| 数据归档负责人 | 维护 memory 文件夹中的数据索引、待同步队列、文件用途说明，并把新的 V3 包、compressed-V3 包以及 Track 1、SGF、BTK 三条线的新包都纳入归档和待同步列表 | 本地输出目录、drive-index、archive checklist、当前持久代码与数据目录 | 数据索引、pending-sync list、归档状态 | 每个关键数据文件都有用途、版本、位置、同步状态 |
| 稿件状态检查者 | 判断当前是否已有足够数据支持正文修改，并限制任何超出数据证据的材料特异性叙述；当前继续记录“暂无可编辑稿件源文件”这一限制 | revision notes、三轨数据进度、归档状态、workspace 搜索结果 | 稿件可修改范围判断 | 不在数据包未闭环或稿件源缺失时写过强结论 |
