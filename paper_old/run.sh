#!/usr/bin/env bash
# Compile main.tex into main.pdf (pdflatex -> bibtex -> pdflatex x2).
#
#   ./run.sh          build main.pdf
#   ./run.sh clean    remove LaTeX intermediate files
#
# Requires TeX Live (pdflatex + bibtex).
set -euo pipefail

cd "$(dirname "$0")"

JOB=main

if [[ "${1:-}" == clean ]]; then
  rm -f "$JOB".{aux,bbl,blg,log,out,fls,fdb_latexmk,synctex.gz,toc}
  echo "Cleaned intermediate files."
  exit 0
fi

for cmd in pdflatex bibtex; do
  command -v "$cmd" >/dev/null || { echo "$cmd not found: install TeX Live." >&2; exit 1; }
done

# Define \aclmode with \def (not main.tex's \providecommand) so the review-mode
# check in main.tex matches and camera_ready.tex is not required.
TEX="\\def\\aclmode{review}\\input{$JOB.tex}"
PDFLATEX=(pdflatex -interaction=nonstopmode -halt-on-error -jobname="$JOB" "$TEX")

"${PDFLATEX[@]}" >/dev/null || { tail -n 30 "$JOB.log" >&2; exit 1; }
bibtex "$JOB"
"${PDFLATEX[@]}" >/dev/null || { tail -n 30 "$JOB.log" >&2; exit 1; }
"${PDFLATEX[@]}" >/dev/null || { tail -n 30 "$JOB.log" >&2; exit 1; }

echo "Built $JOB.pdf"
