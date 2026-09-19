"""
Configuration classes for InsightFlow.

All secrets/settings come from environment variables (never hardcoded),
loaded from a local .env file via python-dotenv during development.

We are NOT connecting to MySQL yet in Phase 0 (per project decision), so
DATABASE_URL is read here and stored on the config so it's ready to use
in a later phase, but nothing in Phase 0 actually opens a DB connection.
"""

import os
from dotenv import load_dotenv

# Load variables from a .env file in the project root, if present.
# In production, real environment variables are set by the host instead
# of a .env file, and load_dotenv() simply does nothing in that case.
load_dotenv()


class BaseConfig:
    """Settings shared by every environment."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")
    APP_NAME = "InsightFlow"

    # Not used yet (no DB connection in Phase 0) — read now so it's
    # available without any code changes when we add SQLAlchemy later.
    DATABASE_URL = os.environ.get("DATABASE_URL", "")


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = False


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    # A separate flag so tests never accidentally rely on dev-only behavior.


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False


# Lookup used by app/__init__.py's create_app(config_name)
config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
