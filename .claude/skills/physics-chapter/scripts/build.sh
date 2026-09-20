#!/usr/bin/env bash
# Compile a chapter with Tectonic and render its pages for visual checking.
#
# Usage:  build.sh <chapter.tex> [render_dir]
#
# - Finds `tectonic` on PATH, in the scratchpad, or downloads the
#   aarch64-apple-darwin 0.15.0 release into $TECTONIC_DIR (default: the
#   directory named by $CLAUDE_SCRATCHPAD, else /tmp/tectonic-bin).
# - Compiles (Tectonic reruns automatically for cross-references).
# - Prints only the lines that matter: errors, Overfull boxes, page count.
# - If pymupdf is importable, renders every page to <render_dir>/pNN.png at
#   70 dpi so the pages can be inspected with an image viewer or Read tool.
set -u
TEX="${1:?usage: build.sh <chapter.tex> [render_dir]}"
RENDER_DIR="${2:-}"
TEXDIR="$(cd "$(dirname "$TEX")" && pwd)"
TEXBASE="$(basename "$TEX" .tex)"

find_tectonic() {
  if command -v tectonic >/dev/null 2>&1; then command -v tectonic; return; fi
  local dir="${TECTONIC_DIR:-${CLAUDE_SCRATCHPAD:-/tmp/tectonic-bin}}"
  if [ -x "$dir/tectonic" ]; then echo "$dir/tectonic"; return; fi
  mkdir -p "$dir"
  echo "downloading tectonic into $dir" >&2
  curl -sL -o "$dir/tectonic.tar.gz" \
    https://github.com/tectonic-typesetting/tectonic/releases/download/tectonic%400.15.0/tectonic-0.15.0-aarch64-apple-darwin.tar.gz \
    && tar xzf "$dir/tectonic.tar.gz" -C "$dir" && chmod +x "$dir/tectonic"
  echo "$dir/tectonic"
}

TECTONIC="$(find_tectonic)"
[ -x "$TECTONIC" ] || { echo "tectonic not available" >&2; exit 2; }

cd "$TEXDIR"
"$TECTONIC" "$TEXBASE.tex" 2>&1 | grep -vE '^note: downloading' \
  | grep -iE 'error|overfull|Writing|halted' || true

if [ -f "$TEXBASE.pdf" ]; then
  python3 - "$TEXBASE.pdf" "$RENDER_DIR" <<'PY'
import sys
pdf, out = sys.argv[1], sys.argv[2]
try:
    import pymupdf
except ImportError:
    print("pages: (install pymupdf to count/render: python3 -m pip install --user pymupdf)")
    sys.exit(0)
doc = pymupdf.open(pdf)
print(f"pages: {len(doc)}")
if out:
    import os
    os.makedirs(out, exist_ok=True)
    for i, page in enumerate(doc):
        page.get_pixmap(dpi=70).save(os.path.join(out, f"p{i+1:02d}.png"))
    print(f"rendered {len(doc)} pages to {out}")
PY
fi
