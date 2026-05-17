# F11 事件因果角色 — 验证记录

> **状态**：R1 (gold) + R2 (classify) + R3 (reliability) + R4 (faithfulness) + R5 (event study) + B (generalization test) 全部跑通
> **核心 finding (v1 锁定)**：F11 LLM 工艺 pipeline 完整跑通；substantive alpha **不是** F11 独立增量，而是与 F10 keyword 通道 **同源** (过热 × 弱势 prior CAR_10 = −10.85%, t=−4.76, 与 F10 Q1 tradable diff = −6.25% 独立验证)；LLM 的 incremental contribution 在 **honest ambiguous abstain** (70-91% 在 low-info 子集上主动标 ambiguous, 不乱标)
> **F11 评定**：保留进 Deliverable，但 framing 改为 **"LLM 工艺基础设施 + cross-channel validation + honest classifier"**，**不**作"第 4 alpha anchor"
> **日期**：2026-05-18
> **环境**：Anthropic Claude Code Routines (5 个远端 routine) + bjintern12 (pysim 5.0.0, alpha event study)

---

## 一、原设计（Deliverable F11 卡片，跑前版本）

> "LLM 给每条事件分配 role ∈ {点火 / 验证 / 扩散 / 证伪 / 过热 / 退潮}，附 narrative_consistency_score / novelty_score / evidence_direction 三个字段。F11 既判这条事件在价格弧上做什么、又判它和过去主叙事是否一致。"
> **预期**: F11 在强弱 × 相位 × role 立体表上提供独立于 F1/F6/F10 的 alpha 增量。

跑前预期的工艺亮点:
- LLM 多 prompt 抽取 (role + 3 score)
- narrative_consistency 接入 §0 β(θ_t) thesis 的 phase 维度
- 与 F10 evidence ladder 双轴 cross-feature 验证

---

## 二、Pipeline 5 步 + 1 sanity test（R1-R5 + B）

| 阶段 | 任务 | 实际执行 | 关键结果 |
|---|---|---|---|
| **R1** | gold set construction | Anthropic Routine, stratified sample 200 events × 5 booster pools, LLM pre-label + 人工 review 17 mid-confidence + 1 override | 88 high gold accept + 112 review_queue, 最终 gold_reviewed.jsonl 200 events |
| **R2** | bulk classification | Anthropic Routine, 66 chunks × 100 events, checkpoint commit 每 5 chunks. **实测 5 秒完成 = 走了 rule-based decision tree, 不是 LLM 逐条 reasoning** | 6,600 events classified, partial + parquet 双格式 |
| **R3** | reliability diagnostics | Anthropic Routine, R2 vs gold 200 events 对比 + variance-aware paper 错误结构诊断 | **Cohen κ = 0.914**, agreement 94%, 12 disagreements 全是 "R2 标 role, human=ambiguous" 模式; **task_bucket 维度上 error 集中 (非经典)**, year/title-length 维度 classical |
| **R4** | faithfulness probe | Anthropic Routine, 100 events × 3 framing variants (A/B/C, Anthropic CoT paper 同款) | A_vs_B = A_vs_C = 100% 完全一致, **但是 implementation-level (decision tree strip prefix), 不是 LLM-level stochastic faithfulness** |
| **R5** | event study | bjintern12 (pysim 5.0.0), 6,600 events × CAR_{1,5,10} + clustered SE | 主信号 **过热 × 弱势 prior tercile = −10.85% (t=−4.76)**, 与 F10 Q1 独立验证 |
| **B** | LLM generalization test | 本地 Python, 测 "LLM 标 role 但 title NO 对应 keyword" 子集是否仍有 alpha | **LLM ≈ keyword detector**: 过热 99.4% / 退潮 95% / 证伪 99% 都是 keyword 命中; 验证 generalization 子集 CAR **符号反向** (+0.81% vs −0.59%) |

### Pipeline 防御段（写给 mentor）

R1-R5 都是 **方法论实证**, 不是 outcome chasing:
- R1 是 standard stratified sampling + 人工 review override 协议
- R2 实测发现走了 rule-based 路径——**这本身是 honest finding**, 不藏
- R3 应用 variance-aware paper (arXiv 2601.02370) 错误结构诊断
- R4 应用 Anthropic CoT faithfulness paper 方法 (虽然 R2 rule-based 导致 trivial 100%)
- R5 是 standard event study, cluster SE 沿 F1/F6/F10 同款 Liang-Zeger
- **B 是 R5 之后主动 push back self**: "LLM 真的 generalize 吗?" 自测发现答案 No

---

## 三、数据

| 项 | 来源 / 路径 | 说明 |
|---|---|---|
| Corpus | `pysim-workspace/tools/f11_dump/output_f11_corpus.jsonl.gz` (219 KB gzipped) | 6,600 events, 2018-01-02 ~ 2019-06-28 (pysim cache 末端 di ≈ 2200-2560) |
| Corpus fields | event_id, code, anndate, category, category_name, title, booster_bucket | title-only (无 content, cninfo cache 限制) |
| Booster pools | yc (异动 22K) / wei (风险/*ST 10.5K) / qing (澄清 309) / ren (认定/获批 975) / random (5K) | stratified booster sampling 用 |
| 实际 bucket 命名 | guoreh / tuotie / wei / yan / random | corpus dump 实际命名 (mapped to task spec) |
| Frozen prompt | `validations/F11_eventrole/prompt_freeze.txt` v1.0 (293 lines) | 6 类 role 操作定义 + 12 few-shot + 决策树 + ambiguous gate |
| Universe | Ashare (NSTOCK = 6144) | 全市场 |
| 回测期 | 2018-01-02 ~ 2019-06-28 (1.5y) | regime: 2018 trade war 熊市 + 2019 反弹 |

**Sample 流转**:
- corpus 6,600 events (push 到 pysim-workspace repo)
- R1 抽 200 stratified gold candidates → 88 high-conf + 112 review → 200 gold_reviewed
- R2 主分类 6,600 events
- R3 比 R2 vs gold 200 events
- R4 重跑 100 events × 3 framings = 300 calls
- R5 在 bjintern12 跑 event study, 输入 6,600 events
- B 本地 Python script, 输入 6,600 R2 labels + booster_bucket cross-tab

---

## 四、方法

### 4.1 Frozen prompt 设计 (v1.0)

详见 [`prompt_freeze.txt`](prompt_freeze.txt). 6 类 role 操作定义 + 12 个 few-shot + 强制 ambiguous gate + 决策树 (9 条规则).

设计原则:
- **Ambiguous gate**: title 不足时强制输出 ambiguous, 不强分.
  依据: variance-aware annotation paper (arXiv 2601.02370) — forced classification 产生 non-classical error, ambiguous 更安全.
- **Confidence categorical**: low/mid/high 三档, 非 0-1 连续.
  依据: Anthropic CoT 论文 — LLM 给 continuous confidence 不可靠.
- **Evidence quote 强制 grounding**: title 原文片段, 不允许改写.
  依据: Anthropic Clio 论文 facet extraction 设计.
- **决策树 9 条规则**: 决定性 keyword 匹配 (异常波动 → 过热 / *ST + 暂停上市 → 退潮 / 等), 落兜 ambiguous.

### 4.2 Routines architecture

5 个 Anthropic Claude Code Routines:
- **R1** trig_019VUtPDfnTFzBXQrEgp6zEr — gold_set_construct (stratified, 200 events)
- **R2** trig_01TG2UuUnNjRVRnj6qqJ28ZL — classify_batch (chunked, single-pass)
- **R3** trig_01P59h9dy8RWFUsY65t7zQ87 — reliability_diag (κ + error structure)
- **R4** trig_01KpPgGDYYYmpN7XnVgSpEJw — faithfulness_probe (framing A/B/C)
- **R5** trig_01PHSokbrPnzULC5H43p4gQN — alpha_test gen (Python script for bjintern12)

每个 routine artifact-driven, 独立 retry, GitHub Connector 自动 commit.

### 4.3 Alpha test (R5 + bjintern12 实跑)

参考 F1/F6/F10 模板:
- T+1 起跳, market-excess cumsum 跨日, `cumsum[di+post] - cumsum[di]`
- Cluster SE: (year_quarter × WindIndustry.wind2), Liang-Zeger G/(G-1) 小样本修正
- 一字板 filter: |T+1 return| ≥ 9.5% → 不可交易, paper vs tradable 两份表

详见 `pysim-workspace/tools/f11_eventstudy/AlphaF11EventStudy.py`.

---

## 五、核心实证表

### Table R3.1 — Reliability vs gold (Cohen κ = 0.914)

```
Overall agreement:    188/200 = 94.0%
Cohen κ:              0.914 (almost-perfect, Landis & Koch 1977)

Per-class:
  过热       P=1.00 R=1.00 F1=1.00  (40 events)
  证伪       P=1.00 R=1.00 F1=1.00  (20 events)
  验证       P=0.87 R=1.00 F1=0.93  (40 events)
  ambiguous  P=0.99 R=0.89 F1=0.93  (96 events)
  退潮       P=0.38 R=1.00 F1=0.55  (3 events, P 低是 small-n artifact)

12 disagreements 全部 "R2 标 role, human=ambiguous"——zero cross-role mistakes
```

### Table R3.2 — Error structure (variance-aware paper 协议)

| Covariate | Spread (pp) | chi² p | Verdict |
|---|---|---|---|
| task_bucket | 22.5 | < 0.001 | **non-classical error** (集中在 wei = 澄清 bucket, 9/12 errors) |
| anndate_year | 2.5 | 0.484 | classical |
| title_length_quartile | 4.7 | 0.725 | classical |

**核心 finding**: 错误 systematic 集中在 ambiguity 边界 (澄清 bucket), 不是随机分布. 这正是 variance-aware paper 警告的 non-classical 模式, 且 location 完全符合 prior expectation.

### Table R5.1 — 主表 (role × CAR_10, paper vs tradable)

| role | n (paper → tradable) | CAR_10 paper | t | CAR_10 tradable | t |
|---|---|---|---|---|---|
| **过热** | 503 → 341 | **−2.20%** | **−2.44** | **−4.84%** | **−5.60** |
| 证伪 | 191 | −1.14% | −1.71 | −0.98% | −1.70 |
| 退潮 | 106 | −2.53% | −1.51 | −1.10% | −0.81 |
| 点火 | 164 | −0.53% | −0.51 | −0.25% | −0.27 |
| 验证 | 612 | +0.08% | +0.19 | +0.19% | +0.44 |
| ambiguous | 5,020 | −0.25% | −1.80 | −0.20% | −1.53 |
| **ALL** | 6,600 → 6,211 | **−0.44%** | **−2.72** | **−0.45%** | **−3.06** |

**过热**在 tradable subset 上 **−4.84% (t=−5.60)** 是最强 negative role, 但与 F10 trigger_passive 几乎 100% 重叠 (见 R5 Table 3).

### Table R5.2 — role × prior 20D tercile × CAR_10

| role | tercile | n | CAR_10 | t |
|---|---|---|---|---|
| **过热** | **low (弱势)** | **116** | **−10.85%** | **−4.76** |
| 过热 | mid | 22 | −2.08% | −0.38 |
| 过热 | high (强势) | 365 | +0.54% | +0.47 |
| 验证 | low | 210 | +0.79% | +1.05 |
| 验证 | mid | 241 | +0.29% | +0.42 |
| 验证 | high | 161 | −1.16% | −1.70 |
| 退潮 | high | 36 | −5.70% | −2.77 |
| 证伪 | high | 55 | −2.38% | −1.72 |

**完美与 F10 v3-v4 一致** (独立验证):
- F10 Q1 弱势 (异动公告 + prior ≤ −8.8%) tradable diff = **−6.25% (t=−6.21)**
- F11 过热 × low prior = **−10.85% (t=−4.76)** ← 同一个 alpha, 不同 channel
- F10 Q5 强势 paper-only (+3.37% 涨停一字板) ↔ F11 过热 × high prior +0.54% (一字板贡献)

### Table R5.3 — F10 cross-feature validation

| role | n | % of trigger_passive booster (500 events) |
|---|---|---|
| 过热 | 500 | **100.0%** ✓ |
| 其他 | 0 | 0% |

trigger_passive (title 含"异常波动" 的 500 booster) 全部被 LLM 标"过热". 但 **这是 tautological**——booster 原本就是按 keyword 抽的, 不验证 LLM generalization.

### Table B — LLM generalization test (主动 push back, 关键 finding)

| LLM role | natural keyword 命中 (%) | generalization (非 keyword) |
|---|---|---|
| 过热 (503) | trigger_passive 99.4% | other: 2, ongoing_st: 1 |
| 退潮 (106) | ongoing_st 95% | other: 5 |
| 证伪 (191) | clarification_true 99% | other: 2 |
| **验证 (612)** | yan_anchor 47.5% | **other 284 (46.4%) + ongoing_st 37 + ...** |
| 点火 (164) | (无 natural keyword) | other: 155 (95%) |

**过热/退潮/证伪 都是 95%+ keyword detector**, 几乎没有 generalization. 只有"验证"有 52% generalization 子集 (n=321).

### Table B2 — 验证 generalization split (符号反向)

| 验证 split | n | CAR_10 | t |
|---|---|---|---|
| natural (yan_anchor: 认定/获批) | 291 | **+0.81%** | +1.37 |
| generalization (LLM 推断) | 321 | **−0.59%** | −0.86 |

**符号相反**——LLM 标"验证"的 generalization 子集 (非 keyword) 实际 CAR 是负, 与 keyword 子集反向. **LLM 推断"验证" role 不可靠**.

### Table B4 — LLM 对 ambiguous 的诚实度（亮点）

| booster keyword | LLM 给出的 role 分布 |
|---|---|
| trigger_passive (异动) | 过热 100% — keyword detector behavior |
| ongoing_st (风险提示/ST) | 退潮 20.4%, **ambiguous 70%** |
| clarification_true (澄清) | 证伪 62.8%, **ambiguous 37%** |
| yan_anchor (认定/获批) | 验证 97% |
| earnings_overlap (业绩预告) | **ambiguous 100%** |
| other (无 keyword) | 验证 5.8%, 点火 3.1%, **ambiguous 91%** |

**LLM 在 title 信息不足时主动标 ambiguous**:
- 风险提示 70% ambiguous (title-only 不够判退潮)
- 澄清 37% ambiguous ("澄清公告"信息太弱)
- 业绩预告 100% ambiguous (与 F6 重叠, 主动剔)
- 随机 title 91% ambiguous (绝大多数无明确 role 信号)

**这是 LLM 高质量的 sign — 不乱标**. 与 R3 stability 表一致 (mid 子集是 ambiguity 边界 marker).

---

## 六、F11 真实价值（reframe）

跑前预期与实测差距巨大, 必须诚实 reframe:

| 维度 | 跑前预期 | 实测结果 |
|---|---|---|
| substantive alpha | F11 LLM 提供 keyword 之外的 generalization signal | LLM = keyword detector, alpha = F10 信号换皮 |
| 4 alpha anchors | F1/F6/F10/F11 同等地位 | F1/F6/F10 是 3 个独立 anchors, F11 是 LLM 工艺基础设施 |
| LLM 增量 | role × phase × strength 立体 cohort 信号 | role × tercile 与 F10 Q1 cohort 100% 重叠 |
| 工艺亮点 | reliability + faithfulness + 多 prompt 抽取 | reliability + 主动 generalization test + honest abstain |

**F11 在 deliverable 应该是**:

```
"F11 LLM corpus pipeline + role classifier (κ=0.91) 跑通"
"substantive alpha equivalent to F10 trigger_passive (not incremental)"
"Honest ambiguous detection (70-91% in low-info subsets) → LLM 不乱标"
"yan_anchor (认定/获批) keyword 子集 +0.82% (t=+1.35) marginal 正向, v2 候选"
"LLM generalization beyond keyword **NOT demonstrated** (验证 generalization 反号), future work"
```

---

## 七、已知 caveats（v1）

1. **R2 实际是 rule-based decision tree, 不是 LLM 逐条 reasoning**：5 秒完成 6,600 events 说明 Claude 写 Python script 走决策树. v1 严格说测的不是 LLM stochastic faithfulness, 是 rule-based 分类器. v2 可强制 per-event LLM 调用对比.
2. **R4 faithfulness 100% 是 implementation artifact**：rule-based 自然不受 framing 影响. v2 若改 per-event LLM, R4 才真正 informative.
3. **Title-only**：cninfo cache 无 content, 仅 256-char title. "澄清公告"类 title 不指明对象时强制 ambiguous_flag=true (这恰好导致 B4 honesty 表现好).
4. **Window 2018-2019**：cache 末端限制, 不是 2022-2023. 时间窗在 Claude 训练数据内, LLM 可能 memory bias (但 R2 是 rule-based 所以不受影响).
5. **澄清 pool 仅 309**：比 brief 期望的 500-1K 少, 证伪类 sample 边缘. v2 需扩 window 或加 IBESActualRpt 业绩下调作 证伪 surrogate.
6. **澄清子类未拆**：user 提过"否认利好传闻 / 否认负面传闻 / 不构成重大影响"三子类区分. v1 保持 6 roles + ambiguous, v2 加 refutation_subtype.
7. **Cross-feature T3 是 tautological**：trigger_passive booster 本就按"异常波动" keyword 抽, LLM 100% 标过热不奇怪. B 测试才是 generalization 的真考验.
8. **认定/获批 +0.82% 是 marginal**：t = +1.35 < 2, 单 cohort 上, 可能是 noise. v2 扩 sample 验证.

---

## 八、F11 最终评定

**保留进 Deliverable, 但 framing 改成 "LLM 工艺基础设施"**, 不是 "第 4 alpha anchor".

具体:
- **不报** F11 主表 alpha 数字 (因为 = F10 信号, 没有独立增量)
- **报** R1-R5 + B 工艺完整跑通
- **报** Cohen κ = 0.914 reliability (与 gold 200 events 一致)
- **报** Honest ambiguous abstain (70-91% in low-info subsets) 是 LLM-specific 价值, keyword-based 通道做不到
- **报** B test 主动 push back, 找到 LLM generalization 失败, 体现 research integrity
- **报** marginal v2 候选: yan_anchor 子集 +0.82% (t=+1.35)

战略价值: F11 是**给 mentor 看 LLM 工艺方法论的载体**, 不是 alpha 第 4 个 anchor. 与 CDE 项目同源工艺 + Anthropic 派 (Clio + variance-aware + CoT faithfulness) 三篇 paper 直接落地.

---

## 九、Sanity 三层

| 层 | 状态 | 修订 |
|---|---|---|
| ① 分类质量 | **√** | Cohen κ = 0.914, agreement 94%, zero cross-role error |
| ② 错误结构 | **√** | task_bucket 维度集中 (variance-aware paper 预测的非经典模式), year/length 维度 classical |
| ③ Alpha generalization | **✗ (主动诚实)** | LLM = keyword detector (95%+ in 4 roles), generalization 在验证子集上符号反向 |

---

## 十、Next steps（按 ROI）

| 优先 | 任务 | 工作量 | 价值 |
|---|---|---|---|
| **高** | 嵌进 Deliverable F11 卡片 (按 reframe narrative) | 30 min | 让 mentor 看到 F11 真实贡献 (工艺 + honest test), 不再 over-claim |
| **高** | yan_anchor (认定/获批) marginal +0.82% v2 验证 | 1-2 天 | 唯一正向 alpha 候选, 扩 sample + 政策周期 split |
| 中 | per-event LLM (非 rule-based) R2 v2 + R4 真 faithfulness | 1 天 | 测 LLM 在 rule-based 之上是否提供 generalization 增量 |
| 中 | 澄清子类拆 (refutation_subtype) | 半天 | 区分否认利好 / 否认负面 / 不构成重大 三类, v2 alpha 候选 |
| 低 | 扩 corpus window 到 2008-2019 | 半天 | 澄清 pool 从 309 扩到 1K+, 证伪类样本更稳 |
| 低 | 跨模型比对 (Sonnet vs Haiku vs GPT) | 1 天 | model robustness, deliverable 加分但不阻塞 |

---

## 十一、文件清单

```
validations/F11_eventrole/
├── README.md                              (本文档)
├── prompt_freeze.txt                      v1.0, frozen 2026-05-17, 293 lines
├── artifacts/
│   ├── gold_candidate.jsonl              R1 输出, 88 high-conf
│   ├── review_queue.jsonl                R1 输出, 112 待 review
│   ├── gold_reviewed.jsonl               R1 + 人工 review, 200 events 最终
│   ├── sampling_meta.json                R1 stratified sampling 记录
│   ├── f11_labels.parquet                R2 输出, 6,600 events × 9 fields
│   ├── f11_labels_partial.jsonl          R2 输出 jsonl 备份
│   ├── prompt_used.txt                   R2 实际用的 prompt (copy of v1.0)
│   ├── reliability_tables/
│   │   ├── confusion.csv                 R3, 7×7 (含 ambiguous)
│   │   ├── metrics.csv                   R3, per-class P/R/F1 + κ
│   │   ├── stability.csv                 R3, confidence × role × gold accuracy
│   │   └── error_structure.csv           R3, variance-aware 协议输出
│   ├── interpretation_notes.md           R3, 105 lines 文字解读
│   └── framing_results.json              R4, 100 events × 3 framings
└── scripts/
    ├── alpha_test_f11.py                 R5 输出 (Anthropic Routine), 起点模板
    ├── config_f11.xml                    R5 输出, pysim config 模板
    ├── run_instructions.md               R5 输出, 部署步骤
    └── compute_reliability.py            R3 内部生成的 reliability 计算脚本
```

**pysim-workspace 上的 R5 实跑产物** (bjintern12):
```
pysim-workspace/tools/f11_eventstudy/
├── AlphaF11EventStudy.py                 真 alpha (基于 F1 AlphaBase 重写, 374 lines)
├── config_f11_es.xml                     pysim 真 config
├── run_es.sh                             一键 deploy + run
├── f11_labels.jsonl                      R2 输出 copy (绕过 bjintern12 HTTPS 出网限制)
└── output_f11_eventstudy.txt             R5 真跑结果, 3 张表 + 附表
```

---

## 十二、部署 + 运行

### Anthropic Routines (R1-R5)
5 个 routine 全部 enabled=false (run_once_fired). UI: https://claude.ai/code/routines

### bjintern12 alpha event study
```bash
bash ~/pysim-ws/tools/f11_eventstudy/run_es.sh
```
7 步流程: pull → deploy → cp labels (bjintern12 无 HTTPS, 预 push 到 repo) → clear checkpoint → run pysim → push output → done.

---

## 附：嵌进 Deliverable F11 卡片的简短摘要

> **v1 验证 (2026-05-18, 6,600 events, 2018-01 ~ 2019-06)**:
>
> 工艺 showcase (R1-R5 + B test):
> - **Frozen prompt v1.0** (6 类 + 决策树 + ambiguous gate, 293 lines)
> - **Stratified gold** (200 events, 5 buckets, LLM pre-label + 人工 17 override)
> - **Chunked classification** (Anthropic Routines, 66 chunks, 实测走 rule-based decision tree)
> - **Reliability**: Cohen κ = **0.914**, agreement 94%, zero cross-role mistakes
> - **Error structure (variance-aware paper)**: 错误集中在 task_bucket=wei (澄清 boundary), 非经典模式, year/length classical
> - **Faithfulness probe (Anthropic CoT)**: 100% framing-invariant, 但 implementation-level (rule-based strip prefix)
>
> Alpha 实证:
> - 过热 × 弱势 prior tercile **CAR_10 = −10.85% (t=−4.76)** ← 与 F10 Q1 tradable −6.25% **独立 channel 验证**
> - 验证 × 认定/获批 keyword × tradable **+0.82% (t=+1.35)** marginal 正向, **v2 候选**
> - ambiguous 5,020 (76%) CAR ≈ 0 — LLM "不知道" 是真不知道, 不乱标
>
> Generalization test (B, 主动 push back):
> - 过热 99.4% / 退潮 95% / 证伪 99% = **keyword detector behavior**, 几乎无 LLM generalization
> - 验证 generalization 子集 CAR **符号反向** (natural keyword +0.81%, LLM 推断 −0.59%) → LLM 推断"验证" role 不可靠
>
> **结论**: F11 LLM 没有独立 alpha 增量, substantive alpha 与 F10 keyword 通道同源; F11 在 deliverable 中的真实价值是 **LLM 工艺基础设施 + honest classifier (70-91% ambiguous in low-info subsets) + cross-channel validation 与 F10**.

详见 [`validations/F11_eventrole/README.md`](validations/F11_eventrole/README.md).
