# F11 EventRole — Routines Index

> F11 = LLM 给每条 A 股公告 title 分配 role ∈ {点火/验证/扩散/证伪/过热/退潮/ambiguous}.
> 5 个 routine 顺序触发, 总成本约 $43, 总时长约 75 min routine + 45 min 人工.

## 触发顺序与依赖

```
R1  gold_set_construct        ──→ gold_candidate.jsonl + review_queue.jsonl
                                  ↓
                              [人工 review 30-40 条, push gold_reviewed.jsonl]
                                  ↓
R2  f11_classify_batch        ──→ f11_labels.parquet (主分类输出)
       ├──→ R3  reliability_diag     ──→ reliability_tables/
       └──→ R4  faithfulness_probe   ──→ framing_results.json
                                  ↓
                              [R3 error_structure gate]
                                  ↓
R5  alpha_test_minimal        ──→ scripts/alpha_test_f11.py
                                  ↓
                              [用户 bjintern12 跑 + push alpha_tables/]
                                  ↓
                              人工拼装 Deliverable F11 卡片
```

## 数据流

```
[input]
  corpus.jsonl.gz                 来自 pysim-workspace/tools/f11_dump/ (6,600 events)
  prompt_freeze.txt               本 repo validations/F11_eventrole/

[artifacts produced]
  gold_candidate.jsonl            R1 (200 events LLM pre-label)
  review_queue.jsonl              R1 (低 confidence 子集, ~30-40 条人工 review)
  gold_reviewed.jsonl             人工 (push 回 repo)
  f11_labels.parquet              R2 (6,600 events 主分类 + ensemble)
  ensemble_disagreements.jsonl    R2 (3-way split events)
  reliability_tables/*.csv        R3 (4 张 reliability 表)
  interpretation_notes.md         R3 (variance-aware 解读)
  framing_results.json            R4 (Anthropic CoT 同款 faithfulness 测试)
  scripts/alpha_test_f11.py       R5 (用户 bjintern12 跑)
  alpha_tables/*.csv              用户上传
```

## 模型 & 成本

| Routine | Model | Cost | Time | Cache key |
|---|---|---|---|---|
| R1 | Sonnet 4.6, temp=0 | $0.5 | 5 min | event_id |
| R2 | Sonnet 4.6, temp=0.3, ×3 ensemble | $40 | 60 min | event_id × run_idx |
| R3 | Sonnet 4.6, temp=0 | $0.2 | 3 min | - |
| R4 | Sonnet 4.6, temp=0.3 | $2 | 5 min | event_id × framing_variant |
| R5 | Sonnet 4.6, temp=0 | $0.1 | 2 min | - |

Total: ~$43, ~75 min routine + ~45 min 人工 = ~2h wall clock.

## 设计原则

1. **Frozen prompt**: `prompt_freeze.txt` 一旦 lock, 不修改. 改了等于重做实验.
2. **Ambiguous gate**: 强制 LLM 在 title 不足时输出 ambiguous, 不强分.
   依据: variance-aware annotation paper (arXiv 2601.02370) — forced classification
   产生 non-classical measurement error, ambiguous label 更安全.
3. **Ensemble stability**: temp=0.3 × 3 runs vote, 测的是 stochastic stability 不是
   prompt sensitivity. 3-way split → ambiguous.
4. **Error structure 验收**: R3 重点不是 accuracy, 是 error 是否与 covariate 相关.
   error correlated with strength/regime → downstream alpha bias.
5. **Faithfulness probe**: R4 加 framing prefix 测 LLM 是否受外部暗示影响.
   依据: Anthropic Reasoning Models 论文 (CoT faithfulness).

## 触发方式

通过 Claude Code Routines UI 手动触发 (你 MAX plan 限 15 routine/day, 这 5 个一天跑完).

每个 routine 完成后自动 commit artifact 到 repo (需开 GitHub Connector + 授权 strong-event-timing repo).

## 失败重跑

每个 routine artifact-driven, 失败重跑只重跑那一个. R2 主跑挂了从 event_id cache 续跑, 不重花钱.

## 后续 routine (v2 候选, 当前不实现)

- `06_3score_extract.yaml`: 抽 narrative_consistency / novelty / evidence_direction
- `07_pdf_fetch.yaml`: 对 ambiguous events 抓 cninfo PDF 补 content
- `08_cross_feature_validate.yaml`: F11 role × F10 trigger_passive 交叉验证
