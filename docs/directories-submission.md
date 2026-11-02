# MCP 目录提交材料包（materials-mcp）

状态：2026-11-02 web 核实。占位符 `https://github.com/<GH_USER>/materials-mcp` 待用户注册 GitHub 后替换。
所有文案草稿见文末「通用字段文案」，各目录直接复制。

> ⚠️ 2026 年生态变动提示：Smithery 被 Arcade.dev 收购，其 proxy/hosting（`*.smithery.ai` 运行端点）
> 已于 2026-10-31 关停，现仅剩纯目录；mcp.so 有第三方报告（2026-10 底）称免费提审队列暂停、
> 仅 $39 premium 通道畅通。两家均收录但把"托管类提交"留到 PRO 版上线，本地 stdio 版走各自允许的仓库/URL 提交路径。

---

## 1. mcp.so

- **提交入口**：https://mcp.so/submit ✅ 已核实在线（页面标题 "Submit your project"）
- **登录方式**：需 Sign In（https://mcp.so/sign-in）；具体 OAuth 提供商未能匿名核实 → **待验证**（惯例为 GitHub OAuth，注册 GitHub 账号后优先试 GitHub 登录）
- **机制**：粘贴 repo/server URL → 自动抓取 README/元数据 → 人工 review 后上架（官网 FAQ 原话 "Listings go live after review"）
- **风险提示**：apideck/linkly 2026-10/11 两份独立综述均提到 mcp.so 免费队列暂停、$39 一次性 premium 为当时唯一可见通道。先走免费提审，被排队 2 周+再考虑付费。
- **表单字段草稿**：
  - Repository URL: `https://github.com/<GH_USER>/materials-mcp`
  - Name: `materials-mcp`（自动抓取）
  - Description: 用文末通用 description
  - Category/Tags: `data` / `finance-prices` / `construction`（以表单实际选项就近选择）
  - Transport: `stdio`

## 2. Smithery

- **提交入口**：https://smithery.ai/new （官方文档 https://smithery.ai/docs/build/publish ✅ 已核实）
- **⚠️ 适配性**：现publish流程要求 **public HTTPS Streamable-HTTP 端点**（"Bring your own hosting — Smithery Gateway proxies to your upstream"）。本仓库是本地 stdio 开源版，**当前不满足**，文档也未说明纯目录条目如何新增（Arcade 接管后入口未定 → **待验证**）。
- **行动项**：挂到 PRO 托管版上线（有 VPS streamable-http 端点）后再提交，10 分钟即可；提交时走 URL publish 流。
- **登录方式**：Smithery 历史支持 GitHub OAuth → 现状待验证
- **表单字段草稿（PRO 阶段）**：Server URL: `https://mcp.<domain>/materials`（占位）；其余元数据自动扫描，或提供 `/.well-known/mcp/server-card.json`

## 3. Glama

- **提交入口**：https://glama.ai/mcp/servers 页面右上角 **"Add MCP Server"** 按钮（FAQ ✅ 已核实："On the servers page, click Add MCP Server and fill in…"；注：/mcp/submit、/add-server 等直链 404，勿用）
- **登录方式**：**GitHub OAuth** ✅（methodology 页明确："maintainer authenticates through GitHub OAuth… verifies write/admin access to the repository"）— 满足"只用 GitHub 不用 Gmail"的要求
- **机制**：从 GitHub repo 直接提交；也可让 repo 自动被爬（~24h）。建议加 `glama.json` 控制展示元数据：
  ```json
  {
    "$schema": "https://glama.ai/mcp/server-schema.json",
    "maintainers": ["<GH_USER>"],
    "name": "materials-mcp",
    "description": "US construction material price indices (BLS/FRED, 33 series) for AI agents. No API key.",
    "category": "data"
  }
  ```
- **表单字段草稿**：GitHub repo URL `https://github.com/<GH_USER>/materials-mcp`；display name / tagline / category 同上

## 4. mcpservers.org (Awesome MCP Servers, punkpeye)

- **提交入口**：https://mcpservers.org/submit ✅ 已核实在线（"Submit Your MCP Server — Listings are free"，premium 可选）
- **机制**：表单提交 repo URL，自动读 GitHub 元数据（该站由 punkpeye/awesome-mcp-servers 仓库驱动，仓库 README 明示不收 PR、走网站表单 ✅）
- **登录方式**：站点支持 GitHub OAuth 登录（同生态惯例）→ 提交是否强制登录 **待验证**（表单可能匿名可用）
- **表单字段草稿**：
  - GitHub URL: `https://github.com/<GH_USER>/materials-mcp`
  - Name: `Materials Prices (US Construction PPI)`
  - Description: 通用 description（见文末）
  - Category: `Finance`（有该分类 ✅）或 `Other`；本站另有 Marketing 分类，勿选
  - Logo：默认抓 repo，无则留空

## 5. Cursor Directory（提案原清单含此项 → 五目录）

- **提交入口**：https://cursor.directory/plugins/new ✅ 已核实在线（"Submit a Plugin — Auto-detect from a GitHub repo or create one manually"，遵循 Open Plugins 标准）
- **登录方式**：**待验证**（提交流程匿名可达表单页；Cursor Directory 历史用 GitHub 账号关联 repo 作者）
- **机制**：粘贴 GitHub repo → 自动检测 README/mcp.json 生成条目。建议 repo 内保留 `.mcp.json` 示例块（README 已含）；若自动检测失败，手填：
  - Name: `materials-mcp`
  - Description: 通用 description
  - MCP config 片段（README Quick-start 中的 JSON）
- **备注**：它现在按 "plugins"（rules+MCP 混合）生态收条目，MCP server 提交入口与旧版 URL 略有差异 → 现场以表单为准

---

## 提交顺序建议

1. **Glama**（GitHub OAuth 最确定、审核自动化、会被 mcp.so 等聚合）
2. **mcpservers.org**（免费、表单简单）
3. **Cursor Directory**（目标用户=Cursor 重度人群，与本产品的 coding-agent 场景最贴）
4. **mcp.so**（免费队列若确实暂停 → 记入待办，$39 视 star 增长再决定）
5. **Smithery**（deferred，等 PRO 托管端点）

提交时间窗：GitHub 仓库公开后 **当天** 提 1–4（Glama 自动爬取约 24h，抢先手动提交可绑定 maintainer 身份）。

## 通用字段文案（英文，直接粘贴）

- **Name**: `materials-mcp`
- **Tagline (≤80 chars)**: `US construction material prices for AI agents — 33 FRED series, no API key`
- **Description (≈2 段)**:
  > materials-mcp is an MCP server that gives Claude Code, Cursor, and any MCP client
  > direct access to US construction-material price indices (PPI) from FRED (BLS data),
  > with no API key. 33 verified series: lumber, steel mill products, rebar, portland
  > cement, insulated wire, copper, aluminum, drywall, concrete and more — with monthly
  > history back decades.
  >
  > Three tools: `list_materials` (machine-readable catalog), `get_price_history`
  > (single series with aliases like LUMBER/STEEL/REBAR), and `get_price_summary`
  > (batch latest value + MoM% + YoY%). Real hook: steel mill products +27.6% YoY
  > (Sep 2026) vs +3.9% average in RSMeans' 2026 report — the volatility gap your
  > agent can now see. Free, MIT, runs locally over stdio; hosted PRO endpoint planned.
- **Repo URL**: `https://github.com/<GH_USER>/materials-mcp`
- **License**: MIT
- **Transport**: stdio（本地）
- **关键词/标签**: `mcp`, `construction`, `ppi`, `fred`, `bls`, `pricing`, `estimating`
