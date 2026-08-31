# Skill: Documentation — Voice Clone Defense

## Scope of This Skill
This skill governs all project documentation: README, architecture docs,
setup instructions, testing documentation, limitations, and project
contribution documentation. This file is subordinate to CLAUDE.md's
Documentation Rules (Section 15).

---

## Responsibilities

When acting under this skill, the assistant is responsible for:

- Keeping `README.md` and the `docs/` folder accurate and in sync with
  what has actually been built (never aspirational or ahead of reality).
- Writing all documentation in beginner-readable language.
- Explicitly and honestly documenting known limitations — especially
  around detection accuracy, per CLAUDE.md's AI Detection Rules.
- Maintaining clear setup/installation instructions that a stranger could
  follow on a clean machine.
- Producing clear contribution documentation so other contributors
  can understand and extend the project.

---

## Required Documentation Set

Per CLAUDE.md Section 15, the project must maintain:

- `README.md` — project overview, problem statement, quick start
- `docs/ARCHITECTURE.md` — the approved technical architecture
- `docs/INSTALLATION.md` — step-by-step setup instructions
- `docs/USAGE.md` — how to use the running application
- `docs/TESTING.md` — what's tested and how (backend automated +
  frontend manual checklist, per testing.md)
- `docs/SECURITY.md` — security measures in place, per cybersecurity.md
- `docs/LIMITATIONS.md` — honest statement of what the system can't
  reliably do
- `docs/FUTURE_IMPROVEMENTS.md` — planned/possible future work (including
  clearly-labeled stretch goals like Stage 2 ML integration or real-time
  streaming)
- `docs/CONTRIBUTING.md` — contribution guidance for project contributors

---

## README Requirements

The README must include, at minimum:

- A one-paragraph, plain-language description of what the project does
  and why it exists.
- An explicit statement that this is a prototype and does not guarantee
  detection accuracy (matching CLAUDE.md's AI Detection Rules).
- Quick-start instructions or a link to `docs/INSTALLATION.md`.
- A short "current status" section reflecting what's actually implemented
  right now — not the full roadmap presented as if it's done.

---

## Architecture Documentation Requirements

- Must reflect the actually-approved architecture (frontend.md, backend.md,
  ai-audio.md stacks) — do not document technologies that were considered
  but not chosen without clearly labeling them as rejected alternatives.
- Should explain *why* each major technology was chosen, not just list it
  — beginners benefit from the reasoning, not just the decision.
- Must be updated whenever a real architectural change happens (e.g., when
  Stage 2 ML integration begins) — documentation drift is treated as a bug.

---

## Setup / Installation Documentation Requirements

- Instructions must be followable by someone with no prior context, on a
  clean machine — exact commands, exact expected output, per CLAUDE.md's
  Beginner Mode.
- Must specify exact versions/requirements (e.g. "Python 3.10+", "Node.js
  LTS") rather than vague statements like "recent Python."
- Should include a basic troubleshooting section for common early errors
  (e.g. port conflicts, missing dependencies).

---

## Testing Documentation Requirements

- Must reflect the actual current test coverage — what's automated
  (pytest/httpx) and what's manual (frontend checklist), per testing.md.
- The manual frontend checklist itself should live here, kept up to date
  as new features/states are added.
- Should note any known gaps in coverage honestly rather than implying
  full coverage exists.

---

## Limitations Documentation Requirements (especially important)

This section must never be skipped or softened. It must clearly state:

- Detection is probabilistic and can produce false positives and false
  negatives.
- The heuristic engine (Stage 1) has meaningfully lower accuracy than
  state-of-practice deep learning detectors.
- The system does not support true real-time/live audio analysis (v1 is
  upload-and-analyze only).
- No claim of guaranteed or certain detection should ever appear anywhere
  in the documentation, matching CLAUDE.md's AI Detection Rules exactly.

---
## Contribution Documentation Requirements


- `docs/CONTRIBUTING.md` should explain, in beginner-friendly terms: how
  to set up the project, the branch/PR workflow (per the approved Git
  workflow), coding conventions, and how to run tests before submitting a
  PR.
- Should reference CLAUDE.md as the authoritative project instruction
  file for anyone (human or AI-assisted) contributing to the project.
- Should make clear that incremental, tested, documented contributions are
  expected — matching the project's own development philosophy.

---

## Quality Requirements

- Documentation must be reviewed/updated as part of finishing a feature,
  not deferred indefinitely — per CLAUDE.md's Definition of Feature
  Complete (Section 8), documentation is part of "done," not an
  afterthought.
- Language must stay beginner-accessible throughout — avoid unexplained
  jargon here just as much as in conversation.
- Documentation should be periodically spot-checked against the actual
  running application (e.g., literally following the installation steps)
  to catch drift.

---

## The Assistant Must NOT

- Must NOT document features, endpoints, or capabilities that don't
  actually exist yet or aren't fully working.
- Must NOT soften, omit, or bury the Limitations documentation — this is
  a core project requirement, not optional context.
- Must NOT let documentation silently fall out of sync with the code —
  flag drift explicitly when noticed, rather than leaving it.
- Must NOT invent setup steps, version numbers, or instructions that
  haven't actually been verified to work.
- Must NOT write documentation for future/unapproved phases as if they
  were current — clearly separate "what exists now" from "what's planned."