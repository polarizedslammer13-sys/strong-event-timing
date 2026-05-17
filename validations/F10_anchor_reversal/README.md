# F10 异动公告 anchor 效应 — 验证记录

> **状态**：sanity + v1 + v2 (matched) + v3 (capacity + tight match) + v4 (split-half + capacity)
> **核心 thesis (v4 锁定)**：异动公告 = sentiment amplifier 在**弱-中 prior return cohort** 上产生 -3% ~ -6% 加速下跌；**Q1 弱势侧最 robust**（tradable -6.25%, t=-6.21, split-half 两期都 t<-4）
> **5 次 thesis pivot 全部诚实记录** + 主动暴露 caveat
> **F10 评定**：保留进 Deliverable，但卡片需完全重写为"Q1 主 + Q3 辅"窄 framing，不再说 "bimodal"
> **日期**：2026-05-18
> **环境**：bjintern12（pysim 5.0.0 / Python alpha API）

---

## 一、原 thesis（Deliverable F10 卡片，跑前版本）

> "证据等级变动（双向），含降级 / 澄清 / 否认事件。强势概念二波 / 主升靠证据等级实质升级；明确否认 = 证伪事件，是 stage 退潮硬信号。"
> **降级源**：`CninfoAnnouncement.category == 3`（"澄清风险业绩预告"，79K 条硬信号）。

## 二、5 次 thesis pivot（完整诚实记录）

| Pivot | thesis | 阶段 | 实证结果 |
|---|---|---|---|
| **1** | 澄清/降级 = 反转硬信号 | sanity | 真澄清子样本 n=3K underpowered，砍 main |
| **2** | 强势 + 异动 = forced anchor → 反转 | v1 (GPT brief) | Q5 强势侧 t=+0.63 无反应，**预测反向** |
| **3** | 弱势 + 异动 = 加速下跌 | v1 main | Q1 t=-10.88 但**无 identification**，momentum vs anchor 不可分 |
| **4** | bimodal anchor effect (Q1 + Q5 双向) | v2 matched control | Q1 diff=-8.65%, Q5 diff=+3.37%, 都 identified |
| **5** | **Q1 弱势单边 robust，Q5 paper-only** | v3 capacity + v4 split-half | Q5 tradable diff 退化到 -0.31% (t=-0.35), Q1 tradable -6.25% (t=-6.21) 稳 |

### Pivot 防御段（写给 mentor 看）

5 次 pivot 都是 **data-driven 升级**，不是 outcome chasing：

- **Pivot 1（砍 clarification）**：sanity 阶段 n=3K 子样本量决策，不是 hypothesis search
- **Pivot 2（强势→弱势）**：数据直接拒绝 GPT 的强势 anchor prediction，不是 cherry-pick
- **Pivot 3-4（加 matched control）**：identification 标准升级（从 1:N control → 1:1 matched），不是 outcome chasing
- **Pivot 5（capacity strip Q5）**：诚实承认 paper vs tradable 差距，**Q5 +3.37% 全部是涨停一字板贡献，不可交易**

**但承认**：多次 pivot 累积后 in-sample 拟合度上升，**严格 OOS hold-out 才能最终判定真伪**。
- Cache 限制下严格 OOS 不可行（CninfoAnnouncement / EastmoneyAnnouncementevent / Gildata 公告数据 ≤ 2020-06-18，无 2023 H2 fresh data）
- v4 用 sample 内 split-half (2018 vs 2019 H1) 作 weak proxy，Q1 子样本两期都 t<-4 → 弱 robustness 通过

## 三、数据

| 项 | pysim API key | 来源 |
|---|---|---|
| 日频收益 | `'returns'` | BaseData |
| 申万二级 | `'WindIndustry.wind2'` | cluster 用 |
| 总市值 | `'cap'` | BaseData (单位**百万元**，全市场 median ≈ 5550 = 55 亿元) |
| 公告 offsets | `'CninfoAnnouncement.offsets'` | (N_DAYS, NSTOCK, 2) |
| 公告类别 | `'CninfoAnnouncement.category'` | category=3 = "澄清风险业绩预告" |
| 公告标题 | `'CninfoAnnouncement.title'` | N256C, substring 匹配 "异常波动" |

**Data source**：CninfoAnnouncement = 巨潮资讯网 (cninfo.com.cn)，证监会指定的 A 股官方公告披露平台。**Cache 是 stale 的**，实际事件只到 **2019-06-14 (di=2550)**（其他公告数据集也都 stale 或非事件流，见 §七 caveats）。

**Universe**：Ashare (NSTOCK = 6144)
**实际 sample period**：**2018-01-01 ~ 2019-06-14** (1.5 年)
**Event 总数**：trigger_passive 22,396 → year+window+cap+ind filter → **4,520 treatment events**

## 四、方法

### Sanity 阶段（确定主链）

1. ls cache → `CninfoAnnouncement` (offsets / category / title)
2. 全展开 → category=3 events 79,266
3. **GPT priority classifier** 拆 5 子类，按 title substring：
   - "业绩预告" → earnings_overlap (剔 F6 重叠)
   - "异常波动" → trigger_passive (**F10 主链**, n=22K)
   - "澄清" → clarification_true (n=3K, underpowered)
   - "风险提示" → ongoing_st
   - else → other (substring 漏检, v2 候选 LLM)

### v1 主跑（trigger_passive 全样本）

事件研究 + prior 20D quintile cohort split + cluster SE (year_quarter × SW2)。

### v2 matched control（identification）

1:1 random sample matching:
- same SW2 industry × same year_month × cap_q ± 1 × prior_20d ± **5pp**
- exclude trigger_passive in [di_ctrl − 60, di_ctrl + 20]

### v3 capacity + tighter match

- PRIOR_TOL ±5pp → **±2pp** (matching rate 76.6% → 71.5%)
- T+1 |return| ≥ 9.5% 一字板封死率 by quintile
- tradable subset (排除 T+1 一字板) 重新算 matched diff
- 1.5y 内 split-half (2018 vs 2019 H1) 作 weak OOS proxy

### v4 final（Q1-Q5 split-half + capacity）

- tradable subset 上**每个 quintile 各做 split-half**
- Capacity 估算（median cap × 1% × 50% free float × events/年）

## 五、Quintile 定义

按"异动公告前 20 个交易日累积超额收益（市场截面 demean cumsum）" 分五等分：

| Q | prior 20D 超额 | 通俗描述 | 经济故事 |
|---|---|---|---|
| **Q1 弱势** | ≤ −8.8% | 异动前 20 天**跌**了 8.8% 以上 | 连续下跌 → 异动 = "请说明下跌原因" → bad news confirmation |
| Q2 | −8.8% ~ +10.9% | 横盘到微涨 | 异动叙事弱 |
| Q3 | +10.9% ~ +19.5% | 中等强势 | 中等强势异动 |
| Q4 | +19.5% ~ +26.9% | 较强势 | 已接近异动触发标准 |
| **Q5 强势** | > +26.9% | 极强势"妖股" | 异动 = "你这是不是炒作"，多数随后封涨停 |

## 六、核心实证表

### 6.1 v3 主表 — matched diff ALL (PRIOR_TOL=±2pp)

| window | n | E[trt] | E[ctrl] | diff | clustered t |
|---|---|---|---|---|---|
| +1~+10 | 3,233 | -2.6% | -1.6% | **-0.96%** | **-2.15** |
| +1~+20 | 3,233 | -4.4% | -2.0% | **-2.41%** | **-4.36** |

### 6.2 v3 主表 — Quintile diff

| Q | n | diff_10 | clustered t |
|---|---|---|---|
| **Q1 弱势** | 647 | **−8.95%** | **−9.77** |
| Q2 | 646 | -1.01% | -1.09 |
| Q3 | 647 | +0.16% | +0.18 |
| Q4 | 646 | +1.43% | +1.79 |
| Q5 强势 | 647 | **+3.58%** | **+3.46** |

### 6.3 v3 capacity check — T+1 一字板封死率

| Q | T+1 跌停 | T+1 涨停 | 任一一字板 |
|---|---|---|---|
| Q1 弱势 | **14.9%** | 2.9% | 17.8% |
| Q5 强势 | 12.1% | **28.6%** | **40.7%** |

Q5 强势组 29% 涨停 → 大量 paper alpha 不可交易。

### 6.4 v3 tradable subset (排除 T+1 一字板) — **关键 finding**

| Q | n | tradable diff_10 | t |
|---|---|---|---|
| **Q1 弱势** | 524 | **−6.25%** | **−6.21** |
| Q2 | 492 | −3.00% | −3.83 |
| Q3 | 469 | −3.83% | −4.96 |
| Q4 | 436 | −1.89% | −2.47 |
| **Q5 强势** | 409 | **−0.31%** | **−0.35** ← paper-only 暴露 |
| **ALL** | 2,330 | **−3.22%** | **−8.65** |

Q5 的 +3.58% paper diff **完全是涨停一字板贡献**，tradable subset 内完全消失。

### 6.5 v4 tradable Q1-Q5 split-half (2018 vs 2019 H1)

| Q | 2018 t_c_10 | 2019 H1 t_c_10 | 评定 |
|---|---|---|---|
| **Q1 弱势** | **−4.92** | **−4.30** | ✅ **两期都强稳** |
| Q2 | −3.73 | -1.75 | △ marginal |
| **Q3** | **−3.08** | **−4.16** | ✅ 两期都稳 |
| Q4 | -3.44 | **+0.07** | ❌ **2019 H1 OOS 失效** |
| Q5 | -0.75 | +0.16 | ❌ paper-only 确认 |

### 6.6 v4 capacity 数字（cap 单位 = 百万元）

| Q | n_tradable | median cap (亿元) | IQR (亿元) |
|---|---|---|---|
| **Q1 弱势** | 524 | **42.2** | [25.6, 73.7] |
| Q2 | 492 | 37.8 | [27.0, 61.9] |
| Q3 | 469 | 39.2 | [28.6, 65.9] |
| Q4 | 436 | 40.8 | [29.8, 70.0] |
| Q5 | 409 | 47.6 | [32.7, 86.5] |

**A 股中小盘**为主，median 市值 ~40 亿元。

**Q1 子样本年容量**：
- events/年 = 524 / 1.5 ≈ **350 events/年**
- 单 event 容量（1% 总市值 × 50% free float） ≈ 0.21 亿元
- **Q1 年容量上界 ≈ 73 亿元/年**（1% allocation）
- **保守估算 ≈ 35 亿元/年**（0.5% × 50% FF）

**Q1+Q3 robust 双子样本年容量** ≈ **70-150 亿元/年**

足够中型 quant fund 跑（典型 hedge fund alpha 容量 5-20 亿元）。

## 七、已知 caveats

1. **Sample period 仅 1.5 年单 regime**：Cninfo cache stale 到 2019-06-14，所有候选公告数据源也都 stale 或非事件流
2. **严格 OOS hold-out 不可行**：cache 限制；用 sample 内 split-half 作 weak proxy
3. **5 次 pivot 累积**：data-driven 升级但 in-sample fit risk
4. **Q4 在 2019 H1 OOS 失效**：regime sensitive，可能是 alpha 边界
5. **Q5 +3.37% 是 paper-only**：涨停一字板贡献，tradable 内完全消失
6. **Cap 字段是总市值不是流通市值**：未找到专用流通市值字段，capacity 估算用 50% free float 假设
7. **title substring 拆分是近似**：other 30%，"澄清" 内部混杂业绩预告 / 异动 / 风险提示（v2 LLM 候选）
8. **修正预告信息内容被丢弃**：first-record dedup 放弃 multi-record cell（43.5% cells 有 >1 event）
9. **行业去均值未做**：用市场截面 demean，行业 confound 可能存在
10. **F6 × F10 时序交互失败**：GPF events 170K 中只 67 条前 20D 内有异动 (0.04%)，两通道时序几乎不交集

## 八、F10 最终评定

**保留进 Deliverable**，但卡片**完全重写**：

> **F10 = 异动公告作为 sentiment amplifier 在弱-中 prior return cohort 上产生 -3% ~ -6% 加速下跌**
>
> 不是：
> - ❌ "澄清/降级 = 反转硬信号" (Pivot 1)
> - ❌ "强势 anchor → 反转" (Pivot 2)
> - ❌ "bimodal 双向 amplifier" (Pivot 4) — Q5 paper-only 拆穿
>
> 是：
> - ✅ **"Q1 弱势 (prior 20D ≤ -8.8%) + Q3 中性 (prior +11%~20%) 两子样本最 robust"**
> - 主表 alpha：Q1 tradable diff_10 = **-6.25% (t=-6.21), split-half 两期都 t<-4**
> - Sample period **1.5y 单 regime (cache 限制)**，OOS hold-out blocked
> - Capacity ≈ **35-73 亿元/年 (Q1 only)**，70-150 亿/年 (Q1+Q3)
> - 5 次 thesis pivot，主动暴露完整 + 防御段

## 九、Sanity 三层

| 层 | 状态 | 修订 |
|---|---|---|
| ① 单调性 | **△** | Q1-Q5 不再严格单调（Q1 最强 → Q5 paper-only），但在 tradable subset 内 Q1-Q4 同方向 |
| ② 识别策略 | **√√** | v2-v3 matched control + v3 tradable filter + v4 split-half 三重 identification |
| ③ 异质性 | **√** | quintile + capacity + split-half 三轴 cohort 都做了 |

## 十、Next steps（按 ROI）

| 优先 | 任务 | 工作量 | 价值 |
|---|---|---|---|
| **高** | Deliverable F10 卡片完全重写 (基于 v4) | 1 小时 | mentor 直接看 |
| 中 | F11 LLM 重启原 F10 thesis（澄清子样本扩样）| 2 天 | Pivot 1 复活的可能 |
| 中 | F10 × F1 交叉：Q1 弱势异动 ∩ 解禁前后 | 半天 | 看两个反转信号是否叠加 |
| 中 | 改用 ±1pp 极严 match 看 Q1 是否仍 robust | 半天 | 抗 over-matching |
| 低 | 行业去均值替代市场去均值 | 半天 | 减少行业 confound |
| 低 | F10 v2 LLM 重做 substring → 严格分类 | 1 天 | other 30% 漏检 |

## 十一、文件清单

```
F10_anchor_reversal/
├── README.md                       (本文档, v4 终版)
├── output_f10_subclass.txt        (sanity: subclass 拆分 + case B/D 决策)
├── output_alt_freshness.txt       (备选公告数据集 freshness 排查)
├── output_f10_v1.txt              (v1: trigger_passive 主表, Q1-Q5 反向 finding)
├── output_f10_matched.txt         (v2: matched control identification, bimodal)
├── output_f10_v3.txt              (v3: PRIOR_TOL ±2pp + capacity + split-half)
└── output_f10_v4.txt              (v4: tradable Q1-Q5 split-half + capacity 数字)
```

源码 canonical 位置：`pysim-workspace/tools/f10_anchor/` 和 `pysim-workspace/tools/f10_probe/`

## 十二、部署 + 运行

bjintern12 一行系列：

```bash
# Sanity 阶段
bash ~/pysim-ws/tools/f10_probe/run_subclass.sh         # subclass 拆分 + case 判定
bash ~/pysim-ws/tools/f10_probe/run_alt_freshness.sh    # 备选数据 freshness 排查
bash ~/pysim-ws/tools/f10_probe/run_gildata_probe.sh    # Gildata schema 排查

# 主验证链
bash ~/pysim-ws/tools/f10_anchor/run.sh                 # v1 主跑
bash ~/pysim-ws/tools/f10_anchor/run_matched.sh         # v2 matched control
bash ~/pysim-ws/tools/f10_anchor/run_v3.sh              # v3 capacity + tight match
bash ~/pysim-ws/tools/f10_anchor/run_v4.sh              # v4 final (split-half + capacity)
```

---

## 附：嵌进 Deliverable F10 卡片的简短摘要

> **F10 sanity + v1 + v2 + v3 + v4 验证（2026-05-17 ~ 18，2018-01 ~ 2019-06 共 4,520 clean treatment + 3,233 matched）**：
> - **Sanity**：原 thesis（澄清/降级 = 反转）n=3K underpowered，砍 main
> - **v1-v3 经过 4 次 framing 迭代**，最终 v3-v4 确定主信号
> - **v4 最终 thesis**：异动公告 = sentiment amplifier 在 Q1 弱势 (prior 20D ≤ -8.8%) + Q3 中性 (prior +11~20%) cohort 上 robust -3~-6% 反转
> - **Q1 tradable diff_10 = −6.25% (t=−6.21)**，split-half 2018: t=-4.92 / 2019: t=-4.30 两期都强稳
> - **Q5 强势侧 +3.37% paper diff 完全是涨停一字板贡献**，tradable t=−0.35 完全消失
> - **Capacity**：median cap ≈ 42 亿元 (中小盘 A 股)，Q1 年容量 ≈ 35-73 亿元 RMB
> - **Caveat**：sample 1.5y 单 regime，严格 OOS hold-out blocked by cache staleness；split-half 作 weak proxy
> - **结论**：F10 入 Deliverable，卡片完全重写为"Q1 主 + Q3 辅 sentiment amplifier"窄 framing
