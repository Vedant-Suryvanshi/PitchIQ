# backend/config.py
"""
PitchIQ Configuration Module
Updated for PostgreSQL support with proper validation
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr, field_validator
from functools import lru_cache
from typing import Optional, Any


class Settings(BaseSettings):
    """All configuration for PitchIQ with PostgreSQL support"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Google AI ─────────────────────────────────────────────────────────────
    google_api_key: SecretStr = Field(
        ..., description="Google AI Studio API key"
    )

    # ── Application ───────────────────────────────────────────────────────────
    environment: str = Field(default="development")
    backend_host: str = Field(default="0.0.0.0")
    backend_port: int = Field(default=8000)

    # ── Database ──────────────────────────────────────────────────────────────
    # PostgreSQL connection string
    database_url: str = Field(
        default="postgresql+asyncpg://pitchiq:pitchiq_secure_password_2024@localhost:5432/pitchiq",
        description="PostgreSQL async URL"
    )

    # ── Database Pool Configuration ──────────────────────────────────────────
    db_pool_size: int = Field(default=20)
    db_max_overflow: int = Field(default=40)
    db_pool_timeout: int = Field(default=30)
    db_pool_recycle: int = Field(default=3600)
    db_pool_pre_ping: bool = Field(default=True)

    # ── Security ──────────────────────────────────────────────────────────────
    secret_key: SecretStr = Field(...)
    allowed_origins: str = Field(default="http://localhost:3000")
    rate_limit_per_minute: int = Field(default=10)

    # ── MCP Server ────────────────────────────────────────────────────────────
    mcp_server_host: str = Field(default="localhost")
    mcp_server_port: int = Field(default=8001)

    # ── Frontend ──────────────────────────────────────────────────────────────
    next_public_api_url: str = Field(default="http://localhost:8000")

    # ── Model ─────────────────────────────────────────────────────────────────
    gemini_model: str = Field(default="gemini-2.5-flash")

    # ── Redis ─────────────────────────────────────────────────────────────────
    redis_url: str = Field(default="redis://localhost:6379")

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Validate and format database URL."""
        # If it's SQLite, use it as is (for testing)
        if v.startswith("sqlite"):
            return v
        
        # Ensure PostgreSQL URL has asyncpg driver
        if v.startswith("postgresql"):
            if "+asyncpg" not in v:
                v = v.replace("postgresql://", "postgresql+asyncpg://")
            return v
        
        # If it's empty or invalid, use default
        if not v or v == "":
            return "postgresql+asyncpg://pitchiq:pitchiq_secure_password_2024@localhost:5432/pitchiq"
        
        return v

    @property
    def cors_origins(self) -> list[str]:
        """Parse comma-separated ALLOWED_ORIGINS into a Python list."""
        return [origin.strip() for origin in self.allowed_origins.split(",")]

    @property
    def is_production(self) -> bool:
        """Convenience flag used by security module."""
        return self.environment == "production"

    @property
    def mcp_server_url(self) -> str:
        """Assembled MCP server URL for agent tool calls."""
        return f"http://{self.mcp_server_host}:{self.mcp_server_port}"

    @property
    def is_postgres(self) -> bool:
        """Check if using PostgreSQL."""
        return "postgresql" in self.database_url


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Returns a cached Settings instance."""
    return Settings()