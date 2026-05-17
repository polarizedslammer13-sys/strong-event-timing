# F11 R5 — bjintern12 Deploy & Run

> Alpha test: role label × CAR 预测力  
> Env: bjintern12 / pysim 5.0.0  
> Output: 3 CSV tables → upload back to repo

---

## 0. Pre-flight checklist

| Item | Check |
|---|---|
| On bjintern12 | `hostname` → bjintern12 |
| pysim active | `python -c "import framework.Universe as uv; print(uv.instsz)"` → 6144 |
| pandas / numpy | `python -c "import pandas, numpy; print('ok')"` |
| pyarrow (parquet) | `python -c "import pyarrow; print('ok')"` or `pip install pyarrow --user` |

---

## 1. Clone / pull the repo

```bash
# If first time:
cd ~
git clone <repo-url> strong-event-timing
cd strong-event-timing

# If already cloned:
cd ~/strong-event-timing
git pull origin main
```

The three new files you need are:
```
validations/F11_eventrole/scripts/alpha_test_f11.py
validations/F11_eventrole/scripts/config_f11.xml
validations/F11_eventrole/artifacts/f11_labels.parquet   ← already in repo
```

---

## 2. Edit config_f11.xml (paths only)

Open `validations/F11_eventrole/scripts/config_f11.xml` and verify:

```xml
<!-- These two lines — adjust if needed -->
<labels_path>~/strong-event-timing/validations/F11_eventrole/artifacts/f11_labels.parquet</labels_path>
<output_dir>~/strong-event-timing/validations/F11_eventrole/artifacts/alpha_tables</output_dir>
```

Default paths assume you cloned to `~/strong-event-timing`. If you cloned elsewhere, edit accordingly.

---

## 3. Run

```bash
cd ~/strong-event-timing

python validations/F11_eventrole/scripts/alpha_test_f11.py \
    --config validations/F11_eventrole/scripts/config_f11.xml
```

Or override paths inline without touching the XML:

```bash
python validations/F11_eventrole/scripts/alpha_test_f11.py \
    --labels ~/strong-event-timing/validations/F11_eventrole/artifacts/f11_labels.parquet \
    --output ~/strong-event-timing/validations/F11_eventrole/artifacts/alpha_tables
```

Expected runtime: **2–5 min** (dominated by loading the full returns matrix).

---

## 4. Expected output

```
validations/F11_eventrole/artifacts/alpha_tables/
├── main.csv              ← Table 1: role × CAR_{1,5,10} (paper + tradable)
├── role_x_strength.csv   ← Table 2: role × strength tercile × CAR_10
└── f10_crossval.csv      ← Table 3: trigger_passive role distribution
```

Terminal will print summary tables inline. Look for:

- `car_10_t` column in Table 1 — clustered t-stat by role  
- `% 过热` in Table 3 — expect ≥ 70% for "异常波动" events  

---

## 5. Troubleshoot

### `ModuleNotFoundError: No module named 'framework'`

pysim is not on PATH. Activate it:

```bash
# Common pattern on bjintern12:
source ~/pysim/activate.sh
# or
export PYTHONPATH=~/pysim:$PYTHONPATH
```

### `0 events mapped`

The code or date format in the parquet doesn't match pysim's universe. Debug:

```python
import pandas as pd
import framework.Universe as uv

df = pd.read_parquet("validations/F11_eventrole/artifacts/f11_labels.parquet")
print(df["code"].head())         # e.g. "000001" or 1 (int)?
print(df["anndate"].head())      # e.g. 20180315 or "2018-03-15"?

# Check a specific date in universe
dates = list(uv.Dates[2150:2250])
print(sorted(dates)[:5])         # should be 8-digit ints like 20180102
```

Then adjust the normalization at the top of `alpha_test_f11.py` (section `[3]`).

### `AttributeError: uv has no attribute 'codes'`

pysim version difference. Try:

```python
import framework.Universe as uv
dir(uv)   # find the codes attribute name
```

Then edit the `build_lookup_tables()` function in the script:

```python
# Change this line to match your pysim version:
codes = [str(uv.codes[ii]) for ii in range(NSTOCK)]
# → try: uv.Codes, uv.inst_codes, Niodata('instcodes'), etc.
```

### Memory error on returns matrix

The returns matrix is (3584 × 6144) float64 ≈ **176 MB**. This is small.  
If you still get OOM, check `free -h` on bjintern12 and close other pysim processes.

---

## 6. Upload results back to repo

```bash
cd ~/strong-event-timing

# Create output dir placeholder if it doesn't exist yet
mkdir -p validations/F11_eventrole/artifacts/alpha_tables

git add validations/F11_eventrole/artifacts/alpha_tables/*.csv
git commit -m "F11 R5: alpha tables from bjintern12 run"
git push origin main
```

---

## 7. Reading the tables

### main.csv — Table 1

| Column | Meaning |
|---|---|
| `role` | F11 role label (7 classes + ALL) |
| `n` | event count |
| `car_{1,5,10}_mean` | mean cumulative excess return |
| `car_{1,5,10}_t` | **clustered** t-stat (year_q × wind2, Liang-Zeger) |
| `car_{1,5,10}_t_naive` | naive OLS t-stat (upper bound — read with caution) |
| `car_{1,5,10}_ng` | number of clusters used |
| `sample` | `paper` (all events) vs `tradable` (T+1 limit-up excluded) |

### role_x_strength.csv — Table 2

Same columns plus:

| Column | Meaning |
|---|---|
| `strength_tercile` | `low / mid / high / ALL` (prior 20D excess return tercile) |
| `strength_q33/q67` | tercile cut points (decimal, not %) |

### f10_crossval.csv — Table 3

| Column | Meaning |
|---|---|
| `subset` | always `trigger_passive` (title ∋ "异常波动") |
| `role` | F11 role for this subset |
| `pct_of_subset` | % of trigger_passive events with this role |
| `expectation_70pct_met` | True if 过热 ≥ 70% (cross-feature reliability check) |

---

## 8. Interpretation hints

| Finding | Implication |
|---|---|
| `car_10_t` > 2 for 过热/退潮 | F11 role has directional alpha in excess returns |
| `car_10_t` < 2 clustered (but > 2 naive) | naive SE is inflated by cross-cluster correlation — use clustered |
| 过热 % in trigger_passive < 70% | F11 LLM label is not consistent with F10 classification → investigate |
| tradable ≈ paper | no capacity distortion from limit-up events |
| tradable ≪ paper | limit-up dominates — F11 signal is paper-only for that role |

---

*Generated by F11 R5 agent (2026-05-17). Repo: strong-event-timing.*
