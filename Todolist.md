# Todolist — strong-event-timing deliverable

> 当前 Deliverable 状态：MD + HTML 已交付 v2，11 个 feature，Top 3 = F1 / F7 / F2，
> Aboody (2010) 引文加在 F2。本 todo 列接下来要做但当前不紧急的事。

## P0 — 重大调整

### 1. §一 Feature 一览的展开内容升级

**问题**：当前 11 个 `<details>` 卡片展开后只看到 简介 / 经济逻辑 / Schema 类型 / 难度备注，
价值不高。Top 3 的字段级 schema 单独在 §二，其他 8 个 feature（F3 / F4 / F5 / F6 / F8 / F9 /
F10 / F11）没有字段级展开。

**想要的状态**：展开任何一条 feature 都能看到字段级 schema + 经济逻辑 + 难度备注，
mentor drill 任何一条都不需要跳到别的章节。

**待办子任务**：
- [ ] 为 F3-F11 这 8 个 feature 各写一份字段级 schema（参考 F1 / F7 / F2 的颗粒度）
- [ ] 决定 §一 vs §二 的关系：
  - 选项 A：§一 每张卡片完整化，§二 砍掉（Top 3 deep-dive 合并进卡片）
  - 选项 B：§一 每张卡片展示完整 schema，§二 保留作"可落地性 + Sanity"专项
- [ ] 重写 HTML `<details>` 内部结构 + CSS
- [ ] MD 同步

**预估**：核心瓶颈在写 8 个 schema 内容，不在视觉重构。每个 schema ~10-15 行，总计 100-150 行新内容。

---

## P1 — MD 与 HTML 标题对齐（上一轮我提的 3 个 yes/no 你还未拍板）

- [ ] **MD 把 A 股全局约束 promote 成独立 `## A 股全局约束`**（HTML 已经是独立 H2）
- [ ] **MD §二 标题补"与可落地性"**：`## 二、Top 3 字段级 schema 与可落地性`
- [ ] **§三 标题保持口语版 "排序与先做哪几个"**（不要改成"排序与执行优先级"）

我推荐前两个 YES、第三个 NO。等你确认就改。

---

## P1 — 内部数据探索回路

- [ ] ssh 登服务器，git pull，跑 `bash tools/probe_strong_event_datasets.sh > tools/output_strong_event_probe.txt 2>&1`
- [ ] 回 mac，git pull，让 Claude 读 output 解读
- [ ] 重点关注三件事的结论：
  1. StarmineEQMatrix 151 字段里是否含 PEAD / SUE / SURP / DRIFT → 决定 F2 反共识 thesis 是否要重新挂载
  2. 龙虎榜 / longhubang / lhb dataset 是否存在 → 决定 F7 / 类似的资金行为 feature 死活（虽然 F7 已经被砍，但思路存档）
  3. NLPFeature 最新 mtime → 决定 LLM 抽取主线（F3 / F4 / F6 / F8 / F9 / F10）是不是空中楼阁
- [ ] 把找到的内部表名（`cqcache.XXX`）替换进 Deliverable 的 Top 3 数据源行
- [ ] 把发现的红旗（如果 F2 baseline 不成立）写进 `internal_data_findings.md`

---

## P2 — 锦上添花

- [ ] F1（解禁透支度）的学术先例：Field & Hanka (2001) "The Expiration of IPO Share Lockups"
      或更近的中文 A 股解禁研究，主动 cite 一条挡 mentor 拷问。当前只有 F2 引了 Aboody。
- [ ] §0 第二段（方法论站位）可以更紧；现在 4 句，可以压成 3 句。但 v2 humanizer 后已经较稳，
      不优先改。
- [ ] 是否做一张 SVG 图说清 F4 证据等级 × F7 题材相位 × F9 事件因果角色的三轴正交关系
      （类似 thariqs 模板 10-svg-illustrations.html 风格）。视觉收益高，工作量中等。
- [ ] PDF 导出/打印样式：若 mentor 要求 PDF 提交，需加 print CSS。

---

## 已完成（存档，备查）

- 13 → 11 features（砍 4 + 加 2 + F4 双向化）
- §0 加 Source 自检段（4 重构 + 7 AI 解锁）
- §三 加识别策略状态自评（A / B / C 三档）
- F1 Sanity 扩成三层（含 β_unlock vs β_control 的识别策略）
- F7 验收拆三层（PIT 实现 / Filter 速度 / Cycle Mismatch）
- TL;DR 改 3 段（角色 framing → 反共识 → CDE 锚定）
- 全局约束加第 4 条（另类注意力 2022 后断更）
- humanizer-zh 过一遍
- Aboody (2010) 引文加在 F2
- 服务器 probe 脚本写好并 push（commit fea733e on pysim-workspace）
- 6 处英文 → 中文清理（机制 reframe → 机制重构 / identification → 识别 / alignment → 对齐度）
- 保留：Source / baseline / universe / PIT / PEAD / Sanity check 等术语
