# 强势股 / 强势行业 / 强势概念 — Event 择时 Feature 收集

## 0. 理解与组织

Task 的限定词不是装饰：「强势」把宇宙压窄后，真正在问的是 **momentum 与 event 的交互**——不是发现强势股，也不是单做事件因子。按交互方式组织（加速 / 反转 / 调制），加一类作为前述的前置输入（状态/相位）。

**方法论站位**：我做这件事的方式是把 LLM 当**事件诊断器 + 标签器**——不让模型预测涨跌，而是用它把非结构化文本（公告、互动易、研报、新闻、政策文件）抽成可回测的事件字段（主体/对象/方向/强度/新鲜度/证据等级/角色/相位），再研究这些字段在强势状态下的择时作用。这是我在 CDE 新药数据集项目里已经验证过的工作方式（mentor 已认可"对幻觉的量化与处理细致"）。所有 LLM 派生字段的验收标准统一锁在「字段误差是否与前向收益相关」上，而非平均准确率——和我在 CDE 上对 LLM 高置信幻觉的处理同源。

**全局约束**（在 A 股做这件事必须就地承认，不另列章节）：
- T+1 + 封板不可成交 → 所有择时 feature 用**次日竞价可成交价**回测，封板日撮合价非真实 fill
- 北向盘中实时披露 2024-08 已取消，仅留收盘后总量 + 前十大活跃股 + 季度持仓 → 任何依赖盘中北向的 feature 须重设
- 同花顺 / 东财概念成员名单**被追溯改写且无版本史** → 任何用到"某只票属于某概念"的 feature 必须从一手源（公告、互动易问答、研报首次覆盖、媒体首次贴标签）PIT 重建 knowledge-time

## 一、Feature 一览

| # | Feature | 类别 | 简介 | 经济逻辑 | Schema 主类型 | 难度 |
|---|---|---|---|---|---|---|
| F1 | 解禁预期透支度 | 反转·结构化 | 解禁前 20D 累计超额，分位上对解禁后 CAR 的预测力 | 解禁负漂移可能不是供给冲击，是"等解禁再走"这个集体期权到期；事前透支越多事后越无方向支撑 | float | 低 — 事件日零 look-ahead |
| F2 | 兑现幅度符号翻转项 | 反转·派生 | event 后 1–10D 漂移对 event 幅度的回归系数，按相位分组 | 后段相催化越好，预期被兑现越彻底，残余持有理由越少→系数变号（与全样本 PEAD 反号） | float 交互 | 中 — 简单回归，难点全在 F9 |
| F3 | 事件新鲜度差 | 加速·派生 | 当前事件 vs 过去 W 天事件的最大语义相似度，与强势状态相乘 | 强势状态下"新叙事"才是边际增量，"旧叙事复读"是热度而非信息→拥挤兑现风险 | float | 中 — NLP 派生 + 历史事件聚类 |
| F4 | 事件确认等级升级 | 加速·派生 | 证据等级（传闻→媒体→IR 答复→正式公告→订单→业绩）的本期最高级 - 历史最高级 | 强势概念二波/主升靠证据等级实质升级，不靠重复模糊叙事 | int + float | 中 — 多源时间戳对齐 |
| F5 | 注意力–价格斜率差 | 反转·调制 | z(attention slope, 5D) − z(price slope, 5D)，多平台注意力合成 | 关注暴涨价跟不上 = 拥挤；价先涨关注未扩散 = 早期机会 | float | 中 — 多平台数据成本 |
| F6 | 龙头催化跨题材传染滞后 | 反转·派生 | 龙头催化后同题材跟风股 +1~3D 滞后 CAR，对题材事前透支度回归 | 后段相龙头催化向跟风梯队释放"已无下一个可等催化"信号→反转链式传染 | float | 中-高 — 依赖 F9 + 跟风识别两层 PIT；容量小 |
| F7 | 龙虎榜游资接力断档 | 反转·结构化 | 高连板后「前期买入游资席位转净卖出」bool × 连板高度 | 连板续航靠游资席位接力，接力断 = 出货 | bool + categorical | 中 — schema 干净，但反转日多一字板，仅作减仓/不进场信号，非多头 alpha |
| F8 | 叙事记忆一致性 | 状态·派生 | 今日事件叙事标签 vs 过去 20D 真正伴随上涨的主叙事的相似度 | 主叙事强化 = 趋势延续；叙事漂移 = 蹭概念/退潮风险 | float | 中-高 — 需 filtered 主叙事估计 |
| F9 | PIT 题材相位 | 状态·潜状态（F2/F6/F13 输入） | filtered 相位 ∈ {发酵, 扩散, 分化, 退潮}，HMM/changepoint，仅用 ≤t 信息；附带 narrative_implied_phase 做 mismatch 检验 | 催化的信息角色在相位边界翻转：早段=证据，后段=期权到期 | categorical | 高 — 验收标准是「在线 vs 事后偏离与前向收益是否相关」而非平均准确率 |
| F10 | 跨平台注意力一致性 | 状态·结构化 | 新闻/研报/社媒/互动易/公告 5 平台 z-score 的协同度（熵或相关） | 多平台同步升温 = 趋势确认；仅社媒升温 = 短炒；仅研报升温但价未动 = 提前信号 | float | 中 — 数据获取成本 |
| F11 | 潮汐 × 强势符号 | 调制·结构化 | 已发表潮汐/聪明钱因子（东吴一脉，base 已半拥挤）× 动量分位的交互项 | 投资者结构随强弱不同 → 因子符号在强势子样本翻转 | float 交互 | 中 — 复现非完全公开口径；仅作稳健性对照，不当主信号 |
| F12 | AI Adoption Inflection | 加速·派生 | 公司 AI 落地阶段 ∈ {口号 / 试点 / 部门级 / 核心流程 / KPI 影响 / 商业化}，本期最高级 - 历史最高级 | 强势 AI 主线靠"叙事→生产率证据"转化，stage 跃迁是真正的二阶催化；纯口号在后段相被市场扣折 | int + float | 中 — LLM 多源抽取（财报/IR/招股书/管理层访谈/管理层电话会）+ KPI 类型对齐 |
| F13 | 事件因果角色 | 状态·派生 | LLM 给每条事件分配角色 ∈ {点火 / 验证 / 扩散 / 证伪 / 过热 / 退潮}，与 F4 证据等级、F9 相位正交 | F9 是题材当下处于哪一相，F4 是这条事件证据多硬，F13 是这条事件**在价格弧上做什么**——三轴正交才能定位具体 event 的择时含义 | categorical | 高 — LLM 角色分类器本身是攻坚点；验收用 forward CAR 分布与 role label 的一致性 |

## 二、Top 3 字段级 schema（其余条目不展开，避免把 collection 写成 plan）

**F1 — 解禁预期透支度**
```
unlock_date              date         公告即知，零 look-ahead
unlock_mktcap_ratio      float        解禁市值 / 流通市值
holder_type              categorical  大股东/定增/股权激励/首发原股东
pre_excess_20d           float        解禁前 20D 累计行业超额（预期透支代理）
industry_mom_pct         float        行业 60D 动量分位（强弱闸门）
label  car_post_1_10     float
分组检验：控制 ratio/市值/换手后，pre_excess_20d 分位单调预测 car_post_1_10
证伪：分位单调性 |t| < 2 或符号不符
```

**F9 — PIT 题材相位**（F2 / F6 / F13 命门）
```
concept_member 双时态表
  code, concept_id, know_date_from, know_date_to
  → 不能用终值名单；从带时间戳一手源重建 first-tagged 时刻

concept_newhigh_breadth      float    概念内创新高家数占比
limitup_decay_slope          float    涨停家数滚动衰减斜率
concept_turnover_share       float    概念成交占全市场比
coverage_accel               float    研报/新闻流速二阶导

phase                        categorical  filtered (HMM 或 changepoint，仅 ≤t 信息)
                                          禁用 smoothed 估计
narrative_implied_phase      categorical  LLM 从研报/媒体叙事抽出
                                          "叙事 implied 的题材位置"
phase_mismatch               bool = (phase ≠ narrative_implied_phase)

验收（拆三层，三件事不混）

  ① PIT 实现正确性（Concern A：filter 是否偷看未来）
     —— 这是代码/训练 pipeline 层面问题，靠以下方式审：
        · filter 训练样本严格按时间切分，保留期 ≥ phase 半衰期
        · 任何 changepoint / HMM 参数都不可在 ≤t 之外的数据上 refit
        · 单独 audit，不指望由 D_t 间接发现

  ② Filter 反应速度 / 不稳定性诊断（Concern B：D_t 真正测的东西）
     D_t = |phase_filtered_t − phase_smoothed_t|
     回归 D_t 对前向 CAR 的解释力
     若 D_t 显著解释前向收益，区分三种来源：
        (a) online estimator 系统性滞后 → 不是污染，是 filter 速度有限
        (b) smoothed 引入未来信息 → 是 benchmark 固有性质，filter 不背锅
        (c) 题材发生突然转折 → D_t 本身是有效的 instability / uncertainty proxy
     处理：F9 主模型严格只用 filtered phase；D_t 单独保留为
           不稳定性诊断项 / 二阶 feature，不作为污染判据砍掉 F9

  ③ Cycle Mismatch 检验（用 narrative_implied_phase）
     phase_mismatch=true 子样本前向 CAR
     vs phase_mismatch=false 子样本是否符号相反
     → 测「叙事 implied 周期 ≠ observed 周期 = 假强势」假设
```

**F2 — 兑现幅度符号翻转项**
```
event_mag               float         标准化 SUE 或催化体量分位
phase                   categorical   来自 F9
strength                float         个股 60D RS 分位
feature = event_mag × I(phase ∈ {分化, 退潮})
label   car_post_1_10  float
分组回归：在「强势 × 后段相」子样本，feature 系数显著为负
（与全样本 PEAD 正系数反号）
证伪：|交互项 t| < 2，或后段相组系数未由正翻负
```

## 三、排序与先做哪几个

**排序 criteria**（criteria 比排序本身重要）：机制可信 × PIT 干净度 × A 股真实可交易性（含容量）× 相对已套利 baseline 的增量 × 与现有动量低相关 × 可证伪样本量。任一维度触雷（潜状态泄露 / 封板不可成交 / 与已发表异象冗余 / N 不足）直接降级，不加权救济。

**若只能先做 3 个**：
1. **F1** — 事件零 look-ahead、纯结构化、约一周可出基准。用它把事件研究 + 强弱分组管线先跑通，并首测「预期透支度 vs 供给比例」哪个驱动方向。
2. **F9** — F2 / F6 / F13 的前置攻坚。验收标准锁死在「在线 vs 事后偏离与前向收益不相关」，不是平均准确率；附带 narrative_implied_phase 做 Cycle Mismatch 检验。
3. **F2** — 在 F1 管线 + F9 相位之上，检验那个与 PEAD 反号的交互项。这是整份的反共识载荷。

**附议**：F7 不作 alpha，作风控（持仓减仓 / 不进场）；F11 作 F2 的稳健性旁证；F12 / F13 是 LLM 抽取主力路线，与 §0 方法论站位呼应；其余 F3 / F4 / F5 / F6 / F8 / F10 在前 3 跑通后按 PnL 边际贡献排队。
