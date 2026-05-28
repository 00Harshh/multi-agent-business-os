import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables from .env file before settings are evaluated
load_dotenv()

from business_os.config import api_keys


def config_value(env_name: str, fallback):
    return os.getenv(env_name, fallback)


@dataclass
class Settings:
    llm_provider: str = config_value("LLM_PROVIDER", api_keys.LLM_PROVIDER)
    openrouter_api_key: str = config_value("OPENROUTER_API_KEY", api_keys.OPENROUTER_API_KEY)
    openrouter_model: str = config_value("OPENROUTER_MODEL", api_keys.OPENROUTER_MODEL)
    gemini_api_key: str = config_value("GEMINI_API_KEY", api_keys.GEMINI_API_KEY)
    gemini_model: str = config_value("GEMINI_MODEL", api_keys.GEMINI_MODEL)
    ollama_model: str = config_value("OLLAMA_MODEL", api_keys.OLLAMA_MODEL)
    ollama_base_url: str = config_value("OLLAMA_BASE_URL", api_keys.OLLAMA_BASE_URL)
    openai_api_key: str = config_value("OPENAI_API_KEY", api_keys.OPENAI_API_KEY)
    model_name: str = config_value("OPENAI_MODEL", api_keys.OPENAI_MODEL)
    db_url: str = config_value("DATABASE_URL", api_keys.DATABASE_URL)
    slack_token: str = config_value("SLACK_BOT_TOKEN", api_keys.SLACK_BOT_TOKEN)
    sendgrid_key: str = config_value("SENDGRID_API_KEY", api_keys.SENDGRID_API_KEY)
    serper_api_key: str = config_value("SERPER_API_KEY", api_keys.SERPER_API_KEY)
    linkedin_api_key: str = config_value("LINKEDIN_API_KEY", api_keys.LINKEDIN_API_KEY)
    crunchbase_api_key: str = config_value("CRUNCHBASE_API_KEY", api_keys.CRUNCHBASE_API_KEY)
    company_name: str = config_value("COMPANY_NAME", api_keys.COMPANY_NAME)
    icp_description: str = config_value(
        "ICP_DESCRIPTION", api_keys.ICP_DESCRIPTION
    )
    pinecone_api_key: str = config_value("PINECONE_API_KEY", api_keys.PINECONE_API_KEY)
    pinecone_index_name: str = config_value("PINECONE_INDEX_NAME", api_keys.PINECONE_INDEX_NAME)

    def __post_init__(self):
        # Automatically populate environment variables for LiteLLM and external clients
        if self.gemini_api_key:
            os.environ["GEMINI_API_KEY"] = self.gemini_api_key
        if self.openrouter_api_key:
            os.environ["OPENROUTER_API_KEY"] = self.openrouter_api_key
        if self.serper_api_key:
            os.environ["SERPER_API_KEY"] = self.serper_api_key
        if self.pinecone_api_key:
            os.environ["PINECONE_API_KEY"] = self.pinecone_api_key

    def build_llm(self, model_name: str = None):
        """Build the CrewAI LLM object used by all agents."""
        from crewai import LLM

        if self.llm_provider.lower() == "openrouter":
            return LLM(
                model=model_name or self.openrouter_model,
                api_key=self.openrouter_api_key or None,
                base_url="https://openrouter.ai/api/v1",
                provider="openai",
            )

        if self.llm_provider.lower() == "ollama":
            base_url = self.ollama_base_url.rstrip("/")
            if not base_url.endswith("/v1"):
                base_url = f"{base_url}/v1"
            final_model = self.ollama_model
            if model_name and not model_name.startswith("gemini/") and not model_name.startswith("openrouter/"):
                final_model = model_name
            return LLM(
                model=final_model,
                api_key="ollama",
                base_url=base_url,
                api_base=base_url,
                provider="ollama",
            )

        if self.llm_provider.lower() == "gemini":
            return LLM(
                model=model_name or self.gemini_model,
                api_key=self.gemini_api_key or None,
                provider="openai",
                is_litellm=True,
                additional_params={"num_retries": 10}
            )

        return LLM(
            model=model_name or self.model_name,
            api_key=self.openai_api_key or None,
            provider="openai",
        )


settings = Settings()
