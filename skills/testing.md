# Skill: Testing — Voice Clone Defense

## Scope of This Skill
This skill governs how every feature in Voice Clone Defense gets tested:
backend automated tests (pytest/httpx), frontend manual testing, edge-case
coverage, and security-specific testing. This file is subordinate to
CLAUDE.md's Testing Requirements (Section 14) and Definition of Feature
Complete (Section 8).

---

## Responsibilities

When acting under this skill, the assistant is responsible for:

- Writing automated backend tests for every new endpoint or processing
  function, using pytest and httpx.
- Producing a clear manual test checklist for every new frontend feature.
- Ensuring every feature is tested against the full edge-case list from
  CLAUDE.md before being called complete.
- Explicitly testing security-relevant behavior (validation, rate
  limiting, error handling) — not just "happy path" functionality.
- Explaining test coverage in plain language: what's tested, what isn't
  yet, and why.

---

## Approved Technologies (do not deviate)

- **pytest** — backend test framework
- **httpx** — used to send test requests directly to the FastAPI app
- **Manual testing checklists** — for frontend, in v1
- **Vitest** — only as an optional future addition once the core app is
  stable, and only with explicit approval before introducing it

Do not introduce other testing frameworks (e.g. unittest, Jest, Cypress,
Playwright) unless explicitly approved — Vitest is the only pre-approved
future frontend testing tool, and only as a later addition.

---

## Backend Testing Rules

Every backend feature must have automated tests covering, at minimum:

- **Normal/valid input** — confirms the feature works as intended.
- **Invalid input** — malformed or wrong-type data.
- **Empty input** — no file, empty file, missing fields.
- **Unsupported file types** — files outside the allow-list.
- **Corrupted files** — files that claim to be audio but aren't valid.
- **Large files** — beyond the configured size limit.
- **Unexpected input** — anything not covered by the cases above that a
  creative or careless user might send.
- **Error conditions** — confirm errors are handled gracefully and don't
  leak internal details (see cybersecurity.md).

Tests should be organized per feature/module (e.g. `test_upload.py`,
`test_feature_extraction.py`) and named descriptively enough that a
beginner reading the test name understands what's being checked.

---

## Frontend Testing Rules (manual, for v1)

For every frontend feature, manually verify and document:

- **Loading state** — does the user see clear feedback while something is
  processing?
- **Success state** — does the result display correctly and completely?
- **Error state** — does a failure show a clear, non-technical message?
- **Desktop layout** — does it look and work correctly at a normal
  desktop width?
- **Mobile layout** — does it look and work correctly at a common mobile
  width (~375–414px)?

Maintain this as a running checklist document (see documentation.md) that
gets updated and re-checked after significant changes, not just once.

---

## Security Testing Rules

Security-relevant behavior must be explicitly tested, not assumed to work
because it was implemented. At minimum:

- Confirm file validation actually rejects disguised/malicious files
  (e.g. a non-audio file renamed with an audio extension).
- Confirm rate limiting actually triggers under repeated rapid requests,
  and that it doesn't block legitimate normal use.
- Confirm error responses do not leak file paths, stack traces, or other
  internal details — inspect actual error response bodies, don't assume.
- Confirm temporary files are actually deleted after both successful and
  failed processing (e.g. by checking the temp directory before/after a
  forced failure).

---

## Quality Requirements

- Tests must be run and shown to pass before a feature is described as
  working — never claim "this should work" as a substitute for running
  the tests.
- When a test reveals a bug, the fix (not just the discovery) must be
  completed and re-tested before the feature is called done.
- Test coverage should be explained in beginner-friendly terms: what
  scenario each test represents and why it matters.
- A feature is only "done" once it satisfies CLAUDE.md's Definition of
  Feature Complete (Section 8) — testing is one required part of that,
  not an optional final step.

---

## The Assistant Must NOT

- Must NOT claim a feature is "tested" without actually running the
  tests and showing the result.
- Must NOT skip edge cases (empty/corrupted/large/unexpected input) to
  save time — these are explicit CLAUDE.md requirements.
- Must NOT introduce a new testing framework/tool without explicit
  approval.
- Must NOT treat security testing as optional or secondary to functional
  testing — both are required per CLAUDE.md and cybersecurity.md.
- Must NOT write large batches of tests for multiple unrelated features
  at once — test each feature as it's built, incrementally, per CLAUDE.md's
  development philosophy.
  