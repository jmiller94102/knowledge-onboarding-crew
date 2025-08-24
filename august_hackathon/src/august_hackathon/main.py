#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
import os
import re
import json
from pathlib import Path
from august_hackathon.crew import MeetingTranscriptFormatterCrew
from dotenv import load_dotenv, find_dotenv

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information
#!/usr/bin/env python



# This main file is intended to be a way for your to run your
# crew locally, so refrain from adding unnecessary logic into this file.

# Load environment variables from .env if present
load_dotenv(find_dotenv())
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

# Global flags
FORCE_REPROCESS = "--force" in sys.argv
try:
    RETRY_MISSING_METADATA = int(os.environ.get("RETRY_MISSING_METADATA", "1"))
except Exception:
    RETRY_MISSING_METADATA = 1

def _extract_text(result):
    """Best-effort extraction of textual output from crewAI kickoff results."""
    if isinstance(result, str):
        return result
    for attr in ("raw", "output", "final_output"):
        if hasattr(result, attr):
            try:
                val = getattr(result, attr)
                if isinstance(val, str):
                    return val
            except Exception:
                pass
    if isinstance(result, dict):
        for k in ("final_output", "output", "raw"):
            if k in result and isinstance(result[k], str):
                return result[k]
        try:
            return json.dumps(result, ensure_ascii=False)
        except Exception:
            return str(result)
    return str(result)


def _slugify_short_name(text: str, max_words: int = 8) -> str:
    words = re.sub(r"[^a-zA-Z0-9]+", " ", text.lower()).strip().split()
    words = words[:max_words] if words else ["summary"]
    return "-".join(words) or "summary"


def _parse_metadata(md_text: str):
    """Parse Title and ShortFileName from the first ~10 lines of the output."""
    title = None
    short = None
    lines = md_text.splitlines()
    head = lines[:10]
    for line in head:
        if title is None:
            m = re.match(r"\s*Title:\s*(.+)\s*$", line, re.IGNORECASE)
            if m:
                title = m.group(1).strip()
        if short is None:
            m = re.match(r"\s*ShortFileName:\s*([a-z0-9\-]+)\s*$", line, re.IGNORECASE)
            if m:
                short = m.group(1).strip()
        if title and short:
            break
    if title and not short:
        short = _slugify_short_name(title)
    return title, short


def _missing_required_metadata(md_text: str) -> bool:
    title, short = _parse_metadata(md_text)
    return not (title and short)


def _unique_stem(out_dir: Path, base: str) -> str:
    """Return a unique stem by appending -2, -3, ... if needed."""
    stem = base
    i = 2
    while (out_dir / f"{stem}.md").exists() or (out_dir / f"{stem}.json").exists():
        stem = f"{base}-{i}"
        i += 1
    return stem


def _write_summary(text: str, out_dir: Path, default_stem: str, source_path: Path) -> Path:
    title, short = _parse_metadata(text)
    stem = short or _slugify_short_name(title or default_stem)
    stem = _unique_stem(out_dir, stem)
    md_path = out_dir / f"{stem}.md"
    md_path.write_text(text, encoding="utf-8")
    # Write sidecar metadata JSON
    meta = {
        "title": title,
        "shortFileName": stem,
        "source_file": str(source_path),
        "created_at": datetime.now().isoformat(),
    }
    (out_dir / f"{stem}.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    return md_path


def _process_one_transcript(path: Path, out_dir: Path) -> Path:
    crew = MeetingTranscriptFormatterCrew().crew()
    result = crew.kickoff(inputs={"file_path": str(path)})
    text = _extract_text(result)
    # Auto-retry if required metadata missing
    attempts = 0
    while _missing_required_metadata(text) and attempts < max(0, RETRY_MISSING_METADATA):
        attempts += 1
        result = crew.kickoff(inputs={"file_path": str(path)})
        text = _extract_text(result)
    return _write_summary(text, out_dir, default_stem=path.stem, source_path=path)


def _already_processed(out_dir: Path, transcript_path: Path) -> bool:
    """Return True if any sidecar JSON in out_dir references this transcript by basename.
    This is robust across relative/absolute paths because we match on basename.
    """
    basename = transcript_path.name
    for js in out_dir.glob("*.json"):
        try:
            data = json.loads(js.read_text(encoding='utf-8'))
            src = data.get("source_file")
            if src and Path(src).name == basename:
                return True
        except Exception:
            continue
    return False


def run():
    """
    Batch-run: read all .txt files in 'meeting_transcripts/' and write summaries
    to 'meeting_summaries/' with filenames derived from the model's ShortFileName.
    """
    input_dir = Path(os.environ.get("MEETING_INPUT_DIR", "meeting_transcripts"))
    output_dir = Path(os.environ.get("MEETING_OUTPUT_DIR", "meeting_summaries"))
    output_dir.mkdir(parents=True, exist_ok=True)
    input_dir.mkdir(parents=True, exist_ok=True)

    txt_files = sorted([p for p in input_dir.glob("*.txt") if p.is_file()])
    if not txt_files:
        print(f"No .txt files found in {input_dir.resolve()}. Add transcripts and re-run.")
        return
    print(f"Found {len(txt_files)} transcript(s) in {input_dir}.")

    error_log = output_dir / "_errors.log"
    for p in txt_files:
        print(f"Processing: {p.name} ...", end=" ")
        if not FORCE_REPROCESS and _already_processed(output_dir, p):
            print("skipped (already processed)")
            continue
        try:
            out_path = _process_one_transcript(p, output_dir)
            print(f"ok -> {out_path.relative_to(Path.cwd()) if out_path.is_absolute() else out_path}")
        except Exception as e:
            print("failed")
            msg = f"{datetime.now().isoformat()} | {p} | {e}\n"
            try:
                error_log.write_text((error_log.read_text(encoding='utf-8') if error_log.exists() else '') + msg, encoding='utf-8')
            except Exception:
                # best-effort logging; ignore failures
                pass


def run_one(file_path):
    """
    Run the crew on a single transcript file.
    """
    input_dir = Path(os.environ.get("MEETING_INPUT_DIR", "meeting_transcripts"))
    output_dir = Path(os.environ.get("MEETING_OUTPUT_DIR", "meeting_summaries"))
    output_dir.mkdir(parents=True, exist_ok=True)
    input_dir.mkdir(parents=True, exist_ok=True)

    path = Path(file_path)
    if not path.is_file():
        print(f"No file found at {path.resolve()}.")
        return
    print(f"Processing: {path.name} ...", end=" ")
    if not FORCE_REPROCESS and _already_processed(output_dir, path):
        print("skipped (already processed)")
        return
    try:
        out_path = _process_one_transcript(path, output_dir)
        print(f"ok -> {out_path.relative_to(Path.cwd()) if out_path.is_absolute() else out_path}")
    except Exception as e:
        print("failed")
        msg = f"{datetime.now().isoformat()} | {path} | {e}\n"
        error_log = output_dir / "_errors.log"
        try:
            error_log.write_text((error_log.read_text(encoding='utf-8') if error_log.exists() else '') + msg, encoding='utf-8')
        except Exception:
            # best-effort logging; ignore failures
            pass


def rerun_failures():
    """
    Rerun the crew on failed transcripts.
    """
    input_dir = Path(os.environ.get("MEETING_INPUT_DIR", "meeting_transcripts"))
    output_dir = Path(os.environ.get("MEETING_OUTPUT_DIR", "meeting_summaries"))
    output_dir.mkdir(parents=True, exist_ok=True)
    input_dir.mkdir(parents=True, exist_ok=True)

    error_log = output_dir / "_errors.log"
    if not error_log.exists():
        print(f"No error log found at {error_log.resolve()}.")
        return
    errors = error_log.read_text(encoding='utf-8').splitlines()
    if not errors:
        print(f"No errors found in {error_log.resolve()}.")
        return
    print(f"Found {len(errors)} error(s) in {error_log}.")
    for error in errors:
        path = Path(error.split(" | ")[1])
        if not path.is_file():
            print(f"No file found at {path.resolve()}.")
            continue
        print(f"Rerunning: {path.name} ...", end=" ")
        try:
            out_path = _process_one_transcript(path, output_dir)
            print(f"ok -> {out_path.relative_to(Path.cwd()) if out_path.is_absolute() else out_path}")
        except Exception as e:
            print("failed")
            msg = f"{datetime.now().isoformat()} | {path} | {e}\n"
            try:
                error_log.write_text((error_log.read_text(encoding='utf-8') if error_log.exists() else '') + msg, encoding='utf-8')
            except Exception:
                # best-effort logging; ignore failures
                pass


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'file_path': 'transcript_full.txt'
    }
    try:
        MeetingTranscriptFormatterCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        MeetingTranscriptFormatterCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'file_path': 'transcript_full.txt'
    }
    try:
        MeetingTranscriptFormatterCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: main.py <command> [<args>]")
        sys.exit(1)

    command = sys.argv[1]
    if command == "run":
        run()
    elif command == "run-one":
        if len(sys.argv) < 3:
            print("Usage: main.py run-one <file_path>")
            sys.exit(1)
        run_one(sys.argv[2])
    elif command == "rerun-failures":
        rerun_failures()
    elif command == "train":
        train()
    elif command == "replay":
        replay()
    elif command == "test":
        test()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
