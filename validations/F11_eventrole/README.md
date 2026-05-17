# F11 事件因果角色 — 验证记录

> **状态**: v0 setup (routines + prompt freeze 已就位), 待 R1-R5 触发
> **核心方法**: LLM 给 A 股公告 title 分类 role ∈ {点火/验证/扩散/证伪/过热/退潮/ambiguous}
> **showcase 重点**: LLM 工艺 + variance-aware reliability + Anthropic 派 faithfulness probe
> **日期**: 2026-05-18

---

## 一、任务定义

F11 = 给定一条 A 股上市公司公告 title, LLM 分类 role ∈ 6 类 + ambiguous.

输出 role label 接入 §0 β(θ_t) 框架, 在下游 alpha test 阶段测 role × strength × CAR 的预测力.

**与 F1 / F6 / F10 的区别**:
- F1 / F6 / F10 是 structured event-driven alpha (解禁 / 业绩预告 / 异动公告)
- F11 主要 showcase: LLM 工艺 + reliability methodology, alpha test 是附属

---

## 二、数据

| 项 | 来源 | 说明 |
|---|---|---|
| Corpus | `pysim-workspace/tools/f11_dump/output_f11_corpus.jsonl.gz` | 6,600 events, 2018-01 to 2019-06 |
| 字段 | event_id, code, anndate, category, category_name, title, booster_bucket | title-only (无 content) |
| Universe | Ashare | 全市场 |
| Window | 2018-01-02 ~ 2019-06-28 (1.5y, di [2200, 2560]) | cache 末端 2019, 不是 2022-2023 |
| Stratified booster pools | yc(异动)/wei(风险)/qing(澄清)/ren(认定) + random | 5000 random + 1600 booster = 6600 |

**Sample 流转**:
- corpus 6,600 events (push 到 pysim-workspace repo)
- R1 抽 200 stratified gold candidates
- 人工 review 30-40 low-confidence
- R2 主分类 6,600 events × 3 ensemble = 19,800 calls

---

## 三、方法

### 3.1 Frozen prompt

详见 [`prompt_freeze.txt`](prompt_freeze.txt). 6 类 role 操作定义 + 12 个 few-shot + 强制
ambiguous gate.

设计原则:
- **Ambiguous gate**: title 不足时强制输出 ambiguous, 不强分.
  依据: variance-aware annotation paper (arXiv 2601.02370) — forced classification 产生
  non-classical error, ambiguous 更安全.
- **Confidence categorical**: low/mid/high 三档, 非 0-1 连续.
  依据: Anthropic CoT 论文 — LLM 给 continuous confidence 不可靠.
- **Evidence quote 强制 grounding**: title 原文片段, 不允许改写.
  依据: Anthropic Clio 论文 facet extraction 设计.

### 3.2 Ensemble

R2 主跑 temp=0.3 × 3 runs vote:
- 3/3 一致 → stability="high"
- 2/3 一致 → stability="mid"
- 3-way split → stability="low" → role_final="ambiguous"

测的是 **stochastic stability**, 不是 prompt sensitivity.

### 3.3 Reliability protocol (variance-aware paper)

R3 输出 4 表:
1. Confusion matrix (gold × LLM)
2. Per-class precision/recall/F1 + Cohen's κ
3. Ensemble stability distribution
4. **Error structure** (核心): P(error | covariate) — 检测 non-classical error

### 3.4 Faithfulness probe (Anthropic CoT paper)

R4 对 100 events 加 framing prefix 重跑:
- Variant A: 无 framing (control)
- Variant B: "[过去 20 天上涨 30% 以上]" prefix
- Variant C: "[过去 20 天下跌 15% 以上]" prefix

测一致率. < 90% → LLM 受 framing 影响, label 不基于 title 本身.

### 3.5 Downstream alpha test (R5)

生成 Python script 给用户 bjintern12 跑:
- Table 1: role × CAR_{1,5,10}
- Table 2: role × strength tercile × CAR_10
- Table 3: F11 × F10 trigger_passive 交叉验证

---

## 四、结果

### 4.1 R1 Gold set construction
*待 R1 触发*

### 4.2 R2 主分类
*待 R2 触发*

### 4.3 R3 Reliability tables
*待 R3 触发, 4 表 + interpretation_notes.md*

### 4.4 R4 Faithfulness probe
*待 R4 触发*

### 4.5 R5 Alpha test
*待 bjintern12 跑*

---

## 五、Caveats (v1)

1. **Title-only**: cninfo cache 无 content, 仅 256-char title.
   "澄清公告" 类 title 不指明对象时强制 ambiguous_flag=true.
2. **Window 2018-2019**: cache 末端限制, 不是 2022-2023.
   regime 含 2018 trade war 熊市 + 2019 反弹, 多样性 OK,
   但**时间窗在 Claude 训练数据内, LLM 可能有 memory bias**. R4 faithfulness probe 测.
3. **澄清 pool 仅 309**: 比 brief 期望的 500-1K 少, 证伪类 sample 边缘.
   v2 需扩 window 或加 IBESActualRpt 业绩下调作 证伪 surrogate.
4. **Title substring booster**: 是近似 stratification, 不是严格分类标签.
   实际 role classification 由 LLM 输出决定, booster 仅影响 sampling 概率.

---

## 六、Next steps (v2 候选)

- 抽 3 个额外 score: narrative_consistency / novelty / evidence_direction
- 对 ambiguous events 抓 cninfo PDF 补 content
- F11 × F10 trigger_passive cross-feature 联合 alpha test
- 扩 window 到全 cache (2008-2019) 增加证伪 sample

---

## 七、文件清单

```
validations/F11_eventrole/
├── README.md                  (本文档)
├── prompt_freeze.txt          (v0 prompt, frozen)
├── artifacts/                 (R1-R5 输出 + 用户上传)
│   ├── gold_candidate.jsonl
│   ├── review_queue.jsonl
│   ├── gold_reviewed.jsonl    (人工 review 后)
│   ├── f11_labels.parquet
│   ├── ensemble_disagreements.jsonl
│   ├── prompt_used.txt
│   ├── reliability_tables/
│   ├── interpretation_notes.md
│   ├── framing_results.json
│   └── alpha_tables/          (用户从 bjintern12 上传)
└── scripts/                   (R5 生成)
    ├── alpha_test_f11.py
    ├── config_f11.xml
    └── run_instructions.md
```

Routines: `.claude/routines/01-05_*.yaml` (索引见 `.claude/routines/README.md`)

---

## 附:嵌进 Deliverable F11 卡片的简短摘要

> *待 R5 完成后填充, 期望 schema*:
>
> v1 验证 (2026-05-XX, 2018-2019, 6,600 events):
> - reliability: Cohen κ = X.XX / macro F1 = X.XX / ensemble 3/3 = X%
> - faithfulness probe: A vs B framing 一致率 X% (>90% = label 基于 title 本身)
> - error structure: P(error | covariate) 检测 [pass/warn]
> - 主 alpha: role={...} × strength X subsample, CAR_{1,10} clustered t = X.X
> - 结论: ...
