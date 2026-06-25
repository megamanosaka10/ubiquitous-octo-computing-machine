"""
Application factory demonstrating secure Flask setup.

SECURITY BEST PRACTICES:
- CORS restricted to explicit origins (not wildcard *)
- Rate limiting on sensitive endpoints
- Debug mode controlled by environment variable only
- No debug toolbar or endpoints in production
- Security headers added via after_request
"""

import os

from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from app.config import Config, DevelopmentConfig, ProductionConfig
from app.database import init_db
from app.routes import api


def create_app(config_class=None) -> Flask:
    """Application factory with security hardening."""
    app = Flask(__name__)

    # Load configuration
    if config_class is None:
        env = os.environ.get("FLASK_ENV", "production")
        config_class = DevelopmentConfig if env == "development" else ProductionConfig
    app.config.from_object(config_class)

    # CORS: only allow specific origins, not wildcard
    # INSECURE pattern (DO NOT USE): CORS(app, origins="*")
    CORS(
        app,
        origins=app.config["CORS_ORIGINS"],
        methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["Authorization", "Content-Type"],
        max_age=3600,
    )

    # Rate limiting to prevent brute-force attacks
    limiter = Limiter(
        key_func=get_remote_address,
        app=app,
        default_limits=["100 per minute"],
        storage_uri="memory://",
    )
    limiter.limit("5 per minute")(api)

    # Register routes
    app.register_blueprint(api)

    # Security headers
    @app.after_request
    def add_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        # Don't leak server info
        response.headers.pop("Server", None)
        return response

    # Initialize database
    with app.app_context():
        init_db()

    return app
