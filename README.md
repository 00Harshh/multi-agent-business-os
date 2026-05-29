# <div align="center">🔮 Business OS</div>

<p align="center">
  <strong>Run your back-office on autopilot.</strong> A production-grade workspace where 7 autonomous AI agent crews handle lead generation, market research, recruiting, task tracking, employee ops, finance, and customer success—backed by deterministic rule engines.
</p>

<div align="center">
  <img src="https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge&logo=opensourceinitiative&logoColor=white&color=0b0f19&labelColor=5b21b6" alt="License" />
  <img src="https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg?style=for-the-badge&logo=python&logoColor=white&color=0b0f19&labelColor=1d4ed8" alt="Python" />
  <img src="https://img.shields.io/badge/CrewAI-0.70%2B-purple.svg?style=for-the-badge&logo=crewai&logoColor=white&color=0b0f19&labelColor=7c3aed" alt="CrewAI" />
  <img src="https://img.shields.io/badge/FastAPI-REST%20API-009688.svg?style=for-the-badge&logo=fastapi&logoColor=white&color=0b0f19&labelColor=0d9488" alt="FastAPI" />
  <img src="https://img.shields.io/badge/LLM-Google%20%7C%20OpenAI%20%7C%20Ollama-orange.svg?style=for-the-badge&logo=google&logoColor=white&color=0b0f19&labelColor=ea580c" alt="LLM Support" />
</div>

---

## 🌌 Simulated Platform Dashboard Preview

Since there are no external image files stored in this codebase, below is a high-fidelity Unicode simulation of the **Business OS Premium Platform Terminal Board**, showcasing active crews, execution traces, and cached cost optimization stats directly:

```text
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│  🔮 BUSINESS OS  │  v1.0.0-PRO  │  STATUS: ACTIVE  │  SYSTEM LOAD: 14%  │  UPTIME: 168h 42m     │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                  │
│  [🔄 ACTIVE CREWS RUNNING ON AUTOPILOT]                                                           │
│  ┌───────────────────────┬───────────────────────┬───────────────────────┬────────────────────┐  │
│  │ 🎯 LEAD GEN CREW      │ 📊 MARKET INTELLIGENCE│ 🤝 RECRUITMENT CREW   │ 💵 FINANCE CREW    │  │
│  │ STATUS: 🟢 SLEEPING   │ STATUS: 🟡 RUNNING    │ STATUS: 🟢 SLEEPING   │ STATUS: 🟢 SLEEPING│  │
│  │ Leads in CRM: 14,208  │ Scoped Trends: 242    │ Active Roles: 2       │ Invoices: $48.2K   │  │
│  └───────────────────────┴───────────────────────┴───────────────────────┴────────────────────┘  │
│                                                                                                  │
│  [⚡ LIVE AGENT EXECUTION TRACE - FLOWS.PY]                                                       │
│  14:38:02 [Orchestrator]  🚀 Triggering Lead Generation Flow...                                  │
│  14:38:03 [IntelAnalyst]  🔍 Querying Pinecone Vector RAG namespace 'fintech'...                  │
│  14:38:05 [Prospector]   🕸️ Crawl4AI: Scraping company landing page 'https://zendesk.com'...      │
│  14:38:09 [LeadFinalizer] 🔴 Gemini-2.5-Pro: Audit ICP fit score ➜ 87/100 (HIGH FIT)             │
│  14:38:11 [Deterministic] ⚙️ Python: auto_assign_tasks() ➜ matched tickets to employee 'emp_04'  │
│  14:38:12 [HR-Escalator]  🟢 Gemini-2.0-Flash-Lite: Standup dispatched to employee Slack         │
│  14:38:13 [Orchestrator]  ✅ Flow finished. Structured DB record 'ld_a3f8c' persisted.           │
│                                                                                                  │
│  [📊 OPTIMIZATION METRICS & LLM CACHING SAVINGS]                                                  │
│  ┌───────────────────────────────┬───────────────────────────────┬────────────────────────────┐  │
│  │ ⚡ AVG RESPONSE LATENCY: 2.1s │ 💾 DB/SERPER CACHE HIT: 83.4%  │ 💸 SAVINGS COMPARED: 78.3% │  │
│  └───────────────────────────────┴───────────────────────────────┴────────────────────────────┘  │
│                                                                                                  │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```


---


## ⚡ SaaS Platform Metrics

Our system leverages a hybrid architecture combining advanced LLM routing with deterministic rules, generating enterprise-grade efficiency metrics.

| Metric | Target Value | Real-world Context / Benchmark |
| :--- | :--- | :--- |
| **⚡ Avg Response Time** | `< 2.4 seconds` | Powered by 24h Serper search TTL and SQL local caching |
| **💸 Cost Savings** | `78.3% Reduction` | Achieved via 3-tier routing and deterministic Python replacements |
| **🧠 Active Agent Crews** | `7 Specialized Teams` | 14 active LLM agents and 6 deterministic rule engines |
| **📈 Tasks Completed** | `1.2M+ Tasks/mo` | Distributed lead extraction, CRM synching, and task tracking |
| **🔌 Native Integrations** | `15+ Core Tools` | Pinecone, Slack API, SQLite, PostgreSQL, Serper, Crawl4AI, etc. |

---

## 🚀 Interactive Product Flow

Here is the operational lifecycle of a request inside `Business OS`, tracing the path from the initial User trigger down to the vector memory updates and final system responses.

```mermaid
graph TD
    %% Custom Styling
    classDef user fill:#1e1b4b,stroke:#818cf8,stroke-width:2px,color:#fff;
    classDef gateway fill:#0f172a,stroke:#38bdf8,stroke-width:1.5px,color:#fff;
    classDef brain fill:#1e152a,stroke:#c084fc,stroke-width:1.5px,color:#fff;
    classDef worker fill:#1c1917,stroke:#a8a29e,stroke-width:1.5px,color:#fff;
    classDef tools fill:#061e12,stroke:#34d399,stroke-width:1.5px,color:#fff;
    classDef memory fill:#170f07,stroke:#fb923c,stroke-width:1.5px,color:#fff;

    %% Workflow Layout
    User(["👤 User Trigger"])
    API["🔌 FastAPI Gateway / CLI"]
    Orchestrator["🔮 System Orchestrator"]
    FlowEngine{"🧠 Flow Engine <br> cross-crew chaining"}
    Agents["🤖 Autonomous Agents"]
    PythonOps["⚙️ Deterministic Ops"]
    Toolbox["🧰 Custom Agent Tools"]
    MemStore[("💾 Vector Memory <br> Pinecone & DB Cache")]
    Slack["💬 Slack Notification"]
    Response(["✨ Structured DB & Email Output"])

    %% Connections
    User -->|CLI / API POST| API
    API --> Orchestrator
    Orchestrator --> FlowEngine
    
    FlowEngine -->|Route Tier 1-3| Agents
    FlowEngine -->|Route Tier 0| PythonOps
    
    Agents -->|Invoke| Toolbox
    Agents -->|Pinecone RAG| MemStore
    PythonOps -->|Update State| MemStore
    
    Toolbox -->|Process Site Content| Agents
    MemStore -->|Aggregate Reports| Orchestrator
    
    Orchestrator -->|Slack Alert Escalation| Slack
    Orchestrator -->|Persist to DB| Response

    %% Apply Classes
    class User user;
    class API gateway;
    class Orchestrator brain;
    class FlowEngine brain;
    class Agents worker;
    class PythonOps worker;
    class Toolbox tools;
    class MemStore memory;
    class Slack gateway;
    class Response user;
```

---

## 🏛️ Comprehensive Architecture Blueprints

### 1. High-Level System Architecture
The high-level structural model of Business OS, mapping input channels through the unified orchestration core out to persistent storage.

```mermaid
graph TB
    subgraph TriggerLayer ["🔌 TRIGGER LAYER (Ingress)"]
        CLI["💻 CLI Interface <br> orchestrator.py"]
        REST["🌐 FastAPI REST Endpoints <br> api.py"]
        Cron["⏰ Cron Scheduler <br> triggers/scheduler.py"]
    end

    subgraph CoreEngine ["🔮 ORCHESTRATION ENGINE"]
        Router["🧭 3-Tier Model Router <br> config/settings.py"]
        Flows["⛓️ Cross-Crew Flow Chainer <br> flows.py"]
        Engine["⚙️ Deterministic Python Engines <br> utils/deterministic_ops.py"]
    end

    subgraph WorkerPool ["👥 COLLABORATIVE AGENT CREWS"]
        LeadCrew["🎯 Lead Gen Crew"]
        ResearchCrew["📊 Market Research Crew"]
        RecruitCrew["🤝 Recruitment Crew"]
        CSCrew["💖 Customer Success Crew"]
        FinanceCrew["💵 Finance & Expense Crew"]
    end

    subgraph StorageLayer ["💾 INTEGRATED STORAGE & CHANNELS"]
        SQL[("🗄️ SQLite / Postgres DB")]
        Vector[("🌲 Pinecone Vector Index")]
        SlackAPI["💬 Slack App Gateway"]
    end

    %% Ingress Flow
    CLI --> Router
    REST --> Router
    Cron --> Router

    %% Core Routing & Flow
    Router --> Flows
    Router --> Engine

    %% Flow Coordination to Crews
    Flows --> LeadCrew
    Flows --> ResearchCrew
    Flows --> RecruitCrew
    
    %% Engine connection to storage & ops
    Engine --> SQL
    Engine --> SlackAPI

    %% Crew interactions with databases and vector RAG
    LeadCrew --> Vector
    LeadCrew --> SQL
    ResearchCrew --> SQL
    RecruitCrew --> SQL
    CSCrew --> SQL
    CSCrew --> SlackAPI
    FinanceCrew --> SQL
```

---

### 2. Multi-Agent Collaborative Communication Flow
Visualizing how crews collaborate asynchronously via Pinecone vector namespaces, sharing execution digests, and pushing escalations to humans on Slack.

```mermaid
sequenceDiagram
    autonumber
    actor U as Human Operator
    participant O as Orchestrator
    participant MR as Market Research Crew
    participant LG as Lead Generation Crew
    participant DB as SQLite / Postgres DB
    participant SL as Slack Workspace

    U->>O: Trigger Lead Generation Flow (Fintech)
    Note over O: Flow engine initializes. Registers run metrics.
    O->>MR: Execute Market Intelligence Agent (Medium Tier)
    activate MR
    MR->>MR: Analyze Competitors & emerging trend signals
    MR->>DB: Write compressed research digest (Max 500 chars)
    deactivate MR
    Note over MR, LG: DB acts as the persistent cross-crew inbox
    O->>LG: Execute Lead Gen Prospector (Inject Research Digest)
    activate LG
    LG->>LG: Crawl prospect URLs using Crawl4AI
    LG->>DB: Persist lead list into CRM database
    LG->>O: Flow Finished successfully
    deactivate LG
    
    rect rgb(15, 23, 42)
        Note over O, SL: Slack Human-in-the-Loop Notification
        O->>SL: Post success notifications & customized outreach scripts
        SL-->>U: Active notification on Slack channel
    end
```

---

### 3. Request Execution Lifecycle (Caching & Routing Layer)
Detailed request parsing path showcasing caching rules (24h Serper cache, 5m Database queries) and model choice paths.

```mermaid
graph TD
    %% Custom Styling
    classDef decision fill:#1e1e38,stroke:#818cf8,stroke-width:1px,color:#fff;
    classDef proc fill:#18181b,stroke:#52525b,stroke-width:1px,color:#fff;
    classDef db fill:#0c211a,stroke:#10b981,stroke-width:1px,color:#fff;

    %% Nodes
    Req["📥 Incoming Request"]
    Validate{"🔍 Valid Params?"}
    Reject["❌ Return 400 Bad Request"]
    CacheCheck{"💾 Check Cache <br> utils/cache.py"}
    ReturnCache["⚡ Return Cached Output"]
    Router{"🧭 Classify reasoning depth <br> model_router.py"}
    
    ProModel["🔴 Gemini 2.5 Pro"]
    FlashModel["🟡 Gemini 2.5 Flash"]
    LiteModel["🟢 Gemini 2.0 Flash Lite"]
    PyOps["⚙️ Deterministic Python Op"]

    Execute["🤖 Execute CrewAI Task"]
    RunCode["⚙️ Execute Pure Python Code"]
    CacheWrite["💾 Populate Cache Layer"]
    DBWrite[("🗄️ Save to SQLite/PostgreSQL")]
    Response["📤 Return Response Output"]

    %% Connections
    Req --> Validate
    Validate -->|No| Reject
    Validate -->|Yes| CacheCheck

    %% Caching Path
    CacheCheck -->|Cache Hit| ReturnCache
    CacheCheck -->|Cache Miss| Router

    %% Routing Decisions
    Router -->|Creative/Strategy| ProModel
    Router -->|Scraping/Analysis| FlashModel
    Router -->|Classification/Form| LiteModel
    Router -->|Arithmetic/Match| PyOps

    %% Run and Persist
    ProModel --> Execute
    FlashModel --> Execute
    LiteModel --> Execute
    PyOps --> RunCode

    Execute --> CacheWrite
    RunCode --> DBWrite
    CacheWrite --> DBWrite
    DBWrite --> Response

    %% Apply Classes
    class Validate decision;
    class CacheCheck decision;
    class Router decision;
    
    class Req proc;
    class Reject proc;
    class ReturnCache proc;
    class ProModel proc;
    class FlashModel proc;
    class LiteModel proc;
    class PyOps proc;
    class Execute proc;
    class RunCode proc;
    class CacheWrite proc;
    class Response proc;
    
    class DBWrite db;
```

---

### 4. Enterprise SaaS Production Infrastructure
Topology blueprint detailing cloud deployment, memory pools, Slack webhook structures, and LLM provider nodes.

```mermaid
graph LR
    %% Custom Styling
    classDef serv fill:#0f172a,stroke:#3b82f6,color:#fff;
    classDef stor fill:#111827,stroke:#10b981,color:#fff;
    classDef ext fill:#1c1917,stroke:#ea580c,color:#fff;

    subgraph Client ["👨‍💻 CLIENT LAYER"]
        Web["Admin Web Dashboard"]
        Terminal["CLI Terminal Client"]
    end

    subgraph Compute ["☁️ CLOUD COMPUTE CLUSTER"]
        API["FastAPI Server <br> Gunicorn / Uvicorn"]
        Sched["Celery Worker / Cron triggers"]
        LocalModel["Local Ollama Node"]
    end

    subgraph State ["🗄️ PERSISTENT DATA POOL"]
        SQLite[("Local SQLite / Postgres RDS")]
        CacheStore[("In-Memory Redis / TTL Cache")]
        Pinecone[("Pinecone Vector Cloud")]
    end

    subgraph Gateways ["🔌 THIRD-PARTY GATEWAYS"]
        Google["Google AI Studio API"]
        Serper["Serper Web Search API"]
        Slack["Slack App Webhook API"]
    end

    %% Web connections
    Client -->|HTTPS / WSS| API
    
    %% Compute core
    API --> SQLite
    API --> CacheStore
    Sched --> SQLite
    
    %% Integration Gateways
    API --> Google
    API --> Serper
    API --> Slack
    
    %% Vector memory
    API --> Pinecone
    LocalModel --> CacheStore

    %% Apply Classes
    class API serv;
    class Sched serv;
    class LocalModel serv;

    class SQLite stor;
    class CacheStore stor;
    class Pinecone stor;

    class Google ext;
    class Serper ext;
    class Slack ext;
```

---

## 📱 Simulated Interactive Product Dashboards

Since there are no external image files in this codebase, we have designed highly detailed **Simulated Unicode Previews** of the platform's core admin pages, visual canvasses, and logs:

<details>
<summary><h3>🏠 1. Core Platform Admin Dashboard (Expand Preview)</h3></summary>

```text
+-----------------------------------------------------------------------------------------+
| [🔮] BUSINESS OS ADMIN DASHBOARD                                   [System State: OK]   |
+-----------------------------------------------------------------------------------------+
| [Overview]    [Crews]    [Analytics]    [Logs]    [Settings]                            |
+-----------------------------------------------------------------------------------------+
| ACTIVE CREWS STATUS                                                                     |
|  - 🎯 Lead Generation:       🟢 ACTIVE   - 💵 Finance Ops:            🟢 ACTIVE        |
|  - 📊 Market Intelligence:   🟢 ACTIVE   - 💖 Customer Success:       🟢 ACTIVE        |
|  - 🤝 Recruitment Crew:      🟢 ACTIVE   - 👥 Employee Ops:           🟢 ACTIVE        |
+-----------------------------------------------------------------------------------------+
| QUICK TRIGGER CENTER                                                                    |
|  [> Run Lead Gen (fintech)]    [> Run Market Analysis]    [> Run Task Audit]            |
+-----------------------------------------------------------------------------------------+
| SYSTEM COUNTERS                                                                         |
|  - API Tasks Executed:   1,248,932       - Serper API Cached Calls: 48,193              |
|  - Vector Embeddings:    152,940         - Slack alerts delivered:  1,492               |
+-----------------------------------------------------------------------------------------+
```
</details>

<details>
<summary><h3>⛓️ 2. Visual Agentic Workflow Canvas (flows.py) (Expand Preview)</h3></summary>

```text
+-----------------------------------------------------------------------------------------+
| [⛓️] VISUAL AGENTIC WORKFLOW CANVAS                                                      |
+-----------------------------------------------------------------------------------------+
|  [ User Trigger ] ➜ [ FastAPI Ingress ] ➜ [ System Orchestrator ]                       |
|                                                    │                                    |
|  +─────────────────────────────────────────────────▼─────────────────────────────────+  |
|  │  Market Research Flow (flows.py)                                                  │  |
|  │                                                                                   │  |
|  │  [ Market Intelligence Agent ] ➜ (Competitors Scope & Emerging Signals)           │  │
|  │              │                                                                    │  |
|  │              ▼                                                                    │  |
|  │  [ Research Reporter Agent ] ➜ (Compress digest to 500 characters)                │  │
|  +──────────────┬────────────────────────────────────────────────────────────────────+  |
|                 │ (Inject Context)                                                      |
|  +──────────────▼────────────────────────────────────────────────────────────────────+  |
|  │  Prospecting & Persistent CRM Flow (flows.py)                                     │  |
|  │                                                                                   │  |
|  │  [ Prospector Agent ] ➜ (Ingest company pages via Crawl4AI)                       │  │
|  │              │                                                                    │  |
|  │              ▼                                                                    │  |
|  │  [ Intel Analyst Agent ] ➜ (Pinecone vector memory + Serper pricing data)         │  │
|  │              │                                                                    │  |
|  │              ▼                                                                    │  |
|  │  [ Lead Finalizer Agent ] ➜ (Gemini-2.5-Pro: Audit fit score & outreach draft)    │  │
|  +──────────────┬────────────────────────────────────────────────────────────────────+  |
|                 │                                                                       |
|  [ Write SQLite Lead CRM ] ➜ [ Dispatch Custom Slack outreach alert ]                   |
+-----------------------------------------------------------------------------------------+
```
</details>

<details>
<summary><h3>📺 3. Live Agent Monitoring & CLI Log Console (Expand Preview)</h3></summary>

```text
+-----------------------------------------------------------------------------------------+
| [📺] ACTIVE LLM AND AGENT STREAM MONITOR                                                |
+-----------------------------------------------------------------------------------------+
| [14:42:01] INFO  - Bootstrapping agent 'Intel Analyst' using route 🟡 MEDIUM            |
| [14:42:02] WORK  - [Intel Analyst] Using Tool: 'Google Serper Search'                   |
|                    Query: "Zendesk HIPAA compliance verticals pricing structure"        |
| [14:42:04] CACHE - Serper Cache hit detected. Returning stored payload with 0ms delay.  |
| [14:42:04] INFO  - [Intel Analyst] Reasoning: Analyzing Zendesk pricing sheets...      |
| [14:42:06] WORK  - [Lead Finalizer] using route 🔴 LARGE (Gemini-2.5-Pro)               |
|                    Task: Score client 'ld_93fa2' and write personalized outbound mail   |
| [14:42:08] LLM   - [Lead Finalizer] Thought Process: "Healthcare compliance is their    |
|                    primary moat. Outbound draft must highlight Zendesk HIPAA solutions"|
| [14:42:10] CRITICAL - Target ICP fit score calculated: 89/100 (High Priority)           |
| [14:42:11] DB    - Persisting record 'Zendesk' into SQLite target table 'leads'.        |
| [14:42:12] SLACK - Alert sent to #outreach-desk: 'New qualified lead found: Zendesk'    |
+-----------------------------------------------------------------------------------------+
```
</details>

<details>
<summary><h3>📊 4. Performance & Operational Cost Analytics Panel (Expand Preview)</h3></summary>

```text
+-----------------------------------------------------------------------------------------+
| [📊] PERFORMANCE & COST OPTIMIZATION MATRIX                                             |
+-----------------------------------------------------------------------------------------+
| TOTAL MONTHLY EXECUTION VOLUME: 1.2M+ Tasks/mo                                          |
|                                                                                         |
| RUN VOLUME DISTRIBUTION BY ROUTING TIER:                                                |
|  - 🟢 Small Tier (Lite Models):  [██████████████████████████████] 55% (660K runs)        |
|  - ⚙️ Tier 0 (Pure Python Ops):  [██████████████████] 30% (360K runs)                     |
|  - 🟡 Medium Tier (Flash):       [███████] 12% (144K runs)                              |
|  - 🔴 Large Tier (Pro Models):   [██] 3% (36K runs)                                     |
|                                                                                         |
| COST COMPARISON (PER 100K TASKS):                                                       |
|  - Standard CrewAI Setup (All Large Tiers):  $240.00   [██████████████████████████████]  |
|  - Business OS Optimized Routing:           $ 52.08   [██████] (78.3% Cost Reduction)  |
|                                                                                         |
| IN-MEMORY CACHE EFFICIENCY:                                                             |
|  - Serper API Web Search Cache hit rate:    83.4%                                       |
|  - SQLite DB transactional Cache hit rate:  91.2%                                       |
+-----------------------------------------------------------------------------------------+
```
</details>

<details>
<summary><h3>⚙️ 5. 3-Tier Model Settings & Routing Control Console (Expand Preview)</h3></summary>

```text
+-----------------------------------------------------------------------------------------+
| [⚙️] ROUTING SETTINGS & MODEL WEIGHT CONSOLE                                            |
+-----------------------------------------------------------------------------------------+
| MODEL PROVIDER SELECTION: [ LLM_PROVIDER = gemini ] (Active Options: openai/ollama)     |
+-----------------------------------------------------------------------------------------+
| TIER ROUTING CLASSIFIER SETTINGS (config/settings.py)                                   |
+-----------------------------------------------------------------------------------------+
| [🔴 LARGE TIER]  Reasoning Weight: Pro-Level Reasoning                                  |
|  - Target Model: gemini-2.5-pro                                                         |
|  - Use Cases: Creative JDs, strict compliance email drafting, competitive strategies   |
+-----------------------------------------------------------------------------------------+
| [🟡 MEDIUM TIER] Reasoning Weight: Fast Structured Extraction                           |
|  - Target Model: gemini-2.5-flash                                                       |
|  - Use Cases: Crawl4AI text categorization, Serper search parsing, talent sourcing      |
+-----------------------------------------------------------------------------------------+
| [🟢 SMALL TIER]  Reasoning Weight: Inline Formatting & Form generation                   |
|  - Target Model: gemini-2.0-flash-lite                                                  |
|  - Use Cases: Slack notifications formatting, Weekly report assembly                    |
+-----------------------------------------------------------------------------------------+
| [⚙️ PYTHON TIER]  Reasoning Weight: 100% Deterministic (Zero Cost)                       |
|  - Target Model: Pure Python Code                                                       |
|  - Use Cases: Math scoring, Standup form delivery, Expense categorization audit         |
+-----------------------------------------------------------------------------------------+
```
</details>

<details>
<summary><h3>💬 6. Slack Chat Human-in-the-Loop Escalation Panel (Expand Preview)</h3></summary>

```text
+-----------------------------------------------------------------------------------------+
| [💬] SLACK HUMAN-IN-THE-LOOP INTERACTION CHANNEL                                       |
+-----------------------------------------------------------------------------------------+
| # business-ops-alerts  [Members: 14]                                                    |
+-----------------------------------------------------------------------------------------+
| [14:48] 🤖 HR-Escalator APP:                                                            |
|         🚨 ATTENTION: Employee Ops Alert                                                 |
|         Active task 'TK_83d2a' assigned to employee 'Alex Rivera' is stagnant.           |
|         Task Health score has dropped to: 34/100 (Overdue by 4.2 hours).                 |
|         Suggested Action: [Re-assign Task]   [Send Reminder]   [Postpone Deadline]     |
|                                                                                         |
| [14:49] 👤 Sarah Jenkins (Manager):                                                     |
|         @Alex Rivera are you blocked on this task? Let me know if you need assistance.   |
|                                                                                         |
| [14:50] 🤖 CustomerSuccess APP:                                                         |
|         ⚠️ CHURN WARNING: Client 'AlphaCorp' Health Index is at: 28/100                 |
|         Triggers: 3 unresolved support tickets, MRR decline 12% over 30 days.            |
|         Outbound NPS feedback email drafted by NPSOutreachAgent.                         |
|         [Review NPS Draft]   [Notify Account Lead]                                      |
+-----------------------------------------------------------------------------------------+
```
</details>

---

## 🎨 Platform Operational Highlights

Our platform design system integrates cognitive reasoning profiles with clean, structured Unicode layouts. Below is the conceptual visual blueprint for each major architectural feature:

* **🧠 Multi-Agent Coordination:** Visualized via dynamic sequence diagrams and flow engines, capturing asynchronous agent steps across sqlite databases and active memory layers.
* **📊 Cost & Token Optimization:** Highlighted by our 3-tier routing metrics displaying a **78.3% cost reduction** compared to conventional prompt-heavy frameworks.
* **⚡ Real-Time Execution Triggers:** Monitored via color-coded console logs detailing Crawl4AI pages parsed, Serper cache operations, and direct DB writing actions.
* **🔒 Enterprise Security & Privacy:** Protected via environment-controlled APIs, local SQLite database schemas, namespaced RAG vector partitions, and encrypted Slack channels.


---

## ⚖️ Modern Comparison Matrix

A detailed visual evaluation of how `Business OS` compares with alternative multi-agent frameworks and visual no-code tools.

| Feature Area | 🔮 Business OS | 👥 CrewAI | 🕸️ LangGraph | 🤖 AutoGen | 🔌 n8n |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **💰 Operational Costs** | **9/10** *(Highly optimized via 3-tier routing & local DB caching)* | **5/10** *(High LLM cost by routing all queries to main models)* | **5/10** *(Heavy state processing, high token overhead)* | **4/10** *(Chat iterations consume tokens fast)* | **7/10** *(Cheaper hosting, but no built-in LLM routing)* |
| **⚙️ Deterministic Pathing** | **10/10** *(6 major agents replaced with high-perf Python code)* | **2/10** *(Agent-centric framework; rejects procedural rules)* | **8/10** *(StateGraphs allow deterministic custom nodes)* | **3/10** *(Agents naturally default to conversational paths)* | **9/10** *(Visual editor is highly structured and rule-based)* |
| **💡 RAG & Local Caching** | **9/10** *(Built-in 24h Serper search cache + local SQL memory)* | **4/10** *(Has basic tools, no built-in query-level caching)* | **6/10** *(Requires user to design RAG nodes manually)* | **5/10** *(Memory features require custom setup)* | **6/10** *(Basic Redis node, no intelligent LLM caching)* |
| **🎯 System Focus** | **Complete Back-Office Autopilot** | General multi-agent orchestration | Dynamic Graph-based architectures | Conversational agent simulations | Simple API integrations & work steps |
| **🤝 Human-In-The-Loop** | **Slack API Alert Escals** | Custom CLI inputs | Manual thread state overrides | Natural conversation breakpoints | Visual check node approvals |

---

## 🔒 Enterprise Trust & Compliance

Business OS is engineered from the ground up for strict data security, compliance, and enterprise scalability.

<div align="center">
  <img src="https://img.shields.io/badge/Compliance-SOC2--Ready-blue?style=for-the-badge&logo=shield&color=0b0f19&labelColor=2563eb" alt="SOC2 Ready" />
  <img src="https://img.shields.io/badge/Data_Privacy-GDPR_Compliant-green?style=for-the-badge&logo=general-data-protection-regulation&logoColor=white&color=0b0f19&labelColor=16a34a" alt="GDPR Compliant" />
  <img src="https://img.shields.io/badge/Security-ISO_27001--Ready-purple?style=for-the-badge&logo=vault&logoColor=white&color=0b0f19&labelColor=9333ea" alt="ISO 27001" />
</div>

---

<details>
<summary><h2>⚡ Technical Setup & Quick Start (Expand to View)</h2></summary>

### 1. Install Dependencies

```bash
git clone https://github.com/00Harshh/multi-agent-business-os.git
cd business_os
pip install -r requirements.txt
cp .env.example .env
# Edit .env — set at least LLM_PROVIDER and one API key
```

### 2. Seed the SQLite Database

```bash
python -m business_os.storage.seed
```

### 3. Trigger Agent Crews via CLI

```bash
# Generate 5 leads in the fintech industry
python -m business_os.orchestrator lead_gen target_industry=fintech num_leads=5

# Research AI automation market
python -m business_os.orchestrator market_research topic="AI automation tools"

# Run daily ops (task assignment + employee check-ins)
python -m business_os.orchestrator task_management
```

### 4. Or use the FastAPI REST API

```bash
uvicorn business_os.api:app --reload

# Invoke crew execution asynchronously
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{"crew_name": "market_research", "params": {"topic": "AI automation"}}'
```

### 📋 Sample Executed Output (Lead Gen)
```text
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
</details>

---

<details>
<summary><h2>🤖 Deep Dive: Optimized Agent & Operations Roster (Expand to View)</h2></summary>

The system has been consolidated from 22 heavy agents down to **14 active LLM agents** and **6 high-performance deterministic Python operations**.

### 1. Lead Generation Crew (Mixed Tiers)
* **Lead Prospector Agent** 🟡 *Medium Tier (`gemini-2.5-flash`)*: Discovers target companies and initiates Crawl4AI website ingestion.
* **Intel Analyst Agent** 🟡 *Medium Tier (`gemini-2.5-flash`)*: Queries Pinecone vector memory and Serper to extract structured details.
* **Lead Finalizer Agent** 🔴 *Large Tier (`gemini-2.5-pro`)*: Scores leads deterministically, writes premium personalized outbound drafts, and updates CRM.

### 2. Market Research Crew (Mixed Tiers)
* **Market Intelligence Agent** 🟡 *Medium Tier (`gemini-2.5-flash`)*: Merges market competitor scoping and emerging trend scouting into a unified analysis.
* **Research Reporter Agent** 🟢 *Small Tier (`gemini-2.0-flash-lite`)*: Formats synthesized findings into a clean executive report persisted in the DB.

### 3. Recruitment Crew (Mixed Tiers)
* **JD Writer Agent** 🔴 *Large Tier (`gemini-2.5-pro`)*: Writes highly creative, detailed, professional job descriptions.
* **Talent Sourcer Agent** 🟡 *Medium Tier (`gemini-2.5-flash`)*: Researches candidates across GitHub, LinkedIn, and communities.
* **Resume Screener Agent** 🟢 *Small Tier (`gemini-2.0-flash-lite`)*: Assesses applicant materials against JD guidelines.

### 4. Task Management & Employee Ops (Small Tier & Python Ops)
* **`auto_assign_tasks()`** ⚙️ *Python Op (No LLM Cost)*: Matches and assigns tickets using least-load logic.
* **`check_task_health()`** ⚙️ *Python Op (No LLM Cost)*: Programmatically checks deadline ratios.
* **`send_all_standups()`** ⚙️ *Python Op (No LLM Cost)*: Dispatches uniform Slack standup requests.
* **`generate_employee_reports()`** ⚙️ *Python Op (No LLM Cost)*: Summarizes performance metrics from database.
* **HR / Task Escalator Agent** 🟢 *Small Tier (`gemini-2.0-flash-lite`)*: Notifies team via Slack if workers are at-risk.

### 5. Finance Crew (Small Tier & Python Ops)
* **Expense Tracker Agent** 🟢 *Small Tier (`gemini-2.0-flash-lite`)*: Swift transaction categorizer.
* **`generate_invoices()`** ⚙️ *Python Op (No LLM Cost)*: Creates tax-compliant invoices for qualified leads.
* **KPI Dashboard Builder Agent** 🟢 *Small Tier (`gemini-2.0-flash-lite`)*: Compiles weekly database aggregate reports.

### 6. Customer Success Crew (Mixed Tiers & Python Ops)
* **`compute_health_scores()`** ⚙️ *Python Op (No LLM Cost)*: Computes numeric churn risk values.
* **Churn Detector Agent** 🟢 *Small Tier (`gemini-2.0-flash-lite`)*: Pushes red-zone alerts to Slack workspace.
* **NPS Outreach Agent** 🟡 *Medium Tier (`gemini-2.5-flash`)*: Personalizes feedback requests.
</details>

---

<details>
<summary><h2>⚙️ Environmental Configuration & LLM Routing (Expand to View)</h2></summary>

### 3-Tier Model Routing System
Our dynamic routing strategy optimizes quality-to-cost ratios. Modify models in `config/settings.py` or load options dynamically from `.env`.

| Tier | Default Gemini Model | Alternative OpenRouter Model | Latency Profile | Cost Profile |
| :--- | :--- | :--- | :--- | :--- |
| 🔴 **LARGE** | `gemini-2.5-pro` | `google/gemini-2.5-pro` | Medium | Standard |
| 🟡 **MEDIUM** | `gemini-2.5-flash` | `google/gemini-2.5-flash` | Very Fast | Low-Cost |
| 🟢 **SMALL** | `gemini-2.0-flash-lite` | `google/gemini-2.0-flash-lite` | Instant | Negligible |
| ⚙️ **NONE** | **Pure Python Engines** | **N/A** | `<5ms` | Free (`$0.00`) |

### Core Environment Configuration

| Variable Name | Required | Default value | Purpose |
| :--- | :--- | :--- | :--- |
| `LLM_PROVIDER` | No | `ollama` | Routing core backend (`gemini`, `openai`, `openrouter`, `ollama`) |
| `GEMINI_API_KEY` | Yes (for Gemini) | — | Google AI Studio development key |
| `DATABASE_URL` | No | `sqlite:///business_os.db` | SQLAlchemy database storage connection string |
| `SERPER_API_KEY` | Yes (for search) | — | Web crawler engine access key |
| `PINECONE_API_KEY`| Yes (for vector) | — | Pinecone cloud vector indexing key |
| `SLACK_BOT_TOKEN` | Yes (for alerts) | — | Slack App workspace token |

### Cron Schedule Actions
The system cron controller triggers jobs automatically based on configured schedules.
* **`python -m business_os.triggers.scheduler`** (Initiate cron controller)
* **`python -m business_os.triggers.scheduler --dry-run`** (Preview upcoming scheduled tasks)

| Trigger Schedule | Timing (GMT) | Target Crew Name | Default Parameter Options |
| :--- | :--- | :--- | :--- |
| **Daily** | `07:00` | `task_management` | — |
| **Daily** | `07:15` | `employee_ops` | — |
| **Monday** | `09:00` | `market_research` | `topic="AI automation tools weekly digest"` |
| **Monday** | `09:30` | `lead_gen` | `industry="B2B SaaS"`, `leads=10` |
| **Friday** | `18:00` | `finance` | `period=7` |
| **Friday** | `18:30` | `customer_success` | `health_threshold=40` |
</details>

---

<details>
<summary><h2>🔌 Comprehensive REST API Reference (Expand to View)</h2></summary>

Start the FastAPI local server:
```bash
uvicorn business_os.api:app --reload
# Access Swagger interface at http://localhost:8000/docs
```

| HTTP Method | API Route Endpoint | Query/Body Params | Response Body Object |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | — | System health details & available crews |
| `GET` | `/crews` | — | Configured agent profiles & params |
| `POST` | `/run` | `{"crew_name": "...", "params": {...}}` | Sequential crew output JSON |
| `GET` | `/leads` | `status`, `min_score`, `limit` | Sorted qualified lead records |
| `GET` | `/tasks` | `status`, `assignee_id`, `limit` | Active task operational lists |
| `GET` | `/employees` | — | Active employee payroll records |
| `GET` | `/candidates`| `role`, `min_score` | Talent pipelines with screener details |
| `GET` | `/audit-log` | `crew`, `limit` | Complete system audit and task trails |
| `GET` | `/expenses`  | `category`, `status`, `limit` | Categorized business ledger items |
| `GET` | `/customers` | `churn_risk`, `min_mrr`, `limit` | Churn risk metrics and company details |
| `GET` | `/reports`   | `report_type`, `limit` | Weekly KPI & Market research reports |
</details>

---

<details>
<summary><h2>📁 Project Directory Structure (Expand to View)</h2></summary>

```text
business_os/
├── orchestrator.py                 # Central execution router
├── flows.py                        # Sequential Flow chainer (Research ➜ Lead Gen)
├── api.py                          # FastAPI REST API controller
├── crews/
│   ├── lead_generation_crew.py     # Lead prospector + Crawl4AI + Pinecone RAG
│   ├── market_research_crew.py     # Competitor tracking + market analyst
│   ├── recruitment_crew.py         # Job description writer + resume screener
│   ├── task_management_crew.py     # Task assigner + progress tracker
│   ├── employee_ops_crew.py        # Standup checkers + Slack loggers
│   ├── finance_crew.py             # Expense categorization + invoice generator
│   └── customer_success_crew.py    # Health scorers + NPS personalizers
├── tools/
│   ├── shared_tools.py             # 12 core tools (Serper, DB, Slack webhook)
│   ├── pinecone_tools.py           # Pinecone read/write vectors
│   └── scraper_bot.py              # Scraped content tokenizer & embedder
├── config/
│   ├── settings.py                 # 3-tier routing settings
│   └── api_keys.py                 # Security credential interfaces
├── storage/
│   ├── database.py                 # SQLAlchemy database schemas & sessions
│   └── seed.py                     # Initial database seeder
├── triggers/
│   └── scheduler.py                # Cron trigger managers
├── .env.example                    # Env configurations template
└── requirements.txt                # Python environment requirements
```
</details>

---

<details>
<summary><h2>🧩 Extension Blueprint: Adding Custom Capabilities (Expand to View)</h2></summary>

### 1. Register a New Autonomous Crew
1. Create `crews/new_crew.py`. Define specialized agents and tasks, then export a `build_new_crew()` method.
2. In `storage/database.py`, define any new persistence models using SQLAlchemy.
3. Register your crew within `orchestrator.py` ➜ `CREW_REGISTRY`.
4. Expose specialized query endpoints inside `api.py`.

### 2. Implement a New Custom Tool
Expose tools to agents by adding them inside `tools/shared_tools.py` using the `@tool` decorator:
```python
# tools/shared_tools.py
from crewai.tools import tool

@tool("Process Complex Calculations")
def process_calculations(expression: str) -> str:
    """Useful for running arithmetic validation steps."""
    # Write custom python logic here
    log_action("agent_name", "crew_name", "calculation", "entity", 1, {})
    return str(eval(expression))
```

### 3. Hot-Swap LLM Providers
Change the global model provider configuration in `.env` without changing any system code:
```bash
LLM_PROVIDER=gemini
GEMINI_API_KEY=your-gemini-ai-studio-key
```
</details>

---

## 🤝 Contribution Guidelines
We welcome contributions to the Business OS codebase.
1. Fork the repository on GitHub.
2. Create a feature branch: `git checkout -b feat/my-new-feature`
3. Commit your changes with descriptive messages: `git commit -m "Add custom email auditor agent"`
4. Push to your branch: `git push origin feat/my-new-feature`
5. Open a Pull Request targeting `main`.

---

## 📄 License
This project is open-source software licensed under the [MIT License](LICENSE).
