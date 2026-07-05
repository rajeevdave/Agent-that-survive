# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.x     | ✅        |

## Reporting a Vulnerability

Please report security vulnerabilities by opening a GitHub Security Advisory.
Do NOT open a public issue for security vulnerabilities.

Response time: within 48 hours for critical issues.

## Security Best Practices

- Never commit API keys or secrets to this repository
- Use `.env` files (excluded from git via `.gitignore`)
- Rotate API keys immediately if accidentally exposed
- All external content is treated as untrusted input (see Chapter 4: Safety Blindspot)
