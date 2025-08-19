# alembic/env.py
from __future__ import annotations
import sys
import os
import importlib
from logging.config import fileConfig
from typing import Sequence, Union

from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine import Connection
from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# Try to import DB URLs from app.config. Fall back to env vars if unavailable.
try:
    from app.config import DATABASE_URL_SYNC, DATABASE_URL_ASYNC
except Exception:
    DATABASE_URL_SYNC = os.environ.get("DATABASE_URL") or os.environ.get("DATABASE_URL_SYNC")
    DATABASE_URL_ASYNC = os.environ.get("DATABASE_URL_ASYNC") or DATABASE_URL_SYNC
    if not DATABASE_URL_SYNC:
        raise RuntimeError(
            "DATABASE_URL not found in app.config or environment. "
            "Set DATABASE_URL or DATABASE_URL_SYNC in env or in app.config."
        )

# Make sure alembic uses a sync-style URL for offline/metadata operations
config.set_main_option("sqlalchemy.url", DATABASE_URL_SYNC)


# ---------- Import Base and model modules so target_metadata is complete ----------
# Import the declarative Base object used by your models
# NOTE: this import must not execute application side-effects (avoid launching app servers).
try:
    # app.db should define Base = declarative_base()
    from app.db import Base
except Exception as e:
    raise ImportError(f"Could not import Base from app.db: {e}")

# Ensure all modules that define models are imported — modify this list to include
# any additional modules in your app that declare SQLAlchemy models.
MODEL_MODULES = [
    "app.models",
    # add any others where models are declared (adjust to your repo structure):
    "app.auth",              # or "app.auth.models" if models are inside module
    "app.users.models",
    "app.contracts.models",
    # services playbooks
    # "services.nda.models",
    # "services.eula.models",
    # "services.pp.models",
    # "services.dpa.models",
]

# Import them so that Base.metadata is populated
for module_path in MODEL_MODULES:
    try:
        importlib.import_module(module_path)
        # print(f"Imported models module: {module_path}")
    except Exception as ex:
        # Do not crash here; print notice so you can add correct module path if needed.
        print(f"Notice: could not import {module_path}: {ex}", file=sys.stderr)

# The metadata object for 'autogenerate' support
target_metadata = Base.metadata

# ----------------------------------------------------------------------
# The following functions are a standard Alembic async-capable env.py.
# We configure online (async) and offline flows. Keep them as-is.
# ----------------------------------------------------------------------
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run migrations in async mode using the async engine."""
    from sqlalchemy.ext.asyncio import create_async_engine

    connectable = create_async_engine(
        DATABASE_URL_ASYNC,
        poolclass=pool.NullPool,
        future=True,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # prefer async path if alembic was invoked in async-capable code
    try:
        import asyncio

        asyncio.run(run_async_migrations())
    except Exception:
        # fallback to sync engine
        engine = engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )
        with engine.connect() as connection:
            do_run_migrations(connection)


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
