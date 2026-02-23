# Repository Guidelines

## Project Structure & Module Organization
Primary code lives under `src/`:
- `src/tg_bot/`: Telegram bot commands, handlers, keyboards, and middlewares.
- `src/logic/`: cartography/geodesy business logic and calculation chains.
- `src/domain/`: core domain models, actions, and facade interfaces.
- `src/core/`: settings and logging setup.

Tests are in `tests/` (pytest), static assets in `static/`, and architecture notes in `diagrams/`. CI is defined in `.github/workflows/python-app.yml`.

## Build, Test, and Development Commands
- `uv sync`: install runtime + dev dependencies from `pyproject.toml`/`uv.lock`.
- `make run-python`: run the bot locally (`python src/main.py`).
- `make run-docker`: start with Docker Compose.
- `make down-docker`: stop and remove Docker Compose services/volumes.
- `pytest`: run the full test suite (same baseline used in CI).
- `pytest --cov=src --cov-report=term-missing tests`: run tests with coverage details.
- `pre-commit run --all-files`: run configured Ruff/format/hooks before pushing.

## Coding Style & Naming Conventions
Use Python 3.10+ and follow Ruff configuration in `pyproject.toml`:
- Max line length: `120`
- Quote style: double quotes
- Prefer absolute imports (parent relative imports are banned)

Naming:
- Files/modules/functions/variables: `snake_case`
- Classes: `PascalCase`
- Tests: `test_*.py` and descriptive `test_*` function names tied to behavior.

## Testing Guidelines
Framework: `pytest` with optional `pytest-cov`/`coverage`.
- Keep tests in `tests/` mirroring functional areas (cartography chains, coordinate actions, resolvers).
- Add regression tests for bug fixes and edge cases in coordinate/nomenclature transformations.
- Run `pytest` locally before opening a PR.

## Commit & Pull Request Guidelines
Commit history uses short imperative messages, with optional Conventional-style prefixes (e.g., `refactor(...)`, `feat(...)`, `fix ...`). Keep commits focused and atomic.

PRs should include:
- Clear summary of behavior changes
- Linked issue/task (if available)
- Test evidence (`pytest` output or coverage command result)
- Screenshots for user-visible bot output changes (when applicable)
