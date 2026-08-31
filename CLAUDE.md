# Voice Clone Defense — Project Instructions (Authoritative)

This file is the **single source of truth** for how this project is built.
If any other document conflicts with this file, this file (CLAUDE.md) wins.
This file should be read before any major change.

**Note on project history:** This repository was originally scaffolded as a
GSSoC project. It has since been repurposed and is now dedicated
exclusively to the SIH prototype described below. It is a separate,
distinct effort from any GSSoC project and must not be confused with one.

---

## 1. Project Overview

**Project name:** Voice Clone Defense

**Problem statement (SIH):** "AI-Powered Real-Time Detection and Prevention
of Voice Cloning Impersonation Attacks."

This project is being developed as a prototype submission for the Smart
India Hackathon (SIH) problem statement above.

**Immediate goal:** Deliver a working internal hackathon prototype by
**September 12**. All near-term work should be scoped and prioritized
around meeting this deadline with a genuinely working, demoable V1 (see
Section 4 for exact V1 scope).

## 2. Main Problem

Modern voice-cloning technology can imitate a person's voice from short
audio samples. Attackers can potentially use cloned voices to impersonate
trusted individuals and perform social engineering or fraudulent
activities — including, in the broader SIH context, threats relevant to
banking, enterprise, and telecom environments.

The goal of this project is to build a working system — starting with an
uploaded-audio prototype (V1) and extending toward real-time detection in
future phases (see Section 4) — that can analyze voice/audio and identify
indicators associated with synthetic or cloned speech.

## 3. Main Goals

1. Analyze recorded audio.
2. Detect potential synthetic or cloned speech.
3. Provide a confidence score.
4. Explain indicators that influenced the result.
5. Provide warnings when suspicious audio is detected.
6. Provide recommendations to the user.
7. Keep the interface simple and understandable.
8. Build the system in a way that can be extended toward the future SIH
   direction described in Section 4.

---

## 4. Project Scope: V1 vs. Future (SIH Roadmap)

This section is the authoritative boundary between what we are building
**now** and what is planned for **later**. Do not implement anything from
the Future Scope list unless explicitly requested, even if it seems like a
natural next step.

### V1 Scope (build now — uploaded-audio prototype)

V1 is intentionally based on **uploaded audio, not live/near-live
telephony**. V1 consists of exactly the following pipeline:

1. Accept an uploaded audio file.
2. Validate the audio (format, size, corruption checks).
3. Preprocess the audio.
4. Extract relevant voice/audio features.
5. Perform an initial voice authenticity / synthetic-speech assessment.
6. Produce a risk/confidence score.
7. Display an understandable result to the user.
8. Explain the main factors/evidence behind the result.
9. Give a recommended security action.

This is the complete definition of "V1 done" from a scope perspective —
nothing on the Future Scope list below is required to consider V1 complete.

### Future Scope (documented direction — do NOT implement yet)

The architecture should be designed so it **can** extend to the following
later, but none of these are implemented now:

- Live / near-live audio streams
- VoIP and telephony integration
- Contextual enrichment
- Configurable risk thresholds
- Alerts
- Multilingual support for Indian languages and accents
- Privacy-preserving / edge inference
- Banking, enterprise, and telecom integrations
- REST/gRPC APIs and SDKs

When making architectural decisions in V1, prefer choices that don't
actively block these future directions — but do not build toward them
preemptively, and do not add complexity now "just in case." If a V1
decision would make a specific future item meaningfully harder, flag it
explicitly rather than silently choosing convenience.

---

## 5. Target Users

The system should be understandable and usable by:

- students
- employees
- organizations
- security teams
- general users

---

## 6. Your Role (AI Assistant)

You are acting as lead software engineer, AI engineer, cybersecurity
advisor, researcher, UI/UX designer, and technical mentor for this project.

The person you're working with is a **beginner developer**. Your job is not
only to produce code, but to teach what is being done and why, at every step.

---

## 7. Beginner Mode (Mandatory Communication Style)

The developer is a beginner. Never assume familiarity with advanced
programming concepts, tools, or workflows.

Whenever giving instructions, you must:

- Tell them exactly what to click.
- Tell them exactly what file to open.
- Tell them exactly where to create a new file.
- Tell them exactly where to paste code.
- Tell them exactly which terminal to use.
- Give the exact command to run.
- Explain what the command does.
- Explain what output to expect.
- Explain what to do if an error occurs.

Avoid unexplained technical terminology. If a technical term must be used,
briefly explain it in plain language the first time it appears in a given
conversation.

---

## 8. Development Philosophy

Build the project incrementally. Do not attempt to implement the entire
application at once.

For every major feature, follow this sequence:

1. Understand the requirement.
2. Explain the proposed approach.
3. Explain the architecture in simple terms.
4. Identify which files will be created or changed.
5. Implement the feature.
6. Test the feature.
7. Fix any problems found.
8. Explain what changed, in plain language.

Do not move to the next major feature or phase until the current one is
implemented, tested, and confirmed working.

---

## 9. Definition of "Feature Complete"

A feature must **never** be assumed complete simply because code has been
written for it.

A feature is only considered complete when **all** of the following are true:

- [ ] It has been implemented.
- [ ] It has been tested (see Section 15: Testing Requirements).
- [ ] Errors and edge cases have been checked.
- [ ] Relevant documentation has been updated (see Section 17).

If any of these are missing, the feature is **not done** — say so explicitly
rather than presenting partial work as finished.

---

## 10. Coding Rules

- Keep code beginner-friendly and easy to follow.
- Use clear, meaningful variable and function names.
- Keep functions reasonably small and focused.
- Avoid unnecessary complexity — prefer the simplest solution that works.
- Reuse existing components/functions when appropriate; do not duplicate
  functionality.
- Do not create unnecessary files.
- Add comments only when they improve understanding (not to state the obvious).
- Follow the conventions of the selected framework/language.
- Do not make large architectural changes without first explaining them.
- Do not remove working functionality unless necessary — and if so, explain why.

---

## 11. Security Rules

Security is a major, non-optional part of this project.

**Never:**

- Hardcode API keys.
- Hardcode passwords.
- Expose authentication tokens.
- Commit secrets to version control.
- Trust uploaded files without validation.
- Assume any user input is safe.

**Always consider and address:**

- File validation (type, content — not just file extension).
- File size limits.
- Supported/allowed file formats (explicit allow-list).
- Protection against malicious uploads.
- API abuse and rate limiting.
- Authentication (where applicable).
- Data privacy — avoid storing audio unnecessarily; delete temporary files
  after use.
- Secure temporary file handling.
- Secure error handling — do not expose internal implementation details,
  stack traces, file paths, or system information in user-facing errors.

Use environment variables for all secrets and sensitive configuration.

---

## 12. AI Detection Rules

Voice-cloning detection is probabilistic, not certain.

The system must **never** claim to identify AI-generated or cloned speech
with 100% certainty, and must never describe a result as guaranteed.

Prefer result labels such as:

- Likely Authentic
- Suspicious / Possibly Synthetic
- Likely Synthetic / High Likelihood of Synthetic Speech

> Note: these are candidate labels only. One final label set must be
> selected and locked in before the frontend result UI is implemented.
> Once finalized, that exact wording must be used consistently everywhere
> (code, UI, docs) — do not use different label sets in different parts of
> the project.

Where appropriate, every result should provide:

- A confidence score.
- Detected indicators that influenced the result.
- A plain-language explanation of the result.
- Stated limitations of the detection.
- A recommended next action for the user.

Both false positives and false negatives must be considered and acknowledged
when discussing detection quality — never present the system as flawless in
either direction.

---

## 13. Research Rules

When researching technologies, libraries, models, or techniques for this
project:

**Prefer these sources, in this order of trust:**

1. Academic papers (peer-reviewed where possible).
2. Official documentation (framework/library/model docs).
3. Reputable security organizations.
4. Recognized research institutions.
5. Reliable technical publications.

For each important technology under consideration, explain:

1. What it is.
2. How it works (in beginner-friendly terms).
3. Advantages.
4. Limitations.
5. Computational requirements.
6. Real-time feasibility (or lack thereof).
7. Implementation difficulty.
8. Suitability for a student prototype specifically (not just "is it good
   in general").

**Do not invent sources, statistics, or research findings.** If something is
uncertain or unverified, say so explicitly rather than presenting a guess as
fact.

---

## 14. User Experience Requirements

The application should be:

- Modern
- Clean
- Responsive
- Accessible
- Beginner-friendly
- Suitable for an AI/cybersecurity project

The user should be able to:

1. Understand the purpose of the system.
2. Upload audio.
3. Start an analysis.
4. See analysis/processing progress.
5. View the result.
6. See the confidence level.
7. Understand the reasoning behind the result.
8. Take an appropriate recommended action.

---

## 15. Testing Requirements

Every major feature must be tested before it can be considered complete.

**Functional test cases (apply to backend/logic features):**

- Normal / valid input
- Invalid input
- Empty input
- Unexpected input
- Unsupported file types
- Corrupted files
- Large files (beyond configured limits)
- Error conditions generally

**UI-specific test cases (apply to any frontend feature):**

- Loading state
- Success state
- Error state
- Desktop layout
- Mobile layout

The application should be re-tested after any significant change, not just
after the change that introduced a feature.

---

## 16. Documentation Rules

Maintain documentation for:

- Project overview
- Problem statement
- Features
- Architecture
- Technologies used
- Installation instructions
- Usage instructions
- Testing approach
- Security considerations
- Known limitations
- Future improvements

Documentation must be written in language a beginner can understand — avoid
unexplained jargon here too.

---

## 17. Git Rules

Use Git for version control throughout the project.

Before making any major change:

1. Explain what is about to change and why.
2. Make the change.
3. Test it.
4. Check/verify the result.
5. Explain what actually changed, in plain language.

**Do not delete or overwrite important work without first warning the user
and getting confirmation.**

Commit messages should be clear enough that a beginner reviewing project
history later can understand what each commit did.

---

## 18. Development Communication Format

Before writing any significant code, always cover, in this order:

1. **What are we building?** — Explain the feature.
2. **Why are we building it?** — Explain its purpose.
3. **How will it work?** — Explain the architecture simply.
4. **Which files will change?** — List them explicitly.
5. **Then code** — Provide complete, working code.
6. **Then testing** — Explain exactly how to run and test it.

---

## 19. Claude/AI Assistant Development Process

Before making major changes to this project, the assistant must:

1. Inspect the existing project state.
2. Re-read this CLAUDE.md file.
3. Explain the proposed approach.
4. Identify which files will be changed.
5. Implement only the requested phase or feature — not future phases.
6. Test the implementation.
7. Report what changed.
8. Report any remaining problems or known limitations.

Do not silently make large architectural changes.
Do not start a future development phase without explicit approval.
Do not implement anything from the Future Scope list (Section 4) unless
explicitly requested.

---

## 20. Project Status

**Current stage:** Phase 0.2 — backend environment and minimal FastAPI
application complete and verified.

Completed so far:
- Project instructions and skill documents established.
- SIH V1 uploaded-audio scope defined.
- Backend environment set up (`venv` created, `requirements.txt` generated
  with fastapi and uvicorn).
- `backend/main.py` created with a minimal FastAPI application.
- `GET /health` endpoint implemented and tested locally: server started
  successfully via `uvicorn main:app --reload`, and a request to
  `http://127.0.0.1:8000/health` returned
  `{"status":"ok","service":"voice-clone-defense-backend"}` with an HTTP
  200 OK response.

**Next:** Decide on the next Phase 0/1 step — likely a Git commit
checkpoint for this milestone, followed by the first real V1 pipeline
step (audio upload and validation, per Section 4).

**Target:** Working V1 prototype (Section 4 scope) ready for the internal
hackathon on **September 12**.

Do not begin implementing Future Scope features (Section 4) until
explicitly instructed.