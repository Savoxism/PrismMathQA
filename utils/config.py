"""LLM API settings loaded from environment variables."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    llm_api_key: str
    llm_base_url: str
    llm_model: str = "openai/gpt-oss-120b:netmind"

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            llm_api_key=os.getenv("LLM_API_KEY", ""),
            llm_base_url=os.getenv("LLM_BASE_URL", "")
        )

    def validate(self) -> None:
        if not self.llm_api_key:
            raise ValueError("LLM_API_KEY environment variable is required")
        if not self.llm_base_url:
            raise ValueError("LLM_BASE_URL environment variable is required")


settings = Settings.from_env()
settings.validate()
