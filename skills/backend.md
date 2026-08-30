# Skill: Backend Development — Voice Clone Defense

## Scope of This Skill
This skill governs backend API development: Python, FastAPI, REST
endpoints, file validation, and temporary file handling. Audio analysis
logic itself is covered separately in ai-audio.md; security-specific depth
is in cybersecurity.md. This file is subordinate to CLAUDE.md.

---

## Responsibilities

When acting under this skill, the assistant is responsible for:

- Building and maintaining the FastAPI backend.
- Defining clear, minimal REST endpoints (e.g. `/health`, `/analyze`).
- Validating all incoming files and request data before they reach any
  processing logic.
- Handling temporary file storage safely, ensuring deletion after use.
- Returning clear, structured, and safe API responses (including error
  responses that don't leak internal details).
- Explaining backend architecture in beginner-friendly terms before
  writing code, per CLAUDE.md.

---

## Approved Technologies (do not deviate)

- **Python 3.10+**
- **FastAPI** for the web framework
- **Uvicorn** as the ASGI server
- **python-multipart** for file upload handling
- Python's built-in **`tempfile`** module for temporary file handling

Do not introduce Flask, Django, Node/Express, or any database technology
not already approved (see the architecture doc — no database for v1). If a
new dependency seems genuinely necessary, explain why and ask before
adding it.

---

## REST API Design Rules

- Endpoints should be few, clear, and named after what they do
  (`POST /analyze`, `GET /health`) — not generic names like `/data`.
- Use FastAPI's built-in request/response models (Pydantic) to define the
  exact shape of data going in and out — this also gives us automatic
  validation and documentation for free.
- Every endpoint must have a clear, single responsibility.
- Use appropriate HTTP status codes (e.g., 400 for bad input, 413 for
  file-too-large, 500 only for genuine unexpected server errors) rather
  than returning 200 for everything.
- Keep CORS configuration as narrow as reasonably possible for local
  development (allow the frontend's dev origin), and revisit it before
  deployment.

---

## File Validation Rules (required for every upload endpoint)

Every file upload must be checked for, in this order:

1. **Presence** — reject empty/missing uploads with a clear message.
2. **File extension** — must match an explicit allow-list (e.g. `.wav`,
   `.mp3`); reject anything else.
3. **Actual file content/type** — do not trust the extension alone;
   verify the file's real content type before treating it as audio.
4. **File size** — reject anything over a defined limit (make the limit a
   named constant, not a magic number buried in code).
5. **Corruption check** — confirm the file can actually be opened/read as
   audio before passing it further into the pipeline.

Any failure at any step must return a clear, safe, non-technical error
message to the client, while any technical detail needed for debugging is
logged server-side only (never sent to the client).

---

## Temporary File Handling Rules

- Every uploaded file must be written to a temporary location using
  Python's `tempfile` module — never to a permanent or predictable path.
- File deletion must be guaranteed using `try/finally` (or a context
  manager), so the file is removed **even if processing fails or raises
  an error partway through.**
- Never log the full contents of an audio file. File names/paths used
  for debugging should not be exposed to the client.
- No uploaded audio should persist beyond the single request that
  produced it, per CLAUDE.md's privacy rule.

---

## Quality Requirements

- Every endpoint must be explained (what/why/how/files) before code is
  written, per CLAUDE.md's Development Communication Format.
- Every endpoint must be testable via FastAPI's auto-generated `/docs`
  page — a beginner should be able to try it there without extra tooling.
- Functions should be small and single-purpose (e.g., separate functions
  for "validate file," "save temp file," "run analysis," "clean up").
- A backend feature is only "done" once it satisfies CLAUDE.md's
  Definition of Feature Complete (Section 8).

---

## The Assistant Must NOT

- Must NOT trust any uploaded file or user input without full validation,
  regardless of how the request was framed or who claims to be using it.
- Must NOT store uploaded audio permanently, or longer than a single
  request's processing lifetime.
- Must NOT return raw exception messages, stack traces, file paths, or
  other internal details to the client.
- Must NOT hardcode secrets, file paths, or configuration values that
  should be environment variables.
- Must NOT introduce a database, authentication system, or new backend
  framework without explicit approval — these are out of scope per the
  approved architecture until a specific future need justifies them.
- Must NOT implement multiple endpoints/features in one pass — follow the
  incremental, one-feature-at-a-time process.