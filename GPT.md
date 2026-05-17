# GPT 对话记录 — 强势股/强势行业/强势概念 Event 择时 Idea Collection

> 用途: 收集与 GPT 的 brainstorm 内容, 后续与 Claude 的想法综合, 形成提交给大 mentor 的成熟方案.
> 个人定位: 擅长用 AI agents 处理非结构化字段.
> Task 定义: 在已经"强"的股票/行业/概念里, 判断事件驱动的热度还能不能继续扩散, 还是已经进入拥挤/反转区间. 不是"发现强势股", 而是 **强势资产的 event timing / 加减仓 filter / 入场窗口识别**.
> 要求: 60% uniqueness + 40% 逻辑性.

---

## ROUND 1 — 初始 brainstorm: 总框架 + 16 个 idea + schema

### GPT 给出的总框架 (一句话概括)

> 我想收集的不是普通事件因子, 而是"强势状态下的事件择时特征": 当股票、行业、概念已经出现价格强势后, 用事件的新鲜度、扩散层级、叙事一致性、注意力拥挤度、兑现风险、产业链传导方向来判断后续是继续走主升、进入补涨扩散, 还是即将过热反转.

### Feature 6 大类

| 类别 | 解决的问题 | 更偏向 |
|---|---|---|
| 事件新鲜度 | 这个强势是刚被事件点燃, 还是已经炒烂? | 入场时机 |
| 叙事强度 | 市场是不是形成了统一故事? | 趋势延续 |
| 扩散结构 | 是龙头带动、行业扩散, 还是末端补涨? | 行业/概念轮动 |
| 注意力拥挤 | 是否已经进入"全市场都知道"的阶段? | 反转/降权 |
| 兑现距离 | 事件离订单、业绩、政策落地还有多远? | 逻辑可靠性 |
| 非结构化增量 | 公告、互动易、研报、新闻里有没有新证据? | 个人特色 |

### 核心 schema 模板 (统一事件表)

```
event_id
trade_date
event_time
source_type              # 公告/新闻/研报/互动易/政策/社媒/龙虎榜/业绩会纪要
source_url_or_doc_id
entity_type              # stock / industry / concept / supply_chain_node
stock_code
stock_name
industry_l1
industry_l2
concept_name
event_type               # policy / order / product / price_hike / capacity / earnings / overseas / regulatory / rumor_clarification
event_subject            # 谁发生了事件
event_object             # 影响谁/哪个产品/哪个产业链环节
event_direction          # positive / negative / uncertain
event_strength           # 0-1
event_novelty            # 0-1
event_confirm_level      # rumor / media / company_response / official / financial_result
narrative_tags           # AI算力/机器人/低空经济/创新药/出口链...
evidence_text
llm_summary
llm_confidence
price_state_before_event # event前是否已强势
volume_state_before_event
limit_up_state           # 是否涨停/几连板/炸板
post_event_return_1d/3d/5d
```

呼应 SER 论文思想: 不要只把新闻丢进 embedding, 而是抽成"主体—事件—方向—强度—新鲜度—证据"的结构化输入.

---

### Idea Pool (16 个)

#### Idea 1: 强势后的"事件新鲜度差" feature
**feature**: `event_novelty_gap`
**逻辑**: 对某股票/概念在过去 W 天的事件文本做聚类或语义相似度, `event_novelty = 1 - max sim(current_event, past_events)`, 再与价格强势状态交叉.
**schema**: trade_date, stock_code/concept_name, current_event_id, event_type, event_novelty, past_sim_max, past_event_count_20d, strength_state_5d/20d, event_novelty_gap
**为什么 unique**: 区分"首发增量"和"复读热度". A 股概念炒作经常: 首事件→龙头涨停→媒体复读→互动易密集→研报覆盖→全民知道→兑现/反转.

#### Idea 2: 事件确认等级升级 feature
**feature**: `event_confirmation_upgrade`
**事件等级**: 0=rumor, 1=media, 2=IR response, 3=official policy, 4=announcement, 5=financial realization
**计算**: `upgrade = confirm_level_t - max(confirm_level_{t-W:t-1})`, 在强势股/概念中: `signal = upgrade × strength_rank`
**逻辑**: 强势股上涨初期常由模糊叙事驱动, 真正主升来自证据升级. 例如机器人概念从"有相关布局"升级到"获得大客户订单/量产/收入确认".

#### Idea 3: 龙头事件 → 补涨股扩散 feature
**feature**: `leader_event_spillover_pressure`
**计算**: 先识别概念龙头 (近 5/10 日收益高、成交额高、涨停多), 龙头出现高强度事件后:
`spillover_pressure_i = event_strength_leader × relation_strength_{i,leader} × low_position_i`
其中 relation_strength = 同概念 + 同产品 + 同客户 + 同产业链上下游 + 研报共现
**schema**: trade_date, leader_code, leader_event_id, target_code, concept_name, relation_type, relation_strength, leader_event_strength, target_position_rank, target_volume_activation, spillover_pressure
**为什么 unique**: 不是"买龙头", 而是捕捉龙头事件后的补涨扩散路径 (龙一龙二、补涨、低位挖掘).

#### Idea 4: 概念内部扩散宽度 feature
**feature**: `concept_breadth_acceleration`
**变量**: up_ratio_1d, outperform_ratio_3d, limitup_ratio, volume_expansion_ratio
**核心**: `breadth_acc = breadth_t - mean(breadth_{t-5:t-1})`, 拥挤过滤: breadth>80% + concept_return_5d 极高 → 反转风险
**逻辑**: 龙头涨 → 少数跟涨 → 宽度扩散 → 全板块高潮 → 分化. 定位"少数龙头"到"扩散"切换.

#### Idea 5: 概念叙事一致性 feature
**feature**: `narrative_coherence`
**标签**: 政策催化/订单落地/产品涨价/海外映射/国产替代/大客户验证/技术突破/业绩兑现
**计算**: `coherence = avg_pairwise_similarity(event_embeddings)` 或 `1 - entropy(tag_distribution)`
**择时含义**:
- coherence↑ + breadth↑ = 叙事形成, 趋势延续
- coherence↓ + 热度仍高 = 叙事发散, 可能退潮
**适合 AI agent**: 自动读公告/新闻/研报/互动易, 归入叙事标签.

#### Idea 6: 注意力斜率 vs 价格斜率 feature
**feature**: `attention_price_slope_gap`
**数据源**: 新闻数、研报数、股吧/雪球讨论、百度指数、互动易提问
**计算**: `gap = zscore(attention_slope) - zscore(price_slope)`
**解释**:
- gap 适中为正 → 利于延续
- gap 极高 → 注意力过热, 可能反转
- gap 为负 → 价格先行但关注未扩散, 早期机会
**呼应**: Hype Index 论文 + A 股注意力/波动/反转研究.

#### Idea 7: 强势股"事件密度衰减" feature
**feature**: `event_density_decay`
**核心**: `density_quality = unique_event_clusters / total_event_count`
**解释**: 事件多+unique 高=真增量密集; 事件多+duplicate 高=热度复读过热.
**unique 点**: 区分"信息密度"与"噪声密度".

#### Idea 8: 政策事件的"距离落地" feature
**feature**: `policy_to_realization_distance`
**事件链**: 中央定调 > 部委细则 > 地方试点 > 招标采购 > 企业订单 > 财报确认
**计算**: `realization_score = policy_level_score × (1 - distance_to_cashflow/5)`
**适用主题**: 低空经济、数据要素、机器人、算力、创新药、设备更新、消费刺激.

#### Idea 9: 海外映射 lead-lag feature
**feature**: `global_theme_mapping_pressure`
**例子**: NVDA→A股算力/光模块/液冷/电源; 特斯拉→A股机器人链; 礼来/诺和诺德→A股 GLP-1; 铜/金/油→A股资源品
**计算**: `mapping_pressure_i = global_return × mapping_strength × (1 - Ashare_reaction_rank)`
**unique 点**: 不是普通 QDII 联动, 而是事件级别的主题映射 (例如 NVDA 财报里提到液冷/推理算力/以太网, 映射到 A 股哪个细分环节).

#### Idea 10: 互动易/投资者问答的"被迫贴概念" feature
**feature**: `irm_concept_attachment_score`
**回答类型**: confirm / weak_confirm / vague / deny / risk_warning
**评分**: confirm + 具体产品/客户/收入 = 高分; vague + 只说关注 = 低分; deny/risk_warning = 负分
**择时**: 低位股首次明确绑定概念 → 补涨; 高位股密集回复但内容模糊 → 蹭概念/过热
**符合个人特色**: 互动易文本非结构化、量大、标准化差, 适合 AI agents 结构化.

#### Idea 11: 强势行业的"业绩解释权" feature
**feature**: `earnings_narrative_alignment`
**计算**: `alignment = sim(growth_drivers, market_narrative)`
**例**: 当前炒作 AI 算力, 财报增长原因若是"传统业务恢复"→ alignment 低; 若是"AI服务器电源/光模块放量"→ alignment 高
**呼应**: 2025 年 press release 研究强调 soft information 中的"解释性信息"值得结构化.

#### Idea 12: 事件"产业链位置" feature
**feature**: `supply_chain_event_position`
**例**: AI 算力里光模块、PCB、液冷、电源、服务器、IDC 节奏不同
**择时**:
- 下游需求事件 → 上游核心瓶颈环节弹性大
- 上游涨价事件 → 中游成本受压, 未必利好
- 龙头订单 → 相关供应商补涨

#### Idea 13: 龙虎榜/大单资金与事件一致性 feature
**feature**: `event_capital_alignment`
**逻辑**:
- 正向事件 + 机构/大单净买入 = alignment 高
- 正向事件 + 游资单日冲高 + 炸板 = 短炒
- 正向事件 + 大资金流出 = 背离

#### Idea 14: 强势股的"澄清公告风险" feature
**feature**: `clarification_risk_score`
**LLM 抽取**: 是否否认相关业务/收入占比很低/未形成订单/股价涨幅偏离基本面/合作不确定
**择时**: 高位+收入占比低 → 降权; 低位+明确确认业务 → 加权
**unique 点**: 专门针对强势概念炒作后期的"监管/公司降温"风险.

#### Idea 15: 概念热度的"跨平台一致性" feature
**feature**: `cross_platform_attention_consensus`
**平台含义**: 新闻=公开传播; 研报=机构叙事; 股吧/雪球=散户注意力; 互动易=投资者追问; 公告=公司确认
**择时**: 多平台同步升温 = 趋势确认; 只有社媒升温 = 短炒; 只有研报升温但价未动 = 提前信号

#### Idea 16: 强势概念的"事件链完整度" feature
**feature**: `event_chain_completeness`
**事件链**: 政策定调 → 技术突破 → 龙头订单 → 产业链扩散 → 业绩兑现
**权重**: 政策 1 / 技术 1 / 订单 2 / 价格供需 2 / 业绩 3
**择时**: 只有政策 = 早期; 政策+订单+业绩 = 可靠; 全链条满+注意力极高 = 拥挤

---

### GPT 最推荐的 5 个 (主推, 其他放 appendix)

1. **事件新鲜度差** `event_novelty_gap` — 贴合 event 择时, 体现 AI agent 文本去重/聚类/相似度优势
2. **确认等级升级** `event_confirmation_upgrade` — A 股"传闻-互动易-公告-订单-业绩"链条清晰
3. **龙头事件后的补涨扩散** `leader_event_spillover_pressure` — 最有交易员/mentor 市场直觉
4. **注意力斜率 vs 价格斜率** `attention_price_slope_gap` — 逻辑硬, 解释强势股延续/反转
5. **事件链完整度** `event_chain_completeness` — 行业/概念层面择时, 判断单点炒作 vs 链条闭合

### 提交版本 (短版)

> 老师, 我先初步整理了一版"强势股/强势行业/强势概念的 event 择时 feature 池". 我的理解是, 这里重点不是单纯识别利好事件, 而是在标的已经强势后, 判断事件是否仍有边际增量、是否进入扩散阶段、还是已经过热拥挤.
>
> 目前我觉得比较有潜力的方向有几类:
> 1. 事件新鲜度
> 2. 事件确认等级升级
> 3. 龙头事件后的补涨扩散
> 4. 注意力斜率 vs 价格斜率
> 5. 事件链完整度
>
> 共同 schema 可以先统一为: trade_date、stock/concept、event_type、source_type、event_direction、event_strength、event_novelty、confirm_level、narrative_tag、evidence_text、llm_summary, 再和价格强度、成交量、涨停、行业/概念宽度、资金行为做 join.

### 个人特色一句话 (定位)

> 我的一个切入点是: 不是直接用 LLM 预测涨跌, 而是用 AI agent 把公告、新闻、互动易、研报、政策文件等非结构化文本抽成可回测的结构化事件字段, 再研究这些事件字段在强势状态下的择时作用.

对比:
- **传统 NLP 情绪因子**: 新闻 → sentiment score → return prediction
- **你的版本**: 非结构化文本 → 事件主体/对象/方向/强度/新鲜度/确认等级/产业链位置/叙事标签 → 强势状态下择时

---

## ROUND 2 — 基于 Daily AI Frontier Digest 的前沿启发

### 最核心启发: 从 feature 到 "event state machine"

不应该只想"这个事件是利好还是利空", 而应该想:

> 一个强势概念从被点燃到扩散、拥挤、兑现、退潮, 能不能被拆成一组可观测状态?

事件出现 → 事件被解释成叙事 → 叙事绑定到股票/行业/概念 → 龙头先反应 → 相关标的扩散 → 注意力平台同步 → 公司/政策/订单确认 → 业绩兑现或证伪 → 过热/澄清/退潮.

不是单点 feature, 而是 **强势行情生命周期的状态变量**.

---

### 1. SER 的启发: 事件不要做情绪, 要做结构化语义

参考 q-fin 综述 + SER 方向 (2025-2026 hedge-fund perspective 综述).

**前沿 idea: Event Causal Role**

不是只问事件类型, 而是问事件在行情链条中的角色:

```
event_role:
  ignition_event        # 点火事件
  validation_event      # 验证事件
  amplification_event   # 扩散事件
  contradiction_event   # 证伪事件
  exhaustion_event      # 过热/退潮事件
```

例: 同样是"公司公告", 首个订单公告 = ignition/validation; 高位异动公告 = exhaustion; 收入占比很低的澄清 = contradiction.

---

### 2. THEME 的启发: 概念不是静态标签, 而是动态语义空间

参考 THEME 论文 (text profile + 层级关系 + 股票收益动态, 学习 theme-stock 语义对齐).

**前沿 idea: Theme-Center Drift**

例: "机器人"在不同阶段可能指: 工业机器人 → 人形机器人 → 减速器 → 丝杠 → 传感器 → 特斯拉供应链 → 国产替代.

```
theme_center_t = embedding(过去N天该概念的核心新闻/研报/公告/涨幅龙头文本)
stock_theme_alignment_{i,t} = sim(stock_profile_i, theme_center_t)
```

**择时**:
- 强势概念中, alignment 上升但价格尚未反应 → 潜在补涨
- alignment 下降但仍被概念标签覆盖 → 伪概念/退潮风险

**schema**: trade_date, concept_name, theme_center_text, theme_center_embedding_id, stock_code, stock_profile_embedding_id, theme_alignment_score, alignment_change_5d, stock_return_5d, underreaction_score

**优势**: 不依赖同花顺/东方财富静态概念标签, 用 AI agent 动态重建概念边界.

---

### 3. Import AI / RSI 启发: 寻找"自动化率拐点"事件

参考 Import AI #456 (RSI/自动化率阈值).

**前沿 idea: AI Adoption Inflection Feature**

把上市公司 AI 相关事件分层:
```
0 = 口号 / 战略合作
1 = 内部试点
2 = 部门级上线
3 = 核心流程接入
4 = 对收入/成本/KPI 产生量化影响
5 = 外部产品化 / 商业化收费
```

**feature**: `ai_adoption_stage_upgrade`
**schema**: trade_date, stock_code, industry, ai_use_case (客服/研发/设计/销售/风控/制造/药研/编程), adoption_stage, previous_max_stage, stage_upgrade, kpi_disclosed_flag, kpi_type (降本/增效/转化率/研发周期/毛利率), kpi_value, evidence_source

**关键转换**: 从 AI narrative → AI productivity evidence. 判断 AI 是否真的进入经营指标.

**应用**: AI 医疗 (药研周期?), AI 客服 (人力替代/转化率?), AI 教育 (付费用户/续费?), AI 制造 (质检/排产/良率?), AI 软件 (ARR/客单价?).

---

### 4. Open Model Ecosystems 启发: "开源生态复利"事件

参考 Nathan Lambert "open model ecosystems compound".

**前沿 idea: Open-Ecosystem Dependency Exposure**

事件不是"DeepSeek/Qwen/Kimi 发布新模型", 而是:
> 某个开源模型生态被下游大量采用 → 推理需求增加 → 国产算力/云/应用/数据服务/Agent 平台受益

**schema**: trade_date, open_model_name, event_type (model_release/license_change/benchmark_jump/enterprise_adoption/api_price_cut), ecosystem_signal (github_stars/HF_downloads/model_derivatives/forks), affected_layer (compute/cloud/app/data/agent/inference_endpoint), a_share_stock_code, exposure_type, dependency_score, ecosystem_momentum

**feature**: `open_ecosystem_compounding_score = ecosystem_momentum × exposure_strength × underreaction`

**unique**: 大部分人只做"模型发布事件", 你做"开源生态扩散事件".

---

### 5. Anthropic 2028 / Export Control 启发: 政策不是利好利空, 而是约束图变化

AI 相关事件越来越像 **constraint shock**: 出口管制/算力租赁限制/先进制程限制/云访问限制/模型开源限制/数据跨境限制.

**前沿 idea: Compute Access Constraint Shock**

针对 AI/半导体/算力链:
- `constraint_tightening_score`
- `constraint_bypass_score`
- `domestic_substitution_pressure`

**schema**: trade_date, policy_event_id, jurisdiction (US/China/EU/Japan/Netherlands), constraint_type (chip_export/cloud_access/EDA/equipment/model_access/data_access), affected_resource (GPU/HBM/EDA/lithography/cloud API/model weights), direction (tightening/loosening/bypass), affected_chain_node, domestic_substitution_relevance, a_share_exposure_stock

**择时**:
- 限制 HBM/GPU → 国产算力增强, 但短期压制依赖海外高端芯片的应用公司
- 云访问限制 → 国内模型/云厂商受益, 跨境 API 依赖方受损

---

### 6. LLM Agent Evaluation 启发: 不要只评估收益, 要评估"决策行为质量"

参考 "LLM judges + closed-loop RL feedback" 论文 (per-day behavioral traces, 多维 domain-specific dimensions 评估).

**前沿 idea: Event Timing Judge**

不是让 LLM 决策买卖, 而是输出可回测字段:

```
timing_judgment: enter / add / hold / avoid / reduce / reversal_watch

reason_dimension:
  novelty
  confirmation
  breadth
  crowding
  supply_chain_position
  valuation_tension
  evidence_quality
```

**schema**: trade_date, event_id, stock_code, concept_name, llm_timing_label, novelty_score, confirmation_score, crowding_score, diffusion_score, evidence_quality_score, judge_rationale_short, forward_return_1d/3d/5d

**回测**: LLM 判 enter 的事件, 1/3/5 日收益如何? 判 overheat 的是否更易反转? 哪个 judge dimension 最有效?

**优势**: 把 LLM 变成 **事件标注器 + 行为诊断器**, 而非买卖建议产生器.

---

### 7. Janus-Q 启发: event-driven trading 需要"事件级 abnormal return 标签"

参考 Janus-Q (62,400 条金融新闻数据集, 10 类事件, 事件驱动 abnormal returns 标注).

**前沿 idea: A-share Event Impact Memory**

每类事件维护历史 impact memory:
```
event_type × confirm_level × concept_state × strength_state
→ historical abnormal return distribution
```

例: 高位强势股 + 异动公告 + 收入占比低 → 历史 3 日 abret 分布; 低位补涨股 + 首次互动易确认 + 概念宽度上升 → 历史 5 日 abret 分布.

**schema**: event_id, trade_date, stock_code, event_type, confirm_level, strength_bucket, concept_breadth_bucket, attention_bucket, abnormal_return_1d/3d/5d, event_impact_bucket

让 feature 从"拍脑袋逻辑"变成"事件记忆库".

---

### 8. StockMem 启发: 强势股看"事件记忆", 不是当天新闻

参考 StockMem (event-reflection memory 框架).

**前沿 idea: Narrative Memory Consistency**

为每只强势股维护 rolling narrative memory:
- 过去 20 天真正伴随上涨的事件主题?
- 今天事件是否强化这个主题, 还是偏离?

**feature**: `narrative_memory_consistency`
**schema**: trade_date, stock_code, dominant_narrative_20d, today_event_narrative, consistency_score, narrative_shift_flag, past_driver_event_ids

**例**:
- 某股过去上涨主线 = 液冷订单, 今天 = 公司布局 AI 应用 → consistency 低, 叙事漂移
- 某股过去上涨主线 = 机器人丝杠, 今天 = 丝杠产能扩张 → consistency 高, 主线强化

---

### 9. Hedge-fund Perspective 反向启发: 必须设计"反泄漏 schema"

参考 2026 年 hedge-fund perspective 综述 (数据泄漏、horizon design、流动性、回测偏差、预测极限).

**反泄漏字段**:
```
event_publish_time
event_first_seen_time
exchange_time_bucket       # before_open / intraday / after_close / weekend
usable_trade_date
source_latency_minutes
revision_flag
```

A 股特别注意: 盘前新闻/盘中互动易/盘后公告/周末政策/假期事件 都必须映射到不同 usable_trade_date.

**意义**: 让 mentor 觉得你不是 LLM 炫技, 而是真的知道 quant 数据工程的坑.

---

### Round 2 最值得收集的 8 个前沿方向 (汇总)

| 方向 | 核心问题 | 前沿性 |
|---|---|---|
| Event Role Classification | 事件在行情生命周期里扮演什么角色? | 比情绪分类更强 |
| Dynamic Theme Center | 概念语义中心如何漂移? | 对应 THEME |
| Narrative Memory | 今天事件是否强化过去上涨主线? | 对应 StockMem |
| Confirmation Upgrade | 事件证据等级是否升级? | A 股很适合 |
| Compute Constraint Shock | 政策/算力约束如何改变产业链可达性? | AI 地缘政治迁移 |
| Open Ecosystem Momentum | 开源生态扩散如何映射到 A 股? | 前沿 AI 生态视角 |
| AI Adoption Inflection | AI 从 demo 到 production 的经营拐点? | 生产率量化 |
| Event Timing Judge | LLM 不做买卖, 而做事件行为诊断 | 对应 agent evaluation |

### Round 2 最有"你味道"的 3 个

1. **Dynamic Theme Center** — 概念不是静态标签, 而是每天漂移的语义中心. AI agent 抓取新闻/研报/公告, 动态更新概念语义中心, 找"alignment 上升但价格未反应"的股票.
2. **Narrative Memory Consistency** — 今天事件是否强化了过去驱动上涨的主叙事? 能区分: 主线强化/叙事漂移/蹭热点/证伪风险.
3. **Event Role Classification** — 系统骨架. 事件角色: 点火/验证/扩散/兑现/证伪/过热/退潮.

### Round 2 凝练总方向

> 用 AI agent 将 A 股强势股/强势行业/强势概念中的非结构化事件流, 转化为动态事件状态机: 识别事件角色、叙事中心漂移、证据等级升级、注意力扩散与拥挤程度, 从而判断强势行情处于点火、扩散、验证、兑现还是退潮阶段.

---

## ROUND 3 — "周期"是这个 task 里最重要的增量维度

### 核心洞察

同一个事件, 在不同周期阶段, 含义完全不同:
- 早期: 小利好 = 点火
- 中期: 同类利好 = 验证
- 高潮期: 大利好 = 兑现
- 退潮期: 利好 = 反弹卖点

> 真正前沿的不是 `event → return`, 而是 `event × cycle_state → return`. 事件的有效性要被周期状态条件化.

---

### 7 种周期 (必须拆开, 不要当单一宏观周期)

| 周期 | 研究对象 | 对 event timing 的意义 |
|---|---|---|
| 市场风险周期 | 全市场风险偏好、流动性、成交额 | 决定事件能否被放大 |
| 行业景气周期 | 行业基本面、价格、库存、订单 | 决定事件是否有基本面承接 |
| 政策周期 | 政策预期、出台、细则、执行、验收 | 决定主题行情处于哪一段 |
| 概念生命周期 | 点火、扩散、高潮、退潮 | 决定强势概念是否还能追 |
| 注意力周期 | 无人关注、扩散、拥挤、疲劳 | 决定 momentum 还是 reversal |
| 事件生命周期 | 传闻、确认、订单、业绩、证伪 | 决定利好是增量还是兑现 |
| 库存/价格周期 | 上游资源、制造业、消费品 | 决定涨价/订单事件的方向 |

---

### 核心思想: 事件因子必须有"相位"

每个强势主题理解成一个 wave:
```
phase 0: 静默期
phase 1: 点火期
phase 2: 扩散期
phase 3: 主升/验证期
phase 4: 高潮/拥挤期
phase 5: 分化/退潮期
phase 6: 二波/再定价期
```

**事件类型 × phase 敏感性矩阵 (示意)**:

| 事件类型 | 点火期 | 扩散期 | 高潮期 | 退潮期 |
|---|---|---|---|---|
| 政策定调 | 强点火 | 验证 | 可能兑现 | 反弹脉冲 |
| 龙头涨停 | 点火确认 | 扩散信号 | 高位拥挤 | 退潮风险 |
| 公司订单 | 强验证 | 趋势延续 | 可能兑现 | 只对个股有效 |
| 互动易确认 | 首次绑定有用 | 补涨有效 | 蹭概念风险 | 多数无效 |
| 研报密集覆盖 | 机构扩散 | 加速 | 拥挤 | 滞后 |
| 澄清公告 | 轻微扰动 | 分化 | 高风险 | 证伪 |
| 业绩兑现 | 基本面确认 | 主升支撑 | 利好落地 | 反弹确认 |

---

### 最有启发性方向: Cycle-Conditioned Event Alpha

`feature = event_strength × cycle_phase_score`

更准确说: 每类事件有自己的 phase sensitivity, `alpha(event_type, phase)` 不同.

**schema**: trade_date, stock_code, concept_name, event_id, event_type, event_strength, cycle_type, cycle_phase, phase_confidence, event_phase_interaction_score, forward_return_1d/3d/5d

**为什么前沿**: 接近"状态依赖因子". A 股动量研究 (Gao/Jiang/Xiong 2024, "Dissecting Momentum in China" 2025) 显示: 中国市场缺乏周/月动量, 但日频动量+新闻日上涨+非新闻日反转的 tug-of-war 显著, 受散户注意力驱动. → A 股 event timing 不能脱离周期和注意力状态.

---

### 周期一: 概念生命周期 (适合强势概念)

**phase**: 静默/点火/扩散/主升/高潮/退潮/二波
**可计算变量**: concept_return_3d/5d/20d, concept_turnover_z, concept_breadth, limitup_count, limitup_open_failure_rate, leader_return, leader_drawdown, news_count_z, research_report_count_z, social_attention_z, concept_member_dispersion
**关键 feature**:
- `concept_phase ∈ {silent, ignition, diffusion, main_uptrend, climax, cooling, second_wave}`
- `event_phase_fit = P(event_type historically works in current concept_phase)`

**例**:
- 低空经济 phase=点火, 政策细则 = 强正向
- 低空经济 phase=高潮, 地方小政策 = 可能兑现
- 机器人 phase=扩散, 低位公司首次确认丝杠/减速器 = 补涨
- 机器人 phase=退潮, 互动易模糊回复 = 无效甚至负向

---

### 周期二: 注意力周期 (A 股很多强势行情是注意力驱动)

参考 2025 Global Finance Journal (中国市场投资者注意力作为动量催化剂), 2026 行为金融综述, 2025 中美信息扩散研究.

**phase**: 低关注/启动/扩散/拥挤/疲劳
**变量**: news_count_z, social_discussion_z, search_index_z, research_report_count_z, irm_question_count_z, turnover_z, limitup_attention
**核心 feature**: `event_attention_interaction = attention_phase × event`

**逻辑**:
- 低关注 + 高新鲜度事件 = 最有 alpha
- 关注启动 + 龙头确认 = 趋势延续
- 关注扩散 + 补涨事件 = 有效
- 关注拥挤 + 重复新闻 = 反转风险
- 关注疲劳 + 真订单/业绩 = 可能二波

---

### 周期三: 政策周期

参考 2026 SSRN A 股政策动量研究 (动量是受监管/政策周期条件化的动态过程, 宽松→动量, 收紧→反转).

**phase**: 无预期/预期发酵/高层定调/部委细则/地方试点&招标/企业订单&执行/监管降温&规范/兑现&评估
**feature**: `policy_cycle_phase`, `policy_event_upgrade`, `policy_execution_distance`
**schema**: trade_date, policy_theme, policy_level (中央/部委/地方/协会), policy_stage, affected_concept, affected_industry, execution_distance

**例**:
- 数据要素: 高层定调→点火; 地方数据局/交易所建设→扩散; 财政预算/招标/订单→验证; 监管边界收紧→分化
- 低空经济: 政策定调→点火; 地方试点/空域改革→区域扩散; eVTOL 订单/适航认证→个股验证

**关键**: 越靠前, 弹性来自想象空间; 越靠后, 弹性来自兑现能力.

---

### 周期四: 行业景气/库存周期 (mentor 提"周期"时最可能想要的)

参考 World Bank 2025 Commodity Markets Outlook + commodity-stock cycle 研究.

**phase**: 去库存后期/补库存初期/主动补库存/被动补库存/去库存

**事件 × phase 影响**:
| 事件 | 补库存初期 | 主动补库存 | 被动补库存 | 去库存 |
|---|---|---|---|---|
| 涨价 | 强正向 | 正向 | 可能滞后 | 可能无效 |
| 扩产 | 中性/正向 | 正向 | 负向 | 负向 |
| 订单 | 强正向 | 正向 | 需看毛利 | 弱 |
| 降价 | 负向 | 分化 | 负向 | 可能出清 |
| 供给收缩 | 强正向 | 正向 | 正向 | 取决于需求 |

**feature**: `industry_inventory_phase`, `price_inventory_divergence`, `event_inventory_fit`

**例**:
- 铜价上涨 + 库存下降 + 有色板块强势 = 涨价事件有效
- 光伏: 扩产公告在景气上行期是利好; 在产能过剩/去库存周期反而可能无效或负面.

---

### 周期五: 财报/业绩周期

**phase**: 预期空窗/预告前传闻&产业数据/业绩预告/业绩快报/正式报告/业绩会&调研解释/一致预期上修/兑现&下修

**feature**: `earnings_cycle_event_stage`

**关键**: 强势股里, 市场交易的是"高增原因是否和当前强势叙事一致", 而非利润高增本身. 例: AI 算力股, 若财报增长来自传统业务修复, 不一定能继续; 来自当前主线产品放量才是验证.

---

### 周期六: 资金/风险偏好周期

**变量**: market_turnover_z, limitup_count, limitdown_count, up_down_ratio, smallcap_vs_largecap_return, growth_vs_value_return, margin_financing_change, northbound_flow, ETF_flow, volatility
**phase**: risk_on / risk_neutral / risk_off / speculative_climax
**event interaction**: `event_strength × risk_appetite_phase` (risk_appetite 是 event amplification coefficient)

---

### 周期七: 强势股自身 price cycle (最直接、最交易化)

**phase**: 低位启动/首次涨停/连板加速/断板分歧/反包/二波/高位震荡/A杀
**feature**: `stock_strength_phase`
**schema**: trade_date, stock_code, return_1d/3d/10d, distance_to_52w_high, limitup_streak, open_board_flag, intraday_drawdown, turnover_z, stock_strength_phase, event_type, event_stock_phase_fit

**事件解释**:
- 首次涨停 + 新事件 = 点火
- 二连板 + 行业扩散 = 主线确认
- 高位断板 + 澄清公告 = 退潮
- 高位震荡 + 订单公告 = 二波可能
- 高位放量 + 研报密集 = 拥挤

---

### Round 3 最前沿的 6 个周期 feature

#### 1. Event Phase Sensitivity Matrix
建立矩阵 rows=event_type, cols=cycle_phase, value=historical forward abnormal return. 让数据学习"什么事件在什么周期有效".

#### 2. Cycle Mismatch Signal ★ (最 unique)
`cycle_mismatch = event_implied_phase - observed_cycle_phase`
**例**:
- 公司讲扩产, 但行业处于去库存 → mismatch
- 媒体讲需求爆发, 但价格/库存没配合 → mismatch
- 政策讲支持, 但执行招标迟迟没有 → mismatch
- 强势股高位, 公司只给模糊互动易回复 → mismatch
**适合 AI agent**: event implied phase 可从文本里抽.

#### 3. Cycle Upgrade Event
不是事件强, 而是事件使周期升级:
- policy 预期 → 部委细则
- 概念炒作 → 订单确认
- 订单确认 → 业绩兑现
- 去库存 → 价格企稳
- 价格企稳 → 主动补库存
比"event_strength"更有用, 关注状态跃迁.

#### 4. Cycle Exhaustion Event
识别周期衰竭事件: 涨停极多但龙头断板; 新闻新高但价格不涨; 研报密集但成交缩量; 政策反复定调但无订单; 公司澄清收入占比低; 价格上涨但库存累积.
强势股择时的"不要追高"过滤器.

#### 5. Second-Wave Detector ★ (最 A 股交易化)
A 股很多强势主题不是一波结束. 二波需要: 前期强势 + 充分调整 + 注意力降温 + 新验证事件 + 龙头未彻底破位 + 行业/政策/订单继续升级.
**schema**: trade_date, concept_name, previous_peak_date, drawdown_from_peak, attention_cooling_degree, new_validation_event, leader_reclaim_strength, breadth_recovery, second_wave_probability
**意义**: 研究退潮后的再定价, 避免拥挤, 适合日频/周频择时.

#### 6. Cycle Transfer / Rotation Signal
强势行业之间会轮动. 一个主题退潮, 资金可能转向同 macro regime 下的另一个主题.
参考 2026 sector rotation 研究 + RRG (relative strength × momentum, leading/weakening/lagging/improving 四阶段).
**例**:
- AI 算力高位拥挤 → 资金扩散到电力/液冷/铜缆/PCB
- 机器人龙头高位 → 资金扩散到低位零部件
- 创新药高潮 → 资金扩散到医疗服务/器械/上游 CXO

---

### 终极 schema: Cycle-Aware Event Table

```
event_id
trade_date
usable_trade_date
stock_code
concept_name
industry
event_type
event_strength
event_novelty
confirm_level
narrative_tag
market_cycle_phase
concept_cycle_phase
attention_cycle_phase
policy_cycle_phase
industry_inventory_phase
earnings_cycle_phase
stock_strength_phase
event_phase_fit
cycle_upgrade_score
cycle_mismatch_score
cycle_exhaustion_score
second_wave_score
forward_abret_1d
forward_abret_3d
forward_abret_5d
```

不是"事件表", 而是 **事件 × 多周期状态表**.

---

### Round 3 最值得深挖的 3 个

1. **Cycle Mismatch** — 最 unique. 不是找利好, 而是找"文本叙事 implied 周期" vs "真实 observed 周期"是否匹配. 不匹配 = 假强势.
2. **Event Phase Sensitivity Matrix** — 最 quant. 历史数据学习 event_type × cycle_phase 的 abnormal return 分布. 可直接回测.
3. **Second-Wave Detector** — 最 A 股交易化. 研究"新验证事件"在注意力降温后的有效性. 比追首波更有研究价值.

---

### Round 3 最终一句话 (加上周期后的高级版本)

> 不是研究强势股出现了什么事件, 而是研究 **事件在强势行情生命周期中的相位**: 同一事件在点火、扩散、主升、高潮、退潮、二波阶段对应完全不同的收益分布; 因此需要构建 event × cycle_state 的 schema, 识别周期升级、周期错配、周期衰竭和二波再定价.

---

## 待办 / 后续整合方向

- [ ] 收集 Claude 对同一 task 的 brainstorm
- [ ] 把 GPT 的 16 个 idea + 8 个前沿方向 + 6 个周期 feature 综合去重
- [ ] 对照 mentor 偏好 ("保留完整数据, 关键参数用 tag 表达", 不用硬阈值) 调整 schema
- [ ] 区分主推 (3-5 个) vs appendix (其余)
- [ ] 准备一版可发 mentor 的精炼方案
