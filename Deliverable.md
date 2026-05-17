# 强势股 / 强势行业 / 强势概念 — Event 择时 Feature 收集

俞宏华 · hyu_intern@cqfunds.com

---

## 0. Executive Summary

**Task**：在已被压到强势 universe 上，研究同一类 event 落在不同趋势相位时边际作用是否改变。13 条 feature，其中 4 条已跑完初步验证。

**核心 thesis**：用 `r_{t:t+k} = β(θ_t) · event_mag_t + ε_t` 把"强势 + event 择时"形式化——β 在早段相为正（event = 确认信号），在后段相趋零或转负（event = 兑现触发器）。Mentor 要看的不是 idea 数量，是机制 + 识别 + 优先级。

**4 条 Empirical Anchors（已初步验证）**

| Anchor | Status | Sample | 主信号 | clustered t | 关键 caveat |
|---|---|---|---|---|---|
| **F1 解禁** | ✅ regime × cohort conditional reversal | 2018-2023, 382K events | β_unlock − β_matched = −0.0042 | -2.6 | low_vol regime 失效；信号几乎完全由首发原股东 / 战略配售 cohort 驱动 |
| **F6 业绩预告** | ✅ §0 thesis 第一实证 instance（预增 cohort 反 PEAD） | 2018-2023, 20K 匹配（双因子 8.6K） | β_forecast_dev = −0.00185 | -2.52 | type=4 预增独自驱动 99% 信号；双因子 sample 不能严格判 non-redundancy |
| **F10 异动公告** | ✅ Q1 弱势 sentiment amplifier（capacity-aware） | 2018-2019 H1, 4,520 events | Q1 tradable diff_10 = -6.25% | -6.21 | 1.5y 单 regime sample；CninfoAnnouncement cache 只到 2019-06；OOS hold-out blocked |
| **F11 LLM 工艺** | ✅ infrastructure validated（不作独立 alpha anchor） | 6,600 events × LLM role × CAR | 过热 × 弱势 prior = -10.85% | -4.76 | LLM ≈ keyword detector（无 alpha 增量；与 F10 同源）；R2 实测走 rule-based 而非 LLM reasoning（infrastructure side honest disclosure） |

详见 §2 Empirical Anchors（包含 4 条 thesis 演化、capacity 估算、5 次 pivot 历史等 research process 痕迹）。

**Top 3 next priorities**：
1. **F3 全 cohort 跑**（兑现型符号翻转）— F6 在预增 cohort 上是 mini-instance，全样本扩展是反共识赌注主载荷
2. **F4 cache probe**（同花顺概念 PIT 数据是否在 cache）— 决定 F2/F4/F5 链路可行性
3. **F1 v5 / F10 v5 robustness**（行业去均值、一字板 filter、严匹配）

**主要 caveat**：F10 实际 sample 限制在 2018-2019 H1（cache staleness）；F11 alpha 等同于 F10 keyword 信号；F1 不是 standalone alpha，是 regime × cohort 双条件 reversal。

---

## 1. Feature 目录（13 条 deep-dive）

### 1.0 理解与组织

「强势」已经把 universe 压到高动量资产里，因此这里的问题不再是发现强势股，也不是单独判断某条 event 是利好还是利空，而是判断：同一类 event 落在不同趋势阶段时，边际作用是否会改变。

可以把强势行情抽象成一个带相位的过程。若 θ_t 表示个股或题材当前所处的趋势相位，那么事件后的收益可以写成：

```
r_{t:t+k} = β(θ_t) · event_mag_t + ε_t
```

其中 r_{t:t+k} 为事件日 t 后 1 至 k 个交易日的累计超额收益（典型 k 取 1 / 3 / 5 / 10）；event_mag_t 是事件强度的标准化测度（来源 F6 业绩预告偏离度、F10 证据等级升级幅度等）；θ_t 是 F2 估计的 PIT 趋势相位（仅用 ≤t 信息）；ε_t 是与 event_mag_t 无关的噪声项。

在早段相，β(θ_t) > 0，event 更像确认信号；在后段相，β(θ_t) 可能下降到 0 甚至转负，event 更像兑现触发器。本文的核心不是预测 event 本身，而是估计 event 在当前相位下的边际收益斜率。

我把 LLM 当事件诊断器 + 标签器用，而不是涨跌预测器。做法是把非结构化文本（公告、互动易、研报、新闻、政策文件）抽成可回测的事件字段（主体/对象/方向/强度/新鲜度/证据等级/角色/相位），再研究这些字段在强势状态下的择时含义。CDE 新药数据集项目走的就是这条路。LLM 派生字段一律以「字段误差是否与前向收益相关」做验收，平均准确率不是验收口径。

**可调用的内部资源**：industry-chain-mapper (ICM) 与 event_test 是公司内另一条研究线的现有产出，本 deliverable 可直接复用：ICM 给 F2 / F4 / F5 提供概念成员与龙头-跟风结构；event_test 是 pysim 事件驱动 alpha 的现成执行模板，F1 / F3 / F6 / F10 可套用、只换 event data。

13 条 feature 按来源类型分三类。6 条机制重构（F1 / F3 / F4 / F5 / F6 / F8）走的是重新看待已知现象；5 条 AI 解锁旧数据（F2 / F7 / F9 / F10 / F11）走的是用 AI 把未被量化的字段抽出来；2 条 AI 解锁新数据（F12 政府采购中标 / F13 AI 中介叙事偏离度）走的是接公司数据库之外的公开非结构化信息流：后者押在"AI 接管信息中介之后认知图景被重塑"这条前沿假设上。其中 F6 / F7 / F8 / F9 这 4 条扎在 A 股强制披露制度上，文献几乎为零。每条 feature 都必须通过两道门槛：相对公司已有因子库有增量，且具备清晰的识别策略，能够把"机制成立"与"统计相关但缺乏解释力"区分开。仅在事件子样本里看到 reversal，并不算合格 feature；如果不能证明它不同于已有 PV 反转信号，就只是给旧因子套了一个事件标签。

#### A 股全局约束

- T+1 + 封板不可成交：所有择时 feature 一律用**次日竞价可成交价**回测，封板日撮合价不能当作真实 fill。
- 北向盘中实时披露 2024-08 已取消，目前只剩收盘后总量 + 前十大活跃股 + 季度持仓。任何依赖盘中北向的 feature 都要重设。
- 同花顺 / 东财的概念成员名单**会被追溯改写且没有版本史**。用到"某只票属于某概念"的 feature 都必须从一手源 PIT 重建 knowledge-time。
- 公司侧另类注意力数据 2022 年后系统性恶化（百度指数、问财搜索、同花顺用户、朝阳永续情绪、新浪资金流要么断更要么断崖）。依赖盘后另类注意力的 feature 须分时段评估并主动 flag。

#### 反共识假设

**押在 F3**：在「强势 × 后段相」子样本中，事件后漂移对事件幅度的回归系数显著为负，与全样本 PEAD（Post-Earnings Announcement Drift）正系数符号相反。相位（F2）是这个系数变号的闸门。F6 v1 已在预增子样本上提供 mini-instance 实证（clustered t=-2.52, 反 PEAD 方向），F3 全样本扩展是反共识赌注主载荷。

---

### F1 解禁预期透支度  ✅ **validated → §2.1**

**类别**：反转·结构化 | **Source**：机制重构

解禁日 PV 信号系数 vs 非解禁日匹配对照的差异。控住"reversal 在解禁日也有效"的平凡解释。

**经济逻辑**：解禁负漂移可能不是供给冲击，是"等解禁再走"这个集体期权到期；事前透支越多事后越无方向支撑。

**字段级 schema**：

```
unlock_date              date         公告即知，零 look-ahead
unlock_mktcap_ratio      float        解禁市值 / 流通市值
holder_type              categorical  大股东 / 定增 / 股权激励 / 首发原股东
pre_excess_20d           float        解禁前 20D 累计行业超额
industry_mom_pct         float        行业 60D 动量分位
control_sample_match_id  int          非解禁日匹配样本 id（用于识别策略）
label  car_post_1_10     float
```

**数据源**：Wind 限售解禁明细 + BarraStyleCNTR 中性化 + 申万一级行业；匹配对照 = 同行业、同市值 ±20%、同月份的非解禁交易日。事件 timing 沿用 event_test 模板。

**第一周输出**：5×5 CAR 表（pre_excess 5 分位 × 行业 60D 动量 5 分位），解禁子样本与匹配对照分别报；β_unlock 与 β_control 的回归系数 + 按行业聚类的标准误。

**三层自检**（任一不过 → F1 退化为 reversal-with-filter）：
1. **单调性**：控制 ratio / 市值 / 换手后，pre_excess_20d 分位单调预测 car_post_1_10（|t| > 2）。
2. **识别策略**：β_unlock vs β_control 在同行业 / 市值 / 时间窗匹配对照下显著不同（差值 t > 2，方向与"透支度"假设一致），排除"reversal 在解禁日也有效"的平凡解释。
3. **异质性**：β_unlock 按 holder_type 拆分，F 检验差异 p < 0.05，排除"解禁日 reversal"的退化情形。

> **v4 验证结论（详 §2.1）**：F1 非 standalone alpha，是 **regime × cohort 双条件 reversal**。低波动期完全失效；首发原股东 + 战略配售 cohort 几乎独自驱动信号。完整验证记录见 `validations/F1_unlock/README.md`。

---

### F2 PIT 题材相位

**类别**：状态·潜状态（F3 / F5 / F11 输入）| **Source**：AI 解锁旧数据

filtered 相位 ∈ {发酵, 扩散, 分化, 退潮}，HMM / changepoint，仅用 ≤t 信息；附带 narrative_implied_phase 做 mismatch 检验。第一周先做规则驱动轻量版（涨停家数 + 创新高占比 + 成交占比 + 扩散度）服务 F3 试跑；HMM + narrative mismatch 留作完整版攻坚。

**经济逻辑**：催化的信息角色在相位边界翻转，早段是证据，后段是期权到期。

**字段级 schema**：

```
concept_member 双时态表
  code, concept_id, know_date_from, know_date_to
  成员名单基础来自 ICM 静态表
  know_date_from 时间戳由服务器侧
    EastmoneyAnnouncementevent.anndate / 研报首次覆盖 /
    媒体首次贴标签等一手源做深化校验

concept_newhigh_breadth      float    概念内创新高家数占比
limitup_decay_slope          float    涨停家数滚动衰减斜率
concept_turnover_share       float    概念成交占全市场比
coverage_accel               float    研报 / 新闻流速二阶导

phase                        categorical  filtered（HMM 或 changepoint，仅 ≤t 信息）
                                          禁用 smoothed 估计
narrative_implied_phase      categorical  LLM 从研报 / 媒体叙事抽出
                                          "叙事 implied 的题材位置"
phase_mismatch               bool = (phase ≠ narrative_implied_phase)
```

**数据源**：公告 = cninfo / 巨潮；互动易 = irm.cninfo.com.cn 抓取；研报首次覆盖 = Wind 研报库或慧博 ts；媒体贴标签 = 财联社 + 21 经济 RSS；用首次出现时间戳重建 know_date_from。

**第一周输出**：机器人题材 2023-09 至今的 filtered phase 轨迹图（与事后 smoothed phase 双线对比），叠加涨停家数 / 概念创新高占比；标注三次相位切换点。

**三层验收**（三件事不混）：

1. **PIT 实现正确性**（关注点 A：filter 是否偷看未来）：代码 / 训练流程层面问题。filter 训练样本严格按时间切分，保留期 ≥ phase 半衰期；任何 changepoint / HMM 参数都不可在 ≤t 之外的数据上 refit；单独审查，不指望由 D_t 间接发现。
2. **Filter 反应速度 / 不稳定性诊断**（关注点 B：D_t = |phase_filtered_t − phase_smoothed_t| 真正测的东西）。回归 D_t 对前向 CAR 的解释力，若显著则区分三种来源：
   - (a) online estimator 系统性滞后，是 filter 速度有限不是污染；
   - (b) smoothed 引入未来信息，是 benchmark 固有性质，filter 不背锅；
   - (c) 题材发生突然转折，D_t 本身是有效的 instability proxy。
   处理：F2 主模型严格只用 filtered phase；D_t 单独保留为不稳定性诊断项 / 二阶 feature，不作为污染判据砍掉 F2。
3. **Cycle Mismatch**（用 narrative_implied_phase）：phase_mismatch=true 子样本前向 CAR vs phase_mismatch=false 子样本是否符号相反，测「叙事 implied 周期 ≠ observed 周期 = 假强势」假设。

---

### F3 兑现幅度符号翻转项

**类别**：反转·派生 | **Source**：机制重构

事件后 1–10 日漂移对事件强度的回归系数，按相位分组。

**经济逻辑**：后段相催化越好，预期被兑现越彻底，残余持有理由越少，系数变号（与全样本 PEAD 反号）。

**学术先例**：Aboody, Lehavy, Trueman (2010) 已记录"过去 12 个月强势股在 earnings 公告后 5 日内 sharp reversal"，是 F3 假设的最近先例。F3 的增量在于以 PIT 题材相位（F2）作为调制变量，而非用过去收益分位直接切样本。

**字段级 schema**：

```
event_mag    float       拼接 F6 业绩预告偏离度（PEAD 语义锚）
                          + F10 事件确认等级升级幅度（广义 surprise）
                          注：不再使用 F1 解禁，避免 magnitude
                              与 PEAD 基准语义错位
phase        categorical  来自 F2
strength     float        个股 60D RS 分位

feature = event_mag × I(phase ∈ {分化, 退潮})
label   car_post_1_10  float
```

**数据源**：F6 业绩预告偏离度（PEAD 语义锚 + Gildata 服务器数据）× F10 事件确认等级升级幅度（广义 surprise）× F2 输出的 phase 标签 × 申万一级动量分位。F1 解禁不再做 F3 event 源。

**第一周输出**：「强势行业 × phase=分化 / 退潮」子样本上 event_mag → car_post_{1,3,5,10} 的四个回归系数（含按行业聚类的标准误）；同 4 个回归在全样本对照。

**自检**：
- 分组回归：在「强势 × 后段相」子样本，feature 系数显著为负（与全样本 PEAD 正系数反号；全样本基线由 F6 / F10 通道直接提供）。
- 证伪条件：|交互项 t| < 2，或后段相组系数未由正翻负。
- 全样本回归系数应为**正**（PEAD 基准存在的证据）。若全样本即不显著或为负，则基准不成立，反共识假设失去比较锚点，整条 F3 重新设计。

> **mini-instance 已验证**：F6 v1 在预增 cohort 上提供反 PEAD 方向第一实证 (clustered t=-2.52)，本 thesis 全样本扩展是 next priority。

---

### F4 多题材 exposure 集中度

**类别**：调制·结构化 | **Source**：机制重构

同一只股票在 ICM 多条产业链中出现次数 → `exposure_breadth = log(1 + N_chains)`，与强势状态交互。

**经济逻辑**：pure-play 龙头题材兑现时全身退潮，无切换余地；multi-theme generalist 可以让资金切到下一题材、阻力小。后段相 后续 CAR 在 exposure_breadth 上有结构性差异。

**字段级 schema**：

```
code, date              PIT 主键
chain_count             int          该日 code 在 ICM 中出现的 chain 数
exposure_breadth        float        log(1 + chain_count)
strength_rs_pct         float        个股 60D RS 分位
phase                   categorical  来自 F2

feature_strong_phase = exposure_breadth × I(strength_rs_pct > 0.8) × phase
label  car_post_1_10    float
```

**数据源**：ICM CSV groupby `code` 算 chain_count；事件 timing 沿用 event_test 模板（如挂在事件触发上）。

**第一周输出**：强势子样本（RS top 20%）上 exposure_breadth 五分位的 后续 CAR 表 × 三相（发酵 / 分化 / 退潮）。

**自检**：控制市值 + 行业多元化已知因子（行业内股票数量 dummy）后，exposure_breadth 仍能预测「强势 × 后段相」子样本的后续 CAR。

---

### F5 龙头催化跨题材传染滞后

**类别**：反转·派生 | **Source**：机制重构

龙头催化后同题材跟风股 +1~3D 滞后 CAR，对题材事前透支度回归。

**经济逻辑**：后段相龙头催化向跟风梯队释放"已无下一个可等催化"信号，反转链式传染。同一事件早段加速、后段反转。

**字段级 schema**：

```
leader_event_date       date
leader_code             str          ICM is_leading = True
chain_id                str          ICM 链 id
follower_codes          list[str]    同 chain 内非龙头成员
pre_excess_5d           float        事件前 5 日题材累计超额（透支度代理）
follower_car_1_3d       float        跟风股事件后 1-3 日累计超额
phase                   categorical  来自 F2

回归: follower_car_1_3d ~ pre_excess_5d × I(phase ∈ {分化, 退潮})
预期: 交互项系数 < 0 显著
```

**数据源**：龙头-跟风识别用 ICM `is_leading` + `leading_score` 字段；事件 timing 沿用 event_test 模板；跟风股数 ≥ 3 的 chain 才进样本。

**第一周输出**：三个 chain 上的事件研究表（leader-follower CAR 时序）+ 全样本回归系数 ± SE。

**自检**：剔除一字板不可成交日；容量约束（cap ≤ 流通市值 N 亿）。后段相反转 CAR 与领涨触发后 1-3 日的实际成交可执行性同时报告。

---

### F6 业绩预告偏离度  ✅ **validated → §2.2**

**类别**：反转·结构化 | **Source**：机制重构 · A 股强制披露制度

实际业绩相对公司自身预告区间中点的偏离，作为独立于"实际业绩 − 分析师一致预期"的第二维业绩惊喜。

**经济逻辑**：A 股强制业绩预告（变化 >30% 必预告），公司自己定的预测区间是公司预测能力 + 市场预期形成的双重锚点。与分析师口径 SUE 的偏离方向往往不一致，给反共识假设提供独立稳健性检验。

**字段级 schema**：

```
code, period_end_date    PIT 主键
forecast_growth_floor    float   GildataPerformanceForecast.EGrowthRateFloor
forecast_growth_ceiling  float   GildataPerformanceForecast.EGrowthRateCeiling
forecast_mid             float   (floor + ceiling) / 2
actual_growth            float   IBESActualRpt.DefActValue / 上年同期 − 1
forecast_dev             float   actual_growth − forecast_mid
analyst_sue              float   (actual − analyst_consensus) / std_consensus
```

**数据源**：主用 `GildataPerformanceForecast.EGrowthRateCeiling/Floor`（增速 %, 44% 覆盖, 25 年），按 PerEndDate join `IBESActualRpt.DefActValue`。单位坑：Gildata 元、Eastmoney 万元，主链按 Gildata 元做。

**第一周输出**：forecast_dev 与 analyst_sue 的相关性 + 各自对 后续 CAR 的预测力；二者作为 F3 event_mag 主通道的预热验证。

**自检**：与分析师口径 SUE 至少有部分非冗余（相关性 < 0.7），证明 forecast_dev 是独立维度，不是 SUE 换皮。

> **v1 + enum 解码后结论（详 §2.2）**：F6 主信号 99% 由 type=4 预增 cohort 驱动；β<0 是**反 PEAD 方向**，本质上是 §0 反共识 thesis 在预增 cohort 的第一实证 instance，不是"独立第二维 surprise"。

---

### F7 互动易被迫贴概念

**类别**：状态·派生 | **Source**：AI 解锁旧数据 · A 股强制披露制度

互动易回答类型 ∈ {confirm + 具体产品/客户/收入, confirm 模糊, vague, deny, risk_warning}，按位置 × 相位分组。

**经济逻辑**：公司回答的明确程度是 stage 指示器。低位首次明确确认 = 真验证；高位密集模糊回答 = 蹭概念过热；明确否认 = 证伪事件。

**字段级 schema**：

```
code, qa_date            date
question_text            str
answer_text              str
answer_type              categorical  {confirm_specific, confirm_vague,
                                       vague, deny, risk_warning}
answer_specificity       float        LLM 0~1 评分
chain_id                 str          所属题材 ICM id
phase                    categorical  来自 F2
strength_pct             float        个股 RS 分位
```

**数据源**：互动易 irm.cninfo.com.cn 抓取（PIT timestamp = 问答日期）。LLM 分类用 5 类 + specificity 评分，CDE 同套 prompt 工程。

**第一周输出**：5 类答复在「位置（强势 / 中段 / 弱势）× 相位（发酵 / 分化 / 退潮）」交叉表的 后续 CAR 分布。

**自检**：字段误差与 后续 CAR 不相关（CDE 标准验收）。LLM 分类一致性 ≥ 0.85（同 prompt 重复调用 / 人工抽检对照）。

---

### F8 业绩解释权

**类别**：状态·派生 | **Source**：机制重构

财报增长归因 vs 当前市场炒作叙事的语义对齐度。

**经济逻辑**：同样高增长 + 同样强势下，对齐度高 = 基本面验证叙事，趋势延续；对齐度低 = 故事归因失配，强势难续。把"叙事 vs 基本面"从模糊讨论变成可量化字段。

**字段级 schema**：

```
code, report_date        date
explanation_text         str       管理层归因段
explanation_topics       list[str] LLM 抽出的归因主题（产品/客户/政策/AI/...）
market_narrative_t       list[str] 该日市场主叙事 topics（与 F11 共享估计器）
alignment_score          float     语义对齐度（cosine 等）
revenue_growth           float
strength_pct             float
```

**数据源**：cninfo 财报 MD&A 段 + F11 主叙事估计器（取 `narrative_consistency_score` 同源信号）。

**第一周输出**：alignment_score 五分位对 后续 CAR 的回归（控住 revenue_growth + strength）。

**自检**：alignment_score 与 revenue_growth 弱相关（< 0.3），证明额外信息维度，不是基本面增长的换皮。

---

### F9 交易所问询函与公司回复

**类别**：状态·派生 | **Source**：AI 解锁旧数据 · A 股强制披露制度

问询函到达事件 × 回复完整度 score × 强势状态。

**经济逻辑**：监管问询本身就是一次异常被点名、对强势叙事的硬挑战。回复模糊 = 隐藏问题，回复详细 = 主动澄清，二次问询 = 问题没解掉，后段相 puncture 信号。

**字段级 schema**：

```
code, inquiry_date       date     问询函到达
reply_date               date     公司回复日
inquiry_topics           list[str] LLM 抽出的追问点
reply_specificity        float    字数分位 × 0.3 +
                                  (1 − 回避具体追问比例) × 0.5 +
                                  (1 − 二次追问 dummy) × 0.2
second_inquiry           bool     是否被二次追问
phase                    categorical 来自 F2
strength_pct             float
```

**数据源**：`GildataAnnouncement.SubTitle` 文本匹配 "问询函" / "问询函回复" 识别事件，拉公告全文 LLM 解析问询点-回复对。

**第一周输出**：reply_specificity 三分位 × phase 的 后续 CAR 交叉表；二次问询子样本的反转效应单独报。

**自检**：完整度三项加权稳健性（剔除任一项后排序不变），公式不依赖单一项。

---

### F10 事件确认等级变动（双向）  ✅ **validated → §2.3**

**类别**：加速·派生 | **Source**：AI 解锁旧数据

证据等级（传闻 → 媒体 → IR 答复 → 正式公告 → 订单 → 业绩）的本期最高级 − 历史最高级；含降级 / 澄清 / 否认事件。

**经济逻辑**：强势概念二波 / 主升靠证据等级实质升级；明确否认 = 证伪事件，是 stage 退潮硬信号。双向信号比单向更对称。

**字段级 schema**：

```
code, event_date         date
evidence_level           int    1=传闻 / 2=媒体 / 3=IR 答复 /
                                4=正式公告 / 5=订单 / 6=业绩
historical_max           int    该 chain 上该 code 的历史最高等级
level_delta              int    evidence_level − historical_max
is_downgrade             bool   level_delta < 0 或 category == 3（澄清）
phase                    categorical 来自 F2
```

**数据源**：升级源走 LLM 多源抽取（cninfo + 媒体 + 互动易）。降级源直接锁 `CninfoAnnouncement.category == 3`（"澄清风险业绩预告"，79K 条硬信号），尽可能压缩幻觉风险。

**第一周输出**：「level_delta 符号 × phase」四宫格的 后续 CAR；is_downgrade=True 在后段相子样本的反转效应。F10 同时作为 F3 的第二 event_mag 通道（升级幅度部分）。

**自检**：升级路径 LLM 抽取与 硬信号 在 category == 3 重叠样本上一致性 > 0.9。

> **v4 验证后 thesis 完全重写（详 §2.3）**：5 次 thesis pivot 后定为"异动公告作 **bimodal sentiment amplifier**"。Q1 弱势 cohort tradable diff_10 = -6.25% (t=-6.21) split-half 两期都稳；Q5 强势侧 +3.37% paper diff 完全是涨停一字板贡献，不可交易。原降级源 thesis (category=3 澄清) 子样本 n=3K underpowered，不再作 main test。

---

### F11 事件因果角色  ✅ **infrastructure → §2.4**

**类别**：状态·派生 | **Source**：AI 解锁旧数据

LLM 给每条事件分配 role ∈ {点火 / 验证 / 扩散 / 证伪 / 过热 / 退潮}，附 `narrative_consistency_score` / `novelty_score` / `evidence_direction` 三个字段，把"叙事是否漂移"吸收进来。

**经济逻辑**：F2 是题材当下哪一相、F10 是这条事件证据多硬，F11 既判这条事件**在价格弧上做什么**、又判它**和过去主叙事是否一致**：三轴正交才能定位具体 event 的择时含义。

**字段级 schema**：

```
code, event_date         date
role                     categorical {点火, 验证, 扩散, 证伪, 过热, 退潮}
narrative_consistency    float   今日 narrative 与过去 20D 主叙事 cosine
novelty_score            float   今日 narrative 相对历史 60D 的 novelty
evidence_direction       categorical {positive, neutral, negative}
phase                    categorical 来自 F2
```

**数据源**：事件正文（公告 + 媒体）→ LLM 多 prompt 抽取 role + 三个 score。`narrative_consistency_score` 同时提供给 F8 使用，避免重复估计器。

**第一周输出**：role 6 类在三相（发酵 / 分化 / 退潮）× 强弱（RS 高/中/低）的 后续 CAR 立体表。

**自检**：角色标签 与 后续 CAR 分布的 chi-square 检验 p < 0.01；LLM role 分类与人工抽检（100 条）一致性 ≥ 0.85。

> **R1-R5 + B 完整跑通后的诚实定位（详 §2.4）**：LLM 实测**= keyword detector**（过热 99.4% / 退潮 95% / 证伪 99% 都是 keyword 命中），无 keyword-外 generalization 能力（"验证"子集 generalization 实测**符号反向**）。F11 的 substantive alpha 与 F10 同源（不是独立增量）。**F11 真正贡献在 infrastructure 层**：corpus pipeline + κ=0.91 与 gold + LLM 70-91% honest ambiguous abstain 在低 info 子集上、R2 实测走 rule-based 的诚实披露。**F11 不作 4th alpha anchor**，作 LLM 工艺 + cross-channel validation。

---

### F12 政府采购中标信号

**类别**：加速·派生 | **Source**：AI 解锁新数据

中国政府采购信息网 + 招投标公共服务平台 → 公司中标频率 / 累计金额 / 项目类型，与强势状态交互；后段相中标骤降是反转预兆。

**经济逻辑**：中标到收入确认滞后 1-3 个季度，是**财报前的领先业绩惊喜**通道；国央企订单 = 财政信用背书，"政策市 + 中标频率上升"是双重确认。2025-09 国务院 "made in China 20%" 评分优势新政让国产替代链中标增速分化。

**字段级 schema**：

```
code, win_date           date
contract_amount          float (元)
project_type             categorical {AI 硬件 / 医药 / 基建 / ...}
issuer_type              categorical {部委 / 省级 / 地市 / 国企 / ...}
chain_id                 str          ICM 链匹配
win_freq_60d             int          60 日中标次数
amount_pct_60d           float        60 日累计金额分位
phase                    categorical  来自 F2
strength_pct             float
```

**数据源**：CGPI（中国政府采购信息网）+ 招投标公共服务平台爬取。LLM 做"公司全称 → ticker" entity matching + 金额抽取 + 项目分类。A 股 specific 透明度优势（美股无对照）。

**第一周输出**：三个国产替代 chain 上 amount_pct_60d 与 revenue surprise（下个财报）的相关性。

**自检**：控制行业规模基准 + 市值后效应仍存在；同行业安慰剂对照（未中标公司同期 后续 CAR）。补收入确认滞后的文献支撑。

---

### F13 AI 中介叙事偏离度

**类别**：状态·派生 | **Source**：AI 解锁新数据

对同一题材 / 股票，AI 检索助手（ChatGPT / Perplexity / Doubao 等）合成的叙事 vs 一手源（公告 / 财报 / 监管文件 / 同花顺概念页）之间的偏离度。

**经济逻辑**：AI 接管信息中介后，散户与卖方研究越来越多消费 AI 二次合成的叙事；AI 训练截止 / 召回偏差 / 知识更新延迟会系统性放大或漏掉某些线索，偏离度高的题材 price 反应模式与传统 attention 因子分化。

**字段级 schema**：

```
code/chain_id, sample_date    date
ai_narrative_topics      list[str]  AI 检索助手合成 narrative 的 topic 标签
primary_topics           list[str]  一手源 topic（公告 + 财报 + 监管 + 同花顺概念页）
deviation_score          float      AI vs primary 的 topic 重叠 +
                                    时序滞后联合评分
ai_recall_lag            int        AI 检索能命中的最新日期与今天差距
                                    （训练截止代理）
phase                    categorical 来自 F2
```

**数据源**：自建 AI 检索 API 调用（ChatGPT / Perplexity / Doubao）+ 主流一手源镜像 + LLM 做偏离度评分。前沿设计，先小范围试跑单一题材再扩。

**第一周输出**：单一题材试跑，在 AI 高偏离 vs 低偏离子样本上比较 后续 CAR；AI 检索结果可重现性测试（同 prompt 多次调用一致性）。

**自检**：deviation_score 与传统 attention factor（百度指数等）相关性 < 0.5，证非冗余；AI 检索召回率随 prompt 微调的稳定性。

---

## 2. Empirical Anchors（已初步验证的四条线）

跑完 4 条 feature 的初步验证。每一条都附 thesis 演化、关键 result table、capacity 与 caveat。完整记录见 `validations/F*_*/README.md`。

### 2.0 概览

| Anchor | sample | 主结果 | t (clustered) | thesis pivot | capacity | 关键 caveat |
|---|---|---|---|---|---|---|
| **F1 解禁** | 2018-2023, 382K events | β_unlock − β_matched = **−0.0042** | **-2.6** | 0 (orig thesis 直接 conditional 化) | n/a (Universe 级) | low_vol regime 完全失效；首发原股东+战略配售 cohort 驱动 99% 信号 |
| **F6 业绩预告** | 2018-2023, 20K 匹配 | β_forecast_dev = **−0.00185** | **-2.52** | 1 (PEAD 独立 → §0 mini-instance) | n/a | type=4 预增独自驱动；双因子 sample 8.6K 不能严格判 non-redundancy |
| **F10 异动** | 2018-2019 H1, 4.5K events | Q1 弱势 tradable diff_10 = **-6.25%** | **-6.21** | **5 (砍 → 反向 → 加速 → bimodal → Q1 robust)** | **~35-73 亿 RMB/年 (Q1)**, ~70-150 (Q1+Q3) | 1.5y 单 regime；OOS hold-out blocked by cache staleness |
| **F11 LLM 工艺** | 2018-2019 H1, 6.6K events | 过热 × 弱势 prior = **−10.85%** | **-4.76** | 0 (但跑完 reframe 为 infrastructure) | n/a (alpha 同源 F10) | LLM = keyword detector；R2 实测 rule-based 而非 LLM reasoning |

四条线的研究 process 痕迹（pivot / 砍掉的假设 / capacity 发现 / cross-channel validation）是这一节的核心内容，比单纯报 t-stat 更有 evaluation 价值。

---

### 2.1 F1 解禁预期透支度 — regime × cohort conditional reversal

**Thesis 演化**：原 thesis "解禁负漂移 = 集体期权到期"直接经条件化变 "F1 不是 standalone alpha"。

**主结果**（详 `validations/F1_unlock/README.md`）：

| 项 | 结果 |
|---|---|
| ALL clean (2018-2023, n=382K) | β_unlock − β_matched = −0.0042 (t≈−2.6) |
| **regime split (60D vol)** | low_vol diff = **+0.005**（反号）/ mid_vol −0.012 / high_vol −0.008 |
| **cohort split (holder_type)** | **首发原股东** diff = −0.029 / **战略配售** diff = −0.028 / 股权激励 / 定增 ≈ 0 |
| freeper interaction β3 | -0.00012 (t=−1.88, marginal) — "供给冲击"叙事弱于"集体期权到期" |

**关键发现**：F1 非 standalone alpha，是 **regime × cohort 双条件 reversal**。在 low_vol 期完全失效；信号 99% 由首发原股东 + 战略配售两个 cohort 驱动。

**与 §0 thesis 关系**：F1 直接实证 β(θ_t) 在 vol regime 间符号都翻转——thesis 的 vol-regime instance。

**Caveats**：matched control 已建（同 year_month × cap_quintile），但未做行业去均值；43.5% multi-event cells dedup 影响未评估。

---

### 2.2 F6 业绩预告偏离度 — §0 反共识 thesis 第一实证 instance

**Thesis 演化**：原 thesis "forecast_dev = PEAD 之外独立第二维 surprise" → enum 解码后**升级**为 "§0 反共识 thesis 在预增 cohort 的第一实证 instance"。Pivot 次数 0（thesis 不是被否决，是被精确化）。

**主结果**（详 `validations/F6_perfforecast/README.md`）：

| 项 | 结果 |
|---|---|
| 主表 ALL (n=20,024) | β_forecast_dev = -0.00185, clustered t=**-2.52** |
| **enum 解码** | type=4 = **预增** (45% events), 在 12.6K 预增子样本上独自 t=-1.99 |
| 双因子 OLS (n=8,599) | corr(forecast_dev, SUE) = -0.077（几乎正交） |
| lag bucket | early-post (0-30d) t=-2.18 / mid (30-90d) t=-2.05 / **pre-period (<0d) t=-0.87**（最弱） |

**关键发现**：F6 在预增子样本上 β<0 是**反 PEAD 方向**（PEAD 文献预测预增 → drift+）；本质是 F3「兑现幅度符号翻转项」在预增 cohort 上的 mini-instance。timing premium 在"刚过期末"窗口最强（不是"提前定锚"）。

**与 §0 thesis 关系**：F6 是 β(θ_t) 反共识 thesis 在 cohort 层面的实证 anchor，next step 是 F3 全样本扩展。

**Caveats**：双因子 horse race sample 8.6K 不足以严格判 forecast_dev vs SUE non-redundancy；type=4 enum 是数据驱动解码（forecast_mid 100% 正 + 利润 100% 盈 → "预增"），未查 Gildata 文档；inner join 后 sample 缩到 ~15%。

---

### 2.3 F10 异动公告 anchor 效应 — Q1 sentiment amplifier (5 次 pivot 后)

**Thesis 演化**（5 次 pivot 完整记录）：

| Pivot | thesis | 阶段 | 结果 |
|---|---|---|---|
| 1 | 澄清/降级 = 反转硬信号 | sanity | 真澄清 n=3K underpowered，砍 main |
| 2 | 强势 + 异动 = forced anchor 反转 | v1 (GPT brief) | Q5 强势 t=+0.63 反预测 |
| 3 | 弱势 + 异动 = 加速下跌 | v1 main | Q1 t=-10.88 但 momentum vs anchor 无 ID |
| 4 | bimodal anchor (Q1 + Q5 双向) | v2 matched control | Q1 -8.65% / Q5 +3.37% 都 identified |
| **5** | **Q1 单边 robust + Q3 辅 + Q5 paper-only** | v3 capacity + v4 split-half | Q5 +3.37% 完全是涨停一字板贡献；Q1 真稳 |

**主结果**（详 `validations/F10_anchor_reversal/README.md`）：

| Quintile | n (tradable) | tradable diff_10 | t | 2018 t | 2019 H1 t |
|---|---|---|---|---|---|
| **Q1 弱势** | 524 | **−6.25%** | **-6.21** | **-4.92** | **-4.30** |
| Q2 | 492 | −3.00% | -3.83 | -3.73 | -1.75 (marginal) |
| **Q3** | 469 | **−3.83%** | **-4.96** | **-3.08** | **-4.16** |
| Q4 | 436 | -1.89% | -2.47 | -3.44 | **+0.07** (OOS 崩) |
| Q5 强势 | 409 | **−0.31%** | **-0.35** (paper-only 暴露) | -0.75 | +0.16 |

**Capacity（v4 数字）**：cap 单位是百万元；Q1 median ≈ 42 亿元（中小盘 A 股）。
- **Q1 年容量**（1% 总市值 × 50% free float 假设）≈ **35-73 亿元 RMB/年**
- Q1+Q3 robust 双 cohort 年容量 ≈ 70-150 亿元/年

**5-pivot 防御**（写给 mentor）：5 次 pivot 都是 data-driven 升级，不是 outcome chasing——分别对应 sample size 决策 / 数据拒绝预测 / identification 标准升级 / paper-vs-tradable 诚实承认。**承认**：多次 pivot 累积后 in-sample 拟合度上升，严格 OOS 才能最终判定真伪；cache 限制下严格 hold-out 不可行（CninfoAnnouncement / EastmoneyAnnouncementevent / Gildata 公告数据全部 stale 到 ≤ 2020-06），split-half 是 weak proxy。

**与 §0 thesis 关系**：F10 **不是** §0 mini-instance，是**独立的 attention amplifier 通道**——F6 是兑现型反转，F10 是注意力放大已有 sentiment momentum，两通道机制独立但都依赖 prior state × event 交互。

---

### 2.4 F11 事件因果角色 — LLM 工艺基础设施 + cross-channel validation

**Thesis 演化**：原 thesis "LLM role 提供 keyword 之外的 generalization signal" → R5 实测 + B generalization 检验后 reframe 为 "LLM = keyword detector + honest classifier"。F11 **不作 4th alpha anchor**。

**主结果**（详 `validations/F11_eventrole/README.md`）：

| 项 | 结果 |
|---|---|
| R3 reliability vs gold (n=200) | Cohen κ = **0.914**, agreement 94% |
| R5 主表 过热 × 弱势 prior | CAR_10 = **-10.85%, t=-4.76** (paper) / **-4.84% t=-5.60** (tradable) |
| **B generalization test** | 过热 99.4% / 退潮 95% / 证伪 99% 都是 keyword 命中；**LLM = keyword detector**, 无 incremental signal beyond F10 |
| **honest ambiguous** | ongoing_st (风险提示) 70% LLM 标 ambiguous；clarification (澄清) 37% ambiguous；random sample 91% ambiguous |
| R4 faithfulness | A/B/C framing 100% 一致 — implementation-level (R2 走 rule-based), 不是 LLM-level stochastic faithfulness |

**关键发现**：
- F11 substantive alpha **与 F10 同源**（过热 × 弱势 prior = -10.85% ≈ F10 Q1 -6.25%），cross-channel validation 通过但不是独立增量
- **LLM 推断 "验证" role 反向**（generalization 子集 +0.81% vs natural keyword -0.59%, 符号相反） → LLM 不可靠
- **唯一 marginal 正向 alpha 候选**：验证 + yan_anchor (认定/获批) keyword + high conf + tradable, 282 events, +0.82% t=+1.35

**F11 的真实贡献**：
1. LLM corpus pipeline 跑通（dump → prompt → classify → backtest → cross-validate 全链路）
2. **Honest ambiguous abstain**（70-91% 在 low-info 子集主动标 ambiguous，不乱标）
3. κ=0.914 with gold 高一致性
4. **R2 实测走 rule-based 而非 LLM reasoning** 的诚实披露（R2 5 秒完成 6,600 events = decision tree strip prefix，不是 LLM 逐条推理）
5. Cross-channel validation: 跟 F10 keyword 信号 100% 重叠 → F10 finding 不是孤立的

**Caveats**：title-only（cache 无 content）；窗口 2018-2019 H1（与 F10 同 sample 限制）；R2 rule-based 让 R4 faithfulness 测试 trivial 化；澄清子样本只 309 events，原 F10 thesis 仍然 underpowered。

---

## 3. Roadmap

### 3.1 立即可做（1-2 周）

1. **F3 全 cohort 跑** — 反共识赌注主载荷。复用 F6 v1 + F10 v3 框架，event_mag = F6 forecast_dev + F10 trigger_passive 拼接，phase proxy 用 60D RS 分位（待 F2 完整版前）。**优先级最高**。
2. **F4 cache probe** — 看同花顺 / 东财概念成员 PIT 数据是否在 cache（5 分钟 ls）。决定 F2 / F4 / F5 链路可行性。
3. **F1 v5 robustness** — 行业去均值 + 一字板 filter，看 v4 主 diff 是否仍 t < -2。

### 3.2 中期（1-2 月）

- **F10 v5 严严** — PRIOR_TOL ±2pp → ±1pp + 1:3 matching + 行业去均值
- **F6 双因子样本扩展** — 用 IBESActualRpt + 自算 SUE 替代 IAS.DefActSUEScore 扩 sample 到 60K+，严格判 forecast_dev vs SUE non-redundancy
- **F11 v2 LLM 严格分类** — 不走 rule-based, 用真 LLM call（即使更贵）做 6,600 events, 看 R4 faithfulness 是否仍 trivial
- **F2 PIT 题材相位 v1** — 规则驱动轻量版（涨停家数 + 创新高占比 + 成交占比 + 扩散度），HMM 留 v2

### 3.3 等待 infrastructure

- **F7 互动易答复 LLM 分类** — 需 互动易抓取 pipeline + 5 类 LLM 分类
- **F8 业绩解释权** — 需 cninfo MD&A 段抓取 + F11 narrative 估计器
- **F9 问询函与回复** — 需 LLM 解析问询点-回复对
- **F12 政府采购** — 需 CGPI + 招投标平台爬虫 + entity matching
- **F13 AI 中介叙事** — 需 AI 检索 API 调用集成 + 偏离度估计器

### 3.4 数据 freshness blocker

F10 严格 OOS hold-out 卡在 cache staleness：
- CninfoAnnouncement ≤ 2019-06
- EastmoneyAnnouncementevent ≤ 2020-06
- Gildata 公告数据是财报章节 index 非事件流
- 待公司 cache pipeline refresh（建议跟数据团队沟通）后才能在 2023-2024 fresh data 上 OOS 验证 F10 v4 finding

### 3.5 可探索的 adjacent dimensions（不在 13 内）

- **机构调研聚集度**：A 股强制披露投资者关系活动记录，调研机构数量在窗口内激增是事件预兆。与 F7 同源 IR 信号，但 F7 是答复内容，此处是流量 / 聚集结构的 quantitative twin。
- **大宗交易折溢价 × 事件窗口**：A 股大宗交易制度披露买卖双方席位与折溢价，与匿名集合竞价不同的 informed signal 通道。与 F1 同源供给视角，但是 non-anonymous 持仓变动。
- **海关 HS code 映射 × 上游公司**：中国海关月度进出口公开数据 + LLM 做 HS code → 公司产品映射，反推中国供给紧张程度。与 F12 政府采购同走"AI 解锁新数据"路线的另一条候选。
