# 期刊标准：计算成像1 / Nature Communications

## 目标期刊
- Nature Communications

## 官方期刊信息来源
1. Nature Communications Aims & Scope  
   https://www.nature.com/ncomms/aims
2. Nature Communications Editorial process  
   https://www.nature.com/ncomms/submit/editorial-process
3. Nature Communications Content types  
   https://www.nature.com/ncomms/submit/content-types
4. Nature Communications formatting guide PDF  
   https://www.nature.com/documents/ncomms-formatting-instructions.pdf
5. Nature Communications brief submission guide PDF  
   https://www.nature.com/documents/ncomms-submission-guide.pdf

## 官方门槛提要
根据 Nature Communications 官方页面，编辑部首先关注：
- 新颖性
- 潜在影响力
- 是否适合期刊 editorial scope
- 是否包含概念性或方法学推进
- 是否对期刊读者群有兴趣

补充说明：
- Nature Communications 是多学科开放获取期刊，要求研究质量高且能清楚说明其科学意义。
- 文章主文结构通常包括 Introduction、Results、Discussion（如适用）和 Methods（如适用）。
- 提交指南给出的参考文献上限指导值高于本项目要求，因此“30 篇以上参考文献”是本项目内部最低标准，而不是期刊上限。

## 本项目对应的投稿判定标准
以下条件必须同时满足，项目才可视为达到投稿准备状态：

### 1. 创新性与研究意义
- 不只是“更强网络”或“更高 PSNR”
- 必须证明本工作回答了 AI 计算成像可信性中的通用问题
- 必须清楚解释为什么 hallucination boundary 是跨 forward model 的问题

### 2. 理论充分性与论证严密性
- hallucination 的定义必须形式化
- DSI、PDR、HCI 需要详细推导、适用条件和边界说明
- 至少在线性情形下给出扎实理论支撑
- 非线性相位恢复场景至少给出局部 Jacobian / Fisher information 近似链条
- 所有理论推导必须详实、可靠、可检查；未完成详细推导的部分不得包装成已证明结论

### 3. 方法、代码与计算流程可靠性
- forward model、噪声模型、model mismatch 设定明确
- 关键代码真实跑通
- baseline 比较公平且参数设置透明
- 结果可复核，不依赖口头描述

### 4. 数据、结果与稳健性
- 至少三类任务形成完整结果链
- 至少一类线性任务、一类非线性任务、一类高应用价值任务
- 包含 OOD、model mismatch、calibration、abstention 等关键验证
- 必须有失败案例与负结果分析，不能只报最好结果

### 5. 图表质量与表达有效性
- 正文图和补充图全部基于真实完整数据
- 图 1 为整体机制 / 概念框架图
- 图 2-6 需形成主论证链，不允许纯堆图
- 配色、符号、命名、坐标系统一
- 机制示意图、结构示意图和概念图可用 GPT-imag-2.0 生成初稿，但必须后续人工校正并与真实结果图分开管理
- 除示意图外，所有图必须以真实数据为唯一来源

### 6. 写作结构与语言完成度
- 主张强度不得超过证据强度
- Introduction 必须充分覆盖可信性、逆问题、深度先验与 UQ 背景
- Results 章节需严格一图一论点
- Supplementary 必须承担消融、附加推导、附加图和实现细节

### 7. 参考文献与学术定位
- 参考文献数不得少于 30
- 至少覆盖：
  - inverse problems stability / hallucination
  - deep priors / diffusion priors
  - phase retrieval
  - computational microscopy / SIM / deconvolution
  - uncertainty quantification
  - calibration / risk-coverage / abstention

## 当前项目距离期刊标准的差距
- 创新叙事：初步具备
- 理论链：已有线性 benchmark 的第一版区域与指标正式定义，但整体仍明显不足
- 真实结果：已有线性任务最小证据链，并新增当前工作区可复核的区域定义重现实验，但跨任务结果链仍明显不足
- 图表：缺失
- 写作：缺失
- 参考文献：数量已达标，但引用体系仍未完成

## 当前阶段性补充判断
- 线性任务已出现从 hand-crafted prior -> PCA prior -> 非线性 autoencoder prior 的递进证据，这有助于证明 unsupported hallucination 不只来自手工候选库。
- 线性任务现已进一步补上 measurement-consistent latent inverse 基线，这意味着“观测区严格一致时仍出现 bridge hallucination”的现象已不再局限于前馈补全器。
- 当前工作区还重新落地了一套 round4 重现实验与正式定义文档，使 observed / unsupported / bridge 三类区域及其指标首次具有可复算口径。
- 但 Nature Communications 级别仍要求更强的方法学闭环：measurement-consistent 深度先验 / posterior baseline、跨任务结果链、理论推导、正文与补图全部成体系。
- 因此当前进展只能视为“提高了方法可靠性证据”，不能视为“已达到投稿门槛”。

## 当前不允许提前宣称的事项
- 不得宣称“理论已完成”
- 不得宣称“结果已证明”
- 不得宣称“图已齐全”
- 不得宣称“达到 Nature Communications 标准”
- 不得宣称“五位审稿人接收概率均大于 70%”

## 当前建议的阶段门槛
1. 启动阶段门槛：双任务最小基准跑通
2. 结果生成阶段门槛：三类任务核心结果齐全
3. 图表完善阶段门槛：正文图与补图全部形成
4. 成稿阶段门槛：manuscript + supplement 完整
5. 审稿迭代停止门槛：
   - 五位审稿人接收概率均大于 70%
   - 所有需要补的 evidence 全部补齐
   - 所有需要的数据全部补齐
   - 正文和补充材料的图全部补齐
   - 参考文献补齐到 30 篇以上并完成可用引用体系
