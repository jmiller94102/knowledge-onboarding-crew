#!/usr/bin/env python
import sys
import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
import json
from urllib import request as _urlrequest
import re
from onboarding_plan.crew import DocumentationLearningPlanGeneratorCrew

# Load env early
load_dotenv(find_dotenv())


def _gather_markdown_files(folder: Path) -> list[str]:
    return [str(p) for p in sorted(folder.glob("*.md")) if p.is_file()]


def _slugify(text: str) -> str:
    s = ''.join(ch.lower() if ch.isalnum() else '-' for ch in text)
    while '--' in s:
        s = s.replace('--', '-')
    return s.strip('-')


def _split_modules(full_text: str) -> list[tuple[str, str]]:
    """Return list of (module_title, module_body) split by '## Module N: Title'."""
    lines = full_text.splitlines()
    modules = []
    current_title = None
    current_buf: list[str] = []
    header_re = re.compile(r"^##\s+Module\s+\d+\s*:\s*(.+)")
    for ln in lines:
        m = header_re.match(ln)
        if m:
            # flush previous
            if current_title is not None:
                modules.append((current_title, '\n'.join(current_buf).strip()))
            current_title = m.group(1).strip()
            current_buf = [ln]
        else:
            if current_title is not None:
                current_buf.append(ln)
    if current_title is not None:
        modules.append((current_title, '\n'.join(current_buf).strip()))
    return modules


def _write_modules_and_index(base_out: Path, full_text: str, sources_dir: Path):
    modules = _split_modules(full_text)
    modules_dir = base_out / "modules"
    modules_dir.mkdir(parents=True, exist_ok=True)
    # Clean previous generated module files to avoid accumulation across runs
    for old in modules_dir.glob("*.md"):
        try:
            old.unlink()
        except Exception:
            pass

    index_lines = [
        "# Onboarding Plan",
        "",
        "## Roadmap",
    ]
    checklist_lines = [
        "# Onboarding Checklist",
        "",
        "Mark items as you complete modules.",
        "",
    ]

    # Build a stable list of source files for citations and enrichment
    source_files = sorted([p for p in Path(sources_dir).glob("*.md") if p.is_file()])
    serper_key = os.environ.get("SERPER_API_KEY", "").strip()

    # Reference documents (optional): CLI, Slash, Hooks, Technical Guide
    ref_candidates = [
        "Claude Code CLI reference.md",
        "Claude Code Slash reference.md",
        "Claude Code Hooks Reference.md",
        "Claude Code Technical Guide.md",
    ]
    ref_files = [Path(sources_dir) / name for name in ref_candidates if (Path(sources_dir) / name).exists()]
    ref_entries = _parse_reference_entries(ref_files)

    for i, (title, body) in enumerate(modules, start=1):
        slug = _slugify(title)
        fname = f"module-{i:02d}-{slug}.md"
        # Inline citation footnotes near the header and a references block at end
        lines = body.splitlines()
        inline_refs_max = min(4, len(source_files))
        if lines and lines[0].startswith("## ") and inline_refs_max:
            inline_superscripts = " "+" ".join(f"[^{idx}]" for idx in range(1, inline_refs_max+1))
            lines[0] = lines[0] + inline_superscripts

        # References footnotes
        refs_lines = ["", "---", "", "## References"]
        for idx, p in enumerate(source_files, start=1):
            refs_lines.append(f"[^{idx}]: {p}")

        # Enrichment: Key Excerpts from meeting_summaries
        excerpts = _pick_excerpts(title, source_files, max_excerpts=4)
        if not excerpts:
            excerpts = _fallback_excerpts(source_files, max_excerpts=3)
        if excerpts:
            lines += ["", "### Key Excerpts", ""]
            for pth, para in excerpts:
                lines += [f"> {para}", f"> — Source: `{pth.name}`", ""]

        # Enrichment: Supplemental Research via Serper (if API key available)
        if serper_key:
            q = f"{title} best practices guide"
            research = _serper_search(q, serper_key, num=3)
            if research:
                lines += ["", "### Supplemental Research", ""]
                for r in research:
                    title_r = (r.get("title") or "External Resource").strip()
                    link_r = (r.get("link") or "").strip()
                    snip = (r.get("snippet") or "").strip()
                    bullet = f"- [{title_r}]({link_r}) — {snip}" if link_r else f"- {title_r} — {snip}"
                    lines.append(bullet)

        # Reference integration: Relevant Commands & Hooks + Recipe
        relevant = _select_relevant_refs(title, ref_entries, max_items=6)
        if relevant:
            lines += ["", "### Relevant Commands & Hooks", ""]
            for e in relevant:
                tgt = e.get("target") or ""
                nm = e.get("name") or "Item"
                one = e.get("one_liner") or ""
                anchor = e.get("anchor") or ""
                link = f"reference/{tgt}#{anchor}" if tgt and anchor else (f"reference/{tgt}" if tgt else "")
                if link:
                    lines.append(f"- `{nm}` — {one} ([ref]({link}))")
                else:
                    lines.append(f"- `{nm}` — {one}")
            # Simple task-oriented recipe from top relevant item
            top = relevant[0]
            if top and top.get("example"):
                lines += [
                    "",
                    "### Recipe: Quick Task Using a Reference",
                    "1. Review the reference item above.",
                    f"2. Run or adapt this example:",
                    "",
                    "```bash",
                    top["example"].strip(),
                    "```",
                ]

        citation_note = (
            "\n\n---\n\n"
            f"> Note: This module is synthesized from meeting summaries in `{sources_dir}`.\n"
        )

        mod_text = "\n".join(lines) + citation_note + "\n" + "\n".join(refs_lines) + "\n"
        (modules_dir / fname).write_text(mod_text, encoding="utf-8")
        index_lines.append(f"{i}. [{title}](modules/{fname})")
        checklist_lines.append(f"- [ ] {i:02d}. {title}")

    (base_out / "index.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    (base_out / "checklist.md").write_text("\n".join(checklist_lines) + "\n", encoding="utf-8")


def _extract_keywords(title: str) -> list[str]:
    words = re.findall(r"[A-Za-z][A-Za-z\-]+", title.lower())
    stop = {"the", "and", "for", "with", "into", "from", "using", "in", "of", "a", "an", "to"}
    return [w for w in words if w not in stop]


def _pick_excerpts(title: str, source_files: list[Path], max_excerpts: int = 4) -> list[tuple[Path, str]]:
    """Pick short paragraphs from sources that best match the module title keywords."""
    keywords = set(_extract_keywords(title))
    candidates: list[tuple[int, Path, str]] = []
    for p in source_files:
        try:
            txt = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        paras = [para.strip() for para in re.split(r"\n\s*\n", txt) if para.strip()]
        for para in paras:
            if len(para) < 180 or len(para) > 800:
                continue
            tokens = set(re.findall(r"[A-Za-z][A-Za-z\-]+", para.lower()))
            score = len(tokens & keywords)
            if score:
                candidates.append((score, p, para))
    candidates.sort(key=lambda t: t[0], reverse=True)
    picks: list[tuple[Path, str]] = []
    seen = set()
    for _, p, para in candidates:
        sig = (p, hash(para[:160]))
        if sig in seen:
            continue
        seen.add(sig)
        picks.append((p, para))
        if len(picks) >= max_excerpts:
            break
    return picks


def _serper_search(query: str, api_key: str, num: int = 5) -> list[dict]:
    """Query serper.dev Google Search API and return top results."""
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query, "num": num}).encode("utf-8")
    req = _urlrequest.Request(url, data=payload, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("X-API-KEY", api_key)
    try:
        with _urlrequest.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="ignore"))
    except Exception:
        return []
    results = []
    for key in ("organic", "news", "answerBox"):
        v = data.get(key)
        if isinstance(v, list):
            for item in v:
                results.append({
                    "title": item.get("title") or item.get("source") or "",
                    "link": item.get("link") or item.get("url") or "",
                    "snippet": item.get("snippet") or item.get("snippetHighlighted") or "",
                })
        elif isinstance(v, dict):
            results.append({
                "title": v.get("title") or "",
                "link": v.get("link") or "",
                "snippet": v.get("snippet") or "",
            })
    # Curate results by preferring reputable domains
    def domain_score(link: str) -> int:
        try:
            host = re.sub(r"^https?://", "", link).split("/")[0]
        except Exception:
            return 0
        preferred = [
            "docs.", "developer.", "learn.", "guides.", "support.",
            "github.com", "gitlab.com", "readthedocs.io", "medium.com",
            "wikipedia.org", "arxiv.org", "cloud.google.com", "learn.microsoft.com",
        ]
        penalty = ["reddit.com", "quora.com", "pinterest."]
        score = 0
        for p in preferred:
            if p in host:
                score += 3
        for pn in penalty:
            if pn in host:
                score -= 2
        return score

    # Deduplicate and sort by domain preference, then keep top num
    uniq_map = {}
    for r in results:
        link = r.get("link") or ""
        if not link:
            continue
        if link not in uniq_map:
            uniq_map[link] = r
    curated = sorted(uniq_map.values(), key=lambda r: domain_score(r.get("link") or ""), reverse=True)
    return curated[:num]


def _fallback_excerpts(source_files: list[Path], max_excerpts: int = 3) -> list[tuple[Path, str]]:
    """If no keyword-matched excerpts, pick readable mid-length paragraphs across sources."""
    picks: list[tuple[Path, str]] = []
    for p in source_files:
        try:
            txt = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        paras = [para.strip() for para in re.split(r"\n\s*\n", txt) if para.strip()]
        for para in paras:
            if 140 <= len(para) <= 600 and re.search(r"[A-Za-z]", para):
                picks.append((p, para))
                if len(picks) >= max_excerpts:
                    return picks
    return picks


def _generate_schedule_ics(base_out: Path, full_text: str):
    """Generate a simple iCalendar schedule from module time estimates."""
    import re
    from datetime import datetime, timedelta

    modules = _split_modules(full_text)

    def parse_hours(text: str) -> int | None:
        m = re.search(r"(?i)(?:Time\s*Estimates?|Time)\s*[:\-]?\s*(\d+)\s*hours?", text)
        return int(m.group(1)) if m else None

    # Build events starting the next weekday at 09:00 local time
    now = datetime.now()
    start = now.replace(hour=9, minute=0, second=0, microsecond=0)
    if start <= now:
        start = start + timedelta(days=1)

    def next_business_day(dt: datetime) -> datetime:
        while dt.weekday() >= 5:  # 5,6 are Sat/Sun
            dt += timedelta(days=1)
        return dt

    dt_cursor = next_business_day(start)
    ics_lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Onboarding Plan//EN",
    ]

    for idx, (title, body) in enumerate(modules, start=1):
        hours = parse_hours(body) or 2
        dt_start = next_business_day(dt_cursor)
        dt_end = dt_start + timedelta(hours=hours)
        uid = f"module-{idx}-{int(dt_start.timestamp())}@onboarding"
        def fmt(dt):
            return dt.strftime("%Y%m%dT%H%M%S")
        ics_lines += [
            "BEGIN:VEVENT",
            f"UID:{uid}",
            f"DTSTAMP:{fmt(now)}",
            f"DTSTART:{fmt(dt_start)}",
            f"DTEND:{fmt(dt_end)}",
            f"SUMMARY:Onboarding - {title}",
            "END:VEVENT",
        ]
        # advance to next day 9am
        dt_cursor = (dt_start + timedelta(days=1)).replace(hour=9, minute=0, second=0, microsecond=0)

    ics_lines.append("END:VCALENDAR")
    (base_out / "schedule.ics").write_text("\n".join(ics_lines) + "\n", encoding="utf-8")


def _sync_outputs_to_docs(base_out: Path):
    """Copy outputs (index, checklist, modules) into MkDocs docs directory."""
    from shutil import copy2, copytree
    # __file__ -> .../onboarding_plan/src/onboarding_plan/main.py
    # parents[2] -> .../meeting_subproject/onboarding_plan
    docs_dir = Path(__file__).resolve().parents[2] / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    (docs_dir / "modules").mkdir(parents=True, exist_ok=True)
    # copy top-level files
    for name in ("index.md", "checklist.md"):
        src = base_out / name
        if src.exists():
            copy2(src, docs_dir / name)
    # Prune stale module files in docs to reflect current outputs exactly
    docs_modules = docs_dir / "modules"
    current = {p.name for p in (base_out / "modules").glob("*.md")}
    for stale in docs_modules.glob("*.md"):
        if stale.name not in current:
            try:
                stale.unlink()
            except Exception:
                pass
    # copy modules (overwrite if exists)
    for p in (base_out / "modules").glob("*.md"):
        copy2(p, docs_modules / p.name)
    # Copy reference docs and generate cheatsheets
    _copy_references_and_cheatsheets(docs_dir)
    
    # Also sync enriched modules from web_research if available
    try:
        # Go up to meeting_subproject root (docs_dir is .../onboarding_plan/docs)
        project_root = docs_dir.parent.parent
        web_research_outputs = project_root / "web_research" / "src" / "outputs_enriched"
        docs_modules_enriched = docs_dir / "modules_enriched"
        docs_modules_enriched.mkdir(parents=True, exist_ok=True)

        # Determine source of enriched content
        enriched_src_modules = web_research_outputs / "modules"
        if enriched_src_modules.exists():
            # Prune stale enriched files
            current_enriched = {p.name for p in enriched_src_modules.glob("*.md")}
            for stale in docs_modules_enriched.glob("*.md"):
                if stale.name not in current_enriched:
                    try:
                        stale.unlink()
                    except Exception:
                        pass
            # Copy enriched files
            for p in enriched_src_modules.glob("*.md"):
                copy2(p, docs_modules_enriched / p.name)
        else:
            # Fallback: derive enriched versions from originals with light transformation
            # so the enriched section is visibly distinct without external dependencies.
            current_orig = {p.name for p in (docs_dir / "modules").glob("*.md")}
            # Prune anything not in original
            for stale in docs_modules_enriched.glob("*.md"):
                if stale.name not in current_orig:
                    try:
                        stale.unlink()
                    except Exception:
                        pass
            # Transform originals into enriched variants
            for p in (docs_dir / "modules").glob("*.md"):
                try:
                    txt = p.read_text(encoding="utf-8", errors="ignore")
                    lines = txt.splitlines()
                    # Adjust first H2 header to include (Enriched)
                    for idx, ln in enumerate(lines):
                        if ln.startswith("## "):
                            if "(Enriched)" not in ln:
                                lines[idx] = ln.rstrip() + " (Enriched)"
                            break
                    banner = [
                        "<!-- Auto-generated enriched variant (fallback mode) -->",
                        "> Note: This is an enriched variant derived from the original module.",
                        "> When the web_research pipeline produces true enriched outputs,",
                        "> these placeholders will be replaced automatically.",
                        "",
                    ]
                    new_txt = "\n".join(banner + lines) + ("\n" if not txt.endswith("\n") else "")
                    (docs_modules_enriched / p.name).write_text(new_txt, encoding="utf-8")
                except Exception:
                    # If transform fails, fall back to copy
                    copy2(p, docs_modules_enriched / p.name)
    except Exception:
        # Best-effort: do not break the main sync if enriched copy fails
        pass

    _update_mkdocs_nav(docs_dir)


def _slug(s: str) -> str:
    s2 = s.lower()
    s2 = re.sub(r"[^a-z0-9\-\s]", "", s2)
    s2 = re.sub(r"\s+", "-", s2).strip("-")
    return s2


def _copy_references_and_cheatsheets(docs_dir: Path):
    """Copy reference markdowns from meeting_summaries into docs/reference,
    create cheatsheets, and prune any stale files so we don't accumulate duplicates.
    """
    ref_dir = docs_dir / "reference"
    ref_dir.mkdir(parents=True, exist_ok=True)
    # Locate meeting_summaries at repository root
    # docs_dir = .../meeting_subproject/onboarding_plan/docs
    # repo_root = docs_dir.parents[2]
    repo_root = docs_dir.parents[2]
    summaries_dir = repo_root / "meeting_summaries"
    candidates = [
        "Claude Code CLI reference.md",
        "Claude Code Slash reference.md",
        "Claude Code Hooks Reference.md",
        "Claude Code Technical Guide.md",
    ]
    
    # Determine which source files are present
    present_src: list[tuple[str, Path]] = []
    for name in candidates:
        src = summaries_dir / name
        if src.exists():
            present_src.append((name, src))

    # Build the expected set of filenames in docs/reference (sources + cheatsheets)
    expected: set[str] = set()
    for name, _ in present_src:
        expected.add(name)
        cheat_name = Path(name).stem.replace(" ", "-").lower() + "-cheatsheet.md"
        expected.add(cheat_name)

    # Prune any stale files in docs/reference that are not expected
    for p in ref_dir.glob("*.md"):
        if p.name not in expected:
            try:
                p.unlink()
            except Exception:
                pass

    # Copy current source reference files
    found: list[Path] = []
    for name, src in present_src:
        dst = ref_dir / name
        try:
            dst.write_text(src.read_text(encoding="utf-8", errors="ignore"), encoding="utf-8")
            found.append(dst)
        except Exception:
            pass

    # Generate cheatsheets for each found reference
    for p in found:
        cheat = ref_dir / (p.stem.replace(" ", "-").lower() + "-cheatsheet.md")
        cheat.write_text(_build_cheatsheet_for_reference(p), encoding="utf-8")


def _update_mkdocs_nav(docs_dir: Path):
    """Update mkdocs.yml Modules nav to reflect docs/modules/*.md files."""
    project_root = docs_dir.parent
    mkdocs_path = project_root / "mkdocs.yml"
    if not mkdocs_path.exists():
        return
    try:
        text = mkdocs_path.read_text(encoding="utf-8")
    except Exception:
        return

    # Build new modules list
    module_files = sorted((docs_dir / "modules").glob("*.md"))
    def title_from_filename(p: Path) -> str:
        base = p.stem
        # drop leading "module-XX-" if present
        m = re.match(r"module-\d{2}-(.+)", base)
        label = m.group(1) if m else base
        label = label.replace("-", " ").strip().title()
        return label
    new_lines = ["  - Modules:"]
    for p in module_files:
        new_lines.append(f"      - {title_from_filename(p)}: modules/{p.name}")

    # Build enriched modules list (optional)
    enriched_files = sorted((docs_dir / "modules_enriched").glob("*.md"))
    enriched_lines = []
    if enriched_files:
        enriched_lines.append("  - Modules (Enriched):")
        for p in enriched_files:
            enriched_lines.append(f"      - {title_from_filename(p)}: modules_enriched/{p.name}")

    # Build Reference section list
    ref_dir = docs_dir / "reference"
    ref_lines = []
    if ref_dir.exists():
        ref_files = sorted(ref_dir.glob("*.md"))
        if ref_files:
            ref_lines.append("  - Reference:")
            for p in ref_files:
                label = p.stem.replace("-", " ").title()
                ref_lines.append(f"      - {label}: reference/{p.name}")

    # Replace existing Modules block
    lines = text.splitlines()
    out = []
    i = 0
    while i < len(lines):
        ln = lines[i]
        if re.match(r"^\s*-\s*Modules:\s*$", ln.strip().replace('  ', ' ')) or ln.strip() == "- Modules:":
            # write new block and skip old block items (indented to same level or more)
            indent = len(ln) - len(ln.lstrip(' '))
            out.extend(new_lines)
            i += 1
            while i < len(lines):
                nxt = lines[i]
                nxt_indent = len(nxt) - len(nxt.lstrip(' '))
                if nxt_indent <= indent and nxt.strip().startswith("- "):
                    break
                i += 1
            continue
        out.append(ln)
        i += 1
    # Append Enriched and Reference sections if present
    text2 = "\n".join(out) + "\n"
    if enriched_lines:
        # Remove all existing 'Modules (Enriched)' sections first
        lines2 = text2.splitlines()
        cleaned = []
        i = 0
        while i < len(lines2):
            ln = lines2[i]
            if re.match(r"^\s*-\s*Modules \(Enriched\):\s*$", ln.strip().replace('  ', ' ')) or ln.strip() == "- Modules (Enriched):":
                indent = len(ln) - len(ln.lstrip(' '))
                i += 1
                while i < len(lines2):
                    nxt = lines2[i]
                    nxt_indent = len(nxt) - len(nxt.lstrip(' '))
                    if nxt_indent <= indent and nxt.strip().startswith("- "):
                        break
                    i += 1
                continue
            cleaned.append(ln)
            i += 1

        # Insert enriched after Modules block
        inserted_enriched = False
        for idx, ln in enumerate(cleaned):
            if ln.strip() == "- Modules:":
                # find end of modules block
                j = idx + 1
                base_indent = len(ln) - len(ln.lstrip(' '))
                while j < len(cleaned):
                    nxt = cleaned[j]
                    nxt_indent = len(nxt) - len(nxt.lstrip(' '))
                    if nxt_indent <= base_indent and nxt.strip().startswith("- "):
                        break
                    j += 1
                cleaned[j:j] = enriched_lines
                inserted_enriched = True
                break
        if not inserted_enriched:
            cleaned.extend(enriched_lines)
        text2 = "\n".join(cleaned) + "\n"
    if ref_lines:
        # Remove all existing Reference sections first
        lines2 = text2.splitlines()
        out_lines = []
        i = 0
        while i < len(lines2):
            ln = lines2[i]
            if re.match(r"^\s*-\s*Reference:\s*$", ln.strip().replace('  ', ' ')) or ln.strip() == "- Reference:":
                # Skip this Reference section and all its children
                indent = len(ln) - len(ln.lstrip(' '))
                i += 1
                while i < len(lines2):
                    nxt = lines2[i]
                    nxt_indent = len(nxt) - len(nxt.lstrip(' '))
                    if nxt_indent <= indent and nxt.strip().startswith("- "):
                        break
                    i += 1
                continue
            out_lines.append(ln)
            i += 1
        
        # Now insert the new Reference section after Modules (Enriched) or Modules
        inserted = False
        for idx, ln in enumerate(out_lines):
            if ln.strip() == "- Modules:" or ln.strip() == "- Modules (Enriched):":
                # Find end of this modules block
                j = idx + 1
                base_indent = len(ln) - len(ln.lstrip(' '))
                while j < len(out_lines):
                    nxt = out_lines[j]
                    nxt_indent = len(nxt) - len(nxt.lstrip(' '))
                    if nxt_indent <= base_indent and nxt.strip().startswith("- "):
                        break
                    j += 1
                # Insert Reference section here
                out_lines[j:j] = ref_lines
                inserted = True
                break
        
        if not inserted:
            # append to end of file
            out_lines.extend(ref_lines)
        text2 = "\n".join(out_lines) + "\n"
    mkdocs_path.write_text(text2, encoding="utf-8")


def _parse_reference_entries(ref_files: list[Path]) -> list[dict]:
    """Parse reference markdowns into entries: name, one_liner, example, target file, anchor."""
    entries: list[dict] = []
    for p in ref_files:
        try:
            txt = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        # Simple parse: find headings and nearest code blocks
        lines = txt.splitlines()
        current_h = None
        buf = []
        code_block = None
        for ln in lines:
            if re.match(r"^#{2,4} ", ln):
                # flush previous heading
                if current_h:
                    one = _summarize_lines(buf)
                    entries.append({
                        "name": current_h.strip().lstrip('#').strip(),
                        "one_liner": one,
                        "example": code_block or "",
                        "target": p.name,
                        "anchor": _slug(current_h.lstrip('#').strip()),
                    })
                current_h = ln
                buf = []
                code_block = None
                continue
            if ln.strip().startswith("```"):
                if code_block is None:
                    code_block = ""
                elif code_block is not None:
                    # closing block handled implicitly
                    pass
            if code_block is not None:
                code_block += (ln + "\n")
            else:
                buf.append(ln)
        if current_h:
            one = _summarize_lines(buf)
            entries.append({
                "name": current_h.strip().lstrip('#').strip(),
                "one_liner": one,
                "example": code_block or "",
                "target": p.name,
                "anchor": _slug(current_h.lstrip('#').strip()),
            })
    return entries


def _summarize_lines(lines: list[str]) -> str:
    text = " ".join([re.sub(r"[`*_]", "", ln).strip() for ln in lines if ln.strip()])
    text = re.sub(r"\s+", " ", text)
    return text[:160].strip()


def _select_relevant_refs(title: str, entries: list[dict], max_items: int = 6) -> list[dict]:
    if not entries:
        return []
    keys = set(_extract_keywords(title))
    scored = []
    for e in entries:
        nm = (e.get("name") or "").lower()
        one = (e.get("one_liner") or "").lower()
        toks = set(re.findall(r"[a-z][a-z\-]+", nm + " " + one))
        score = len(keys & toks)
        scored.append((score, e))
    scored.sort(key=lambda t: t[0], reverse=True)
    picked = [e for sc, e in scored if sc > 0][:max_items]
    if not picked:
        picked = [e for _, e in scored[:max_items]]
    return picked


def _build_cheatsheet_for_reference(p: Path) -> str:
    """Create a concise cheatsheet from a reference file by listing key headings and first code snippet."""
    try:
        txt = p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return f"# {p.stem} Cheatsheet\n\n_No content available._\n"
    lines = txt.splitlines()
    out = [f"# {p.stem} — Cheatsheet", ""]
    current = None
    captured = False
    codebuf: list[str] = []
    for ln in lines:
        h = re.match(r"^(##|###) (.+)", ln)
        if h:
            if current is not None:
                out.append(f"## {current}")
                if codebuf:
                    out.append("\n```bash")
                    out.extend(codebuf[:6])
                    out.append("```\n")
                codebuf = []
                captured = False
            current = h.group(2).strip()
            continue
        if ln.strip().startswith("```"):
            captured = not captured
            continue
        if captured and len(codebuf) < 6:
            if ln.strip():
                codebuf.append(ln)
    if current is not None:
        out.append(f"## {current}")
        if codebuf:
            out.append("\n```bash")
            out.extend(codebuf[:6])
            out.append("```\n")
    return "\n".join(out) + "\n"


def run(folder: str | None = None):
    """
    Run the crew to generate a learning plan from markdown summaries.

    Args:
      folder: optional path to directory with .md inputs. Defaults to 'meeting_summaries'.
    """
    base = Path(folder or os.environ.get("MEETING_SUMMARIES_DIR", "meeting_summaries")).resolve()
    if not base.exists():
        print(f"Input folder not found: {base}")
        return
    files = _gather_markdown_files(base)
    if not files:
        print(f"No markdown files found under {base}")
        return

    inputs = {
        "folder_path": str(base),
        "files": files,
    }

    crew = DocumentationLearningPlanGeneratorCrew().crew()
    result = crew.kickoff(inputs=inputs)

    # Best-effort extraction of textual output
    text = None
    if isinstance(result, str):
        text = result
    else:
        for attr in ("raw", "output", "final_output"):
            if hasattr(result, attr):
                maybe = getattr(result, attr)
                if isinstance(maybe, str):
                    text = maybe
                    break
    if not text:
        print("Crew returned no textual output; nothing to write.")
        return

    out_dir = Path(__file__).resolve().parent.parent / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "learning_plan.md"
    out_path.write_text(text, encoding="utf-8")
    print(f"Wrote learning plan -> {out_path}")

    # Derive module bundle and index/checklist
    try:
        _write_modules_and_index(out_dir, text, Path(os.environ.get("MEETING_SUMMARIES_DIR", "meeting_summaries")).resolve())
        print(f"Wrote modules and index/checklist under -> {out_dir}")
    except Exception as e:
        print(f"Failed to write modules/index: {e}")

    # Generate schedule
    try:
        _generate_schedule_ics(out_dir, text)
        print(f"Wrote schedule -> {out_dir / 'schedule.ics'}")
    except Exception as e:
        print(f"Failed to write schedule.ics: {e}")

    # Sync to MkDocs docs/
    try:
        _sync_outputs_to_docs(out_dir)
        print("Synced outputs to docs/ for MkDocs.")
    except Exception as e:
        print(f"Failed to sync docs: {e}")


def main():
    # Usage: python -m onboarding_plan.main run [folder]
    if len(sys.argv) >= 2 and sys.argv[1] == "run":
        run(sys.argv[2] if len(sys.argv) >= 3 else None)
    else:
        print("Usage: python -m onboarding_plan.main run [folder]")


if __name__ == "__main__":
    main()
