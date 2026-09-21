# Chapter conventions

These are the conventions established by `chapter/velocity.tex` (Ch. 1) and
`chapter/acceleration.tex` (Ch. 2). Read the most recent chapter's source
before writing a new one; it is the ground truth if anything here drifts.

## Contents
1. Chapter skeleton (order of parts)
2. The boxed environments and when to use each
3. The two-perspective (Elementary / Calculus) convention
4. Prose and physics style
5. Figures and tables
6. Exercises and answers
7. LaTeX gotchas seen so far

---

## 1. Chapter skeleton

```
\chapter{Title}
[In this chapter]  tcolorbox: 8-10 "you should be able to" bullets
[How to read this chapter: two perspectives]  (copy from acceleration.tex)
\section ... narrative sections following the handout's arc (5-8 sections)
\section{Summary}
   \subsection*{Key ideas}      bullets, bold keyword first
   \subsection*{Key equations}  booktabs table, Elementary | Calculus columns
   \subsection*{Key terms}      \textperiodcentered-separated list
\section{Exercises}             grouped by \subsection*, ~40-55 items, star = harder
   ... last group is always "Hands-on"
\section*{Answers to Check Your Understanding}
\section*{Answers to Selected Exercises}
\section*{Sources and Further Reading}
```

Set `\setcounter{chapter}{N-1}` before `\chapter` so numbering is N.x.
Update the running header text in the preamble (`CHAPTERTITLE`).

## 2. Boxed environments

| Environment | Use for | Syntax |
|---|---|---|
| `example` | Worked Example, numbered N.k | `\begin{example}{Title}{label}` ... `\qed` ... `\end{example}`; refer with `Worked Example~\ref{ex:label}` |
| `definition` | formal definition of a term | `\begin{definition}{Term}{label}`; refer with `Definition~\ref{def:label}` |
| `keyidea` | a result to remember | `\begin{keyidea}[Title]` |
| `modelnote` | modelling caveats, history, asides | `\begin{modelnote}[Title]` |
| `twoviews` | one concept, Elementary then Calculus | `\begin{twoviews}{concept name}` containing `\elem ...` and `\calc ...` |
| `checkbox` | Check Your Understanding, auto-numbered N.k | `\begin{checkbox}` ... ; answers go in the back section keyed by number |

Roughly per chapter: 12-15 worked examples, 4-6 definitions, 4-6 key ideas,
4-6 modeling notes, 4-6 two-views boxes, 6-8 check boxes. Every check box
needs an answer at the back; count them in order to key the answers.

## 3. Two-perspective convention

The user asked (2026-09-12) that *each concept and each worked example* be
explained from two labelled perspectives so students see both:

- `\elem` starts an **Elementary** paragraph: ratios, proportional
  reasoning, averages, tables of first/second differences, areas of
  rectangles/triangles/trapezia, symmetry arguments. This is Galileo's and
  Hewitt's route, and it must be complete on its own.
- `\calc` starts a **Calculus** paragraph: derivatives, integrals,
  differential equations, chain rule, setting a derivative to zero for a
  maximum, and checks by differentiation. It must reach the same result and
  say so.

Inline tags `\elemtag` / `\calctag` mark short asides inside prose, key-idea
boxes, summary bullets, and answers. `\elemsub{pictures}` etc. labels
sub-variants of the elementary route. The Key Equations table has an
Elementary column and a Calculus column.

Why both: the two routes cross-check each other, and students who have not
met integration can still follow the whole chapter on the Elementary route.
When a topic has no meaningful calculus content (a drawing, a unit
conversion), a single `\solution` is fine, but note the calculus reading
in a sentence if there is one.

## 4. Prose and physics style

- Original prose. The AoPS handouts are copyrighted: follow their arc and
  ideas, rewrite everything, use new numbers in examples where possible,
  omit their photos. Cite the handout's historical sources directly.
- Textbook depth: longer and more thorough than the handout (Ch. 1 was
  26 pp, Ch. 2 is 37 pp). Add related material from Hewitt's matching
  chapter (definitions, check-point questions, tables) and cite it.
- British/Commonwealth spelling as in the earlier chapters (metre, modelling).
- Sign conventions stated explicitly (e.g. $y$ up, so $v_y<0$ when falling;
  $g>0$). Write vector components with subscripts ($v_x$, $a_y$).
- siunitx everywhere: `\SI{9.8}{\metre\per\second\squared}`,
  `\si{\kilo\metre\per\hour\per\second}`. `\mile` is declared in the
  preamble. Never put fractions inside `\SI{}` (use `$\tfrac13\,\si{\second}$`).
- Every worked example ends with a sanity check or an interpretive sentence,
  then `\qed`.
- Refer to Chapter 1 ideas (dot diagrams, average speed, sanity checks,
  uncertainty, models) rather than re-deriving them.
- Hewitt is the fact reference. Cross-check every number and definition
  against `book/hewitt-conceptual-physics-12e.txt`; where Hewitt rounds
  ($g \approx 10$) say so and use the precise value.

## 5. Figures and tables

- TikZ/pgfplots only, drawn inline, `[htb]`, `\caption` with a full sentence
  that says what to notice, `\label{fig:...}`.
- pgfplots: `width=11cm,height=7cm` for single plots, two side-by-side at
  `7.2cm` using `name=` and `at={(vt.right of south east)}`. Colours: teal
  for curves, `red!70!black` for annotation lines, `gray!25` grid.
- Motion/dot diagrams: dots `circle (2.2pt)`, arrows `[->,>=Stealth,thick,teal]`.
- Tables: booktabs, `\renewcommand{\arraystretch}{1.2}`, `\small` if wide,
  caption above, `\label{tab:...}`. Rows containing `\dfrac` or `\int` need
  `\arraystretch` of about 2.4 or `\\[6pt]`.
- Typical count: 5-7 figures, 2-4 tables per chapter.

## 6. Exercises and answers

- `\begin{enumerate}[label=\textbf{\thechapter.\arabic*},series=exercises,leftmargin=*]`
  for the first group, `resume=exercises` after. Numbering runs through
  the whole chapter.
- Groups mirror the section order; the final group is "Hands-on"
  (measure something with a phone, build the experiment, write to a friend).
- Mark harder ones `$\star$`. Give `\label{ex:...}` to exercises referenced
  from the text.
- Answers section: `\begin{description}[leftmargin=2.6em,itemsep=3pt,style=sameline]`
  with `\item[N.k]`. Answer most numeric exercises; for hands-on give typical
  ranges. Show both routes with `\elemtag`/`\calctag` where it helps.
- Check Your Understanding answers: `\begin{description}[leftmargin=2em,itemsep=2pt]`.

## 7. LaTeX gotchas seen so far

- `\newtcolorbox{...}[1][Title]{ title={#1}, ...}`: brace `{#1}` or a comma
  in a box title breaks pgfkeys.
- Long inline math in `description` items overflows the margin; move it
  to `\[ \]` or `align*`.
- `\url{}` (hyperref) for web addresses, not `\texttt{}`.
- Inside `\foreach`, prefer `\coordinate (P) at ($ (A)!\s!(B) $)` and calc
  library arithmetic over `let \p1 = ...`, which failed once.
- Node names built from `\foreach` variables caused a `\endcsname` error;
  avoid naming nodes inside loops.
- Tectonic downloads packages on first use and needs network; ~1-2 min.
- In `checkbox`, keep `coltitle=white`: with `enhanced` boxes the title bar
  is filled with `colframe`, so a `coltitle` equal to the frame colour makes
  the title invisible (bug found 2026-09-13, fixed in both chapters).
- `\foreach \X/\Y in {...}` *inside* a pgfplots `axis` with `(axis cs:\X,\Y)`
  fails with "Undefined control sequence" (hit 2026-09-20 drawing projection
  guide lines). Generate the `\draw` lines explicitly instead; a `\foreach`
  in a plain `tikzpicture` is fine.
- Labels that sit on top of a curve: add `fill=white,inner sep=1.5pt` to the
  node rather than hunting for a free spot. Used throughout Ch. 3's figures.
- A `\label` placed on a `modelnote`/`keyidea` (no counter) silently latches
  onto the last stepped counter and produces a wrong `\ref`. Refer to such
  boxes in words ("the Modeling Note below").
- A wide three-column Key Equations table fits at `\small` once
  `\setlength{\tabcolsep}{4pt}` is added and the longest cell in each column
  is shortened; check which *row* sets each column's width before trimming.
- The `In this chapter` tcolorbox is not `breakable` by default. Growing it
  past about ten bullets overflows the page (`Overfull \\vbox ... while
  \\output is active`); add `breakable` to its option list.
- Class transcripts (`chapter/chapterN/*.pdf`) are a second source alongside
  the handout, and they cover different ground: Lesson 1 added coordinate
  systems and video measurement, Lesson 2 added the lift, the sign trap, and
  the equivalence principle. Extract with `scripts/extract_pdf.py`, then pull
  the instructor's lines with
  `awk '/^<instructor> 2026/{getline; print}'`; the maths renders as detached
  fragments, so recover numbers by grepping the raw page ranges.
- Hardcoded cross-chapter references ("Definition 2.2") go stale as soon as a
  chapter gains a box. After editing an earlier chapter, grep the later ones
  for `Definition N\\.`, `Worked Example N\\.`, `Figure N\\.`, `Table N\\.` and
  check each against the rebuilt PDF.
- Aim for zero Overfull boxes wider than ~2pt; Underfull vbox warnings from
  breakable boxes are harmless.
