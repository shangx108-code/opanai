可以。下面我把它压成一份**真正可执行、可分工、按 PRL 标准推进的理论任务书**。我会默认一个常见配置：

* **PI / 通讯作者**：总体把关、物理叙事、关键判据裁决
* **博士后 A**：正常态与多轨道校准负责人
* **博士后 B**：散射矩阵 / BTK 主计算负责人
* **博士生 A**：配对对称性、群论与边界态分析
* **博士生 B**：数值收敛、鲁棒性、作图与数据整理

你们可以把角色替换成组内真实姓名，但建议**职责不要混**，否则很容易出现“大家都算了一点，但没有一条主线算透”的问题。

---

# 一、任务书总目标

## 总题目

**Phase-sensitive Andreev fingerprints of unconventional pairing in twisted bilayer WSe(_2)**

## 总交付

一篇 **PRL 目标稿**，主结论限定为：

1. Andreev 光谱选择性追踪 **inner superconducting gap**；
2. ordinary same-sign (s)-wave **不能同时解释** inner-gap tracking 与 ((\alpha, Z, \phi)) 的联合选择规则；
3. 配对被锁定到 **unconventional family**，重点是 sign-changing / valley-odd / chiral-family。

## 项目总门槛

只有同时满足下面四条，才进入 PRL 写作：

* 有一套**清楚的 inner/outer gap 分离理论**
* 有一套**generalized BTK 主引擎**
* 有一张**ordinary (s)-wave 失败图**
* 有一套**可直接给实验使用的指纹 atlas / decision tree**

---

# 二、总体分工图

## PI / 通讯作者

负责：

* 确定文章主 claim
* 决定哪些结果进正文、哪些进补充
* 裁决是否真的“排除了 ordinary (s)-wave”
* 控制论文不滑向“泛拟合文章”

不直接承担重数值，但必须每周审一次“判据是否在变硬”。

---

## 博士后 A：正常态与 correlated background 负责人

负责：

* tWSe(_2) 低能正常态模型
* outer correlated gap / self-energy 的最小表示
* 与近期文献的一致性校准
* 图 1 理论基础、图 2 的 normal-state 部分

---

## 博士后 B：BTK / scattering 主引擎负责人

负责：

* generalized BTK / scattering matrix / Green’s function 代码
* 界面项 (Z,\eta,\alpha) 的实现
* 角向 (\phi) 与 barrier 扫描
* 图 3 的主体与图 4 的核心反证

---

## 博士生 A：配对候选与对称性负责人

负责：

* 三类 pairing candidate 的定义与裁剪
* 对称性分析
* 边界态 / 低能 DOS / strip 几何
* 哪些指纹理论上应该存在，哪些不该存在

---

## 博士生 B：鲁棒性、自动化与图谱整理负责人

负责：

* 参数扫描自动化
* 收敛、宽化、粗糙平均、数值交叉验证
* 指纹 atlas、decision tree、正文作图
* 补充材料中的鲁棒性图

---

# 三、Work Package 拆分

---

# WP0：项目起盘与统一规范

## 负责人

PI 主导，所有人参加

## 要做什么

先统一所有人的“问题定义”和“文章边界”。

### 必须统一的四件事

第一，**第一篇 PRL 不证明唯一拓扑态**。
第二，文章主张是 **phase-sensitive Andreev criterion**，不是“某模型更像实验”。
第三，所有计算都必须服务于四张主图。
第四，所有自由参数必须有物理角色，不能把正文变成可调拟合器。

## 具体任务

* 定出统一记号：(\Delta_{\rm in}, E_{\rm out}, Z, \eta, \alpha, \phi, \Gamma)
* 定出统一候选态：(s)、(s^\pm)/valley-odd、chiral-family
* 定出统一 figure map：每个人知道自己算的东西最终进哪张图

## 预计产出

一页项目白皮书，内容包括：

* 文章一句话 claim
* 四张主图草图
* 各 WP 的输入/输出关系

## 失败后如何转向

如果组内对“是否要声称拓扑”仍反复摇摆，就先把标题和摘要锁死在
**“beyond ordinary (s)-wave”**
不要继续空转。

---

# WP1：正常态与 correlated background 校准

## 负责人

博士后 A
配合：博士生 B 做数值自动化

## 目标

构建一个最小但可信的正常态背景，使文章能自然容纳：

* inner superconducting gap
* outer correlated gap
* 位移场与面内场效应
* valley / spin / band-topology 的最低必要信息

## 要算什么

### 1. 正常态哈密顿量

从 continuum / 三轨道有效模型出发，压缩成低能形式：

[
H_N(\mathbf{k})=
\xi_{\mathbf{k}}\tau_0 s_0
+\mathbf{g}*v(\mathbf{k},D)\cdot \boldsymbol{\tau}
+\mu_B \mathbf{B}*\parallel\cdot \hat g_s \mathbf{s}
]

### 2. correlated background

加入一个最小的正常自能：

[
\Sigma_{\rm corr}(E,\mathbf{k};n,D,T)
]

它不需要一开始就是严格微观推导，但必须满足：

* 能自然给出 outer feature
* 与 superconducting anomalous sector 分离
* 可随 (n,D,T,B) 调整强弱

### 3. DOS 与 normal tunnelling

计算：

* 普通 DOS
* 高势垒极限的 tunnelling conductance
* 两个能标的可见性条件

## 计算设置

建议两层计算。

### 快速层

* (k)-mesh：(60\times 60) 到 (90\times 90)
* 展宽：(\Gamma/\Delta_{\rm in}=0.03,0.05,0.08)
* 参数扫描：(\nu\sim 1) 附近 5–7 个代表点，(D) 取 4–6 个代表值

### 收敛层

* (k)-mesh：(150\times 150) 到 (240\times 240)
* 输出高质量 DOS、谱函数和 normal conductance

## 需要回答的理论问题

* 是否能在不细调的情况下出现 inner/outer 两个能标
* outer feature 是否比 inner gap 更稳健
* 位移场 (D) 是否能自然改变 valley / band 结构，从而影响配对判据

## 预计产出哪张图

### 正文图 1

* 模型示意
* 正常态与 correlated background 的相图草图

### 正文图 2 左半

* high-barrier tunnelling 中的 outer / inner 双能标示意

### 补充材料

* 正常态参数扫描
* 与不同低能模型的对比

## Go 判据

* 双能标是模型自然产物，不是纯拟合构造
* outer 与 inner 的演化可区分
* 正常态背景与近年 tWSe(_2) 文献趋势不冲突

## 失败后如何转向

### 情况 A：双能标始终出不来

转向“phenomenological two-self-energy model”，明确把 (\Sigma_{\rm corr}) 视为输入，而不是试图在第一篇 PRL 里完整解释 correlated background 的微观起源。

### 情况 B：正常态太复杂，参数太多

压缩到单一有效低能 pocket + valley pseudospin 模型，只保留对 (\alpha,\eta,\phi) 有影响的成分。
**宁可简化，也不要让正文被多轨道细节淹没。**

---

# WP2：配对候选库与对称性裁剪

## 负责人

博士生 A
配合：PI 把关物理叙事

## 目标

把候选态压缩到三类，并明确它们在界面 Andreev 中为什么可区分。

## 要算什么

### 1. 三类候选配对

普通 (s)-wave：
[
\Delta_s=\Delta_0 i s_y \tau_0
]

intervalley sign-changing / valley-odd：
[
\Delta_{s^\pm}=\Delta_v i s_y \tau_z
]

chiral-family 低能代表：
[
\Delta_{\rm ch}(\mathbf{k})=\Delta_2 e^{i2\theta_{\mathbf{k}}} i s_y
]

### 2. 对称性分析

写清：

* valley 变换性质
* spin 结构
* TRS / chirality 的差异
* 哪些界面项会采样到其相位结构

### 3. 边界态 / strip geometry

在半无限平面或 strip 中计算：

* low-energy edge DOS
* 局域边界谱权重
* 随 (\phi) 的变化

## 计算设置

* 几何：strip，开放边界一维，平行方向保留动量
* (k_\parallel) 网格：300–800 点
* (\phi)：先取 24 个角点预扫，最终图 72 个角点
* 温度先取 0，后续通过热卷积处理

## 需要回答的理论问题

* ordinary (s)-wave 为什么天然更“平滑”
* sign-changing 态为什么依赖 (\eta) 和 (\alpha)
* chiral-family 为什么可能在较弱 (\eta) 下也保留低能边界谱

## 预计产出哪张图

### 正文图 1 右半

* 三类候选配对示意
* 各自边界态的概念图

### 正文图 4 左列

* 三类态的理论指纹模板

### 补充材料

* 更完整的群论与序参量分类
* 其他被排除的 irreps 简述

## Go 判据

* 三类态在边界低能谱上存在定性可分辨差异
* 这些差异能映射到 ((\alpha,\eta,Z,\phi)) 的实验控制量

## 失败后如何转向

### 情况 A：三类态在边界谱上都太像

说明边界模型过于贫乏。优先回到界面建模，加入更合理的 valley-mixing / orientation form factor，而不是盲目增加更多配对态。

### 情况 B：chiral-family 与 sign-changing 过于难分

第一篇 PRL 就只保留“ordinary (s)-wave vs unconventional family”的二分法；把 sign-changing 与 chiral 的细分推到后续工作。

---

# WP3：generalized BTK / scattering 主引擎

## 负责人

博士后 B
配合：博士生 B 负责自动化与数据管理

## 目标

建立全文最核心的数值引擎，输出所有 (dI/dV) 指纹图。

## 要算什么

### 1. 界面模型

[
U_{\rm int}(x)=Z\delta(x)+\eta\tau_x\delta(x)+U_\alpha(\theta)\delta(x)
]

### 2. 反射概率

对每个入射角 (\theta) 求：

* Andreev reflection (A(E,\theta))
* normal reflection (B(E,\theta))

### 3. 电导

[
\frac{G(V)}{G_N}
================

\frac{\int d\theta,W(\theta,\alpha),[1+A-B]}
{\int d\theta,W(\theta,\alpha)}
\Big|_{E=eV}
]

### 4. 三套主扫描

* (G(V;Z))
* (G(V;\phi))
* (G(V;Z,\phi))

## 计算设置

### 参数网格

* (Z=0) 到 5，先 21 点，最终图可加密到 41 点
* (\eta=0) 到 1，先 11 点
* (\phi=0) 到 (2\pi)，先 36 点，最终 72–144 点
* (\alpha)：两类高对称方向 + 一个偏离方向
* (\Gamma/\Delta_{\rm in}=0.02,0.05,0.10)

### 数值精度

* 入射角 (\theta)：200 点预扫，最终 400–600 点
* 电压 (V)：至少 600–1000 点，确保低能峰不被采样稀释

### 交叉验证

至少对关键参数点，用 Green’s function 方法复算一次，防止波函数匹配算法引入 artifact。

## 需要回答的理论问题

* ordinary (s)-wave 是否只能给出近单调 (Z) 依赖
* sign-changing 态是否在特定 (\eta,\alpha) 下出现阈值型低能峰
* chiral-family 是否在更广参数区间内保留低能边界谱

## 预计产出哪张图

### 正文图 3

* (G(V,\phi))
* (G(V;Z))
* 双晶向 / 双界面方向比较

### 正文图 4 核心

* ordinary (s)-wave 与非常规 family 的直接对照

### 补充材料

* 更多 (\eta,\Gamma,\sigma_\alpha) 参数扫图
* 数值方法互证图

## Go 判据

* 至少得到两类对 ordinary (s)-wave 不利的稳健特征：

  * 晶向选择性
  * barrier 非单调性
  * (\phi)-dependent 的峰增强/分裂/临界关闭

## 失败后如何转向

### 情况 A：所有特征都不稳健

先检查是界面 form factor 太简单，还是宽化太大。
优先优化 (U_\alpha(\theta)) 与 valley mixing 的实现，再重新扫。

### 情况 B：每种态都能调参数拟合

立即暂停“拟合导向”，转去做**decision tree 指标化**。
把注意力从整条谱转移到少数稳健指标，如 (A_\phi, R_0, S)。

---

# WP4：inner-gap selectivity 的理论证明

## 负责人

博士后 A 与博士后 B 联合
配合：博士生 B 负责批处理与数据整理

## 目标

把“AR 只跟 inner gap 走”写成整篇文章的理论地基。

## 要算什么

### 1. 高势垒极限

计算 quasiparticle tunnelling conductance，识别：

* outer feature (E_{\rm out})
* inner superconducting gap (\Delta_{\rm in})

### 2. 低势垒极限

计算 Andreev-dominated conductance，提取：

* (E_{\rm AR})
* 亚隙增强强度
* excess spectral weight

### 3. 定义选择性指标

[
\Xi_{\rm AR}(p)=
\frac{\partial E_{\rm AR}/\partial p}{\partial \Delta_{\rm in}/\partial p},
\quad
p\in{n,D,T,B_\parallel}
]

并与 outer feature 的对应量做比较。

## 计算设置

* 参数点选取：(\nu\sim1) 附近 5–7 个代表点
* 每个点在 3 个 barrier 条件下比较：高 (Z)、中 (Z)、低 (Z)
* (T/T_c)：0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2
* (B_\parallel)：从 0 到配对明显抑制前

## 需要回答的理论问题

* 为什么 outer correlated gap 会出现在 tunnelling 中
* 为什么 AR 对 anomalous self-energy 更敏感
* 在哪些情况下 AR 仍可能混入 outer feature，哪些情况下不会

## 预计产出哪张图

### 正文图 2

* high-barrier vs low-barrier conductance 对比
* (E_{\rm out}, \Delta_{\rm in}, E_{\rm AR}) 的并列演化

### 补充材料

* 不同 (\Sigma_{\rm corr}) 模型下的稳健性
* 选择性指标 (\Xi_{\rm AR}) 的参数扫描

## Go 判据

* 理论上清楚展示 tunnelling 与 AR 对两个能标的不同敏感性
* (E_{\rm AR}) 与 (\Delta_{\rm in}) 同步，而不与 outer feature 同步

## 失败后如何转向

### 情况 A：AR 与 tunnelling 总是追同一个单一能标

则第一篇文章不能再打“inner-gap selectivity”这张牌。
这时需转为纯相位敏感路线：把重点改成 ((\alpha,Z,\phi)) 对不同 pairing 的判据，而不把 outer/inner gap 分离作为主 claim。

### 情况 B：selectivity 只在极窄参数区间出现

把它从正文主结论降为“supporting observation”，正文主结论改成 ordinary (s)-wave exclusion。

---

# WP5：ordinary (s)-wave 失败图与判据树

## 负责人

PI 主导物理判据
博士后 B 负责主计算
博士生 A/B 辅助整理

## 目标

把文章最关键的一句话做实：

**ordinary same-sign (s)-wave cannot simultaneously account for the inner-gap tracking and the joint ((\alpha, Z, \phi)) selection rules.**

## 要算什么

### 1. 给 (s)-wave 最有利条件

允许：

* 各向异性 Zeeman tensor
* 有限 (\Gamma)
* 轻微界面粗糙
* 小到中等的 (\eta)

### 2. 用同一组参数族同时拟合四类约束

* inner-gap tracking
* 晶向选择性
* barrier 非单调性
* 角向临界行为

### 3. 形成失败地图

列出 ordinary (s)-wave：

* 能解释什么
* 解释不了什么
* 需要多不自然的参数才能勉强解释

### 4. 建立 decision tree

定义四个主指标：

[
G_{\rm sub}=\frac{1}{2V_c}\int_{-V_c}^{V_c}G(V)dV
]

[
A_\phi=
\frac{G_{\rm sub}^{\max}-G_{\rm sub}^{\min}}
{G_{\rm sub}^{\max}+G_{\rm sub}^{\min}}
]

[
R_0=\frac{G(0)}{G_N}
]

[
S=\frac{\delta V_{\rm split}}{\Delta_{\rm in}}
]

再联合 (\Xi_{\rm AR}) 形成判据图。

## 计算设置

* 对三类配对统一扫描同一参数盒子
* 每个参数盒子输出同一组 observables
* 不允许对每条曲线单独手工调参

## 预计产出哪张图

### 正文图 4

* 左边：三类配对的指纹模板
* 右边：decision tree
* 底部：ordinary (s)-wave 失败总结图

### 补充材料

* 更大参数空间中的失败统计
* 多种拟合策略的一致失败结果

## Go 判据

* ordinary (s)-wave 的失败是结构性的，而不是“某条曲线不够像”
* 至少有一类非常规 family 在合理参数下自然满足全部主约束

## 失败后如何转向

### 情况 A：ordinary (s)-wave 也能解释全部主特征

这时必须诚实降级。
文章改投 PRB / PRResearch，题目改为
**“Andreev signatures of candidate pairing states...”**
而不是继续坚持 PRL claim。

### 情况 B：非常规 family 之间分不清

第一篇 PRL 保留到 “beyond ordinary (s)-wave”，不要强行细分。

---

# WP6：稳健性、补充材料与成稿

## 负责人

博士生 B 主整理
PI 终审
所有人配合

## 目标

把主结论做“抗审稿”。

## 要做什么

### 1. 鲁棒性测试

* 展宽 (\Gamma) 扫描
* 界面粗糙平均 (\sigma_\alpha)
* (\eta) 分布而非单一值
* 少量自洽界面序参量抑制检查
* 不同数值算法互证

### 2. 文章组织

正文只放四件事：

* 模型框架与候选态
* inner-gap selectivity
* ((\alpha,Z,\phi)) 指纹
* ordinary (s)-wave exclusion

### 3. 补充材料

把所有“但如果参数这样改呢”的问题提前准备好。

## 预计产出哪张图

### 正文

图 1–4 完整版

### 补充

S1–S10：

* 收敛性
* 参数鲁棒性
* 算法互证
* 候选态扩展说明

## Go 判据

* 每个正文结论都有至少一张补充图支撑
* 所有关键图都经过数值方法互证或参数鲁棒性检验

## 失败后如何转向

如果补充材料一旦加入合理粗糙/展宽就摧毁主结论，必须回到 WP3 / WP5 重构判据，不能硬写。

---

# 四、对应四张主图的责任归属

## 图 1：模型与候选态

* 主责：博士后 A + 博士生 A
* 内容：

  * 正常态低能模型
  * (\Sigma_{\rm corr}) 与 (\Delta) 分离
  * 三类配对示意
* 风险：

  * 写得太重，像综述
* 转向：

  * 只保留与后文 observables 直接相关的最小模型

---

## 图 2：inner-gap selectivity

* 主责：博士后 A + 博士后 B
* 内容：

  * tunnelling vs AR
  * (E_{\rm out}, \Delta_{\rm in}, E_{\rm AR})
* 风险：

  * 只是在拟合两个峰
* 转向：

  * 必须用 self-energy 语言说明通道敏感性差异

---

## 图 3：((\alpha,Z,\phi)) phase-sensitive 指纹

* 主责：博士后 B
* 协作：博士生 B
* 内容：

  * (G(V,\phi))
  * barrier 依赖
  * 晶向依赖
* 风险：

  * 谱图太多、主线不清
* 转向：

  * 统一转成 (A_\phi,R_0,S) 三个指标

---

## 图 4：ordinary (s)-wave 失败图 + decision tree

* 主责：PI + 博士后 B
* 协作：全体
* 内容：

  * 三类态对照
  * ordinary (s)-wave 失败清单
  * 指纹决策树
* 风险：

  * 结论写得太满
* 转向：

  * 若无法细分非常规 family，就只保留 “exclude ordinary (s)-wave”

---

# 五、推荐推进节奏

## 第 1 阶段：两周

完成 WP0 + WP1 骨架
目标：知道正常态背景是否站得住。

## 第 2 阶段：两到三周

完成 WP2 + WP3 初版
目标：知道三类态是否真的可区分。

## 第 3 阶段：两周

完成 WP4
目标：知道 inner-gap selectivity 能否成立。

## 第 4 阶段：两周

完成 WP5
目标：知道 ordinary (s)-wave 是否真的失败。

## 第 5 阶段：一到两周

完成 WP6
目标：形成可投 PRL 的正文 + 补充材料骨架。

---

# 六、每周组会应该问的四个问题

为了防止项目跑偏，建议每周例会只问四个问题：

第一，**本周有没有一个结果让 ordinary (s)-wave 更难活下去？**
第二，**本周有没有一个结果让判据更“可操作”，而不是更“漂亮”？**
第三，**有没有哪一块只是增加复杂度，却没有增加判别力？**
第四，**如果今天就投稿，最薄弱的一句 claim 是哪一句？**

---

# 七、最终内部验收标准

在真正进入 PRL 写作前，PI 应该做一次内部“红队审查”。只有以下问题都能答“是”，才进入成稿：

* 我们是否提出了一个**新的 phase-sensitive Andreev 判据**？
* 我们是否说明了**为什么 AR 追踪 inner gap**？
* 我们是否证明了 **ordinary (s)-wave 的结构性失败**？
* 我们是否给出了 **实验上可直接使用的 decision tree**？
* 如果审稿人不接受“拓扑”，这篇文章是否仍然成立？

最后这一条尤其重要。
**最好的 PRL 写法是：即使把“拓扑”二字全部删掉，文章仍然成立。**

如果你们愿意，我下一步可以把这份任务书继续压成一份**周会版甘特图 + 图 1–4 的详细 panel 设计单**。
