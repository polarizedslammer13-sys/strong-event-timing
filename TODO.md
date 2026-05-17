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

**回写位置**：Deliverable.md §一 F1 卡片 + 简短摘要嵌入 §0 TL;DR

---

### B. F6 卡片（v1 + enum 解码后的 thesis 重写）— **重写而非更新**

**当前 deliverable F6 卡片**：写"forecast_dev 是 PEAD 之外的独立第二维 surprise"

**v1 实证 + enum 解码结论**（见 `validations/F6_perfforecast/README.md`）：
- 主表 clustered t = **−2.52** ✅ 通过门槛
- ForcastType_INTEGER 数据驱动解码：type=4 = 预增 (45% events)，**几乎独自驱动主信号**（在 12.6K 预增匹配上 t=−1.99）
- F6 在预增子样本上 β<0 是**反 PEAD 方向**（PEAD 文献预测预增 → drift+，实测 → drift−）
- **不再是"PEAD 之外的独立第二维"**，**是 §0 β(θ_t) 反共识 thesis 的第一个干净实证 instance**

**lag bucket 额外发现**：
- early-post (0-30d) t=−2.18 / mid (30-90d) t=−2.05
- pre-period (<0d) t=−0.87（GPT pre-run 预测的"提前定锚"被反驳）

**回写位置**：Deliverable.md §一 F6 卡片**整段重写**

---

### C. F10 卡片（sanity + v1 + v2 + v3 + v4 后**完全重写**）— **五次 thesis pivot**

**当前 deliverable F10 卡片**：写"证据等级变动（双向），category=3 = 79K 条澄清硬信号"

**完整验证链结论**（见 `validations/F10_anchor_reversal/README.md`）：

**5 次 thesis pivot 史**：
1. 澄清/降级 = 反转硬信号 → sanity 阶段 n=3K underpowered, 砍
2. GPT brief: 强势 + 异动 = forced anchor 反转 → v1 实测 Q5 t=+0.63 反向
3. 弱势 + 异动 = 加速下跌 → v1 Q1 t=-10.88 但 momentum vs anchor 无 ID
4. v2 matched control bimodal → Q1 -8.65% + Q5 +3.37% 都 identified
5. **v3 capacity check + v4 split-half**：Q5 +3.37% paper-only (tradable t=-0.35)，Q1 真稳

**v4 最终 thesis**：
- F10 = **异动公告作 sentiment amplifier 在弱-中 prior return cohort 上加速反转**
- **Q1 弱势 (prior 20D ≤ -8.8%) tradable diff_10 = -6.25% (t=-6.21)**，split-half 2018: t=-4.92 / 2019: t=-4.30 极稳
- **Q3 中性 (prior +11~20%)** 同方向稳但弱
- Q2 marginal, Q4 OOS 失效, **Q5 涨停一字板 paper-only**
- **Capacity ≈ 35-73 亿元/年 (Q1)**，70-150 亿/年 (Q1+Q3)
- Cache 限制 → 1.5y 单 regime sample，严格 OOS hold-out 不可行

**需要改的 F10 卡片**：
- thesis 段：从"证据等级变动 双向"完全重写为"Q1+Q3 弱-中 cohort sentiment amplifier"
- 字段级 schema：去掉 evidence_level / historical_max / level_delta，改为 prior_20d_return cohort + trigger_passive flag
- 数据源：从 "LLM 多源 + category=3 79K" 简化为 "CninfoAnnouncement.title 含异常波动"
- 与 §0 关系：**独立通道**，不是 §0 反共识 thesis mini-instance（与 F6 不同）
- 必加 5-pivot 防御段（数据驱动升级 + cache 限制 + split-half weak proxy）

**回写位置**：Deliverable.md §一 F10 卡片**整段重写** + Schema 重设

---

### D. §0 TL;DR 引用 F6 + F10 作为两条独立实证通道

§0 写 β(θ_t) 反共识 thesis 时，至今没有 empirical anchor。现在可以引：

> "F6 v1 在预增 cohort 上提供 β(θ_t) 反共识 thesis 第一个实证 instance：
> 预增公司业绩兑现幅度越正 → 短期 CAR 越负 (clustered t=−2.52)。
> F10 v4 揭示独立的 attention amplifier 通道：异动公告对弱-中 prior cohort 加速反转，
> Q1 弱势 tradable diff_10 = −6.25% (t=−6.21)，split-half 两期都 t<-4。
> 两通道独立但都印证：A 股事件择时 alpha 由 event × prior state 的交互决定。"

**回写位置**：Deliverable.md §0 末尾 or TL;DR 中加一段实证锚

---

### E. §二 排序与先做 — 重排

**当前 §二**：F1/F2/F3 是 Top 3

**改动**：
- F1 评定改"保留但条件化"——不再 standalone 推荐
- F6 升到前列（已通过验证 + §0 mini-instance）
- **F10 升到前列**（v4 通过 ID + capacity check，独立 attention 通道）
- F3 仍是反共识载荷主线，链路：F6 (单 cohort mini-instance) → F3 (全 cohort)

**回写位置**：Deliverable.md §二

---

### F. HTML + PDF 同步

Deliverable.md 改完后：
- 同步改 Deliverable.html
- Chrome headless 重出 PDF

---

## 二、CLAUDE.md 项目记录

CLAUDE.md 截止 ROUND 11，F1/F6/F10 三轮验证没记。

**建议**：在末尾加 "ROUND 11 之后转入验证阶段，详见 validations/" 一行 pointer，不写 ROUND 12-14。

---

## 三、可选的下一轮验证（按 ROI）

| 优先 | 任务 | 工作量 | 价值 |
|---|---|---|---|
| **高** | **F3 全 cohort 跑**（兑现幅度符号翻转，反共识赌注主载荷）| 1-2 天 | F6 单 cohort 验证后的 logical next step |
| **高** | **F11 corpus dump 已完成** + GPT 5 routine（LLM role classifier）| GPT 那边在做 | F11 LLM 链路 |
| 中 | F6 在 type=4 预增子样本内部跑 SUE 双因子（n=12.6K）| 半天 | 严格判定 F6 vs PEAD-on-预增 非冗余 |
| 中 | F10 v5：≤±1pp 极严 match + 行业去均值 | 半天 | 抗 over-matching 稳健性 |
| 中 | F1 v5：行业去均值 + 一字板 filter | 半天 | F1 v4 diff 是否仍稳 |
| 中 | F4 probe（同花顺概念成员 PIT 数据是否在 cache）| 1 天 | 决定 F2/F4/F5 链可行性 |
| 低 | F10 × F1 × F6 三个 reversal 信号交叉 cohort | 1 天 | 看是否叠加 |
| 低 | F10 v2 LLM 严格重做 substring 分类 | 1 天 | other 30% 漏检 |

---

## 四、F11 LLM routine 链路状态（GPT 那边在做）

- ✅ **Corpus dump 已完成**（2018-01 ~ 2019-06，6,600 records pushed to git）
- ⏸ GPT 那边在写：R2 frozen prompt + 5 routine yaml
- ⏳ **数据约束已告知 GPT**：
  - 窗口 2018-2019 H1 (cache 限制，不是 2022-2023 AI 行情)
  - 澄清 subclass pool 只 309 events（其中 300 全取了）
  - title-only，无 content

---

## 五、长期：v1 邮件交付

所有 F 卡片验证 + Deliverable 重写完成后：
- 打包 tarball
- 邮件 mentor B
- 标注哪些 validated, 哪些 unvalidated

---

## 当前 batch 状态总结

| Feature | Sanity | v1 | v2 | v3+ | Deliverable 回写 |
|---|---|---|---|---|---|
| F1 | n/a | ✅ | ✅ (v4) | — | ❌ pending |
| F6 | ✅ | ✅ | enum 解码 ✅ | — | ❌ pending (需重写) |
| F10 | ✅ | ✅ | ✅ matched | ✅ v3 + v4 capacity/split-half | ❌ pending (完全重写) |
| F11 corpus | ✅ dump | — | — | — | — (GPT 在做 LLM 链) |
| F3 | — | — | — | — | — (next) |
| F2/F4/F5 | — | — | — | — | — |
| F7-F9/F12/F13 | — | — | — | — | — |

---

## 决策时点

**用户可以一句话告诉我做哪条**：
- "回写 F1 卡片" → 做 A
- "回写 F6 卡片" → 做 B
- "回写 F10 卡片" → 做 C
- "全部回写 + 重出 PDF" → 做 A+B+C+D+E+F（约 2.5 小时）
- "继续 F3 验证" → 做三的第一项
- "F10 v5 严严" → 做三的 F10 v5
- "先什么都不动，等下一个 idea" → 我等着

不再 push 一个个动作往前走，等你 batch 决策。
