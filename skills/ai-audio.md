# Skill: AI & Audio Processing — Voice Clone Defense

## Scope of This Skill
This skill governs audio feature extraction and the detection engine
itself: librosa/soundfile/numpy-based analysis, the Stage 1 heuristic
scoring engine, and (later) Stage 2 pretrained-model integration. This
file is subordinate to CLAUDE.md, especially its AI Detection Rules and
Research Rules.

---

## Responsibilities

When acting under this skill, the assistant is responsible for:

- Extracting numeric audio features from validated audio files.
- Building and maintaining the Stage 1 explainable heuristic detection
  engine.
- Producing results that always include: a label, a confidence score,
  triggered indicators, a plain-language explanation, stated limitations,
  and a recommended action.
- Later (only when explicitly approved), integrating a pretrained
  Wav2Vec2-based model as a second detection signal.
- Explaining audio/ML concepts in beginner-friendly terms — this is
  genuinely new territory for a beginner, so go slower here than in other
  areas.

---

## Approved Technologies (do not deviate)

**Stage 1 (current):**
- **librosa** — feature extraction (pitch, spectral features, etc.)
- **soundfile** — reading/writing audio files
- **numpy** — underlying numeric operations

**Stage 2 (future, only when explicitly approved to begin):**
- **transformers** (Hugging Face) — for loading a pretrained Wav2Vec2/
  WavLM-based real-vs-synthetic classifier
- **torchaudio** — audio loading/processing compatible with the pretrained
  model pipeline
- **torch** (CPU version is sufficient for a prototype)

Do not introduce other ML frameworks (e.g. TensorFlow), other audio
libraries, or attempt to train a model from scratch — this is explicitly
out of scope per the approved architecture (training from scratch requires
large labeled datasets and compute not realistic for this project).

---

## AI Detection Rules (from CLAUDE.md — repeated here because they are
## especially critical to this skill)

- Never claim 100% certainty. Never describe a result as guaranteed.
- Use only the agreed result labels (Likely Authentic / Suspicious or
  Possibly Synthetic / Likely Synthetic) — do not invent new ones in code
  or explanations.
- Every result must include: confidence score, indicators, explanation,
  limitations, recommended action.
- Both false positives and false negatives must be acknowledged when
  discussing or documenting detection quality — never present the system
  as flawless in either direction.

---

## Feature Extraction Rules

- Define a clear, documented list of features being extracted (e.g.
  pitch/F0 contour, jitter/shimmer-like variability, spectral flatness,
  silence/pause pattern) — don't add undocumented "black box" features.
- Handle edge cases explicitly: silence-only audio, extremely short
  clips, non-speech audio (e.g. music) — define and document fallback
  behavior rather than letting these crash or silently produce nonsense.
- Respect the file-size/length limits enforced at the backend layer
  (backend.md) — don't attempt to process files that should have already
  been rejected.

---

## Heuristic Scoring Rules (Stage 1)

- Every rule/threshold used in scoring must be traceable to a specific
  feature and explainable in plain language — if a rule can't be
  explained simply, it doesn't belong in the heuristic engine.
- Each triggered rule must produce a human-readable indicator string
  (e.g. "Pitch variation is unusually low, which can indicate synthetic
  speech") — never just a raw number with no explanation.
- Document the known accuracy limitations of the heuristic approach
  clearly and honestly — this is a prototype-level, explainable-but-
  imperfect method, and that must never be overstated.

---

## Research Rules (for this skill specifically)

- When choosing thresholds, features, or referencing "what real vs.
  synthetic speech looks like," prefer real research sources (academic
  papers, official documentation, established benchmarks like the
  ASVspoof series) over assumptions.
- Do not invent research findings, statistics, or claimed accuracy
  numbers. If something is uncertain, say so explicitly.
- If test/sample audio data is needed, prefer publicly available,
  properly licensed research datasets over ad hoc or unclear sources.

---

## Quality Requirements

- Every feature or scoring change must be explained (what/why/how) before
  code is written, per CLAUDE.md.
- Test against real, varied audio: genuine speech samples, known
  synthetic samples (from a legitimate dataset), silence, very short
  clips, noisy clips, non-speech audio.
- A detection-engine feature is only "done" once it satisfies CLAUDE.md's
  Definition of Feature Complete (Section 8), including documented
  limitations.

---

## The Assistant Must NOT

- Must NOT claim or imply certainty in any detection result, code
  comment, log message, or explanation.
- Must NOT begin Stage 2 (pretrained model integration) without explicit
  approval — Stage 1 must be complete, tested, and working first.
- Must NOT attempt to train a model from scratch.
- Must NOT invent research findings, benchmark numbers, or sources.
- Must NOT silently change result label wording, scoring weights, or
  thresholds without explaining the change and its impact.
- Must NOT process audio that hasn't already passed backend validation
  (file type, size, corruption checks) — this skill assumes that gate has
  already run.