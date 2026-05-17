# F11 R3 — Reliability Diagnostics

## Summary

**Dataset:** 200 gold-reviewed events (human_role) matched against R2 labels (f11_labels.parquet, n=6,600).

**Overall agreement:** 188/200 = 94.0%
**Cohen κ:** 0.914 (almost-perfect agreement, Landis & Koch 1977)

## Per-class metrics

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 过热 | 1.00 | 1.00 | 1.00 | 40 |
| 退潮 | 0.38 | 1.00 | 0.55 | 3 |
| 证伪 | 1.00 | 1.00 | 1.00 | 20 |
| 验证 | 0.87 | 1.00 | 0.93 | 40 |
| 点火 | — | 0.00 | — | 1 |
| 扩散 | — | — | — | 0 |
| ambiguous | 0.99 | 0.89 | 0.93 | 96 |

**Macro F1:** 0.882  **Weighted F1:** 0.947

## Disagreement structure

Of the 12 disagreements:
- **11** follow the pattern `gold=ambiguous → pred=<specific_role>` (6×验证, 5×退潮).
  R2 assigned a concrete role to events that human reviewers marked ambiguous.
- **1** follows the reverse pattern `gold=点火 → pred=ambiguous`.
  R2 over-flagged a clear ignition signal as uncertain.

There are **zero** cross-role errors among clearly labeled events (e.g., 过热 vs 验证).
The dominant error mode is **ambiguity boundary disagreement**, not role mis-classification.

Notably, 9 of the 12 errors come from the `wei` task bucket (see error-structure section),
suggesting these events share structural features that make the ambiguous/role boundary harder
to resolve consistently.

## Stability (R2 confidence × gold accuracy)

High-confidence predictions are perfectly accurate (100% agreement with gold for 过热, 验证).
Mid-confidence 退潮 and 验证 predictions show lower gold accuracy (0% and 14% respectively)
because those mid-confidence assignments correspond to events gold-labeled ambiguous —
R2 resolved the ambiguity with moderate confidence, but human reviewers disagreed.
Low-confidence predictions map almost entirely to R2=ambiguous (86 events, 98.8% gold accuracy).

In short: R2 confidence is well-calibrated for non-ambiguous classes, but
mid-confidence is a marker of the ambiguity boundary where systematic disagreement occurs.

## Error-structure analysis (variance-aware paper §4)

### task_bucket

Spread across buckets: **22.5 pp**, chi² p<0.001  
Verdict: **non-classical measurement error**

| Bucket | n | errors | error_rate |
|--------|---|--------|------------|
| null | 40 | 3 | 0.075 |
| qing | 40 | 0 | 0.000 |
| ren | 40 | 0 | 0.000 |
| wei | 40 | 9 | 0.225 |
| yc | 40 | 0 | 0.000 |

### anndate_year

Spread across buckets: **2.5 pp**, chi² p=0.4844  
Verdict: **errors approximately classical**

| Bucket | n | errors | error_rate |
|--------|---|--------|------------|
| 2018 | 135 | 7 | 0.052 |
| 2019 | 65 | 5 | 0.077 |

### title_length_quartile

Spread across buckets: **4.7 pp**, chi² p=0.7252  
Verdict: **errors approximately classical**

| Bucket | n | errors | error_rate |
|--------|---|--------|------------|
| Q1 | 61 | 2 | 0.033 |
| Q2 | 40 | 3 | 0.075 |
| Q3 | 49 | 3 | 0.061 |
| Q4 | 50 | 4 | 0.080 |

## Conclusion

R2 labels are highly reliable (κ=0.914, 94.0% agreement). The dominant error mode is
**ambiguity boundary disagreement**: R2 resolves events into a specific role that human reviewers
left ambiguous (11/12 errors), rather than cross-role mis-classification.

Error structure analysis (variance-aware framework, arXiv 2601.02370) reveals:
- **task_bucket** (yc/wei/qing/ren/null): **non-classical measurement error** flagged.
  The `wei` bucket has error rate 22.5% vs 0–7.5% for other buckets (spread=22.5 pp, p<0.001).
  All 9 wei-bucket errors are ambiguous→role disagreements, suggesting `wei`-type announcements
  sit systematically near the ambiguous/role boundary and should be treated with caution in
  downstream analyses that assume classical label noise.
- **anndate_year** (2018/2019): errors approximately classical (spread=2.5 pp, p=0.48).
- **title_length_quartile** (Q1–Q4): errors approximately classical (spread=4.7 pp, p=0.73).

For downstream causal inference: stratify or down-weight `wei`-bucket events, or apply
differential measurement-error corrections for that stratum. The remaining 4 task buckets
satisfy the classical-error assumption and can be pooled without correction.
