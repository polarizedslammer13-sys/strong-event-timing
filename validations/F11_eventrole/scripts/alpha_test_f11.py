"""
F11 v1 alpha test — role label × CAR 预测力
Run on bjintern12 (pysim 5.0.0).

Input:  f11_labels.parquet  (6,600 events)
        Fields: event_id, code, anndate, title, role, confidence, ambiguous_flag, ...
Output: alpha_tables/main.csv            — Table 1: role × CAR_{1,5,10}
        alpha_tables/role_x_strength.csv — Table 2: role × strength tercile × CAR_10
        alpha_tables/f10_crossval.csv    — Table 3: trigger_passive role distribution

Usage:
    python alpha_test_f11.py --config config_f11.xml
    python alpha_test_f11.py --labels ~/path/to/f11_labels.parquet [--output alpha_tables]

Window:  2018-01-02 ~ 2019-06-28 (pysim di ≈ 2200–2560)
Cluster: year_quarter × SW2 (wind2), Liang-Zeger small-sample correction
CAR:     T+1 to T+post, market-excess cumsum (T+0 = anndate, excluded)
"""

import argparse
import os
import sys
import xml.etree.ElementTree as ET

import numpy as np
import pandas as pd

# ── pysim imports (available on bjintern12) ────────────────────────────────────
import framework.Universe as uv
from framework.Niodata import Niodata

# ─── Constants ─────────────────────────────────────────────────────────────────
N_DAYS  = uv.datasz   # 3584 total (3533 trading + 51 sentinel padding)
NSTOCK  = uv.instsz   # 6144

PRE_DAYS          = 20      # strength = prior 20D excess return
POST_LIST         = [1, 5, 10]
BOARD_THRESHOLD   = 0.095   # |return| >= 9.5% → limit-up/down (一字板, not tradable)

CLASSES = ["点火", "验证", "扩散", "证伪", "过热", "退潮", "ambiguous"]

# ─── CLI + config ───────────────────────────────────────────────────────────────
def parse_args():
    p = argparse.ArgumentParser(description="F11 alpha test — role × CAR")
    p.add_argument("--config",  default=None,           help="config_f11.xml path")
    p.add_argument("--labels",  default=None,           help="f11_labels.parquet path")
    p.add_argument("--output",  default="alpha_tables", help="output directory")
    return p.parse_args()


def load_config(config_path, args):
    cfg = {
        "labels": args.labels,
        "output": args.output,
    }
    if config_path and os.path.exists(config_path):
        root = ET.parse(config_path).getroot()
        for child in root:
            tag, text = child.tag, (child.text or "").strip()
            if text:
                cfg.setdefault(tag, text)   # CLI overrides config
        # also respect explicit CLI flags
        if args.labels:
            cfg["labels"] = args.labels
        if args.output != "alpha_tables":
            cfg["output"] = args.output
    return cfg


# ─── Clustered SE (Liang-Zeger 1986) ───────────────────────────────────────────
def clustered_se_mean(y, cluster_ids):
    """
    Clustered SE for group mean, H0: E[y]=0.
    Returns (mean, se_clust, t_clust, n_clusters, se_naive, t_naive).
    Small-sample correction: G/(G-1).
    """
    y = np.asarray(y, dtype=np.float64)
    finite = np.isfinite(y)
    y = y[finite]
    cluster_ids = np.asarray(cluster_ids)[finite]
    n = len(y)

    if n == 0:
        return np.nan, np.nan, np.nan, 0, np.nan, np.nan

    mu      = y.mean()
    se_naive = y.std(ddof=1) / np.sqrt(n) if n > 1 else np.nan
    t_naive  = mu / se_naive if (se_naive and se_naive > 0) else np.nan

    eps = y - mu  # residuals from constant model

    # aggregate by cluster
    cluster_sums = {}
    for i, g in enumerate(cluster_ids):
        cluster_sums[g] = cluster_sums.get(g, 0.0) + eps[i]

    G = len(cluster_sums)
    if G <= 1:
        return mu, se_naive, t_naive, G, se_naive, t_naive

    meat = sum(v * v for v in cluster_sums.values())
    var_raw = meat / (n * n)               # bread^{-1} = n (constant regressor)
    var_lz  = var_raw * (G / (G - 1.0))   # Liang-Zeger G/(G-1) correction
    se_lz   = np.sqrt(var_lz)
    t_lz    = mu / se_lz if se_lz > 0 else np.nan
    return mu, se_lz, t_lz, G, se_naive, t_naive


def _mean_row(y, cid, tag_prefix):
    """Return dict of stats for a y-vector under cluster_id array cid."""
    mu, se, t, ng, se_n, t_n = clustered_se_mean(y, cid)
    return {
        f"{tag_prefix}_mean"  : round(float(mu),  6) if np.isfinite(mu)  else np.nan,
        f"{tag_prefix}_se"    : round(float(se),  6) if np.isfinite(se)  else np.nan,
        f"{tag_prefix}_t"     : round(float(t),   3) if np.isfinite(t)   else np.nan,
        f"{tag_prefix}_ng"    : int(ng),
        f"{tag_prefix}_t_naive": round(float(t_n), 3) if np.isfinite(t_n) else np.nan,
    }


# ─── Universe helpers ───────────────────────────────────────────────────────────
def build_lookup_tables():
    """
    Build date→di and code→ii dicts.
    uv.codes[ii] returns the A-share code string (6-char or with suffix).
    """
    dates_arr = np.array(uv.Dates[0:N_DAYS], dtype=np.int64)
    valid_dis = np.where(dates_arr > 0)[0]  # exclude -1 sentinel rows
    date2di   = {int(dates_arr[di]): int(di) for di in valid_dis}

    # pysim may expose codes as uv.codes[ii] or uv.Codes; try both
    codes = []
    try:
        codes = [str(uv.codes[ii]) for ii in range(NSTOCK)]
    except AttributeError:
        try:
            codes = [str(uv.Codes[ii]) for ii in range(NSTOCK)]
        except AttributeError:
            # last resort: Niodata('codes') if available
            raw = Niodata('codes')
            codes = [str(raw[ii]) for ii in range(NSTOCK)]

    code2ii = {}
    for ii, c in enumerate(codes):
        # index by bare 6-char code and by full code (e.g. "000001.SZ")
        bare = c.split(".")[0].zfill(6)
        code2ii[bare] = ii
        code2ii[c]    = ii

    return date2di, code2ii


# ─── Main ───────────────────────────────────────────────────────────────────────
def main():
    args = parse_args()
    cfg  = load_config(args.config, args)

    labels_path = cfg.get("labels")
    if not labels_path:
        sys.exit(
            "ERROR: supply --labels /path/to/f11_labels.parquet "
            "or set <labels_path> in config_f11.xml"
        )
    output_dir = os.path.expanduser(cfg.get("output", "alpha_tables"))
    os.makedirs(output_dir, exist_ok=True)

    print("=" * 64)
    print("F11 R5 — role × CAR alpha test (pysim 5.0.0 / bjintern12)")
    print(f"  labels  : {labels_path}")
    print(f"  output  : {output_dir}")
    print(f"  horizon : CAR_1, CAR_5, CAR_10  (T+1 start, T+0 excluded)")
    print(f"  cluster : year_quarter × wind2 (Liang-Zeger corr.)")
    print("=" * 64)

    # ── 1. Returns matrix + market-excess cumsum ─────────────────────────────
    print("\n[1] Loading returns matrix (pysim Niodata)...")
    ret_raw = Niodata("returns")[0:N_DAYS, 0:NSTOCK].astype(np.float64)
    print(f"    shape: {ret_raw.shape}")

    print("[1] Computing market-excess cumsum...")
    mkt_mean      = np.nanmean(ret_raw, axis=1, keepdims=True)   # (N_DAYS, 1)
    excess        = ret_raw - mkt_mean                           # (N_DAYS, NSTOCK)
    excess_filled = np.where(np.isfinite(excess), excess, 0.0)
    cumsum        = np.cumsum(excess_filled, axis=0)             # (N_DAYS, NSTOCK)

    # ── 2. Wind2 industry ────────────────────────────────────────────────────
    print("[1] Loading WindIndustry.wind2...")
    wind2_raw = Niodata("WindIndustry.wind2")
    if wind2_raw.ndim == 2:
        # time-varying (N_DAYS, NSTOCK); cache full matrix for per-event lookup
        wind2_matrix    = wind2_raw[0:N_DAYS, 0:NSTOCK].astype(np.int32)
        wind2_static    = None
        use_wind2_matrix = True
    else:
        wind2_static    = wind2_raw[0:NSTOCK].astype(np.int32)
        wind2_matrix    = None
        use_wind2_matrix = False

    # ── 2. Lookup tables ─────────────────────────────────────────────────────
    print("\n[2] Building date→di and code→ii maps...")
    date2di, code2ii = build_lookup_tables()
    print(f"    dates mapped: {len(date2di)}")
    print(f"    codes mapped: {len(set(code2ii.values()))}")

    # ── 3. Load f11_labels.parquet ───────────────────────────────────────────
    print("\n[3] Loading f11_labels.parquet...")
    labels = pd.read_parquet(os.path.expanduser(labels_path))
    print(f"    shape   : {labels.shape}")
    print(f"    columns : {list(labels.columns)}")
    print(f"\n    role distribution:\n{labels['role'].value_counts().to_string()}")

    # Normalize anndate → int YYYYMMDD
    if pd.api.types.is_datetime64_any_dtype(labels["anndate"]):
        labels["anndate_int"] = labels["anndate"].dt.strftime("%Y%m%d").astype(int)
    else:
        labels["anndate_int"] = (
            labels["anndate"].astype(str)
            .str.replace("-", "", regex=False)
            .str[:8]
            .astype(int)
        )

    # Normalize code → 6-char string
    labels["code_str"] = labels["code"].astype(str).str.split(".").str[0].str.zfill(6)

    # ── 4. Map events → (di, ii) ─────────────────────────────────────────────
    print("\n[4] Mapping events to (di, ii)...")
    max_pre  = PRE_DAYS + 2   # need di-PRE_DAYS-1 to be valid
    max_post = max(POST_LIST) + 1

    event_rows = []
    skip = {"no_date": 0, "no_code": 0, "boundary": 0}

    for _, ev in labels.iterrows():
        di = date2di.get(int(ev["anndate_int"]))
        if di is None:
            skip["no_date"] += 1
            continue
        ii = code2ii.get(ev["code_str"])
        if ii is None:
            # try without leading zeros as fallback
            ii = code2ii.get(ev["code_str"].lstrip("0"))
        if ii is None:
            skip["no_code"] += 1
            continue
        if di < max_pre or di + max_post >= N_DAYS:
            skip["boundary"] += 1
            continue
        event_rows.append({
            "event_id"      : ev["event_id"],
            "di"            : int(di),
            "ii"            : int(ii),
            "role"          : str(ev["role"]),
            "confidence"    : str(ev.get("confidence", "")),
            "ambiguous_flag": bool(ev.get("ambiguous_flag", False)),
            "title"         : str(ev.get("title", "")),
            "anndate_int"   : int(ev["anndate_int"]),
        })

    events = pd.DataFrame(event_rows)
    print(f"    mapped     : {len(events)}")
    print(f"    skip (no_date={skip['no_date']}, no_code={skip['no_code']}, boundary={skip['boundary']})")

    if len(events) == 0:
        sys.exit(
            "ERROR: 0 events mapped.  Check that code / anndate format matches pysim universe.\n"
            "  Expected code format: '000001' (6-char).  anndate format: YYYYMMDD int."
        )

    # ── 5. Per-event CARs + strength ─────────────────────────────────────────
    print("\n[5] Computing per-event CARs and strength...")
    dis = events["di"].values
    iis = events["ii"].values

    # strength = pre-event excess momentum = cumsum[di-1, ii] - cumsum[di-1-PRE_DAYS, ii]
    events["strength"] = cumsum[dis - 1, iis] - cumsum[dis - 1 - PRE_DAYS, iis]

    # CAR_{post} = cumsum[di+post, ii] - cumsum[di, ii]
    # T+0 is excluded; T+1..T+post is the window.
    for post in POST_LIST:
        events[f"car_{post}"] = cumsum[dis + post, iis] - cumsum[dis, iis]

    # 一字板 flag at T+1
    ret_t1 = ret_raw[dis + 1, iis]
    events["limit_up_t1"] = np.abs(ret_t1) >= BOARD_THRESHOLD

    # Cluster key: year_quarter × wind2
    events["year"]    = (events["anndate_int"] // 10000).astype(int)
    events["quarter"] = ((events["anndate_int"] % 10000) // 100 - 1) // 3 + 1
    events["year_q"]  = events["year"].astype(str) + "Q" + events["quarter"].astype(str)

    if use_wind2_matrix:
        events["wind2"] = wind2_matrix[dis, iis]
    else:
        events["wind2"] = wind2_static[iis]

    events["cluster_id"] = events["year_q"] + "_" + events["wind2"].astype(str)

    n_clusters  = events["cluster_id"].nunique()
    n_limit_up  = events["limit_up_t1"].sum()
    print(f"    n_events    : {len(events)}")
    print(f"    n_clusters  : {n_clusters}")
    print(f"    limit_up_t1 : {n_limit_up} ({n_limit_up/len(events):.1%})")

    # Two samples: paper (all) and tradable (exclude limit-up T+1)
    ev_paper    = events
    ev_tradable = events[~events["limit_up_t1"]].copy()

    # ── 6. Table 1 — role × CAR_{1,5,10} ─────────────────────────────────────
    print("\n[6] Table 1: role × CAR_{1,5,10} (paper + tradable) ...")

    def table1_rows(df):
        rows = []
        for role in CLASSES + ["ALL"]:
            sub = df if role == "ALL" else df[df["role"] == role]
            n   = len(sub)
            row = {"role": role, "n": n}
            if n == 0:
                rows.append(row)
                continue
            cid = sub["cluster_id"].values
            for post in POST_LIST:
                row.update(_mean_row(sub[f"car_{post}"].values, cid, f"car_{post}"))
            rows.append(row)
        return rows

    t1_paper    = pd.DataFrame(table1_rows(ev_paper))
    t1_tradable = pd.DataFrame(table1_rows(ev_tradable))
    t1_paper["sample"]    = "paper"
    t1_tradable["sample"] = "tradable"
    t1 = pd.concat([t1_paper, t1_tradable], ignore_index=True)

    t1_path = os.path.join(output_dir, "main.csv")
    t1.to_csv(t1_path, index=False)
    print(f"    → {t1_path}")

    cols_show = ["role", "n", "car_1_mean", "car_5_mean", "car_10_mean", "car_10_t", "car_10_ng"]
    available = [c for c in cols_show if c in t1_paper.columns]
    print("\n  [paper sample]")
    print(t1_paper[available].to_string(index=False))

    # ── 7. Table 2 — role × strength tercile × CAR_10 ────────────────────────
    print("\n[7] Table 2: role × strength tercile × CAR_10 ...")

    def table2_rows(df):
        q33, q67 = np.nanpercentile(df["strength"].values, [33.33, 66.67])
        df = df.copy()
        df["str_t"] = pd.cut(
            df["strength"],
            bins=[-np.inf, q33, q67, np.inf],
            labels=["low", "mid", "high"],
        )
        rows = []
        for role in CLASSES + ["ALL"]:
            sub_r = df if role == "ALL" else df[df["role"] == role]
            for tercile in ["low", "mid", "high", "ALL"]:
                sub = sub_r if tercile == "ALL" else sub_r[sub_r["str_t"] == tercile]
                n   = len(sub)
                row = {
                    "role": role, "strength_tercile": tercile, "n": n,
                    "strength_q33": round(float(q33), 6),
                    "strength_q67": round(float(q67), 6),
                }
                if n == 0:
                    rows.append(row)
                    continue
                row.update(_mean_row(sub["car_10"].values, sub["cluster_id"].values, "car_10"))
                rows.append(row)
        return rows

    t2_paper    = pd.DataFrame(table2_rows(ev_paper))
    t2_tradable = pd.DataFrame(table2_rows(ev_tradable))
    t2_paper["sample"]    = "paper"
    t2_tradable["sample"] = "tradable"
    t2 = pd.concat([t2_paper, t2_tradable], ignore_index=True)

    t2_path = os.path.join(output_dir, "role_x_strength.csv")
    t2.to_csv(t2_path, index=False)
    print(f"    → {t2_path}")

    preview_roles = ["过热", "退潮", "证伪", "验证", "点火", "ALL"]
    prev_cols = ["role", "n", "car_10_mean", "car_10_t"]
    prev = t2_paper[t2_paper["role"].isin(preview_roles) & (t2_paper["strength_tercile"] == "ALL")]
    print("\n  [paper sample, strength=ALL]")
    print(prev[[c for c in prev_cols if c in prev.columns]].to_string(index=False))

    # ── 8. Table 3 — F11 × F10 trigger_passive cross-validation ──────────────
    print("\n[8] Table 3: F11 × F10 cross-validation (title ∋ '异常波动') ...")

    if "title" not in events.columns or events["title"].str.strip().eq("").all():
        print("    WARNING: 'title' column absent or blank — Table 3 skipped.")
        pd.DataFrame([{
            "subset": "trigger_passive", "n": 0,
            "note": "title column missing",
        }]).to_csv(os.path.join(output_dir, "f10_crossval.csv"), index=False)
    else:
        mask_yc = events["title"].str.contains("异常波动", na=False)
        sub_yc  = events[mask_yc].copy()
        n_yc    = len(sub_yc)
        print(f"    trigger_passive events (title ∋ '异常波动'): n = {n_yc}")

        rows3 = []
        if n_yc == 0:
            rows3.append({
                "subset": "trigger_passive", "role": "ALL", "n": 0,
                "note": "no events with '异常波动' in title",
            })
        else:
            role_cnt  = sub_yc["role"].value_counts()
            role_pct  = (role_cnt / n_yc * 100).round(1)
            pct_guore = float(role_pct.get("过热", 0.0))
            expect_ok = pct_guore >= 70.0

            print(f"\n    role distribution in trigger_passive subset:")
            for r in CLASSES:
                cnt = role_cnt.get(r, 0)
                pct = role_pct.get(r, 0.0)
                print(f"      {r:12s}: n={cnt:4d}  {pct:5.1f}%")
            print(
                f"\n    % 过热 = {pct_guore:.1f}%  "
                f"(≥70% threshold: {'✓ PASS' if expect_ok else '✗ WARN — below 70%'})"
            )

            for role in CLASSES:
                sub = sub_yc[sub_yc["role"] == role]
                n   = len(sub)
                row = {
                    "subset"        : "trigger_passive",
                    "role"          : role,
                    "n"             : n,
                    "pct_of_subset" : float(role_pct.get(role, 0.0)),
                }
                if n > 0:
                    row.update(
                        _mean_row(sub["car_10"].values, sub["cluster_id"].values, "car_10")
                    )
                rows3.append(row)

            # Summary row
            mu_all, se_all, t_all, ng_all, *_ = clustered_se_mean(
                sub_yc["car_10"].values, sub_yc["cluster_id"].values
            )
            rows3.append({
                "subset"          : "trigger_passive",
                "role"            : "ALL",
                "n"               : n_yc,
                "pct_of_subset"   : 100.0,
                "car_10_mean"     : round(float(mu_all), 6) if np.isfinite(mu_all) else np.nan,
                "car_10_t"        : round(float(t_all), 3)  if np.isfinite(t_all)  else np.nan,
                "car_10_ng"       : int(ng_all),
                "pct_guore"       : pct_guore,
                "expectation_70pct_met": expect_ok,
            })

        t3 = pd.DataFrame(rows3)
        t3_path = os.path.join(output_dir, "f10_crossval.csv")
        t3.to_csv(t3_path, index=False)
        print(f"    → {t3_path}")

    # ── 9. Summary ───────────────────────────────────────────────────────────
    print("\n" + "=" * 64)
    print("DONE.  Output files:")
    for fname in ["main.csv", "role_x_strength.csv", "f10_crossval.csv"]:
        fpath = os.path.join(output_dir, fname)
        size  = os.path.getsize(fpath) if os.path.exists(fpath) else 0
        print(f"  {fpath}  ({size:,} bytes)")

    print("\nNotes:")
    print("  - All t-stats above are clustered (year_quarter × wind2, Liang-Zeger G/(G-1)).")
    print("  - t_naive columns = non-clustered upper bound for comparison.")
    print("  - 'paper' sample includes limit-up events; 'tradable' excludes T+1 |ret|>=9.5%.")
    print("  - Upload alpha_tables/ back to the repo under")
    print("    validations/F11_eventrole/artifacts/alpha_tables/")
    print("=" * 64)


if __name__ == "__main__":
    main()
