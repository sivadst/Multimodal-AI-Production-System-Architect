from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Literal

class Settings(BaseSettings):
    # LLM Settings
    llm_provider: Literal["openai", "anthropic"] = Field(default="openai")
    openai_api_key: str = Field(default="")
    anthropic_api_key: str = Field(default="")
    model_name: str = Field(default="gpt-4o")
    
    # DB Settings
    database_url: str = Field(default="postgresql+asyncpg://postgres:postgres@localhost:5432/arch_mind")
    redis_url: str = Field(default="redis://localhost:6379/0")
    
    # Diagram Engine Settings
    diagram_engine: Literal["mermaid", "d2"] = Field(default="mermaid")
    
    # Templates Settings
    templates_dir: str = Field(default="arch_mind/code_generation/templates")
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
