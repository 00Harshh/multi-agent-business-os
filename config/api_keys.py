"""
Single local config file for Business OS credentials and API settings.

Paste your keys and local settings here. Environment variables still override
these values, so this file works for local development without blocking deploys.
Do not commit real secrets to a public repository.
"""

# LLM provider: "ollama", "gemini", "openai", or "openrouter".
LLM_PROVIDER = "ollama"

# OpenRouter. Paste your OpenRouter API key here and set
# LLM_PROVIDER = "openrouter" to use OpenRouter.
OPENROUTER_API_KEY = ""
OPENROUTER_MODEL = "meta-llama/llama-3.2-3b-instruct:free"

# Gemini. Paste your Google AI Studio API key here and set
# LLM_PROVIDER = "gemini" to use Gemini 2.5 Flash.
GEMINI_API_KEY = ""
GEMINI_MODEL = "gemini/gemini-2.5-flash"

# Local LLM: Ollama does not need an API key.
OLLAMA_MODEL = "mistral"
OLLAMA_BASE_URL = "http://localhost:11434"

# Optional if you ever switch back to OpenAI or another hosted LLM.
OPENAI_API_KEY = ""
OPENAI_MODEL = "gpt-4o"

# Database URL. Defaults to SQLite. Swap with your Supabase PostgreSQL connection string when ready.
DATABASE_URL = "sqlite:///business_os.db"
# DATABASE_URL = "postgresql://postgres.YOUR_PROJECT_ID:YOUR_PASSWORD@aws-0-us-east-1.pooler.supabase.com:6543/postgres?pgbouncer=true"

# Web search used for market research, lead discovery, LinkedIn public results,
# and Crunchbase public results.
SERPER_API_KEY = ""

# Pinecone Vector Memory (used for storing Crawl4AI scraped knowledge)
PINECONE_API_KEY = ""
PINECONE_INDEX_NAME = "business-os-knowledge"

# Optional direct vendor APIs for future dedicated integrations.
LINKEDIN_API_KEY = ""
CRUNCHBASE_API_KEY = ""

# Integrations.
SLACK_BOT_TOKEN = ""
SENDGRID_API_KEY = ""

# Business context used by lead generation and outreach agents.
COMPANY_NAME = "Acme Corp"
ICP_DESCRIPTION = "B2B SaaS companies with 10-200 employees in the US"
