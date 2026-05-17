# TODO — Deliverable & 周边写作待办

> 验证跑完但还没回写进 Deliverable 的内容 + 后续候选任务
> 所有写作动作需用户先确认再做，避免过载

---

## 一、Deliverable.md / .html / .pdf 待回写（**主要积压**）

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

### C. F10 卡片（sanity + v1 + v2 后**完全重写**）— **三次 thesis pivot**

**当前 deliverable F10 卡片**：写"证据等级变动（双向），category=3 = 79K 条澄清硬信号"

**Sanity + v1 + v2 实证结论**（见 `validations/F10_anchor_reversal/README.md`）：

三次 thesis pivot：
1. **原 thesis（澄清/降级 反转）**：sanity 阶段拆分 category=3 后真澄清 n=3K underpowered → 砍 main
2. **GPT brief（强势 + 异动 → 反转）**：v1 实测 Q5 强势侧无反应 (t=+0.63)，预测方向反了
3. **v2 matched control 确认 bimodal anchor effect**：
   - Q1 弱势 matched diff_10 = **−8.65% (t=−10.4)**
   - Q5 强势 matched diff_10 = **+3.37% (t=+3.15)**
   - 中间 Q3/Q4 几乎无 effect

**真正的 F10 thesis**：
- 异动公告 = **bimodal attention amplifier**（不是降级，不是反转，是双向放大器）
- 机制：交易所强制注意力放大 sentiment-driven price anomaly
- 弱势侧：bad news confirmation → 加速下跌
- 强势侧：注意力刺激 → 追买
- 与 F6（兑现型反共识）独立通道：F6 在 "涨太多→兑现→反转"，F10 在 "已涨/已跌→异动放大"

**需要改的 F10 卡片**：
- thesis 段：从"事件确认等级变动（双向）"改写为"异动公告 bimodal attention amplifier"
- 经济逻辑段：注意力 anchor × prior sentiment state 双向放大
- 字段级 schema：从 evidence_level / historical_max / level_delta 改为 prior_20d_return + cluster (anchor_event flag)
- 数据源：从 LLM 多源抽取 / CninfoAnnouncement.category=3 简化为 CninfoAnnouncement.title 含"异常波动"
- 与 §0 关系：**不是 mini-instance**，是**独立 attention channel**

**回写位置**：Deliverable.md §一 F10 卡片**整段重写** + Schema 重设

---

### D. §0 TL;DR 引用 F6 + F10 作为两个独立实证通道

§0 写 β(θ_t) 反共识 thesis 时，**至今没有 empirical anchor**。现在可以引：

> "F6 v1 在预增 cohort 上提供 β(θ_t) 反共识 thesis 第一个实证 instance：
> 预增公司业绩兑现幅度越正 → 短期 CAR 越负 (clustered t=−2.52)。
> F10 v2 揭示独立的 attention amplifier 通道：异动公告 bimodal 放大 prior sentiment，
> 弱势侧 matched diff_10 = −8.65% (t=−10.4)、强势侧 +3.37% (t=+3.15)。
> 两通道独立但都印证：A 股事件择时 alpha 由 event × prior state 的交互决定。"

**回写位置**：Deliverable.md §0 末尾 or TL;DR 中加一段实证锚

---

### E. §二 排序与先做 — 重排（已有验证证据后）

**当前 §二**：F1/F2/F3 是 Top 3，F6/F10 是后排

**改动**：
- F1 评定改"保留但条件化"——不再 standalone 推荐
- F6 升到 §二 前列（已通过验证 + 锚定 §0 thesis）
- **F10 升到 §二 前列**（v2 matched control 通过，bimodal 实证）
- F3 仍然是反共识载荷，但**链路**：F6 (单 cohort mini-instance) → F3 (全 cohort)
- F10 是独立 attention 通道，不在 §0 §3 链路上，但作为第二个"validated by v2 with strong t-stat"的 feature

**回写位置**：Deliverable.md §二

---

### F. HTML + PDF 同步

Deliverable.md 改完后：
- 同步改 Deliverable.html
- Chrome headless 重出 PDF
- 16 页可能扩到 17-19 页

---

## 二、CLAUDE.md 项目记录待回写

`/Users/yuhonghua/Downloads/strong-event-timing/CLAUDE.md` 是这次对话的完整心路历程，但截止 ROUND 11 (F1-F7 目录交付物)。F1 v4 + F6 v1 + F10 v2 三轮验证没记。

**建议**：不写 ROUND 12/13/14，但在 CLAUDE.md 末尾加 "ROUND 11 之后转入验证阶段，详见 validations/" 一行 pointer。

---

## 三、可选的下一轮验证（按 ROI）

| 优先 | 任务 | 工作量 | 价值 |
|---|---|---|---|
| **高** | **F3 全 cohort 跑**（兑现幅度符号翻转，反共识赌注主载荷）| 1-2 天 | F6 单 cohort 验证后的 logical next step，反共识 thesis 全样本检验 |
| **高** | **F11 corpus dump**（5K title-only sample 给 LLM role classifier）| 2 小时 | F11 LLM 链路启动，data prep 是必经路径 |
| 中 | F6 在 type=4 预增子样本内部跑 SUE 双因子（n=12.6K）| 半天 | GPT 提的"F6 vs PEAD-on-预增 严格非冗余"检验 |
| 中 | F10 v3：收紧 PRIOR_TOL ±5pp → ±2pp + 1:3 matching | 半天 | F10 bimodal finding 稳健性 |
| 中 | F1 v5：行业去均值 + 一字板 filter | 半天 | 验证 F1 v4 diff 是否仍在 |
| 中 | F4 probe（同花顺概念成员 PIT 数据是否在 cache）| 1 天 | 决定 F2/F4/F5 链是否可行 |
| 低 | F1 / F6 / F10 跨 feature 交叉 cohort 跑 | 1 天 | 看三个 reversal/amplifier 信号是否叠加 |

---

## 四、F11 LLM routine 链路状态（GPT 那边在做）

GPT 已 commit 砍到 5 个 routine + 1 个 corpus dump。我这边需要：

1. **Sample title 已给 GPT**（5 条来自 F10 sanity output）
2. **GPT 确认 title-only 够用** → 我开写 dump_announcements.py
3. **GPT 给出最终 dump spec** → bjintern12 跑 corpus dump → push corpus.jsonl.gz
4. GPT 跑 5 个 routine（gold_set / classify / reliability / faithfulness / alpha_test_minimal）

**当前状态**：等 GPT 反馈 title-only 是否够用 + 窗口（2022-2023 vs 2023 only）。

---

## 五、长期：v1 邮件交付

所有 F 卡片验证 + Deliverable 重写完成后：
- 打包 tarball
- 邮件 mentor B
- 标注哪些是 validated, 哪些是 unvalidated

---

## 当前 batch 状态总结（按完成度）

| Feature | Sanity | v1 | v2 | Deliverable 回写 |
|---|---|---|---|---|
| F1 | n/a | ✅ | ✅ (v4) | ❌ pending |
| F6 | ✅ | ✅ | enum 解码 ✅ | ❌ pending (需重写) |
| F10 | ✅ | ✅ | ✅ matched | ❌ pending (完全重写) |
| F3 | — | — | — | — (next) |
| F11 | corpus 待 dump | — | — | — |
| F2/F4/F5 | — | — | — | — |
| F7-F9/F12/F13 | — | — | — | — |

---

## 决策时点

**用户可以一句话告诉我做哪条**：
- "回写 F1 卡片" → 做 A
- "回写 F6 卡片" → 做 B
- "回写 F10 卡片" → 做 C
- "全部回写 + 重出 PDF" → 做 A+B+C+D+E+F（约 2 小时）
- "继续 F3 验证" → 做三的第一项
- "F11 corpus dump" → 做四
- "先什么都不动，等下一个 idea" → 我等着

不再 push 一个个动作往前走，等你 batch 决策。
