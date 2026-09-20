#!/usr/bin/env python3
"""Report which PDF pages contain given strings, e.g. figure or table captions.

Usage:
    python3 find_pages.py <chapter.pdf> "Figure 2.1" "Table 2.2" "Key equations"

Useful after build.sh to decide which rendered pages to look at.
"""
import sys
import unicodedata
import pymupdf

if len(sys.argv) < 3:
    sys.exit(__doc__)
pdf, needles = sys.argv[1], sys.argv[2:]
for i, page in enumerate(pymupdf.open(pdf)):
    # NFKC folds ligatures (ﬀ, ﬁ) so "different" matches "diﬀerent".
    text = unicodedata.normalize("NFKC", page.get_text())
    hits = [n for n in needles if n in text]
    if hits:
        print(i + 1, hits)
