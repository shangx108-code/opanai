# round6：phase ambiguity 指标正式说明

## 适用对象
- 当前说明只覆盖计算成像1项目中已经登记过的 round5 相位恢复 benchmark。
- 当前 benchmark 的 forward model 是 Fourier-magnitude phase retrieval。
- 当前说明只绑定已经在项目状态中登记过的字段：
  - `true_reversed_measurement_error`
  - `recovered_measurement_error`
  - `distance_to_true`
  - `distance_to_reversed`
  - `branch_bias`
- 当前工作区未找到 round5 的原始脚本与原始输出文件，因此本说明不重新声明脚本内部实现细节，不补写未现场核验的归一化约定。

## 当前阶段
- 理论强化与最小结果生成阶段。

## 当前总目标
- 把 round5 相位恢复结果从“内部经验现象”推进成 Methods/Results 可直接引用的边界清晰口径，并据此决定下一轮唯一优先级。

## 当前唯一主瓶颈
- 当前 `x_true` 与 `x_rev` 的等测量性是精确事实，但 learned prior 输出 `x_hat` 仍有较高 measurement mismatch。
- 因此目前最大的混淆风险是：把“精确 ambiguity”与“经验性 branch selection”写成同一层级结论。

## 本轮唯一最高优先级
- 固定 exact ambiguity quantity、empirical branch-selection quantity 与 measurement-consistency quantity 的定义边界。

## 本轮交付物
- 一份可检查的 phase ambiguity 指标说明。
- 一份 exact / empirical 结论边界表。
- 一条下一轮优先级判断。

## 完成标准
- 明确哪些量可以写成精确结论。
- 明确哪些量只能写成当前 learned prior baseline 的经验结果。
- 给出下一轮是否优先补强 phase solver 的判断依据。

## 统一记号
令
- \(x_\mathrm{true}\)：ground-truth object
- \(x_\mathrm{rev} := R x_\mathrm{true}\)：当前 benchmark 中与 \(x_\mathrm{true}\) 构成 ambiguity branch 的 reversed object
- \(x_\mathrm{hat}\)：round5 learned prior baseline 的恢复结果
- \(\mathcal{M}(x)\)：当前 phase retrieval 的 measurement map

在当前 round5 口径下，只使用下述三个层级的量：

### 1. 精确 ambiguity 量
\[
\varepsilon_{\mathrm{amb}}(x_\mathrm{true}, x_\mathrm{rev})
:=
\frac{\|\mathcal{M}(x_\mathrm{true})-\mathcal{M}(x_\mathrm{rev})\|_2}
{\max(\|\mathcal{M}(x_\mathrm{true})\|_2,\delta)}.
\]

- 该量对应 round5 字段 `true_reversed_measurement_error`。
- 当前已登记聚合值约为 `1.26e-16`。
- 在本项目当前口径中，它只用于表述：`x_true` 与 `x_rev` 在 measurement 层面数值上等价到机器精度。
- 这是 exact ambiguity quantity，不依赖 learned prior 是否成功恢复。

### 2. 经验 measurement-consistency 量
\[
\varepsilon_{\mathrm{rec}}(x_\mathrm{hat})
:=
\frac{\|\mathcal{M}(x_\mathrm{hat})-\mathcal{M}(x_\mathrm{true})\|_2}
{\max(\|\mathcal{M}(x_\mathrm{true})\|_2,\delta)}.
\]

- 该量对应 round5 字段 `recovered_measurement_error`。
- 因为当前 `x_true` 与 `x_rev` 在测量上等价，所以也可等价地相对于 `x_rev` 书写。
- 当前已登记聚合值约为 `2.52e-01`。
- 该量不是 ambiguity existence 的证据，而是当前 learned prior baseline 是否足够靠近 measurement manifold 的诊断量。

### 3. 经验 branch-selection 量
令 \(D(\cdot,\cdot)\) 表示 round5 已登记字段 `distance_to_true` 与 `distance_to_reversed` 所共用的同一对象域距离泛函。由于 round5 原始脚本当前不在工作区，本轮不重新发明其归一化细节，只要求后续继续使用同一实现。

定义
\[
d_\mathrm{true} := D(x_\mathrm{hat}, x_\mathrm{true}),
\quad
d_\mathrm{rev} := D(x_\mathrm{hat}, x_\mathrm{rev}),
\]
\[
b := d_\mathrm{rev} - d_\mathrm{true}.
\]

- 这里的 \(b\) 对应 round5 字段 `branch_bias`。
- 当前已登记聚合值为：
  - `distance_to_true = 0.4380`
  - `distance_to_reversed = 1.2072`
  - `branch_bias = 0.7692`
- 数值关系满足：
\[
1.2072 - 0.4380 = 0.7692,
\]
  因而当前 `branch_bias` 应解释为“恢复结果更接近 reversed branch 还是 true branch 的距离差”。
- 若 \(b>0\)，说明当前恢复结果在对象域上更接近 \(x_\mathrm{true}\)；
  若 \(b<0\)，说明更接近 \(x_\mathrm{rev}\)；
  若 \(b=0\)，说明当前距离口径下不偏向任一 branch。

## exact / empirical 边界表

| 命题 | 当前状态 | 可否写成精确结论 | 说明 |
| --- | --- | --- | --- |
| \(x_\mathrm{true}\) 与 \(x_\mathrm{rev}\) 在当前 measurement 下等价 | 已有登记数值支撑 | 可以 | 只对应 ambiguity existence |
| `true_reversed_measurement_error` 约为 `1.26e-16` | 已有登记数值支撑 | 可以 | 是 exact ambiguity quantity 的数值实现 |
| `x_hat` 更接近 true branch 而非 reversed branch | 已有登记数值支撑 | 不可以写成普适定理 | 只能写成当前 learned prior baseline 的经验结果 |
| `branch_bias = 0.7692` 且 4/4 个样例为正偏向 | 已有登记数值支撑 | 不可以写成理论必然性 | 只说明当前 baseline 存在经验性 branch bias |
| 当前 learned prior 已解决 phase retrieval ambiguity | 不成立 | 不可以 | 因为 `recovered_measurement_error = 2.52e-01` 仍偏高 |
| 当前结果已经闭合到 DSI / PDR / HCI 理论 | 不成立 | 不可以 | 因为经验 branch selection 仍与 solver 误差耦合 |

## Methods/Results 可写入口径

### 可以写入 Methods 的内容
- 当前 phase benchmark 同时记录：
  - exact ambiguity quantity：`true_reversed_measurement_error`
  - empirical measurement-consistency quantity：`recovered_measurement_error`
  - empirical branch-selection quantities：`distance_to_true`、`distance_to_reversed`、`branch_bias`
- 这样可以把“ambiguity 是否存在”和“当前 learned prior 更偏向哪个 branch”拆成两个不同问题。

### 可以写入 Results 的内容
- 在当前 benchmark 上，`x_true` 与 `x_rev` 的 measurement mismatch 处于 `1.26e-16` 量级，说明 ambiguity branch 的存在是测量层面的精确事实。
- 在同一 benchmark 上，当前 learned prior baseline 的 `branch_bias` 为正，且 4/4 个 held-out 样例均更接近 true branch，说明当前 baseline 存在经验性 true-branch preference。
- 但当前 `recovered_measurement_error` 仍为 `2.52e-01`，因此这一步不能写成“learned prior 已在 ambiguity set 内完成高质量 branch disambiguation”，只能写成“在尚未达到强 measurement consistency 的前提下出现了经验性 branch bias”。

### 当前不能写入正文主结论的内容
- 不能把 branch bias 写成 phase retrieval 的一般定理。
- 不能把当前 toy decoder prior 写成 posterior / diffusion / Bayesian 证据。
- 不能把经验性 branch preference 写成 DSI / PDR / HCI 的已证明接口。

## 与线性任务的接口
- 线性任务中的 observed / unsupported / bridge 指标，描述的是“在 measurement 未支撑区域出现了何种结构”。
- 当前 phase retrieval round5 中的 `branch_bias` 描述的是“在 ambiguity set 的两个等测量 branch 之间，恢复结果更接近哪一支”。
- 两者目前只在“都属于 measurement information 不足时的 prior-induced selection 现象”这一叙述层面可连接。
- 两者目前还不能写成同一个统一指标，因为：
  - 线性任务已有 measurement-consistent baseline；
  - 当前 phase round5 的 `recovered_measurement_error` 仍偏高，solver failure 与 branch bias 尚未完全分离。

## 下一轮优先级判断
- 下一轮应优先补强 phase solver 的 measurement consistency，而不是立刻把 round5 直接接成 DSI / PDR / HCI 理论主接口。

理由：
1. `true_reversed_measurement_error` 已足够说明 exact ambiguity 存在，本轮瓶颈已不在 existence statement。
2. 当前 `branch_bias` 只能说明经验偏向，尚不能脱离 solver error 独立解释。
3. 当 `recovered_measurement_error` 仍在 `2.52e-01` 量级时，若直接推进统一理论接口，容易把 solver 不充分与 prior branch selection 混写。

## 下一轮立即动作
- 以当前 formalization 为约束，设计一个更强的 phase baseline，使 `recovered_measurement_error` 明显下降。
- 在不改变 exact / empirical 边界的前提下，再判断 branch bias 是否仍稳定存在。
