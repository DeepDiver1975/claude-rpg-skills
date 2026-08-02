#!/usr/bin/env python3
"""Extract the AcroForm field catalog from a fillable CPR PDF into JSON."""
import json
import subprocess
import sys
from pathlib import Path


def extract_fields(pdf_path: Path) -> list[dict]:
    result = subprocess.run(
        ["pdftk", str(pdf_path), "dump_data_fields_utf8"],
        check=True, capture_output=True, text=True,
    )
    fields: list[dict] = []
    current: dict = {}
    for line in result.stdout.splitlines():
        if line == "---":
            if current:
                fields.append(current)
            current = {}
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        value = value.strip()
        if key == "FieldType":
            current["type"] = value
        elif key == "FieldName":
            current["name"] = value
        elif key == "FieldJustification":
            current["justification"] = value
    if current:
        fields.append(current)
    return fields


def main() -> None:
    if len(sys.argv) != 3:
        print("usage: extract_fields.py <input.pdf> <output.json>", file=sys.stderr)
        raise SystemExit(2)
    pdf_path, out_path = Path(sys.argv[1]), Path(sys.argv[2])
    fields = extract_fields(pdf_path)
    out_path.write_text(
        json.dumps(fields, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"wrote {len(fields)} fields to {out_path}")


if __name__ == "__main__":
    main()
