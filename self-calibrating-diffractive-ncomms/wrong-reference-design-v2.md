# Wrong-reference Design v2

## 状态
- 状态标签：未验证设计说明
- 用途：为下一轮 processor-level wrong-reference 排他性测试提供更强的 decoy/control 家族
- 证据边界：以下内容是已写入工作区脚本的设计入口，不是已运行并验证过的结果

## 当前阶段
- 当前处于 Figure 5 论证目标重写后的设计补强阶段。

## 当前主瓶颈
- 现有 `wrong-reference` 控制仍难以在更高重复数下稳定拉开与 common-path 的差距。

## 本轮最高优先级
- 把更具破坏性的 wrong-reference 家族整理成可复用入口，供下一轮最小增量扫描直接调用。

## 已写入代码的设计家族
- `decoy_bandstop`
  - 使用 `GOOD_REFERENCE` 振幅，但把相位改写为 `bandstop_shuffle` 型混合系数后再放大到 `1.45x`。
  - 设计意图：保留“像是正确参考”的振幅外观，同时在相位上引入跨模态错配。
- `orthogonal_decoy`
  - 使用 `GOOD_REFERENCE` 振幅，并采用 `orthogonal_swap` 型相位置换，系数放大到 `1.30x`。
  - 设计意图：构造与对象相位近似正交的 decoy，相对更直接地破坏共路状态提示。
- `chirped_opposition`
  - 使用 `WRONG_REFERENCE` 振幅，并采用 `chirped_reflection` 相位混合，系数放大到 `1.55x`。
  - 设计意图：同时破坏振幅与相位，并引入更强的 chirped opposition。
- `task_matched_decoy`
  - 使用 `0.6 * GOOD_REFERENCE + 0.4 * WRONG_REFERENCE` 的混合振幅，配合 `task_decoy` 型错配相位，系数放大到 `1.35x`。
  - 设计意图：构造更接近任务统计但不对应真实共路状态的伪参考，测试是否存在“任务匹配假阳性”。
- `anti_phase_plus_decoy`
  - 使用 `WRONG_REFERENCE` 振幅，主相位为 `-1.10 * object_phase`，再叠加 `0.65` 倍 `orthogonal_swap` decoy 相位。
  - 设计意图：在 round9 `anti_phase` 思路基础上加入更明确的 decoy 扰动，看看是否能把暂时出现但未稳定确认的排他性窗口重新拉开。

## 当前判断
- 这些入口已经足够支持下一轮 focused scan，不需要再从零重写 wrong-reference 生成逻辑。
- 但在没有真实运行前，不能把它们写进正文或补充材料当成已证实证据。

## 下一轮立即动作
1. 仅选 `anti_phase_plus_decoy` 与 `task_matched_decoy` 两个优先候选做小规模 repeat 扫描。
2. 固定 round8 稳定 ordinary-positive 窗口，避免同时改太多自由度。
3. 只要 `common minus wrong-reference` 不能跨重复保持正值，就继续把 Figure 5 保持为“ordinary 优势稳健、排他性未闭环”的口径。
