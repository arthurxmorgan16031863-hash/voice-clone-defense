# Skill: Frontend Development — Voice Clone Defense

## Scope of This Skill
This skill governs all frontend work for Voice Clone Defense: UI structure,
UX flow, accessibility, and responsive design. It applies only to the
approved stack — **React + Vite (JavaScript)**. This file does not cover
backend, ML, or security logic (see backend.md, ai-audio.md, cybersecurity.md).

This skill is subordinate to CLAUDE.md. If anything here seems to conflict
with CLAUDE.md, CLAUDE.md wins.

---

## Responsibilities

When acting under this skill, the assistant is responsible for:

- Building and maintaining the React + Vite frontend.
- Implementing the required UX flow: open app → understand purpose →
  upload/record audio → start analysis → see processing status → see
  result → see confidence → understand why → see recommended action.
- Implementing loading, success, and error states for every async feature.
- Ensuring the UI works on both desktop and mobile widths.
- Ensuring the UI is usable by people relying on accessibility tools
  (screen readers, keyboard navigation).
- Explaining every UI decision in beginner-friendly terms, per CLAUDE.md's
  Beginner Mode and Development Communication Format.

---

## Approved Technologies (do not deviate)

- **React** (functional components + hooks — no class components unless
  there's a specific, explained reason).
- **Vite** as the build tool / dev server.
- Plain **CSS** (or CSS modules) for styling. No CSS-in-JS libraries, no
  component libraries (e.g. Material UI, Chakra) unless the user explicitly
  approves adding one — the approved architecture calls for plain CSS to
  keep the stack simple.
- **React Router** only if multiple distinct pages/screens are needed.

Do not introduce Next.js, Redux, TypeScript, Tailwind, or any other
framework/tool not listed in the approved architecture document, even if it
seems like a reasonable improvement. If you believe one would genuinely
help, explain why and ask before using it — do not add it silently.

---

## Important Rules

1. **State-driven UI.** Every async action (upload, analyze) must have
   explicit `loading`, `success`, and `error` states — never leave the user
   looking at a blank or ambiguous screen.
2. **No fabricated confidence.** The UI must never imply more certainty
   than the backend actually returns. Display the label, confidence score,
   indicators, and limitations exactly as provided — don't round up
   language (e.g., don't turn "Suspicious" into "Fake" in the UI).
3. **Consistent labels.** Use the exact result label wording agreed upon
   in CLAUDE.md/architecture docs. Do not invent new label variants in the
   UI layer.
4. **Small components.** Keep components focused on one responsibility
   (e.g., `ResultCard`, `ConfidenceMeter`, `UploadForm`) rather than one
   large monolithic component.
5. **No premature complexity.** Don't add global state management, routing
   complexity, or abstractions the app doesn't need yet — build for the
   current phase, not imagined future phases.

---

## Accessibility Requirements

- All interactive elements (buttons, upload controls) must be reachable
  and operable via keyboard alone.
- Use semantic HTML elements (`<button>`, `<label>`, `<main>`, `<nav>`)
  instead of generic `<div>`s with click handlers wherever possible.
- Every form input must have an associated, visible or screen-reader
  label — never rely on placeholder text alone as a label.
- Color must never be the only way information is conveyed (e.g., a
  "Suspicious" result should have a label/icon, not just a red color).
- Ensure sufficient color contrast for text and important UI elements.
- Loading and error states must be announced in a way assistive
  technology can detect (e.g., appropriate ARIA live regions for
  dynamically appearing status messages), explained simply when introduced.

---

## Responsive Design Requirements

- Layout must work correctly at common mobile widths (~375–414px) and
  standard desktop widths.
- Test every new screen/state at both a mobile and a desktop width before
  calling it done, per CLAUDE.md's Testing Requirements.
- Prefer flexible layout techniques (flexbox/grid with relative units)
  over fixed pixel widths that only work at one screen size.

---

## Quality Requirements

- Every new component must be explained in plain language before code is
  shown: what it does, why it exists, which file it lives in.
- No component should silently swallow errors — if an API call fails, the
  user must see a clear, non-technical error message.
- File and component names must be descriptive (`ResultCard.jsx`, not
  `Comp1.jsx`).
- Before a frontend feature is called "done," it must satisfy CLAUDE.md's
  Definition of Feature Complete (Section 8): implemented, tested, edge
  cases checked, documented where appropriate.

---

## The Assistant Must NOT

- Must NOT introduce a framework, library, or tool outside the approved
  architecture without explicit approval first.
- Must NOT build multiple phases of UI at once — follow the incremental,
  one-feature-at-a-time process from CLAUDE.md.
- Must NOT hardcode backend URLs, API keys, or secrets into frontend code
  — these belong in environment variables (see cybersecurity.md).
- Must NOT present a detection result as certain, guaranteed, or
  definitive in any UI copy, even casually (e.g., never write "This voice
  IS fake").
- Must NOT skip accessibility or responsive checks "to save time" — these
  are explicit CLAUDE.md/architecture requirements, not optional polish.
- Must NOT write application code without first explaining what/why/how
  and which files change, per CLAUDE.md's Development Communication Format.