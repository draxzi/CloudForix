# Contributing to Cloud Forix

Thank you for your interest in contributing to Cloud Forix.

---

## Getting Started

1. **Fork** the repository on GitHub
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/your-username/CloudForix.git
   cd CloudForix/cloud_forensic_tool
   ```
3. **Create a virtual environment** and install dependencies:
   ```bash
   python -m venv venv
   venv\Scripts\activate    # Windows
   pip install -r requirements.txt
   ```
4. **Set up credentials** — copy `.env.example` to `.env` and fill in your own test credentials (never commit real credentials)

---

## Development Guidelines

### Code Style

- Follow [PEP 8](https://peps.python.org/pep-0008/) for Python style
- Use descriptive variable and function names
- Add docstrings to all public functions
- Keep functions focused and single-purpose

### Security Rules (Mandatory)

- **Never** hardcode API keys, passwords, tokens, or secrets in source files
- **Never** commit `.env`, `credentials.json`, `token.json`, or `*.key` files
- Load credentials from environment variables
- Review `.gitignore` before every commit: `git status`

---

## Branching

| Branch | Purpose |
|---|---|
| `main` | Stable release |
| `feature/<name>` | New features |
| `fix/<name>` | Bug fixes |
| `docs/<name>` | Documentation changes |

**Always branch from `main`:**
```bash
git checkout main
git pull origin main
git checkout -b feature/your-feature-name
```

---

## Commits

Use [Conventional Commits](https://www.conventionalcommits.org/) format:

```
feat: add AWS CloudTrail log collection
fix: handle expired Azure token gracefully
docs: update configuration section in README
refactor: extract credential loading to config module
test: add unit tests for hash_module
```

---

## Pull Requests

1. Ensure your branch is up to date with `main`
2. Run any existing tests before submitting
3. Verify that `git status` shows no secrets or sensitive files staged
4. Create a pull request with:
   - A clear title
   - A description of what changed and why
   - Reference to any related issues

---

## Testing

```bash
# Run the existing test file
python test.py

# Manual smoke test
python main.py
```

When adding new features, please include corresponding tests.

---

## Reporting Issues

- Use the [GitHub Issues](https://github.com/draxzi/CloudForix/issues) page
- For security vulnerabilities, see [SECURITY.md](SECURITY.md) — do **not** open a public issue

---

## Code of Conduct

All contributors are expected to follow the [Code of Conduct](CODE_OF_CONDUCT.md).
