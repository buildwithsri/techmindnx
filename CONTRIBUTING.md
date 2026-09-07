# Contributing Guidelines

Thank you for contributing to the **AI-Powered Student Support & Smart Campus Intelligence System**!

To maintain repository quality, consistency, and reliability across our multi-module team, please follow these guidelines.

---

## 1. Branch Naming Conventions

All branches must follow standardized prefixes matching the assigned module:

```text
feature/<module_id>-<short-description>    # New features or models
fix/<module_id>-<issue-description>        # Bug fixes
docs/<module_id>-<doc-update>              # Documentation updates
refactor/<module_id>-<change>              # Code refactoring
test/<module_id>-<test-suite>              # Test scripts and datasets
```

### Examples:
- `feature/01-support-ticket-escalation`
- `feature/03-face-haar-pipeline`
- `fix/04-anomaly-threshold-overflow`
- `docs/06-fastapi-swagger-spec`

---

## 2. Commit Message Standards

Use [Conventional Commits](https://www.conventionalcommits.org/) format:

```text
<type>(<scope>): <short description in present tense>

[optional body providing rationale and details]

[optional issue/ticket reference]
```

### Types:
- `feat`: New feature or deep learning model
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Formatting, missing semi-colons, no code change
- `refactor`: Refactoring production code without changing behavior
- `test`: Adding or correcting tests
- `chore`: Build tasks, package configs, gitignore updates

### Example:
```text
feat(02-academic): add random forest regressor for GPA prediction

- Preprocesses semester credit hours and midterm scores
- Implements 5-fold cross validation with RMSE = 0.28
```

---

## 3. Pull Request Process

1. **Keep PRs Focused**: One PR should address a single feature, bug fix, or documentation update.
2. **Sync with Main**: Before submitting, ensure your feature branch is up to date:
   ```bash
   git fetch origin
   git rebase origin/main
   ```
3. **Use the PR Template**: Fill out all sections in the [PR Template](.github/pull_request_template.md).
4. **Code Quality**:
   - Ensure code is formatted (PEP 8 for Python).
   - Ensure type hints and docstrings are provided.
   - Never commit raw API keys, credentials, large binary model files (>50MB), or raw CSV datasets.
5. **Review & Merge**:
   - Require at least **1 review approval** from a Module Lead or the Project Lead.
   - QA team must verify test coverage where applicable.

---

## 4. Code Standards & Architecture

Please read:
- [`docs/coding_standards.md`](docs/coding_standards.md) for code styling, typing, and testing rules.
- [`docs/architecture.md`](docs/architecture.md) for system architecture and API conventions.
