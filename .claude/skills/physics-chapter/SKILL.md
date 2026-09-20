---
name: physics-chapter
description: Write an original LaTeX textbook chapter for the "Physics 1: Mechanics" book from an AoPS handout PDF (Handout_*.pdf), matching the established chapter style (tcolorbox worked examples, definitions, key ideas, modeling notes, two-perspective Elementary/Calculus explanations, TikZ figures, exercises with answers, Hewitt-checked facts) and compiling it to PDF with Tectonic. Use this whenever the user asks to write, draft, extend, or rebuild a chapter, "do the same as we did for velocity/acceleration", turn a handout into a chapter, or add sections/exercises/figures to an existing chapter in chapter/*.tex, even if they do not say "skill" or "LaTeX".
---

# Physics chapter writer

Turn an AoPS *Physics 1: Mechanics* handout into a full, original textbook
chapter in LaTeX, consistent with the chapters already in `chapter/`, and
deliver a compiled, visually checked PDF.

## What "like the earlier chapters" means

Two chapters exist and define the house style: `chapter/velocity.tex`
(Ch. 1) and `chapter/acceleration.tex` (Ch. 2, the current reference).
The reader is a strong high-school or first-year student. Each chapter:

- follows the handout's narrative arc but is written from scratch, with
  new worked-example numbers, no handout photos, and roughly 1.5-3x the
  handout's depth (30-40 pages);
- explains every concept and solves every worked example from **two
  labelled perspectives**, Elementary and Calculus (see
  `references/conventions.md` §3), so students can cross-check the two;
- uses the fixed preamble in `assets/preamble.tex` and its environments:
  Worked Example, Definition, Key Idea, Modeling Note, Two Views, Check
  Your Understanding;
- cross-checks facts and definitions against Hewitt's *Conceptual Physics*
  12e, the designated reference, and cites it;
- ends with Summary (key ideas, key equations, key terms), grouped
  Exercises with a Hands-on group, answers, and Sources.

Read `references/conventions.md` before writing; it holds the skeleton,
environment syntax, style rules, and the LaTeX gotchas already hit.

## Workflow

1. **Extract the handout.** `python3 scripts/extract_pdf.py Handout_X.pdf
   <scratchpad>/x.txt` and read it all. Note the handout's sections,
   problems, exercises with answers, historical references, and which
   ideas from earlier chapters it leans on.

2. **Read the latest chapter source** (`chapter/acceleration.tex`, or
   whichever is newest) end to end. It is the live style guide; copy its
   patterns rather than inventing new ones. Note how the answers key to
   check-box numbers and how figures are drawn.

3. **Pull the matching Hewitt material.** The searchable extract is
   `book/hewitt-conceptual-physics-12e.txt` (page markers
   `===== PAGE n =====`). Grep the table of contents near the top for the
   relevant chapter and section titles, then read those sections
   (typically 200-400 lines). Collect: definitions, check-point questions
   with answers (adapt them), tables, and memorable examples. Where Hewitt
   rounds or stays qualitative, keep his facts and go deeper mathematically.

4. **Outline before writing.** Map handout sections to chapter sections;
   decide the worked examples (12-15), which get Two Views boxes (4-6),
   figures (5-7), tables (2-4), check boxes (6-8), and exercise groups.
   Choose fresh numbers for examples and verify every result by
   calculation before it goes on the page (a tiny Python check is cheap).

5. **Write `chapter/<name>.tex`.** Start from `assets/preamble.tex`
   (replace `CHAPTERTITLE`, set `\setcounter{chapter}{N-1}`), then the
   body following the skeleton in `references/conventions.md`. For each
   concept: `twoviews` box or `\elem`/`\calc` paragraphs. For each worked
   example: both routes, ending with a sanity check and `\qed`. Write the
   answers as you write the exercises so nothing is left unanswered.

6. **Compile and inspect.** `bash scripts/build.sh chapter/<name>.tex
   <scratchpad>/render` compiles with Tectonic (downloading it if needed),
   prints errors and Overfull boxes, and renders pages to PNG. Fix every
   error and every Overfull box over ~2pt (tables: `\small` or shorter
   headers; long inline math in answers: move to display math). Then use
   `scripts/find_pages.py` to locate figure/table pages and *look at them*
   with the Read tool: check that figure geometry is right, labels do not
   collide, and boxes render. Iterate until clean.

7. **Report.** Tell the user the file paths, page count, what the chapter
   covers beyond the handout, any assumption made (e.g. calculus
   prerequisites), and anything left out. Update project memory if a new
   convention was established.

## Judgement calls worth knowing

- The handouts are copyrighted teaching material; the chapter must be
  original prose that teaches the same ideas. Never paste handout
  sentences or reuse their exact problem numbers wholesale.
- Historical claims (Galileo, Oresme, Drake's music hypothesis, dates)
  should come from Hewitt or well-known sources you can name in Sources;
  hedge where historians disagree.
- The Elementary route must be self-sufficient. If it needs the calculus
  result to work, restructure so the elementary argument stands alone
  (areas, averages, differences, proportional scaling).
- Keep g = 9.8 m/s^2 unless the point is arithmetic transparency, then say
  Hewitt rounds to 10 and why.
- Do not ask the user which sections to include; the handout arc plus
  Hewitt's matching chapter is the scope. Do ask if the requested chapter
  has no handout or if it should replace an existing file.
