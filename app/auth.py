"""
Authentication module demonstrating secure patterns.

SECURITY BEST PRACTICES:
- Passwords hashed with bcrypt (adaptive cost factor)
- JWT tokens with expiration
- Decorator-based auth checks so endpoints can't accidentally skip auth
"""

import functools
import time

import bcrypt
import jwt
from flask import current_app, request

from app.database import find_user_by_id


def hash_password(password: str) -> str:
    """Hash a password using bcrypt with a random salt."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against its bcrypt hash."""
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))


def create_token(user_id: int) -> str:
    """Create a JWT token with expiration."""
    payload = {
        "user_id": user_id,
        "exp": int(time.time()) + current_app.config["JWT_EXPIRATION_SECONDS"],
        "iat": int(time.time()),
    }
    return jwt.encode(
        payload,
        current_app.config["SECRET_KEY"],
        algorithm=current_app.config["JWT_ALGORITHM"],
    )


def decode_token(token: str) -> dict | None:
    """Decode and validate a JWT token."""
    try:
        return jwt.decode(
            token,
            current_app.config["SECRET_KEY"],
            algorithms=[current_app.config["JWT_ALGORITHM"]],
        )
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None


def require_auth(f):
    """
    Decorator that enforces authentication on an endpoint.

    SECURITY BEST PRACTICE: Use decorators to ensure auth can't be
    accidentally omitted from protected endpoints.
    """

    @functools.wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return {"error": "Missing or invalid Authorization header"}, 401

        token = auth_header.split(" ", 1)[1]
        payload = decode_token(token)
        if payload is None:
            return {"error": "Invalid or expired token"}, 401

        user = find_user_by_id(payload["user_id"])
        if user is None:
            return {"error": "User not found"}, 401

        request.current_user = user
        return f(*args, **kwargs)

    return decorated


def require_role(role: str):
    """
    Decorator that enforces a specific role after authentication.

    Usage: @require_role("admin")
    """

    def decorator(f):
        @functools.wraps(f)
        @require_auth
        def decorated(*args, **kwargs):
            if request.current_user["role"] != role:
                return {"error": "Insufficient permissions"}, 403
            return f(*args, **kwargs)

        return decorated

    return decorator
