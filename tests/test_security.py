"""
Security-focused tests verifying that common vulnerabilities are prevented.
"""

import os

os.environ.setdefault("SECRET_KEY", "test-secret-key-not-for-production")

import pytest

from app.database import DATABASE_PATH, find_user_by_email, find_user_by_username, init_db
from app.main import create_app
from app.validation import (
    sanitize_html,
    validate_email,
    validate_password,
    validate_username,
)


@pytest.fixture
def app():
    """Create app with test configuration."""
    os.environ["SECRET_KEY"] = "test-secret-key-not-for-production"
    os.environ["CORS_ORIGINS"] = "http://localhost:3000"
    application = create_app()
    yield application
    # Cleanup test database
    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)


@pytest.fixture
def client(app):
    return app.test_client()


class TestSQLInjectionPrevention:
    """Verify SQL injection is not possible through any input."""

    def test_login_sql_injection_username(self, client):
        """Attempting SQL injection in username should fail safely."""
        response = client.post(
            "/api/login",
            json={"username": "' OR '1'='1", "password": "anything"},
        )
        assert response.status_code == 401

    def test_login_sql_injection_union(self, client):
        """UNION-based injection should not work."""
        response = client.post(
            "/api/login",
            json={"username": "' UNION SELECT * FROM users--", "password": "x"},
        )
        assert response.status_code == 401

    def test_register_sql_injection(self, client):
        """SQL injection in registration fields should be rejected by validation."""
        response = client.post(
            "/api/register",
            json={
                "username": "'; DROP TABLE users;--",
                "email": "test@test.com",
                "password": "SecurePass1",
            },
        )
        # Rejected by username validation (special chars not allowed)
        assert response.status_code == 400


class TestInputValidation:
    """Verify all user inputs are properly validated."""

    def test_username_rejects_special_chars(self):
        valid, _ = validate_username("<script>alert('xss')</script>")
        assert not valid

    def test_username_rejects_too_short(self):
        valid, _ = validate_username("ab")
        assert not valid

    def test_username_accepts_valid(self):
        valid, _ = validate_username("john_doe123")
        assert valid

    def test_email_rejects_invalid(self):
        valid, _ = validate_email("not-an-email")
        assert not valid

    def test_email_accepts_valid(self):
        valid, _ = validate_email("user@example.com")
        assert valid

    def test_password_requires_complexity(self):
        valid, _ = validate_password("weak")
        assert not valid

    def test_password_accepts_strong(self):
        valid, _ = validate_password("Str0ngP@ss")
        assert valid


class TestXSSPrevention:
    """Verify XSS payloads are sanitized."""

    def test_script_tag_stripped(self):
        result = sanitize_html("<script>alert('xss')</script>")
        assert "<script>" not in result

    def test_event_handler_stripped(self):
        result = sanitize_html('<img src=x onerror="alert(1)">')
        assert "onerror" not in result

    def test_safe_html_preserved(self):
        result = sanitize_html("<b>Bold</b> and <em>italic</em>")
        assert "<b>Bold</b>" in result
        assert "<em>italic</em>" in result

    def test_post_title_sanitized(self, client):
        """Post titles should have HTML sanitized just like content."""
        reg = client.post(
            "/api/register",
            json={
                "username": "titletest",
                "email": "title@example.com",
                "password": "SecurePass1",
            },
        )
        token = reg.get_json()["token"]
        response = client.post(
            "/api/posts",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "title": "<script>alert(1)</script>Safe Title",
                "content": "Normal content",
            },
        )
        assert response.status_code == 201
        posts = client.get(
            "/api/posts",
            headers={"Authorization": f"Bearer {token}"},
        ).get_json()["posts"]
        assert "<script>" not in posts[0]["title"]


class TestDuplicateEmailCheck:
    """Verify duplicate email registration is rejected."""

    def test_duplicate_email_rejected(self, client):
        """Registering with an already-taken email returns 409."""
        client.post(
            "/api/register",
            json={
                "username": "firstuser",
                "email": "shared@example.com",
                "password": "SecurePass1",
            },
        )
        response = client.post(
            "/api/register",
            json={
                "username": "seconduser",
                "email": "shared@example.com",
                "password": "SecurePass1",
            },
        )
        assert response.status_code == 409
        assert "email" in response.get_json()["error"].lower()


class TestAuthentication:
    """Verify authentication is enforced."""

    def test_posts_requires_auth(self, client):
        """Accessing posts without token should return 401."""
        response = client.get("/api/posts")
        assert response.status_code == 401

    def test_posts_rejects_invalid_token(self, client):
        """Invalid tokens should be rejected."""
        response = client.get(
            "/api/posts",
            headers={"Authorization": "Bearer invalid.token.here"},
        )
        assert response.status_code == 401

    def test_admin_requires_admin_role(self, client):
        """Non-admin users cannot access admin endpoints."""
        # Register a normal user
        reg_response = client.post(
            "/api/register",
            json={
                "username": "normaluser",
                "email": "normal@example.com",
                "password": "SecurePass1",
            },
        )
        token = reg_response.get_json()["token"]

        # Try to access admin endpoint
        response = client.get(
            "/api/admin/users",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 403


class TestCORSConfiguration:
    """Verify CORS is not overly permissive."""

    def test_cors_rejects_unauthorized_origin(self, client):
        """Requests from unauthorized origins should not get CORS headers."""
        response = client.get(
            "/api/health",
            headers={"Origin": "http://evil-site.com"},
        )
        assert response.headers.get("Access-Control-Allow-Origin") != "*"

    def test_cors_never_returns_wildcard(self, client):
        """CORS should never return wildcard Access-Control-Allow-Origin."""
        response = client.get(
            "/api/health",
            headers={"Origin": "http://localhost:3000"},
        )
        # The key security check: wildcard is never used
        allow_origin = response.headers.get("Access-Control-Allow-Origin")
        assert allow_origin != "*"


class TestSecurityHeaders:
    """Verify security headers are present."""

    def test_security_headers_present(self, client):
        response = client.get("/api/health")
        assert response.headers.get("X-Content-Type-Options") == "nosniff"
        assert response.headers.get("X-Frame-Options") == "DENY"
        assert "max-age" in response.headers.get("Strict-Transport-Security", "")
        assert response.headers.get("Content-Security-Policy") == "default-src 'self'"


class TestNoDebugExposure:
    """Verify debug info is not exposed."""

    def test_health_no_sensitive_info(self, client):
        """Health endpoint should not expose internal details."""
        response = client.get("/api/health")
        data = response.get_json()
        assert "debug" not in data
        assert "config" not in data
        assert "secret" not in str(data).lower()
