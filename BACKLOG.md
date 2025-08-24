# Onboarding UX Backlog

This backlog tracks future improvements for the onboarding experience beyond the current Module-per-File bundle (Option B).

## Option D: MkDocs Knowledge Site

- [ ] Scaffold MkDocs (mkdocs.yml + docs/) with Material theme
- [ ] Sync generated outputs (index.md, checklist.md, modules/*.md) into docs/
- [ ] Add search, tags, and improved navigation
- [ ] Add landing page with roadmap, time budget, and prerequisites
- [ ] Add CI build (GitHub Actions) to publish site (GitHub Pages/Netlify)
- [ ] Add styling and callouts (admonitions) for objectives, activities, and success criteria
- [ ] Add “Start here” checklist and per-module progress indicators
- [ ] Add versioning strategy for onboarding plans (optional)

## Option C: Interactive Learning App

- [ ] Lightweight Streamlit app with module-by-module view and progress tracking
- [ ] Local JSON persistence for progress; optional user auth later
- [ ] Inline quizzes and short-answer prompts with immediate feedback
- [ ] Upload evidence (links/screenshots) for activities, attach to module entries
- [ ] Export progress report (PDF/Markdown)
- [ ] Calendar export (ICS) for time-boxed schedule
- [ ] Optional integration with Notion/Confluence for team visibility

## Enhancements (cross-cutting)

- [ ] Automatic citation trails to source excerpts with paraphrase notes
- [ ] Lint / validate outputs for required sections per module
- [ ] Add a sync script to regenerate and stage docs for MkDocs automatically
- [ ] Add tests for splitting, slugging, and index/checklist generation
