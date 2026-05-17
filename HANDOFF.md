# Session Handoff — 2026-05-17

> 用途：会话重启后让 Claude 快速回到当前位置。读这一份 + 文件目录即可。

## 当前位置

刚装好 humanizer-zh skill，因当前会话已加载完 skill 列表，`/humanizer-zh` 这一会话内无法使用。用户决定**重启 Claude Code**以注册 slash command。重启后第一件事是对 `Deliverable.md` 跑 humanizer-zh。

## 目录文件清单

| 文件 | 内容 |
|---|---|
| `GPT.md` | 与 GPT 的 brainstorm 记录，3 个 ROUND（16 idea + 8 前沿方向 + 7 周期 + 6 cycle feature） |
| `Claude.md` | 与 Claude 的 brainstorm 记录，11 个 ROUND（paper 综述 → 范式判断 → 多轮冷审 → F1-F7 目录） |
| `Deliverable.md` | **当前要提交的成品**：12 个 feature 一览表 + Top 3 (F1/F10/F2) 字段级 schema + 排序 criteria |
| `HANDOFF.md` | 本文件 |
| `.agents/skills/humanizer-zh/` | skill 原始位置（npx skills 安装路径） |
| `~/.claude/skills/humanizer-zh` | 软链到上面（Claude Code 实际读取位置） |

## 重启后第一步

```
/humanizer-zh 请人性化 Deliverable.md（原始文档先备份）
```

> 注意：用户 R11 反馈过最终交付物"读起来像 AI"。当前 Deliverable.md 已尽量压了脊柱/三角验证/可被拷问那些修辞，但 humanizer 还能再去一层。

## 这个项目是什么

用户要给 **「另一个大 mentor」**（不是 CDE 项目的宋老师，是另一位）提交一份 **A 股【强势股 / 强势行业 / 强势概念的 event 择时】idea 收集**。本质是 mentor 在测 junior → 能被信任的 researcher 的分水岭：给一个模糊方向，能不能自己拆成结构化、有优先级、可执行的研究地图。

用户个人定位：擅长用 AI agents 处理非结构化字段。已交付的 CDE 新药数据集项目让 mentor 认可"对幻觉的量化与处理工作细致"。

## 关键决定（必须保留，重启后不要回滚）

1. **组织维度**：按"动量 × 事件交互方式"切（加速 / 反转 / 调制 / 状态），不按事件类型平铺。
2. **核心反共识 thesis**：把有日程的催化重构成"集体预期的兑现 / 等待期权的到期"，而非 information shock。推出与 PEAD 反号的预测：「强势 × 后段相」子样本，post-event drift 对 event magnitude 回归系数为负。
3. **无否决表**。用户明确说：mentor 是在 collect idea 横向比较，否决表是 research agenda 的体裁，会浪费同样篇幅对手能多塞 2 个 idea 的空间。
4. **只展开 Top 3 schema**（F1/F10/F2），不把每条都写成 plan。
5. **F1 先做**（解禁，零 look-ahead 的稳件，一周出基准管线）→ **F10 攻坚**（PIT 题材相位，潜状态估计）→ **F2 兑现**（反共识 thesis 验证）。
6. **F7 不作 alpha**，作风控（持仓减仓 / 不进场）；**F12 潮汐**显式标"base 已半拥挤，仅作稳健性对照"。
7. **A 股全局约束就地承认**：T+1 + 封板不可成交；北向盘中实时披露 2024-08 已停；同花顺/东财概念名单被追溯改写无版本史。

## 用户的互动偏好（关键，避免再次踩雷）

- **不要 AI essay 修辞**：脊柱 / 三角验证 / 可被拷问 / 前沿性 这些词是雷区。
- **不要平铺清单**：宁可少而深。15 个有机制的 ≫ 40 个罗列。
- **要 push back，不要 sycophancy**：用户期望 honest disagreement，多次主动顶回你的判断。
- **要带数字的真实瓶颈**，不写"复杂/困难"这类形容词。
- **要"做过的人才会写"的具体处**（例如同花顺名单追溯改写、一字板反转不可交易）。
- **答有立场**：用户问对比/未来演化时，期望有立场的判断而非和稀泥。

## 已讨论但暂未做的事

- **Deliverable.md 走一遍 humanizer-zh**（重启后第一件事）。
- **综合 GPT 没采纳的好点子**：GPT 在周期那一轮提的 **Cycle Mismatch / Second-Wave Detector / Event Phase Sensitivity Matrix** 三条和 Claude 反共识 thesis 同源，目前 Deliverable 没显式认领。若后续 mentor 反馈想要更多，可以从这里扩。
- **F1 单独写一页可交数据团队的事件研究规格**（用户问过是否要，未拍板）。
- **转 Word/PDF 便于正式提交**（备选）。

## 待办决策点（用户尚未拍板）

1. Deliverable 走 humanizer 后是否还需要再轮迭代？
2. 是否需要把 F1 展开成可交数据团队的事件研究规格？
3. 提交格式：直接 Markdown / Word / PDF？

## 几个不能忘的引用源（用户认可的真实事实，避免重新查）

- 北向盘中实时披露：沪深港 2024-04-12 宣布、2024-05-13 关闭、2024-08-19 起改为收盘后总量 + 前十大活跃股 + 季度持仓
- 潮汐/聪明钱因子：东吴金工"市场行为的宝藏 / 技术分析拥抱选股因子"系列已发表，A 股部分拥挤
- arXiv 2605.05211：Olivia Zhang + Zhilin Zhang，IEEE CAI Spain 2026-05-08~10，2026-04-10 上 arXiv（hedge-fund perspective on LLM stock forecasting）
- arXiv 2601.02370：Variance-Aware LLM Annotation for Strategy Research（核心论点：与协变量相关的标注误差使参数估计有偏，平均准确率无意义）
