# Knowledge Capture and Onboarding Plan

A structured workspace for turning real-world knowledge (talks, interviews, transcripts, docs) into a navigable onboarding plan and reference site using MkDocs and an agentic enrichment pipeline.

This repo demonstrates a practical use case: capturing knowledge from departing employees during the typical two‑week resignation window and converting it into a durable, searchable onboarding plan that accelerates ramp-up for replacements.

---

## Why this exists: fix the broken knowledge capture process

Most teams handle knowledge transfer with rushed meetings, scattered notes, and ad‑hoc docs. That results in:

- Inefficient interviews and repeated questions
- Inconsistent or missing handoffs
- Onboarding plans that are outdated on day one

This project replaces that with a repeatable, automated pipeline that:

1. Captures raw knowledge (transcripts, notes, slides) into version control.
2. Summarizes and normalizes it into clean reference material.
3. Enriches the content with current best practices and links.
4. Publishes a consistent onboarding curriculum and knowledge base (MkDocs).

Outcome: Less manual effort, higher quality, durable institutional memory.

---

## Repository overview

- `meeting_transcripts/`
  - Raw transcripts and long-form notes (e.g., `transcript_full.txt`, `transcript2_full.txt`).
- `meeting_summaries/`
  - Curated summaries and references extracted from transcripts. These are human-readable source materials that feed enrichment and onboarding.
- `meeting_subproject/onboarding_plan/`
  - MkDocs site + orchestrator to compile onboarding docs.
  - Key paths:
    - `onboarding_plan/mkdocs.yml` — site configuration and nav
    - `onboarding_plan/docs/` — published documentation (generated/synced content lives here)
    - `src/onboarding_plan/main.py` — sync/transform logic to move content into `docs/`
    - `src/outputs/` — baseline outputs
    - `docs/modules_enriched/` — enriched, publish-ready modules
- `meeting_subproject/web_research/`
  - Agentic enrichment pipeline that augments modules with current research.
  - Key paths:
    - `src/web_research/crew.py` — Crew/agents definition (uses `EXA_API_KEY` if available)
    - `src/web_research/config/*.yaml` — tasks/agents configuration
    - `src/outputs_enriched/modules/` — enriched module markdown artifacts

---

## End-to-end knowledge-to-onboarding workflow

1. Capture knowledge
   - Place raw inputs in `meeting_transcripts/` (interviews, talks, demos).
   - Produce concise, structured summaries into `meeting_summaries/`.

2. Enrich modules with up-to-date research
   - Run the `web_research` crew to create enriched variants in
     `meeting_subproject/web_research/src/outputs_enriched/modules/`.

3. Sync into the onboarding site
   - `meeting_subproject/onboarding_plan/src/onboarding_plan/main.py` copies/syncs enriched content into
     `meeting_subproject/onboarding_plan/docs/modules_enriched/` and maintains nav.

4. Publish
   - Serve locally with MkDocs for review; deploy as needed.

This transforms a chaotic two-week handoff into a consistent, automated pipeline producing a durable onboarding curriculum.

---

## Quick start

Prereqs: Python 3.12+, Git. Recommended: a local virtualenv per subproject.

- Create and activate a venv for the MkDocs site:
  ```bash
  cd meeting_subproject/onboarding_plan
  python3 -m venv .venv
  . .venv/bin/activate
  pip install -r requirements.txt  # if present, or install mkdocs + plugins you use
  ```

- Serve MkDocs locally on port 8001:
  ```bash
  . .venv/bin/activate
  python -m mkdocs serve -a localhost:8001
  # Open http://localhost:8001
  ```

- Run enrichment (web_research):
  ```bash
  cd meeting_subproject/web_research
  # If using hatch/uv/pip-tools, install deps accordingly; otherwise:
  python3 -m venv .venv && . .venv/bin/activate
  pip install -e .
  # Optional: export EXA_API_KEY to enable EXA-powered search
  export EXA_API_KEY=...
  python -m web_research.main
  ```
  Outputs write to `src/outputs_enriched/modules/`.

- Sync enriched content to the onboarding site:
  ```bash
  cd meeting_subproject/onboarding_plan
  . .venv/bin/activate
  python -m onboarding_plan.main
  # Enriched files land in docs/modules_enriched/
  ```

---

## Configuration and environment

- `EXA_API_KEY` (optional)
  - Used by `meeting_subproject/web_research/src/web_research/crew.py` when available.
  - Set via environment variable to enable live research during enrichment.
- Local virtualenvs
  - Repo-level `.gitignore` excludes `**/.venv/` and `**/venv/` to keep environments out of Git.

---

## Project structure (partial)

```
windsurf-project/
├─ meeting_transcripts/
├─ meeting_summaries/
├─ meeting_subproject/
│  ├─ onboarding_plan/
│  │  ├─ mkdocs.yml
│  │  ├─ docs/
│  │  └─ src/
│  │     └─ onboarding_plan/main.py
│  └─ web_research/
│     ├─ src/web_research/crew.py
│     └─ src/outputs_enriched/modules/
├─ system-architecture.md
└─ README.md
```

---

## Common tasks

- Update summaries from transcripts
  - Add/update files under `meeting_transcripts/`, then curate `meeting_summaries/`.
- Regenerate enriched modules
  - Run `web_research` crew; verify content and citations.
- Refresh onboarding site
  - Run `onboarding_plan.main` to sync `modules_enriched/`; serve with MkDocs.

---

## Contributing

- Keep raw inputs in `meeting_transcripts/` and curated outputs in `meeting_summaries/`.
- Prefer small, reviewable PRs for content and config changes.
- Avoid committing local virtualenvs; ensure `.venv` stays ignored.

---

## License

Add your license here (e.g., Apache-2.0, MIT).
