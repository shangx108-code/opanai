# Role Assignments

Last updated: 2026-04-26

| Role | Current task | Input | Deliverable | Completion standard |
| --- | --- | --- | --- | --- |
| 统筹者 | 保持唯一主瓶颈为 `K` 点 valley 闭合，同时把 SGF 与 BTK 组织成紧随其后的两条执行线 | 用户 evidence ledger、上传文献包、现有 PRL 修改计划 | 当前轮状态判断与优先级 | 只保留一个主瓶颈并给出下一步可执行动作 |
| 技术状态检查者 | 核查 `K` 点闭合、SGF、BTK/robustness 三条线哪些已真实验证，哪些仍只是设想 | SI、source data、局部重建脚本输出、revision notes | 已验证 / 部分验证 / 未验证清单 | 不把近似重建或计划性模块包装成已闭环 |
| 环境配置负责人 | 确认 PDF、xlsx、数值脚本可正常读取运行，并记录未来 SGF / BTK 最小可运行链路已具备哪些前提 | 本地 workspace 与 Python 工具链 | 可运行链路记录 | 至少完成 SI 提取、xlsx 读取、带结构对比，并明确“环境可跑”不等于“代码已存在” |
| 理论与数值负责人 A | 从 Eq. (S1) 与 Fig. S1 重建完整 hopping 表和 `H_TB(k)`，优先消除 `K^B / K^T` 歧义 | Tuo SI、source data Fig. 1c | 可复算的 exact-TB 闭环脚本与 band-check 数据 | true Tuo TB 在全路径无歧义闭合 |
| 理论与数值负责人 B | 设计并实现 surface Green's-function 基准模块 | exact TB closure、pairing library、edge geometry | SGF 代码 / 数据规范与边谱输出 | edge spectral benchmark 可复算且能与 BTK hierarchy 对照 |
| 理论与数值负责人 C | 设计并实现 valley-resolved BTK 与 robustness 全数据包 | exact TB closure、interface model、candidate pairings | conductance arrays、robustness maps、observable tables | 主要 BTK 结论都有保存数组支持 |
| 稿件状态检查者 | 判断当前是否具备真正修改论文正文的证据条件，并持续限制材料特异性表述 | 现有 revision notes 与三轨进度 | 稿件可修改范围判断 | 不在 true TB 尚未闭环时写过强材料特异性表述 |
