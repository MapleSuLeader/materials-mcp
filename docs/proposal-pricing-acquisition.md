# 定价与获客落地提案（海外建材价格 MCP）

日期：2026-10-28 ｜ 状态：基于真实证据的 v1 ｜ 关联：series_catalog.json / server.py

## 1. 市场锚点（全部有出处，非拍脑袋）

| 事实 | 数据 | 来源 |
|---|---|---|
| 行业标杆贵且重 | RSMeans Core 订阅 $408/年起，Complete $1,049/年起，主流成本库 $2,000–7,000/人/年，企业级 $25,000+/年 | rsmeans.com 产品页、meltplan.com 行业综述 |
| 痛点正热 | 2026 前两个月非住宅建材价格年化 +12.6%；建材 PPI 3 月创历史新高 354.9（YoY +6.0%） | Coherent MI 援引 ABC 数据 |
| 关税冲击可量化 | 本 server 实测：钢材厂产品指数 YoY **+27.58%**（WPU1017，2026-09: 388.58）；绝缘电缆 YoY +14.2%；2026 RSMeans 年报材料均值仅 +3.9% → 金属类波动远超均值，正是小承包商报价盲区 | test_client.py 实跑输出 + bdcnetwork |
| 竞品空档 | GitHub 仅 trades-mcp(★1)/buildwatch-mcp(★0)；1build(YC) 做企业 API 不服务散户；EstimationPro 有免费 API 但非 MCP、无长历史 | 前期调研 + 本轮搜索 |

结论：**$408/年 RSMeans 与 $0 免费网页之间存在 MCP 原生价格带（$60–300/年）**，买家是"用 AI Agent 报价的独立估算师/小承包商/proptech 开发者"。

## 2. 产品分层与定价

| 层 | 内容 | 价格 | 目的 |
|---|---|---|---|
| **Free（开源本地版）** | stdio MCP server 全部 33 序列 + 工具三件套，MIT，GitHub 发布 | $0 | 获客钩子、star、SEO；数据本身免费（BLS），不心疼 |
| **Pro（托管远程 MCP）** | streamable-http 端点（境外 VPS，国内用户无墙阻）、每日自动更新、别名+多序列对比、图表导出链接、SLA | **$19/月 或 $150/年**（前 100 名 $99/年 早鸟） | 主力营收；对标 RSMeans 仅 37% 价格 |
| **Team/API** | 无限序列自定义、CSV 快照归档（投标留证）、Webhook 价格警报（月报邮件）、API key | **$79/月** | 估算师事务所/小型 proptech |
| 增值（后期） | "把报价单拍给我→Agent 自动做价差分析" 的 prompt 模板包；关税情景推演 | $29 一次性 | 提高 LTV |

成本结构：VPS ~$10/月 + 域名，无数据授权费（BLS 公版，引用即可）。**毛利≈95%，盈亏平衡 ≈ 8 个 Pro 订阅。**

## 3. 获客路径（按 ROI 排序，前 6 周执行）

1. **GitHub 开源引流（W1）**：`materials-mcp` 仓库，README 带实跑 GIF/终端录屏（test_client.py 输出就是最好 demo），提交 mcp.so / Smithery / Cursor Directory / mcpservers.org 四个目录。目标：100 star。
2. **数据故事发帖（W1–2）**：关税叙事自带流量——"2026 美国钢材 PPI 同比 +27.6%，我用 30 行 Python + MCP 让 Claude 帮我盯价"。发 HN Show、r/Construction、r/Estimating、r/cursor、X(#buildwithAI)。每条附真实数字截图。
3. **估算师社群渗透（W2–4)**：Commercial Estimating Facebook 群、BuildCamp 等社区做 10 个免费 Pro 内测码换访谈；关键验证问题：*你现在报价前怎么查最近三个月钢材价？愿意为省 30 分钟/次付多少钱？*
4. **MCP 原生生态位（W4–6）**：给 Projul/Element/Joist 等小 SaaS 发合作邮件（"内嵌我们的 MCP，你的用户就能问 AI 材料趋势"），B2B2C 一条 API 单 = $79/月 Team 层。
5. **SEO 长尾（持续）**：落地页 `lumber-ppi-2026.com` 类程序化页面（每序列一页，数据自动生成），吃"steel price index 2026"搜索流量 → 转化注册托管版。

## 4. 验证指标与止损线

- W2：目录收录完成，GitHub star ≥50，帖子上 HN 首页或 r/Construction ≥200 upvotes
- W4：≥10 个访谈，≥5 人进内测，**≥2 人愿付（预付或信用卡挂账）**
- W8：托管版付费 ≥8 人（盈亏平衡）或 ≥20 个内测活跃；否则 pivoting：
  - 备选 A：改卖"关税价差监控 + 邮件警报"单点工具（$9/月，更轻）
  - 备选 B：只做开源 + 接单定制（给 proptech 做数据管道咨询）
- 反信号处理：若访谈显示承包商根本不碰 AI Agent → 转向 proptech 开发者单客（1build 服务不到的长尾开发者）。

## 5. 风险与对策

| 风险 | 对策 |
|---|---|
| 直连 FRED 在国内被墙（本环境经代理验证，直连未剥离测试） | 托管版本就跑境外 VPS；本地版提供 BASE_URL 镜像开关；已实测代理/直连/curl 三级回退 |
| EstimationPro 等免费 API 跟进 MCP | 他们数据是零售装修向、无 1982 起长历史；以"官方 BLS 序列 + 40 年回溯"卡位 |
| 指数≠美元绝对价，客户预期错位 | 文档明示 + Pro 层增加"指数→典型品类美元价"换算锚点（引用 BLS 发布表） |
| BLS 转载条款 | 公开数据注明来源即可（FRED copyright 提示已在 README 声明） |

## 6. 本周就能做的三件事

1. 开源推送 GitHub + 提交 4 个 MCP 目录（半天）
2. 用 get_price_summary 真实输出写 HN 帖 + 3 个 subreddit 帖（半天）
3. 上线 Waitlist 落地页（ Carrd/Framer，$0–20），跑通"star→waitlist→内测码"漏斗（1 天）
