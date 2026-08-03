#!/usr/bin/env python3
"""Generate a PNG image from an English image-generation prompt via the Google Gemini API."""
import argparse
import os
import sys
from pathlib import Path

# Re-verify against current Gemini API docs before relying on this — the
# API surface moves fast (imagen-4.0-generate-001, an earlier choice for
# this constant, was found deprecated with a 2026-08-17 shutdown date
# during implementation). gemini-3.1-flash-image is the current
# recommended general-purpose image model as of 2026-08, but confirm that
# still holds before trusting it blindly.
DEFAULT_MODEL = "gemini-3.1-flash-image"


def generate_image_bytes(prompt_text: str, model: str = DEFAULT_MODEL) -> bytes:
    """Call the Gemini API and return the generated image's raw bytes.

    Raises RuntimeError with a clear, user-facing message on any failure:
    google-genai not installed, no API key configured, an SDK/API error
    (auth, quota, etc.), or a response with no image (commonly a
    safety-filter rejection).
    """
    if not prompt_text.strip():
        raise RuntimeError("prompt file is empty — nothing to send to Gemini")

    if not (os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")):
        raise RuntimeError(
            "no GEMINI_API_KEY or GOOGLE_API_KEY environment variable set — "
            "image auto-generation requires one of these"
        )

    try:
        from google import genai
        from google.genai import types
    except ImportError as exc:
        raise RuntimeError(
            "google-genai is not installed — run `pip install google-genai` "
            "to use image auto-generation, or answer no to that question in Step 1"
        ) from exc

    client = genai.Client()  # auto-detects the key from the env vars above
    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt_text,
            config=types.GenerateContentConfig(response_modalities=["IMAGE"]),
        )
    except Exception as exc:  # deliberately broad: wrap any SDK error into one clear message
        raise RuntimeError(f"Gemini image generation failed: {exc}") from exc

    for part in getattr(response, "parts", None) or []:
        if getattr(part, "inline_data", None):
            return part.inline_data.data

    raise RuntimeError(
        "Gemini returned no image (commonly a safety-filter rejection) — "
        "check the prompt for content that may need adjusting"
    )


def generate_image(prompt_txt_path: Path, output_png_path: Path, model: str = DEFAULT_MODEL) -> None:
    try:
        prompt_text = Path(prompt_txt_path).read_text(encoding="utf-8")
    except OSError as exc:
        raise RuntimeError(f"couldn't read prompt file {prompt_txt_path}: {exc}") from exc

    image_bytes = generate_image_bytes(prompt_text, model=model)

    try:
        Path(output_png_path).write_bytes(image_bytes)
    except OSError as exc:
        raise RuntimeError(f"couldn't write output file {output_png_path}: {exc}") from exc


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prompt_txt", type=Path)
    parser.add_argument("output_png", type=Path)
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Gemini image model name")
    args = parser.parse_args()
    try:
        generate_image(args.prompt_txt, args.output_png, model=args.model)
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
    print(f"wrote {args.output_png}")


if __name__ == "__main__":
    main()
