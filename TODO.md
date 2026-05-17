# TODO — Deliverable & 周边写作待办

> 验证跑完但还没回写进 Deliverable 的内容 + 后续候选任务
> 所有写作动作需用户先确认再做，避免过载

---

## 一、Deliverable.md / .html / .pdf 待回写

### A. F1 卡片（v4 验证结果）— 待回写

**当前 deliverable F1 卡片**：写于跑验证之前，把 F1 当 standalone alpha

**v4 实证结论**（见 `validations/F1_unlock/README.md`）：
- ALL clean (2018-2023, n=382K)：β_unlock − β_matched = **−0.0042 (t≈−2.6)**
- **regime conditional**：60D vol regime split 显示 low_vol diff=+0.005（反号）/ mid_vol −0.012 / high_vol −0.008 → F1 在低波动期不存在
- **cohort conditional**：首发原股东限售 diff=−0.029 + 首发战略配售 diff=−0.028 撑起信号；股权激励/定增 essentially zero
- freeper interaction β3 marginal (t=−1.88)，"集体期权到期"叙事赢"供给冲击"

**需要改的 F1 卡片表述**：
- "F1 不是 standalone alpha，是 regime × cohort 双条件 reversal"
- 完美 fit §0 β(θ_t) thesis（β 在 regime 间符号都翻转）
- 必须接 vol regime + IPO cohort 两层闸门才能交易
- 这本来就是 deliverable §0 thesis 在 unlock 事件上的具体形态

**回写位置**：Deliverable.md §一 F1 卡片 + 简短摘要嵌入 §0 TL;DR

---

### B. F6 卡片（v1 + enum 解码后的 thesis 重写）— **重写而非更新**

**当前 deliverable F6 卡片**：写"forecast_dev 是 PEAD 之外的独立第二维 surprise"

**v1 实证 + enum 解码结论**（见 `validations/F6_perfforecast/README.md`）：
- 主表 clustered t = **−2.52** ✅ 通过门槛
- ForcastType_INTEGER 数据驱动解码：type=4 = 预增 (45% events)，**几乎独自驱动主信号**（在 12.6K 预增匹配上 t=−1.99）
- F6 在预增子样本上 β<0 是**反 PEAD 方向**（PEAD 文献预测预增 → drift+，实测 → drift−）
- **不再是"PEAD 之外的独立第二维"**，**是 §0 β(θ_t) 反共识 thesis 的第一个干净实证 instance**
- 本质是 F3「兑现幅度符号翻转项」在预增 cohort 上的 mini 验证

**lag bucket 额外发现**：
- early-post (0-30d) t=−2.18 / mid (30-90d) t=−2.05
- pre-period (<0d) t=−0.87（GPT pre-run 预测的"提前定锚"被反驳）

**需要改的 F6 卡片**：
- thesis 段：从"PEAD 第二维"重写为"§0 反共识 thesis 在预增 cohort 的第一个实证"
- 经济逻辑段：集体期权到期 → 反 PEAD 方向
- 与 F3 的关系：F6 是 F3 在单一 cohort 上的 mini-instance，F3 全 cohort 跑是 logical next step
- 注意：原"双重锚点"说法保留为机制论述，但**别说"与 PEAD 独立"**

**回写位置**：Deliverable.md §一 F6 卡片**整段重写**

---

### C. §0 TL;DR 引用 F6 作为第一个实证

§0 写 β(θ_t) 反共识 thesis 时，**至今没有 empirical anchor**。现在可以引：

> "F6 v1 在预增子样本上提供了 β(θ_t) 反共识 thesis 的第一个实证 instance：
> 预增公司业绩兑现幅度越正 → 短期 CAR 越负 (clustered t=−2.52)，
> 反 PEAD 方向，与 §0 thesis 一致"

**回写位置**：Deliverable.md §0 末尾 or TL;DR 中加一行实证锚

---

### D. §二 排序与先做 — 重排

**当前 §二**：F1/F2/F3 是 Top 3，F6 是后排

**改动**：
- F1 评定改"保留但条件化"——不再 standalone 推荐
- F6 升到 §二 前列（已通过验证 + 锚定 §0 thesis）
- F3 仍然是反共识载荷，但**链路**：F6 (单 cohort mini-instance) → F3 (全 cohort)

**回写位置**：Deliverable.md §二

---

### E. HTML + PDF 同步

Deliverable.md 改完后：
- 同步改 Deliverable.html
- Chrome headless 重出 PDF
- 16 页可能扩到 17-18 页

---

## 二、CLAUDE.md 项目记录待回写

`/Users/yuhonghua/Downloads/strong-event-timing/CLAUDE.md` 是这次对话的完整心路历程，但截止 ROUND 11 (F1-F7 目录交付物)。F1 v4 验证 + F6 v1 验证两轮没记。

可考虑加 ROUND 12: F1 验证 + ROUND 13: F6 验证 — 但工作量大，且 validations/ 目录里 README 已经详细记录了，CLAUDE.md 主要价值是 idea 演进而非验证流程。

**建议**：不写 ROUND 12/13，但在 CLAUDE.md 末尾加 "ROUND 11 之后转入验证阶段，详见 validations/" 一行 pointer。

---

## 三、可选的下一轮验证

按 ROI 优先级（F6 已验证后的剩余 ranking）：

| 优先 | 任务 | 工作量 | 价值 |
|---|---|---|---|
| **高** | **F3 全 cohort 跑**（兑现幅度符号翻转，反共识赌注主载荷）| 1-2 天 | F6 单 cohort 验证后的 logical next step，反共识 thesis 全样本检验 |
| 中 | F6 在 type=4 预增子样本内部跑 SUE 双因子（n=12.6K）| 半天 | GPT 提的"F6 vs PEAD-on-预增 严格非冗余"检验 |
| 中 | F1 v5：行业去均值 + 一字板 filter | 半天 | 验证 F1 v4 diff 是否仍在 |
| 中 | F4 probe（同花顺概念成员 PIT 数据是否在 cache）| 1 天 | 决定 F2/F4/F5 链是否可行 |
| 低 | F1 / F6 在 type=4 预增 × IPO 原股东 cohort 交叉跑 | 半天 | 看 F1 + F6 两个 reversal 信号是否叠加 |
| 低 | F6 在其他 cohort（首亏、扭亏）单独看 | 半天 | 完整 cohort map，目前 n 都太小 |

---

## 四、长期：v1 邮件交付

F1-F7 卡片全部验证 + Deliverable 重写完成后：
- 打包 tarball
- 邮件 mentor B（lsong_intern@cqfunds.com 不对，是另一个 mentor）
- 标注哪些是 validated, 哪些是 unvalidated

---

## 决策时点

**用户可以一句话告诉我做哪条**：
- "回写 F1 卡片" → 做一
- "回写 F6 卡片" → 做二
- "都回写，重出 PDF" → 做 A+B+C+D+E
- "继续 F3 验证" → 做三的第一项
- "先什么都不动，看下一个 F" → 我等着

不再 push 一个个动作往前走，等你 batch 决策。
