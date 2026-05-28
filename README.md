# Business OS

**Run your back-office on autopilot.** 7 AI agent crews handle lead gen, market research, hiring, task tracking, employee ops, finance, and customer success — while you focus on building.

```
                        ┌──────────────────────────────────────────────────────┐
                        │               BUSINESS OS PIPELINE                   │
                        │                                                      │
  CLI / API / Cron ───▶ │  Orchestrator ──▶ Crew 1 ──▶ Crew 2 ──▶ ... ──▶ DB │
                        │       │                                         │    │
                        │       └── Flow Engine (cross-crew chaining) ────┘    │
                        │                        │                             │
                        │              Pinecone Vector Memory                  │
                        │              Slack Alerts & Reports                   │
                        └──────────────────────────────────────────────────────┘
```

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-brightgreen.svg)
![CrewAI](https://img.shields.io/badge/CrewAI-0.70%2B-purple.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-REST%20API-009688.svg)
![LLM](https://img.shields.io/badge/LLM-Ollama%20%7C%20Gemini%20%7C%20OpenAI%20%7C%20OpenRouter-orange.svg)

---

## 🎯 What This Does

Business OS replaces manual back-office work with autonomous agent crews. Each crew is a team of specialized AI agents that collaborate, use real tools, and write results to a shared database.

You give it a trigger. It gives you back structured, actionable output.

| Use Case | You Provide | What the Crew Does | You Get Back |
|---|---|---|---|
| **B2B Lead Generation** | Target industry, lead count | Market Research crew finds trends → Lead Gen crew scrapes company sites into vector memory → Intelligence agent extracts pricing & contacts → Auditor writes hyper-personalized cold emails | Qualified leads in CRM with ICP scores + ready-to-send outreach emails |
| **Market Intelligence** | A topic (e.g., "AI automation tools") | Market Analyst maps competitors → Trend Scout finds emerging signals → Reporter synthesizes everything | Executive-ready research report saved to DB |
| **Automated Hiring Pipeline** | Role title + requirements | JD Writer drafts the posting → Talent Sourcer searches LinkedIn/GitHub → Resume Screener scores and saves | Job description + scored candidate pipeline |
| **Weekly Finance Ops** | Nothing (runs on schedule) | Expense Tracker categorizes spend → Invoice Generator drafts invoices for qualified leads → KPI Builder computes weekly metrics | Categorized expenses, invoices, and a KPI dashboard report |

> **"I'm a founder who needs…"** leads without cold-calling → run `lead_gen`
>
> **"I'm a VP Eng who needs…"** to know which tasks are blocked → run `task_management`
>
> **"I'm a CS lead who needs…"** churn alerts before it's too late → run `customer_success`

---

## 🏗 Architecture

### The Full Pipeline

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           TRIGGER LAYER                                 │
│   ┌─────────┐    ┌──────────────────┐    ┌────────────────────────┐    │
│   │   CLI   │    │   FastAPI REST   │    │   Cron Scheduler       │    │
│   │         │    │   POST /run      │    │   Daily 07:00, 07:15   │    │
│   │         │    │   GET /leads     │    │   Mon  09:00, 09:30    │    │
│   │         │    │   GET /reports   │    │   Fri  18:00, 18:30    │    │
│   └────┬────┘    └────────┬─────────┘    └───────────┬────────────┘    │
│        └──────────────────┼──────────────────────────┘                  │
│                           ▼                                             │
│                  ┌─────────────────┐                                    │
│                  │  ORCHESTRATOR   │                                    │
│                  │  orchestrator.py│                                    │
│                  └────────┬────────┘                                    │
│                           │                                             │
│              ┌────────────┼─────────────┐                              │
│              ▼            ▼             ▼                               │
│     ┌────────────┐ ┌───────────┐ ┌───────────────┐                    │
│     │ Flow Engine│ │Direct Crew│ │ Daily Ops     │                    │
│     │ (chained)  │ │ Execution │ │ Cycle         │                    │
│     └────────────┘ └───────────┘ └───────────────┘                    │
└─────────────────────────────────────────────────────────────────────────┘
```

### Lead Gen Flow — Cross-Crew Chaining in Action

This is the most advanced pipeline. Two crews execute in sequence, with the first crew's output injected as context into the second:

```
  ┌────────────────────────── LEAD GEN FLOW (flows.py) ──────────────────────────┐
  │                                                                               │
  │  PHASE 1: Market Intelligence                                                 │
  │  ┌──────────────┐    ┌──────────────┐    ┌──────────────────┐                │
  │  │Market Analyst │──▶│ Trend Scout  │──▶│ Research Reporter │                │
  │  │              │    │              │    │                  │                │
  │  │ Serper search│    │ Serper search│    │ Save report to DB│                │
  │  └──────────────┘    └──────────────┘    └────────┬─────────┘                │
  │                                                    │                          │
  │                              ┌─────────────────────┘                          │
  │                              ▼                                                │
  │                   ╔══════════════════════╗                                    │
  │                   ║  CONTEXT INJECTION   ║                                    │
  │                   ║  Research report is   ║                                    │
  │                   ║  injected into Lead   ║                                    │
  │                   ║  Gen Crew's first task║                                    │
  │                   ╚══════════╤═══════════╝                                    │
  │                              ▼                                                │
  │  PHASE 2: Targeted Prospecting                                                │
  │  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐   ┌─────────────┐  │
  │  │Lead Prospector│──▶│Intel Analyst │──▶│CRM & Outreach│──▶│  Compliance │  │
  │  │              │    │              │    │   Manager    │   │   Auditor   │  │
  │  │Serper search │    │Pinecone query│    │Deterministic │   │Save to CRM  │  │
  │  │Crawl4AI      │    │Serper search │    │ICP scoring   │   │Email QA     │  │
  │  │  + Pinecone  │    │              │    │Email drafting│   │             │  │
  │  └──────────────┘    └──────────────┘    └──────────────┘   └─────────────┘  │
  │       │                    │                                       │          │
  │       ▼                    ▼                                       ▼          │
  │  ┌──────────┐       ┌──────────┐                            ┌──────────┐     │
  │  │ Pinecone │◀─────▶│ Pinecone │                            │ SQLite / │     │
  │  │ (write)  │       │ (read)   │                            │ Postgres │     │
  │  └──────────┘       └──────────┘                            └──────────┘     │
  └───────────────────────────────────────────────────────────────────────────────┘
```

> **Why this works:** Most AI lead gen tools search and blast. Business OS does research *first* — it maps the market landscape, identifies pain points, then prospects into those exact niches. The Lead Prospector scrapes target websites into vector memory, the Intel Analyst queries that same memory for pricing tiers and tech stacks, and the Outreach Manager writes cold emails referencing *actual facts from their website*. A compliance auditor catches hallucinated placeholders before anything hits the CRM.

### How Crews Collaborate

Agents don't run in isolation. Four coordination mechanisms keep them in sync:

| Mechanism | How It Works | Example |
|---|---|---|
| **Cross-Crew Flows** | CrewAI Flow chains crews sequentially, injecting output as context | Market Research report feeds into Lead Gen prospecting |
| **Shared Database** | SQLite/Postgres acts as a persistent message board between crews | Finance crew reads leads table to generate invoices |
| **Vector Memory Pool** | Pinecone stores scraped website content as embeddings | Prospector writes, Intel Analyst reads the same vectors |
| **Slack Escalations** | Crews post alerts to human workspaces for high-priority events | Task Management sends overdue alerts; Customer Success sends churn warnings |

---

## ⚡ Quick Start

### 1. Install

```bash
git clone https://github.com/00Harshh/multi-agent-business-os.git
cd business_os
pip install -r requirements.txt
cp .env.example .env
# Edit .env — set at least LLM_PROVIDER and one API key
```

### 2. Seed the database

```bash
python -m business_os.storage.seed
```

### 3. Run a crew

```bash
# Generate 5 leads in the fintech industry
python -m business_os.orchestrator lead_gen target_industry=fintech num_leads=5

# Research AI automation market
python -m business_os.orchestrator market_research topic="AI automation tools"

# Run daily ops (task assignment + employee check-ins)
python -m business_os.orchestrator task_management
```

### 4. Or use the REST API

```bash
uvicorn business_os.api:app --reload

# Then:
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{"crew_name": "market_research", "params": {"topic": "AI automation"}}'
```

### Sample output (lead gen)

```
Lead 'Zendesk' successfully saved (ID: a3f8c..., ICP Score: 85/100)

Business Model & Pain Points:
Enterprise helpdesk SaaS with HIPAA-compliant verticals. Custom pricing for
healthcare networks. High-margin enterprise tier starting at $150/seat/month.

High-Margin Indicators:
Enterprise pricing tier, custom quotes, verticalized compliance packages

--- CUSTOM COLD OUTREACH EMAIL ---
Subject: Scaling Zendesk's healthcare compliance outreach

Hi Mikkel,

I recently came across Zendesk and was impressed by your dedicated focus on
providing HIPAA-compliant, verticalized solutions for healthcare networks...
```

---

## 🤖 Agent Roster

### Lead Generation Crew

| Agent | Role | Tools | Output |
|---|---|---|---|
| Lead Prospector | Discover target companies and scrape their websites | Web Search, Crawl4AI + Pinecone | List of real prospects indexed in vector memory |
| Intel Analyst | Extract pricing, tech stack, contacts from scraped data | Pinecone Query, Web Search | Deep intelligence profiles per prospect |
| Outreach Manager | Score leads and draft personalized cold emails | Deterministic ICP Scorer, DB Query | ICP scores + bespoke outreach drafts |
| Compliance Auditor | QA email drafts, reject placeholders, save to CRM | Save Lead to CRM, DB Query | Polished leads persisted to database |

### Market Research Crew

| Agent | Role | Tools | Output |
|---|---|---|---|
| Market Analyst | Map competitors, market size, funding activity | Web Search | Structured market overview |
| Trend Scout | Identify 5 emerging trends with evidence | Web Search | Trends with time horizons |
| Research Reporter | Synthesize into executive-ready report | Save Report | Report saved to database |

### Recruitment Crew

| Agent | Role | Tools | Output |
|---|---|---|---|
| JD Writer | Craft compelling job descriptions | — | Ready-to-post job description |
| Talent Sourcer | Find candidates on LinkedIn, GitHub, communities | Web Search | 10 candidate profiles |
| Resume Screener | Score candidates against requirements, save top ones | Save Candidate | Scored candidate pipeline |

### Task Management Crew

| Agent | Role | Tools | Output |
|---|---|---|---|
| Task Assigner | Match unassigned tasks to employees by role and load | Assign Task, DB Query | Tasks assigned with deadlines |
| Progress Tracker | Monitor in-progress tasks, flag at-risk ones | Get Employee Tasks, Get Overdue, DB Query | Progress health report |
| Escalation Agent | Send Slack alerts for blocked/overdue tasks | Get Overdue, Slack, Log Progress | Slack notifications sent |

### Employee Operations Crew

| Agent | Role | Tools | Output |
|---|---|---|---|
| Check-in Bot | Send daily standup prompts to all employees | Get Employees, Slack | Standup messages delivered |
| Progress Logger | Compile task reports, find stale updates | DB Query, Employee Report | Stale-update employee list |
| HR Operations Bot | Flag overloaded or disengaged employees | Get Employees, Employee Report, Slack, DB Query | Burnout alerts + utilization flags |

### Finance Crew

| Agent | Role | Tools | Output |
|---|---|---|---|
| Expense Tracker | Categorize uncategorized expenses, flag outliers | DB Query, Save Expense, Expenses Summary, Categorize | Categorized expenses with flags |
| Invoice Generator | Draft invoices for qualified leads | DB Query, Save Report | Invoice reports saved |
| KPI Dashboard Builder | Compute weekly business KPIs | DB Query, Expenses Summary, Save Report | Weekly KPI dashboard report |

### Customer Success Crew

| Agent | Role | Tools | Output |
|---|---|---|---|
| Health Scorer | Compute health score (0–100) for every customer | DB Query, Update Customer Health | Health scores + churn risk levels |
| Churn Detector | Alert team on at-risk accounts via Slack | DB Query, Slack, Save Report | Slack churn alerts + report |
| NPS Outreach Agent | Draft check-in emails for healthy customers | DB Query, Save Report | NPS outreach email drafts |

---

## ⚙️ Configuration

### LLM Provider

Business OS supports four LLM backends. Set `LLM_PROVIDER` in your `.env`:

| Provider | `LLM_PROVIDER` | API Key Needed | Default Model |
|---|---|---|---|
| Ollama (local) | `ollama` | None | `llama3.1` |
| Google Gemini | `gemini` | `GEMINI_API_KEY` | `gemini/gemini-2.5-flash` |
| OpenAI | `openai` | `OPENAI_API_KEY` | `gpt-4o` |
| OpenRouter | `openrouter` | `OPENROUTER_API_KEY` | `google/gemini-2.5-flash:free` |

### Environment Variables

| Variable | Required | Default | Purpose |
|---|---|---|---|
| `LLM_PROVIDER` | No | `ollama` | LLM backend to use |
| `OPENROUTER_API_KEY` | If using OpenRouter | — | OpenRouter API key |
| `OPENROUTER_MODEL` | No | `google/gemini-2.5-flash:free` | OpenRouter model name |
| `GEMINI_API_KEY` | If using Gemini or Pinecone | — | Google AI Studio key (also used for embeddings) |
| `GEMINI_MODEL` | No | `gemini/gemini-2.5-flash` | Gemini model name |
| `OLLAMA_MODEL` | No | `llama3.1` | Ollama model name |
| `OLLAMA_BASE_URL` | No | `http://localhost:11434` | Ollama server URL |
| `OPENAI_API_KEY` | If using OpenAI | — | OpenAI API key |
| `OPENAI_MODEL` | No | `gpt-4o` | OpenAI model name |
| `DATABASE_URL` | No | `sqlite:///business_os.db` | SQLAlchemy connection string |
| `SERPER_API_KEY` | For web search | — | Serper.dev API key |
| `PINECONE_API_KEY` | For vector memory | — | Pinecone API key |
| `PINECONE_INDEX_NAME` | No | `business-os-knowledge` | Pinecone index name |
| `SLACK_BOT_TOKEN` | For Slack alerts | — | Slack bot OAuth token |
| `SENDGRID_API_KEY` | No | — | SendGrid key (future) |
| `COMPANY_NAME` | No | `Acme Corp` | Company name used in agent outputs |
| `ICP_DESCRIPTION` | No | `B2B SaaS companies with 10-200 employees in the US` | Ideal customer profile for lead scoring |

> **⚠️ Never commit real API keys.** The `.env` file is gitignored. Use `.env.example` as your template.

### Scheduled Jobs

The cron scheduler runs crews automatically:

```bash
python -m business_os.triggers.scheduler        # Start scheduler
python -m business_os.triggers.scheduler --dry-run  # Preview schedule
```

| Schedule | Time | Crew | Default Params |
|---|---|---|---|
| Daily | 07:00 | `task_management` | — |
| Daily | 07:15 | `employee_ops` | — |
| Monday | 09:00 | `market_research` | topic: "AI automation tools weekly digest" |
| Monday | 09:30 | `lead_gen` | industry: "B2B SaaS", leads: 10 |
| Friday | 18:00 | `finance` | period: 7 days |
| Friday | 18:30 | `customer_success` | health_threshold: 40 |

---

## 📊 Example Outputs

### Market Research Report

```
══════════════════════════════════════════════════
  MARKET RESEARCH REPORT: AI Automation Tools
  Report ID: rpt_7a3c1e
══════════════════════════════════════════════════

EXECUTIVE SUMMARY
The AI automation market is projected at $14.2B (2025), growing 32% YoY.
Key segments: RPA + AI copilots, autonomous agents, and workflow orchestration.

TOP 5 COMPETITORS
1. UiPath      — Enterprise RPA. $1.3B revenue. Focus: regulated industries.
2. Zapier AI   — SMB workflow automation. 7M+ users. Focus: no-code AI actions.
3. Make.com    — Visual automation builder. Growing 45% YoY in EU markets.
4. n8n         — Open-source alternative. 40K GitHub stars. Self-hosted focus.
5. CrewAI      — Multi-agent framework. Fastest-growing in agent orchestration.

TOP 5 TRENDS
1. Agent-to-agent orchestration (3-month horizon)
2. RAG-powered enterprise copilots (1-year horizon)
3. Vertical AI agents for compliance-heavy industries (1-year horizon)
4. Open-source agent frameworks replacing SaaS (3-year horizon)
5. Human-in-the-loop guardrails as a product category (3-month horizon)

RECOMMENDATIONS
1. Target regulated verticals (healthcare, finance) where compliance is a moat.
2. Build RAG pipelines as a core differentiator over prompt-only competitors.
3. Ship agent audit trails — enterprises will require them for procurement.
```

### Weekly KPI Dashboard

```
══════════════════════════════════════════════════
  WEEKLY KPI REPORT — May 23, 2025
══════════════════════════════════════════════════

LEAD PIPELINE
  New leads this week:       12
  Average ICP score:         67/100
  Leads qualified:           8
  Outreach emails drafted:   8

TASK OPERATIONS
  Tasks completed:           23
  Tasks overdue:             3
  Tasks blocked:             1

HIRING PIPELINE
  Active roles:              2
  Candidates in pipeline:    18
  Avg fit score:             72/100

WEEKLY BURN RATE
  SaaS:        $2,340.00
  Marketing:   $1,875.00
  Travel:      $890.00
  Payroll:     $12,500.00
  ─────────────────────
  Total:       $17,605.00

CUSTOMER HEALTH
  Active customers:          34
  At-risk (health < 40):     4
  Churn alerts sent:         2
```

### Invoice Draft

```
══════════════════════════════════════════════════
  INVOICE INV-a3f8c291
══════════════════════════════════════════════════

Bill To:    Zendesk, Inc.
Contact:    Mikkel Svane
Date:       2025-05-23
Due Date:   2025-06-22

Line Items:
  1. Consulting Services — AI Integration      $8,500.00
  2. Platform Access Fee — Enterprise Tier      $2,400.00
                                               ──────────
  Subtotal:                                    $10,900.00
  Tax (18%):                                    $1,962.00
                                               ──────────
  TOTAL DUE:                                   $12,862.00
```

---

## 📁 Project Structure

```
business_os/
├── orchestrator.py          # Central entry point — routes crews by name
├── flows.py                 # Cross-crew Flow engine (Market Research → Lead Gen)
├── api.py                   # FastAPI REST layer with 10 endpoints
├── crews/
│   ├── lead_generation_crew.py     # 4 agents, Crawl4AI + Pinecone pipeline
│   ├── market_research_crew.py     # 3 agents, web search → report
│   ├── recruitment_crew.py         # 3 agents, JD → source → screen
│   ├── task_management_crew.py     # 3 agents, assign → track → escalate
│   ├── employee_ops_crew.py        # 3 agents, standup → log → HR flags
│   ├── finance_crew.py             # 3 agents, expenses → invoices → KPIs
│   └── customer_success_crew.py    # 3 agents, health → churn → NPS
├── tools/
│   ├── shared_tools.py      # 12 reusable tools (search, DB, Slack, etc.)
│   ├── pinecone_tools.py    # Vector memory read/write tools
│   └── scraper_bot.py       # Crawl4AI scraper + Gemini embeddings
├── config/
│   ├── settings.py          # Multi-provider LLM builder + env config
│   └── api_keys.py          # Placeholder defaults (never commit real keys)
├── storage/
│   ├── database.py          # SQLAlchemy models (Lead, Task, Employee, etc.)
│   └── seed.py              # Sample data seeder
├── triggers/
│   └── scheduler.py         # Cron-style job scheduler
├── .env.example             # Environment variable template
└── requirements.txt         # Python dependencies
```

---

## 🔌 REST API Reference

Start the server:

```bash
uvicorn business_os.api:app --reload
# Docs at http://localhost:8000/docs
```

| Method | Endpoint | Params | Returns |
|---|---|---|---|
| `GET` | `/` | — | Service status + registered crew names |
| `GET` | `/crews` | — | Crew descriptions and accepted params |
| `POST` | `/run` | `{"crew_name": "...", "params": {...}}` | Crew execution result |
| `GET` | `/leads` | `status`, `min_score`, `limit` | Leads ordered by ICP score |
| `GET` | `/tasks` | `status`, `assignee_id`, `limit` | Tasks with progress data |
| `GET` | `/employees` | — | Active employee records |
| `GET` | `/candidates` | `role`, `min_score` | Recruitment pipeline |
| `GET` | `/audit-log` | `crew`, `limit` | Agent action audit trail |
| `GET` | `/expenses` | `category`, `status`, `limit` | Expense records |
| `GET` | `/customers` | `churn_risk`, `min_mrr`, `limit` | Customer health data |
| `GET` | `/reports` | `report_type`, `limit` | Reports with content previews |

---

## 🧩 Extending Business OS

### Add a new crew

1. Create `crews/your_crew.py` — define agents, tasks, and `build_your_crew()`
2. Add DB models to `storage/database.py` if needed
3. Add tools to `tools/shared_tools.py` with `@tool` decorator
4. Register in `orchestrator.py` → `CREW_REGISTRY`
5. Add API endpoints in `api.py` for any new tables

### Swap the LLM

Change one line in `.env`:

```bash
LLM_PROVIDER=gemini          # or: ollama, openai, openrouter
GEMINI_API_KEY=your-key-here
```

All 22 agents switch to the new provider. No code changes.

### Add a tool

```python
# tools/shared_tools.py
from crewai.tools import tool

@tool("Your New Tool")
def your_tool(param: str) -> str:
    """Description of what it does."""
    # Your logic here
    log_action("agent_name", "crew_name", "action", "entity", entity_id, {})
    return "result"
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Commit changes: `git commit -m "Add your feature"`
4. Push: `git push origin feat/your-feature`
5. Open a Pull Request

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.
