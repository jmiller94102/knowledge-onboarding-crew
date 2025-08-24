#!/usr/bin/env python3
"""
YouTube Transcriber using Google Gemini

Usage:
  export GOOGLE_API_KEY=your_key_here
  python -m august_hackathon.youtube_transcribe --url "https://www.youtube.com/watch?v=JU8BwMe_BWg&t=30s"

Notes:
- Requires: pip install google-genai
- Model: gemini-2.5-pro-exp-03-25
- The Gemini YouTube connector ingests the video by URI. We ask for a full transcript.
"""

import os
import sys
import argparse
from typing import Optional

try:
    from google import genai
    from google.genai import types
except ImportError as e:
    print("Missing dependency. Please install with: pip install google-genai", file=sys.stderr)
    raise


DEFAULT_MODEL = "gemini-2.0-flash"
DEFAULT_PROMPT = (
    "Transcribe the following YouTube video in full as plain text. "
    "If speaker changes are inferable, include simple labels like 'Speaker 1:', 'Speaker 2:'. "
    "Do not summarize; output the full transcript only."
)


def transcribe_youtube(
    url: str,
    api_key: str,
    model: str = DEFAULT_MODEL,
    prompt: Optional[str] = None,
    max_tokens: int = 8192,
) -> str:
    """Call Gemini to transcribe a YouTube video by URL and return text."""
    client = genai.Client(api_key=api_key)

    prompt_text = prompt or DEFAULT_PROMPT

    response = client.models.generate_content(
        model=model,
        contents=types.Content(
            parts=[
                types.Part(text=prompt_text),
                types.Part(file_data=types.FileData(file_uri=url)),
            ]
        ),
        config=types.GenerateContentConfig(
            max_output_tokens=max_tokens,
            temperature=0.2,
        ),
    )

    # response.text usually carries the best-effort stitched output
    return response.text or ""


def main():
    parser = argparse.ArgumentParser(description="Transcribe a YouTube video using Gemini")
    parser.add_argument("--url", required=True, help="YouTube URL to transcribe")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Gemini model (default: {DEFAULT_MODEL})")
    parser.add_argument(
        "--prompt",
        default=None,
        help="Optional custom prompt to control transcription style/output",
    )
    parser.add_argument(
        "--max_tokens",
        type=int,
        default=12000,
        help="Max output tokens to request from the model (default: 12000)",
    )
    parser.add_argument(
        "--out",
        default=None,
        help="Optional path to write transcript output to a file",
    )

    args = parser.parse_args()

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(1)

    try:
        transcript = transcribe_youtube(
            args.url,
            api_key=api_key,
            model=args.model,
            prompt=args.prompt,
            max_tokens=args.max_tokens,
        )
    except Exception as e:
        print(f"Failed to transcribe: {e}", file=sys.stderr)
        sys.exit(2)

    if not transcript.strip():
        print("No transcript text returned.", file=sys.stderr)
        sys.exit(3)

    if args.out:
        try:
            with open(args.out, "w", encoding="utf-8") as f:
                f.write(transcript)
        except Exception as e:
            print(f"Failed to write output file: {e}", file=sys.stderr)
            sys.exit(4)
    else:
        print(transcript)


if __name__ == "__main__":
    main()
