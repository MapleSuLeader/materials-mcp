# 发布文案草稿（launch posts）— materials-mcp

日期：2026-11-02 ｜ 全部数字来自 2026-11-02 实跑 `test_client.py`（docs/demo-output.txt）
与提案文档（docs/proposal-pricing-acquisition.md）既有出处，无虚构。
GitHub 地址占位：`https://github.com/MapleSuLeader/materials-mcp`（推送后替换全文）。
📸 占位说明：凡标 [SCREENSHOT] 处，发布前用终端录屏/README 顶部截图替换（macOS: `clean` + `script`，或 asciinema）。

---

## 1. Hacker News — Show HN

**标题（<80 chars）**：
> Show HN: I give Claude/Cursor free US construction material prices via MCP (BLS data)

**正文**：

> Steel mill products are up 27.6% year-over-year (BLS WPU1017, Sep 2026 print), while
> the "average material" in RSMeans' 2026 annual report moved just 3.9%. If you're a
> small contractor or estimator using AI agents to help with quotes, that gap is exactly
> where you bleed money — and your agent has no way to see it.
>
> So I built materials-mcp: an MCP server that hands any MCP client (Claude Code, Cursor,
> whatever) the official BLS/FRED price indices for 33 construction material series —
> lumber, rebar, portland cement, insulated wire, copper, aluminum, drywall, concrete —
> with monthly history going back decades.
>
> No API key. FRED publishes a keyless CSV endpoint (fredgraph.csv); the server wraps it
> with a 24h cache and a proxy→direct→curl fallback chain. Three tools:
>
> - `list_materials` — machine-readable catalog of the 33 verified series
> - `get_price_history("STEEL", start_date=...)` — full history, accepts aliases
>   (LUMBER/STEEL/REBAR/CEMENT/WIRE...)
> - `get_price_summary("LUMBER,STEEL,CEMENT")` — batch latest + MoM% + YoY%
>
> Terminal proof from today's run (all series live, latest obs 2026-09-01):
>
> ```
> steel_mill       WPU1017            388.58   YoY +27.58%
> insulated_wire   PCU335929335929F   193.55   YoY +14.2%
> portland_cement  WPU132201          356.21   YoY -1.18%
> lumber           WPU1011            206.60   YoY +0.38%
> ```
>
> [SCREENSHOT: README demo block / asciinema cast of test_client.py]
>
> MIT licensed, ~190 lines of Python in server.py. Dead/discontinued series (BLS killed
> WPU1324 etc. in recent reclassifications) are cataloged and rejected gracefully rather
> than hallucinated.
>
> Honest limits: values are PPI indices (1982=100 base), not dollar prices; data is
> monthly, not spot. A hosted PRO tier (remote streamable-HTTP endpoint, daily refresh,
> alerts) is planned — the local stdio server stays free forever.
>
> Repo: https://github.com/MapleSuLeader/materials-mcp
>
> Would love feedback from anyone in estimating/proptech: does your agent need material
> prices, and what would make you pay vs. RSMeans at $408/yr?

## 2. r/cursor

**标题**：
> Free MCP server: US construction material prices (BLS/FRED, 33 series, no API key) — steel is +27.6% YoY and your agent probably doesn't know

**正文**：

> Made this for anyone doing estimating / construction side projects with Cursor.
>
> What it does: adds 3 tools to Cursor via MCP that pull official US producer price
> indices for building materials — lumber, rebar, cement, wire, copper, drywall, etc.
> (33 verified FRED series, monthly history back decades). No API key, runs locally
> over stdio.
>
> Why it's interesting right now: steel mill products WPU1017 printed **+27.58% YoY**
> (Sep 2026, verified live from the server today), insulated wire +14.2%, while cement
> is flat (-1.2%) and lumber basically unchanged (+0.4%). Generic "material cost +5%"
> assumptions in agent prompts are wrong in both directions depending on the category.
>
> Setup (Cursor → Settings → MCP → Add):
> ```json
> {
>   "mcpServers": {
>     "materials-prices": {
>       "command": "/path/to/.venv/bin/python",
>       "args": ["/path/to/server.py"]
>     }
>   }
> }
> ```
> Then prompt: *"Summarize YoY moves for LUMBER, STEEL, CEMENT, WIRE and flag anything
> over ±10% for my next bid"*.
>
> [SCREENSHOT: Cursor chat calling get_price_summary, real numbers visible]
>
> MIT, repo: https://github.com/MapleSuLeader/materials-mcp
> Hosted remote version planned (that'll be paid); local version stays free.

## 3. r/Construction 或 r/Estimating

（r/Estimating 优先——受众更精准；两边发帖需先过各自 no-self-promo 规则，建议以"工具+数据"姿态，把开源放评论区）

**标题**：
> Data point: BLS says steel mill products +27.6% YoY, RSMeans' 2026 average material is +3.9% — built a free tool so you can check your own categories

**正文**：

> Not selling anything, sharing a dataset + a small tool.
>
> While pricing a bid I kept running into the same problem: published cost books give a
> blended "materials up ~4%" number, but the actual PPI components move wildly apart.
> Latest BLS prints (Sep 2026, via FRED):
>
> - Steel mill products: **+27.6% YoY** (MoM +2.2%)
> - Insulated wire & cable: **+14.2% YoY** (but -6.7% last month — volatile)
> - Portland cement: -1.2% YoY
> - Lumber & wood: +0.4% YoY
>
> If your bid assumes "average" escalation, metals-heavy scopes are under-priced by
> double digits. I wired these official series into an MCP server so an AI assistant
> (Claude/Cursor) can answer "what happened to rebar prices since January?" from BLS
> data directly instead of the model's stale memory. 33 series, keyless, MIT licensed.
>
> [SCREENSHOT: get_price_summary terminal output]
>
> Happy to post the repo link if mods allow; meanwhile curious how you all sanity-check
> material escalation between quarterly cost-book updates — phone calls to suppliers?
> published indices? This is my workaround.

## 4. X thread（5 条，每条 ≤280 chars）

**1/**
> US steel mill products: +27.6% YoY (BLS, Sep 2026).
> The "average material" in RSMeans' 2026 report: +3.9%.
>
> If you're estimating with the average, you're eating a 24-pt miss on every metals-heavy scope.
>
> I built a free MCP server so your AI agent can check the real numbers → 🧵

**2/**
> materials-mcp: 33 verified FRED/BLS construction series — lumber, rebar, cement, wire, copper, aluminum, drywall.
>
> Monthly history back decades. No API key. MIT. Runs locally over stdio in Claude Code, Cursor, any MCP client.
>
> [SCREENSHOT: terminal running test_client.py]

**3/**
> 3 tools:
>
> • list_materials — the catalog
> • get_price_history("STEEL") — full series, aliases work (LUMBER/REBAR/WIRE…)
> • get_price_summary("LUMBER,STEEL,CEMENT") — latest + MoM% + YoY% in one call
>
> Today's live output: steel +27.58% / wire +14.2% / cement −1.18% / lumber +0.38%

**4/**
> Example prompt after install:
>
> "Quote me drywall + rebar cost trends vs 6 months ago and flag anything >10% move before I price this addition."
>
> Agent pulls official BLS data itself. No scraping FRED dashboards, no $408/yr login just to sanity-check one number.

**5/**
> Repo (MIT, ~190 LOC): https://github.com/MapleSuLeader/materials-mcp
>
> Free forever locally. A hosted remote endpoint (daily auto-refresh, alerts) is coming as the paid tier.
>
> Estimators/proptech devs: what series would you watch weekly? Building that next. #buildwithAI #MCP

---

## 发布 checklist

- [ ] 替换全部 `MapleSuLeader` 占位 + 确认仓库公开、About/Topics 已设（topics: `mcp`, `construction`, `pricing`, `fred`, `bls`）
- [ ] 截图 ×3：① README 顶部（含 value prop 行）② test_client.py 终端实跑（demo-output.txt 同款）③ Cursor/Claude Code 内实际调用一帧
- [ ] HN 工作日 14:30–15:30 (UTC) CST≈东八区晚间发帖→对应美东早高峰前；2 小时内在线回评论
- [ ] Reddit：r/Estimating 先发（数据向），r/Construction 隔天再发（改写更软）；自查两版 subreddit rules 的 self-promo 条款
- [ ] X：thread 连发，推文 2 挂 GIF/截图；标签 #MCP #buildwithAI 已含
- [ ] 数字时效：若发布日跨入 11/20 后（10 月 PPI 打印），重跑 `.venv/bin/python test_client.py` 更新 thread #3 与 HN 表格后再发
