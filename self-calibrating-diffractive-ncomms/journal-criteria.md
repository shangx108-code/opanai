# 期刊标准：self-calibrating-diffractive-ncomms

## 目标期刊
Nature Communications

## 当前必须满足而尚未满足的门槛
- ordinary D2NN vs pilot-assisted D2NN 的核心阳性对照必须从“弱原型信号”提升到“清晰且稳健”
- 至少两到三类动态退化的统一证据链
- 强基线对照：传统恢复、电子网络、理想上限
- 完整理论边界：为何共路 pilot 有效、何时失效、何时只剩有限增益
- 制造误差与系统误差鲁棒性
- 30+ 篇已核对参考文献
- 正文与补充材料成体系图表

## 当前已初步碰到的积极信号
- 共路 pilot 在 stronger-aberration OOD 集上优于无 reference 和非共路 reference
- 这一积极信号已在 Gaussian surrogate 和 Zernike wave-optics pupil 两轮真实数值链中重复出现
- pilot-channel CRLB 已形成第一版可计算理论支撑
- task-level tight bound 已把 pilot-channel covariance 与 downstream task loss 连接起来
- cross-task surrogate 上已出现第一轮正向泛化信号

## 当前仍存在的高风险
- 该积极信号在最小被动衍射处理器场景下虽然未消失，但目前过弱，仍可能在稍微改变协议后消失
- 如果 pilot-assisted 在 OOD 对照中仍不能显著优于 ordinary D2NN，论文主线将削弱
- 如果更强 ML baseline 仍然不能利用 pilot，ML 说服力会明显不足
- 若只能在单一 surrogate 上成立，目标期刊可能下调
- 在当前纯理论与仿真路线下，实验缺失不作为当前执行失败项，但可能继续限制最终期刊匹配上限
