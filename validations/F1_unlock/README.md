# F1 解禁预期透支度 — 验证记录

> **状态**：v1 最小验证 → v3 逐年拆分 → **v4 干净样本 + matched + regime / holder / freeper 拆分**
> **核心发现**：F1 是 **regime × cohort 双条件**的 reversal，不是常数 alpha；β 在 vol 维度上呈现状态依赖性，与 §0 β(θ_t) thesis 同方向——但 §0 thesis 严格定义里的 θ_t 是 F2 题材相位（concept-level），不是 60D 截面 vol（market-level），所以这是 **vol 维度首验，不是 thesis 终验**
> **F1 评定**：保留但条件化（IPO 原股东 / 战略配售 cohort + mid/high vol regime 才成立）
> **日期**：2026-05-17
> **环境**：bjintern12（pysim 5.0.0 / Python alpha API）

---

## 一、假设（Deliverable.md F1 卡片）

> 解禁负漂移可能不是供给冲击，是"等解禁再走"这个集体期权到期；事前透支越多事后越无方向支撑。

**可证伪形式**：
- 全样本：回归 `car_post_1_10 = α + β · pre_excess_20d + ε`
- 预期 β_unlock 显著为负
- 关键比较：**β_unlock vs β_random**（同方法但非解禁日匹配对照）
- 若 β_unlock − β_random 不显著 → 假设退化为"reversal 在解禁日也有效"的平凡解释 → F1 砍掉

## 二、数据

| 项 | pysim API key | 来源 |
|---|---|---|
| 日频收益 | `'returns'` | BaseData |
| 解禁事件 offsets | `'EastmoneyConstrainedshare.offsets'` | EastmoneyConstrainedshare |
| 解禁日 | `'.releasedate'` | 同上 |
| 解禁占流通比 | `'.freeper'` | 同上 |
| 类型 | `'.type'` | 同上（76 类） |
| 日期轴 | `uv.Dates[di]` | pysim Universe |
| Universe 大小 | `uv.instsz` | pysim Universe |

**Universe**：Ashare（NSTOCK = 6144）
**回测期**：20081216 — 20230630（3533 trading days，矩阵分配 3584 行，末尾 51 行是 padding）
**事件总数**：420,988 展开后 → 412,811 过滤后（边界 + freeper ∈ (0, 100)）

## 三、方法

1. 加载全市场 returns 矩阵 (3584, 6144) via `self.returns[0:N_DAYS, 0:NSTOCK].astype(float64)`
2. 计算市场超额收益 `excess = returns − cross_section_mean`
3. cumsum 跨日 → (3584, 6144) cumsum 矩阵
4. 遍历 `EastmoneyConstrainedshare.offsets`，每个 unlock 事件 (di_e, ii) 向量化计算：
   - `pre_excess_20d = cumsum[di_e-1, ii] − cumsum[di_e-1-20, ii]`
   - `car_post_1_10  = cumsum[di_e+10, ii] − cumsum[di_e, ii]`
5. 5 分位 CAR 表（按 pre_excess 分组）
6. OLS β 回归 + t-stat
7. 随机基线：同数量 (di_r, ii_r) 抽样，(di_r, ii_r) ∉ unlock_set
8. **逐年拆分**（v3 加）：按 `uv.Dates[di_e] // 10000` 分组，跑年度 β

## 四、ALL 全样本结果

### 4.1 描述统计

| 项 | median | std | pct1/99 |
|---|---|---|---|
| pre_excess_20d | −0.0164 | 0.1187 | [−0.2687, +0.3652] |
| car_post_1_10 | −0.0103 | 0.0880 | [−0.2099, +0.2650] |
| freeper (%) | 2.00 | — | [0.01, 73.50] |

### 4.2 5 分位 CAR 表

| 分位 | pre_excess 区间 | mean car_post_1_10 | n |
|---|---|---|---|
| Q1 (最低透支) | [−1.01, −0.087] | −0.0034 | 82,562 |
| Q2 | [−0.087, −0.037] | −0.0021 | 82,562 |
| Q3 | [−0.037, +0.006] | −0.0019 | 82,562 |
| Q4 | [+0.006, +0.068] | −0.0036 | 82,560 |
| Q5 (最高透支) | [+0.068, +2.36] | −0.0103 | 82,565 |
| **Q5 − Q1** | | **−0.69%** | |

→ 5 分位非完美单调（Q2/Q3 略反），但端点 Q1/Q5 方向符合 F1：高透支 → 后续衰减

### 4.3 β 回归

| | β | SE | t | n |
|---|---|---|---|---|
| **unlock** | **−0.0246** | 0.0012 | **−21.3** | 412,811 |
| 随机基线 | −0.0181 | 0.0011 | −16.4 | 412,811 |
| **差** | **−0.0064** | ~0.0016 | **~4.0** | — |

## 五、逐年拆分（关键发现）

```
year   n_unlock    β_unlock      t_u   n_random    β_random      t_r        diff      Q5-Q1
-----------------------------------------------------------------------------------------------
-1     12,485     -0.1063   -16.38      4,281     -0.0816    -7.88     -0.0247   -0.0276 ⚠️
2009      1,186   -0.0947    -3.49     27,602    -0.0299    -6.72     -0.0648   -0.0291
2010      1,181   -0.0217    -0.85     28,522    -0.0132    -3.43     -0.0085   -0.0136
2011      1,247   +0.0271    +0.84     28,663    -0.0212    -4.97     +0.0483   +0.0079
2012      1,033   +0.0049    +0.20     28,805    -0.0384   -10.16     +0.0433   +0.0035
2013      1,091   -0.0066    -0.32     27,848    -0.0200    -4.40     +0.0134   +0.0001
2014      1,015   +0.0018    +0.10     28,910    -0.0102    -2.54     +0.0120   +0.0078
2015      1,163   -0.0797    -2.92     28,622    -0.0440    -9.96     -0.0357   -0.0343
2016      1,515   +0.0509    +2.59     28,912    +0.0039    +0.96     +0.0470   +0.0005
2017      1,828   -0.0226    -1.10     28,920    +0.0059    +1.54     -0.0285   -0.0092
2018     52,374   -0.0328   -10.06     27,993    -0.0380    -8.55     +0.0051   -0.0150
2019     62,288   -0.0420   -14.01     27,800    -0.0284    -6.48     -0.0137   -0.0086
2020     71,888   +0.0191    +6.81     27,600    +0.0169    +3.95     +0.0022   +0.0088
2021     76,312   -0.0108    -4.12     27,421    -0.0032    -0.76     -0.0076   -0.0037
2022     83,848   -0.0621   -25.06     27,553    -0.0392    -9.12     -0.0229   -0.0163
2023     42,357   -0.0395   -10.84     13,359    -0.0310    -4.98     -0.0085   -0.0136
-----------------------------------------------------------------------------------------------
ALL     412,811   -0.0245   -21.28    412,811   -0.0181   -16.39     -0.0064   -0.0069
```

### 5.1 三件不能忽视的事

**① 数据覆盖率断层（2017→2018）**：unlock 事件数从年均 1.1K-1.8K 跳到 52K-83K。pre-2018 的样本远低于 A 股实际解禁规模（年均上千只票，几百条不合理低），**pre-2018 的 β 估计不可信**。

**② year = −1 数据污染**：12,485 条 events 落在 `uv.Dates` sentinel padding 行上（N_DAYS=3584 但实际 trading days 仅 3533，末尾 51 行是 −1 sentinel）。这部分要么修代码、要么 filter 掉。

**③ 2020 反向**：COVID 极端波动 regime，β_unlock = **+0.019** (t=+6.8)。市场普遍 mean-reversion 在这一年消失（β_random 也 +0.017），unlock-specific 差几乎为零（diff=+0.002）。

### 5.2 剥掉污染后的"真"年份（2018-2023, 高 N）

| year | β_unlock | t | diff (vs random) | F1 评定 |
|---|---|---|---|---|
| 2018 | −0.033 | −10.1 | **+0.005** | unlock 不特殊 |
| 2019 | −0.042 | −14.0 | −0.014 | 弱成立 |
| **2020** | **+0.019** | **+6.8** | +0.002 | **反向（COVID）** |
| 2021 | −0.011 | −4.1 | −0.008 | 弱成立 |
| **2022** | **−0.062** | **−25.1** | **−0.023** | **最强（熊市）** |
| 2023 | −0.040 | −10.8 | −0.009 | 弱成立 |

6 年里：F1 强成立 1 年（2022 熊市），明显反向 1 年（2020 COVID），弱成立或边界 4 年。

## 六、v4 跑出来的 5 张表

### 6.1 Table 1 — clean ALL（2018-2023）

| 系列 | n | β | SE | t | Q5-Q1 |
|---|---|---|---|---|---|
| unlock | 382,301 | −0.0221 | 0.0012 | −18.49 | −0.0060 |
| matched | 381,167 | −0.0180 | 0.0011 | −15.78 | −0.0053 |
| **diff** | | **−0.0042** | | **≈ −2.6** | −0.0007 |

matched baseline（同 year_month × cap_quintile）把 diff 从 v3 的 −0.0064 缩到 **−0.0042**，仍显著但弱化了三分之一。matched rate 99.7%，对照建得很干净。

### 6.2 Table 2 — 逐年 diff（核心 caveat）

| year | diff | 主导哪一面 |
|---|---|---|
| 2018 | **+0.0060** | 反号 |
| 2019 | −0.0094 | 弱成立 |
| 2020 | +0.0033 | 反号（COVID） |
| 2021 | −0.0001 | 等于零 |
| **2022** | **−0.0241** | **强成立（熊市）** |
| 2023 | −0.0061 | 弱成立 |

**2022 一年的 −0.024 撑起 pooled diff 的大部分**。剔掉 2022 后，剩下 5 年 diff 平均约 −0.001，几乎完全平。

这有两种解读，目前**无法在数据里判别**：

- (a) **regime-conditional**：F1 真实存在，只在 2022 这样的熊市状态下点亮，其他 5 年因 regime 不对而沉默
- (b) **single-year artifact**：F1 在 6 年里就只有 2022 一年成立，本质是 outlier-driven 而非真正 regime 依赖

leave-one-year-out 未做。Table 3 vol regime split 给 (a) 的解释提供了一条平行证据（vol regime 也能切出 β 翻号），但 vol regime 和年度也未做正交化，所以不能 dispositive。**这一条是 F1 当前最大的开放风险，必须诚实标注**。

### 6.3 Table 3 — 60D vol regime split（**最干净的证据**）

| regime | n_u | β_u | t_u | diff | Q5-Q1_u |
|---|---|---|---|---|---|
| low_vol | 127,402 | +0.0019 | +0.91 | **+0.0047** | +0.0026 |
| mid_vol | 127,443 | −0.0274 | −13.10 | −0.0119 | −0.0067 |
| high_vol | 127,456 | −0.0447 | −22.54 | −0.0077 | −0.0139 |

低波动期 **β 完全反号**，F1 在低 vol regime 里不存在。中/高 vol 才成立。

**这在 vol 维度上展示了 β 的状态依赖性**：F1 的 β 不是常数，能在 vol regime 间翻号。注意 §0 thesis 严格定义的 θ_t 是 F2 PIT 题材相位（concept-level），与这里用的 60D 截面 vol（market-level）**不同**——所以这是 vol 维度首验，**phase 维度的严格 thesis 验证待 F2 出来后做**。两者方向一致是好兆头，但替代不了。

警告: 2020 全年 diff = +0.0033 (反号)，但 2020 时间波动率极高——这与 "high_vol → 强 reversal" 看似矛盾。原因可能是这里用的是**截面 vol** (cross-sectional std)，2020 国家队进场压低了截面分散，时间 vol 与截面 vol 在该年分歧。这是 vol regime 分类器的边界 case，提示用 vol 当 θ 代理的精度上限。

### 6.4 Table 4 — holder_type 异质性（**第二干净**）

| 持有人类型 | n_u | β_u | diff（vs full matched） |
|---|---|---|---|
| 股权激励限售 | 130,723 | −0.0178 | +0.0002 |
| 定向增发机构配售 | 110,884 | −0.0130 | +0.0050 |
| **首发原股东限售** | 81,853 | −0.0473 | **−0.0293** |
| 首发机构配售 | 24,668 | −0.0070 | +0.0109 |
| **首发战略配售** | 10,225 | −0.0460 | **−0.0280** |
| 其他类型聚合 | 23,948 | −0.0399 | −0.0220 |

F1 几乎完全集中在 **首发原股东 + 首发战略配售**（最长锁定期 / 最坚定 cohort）。股权激励 / 定增机构 essentially zero，定增甚至小幅反号。
**经济故事干净**：长锁定期 + 大股东 cohort 的"等解禁"集体期权到期效应最显著；短锁定期 / 机构 cohort 的 anticipation 效应几乎没有。

### 6.5 Table 5 — freeper interaction（**供给冲击通道 marginal**）

| freeper bucket | n_u | β_u | diff（vs full matched） |
|---|---|---|---|
| low (<0.69%) | 126,741 | −0.0093 | +0.0086 |
| mid (0.69-8.76%) | 128,099 | −0.0343 | −0.0163 |
| high (>8.76%) | 127,461 | −0.0308 | −0.0128 |

Interaction OLS `car_post = α + β1·pre + β2·freeper + β3·pre·freeper`：
- β1 (pre_excess) = −0.02298, t = −19.19
- β2 (freeper) = −0.00020, t = −25.12
- β3 (pre × freeper) = **−0.00012, t = −1.88**（关键检验：方向对但 marginal）

供给冲击叙事的预测是 β3 显著为负（解禁规模越大，pre-excess 的 reversal 越强）。**实际 β3 方向对但 t=-1.88，没到 |t|>2，不能 reject 供给冲击有贡献，只是 noisier than expected**。pre-excess 的 β1 (t=-19.19) 量级远大于 freeper 的 β2/β3——**主导通道是 pre-excess，freeper 角色 marginal**。这不是"两条叙事赢与输"，是**量级分层**：pre-excess 是 first-order，freeper 是 second-order。

### 6.6 综合解读：F1 是 regime × cohort 双条件 reversal

- **不是常数 alpha**：pooled diff −0.0042 看起来显著，但拆开是 2022 + IPO 原股东 / 战略配售 + mid/high vol 这几个条件叠加才出来
- **§0 β(θ_t) thesis 直接验证**：Table 3 vol regime split 里 β 在 regime 间翻号，最直接的 evidence
- **供给冲击 vs 集体期权到期**：Table 5 freeper interaction marginal（β3 t=-1.88），Table 4 holder cohort 集中在长锁定期 IPO 原股东 / 战略配售（diff −0.029）→ pre-excess 是 first-order 通道，freeper 仅 second-order 贡献。不是 "集体期权到期赢"，是 **"pre-excess 量级远大于 freeper"** ——前者是机制声明，需更细的工具变量才能严格识别，后者是观察事实，数据直接支持

## 七、已知 caveats（v3+v4 累积）

1. ~~`year=-1` padding 污染~~ → v4 已 filter
2. ~~pre-2018 数据稀疏~~ → v4 限制到 2018-2023
3. ~~随机基线没匹配~~ → v4 用 year_month × cap_quintile matched
4. ~~holder_type 异质性没拆~~ → v4 已拆
5. ~~freeper 没控~~ → v4 已交互
6. **`market-excess` 而非 industry-excess**（仍是 caveat）
7. **窗口选择敏感性没测**（pre=20, post=10 单一选择）
8. **不可成交日没剔**（一字板不可交易未排除）—— F1 是 reversal，高 pre_excess 的票常常正在一字板状态，paper alpha 与 tradable alpha 的差距未量化
9. **regime 用的是 60D 截面波动而非更细致的市场状态变量**（trend / mean-reversion 强度等）
10. **SE 是 naive OLS，不是行业 × 月份聚类** —— 同日同行业 events 高度 correlated，naive SE 系统性低估真实方差。Table 1 报告的 t=-18.49 在加聚类后保守估计可能掉到 t = -8 ~ -12 区间；diff 的 t≈-2.6 也可能掉到 -1.5 边界，**当前所有 t-stat 应作为乐观上界读**
11. **Leave-one-year-out 未做** —— 2022 一年撑起 pooled diff 的大部分（节 5.2 / 6.2），无法在数据上判别 F1 是 "regime-conditional" 还是 "2022-specific outlier"。这是 F1 当前最大的开放风险

## 八、F1 评定

**保留，但条件化**。F1 不能作为 standalone alpha 用，必须接 regime × cohort 两层闸门：

- **regime 闸门**：60D 截面波动率必须 ≥ mid（vol tercile 阈值约 1.08%/1.48%）
- **cohort 闸门**：仅在 holder_type ∈ {首发原股东限售, 首发战略配售} 上交易
- 在这两条条件都成立时，F1 提供 −0.024 到 −0.029 的 conditional reversal
- 在 low_vol 或股权激励/定增 cohort 上，F1 不存在甚至反号

这样的 conditional 形态在方向上**符合** §0 "β 状态依赖" 的预言，但**不等于** §0 thesis 已经在 F1 上被验证：

- §0 thesis 严格意义上的 θ_t 是 **F2 PIT 题材相位**（concept-level）。当前 F1 用的是 60D 截面 vol（market-level），两者只是同属"市场状态"这个大类，不可互相替代。**严格按 §0 (用 F2 phase 调制 F1) 验证待 F2 出来后做**
- 2022 dominance 让"regime-conditional vs single-year"的判别也悬而未决（caveat 11）
- SE 未聚类，所有 t-stat 应作上界读（caveat 10）

把 F1 当 vol 维度的**首验**，不当 thesis 终验。

## 九、Next steps（按优先级）

| 优先 | 任务 | 工作量 | 价值 |
|---|---|---|---|
| **高** | 行业去均值替代截面去均值 | 半天 | Table 4 的 cohort 异质性可能部分是行业 confound |
| **高** | 不可交易日 filter（一字板）| 半天 | Table 1 diff 是否仍存在 |
| **高** | 与 F2 / F4 串联——把 vol regime / 题材相位 当 F1 的闸门变量 | 1 天 | 完成 deliverable §0 在 unlock 事件上的闭环 |
| 中 | 窗口选择 robustness（pre=10/20/40, post=5/10/20）| 1 天 | Table 1 diff 是否稳定 |
| 中 | regime split 改用 trend / mean-reversion 而非 vol | 半天 | 更细致的状态变量 |
| 中 | 在 IPO 原股东 / 战略配售 cohort 内复测 freeper interaction | 半天 | β3 在干净 cohort 内是否变显著 |
| 低 | 控制 pre-event illiquidity / size | 半天 | 排除规模 confound |

## 十、文件清单

```
F1_unlock/
├── README.md                 (本文档, v4 更新)
├── AlphaF1Unlock.py          (pysim Python alpha module, v4)
├── config_f1.xml             (pysim 配置)
├── output_f1_v4.txt          (v4 跑出来的全文输出)
└── output_f1_backtest.txt    (v3 archive)
```

## 十一、部署 + 运行

bjintern12 一行（自动 pull / 跑 / push output 回 repo）：

```bash
bash ~/pysim-ws/tools/f1_unlock/run.sh
```

输出落到 `~/pysim/alphas/f1/output_f1_backtest.txt` 并自动 cp 到 `tools/f1_unlock/output_f1_v4.txt` 且 git push。log 在 `~/pysim/alphas/f1/run_log.txt`。

---

## 附：嵌进 Deliverable F1 卡片的简短摘要

> **v4 验证（2026-05-17，2018-2023 共 382,301 个干净解禁事件 + matched baseline n=381,167）**：
> - **clean ALL**：β_unlock = −0.0221 (t=−18.5)，β_matched = −0.0180 (t=−15.8)，**diff = −0.0042 (t≈−2.6)**
> - **regime split (60D vol)**：low_vol diff = +0.005（反号）/ mid_vol −0.012 / high_vol −0.008 —— **F1 在低波动期完全消失**
> - **holder cohort**：首发原股东限售 diff = −0.029，首发战略配售 diff = −0.028，股权激励 / 定增 essentially zero —— **F1 集中在最长锁定期 cohort**
> - **freeper interaction**：β3 (pre × freeper) = −0.00012, t = −1.88（方向对但 marginal）—— pre-excess 是 first-order 通道，freeper 仅 second-order
> - **caveats**：所有 t-stat 是 naive OLS（未行业聚类），应作上界读；2022 一年撑起 pooled diff，leave-one-year-out 未做；一字板未剔，是 paper alpha 不是 tradable alpha
> - **结论**：F1 在 vol regime × cohort 双闸门下呈现 conditional reversal；β 状态依赖性与 §0 thesis 同方向（vol 维度首验），**严格 phase 维度待 F2 出来后做**；2022 dominance + SE 未聚类是两个未闭合的 robustness 风险

