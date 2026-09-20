#!/usr/bin/env python3
"""Extract the text of a PDF (a handout, or a reference book) with page markers.

Usage:
    python3 extract_pdf.py <input.pdf> [output.txt]

Writes "===== PAGE n =====" before each page so that grep hits can be
located in the original PDF. If no output path is given, prints to stdout.
Requires pypdf (pip install --user pypdf) or falls back to pymupdf.
"""
import sys


def extract(path):
    try:
        import pypdf
        reader = pypdf.PdfReader(path)
        return [(p.extract_text() or "") for p in reader.pages]
    except ImportError:
        import pymupdf
        return [p.get_text() for p in pymupdf.open(path)]


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    pages = extract(sys.argv[1])
    chunks = [f"\n===== PAGE {i + 1} =====\n{t}" for i, t in enumerate(pages)]
    text = "".join(chunks)
    if len(sys.argv) > 2:
        with open(sys.argv[2], "w") as fh:
            fh.write(text)
        print(f"{len(pages)} pages -> {sys.argv[2]} ({len(text)} chars)")
    else:
        print(text)


if __name__ == "__main__":
    main()
