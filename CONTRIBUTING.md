# Contributing to AgriPulse

Thank you for contributing! Please read these guidelines before opening a PR.

---

## Branch Strategy

| Branch | Purpose |
|---|---|
| `main` | Production-stable code only |
| `dev` | Integration branch — merge feature branches here first |
| `feature/<name>` | New features (e.g. `feature/sms-alerts`) |
| `fix/<name>` | Bug fixes (e.g. `fix/breeding-sex-validation`) |
| `chore/<name>` | Tooling, deps, CI (e.g. `chore/update-requirements`) |

---

## Coding Standards

### Python
- Follow **PEP 8** (max line length: 100).
- All functions and classes must have docstrings.
- Use type hints on all public function signatures.
- Keep routes thin — business logic goes in `services/` or `calculations/`.
- Never import directly from `app` at module level in services — use `current_app` or pass values in.

### JavaScript
- Vanilla JS only — no frameworks.
- All methods live on the `AgriPulse` object literal.
- Use `async/await` throughout; always wrap API calls in `try/catch` and call `this.toast(err.message, true)` on error.
- Use `this.weightUnit` / `this.milkUnit` / `this.currency` for all unit labels — never hardcode `'kg'` or `'L'` in display strings.

### HTML / CSS
- Follow BEM-style class naming for new components.
- All new responsive rules go in the correct breakpoint block in `style.css` — never add a new `@media` block outside the existing three (1024px tablet, 768px mobile, 480px small mobile).
- Forms must call `e.target.reset()` and `this.setDefaultDates()` after successful submission.

### SQL / Models
- All new models must include a `to_dict()` method.
- Use `db.session.add()` + `db.session.commit()` — never raw SQL.
- Never break existing migrations — add columns with `server_default` or `nullable=True`.

---

## Running the Test Suite

```powershell
venv\Scripts\python -m pytest tests/ -v --tb=short
```

All 5 tests must pass before opening a PR. Add a new test for any significant new feature or bug fix.

---

## Pull Request Checklist

- [ ] Branch is off `dev`, not `main`
- [ ] Code follows the standards above
- [ ] `pytest tests/ -v` passes (5/5)
- [ ] Flask smoke test: all core API endpoints return 200
- [ ] New feature or fix documented in `CHANGELOG.md` under `[Unreleased]`
- [ ] `README.md` updated if API surface or project structure changed
- [ ] No hardcoded unit strings (`kg`, `L`, `KES`) in display-facing JS

---

## Reporting Bugs

Open an issue with:
1. Steps to reproduce
2. Expected behaviour
3. Actual behaviour
4. OS and Python version (`python --version`)
5. Any error from the terminal running `run.py`
