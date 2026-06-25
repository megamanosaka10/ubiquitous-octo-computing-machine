# Security Practices

This application demonstrates secure coding patterns for common web vulnerabilities.

## Protections Implemented

| Vulnerability | Mitigation |
|---|---|
| **Hardcoded secrets** | All secrets loaded from environment variables (`app/config.py`). App refuses to start without `SECRET_KEY`. |
| **SQL injection** | All queries use parameterized statements (`app/database.py`). No string concatenation with user input. |
| **Unvalidated input** | All user inputs validated with strict patterns before processing (`app/validation.py`). |
| **XSS (Cross-Site Scripting)** | User-generated HTML sanitized with `bleach` before storage (`app/validation.py`). |
| **Overly permissive CORS** | CORS restricted to explicit origins from config — no wildcard `*` (`app/main.py`). |
| **Missing authentication** | Protected endpoints use `@require_auth` decorator. Admin endpoints use `@require_role("admin")` (`app/auth.py`). |
| **Exposed debug endpoints** | No debug routes. Debug mode only via env var. Security headers strip server info (`app/main.py`). |
| **Weak passwords** | Passwords hashed with bcrypt. Password complexity enforced on registration. |
| **Brute-force attacks** | Rate limiting via `flask-limiter` on all API endpoints. |
| **Security headers** | HSTS, X-Frame-Options, CSP, X-Content-Type-Options all set. |

## Running Tests

```bash
pip install -r requirements.txt
pip install pytest
SECRET_KEY=test-key pytest tests/ -v
```

## Anti-Patterns (What NOT to Do)

See inline comments in `app/config.py` and `app/main.py` for examples of insecure patterns to avoid.
