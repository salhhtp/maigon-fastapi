# app/config.py
from pydantic import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    # Postgres DB URL (use Supabase Postgres connection string)
    DATABASE_URL: str

    # Supabase project URL, e.g., https://xyzproj.supabase.co
    SUPABASE_URL: str

    # Supabase anon key (used client-side normally). Not required server-side for verify.
    SUPABASE_ANON_KEY: str | None = None

    # External AI/edge analysis service URL (e.g., https://edge.maigon.ai)
    ANALYSIS_API_URL: str

    # Stripe
    STRIPE_SECRET_KEY: str
    STRIPE_WEBHOOK_SECRET: str

    # App secret (for internal uses)
    APP_SECRET_KEY: str = "change-me-to-a-secure-random-value"

    # Misc
    DEBUG: bool = True

    class Config:
        env_file = ".env"


settings = Settings()

# --- Module-level exports (useful for Alembic and scripts) ---
# settings.DATABASE_URL will be whatever you set in .env

# Standard DATABASE_URL as provided in .env
DATABASE_URL = settings.DATABASE_URL

# Provide an async variant used by SQLAlchemy async engine code.
# If DATABASE_URL already includes "+asyncpg", use it; otherwise append it.
if "+asyncpg" in DATABASE_URL:
    DATABASE_URL_ASYNC = DATABASE_URL
else:
    DATABASE_URL_ASYNC = DATABASE_URL + "+asyncpg"

# Also export a sync-only URL (some scripts / Alembic offline mode prefer no +asyncpg)
if "+asyncpg" in DATABASE_URL:
    DATABASE_URL_SYNC = DATABASE_URL.split("+asyncpg")[0]
else:
    DATABASE_URL_SYNC = DATABASE_URL

# --- Backwards-compatible aliases (for older imports in the codebase) ---
# Some parts of the repo expect these variable names:
SYNC_DATABASE_URL = DATABASE_URL_SYNC
ASYNC_DATABASE_URL = DATABASE_URL_ASYNC
