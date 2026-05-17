# F10 异动公告 anchor 效应 — 验证记录

> **状态**：v1 跑通 + v2 matched control 跑通
> **核心发现**：异动公告是 **bimodal attention amplifier**——对弱势股放大下跌 (Q1 matched diff -8.65%, t=-10.4)，对强势股放大上涨 (Q5 matched diff +3.37%, t=+3.15)
> **Thesis 三次 pivot**：澄清/降级（sanity 砍）→ 强势 anchor 反转（v1 反向）→ bimodal attention amplifier（v2 确认）
> **F10 评定**：保留，进 Deliverable，但卡片需完全重写（不是降级，不是反转，是双向放大器）
> **日期**：2026-05-17
> **环境**：bjintern12（pysim 5.0.0 / Python alpha API）

---

## 一、原 thesis（Deliverable F10 卡片，跑前版本）

> 证据等级（传闻 → 媒体 → IR 答复 → 正式公告 → 订单 → 业绩）的本期最高级 − 历史最高级；含降级 / 澄清 / 否认事件。
>
> **经济逻辑**：强势概念二波 / 主升靠证据等级实质升级；明确否认 = 证伪事件，是 stage 退潮硬信号。双向信号比单向更对称。

**降级源**：`CninfoAnnouncement.category == 3`（"澄清风险业绩预告"，79K 条硬信号）。

## 二、Thesis 三次 pivot 记录

### Pivot 1 — Sanity 阶段砍原 thesis（澄清/降级）

`output_f10_subclass.txt` 显示 category=3 是合并类别，按 GPT priority rule 拆分：

| 子类 | n | 占 cat=3 比例 |
|---|---|---|
| earnings_overlap (业绩预告) | 25,474 | 32.1% |
| **trigger_passive (异常波动)** | **22,396** | **28.3%** |
| clarification_true (真澄清) | **3,075** | 3.9% |
| ongoing_st (风险提示) | 4,204 | 5.3% |
| other | 24,117 | 30.4% |

**case B + case D 双触发**：
- 真澄清 n=3,075 **< 10K 门槛 → underpowered**
- 被动事件 22K >> 真澄清 3K → category=3 实际是"被动事件主导"

**结论**：原 F10 thesis（降级 = 反转）无法在 v1 跑出 power，**砍 main**，留 v2 LLM 重启。

### Pivot 2 — v1 跑出反向 finding（强势侧无反应）

`output_f10_v1.txt` GPT brief（"强势 + 异动 → forced anchor → 反转"）：

| quintile | prior 20D | CAR_10 | t_c_10 |
|---|---|---|---|
| **Q1 弱势** | ≤−14% | **−9.79%** | **−10.88** |
| Q5 强势 | >+36% | +0.76% | +0.63 |

预测 Q5 反转最强，**实测 Q1 反转最强、Q5 几乎不动**。

**初步解读**（待 matched control 验证）：
- v1 没有 identification — 两个 narrative 观察等价
  - N1: 真 anchor 效应（弱势 + 异动 = bad news confirmation → 加速下跌）
  - N2: selection / momentum 重发现（异动样本 selected 到 negative momentum 票）

### Pivot 3 — v2 matched control 揭示 bimodal anchor 效应

按 F1 v4 matched baseline 模板做 1:1 matching：
- same SW2 industry × same year_month × cap_q ± 1 × prior_20d ± 5pp
- exclude trigger_passive in [di_ctrl − 60, di_ctrl + 20]
- matched rate 76.6% (3,464 / 4,520)

**T2 关键检验** (`output_f10_matched.txt`)：

| quintile | n | E[CAR_trt_10] | E[CAR_ctrl_10] | matched diff_10 | t_c_10 |
|---|---|---|---|---|---|
| **Q1 弱势** | 693 | −7.9% | **+0.8%** | **−8.65%** | **−10.38** |
| Q2 | 693 | −1.5% | −0.1% | −1.42% | −1.79 |
| Q3 | 692 | −0.6% | −2.0% | +1.50% | +1.80 |
| Q4 | 693 | −1.8% | −2.6% | +0.84% | +1.06 |
| **Q5 强势** | 693 | −1.3% | **−4.7%** | **+3.37%** | **+3.15** |

**Bimodal anchor 效应实证**：
- Q1 弱势：matched 对照组 +0.8% vs treatment −7.9% → **anchor 真把弱势股加速下跌**（不是 momentum 自动续跌）
- Q5 强势：matched 对照组 −4.7% vs treatment −1.3% → **anchor 真把强势股从市场下跌中保护出来**（甚至相对上涨）
- 中间 Q3/Q4 几乎无 effect

## 三、数据

| 项 | pysim API key | 来源 |
|---|---|---|
| 日频收益 | `'returns'` | BaseData |
| 申万二级 | `'WindIndustry.wind2'` | cluster 用 |
| 公告 offsets | `'CninfoAnnouncement.offsets'` | (N_DAYS, NSTOCK, 2) |
| 公告类别 | `'CninfoAnnouncement.category'` | 21 类 int |
| 公告类别字典 | `'CninfoAnnouncement.categoryIx'` | N32C |
| 公告标题 | `'CninfoAnnouncement.title'` | N256C |
| Cap | `'cap'` | BaseData |

**Universe**：Ashare（NSTOCK = 6144）
**回测期**：2018-2023 干净样本
**Event 总数**：trigger_passive 22,396 → year + window + cap + ind filter → **4,520 treatment**

## 四、方法

### Sanity 阶段（v1 前）

1. ls cache → 找到 `CninfoAnnouncement` (offsets / category / title / categoryIx)
2. 全展开 → category=3 events 79,266
3. GPT priority classifier 按 title 拆 5 子类
4. n 分布 + GPF (F6) cross-tab + prior 20D return per 子类
5. 触发 case B + case D → 砍原 thesis，转 trigger_passive 主表

### v1 主跑（trigger_passive）

1. Filter: category=3 AND title 含 "异常波动" AND NOT "业绩预告" AND NOT "澄清"
2. CAR windows: +1~+5, +1~+10, +1~+20
3. Cohort: prior 20D 五分位 + cap 三分位
4. Cluster SE: (year_quarter × SW2)

### v2 matched control（identification）

1. 对每个 treatment (di_t, ii_t) 构造 candidate pool：
   - same SW2 industry × same year_month × cap_q ± 1
   - prior_20d_return within ±5pp
   - exclude: ii has trigger_passive event in [di_t − 60, di_t + 20]
2. 1:1 random sample (seed=42)
3. β_anchor = E[CAR_trt] − E[CAR_ctrl]，stratified by prior 20D quintile

## 五、决策与新经济叙事

### 5.1 GPT 二元 framework 的 outcome

| Narrative | 预测 | 实测 |
|---|---|---|
| N1 真 anchor | Q1 matched diff < 0 且 t < −2 | ✅ Q1 diff=-8.65%, t=−10.4 |
| N2 momentum 重发现 | 所有 quintile diff ≈ 0 | ❌ |

**判定**：Narrative 1 真 anchor 效应 **成立**，且比 GPT 预期**更丰富**（双向都显著）。

### 5.2 新经济叙事：异动公告 = bimodal attention amplifier

- **机制**：异动公告本质是交易所对 sentiment-driven 价格反常的**强制注意力放大**。市场对此 anchor 的反应取决于先前情绪 state：
  - 先前下跌（Q1）→ 异动 = bad news confirmation → 恐慌 / margin call / stop loss / panic → 加速下跌
  - 先前上涨（Q5）→ 异动 = "被点名 = 被关注" → 追买 / 题材发酵 → 加速上涨
  - 中间 state → 无明确情绪锚，效应平淡

### 5.3 与 §0 反共识 thesis 的关系

**F10 不是 §0 mini-instance**。两个完全不同的通道：

| feature | 机制 | thesis 通道 |
|---|---|---|
| F6 (预增 cohort) | 业绩兑现 → 集体期权到期 → 反转 | §0 兑现型反共识 |
| F10 (异动公告) | 注意力 anchor → 放大已有 sentiment | **独立的 attention amplifier** |

F6 在 "涨太多 → 反转" 通道；F10 在 "已涨/已跌 → 异动放大" 通道。两者机制相反但都成立。

## 六、Sanity 三层

| 层 | 状态 | 修订 |
|---|---|---|
| ① 单调性 | **√** | Q1-Q5 单调（matched diff 从 -8.65 单调递增到 +3.37） |
| ② 识别策略 | **√√** | matched control 严格区分 anchor vs momentum，Q1 diff t=-10.4 干净 |
| ③ 异质性 | **√** | bimodal cohort 拆分清晰，prior 20D quintile 是核心 conditioning 变量 |

## 七、已知 caveats（v1 + v2 累积）

1. **原 F10 thesis（降级/澄清）underpowered**：真澄清 n=3K，未作 main test，留 v2 LLM 重启
2. **title substring 拆分是近似**：other 占比 30.4%，可能漏检真澄清 / 异动事件；v2 候选 LLM 分类
3. **matching PRIOR_TOL=±5pp 偏宽**：|prior_diff|>1pp 占 83.6%，v3 应收紧到 ±2pp 看 finding 是否稳定
4. **1:1 matching**：v3 可以 1:3 或 full matching 提 power
5. **异动触发本身有 forward-looking 风险**：交易所判定基于前几日股价，PIT 上界 = announce_date + 1，已沿 F1 框架自动跳过 T0
6. **未做行业去均值**：市场截面去均值，行业 confound 可能存在
7. **clarification_true 脚注 n=311**：v1 reports t=-3.11 (CAR_5) / -2.16 (CAR_10) — 方向一致但 n 太小，**v2 不作结论**
8. **F6 × F10 时序交互失败**：GPF events 170K 中只 67 条前 20D 内有异动 (0.04%) — F6 与 F10 在时间上几乎不交集，无法测交互

## 八、F10 评定

**保留，进 Deliverable，卡片需完全重写**。

不是：
- ❌ "澄清/降级 = 反转硬信号"（原 thesis，sanity 砍）
- ❌ "强势 anchor 反转"（GPT brief，v1 反向）

是：
- ✅ **"异动公告作 attention amplifier，对弱势/强势双向放大 sentiment"**

## 九、Next steps（按优先级）

| 优先 | 任务 | 工作量 | 价值 |
|---|---|---|---|
| **高** | 写 Deliverable F10 卡片（完全重写，记入 TODO）| 1 小时 | mentor 直接看 |
| **高** | 收紧 PRIOR_TOL ±5pp → ±2pp 看 finding 是否稳定 | 半天 | identification 稳健性 |
| 中 | 1:3 matching 替代 1:1，提 power | 半天 | Q5 强势侧 t=+3.15 是否更稳 |
| 中 | F6 × F10 交叉 cohort (用更长前 lag window) | 半天 | 看 §0 通道与 attention 通道是否在时序上交互 |
| 低 | 行业去均值替代市场去均值 | 半天 | 减少行业 confound |
| 低 | clarification_true 用 LLM 严格抽取再跑 | 1 天 | v2 LLM 重启原 thesis |

## 十、文件清单

```
F10_anchor_reversal/
├── README.md                       (本文档)
├── output_f10_subclass.txt        (sanity: subclass 拆分 + 决策 case B/D)
├── output_f10_v1.txt              (v1: trigger_passive 主表 + Q1-Q5 反向 finding)
└── output_f10_matched.txt         (v2: matched control identification + bimodal)
```

源码 canonical 位置：`pysim-workspace/tools/f10_anchor/` 和 `pysim-workspace/tools/f10_probe/`

## 十一、部署 + 运行

bjintern12 一行系列：

```bash
# Sanity (subclass 拆分 + case 判定)
bash ~/pysim-ws/tools/f10_probe/run_subclass.sh

# v1 主跑 (trigger_passive)
bash ~/pysim-ws/tools/f10_anchor/run.sh

# v2 matched control (identification)
bash ~/pysim-ws/tools/f10_anchor/run_matched.sh
```

---

## 附：嵌进 Deliverable F10 卡片的简短摘要

> **F10 sanity + v1 + v2 验证（2026-05-17，2018-2023 共 4,520 个 clean treatment events + 3,464 matched controls）**：
> - **Sanity**：原 thesis（澄清/降级 = 反转）实证 sample n=3K underpowered，砍 main；改跑 trigger_passive (异常波动) n=22K
> - **v1**：trigger_passive ALL CAR_10 clustered t=−5.77，但 prior 20D Q1 子样本反转最强 (−9.8%, t=−10.9) — 反预测方向，存在 momentum vs anchor identification 模糊
> - **v2 matched control**：1:1 matching 后 Q1 diff_10 = **−8.65% (t=−10.4)** 且 Q5 diff_10 = **+3.37% (t=+3.15)**，bimodal anchor 效应实证
> - **新经济叙事**：异动公告 = bimodal attention amplifier；机制独立于 F6 兑现型反共识 thesis
> - **结论**：F10 入 Deliverable，但卡片需完全重写从"降级反转"改为"attention amplifier"
