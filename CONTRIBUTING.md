# Contributing to Voice Clone Defense

Thank you for contributing to Voice Clone Defense. This project is being developed as a Smart India Hackathon prototype, so changes should be focused, easy to review, and consistent with the current V1 scope.

## Before You Start

- Read `CLAUDE.md` before making a major change.
- Check the existing code before creating a new implementation.
- Keep the current uploaded-audio V1 scope in mind.
- Do not implement future-scope features without explicit agreement from the team.

## Development Workflow

1. Update your local `main` branch.
2. Create a focused feature branch.
3. Make the smallest reasonable set of changes.
4. Run relevant tests and checks.
5. Update documentation if behavior, setup, or architecture changed.
6. Review the final diff.
7. Open a pull request against `main`.
8. Explain what changed, why it changed, and how it was tested.

Example:

```bash
git checkout main
git pull origin main
git checkout -b feature/short-description
```

## Commit Messages

Use short, descriptive commit messages. Examples:

```text
feat: add audio validation
fix: handle short audio safely
docs: update setup instructions
test: add risk engine edge cases
```

Avoid vague messages such as `changes`, `update`, or `final`.

## Pull Requests

A good pull request should include:

- A clear title.
- A short explanation of the change.
- Files/components affected.
- Tests or checks performed.
- Known limitations or follow-up work, if any.

Do not describe an unfinished feature as complete.

## Testing

For backend changes:

```bash
cd backend
python -m pytest tests -v
```

For frontend changes:

```bash
cd frontend
npm ci
npm run build
npm run lint
```

Choose the checks relevant to the files you changed. When a feature introduces new behavior, add or update tests where practical.

## Security Rules

Never commit:

- API keys or passwords.
- Authentication tokens.
- `.env` files containing secrets.
- Uploaded audio recordings.
- Local virtual environments.
- Generated build output.

Treat uploaded files and user input as untrusted data. Preserve the project's validation, size-limit, temporary-file, and cleanup safeguards.

## Documentation Rules

Documentation must describe the repository's actual state.

Use labels such as **Implemented**, **In Development**, or **Planned** when a feature is not complete. Do not invent accuracy values, benchmark results, screenshots, deployment results, or detection performance.

When a module changes its public behavior, update the relevant README or documentation in the same pull request.

## Scope Reminder

The current V1 focuses on uploaded audio. Live/near-live telephony, VoIP integration, multilingual support, configurable alerts, and other future directions are roadmap items unless explicitly brought into the active scope.
