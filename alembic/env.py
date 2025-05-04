import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

from dotenv import load_dotenv

# ✅ Load env vars first!
load_dotenv()

# ✅ Add src/ to path so we can import from src.db
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "src")))


from src.db import Base
from src.models import (
    organisation_model,
    admin_model,
    application_model,
    contact_model,
    employee_model,
    role_model,
    application_contact_model,
    role_application_model,
    user_model,
    employee_onboarding_model,
    employee_onboarding_requests_model,
)  # import models to reflect schema

# Alembic config
config = context.config

# ✅ Load DB URL from environment before it's used
DB_URL = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# Inject DB URL into Alembic config
config.set_main_option("sqlalchemy.url", DB_URL)

# Logging setup
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


# Offline migration mode
def run_migrations_offline():
    context.configure(
        url=DB_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# Online migration mode
def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


# Run appropriate mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
