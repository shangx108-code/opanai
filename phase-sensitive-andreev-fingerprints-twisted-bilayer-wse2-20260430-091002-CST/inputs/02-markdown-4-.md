下面给你们一版**纯理论 PRL 方案书**。它的核心不是“给实验配套做几张谱图”，而是把问题压成一篇**方法型、判据型 PRL**：在刚被建立起来的 twisted bilayer WSe(_2) 超导平台上，提出一套**相位敏感的 Andreev 指纹判据**，它能在不先验假设具体 pairing glue 的前提下，先把真正的 superconducting inner gap 从 correlated outer gap 中分离出来，再用界面晶向、势垒透明度和面内场方向的联合选择规则，**系统排除 ordinary same-sign (s)-wave**。这类工作最符合 PRL 官方强调的两类接受标准：要么“开辟一个新方向/新 avenue”，要么“引入一个高影响力的方法或技术”。你们的理论文章应该明确朝这个标准去设计，而不是写成一篇“多算了几种谱线形”的常规理论论文。([APS Journals][1])

---

## 一、研究目标

### 1. 总目标

构建一套适用于 twisted bilayer WSe(_2) 的**两谷 moiré BdG + generalized BTK** 理论框架，给出可直接用于实验判别的 phase-sensitive Andreev 指纹图谱。文章的中心结论应压成一句话：

**在 tWSe(_2) 中，Andreev 光谱对 inner superconducting gap 具有选择性；而其对界面晶向、intervalley mixing、透明度和面内场方向的联合响应，与 ordinary same-sign (s)-wave 不相容，因此把配对锁定到非常规 family。**

这条目标之所以成立，是因为平台本身已经在 2024–2026 年间被连续坐实：2024 年 10 月首先在 3.5°/3.65° 器件中观察到超导，2025 年 1 月又在 5.0° 器件中独立复现，2026 年 1 月进一步展示了带宽调控下的 Mott–超导–异常金属图景，2026 年 4 月最新工作则把 3.65°–5.0° 的超导相图连成一个连续演化的问题。([Nature][2])

### 2. PRL 级主目标

第一篇 PRL 不应声称“唯一确定具体拓扑态”，而应完成以下三件事：

第一，证明 **Andreev 追踪的是 inner superconducting gap，而不是 outer correlated gap**。
第二，证明 **ordinary same-sign (s)-wave 无法同时解释 inner-gap tracking 与角向/晶向/势垒三重选择规则**。
第三，证明 **至少一类非常规候选（sign-changing / valley-odd / chiral-family）能自然解释主特征**。

这种收敛式论证，比一上来直接宣称“发现 chiral topological superconductivity”更符合 PRL 的证据门槛。([APS Journals][1])

### 3. 次级目标

在第一篇 PRL 的理论主线之外，预留第二阶段扩展：把 N–S 结推广到短 SNS 相位偏置几何，研究 Josephson 谐波、(\phi_0) 偏移和边界定向依赖，用来继续把 sign-changing 与 chiral/topological-family 区分开。这个目标更像后续高水平工作的延伸，而不是第一篇 PRL 的必要条件。

---

## 二、研究背景

### 1. 为什么这篇理论文章现在值得做

现在做这篇理论 PRL，最重要的原因不是“tWSe(_2) 有超导了”，而是这个平台已经从“发现超导”推进到“机制竞争清单已经足够丰富，但缺乏对称性判别”的阶段。实验上，tWSe(_2) 超导已在多个角度区间被独立建立，并显示它与 AFM 邻近的 Fermi-surface reconstruction、Mott 邻近性和强相关行为密切相关。理论上，也已经出现几条有代表性的路径：Schrade–Fu 的弱耦合 spin-valley fluctuation 理论给出两分量序参量并指向 nematic / chiral / topological superconductivity；Das Sarma 一系的 PRB Letter 指向 intervalley intralayer pairing 的普适性；Qimiao Si 团队的 2025 PRL 则提出 topology-induced quantum fluctuations 机制；Hong Yao 团队的 2025 Nature Communications 三轨道模型给出拓扑超导与 AFM 相关绝缘体的统一图景。也就是说，候选态并不缺，真正缺的是**一个对 broad audience 有意义、而且实验可验证的对称性判据**。([Nature][3])

### 2. 为什么选 Andreev，而不是继续做普通配对态分类

如果你们只写“在某个模型里 (d+id) 比 (s^\pm) 稍低一点自由能”，这对 PRL 不够。PRL 更需要的是一个**方法论层面的推进**。Andreev 的优势在于，它在原则上是对异常格林函数、即配对通道本身敏感；而普通隧穿往往同时混入正常自能造成的 correlated gap、intervalley gap 或 many-body resonance。这个区分在 2026 年关于 MATTG 的 Nature 中已经被实验清楚展示：在同一位置观测到 outer gap 和 inner gap 后，Andreev 只跟 inner gap 的掺杂演化一致，而不跟 outer gap 走。这个结果并不是要你们去“复制 MATTG”，而是告诉你们：**在 moiré 超导里，Andreev 可以被升级成真正的 pairing-sensitive probe。** 你们的理论工作要做的，是把这一直觉在 tWSe(_2) 中系统化、相位敏感化、并转化为可操作判据。([Nature][4])

---

## 三、理论依据

### 1. 文章的理论核心

这篇理论 PRL 的最核心思想可以概括成三句话。

第一，**outer correlated gap 与 inner superconducting gap 必须在理论上分开表示**。
第二，**ordinary same-sign (s)-wave 的界面谱响应通常是平滑且近单调的**，很难自然生成“只在某些晶向、某些 intervalley mixing、某些 (Z) 区间才突出的低能 bound-state 指纹”。
第三，**sign-changing / valley-odd / chiral-family 配对会把其相位结构投影到界面散射矩阵里**，因此会在 (\alpha)、(\eta)、(Z)、(\phi) 的联合空间中表现出明显选择规则。

这三点分别对应你们文章中的三条主 claim。

### 2. 最小模型

建议采用下面这套最小模型，而不是一开始就上最重的多体数值。

#### 正常态 + 相关自能 + BdG

[
H_{\rm BdG}(\mathbf{k})=
\begin{pmatrix}
H_N(\mathbf{k})-\mu+\Sigma_{\rm corr}(E,\mathbf{k}) & \Delta(\mathbf{k})\
\Delta^\dagger(\mathbf{k}) & -H_N^T(-\mathbf{k})+\mu-\Sigma_{\rm corr}^T(-E,-\mathbf{k})
\end{pmatrix}.
]

其中正常态最小写成

[
H_N(\mathbf{k})=
\xi_{\mathbf{k}}\tau_0 s_0
+\mathbf{g}*v(\mathbf{k},D)\cdot \boldsymbol{\tau}
+\mu_B \mathbf{B}*{\parallel}\cdot \hat g_s \mathbf{s}.
]

这里 (\tau) 是 valley Pauli 矩阵，(s) 是 spin Pauli 矩阵，(\Sigma_{\rm corr}) 用来承载 outer correlated gap / intervalley gap / many-body resonance splitting，(\Delta) 则只承载真正的 superconducting anomalous self-energy。这样做的目的不是追求形式复杂，而是把图 2 的物理逻辑——“普通隧穿与 Andreev 对不同能标的敏感性不同”——直接写进模型。

#### 三类候选配对

普通同号 (s)-wave：
[
\Delta_s=\Delta_0, i s_y \tau_0
]

intervalley sign-changing / valley-odd：
[
\Delta_{s^\pm}=\Delta_v, i s_y \tau_z
]

chiral/topological-family 的低能代表：
[
\Delta_{\rm ch}(\mathbf{k})=\Delta_2 e^{i2\theta_{\mathbf{k}}} i s_y.
]

这三类候选并不是随意挑的。它们正对应当前文献中最需要被实验区分的三条主要路线：普通配对、valley sign change，以及两分量/手征 family。Schrade–Fu 的 2024 PRB 已经给出两分量序参量与 nematic/chiral/topological 的自然联系；Das Sarma 的 2025 PRB Letter 支持 intervalley intralayer pairing；Yao 团队的 2025 Nature Communications 又给出了拓扑超导与 AFM 邻近性的统一背景。([APS Journals][5])

#### 界面项

[
U_{\rm int}(x)=Z\delta(x)+\eta\tau_x\delta(x)+U_{\alpha}(\theta)\delta(x).
]

其中 (Z) 是势垒强度，(\eta) 是 intervalley mixing，(\alpha) 是界面晶向。理论上最关键的不是把界面写得多精细，而是保证这三个量都能进入谱学 observables。

#### generalized BTK 电导

[
\frac{G(V)}{G_N}
================

\frac{\int d\theta,W(\theta,\alpha),[1+A(E,\theta)-B(E,\theta)]}
{\int d\theta,W(\theta,\alpha)}
\Big|_{E=eV}.
]

(A) 为 Andreev 反射概率，(B) 为正常反射概率，(W(\theta,\alpha)) 给出入射角与界面定向的权重。

---

## 四、总体研究规划

建议把整项理论工作拆成五个 work package。这样更像真正能执行的 PRL 路线，而不是“大一统理论蓝图”。

### WP1：正常态与相关背景的最小校准

任务不是解释所有实验，而是得到一个**已知与近期实验相容的正常态背景**：超导出现在 (\nu!\sim!1) 附近，与 AFM 邻近的 Fermi-surface reconstruction / Mott 邻近性相关，但不必然锁死在 Van Hove 或严格半填充。这个背景与 2025–2026 年的实验结论是一致的。([Nature][6])

### WP2：建立 pairing library

只保留三类最小候选：ordinary (s)、sign-changing / valley-odd、chiral-family。不要在第一篇 PRL 里扩展到十几种 irreps，否则文章会失焦。

### WP3：构建 phase-sensitive generalized BTK

把 (\alpha,\eta,Z,\phi) 全部纳入界面散射。文章的创新点主要落在这里：不是“计算了 (dI/dV)”本身，而是提出一套**能把配对相位结构投影到 Andreev 光谱中的通用框架**。

### WP4：建立“inner-gap selectivity + (s)-wave exclusion”的决策树

这一步是 PRL 的真正结论区。你们最终不能只说“某非常规态更像”，而要说“ordinary (s)-wave 在同一组参数族下无法同时解释若干独立特征”。

### WP5：做稳健性检验与稿件压缩

只保留最硬结论。任何需要大量自由参数才能出现的特征，都不应成为主结论。

---

## 五、详细执行计划

下面我按“每一步要做什么、怎么算、算到什么程度算成功、什么情况下要止损”来写。

---

### 第一步：建立正常态与 correlated background 的校准模型

#### 目标

得到一个足以支撑 superconducting fingerprint 研究的正常态背景，而不是从第一天起就做完整微观机制求解。

#### 建议模型层级

第一层用 **continuum / three-orbital Wannier 校准的低能正常态**。
第二层用 **phenomenological (\Sigma_{\rm corr})** 表征 outer correlated gap、IVC gap 或 many-body resonance splitting。
第三层把 superconducting (\Delta) 单独加入 BdG。

#### 计算设置

探索阶段建议用 moiré BZ 的 (60\times 60) 到 (90\times 90) (k)-mesh；最终收敛图用 (150\times 150) 到 (240\times 240) (k)-mesh。位移场 (D) 与填充 (\nu) 扫描集中在超导相关窗口，优先覆盖 (\nu\approx 1) 附近以及相邻掺杂区。频率轴若采用实频格林函数，建议使用 (\Gamma/\Delta_{\rm in}=0.02)–0.10 的展宽窗口做系统测试，而不是只固定一个宽化值。

#### 这一步的理论分析内容

你们要先回答三个问题：

1. 模型是否自然允许两个费米能附近能标，即一个更脆弱的 inner gap 与一个更稳健的 outer feature。
2. outer feature 是否可以在更高 (T) / (B) / 更宽参数区间中保留。
3. 该正常态背景是否与现有 tWSe(_2) 实验关于 AFM 邻近、Mott 邻近和 angle evolution 的整体趋势相容。([Nature][3])

#### Go / no-go 判据

Go：模型在不引入大量微调的情况下，能给出 inner/outer 双能标的自然分离，并与现有相图趋势兼容。
No-go：若 inner/outer 双能标只能靠纯经验双峰拟合硬塞出来，或者正常态背景与已知相图完全矛盾，则必须先重构正常态模型，不能进入下一步。

---

### 第二步：构建 pairing candidate library，并做对称性裁剪

#### 目标

把文章的候选空间严格限制在三类，并给出它们在 tWSe(_2) 背景下为何最 relevant。

#### 要做的理论分析

对三类配对逐一分析：

* 它们在 valley、spin、point-group 下的变换性质；
* 哪些界面散射过程会显式采样到其相位结构；
* 在面内场 (\mathbf{B}_\parallel) 存在时，哪些特征是对称性允许的，哪些本来就不可能出现。

这一步不能只写“我们考虑三种配对”。你们需要说明：为什么普通 (s)-wave 是零假设，为什么 sign-changing / valley-odd 是基于近期文献的强候选，为什么 chiral-family 作为两分量/拓扑候选的低能代表是有理论基础的。([APS Journals][5])

#### 计算设置

先在均匀体系中求三类态的 bulk gap、边界态谱权重和低能 DOS。这里不必一开始就做全自洽界面 BdG，先在半无限平面或 strip 几何中用格林函数方法求边界谱。建议参数扫描：

* (\Delta/)带宽：从弱耦合到中等耦合的三个代表值；
* (B_\parallel)：从 0 到理论上的 pair-breaking 前阈值；
* (\phi)：至少 36 个角点，最终图建议 72 个角点。

#### Go / no-go 判据

Go：三类候选在统一正常态背景下给出定性可区分的低能边界谱特征。
No-go：若三类候选在你们模型里几乎完全不可区分，说明界面自由度写得过于贫乏，或者正常态投影方式不对，需要回到界面建模而不是继续堆数值。

---

### 第三步：建立 generalized BTK / scattering-matrix 主计算框架

#### 目标

把 pairing symmetry 的区别真正转化成实验可见的 (dI/dV) 指纹。

#### 建议方法

主方法用 **wave-function matching 或 scattering matrix** 做 BTK；
交叉验证用 **surface Green’s function / recursive Green’s function**。
两种方法至少对关键图做一次互证，避免文章被质疑为数值实现 artifact。

#### 计算变量

[
G(V;n,D,T,B_\parallel,\phi;Z,\eta,\alpha,\Gamma)
]

你们真正要扫的是：

* (Z: 0 \to 5)
* (\eta: 0 \to 1)
* (\phi: 0 \to 2\pi)
* (\alpha)：至少两类高对称界面，再加一个偏离高对称方向的中间角
* (T/T_c: 0 \to 1.5)

角积分建议每组参数至少取 200–400 个入射角；最终收敛图可提升到 600 个。温度通过对零温谱与 (-\partial f/\partial E) 卷积实现。必要时加入一个小的 Dynes 宽化 (\Gamma) 与一个小的界面粗糙平均 (\sigma_\alpha)。

#### 这一步的理论分析重点

你们需要明确回答：

1. ordinary (s)-wave 的亚隙谱随 (Z) 是否基本单调、随 (\phi) 是否只是平滑 pair breaking。
2. sign-changing / valley-odd 态是否只有在足够 (\eta) 或特定 (\alpha) 下才显示明显低能峰。
3. chiral-family 是否即使在较弱 (\eta) 下也容易保留低能边界谱权重，并呈现不同的角向模式。
4. 哪些特征是对 (\Gamma) 和 (\sigma_\alpha) 稳健的，哪些只是精细结构。

#### Go / no-go 判据

Go：至少出现两类对 ordinary (s)-wave 不利、且对某非常规 family 稳健的特征，例如晶向选择性、非单调 (Z) 依赖、或者 (\phi)-dependent 的峰增强/分裂。
No-go：如果所有奇特特征都只在极端精细调参下出现，或者一加轻微粗糙平均就消失，则不够 PRL。

---

### 第四步：建立 inner-gap selectivity 的理论证明

#### 目标

把“AR 选中 inner superconducting gap”从一句启发性叙述，变成你们文章里的严谨理论命题。

#### 需要做的事

分别计算：

* 高势垒极限的 quasiparticle tunnelling conductance；
* 低势垒极限的 Andreev-dominated conductance；
* 同一参数下的 DOS 与 anomalous spectral weight。

最简单可操作的做法，是在格林函数语言中显式分离 normal self-energy (\Sigma_{\rm corr}) 与 anomalous self-energy (\Delta)，然后比较两类 transport channel 对它们的敏感性。

#### 计算设置

对每个 ((n,D,T,B)) 点同时输出：

* 隧穿峰位置 (E_{\rm out}), (\Delta_{\rm in})
* Andreev 主要特征位置 (E_{\rm AR})
* anomalous spectral weight 的能量尺度

定义一个选择性指标：

[
\Xi_{\rm AR}(p)=
\frac{\partial E_{\rm AR}/\partial p}{\partial \Delta_{\rm in}/\partial p},
\quad p\in{n,D,T,B_\parallel}.
]

若 (\Xi_{\rm AR}\approx 1)，而与 outer-gap 的对应量不一致，这就是最直接的理论表述。

#### 这一步为什么重要

因为一旦 inner-gap selectivity 站住了，后面的角向谱就不再只是“低能结构学”，而变成了真正的 pairing-sensitive observable。这一步在逻辑上直接承接了 2026 年 MATTG Nature 所给出的实验启发。([Nature][4])

#### Go / no-go 判据

Go：理论上明确区分出 tunnelling 与 AR 对 outer/inner 两个能标的不同敏感性。
No-go：若你们的模型里 AR 与 tunnelling 始终追着同一单一能标走，那么这条 PRL 路线会失去一半以上的说服力。

---

### 第五步：构造“ordinary (s)-wave 失败”的反证体系

#### 目标

把文章从“某非常规态拟合得更好”升级成“ordinary (s)-wave 结构性失败”。

#### 做法

给 ordinary (s)-wave 最有利的条件：

* 允许各向异性 Zeeman tensor；
* 允许有限 (\Gamma)；
* 允许一定界面粗糙；
* 允许小到中等的 valley mixing。

然后用**同一组参数族**去同时解释以下四类特征：

1. inner-gap tracking
2. 晶向选择性
3. (Z) 非单调性
4. (\phi)-dependent 的低能峰增强/分裂或临界关闭

#### 你们最终需要的不是“拟合残差最小”，而是“失败地图”

例如：

* ordinary (s)-wave 可以解释图 2，但解释不了图 3；
* 或它能给出弱角向各向异性，但给不出强晶向选择性；
* 或它能在大 (\eta) 下给出某些峰，但此时又破坏了 inner-gap selectivity。

这类“互不相容的约束”正是 PRL 喜欢的强论证方式。

#### Go / no-go 判据

Go：ordinary (s)-wave 在合理参数空间内无法同时满足四类约束。
No-go：如果 ordinary (s)-wave 也能自然解释全部主特征，那么这篇 PRL 的标题和摘要必须完全重写，不能再以“排除普通 (s)-wave”为主结论。

---

### 第六步：构建可直接写进论文的指纹 atlas 和 decision tree

#### 目标

把理论结果压缩成一套实验可直接使用的判据图，而不是一堆散乱的数值图。

#### 建议定义的三个主指标

亚隙平均电导：
[
G_{\rm sub}=\frac{1}{2V_c}\int_{-V_c}^{V_c}G(V),dV
]

角向各向异性：
[
A_\phi=
\frac{G_{\rm sub}^{\max}-G_{\rm sub}^{\min}}
{G_{\rm sub}^{\max}+G_{\rm sub}^{\min}}
]

低能峰分裂尺度：
[
S=\frac{\delta V_{\rm split}}{\Delta_{\rm in}}.
]

再加上前面的 (\Xi_{\rm AR})，就足以组成一个四维 decision tree：

* 若 (\Xi_{\rm AR}\sim 1) 且 outer gap 不跟随，则先确认 inner-gap selectivity；
* 若 (A_\phi) 很小且 (G_{\rm sub}(Z)) 单调，则更接近 ordinary (s)-wave；
* 若 (A_\phi) 大、且只有在某 (\alpha,\eta) 下出现明显低能峰，则支持 sign-changing / valley-odd；
* 若低能边界谱权重对 (\phi) 呈稳健而非阈值型响应，并在较弱 (\eta) 下仍明显，则更偏向 chiral-family。

#### 这一步的 PRL 价值

这一步最能体现“方法论文”的价值：你们不是在预测某一条曲线，而是在提出一套**与微观机制部分解耦的、可跨实验平台使用的 phase-sensitive diagnostic**。这更接近 PRL 官方强调的“introduce techniques or methods with highly significant impact”。([APS Journals][1])

---

## 六、建议的数值路线与资源分配

如果你们团队只有理论资源，没有实验配合，我建议用“主线 + 验证线”的结构。

主线计算：

* continuum/three-band 校准的正常态；
* phenomenological (\Sigma_{\rm corr})；
* 三类 pairing candidate；
* scattering-matrix BTK；
* parameter atlas + decision tree。

验证线计算：

* surface Green’s function / recursive Green’s function 复核关键结论；
* 有限 (\Gamma)、有限 (\sigma_\alpha)、有限 (\eta) 的鲁棒性；
* 少量自洽 BdG 检查界面附近序参量抑制是否改变主结论。

这样文章不会太重，但又足够抗审稿。

---

## 七、PRL 级别的硬性判据

这篇理论 PRL 是否成立，我建议内部就按以下四条审自己。

第一，是否真正提出了一个**新判据**，而不是又一次 pairing catalog。
第二，是否给出了**inner-gap selectivity** 的明确理论理由。
第三，是否能用**同一参数族**系统排除 ordinary (s)-wave。
第四，是否给出了一套**实验上可执行、且对 broad audience 也讲得清楚**的指纹 atlas。

只要这四条中有两条做不实，这篇文章就更像 PRB；四条都做实，才是 PRL。

---

## 八、建议的论文组织

你们最终的 PRL 不要写成“模型堆砌”。更好的组织是：

第一段：tWSe(_2) 超导平台已建立，但 pairing symmetry 未定。([Nature][2])
第二段：moiré 超导中 ordinary tunnelling 容易混入 correlated outer gap，而 Andreev 可单独追踪 inner gap。([Nature][4])
第三段：我们提出 generalized phase-sensitive BTK 框架，并证明 ordinary (s)-wave 的结构性失败。
正文四图建议为：
图 1 模型与候选态；
图 2 tunnelling vs AR 的 inner/outer gap 分离；
图 3 (\alpha)-(Z)-(\phi) 指纹图；
图 4 decision tree 与 (s)-wave 失败图。

---

## 九、最值得避免的两个误区

第一个误区，是把文章写成“更精致的拟合”。这不够 PRL。
第二个误区，是在没有 topological invariant、相位偏置或边界模稳健证据时，过早宣称“唯一确定为拓扑超导”。当前理论文献的确已经把 tWSe(_2) 与 chiral/topological possibilities 联系起来，但第一篇理论 PRL 最稳的表述仍应是：**ordinary (s)-wave excluded; unconventional family identified.** ([APS Journals][5])

---

如果你们愿意，我下一步可以把这份方案继续压成一份**真正可分工的任务书**：把每个 work package 拆成“谁做、算什么、预计产出哪张图、失败后如何转向”。

[1]: https://journals.aps.org/prl/about?utm_source=chatgpt.com "Physical Review Letters - About Physical Review Letters"
[2]: https://www.nature.com/articles/s41586-024-08116-2?utm_source=chatgpt.com "Superconductivity in twisted bilayer WSe2 | Nature"
[3]: https://www.nature.com/articles/s41586-026-10357-2?utm_source=chatgpt.com "Angle evolution of the superconducting phase diagram in twisted bilayer WSe2 | Nature"
[4]: https://www.nature.com/articles/s41586-025-10067-1?utm_source=chatgpt.com "Resolving intervalley gaps and many-body resonances in moiré superconductors | Nature"
[5]: https://journals.aps.org/prb/abstract/10.1103/PhysRevB.110.035143?utm_source=chatgpt.com "Nematic, chiral, and topological superconductivity in twisted transition metal dichalcogenides | Phys. Rev. B"
[6]: https://www.nature.com/articles/s41586-024-08381-1?utm_source=chatgpt.com "Superconductivity in 5.0° twisted bilayer WSe2 | Nature"
