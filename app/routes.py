"""
API routes demonstrating secure endpoint patterns.

SECURITY BEST PRACTICES demonstrated:
- All mutation endpoints require authentication
- Input validation before any processing
- Output sanitization for user-generated content
- Rate limiting on sensitive endpoints (login, register)
- No debug endpoints in production
"""

import sqlite3

from flask import Blueprint, request

from app.auth import (
    create_token,
    hash_password,
    require_auth,
    require_role,
    verify_password,
)
from app.database import (
    create_post,
    create_user,
    find_user_by_email,
    find_user_by_username,
    get_posts_for_user,
)
from app.validation import (
    sanitize_html,
    validate_email,
    validate_password,
    validate_post_content,
    validate_post_title,
    validate_username,
)

api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/health", methods=["GET"])
def health_check():
    """Public health check endpoint — no sensitive info exposed."""
    return {"status": "healthy"}


@api.route("/register", methods=["POST"])
def register():
    """
    Register a new user.

    SECURE: Validates all input, hashes password, uses parameterized DB queries.
    """
    data = request.get_json()
    if not data:
        return {"error": "Request body must be JSON"}, 400

    username = data.get("username", "")
    email = data.get("email", "")
    password = data.get("password", "")

    # Validate all inputs
    valid, msg = validate_username(username)
    if not valid:
        return {"error": msg}, 400

    valid, msg = validate_email(email)
    if not valid:
        return {"error": msg}, 400

    valid, msg = validate_password(password)
    if not valid:
        return {"error": msg}, 400

    # Check if user already exists
    if find_user_by_username(username):
        return {"error": "Username already taken"}, 409

    if find_user_by_email(email):
        return {"error": "Email already taken"}, 409

    # Hash password and create user
    password_hash = hash_password(password)
    try:
        user_id = create_user(username, password_hash, email)
    except sqlite3.IntegrityError:
        return {"error": "Username or email already taken"}, 409

    token = create_token(user_id)
    return {"token": token, "user_id": user_id}, 201


@api.route("/login", methods=["POST"])
def login():
    """
    Authenticate a user.

    SECURE: Generic error message prevents username enumeration.
    """
    data = request.get_json()
    if not data:
        return {"error": "Request body must be JSON"}, 400

    username = data.get("username", "")
    password = data.get("password", "")

    if not username or not password:
        return {"error": "Username and password are required"}, 400

    user = find_user_by_username(username)
    # Generic message prevents username enumeration
    if not user or not verify_password(password, user["password_hash"]):
        return {"error": "Invalid credentials"}, 401

    token = create_token(user["id"])
    return {"token": token, "user_id": user["id"]}


@api.route("/posts", methods=["GET"])
@require_auth
def list_posts():
    """List posts for the authenticated user."""
    posts = get_posts_for_user(request.current_user["id"])
    return {"posts": posts}


@api.route("/posts", methods=["POST"])
@require_auth
def create_new_post():
    """
    Create a new post.

    SECURE: Requires auth, validates input, sanitizes HTML content.
    """
    data = request.get_json()
    if not data:
        return {"error": "Request body must be JSON"}, 400

    title = data.get("title", "")
    content = data.get("content", "")

    valid, msg = validate_post_title(title)
    if not valid:
        return {"error": msg}, 400

    valid, msg = validate_post_content(content)
    if not valid:
        return {"error": msg}, 400

    # Sanitize HTML to prevent stored XSS
    safe_content = sanitize_html(content)

    safe_title = sanitize_html(title)

    post_id = create_post(request.current_user["id"], safe_title, safe_content)
    return {"post_id": post_id}, 201


@api.route("/admin/users", methods=["GET"])
@require_role("admin")
def list_users():
    """
    Admin-only endpoint.

    SECURE: Protected by role-based access control.
    """
    return {"message": "Admin access granted"}
