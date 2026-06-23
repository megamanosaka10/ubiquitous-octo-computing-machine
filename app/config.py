"""
Application configuration.

SECURITY BEST PRACTICE: Never hardcode secrets. Load them from environment
variables or a secrets manager. The .env file should never be committed.
"""

import os


class Config:
    """Base configuration loaded from environment variables."""

    SECRET_KEY = os.environ.get("SECRET_KEY")
    if not SECRET_KEY:
        raise RuntimeError(
            "SECRET_KEY environment variable is required. "
            "Generate one with: python -c \"import secrets; print(secrets.token_hex(32))\""
        )

    DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///app.db")

    # JWT settings
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRATION_SECONDS = 3600

    # CORS: restrict to specific origins in production
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "").split(",")
    if CORS_ORIGINS == [""]:
        CORS_ORIGINS = []

    DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"


class DevelopmentConfig(Config):
    """Development overrides — still requires SECRET_KEY from env."""

    DEBUG = True


class ProductionConfig(Config):
    """Production hardening."""

    DEBUG = False
