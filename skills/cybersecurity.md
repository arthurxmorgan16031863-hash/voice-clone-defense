# Skill: Cybersecurity — Voice Clone Defense

## Scope of This Skill
This skill governs security across the whole project: file upload safety,
API security, secrets management, privacy, rate limiting, and basic threat
modeling. It applies to both frontend and backend work and takes
precedence whenever there's tension between "make it work quickly" and
"make it safe." This file is subordinate to CLAUDE.md's Security Rules,
which it expands on.

---

## Responsibilities

When acting under this skill, the assistant is responsible for:

- Ensuring every user-facing input (file uploads, form data) is validated
  and never trusted by default.
- Ensuring secrets and configuration are never hardcoded.
- Ensuring temporary files are handled and cleaned up safely.
- Designing and applying rate limiting to prevent abuse.
- Thinking through, and explaining, realistic threats to this specific
  project — not generic security theory.
- Ensuring error handling never leaks internal system details.

---

## Threat Model (specific to Voice Clone Defense)

Realistic threats for this project include:

1. **Malicious file uploads** — a file disguised as audio (e.g. renamed
   extension) attempting to exploit a parsing library or waste server
   resources.
2. **Resource exhaustion / abuse** — repeated large uploads or rapid-fire
   requests intended to slow down or crash the service.
3. **Information leakage via error messages** — stack traces, file paths,
   or library versions exposed in API error responses, useful to an
   attacker probing the system.
4. **Secret exposure** — API keys or config values accidentally committed
   to the repository or exposed via error output.
5. **Unnecessary data retention** — audio files persisting longer than
   needed, creating a privacy risk if the server were ever compromised.

This list should be revisited and expanded as the project grows — it is a
starting point, not a final answer.

---

## Secure File Upload Rules

- Validate file extension **and** actual file content (not extension
  alone) before treating anything as audio — see backend.md for the
  ordered validation sequence.
- Enforce a defined, named file-size limit.
- Never execute, `eval`, or otherwise treat uploaded file content as code
  in any way.
- Reject files that fail to open/parse as valid audio rather than passing
  them further into the pipeline "just in case."

---

## API Security Rules

- Apply **rate limiting** on any endpoint that triggers real processing
  work (especially `/analyze`), scoped per IP address at minimum for v1
  (since there's no authentication yet).
- Keep CORS configuration as narrow as possible — only allow the actual
  frontend origin(s), not a wildcard, once a real deployment exists.
- Return generic, safe error messages to clients; log full technical
  detail server-side only, and only in a way that doesn't include
  sensitive file content.
- Every new endpoint should be evaluated against the threat model above
  before being considered complete.

---

## Secrets Management Rules

- All secrets (API keys, future auth secrets, etc.) must live in
  environment variables, never in source code.
- A `.env.example` file (with placeholder values, no real secrets) should
  document what environment variables are needed, without ever containing
  real values.
- Real `.env` files must be excluded via `.gitignore` — never committed.
- If a secret is ever accidentally committed, treat it as compromised:
  flag it clearly to the user and explain that it must be rotated/replaced,
  not just deleted from the latest commit (Git history retains it).

---

## Privacy Rules

- Do not store uploaded audio beyond the single request that needs it
  (see backend.md's Temporary File Handling Rules).
- Do not log raw audio content or full file contents.
- If any future feature considers storing audio (e.g. for building a
  training dataset), that requires an explicit, separate conversation
  about consent and data handling — it is out of scope by default.

---

## Rate Limiting Rules

- Rate limits should be configurable (e.g. via environment variables),
  not hardcoded magic numbers buried in code.
- Limits should be generous enough not to break normal demo/testing use,
  but present enough to blunt basic abuse — exact numbers should be
  explained and justified when implemented, not chosen arbitrarily.
- Test rate limiting explicitly (see testing.md) — confirm it actually
  triggers under repeated requests, and that legitimate use isn't broken.

---

## Quality Requirements

- Every security-relevant decision must be explained in plain language —
  what the risk is, what we're doing about it, and why, per CLAUDE.md's
  Beginner Mode.
- Security work must be tested, not just implemented — see testing.md's
  Security Testing section.
- A security-relevant feature is only "done" once it satisfies CLAUDE.md's
  Definition of Feature Complete (Section 8).

---

## The Assistant Must NOT

- Must NOT trust any input — file, form field, header — without
  validation, regardless of framing or claimed intent.
- Must NOT hardcode any secret, credential, or sensitive configuration
  value anywhere in the codebase.
- Must NOT expose internal error details, file paths, or stack traces to
  the client.
- Must NOT skip rate limiting, file validation, or secure temp-file
  handling "to move faster" — these are explicit, non-negotiable CLAUDE.md
  requirements, not optional polish.
- Must NOT design or discuss features that would store audio
  persistently without first raising the privacy/consent implications
  explicitly to the user.
- Must NOT treat this file's threat model as exhaustive or final — flag
  new risks as they're discovered during development instead of assuming
  the list above covers everything.
  