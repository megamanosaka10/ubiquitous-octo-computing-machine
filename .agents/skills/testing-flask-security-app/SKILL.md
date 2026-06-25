---
name: testing-flask-security-app
description: Test the Flask security-focused API application end-to-end. Use when verifying security controls, authentication, input validation, or API endpoint changes.
---

# Testing the Secure Flask App

## Prerequisites
- Python 3.12+ with pip
- Install dependencies: `pip install -r requirements.txt pytest`

## Running the App Locally

```bash
cd /path/to/ubiquitous-octo-computing-machine
SECRET_KEY=test-secret-key CORS_ORIGINS=http://localhost:5000 python -c "
from app.main import create_app
app = create_app()
app.run(host='127.0.0.1', port=5000, debug=False)
"
```

The app requires `SECRET_KEY` env var — it will refuse to start without it.

## Running Tests

```bash
SECRET_KEY=test-key pytest tests/ -v
```

All 20 tests should pass. They cover: SQL injection, XSS, auth bypass, CORS, security headers, and debug exposure.

## Manual API Testing

Key endpoints:
- `GET /api/health` — public, returns `{"status": "healthy"}`
- `POST /api/register` — body: `{"username", "email", "password"}`
- `POST /api/login` — body: `{"username", "password"}`, returns JWT token
- `GET /api/posts` — requires `Authorization: Bearer <token>`
- `POST /api/posts` — requires auth, body: `{"title", "content"}`
- `GET /api/admin/users` — requires admin role

## Security Controls to Verify

1. **No SECRET_KEY → crash**: unset SECRET_KEY and try to import config
2. **SQL injection**: send `' OR '1'='1` as username on login → expect 401
3. **XSS sanitization**: post content with `<script>` tags → verify stripped on retrieval
4. **Auth enforcement**: access protected endpoints without token → expect 401
5. **Role-based access**: regular user on admin endpoint → expect 403
6. **Input validation**: special chars in username → expect 400
7. **Password complexity**: short/weak password → expect 400
8. **Security headers**: check HSTS, CSP, X-Frame-Options on any response

## Notes
- This is an API-only app (no frontend). Testing is done via curl/httpie or pytest.
- No browser recording needed — use shell commands for all testing.
- The database is SQLite (`app.db`) and auto-created on app start. Delete it for a fresh state.

## Devin Secrets Needed
None — the app uses a test SECRET_KEY for local testing. No external services or credentials required.
