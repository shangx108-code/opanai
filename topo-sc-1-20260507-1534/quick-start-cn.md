# 快速使用说明

这套包的目的，是把“拓扑超导1”的理论主线压成一套可直接交给 Codex 的计算执行规范，而不是继续扩项目路线。

## 你先看什么

1. `theory-execution-brief.md`
   先确认理论边界、主张层级和不能越界的地方。
2. `codex-prompts/00-master-prompt.md`
   这是给 Codex 的总约束。
3. `codex-prompts/01` 到 `05`
   这是分工作包的计算提示词。
4. `feedback-templates/`
   这是 Codex 每跑完一个块后必须回填的反馈文件。

## 推荐使用方式

### 方式 A：分块推进

按 `WP1 -> WP2 -> WP3 -> WP4 -> WP5` 依次给 Codex。

适合你们想先把基线模型和应变相图做扎实。

### 方式 B：一键启动后再拆块

先把 `codex-prompts/06-one-shot-execution-prompt.md` 整体贴给 Codex，让它理解全局，再让它单独执行具体 WP。

适合你们已经准备开始实际编码。

## 这套反馈文件解决什么问题

- 防止 Codex 只给图不给证据判断
- 防止 near-zero 态被直接写成 Majorana
- 防止模型参数、单位、符号约定丢失
- 防止图能看但不能进稿

## 这轮已经帮你锁死的东西

- 主平台是 Fe(Te,Se)，不切到 TaS2 或 2M-WS2
- 目标稿件线按 Nature Communications 组织
- 主叙事是“应变-位错-涡旋协同编程 Majorana”，不是单一应变调零模
- 本项目按一次性交付包处理，不按长期项目迭代管理
