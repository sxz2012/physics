#!/usr/bin/env python3
"""Grade one eval run directory: writes grading.json with text/passed/evidence.
Usage: python3 grade.py <iteration_dir>/<eval-name>/<run>   (run = with_skill|without_skill)
"""
import json, os, re, subprocess, sys
run = sys.argv[1].rstrip('/')
evaldir = os.path.dirname(run); name = os.path.basename(evaldir)
out = os.path.join(run, 'outputs')
res = []
def check(text, passed, evidence): res.append({"text": text, "passed": bool(passed), "evidence": str(evidence)})

def pages(pdf):
    try:
        import pymupdf; return len(pymupdf.open(pdf))
    except Exception as e: return -1

def compile_clean(tex):
    d, b = os.path.split(tex)
    p = subprocess.run(['/tmp/tectonic-bin/tectonic', b], cwd=d, capture_output=True, text=True)
    log = p.stderr + p.stdout
    errs = [l for l in log.splitlines() if l.startswith('error')]
    over = [l for l in log.splitlines() if 'Overfull' in l]
    big = [l for l in over if float(re.search(r'\(([\d.]+)pt', l).group(1)) > 5]
    return errs, over, big

def section_items(tex, start, end):
    i = tex.find(start); j = tex.find(end, i)
    return tex[i:j].count('\\item') if i >= 0 and j >= 0 else 0

if name == 'velocity-rewrite':
    tex_p = os.path.join(out, 'velocity-v2.tex'); pdf_p = os.path.join(out, 'velocity-v2.pdf')
    ok = os.path.exists(tex_p) and os.path.exists(pdf_p)
    check("velocity-v2.tex and velocity-v2.pdf both exist", ok, f"tex={os.path.exists(tex_p)} pdf={os.path.exists(pdf_p)}")
    tex = open(tex_p).read() if os.path.exists(tex_p) else ''
    n = pages(pdf_p) if os.path.exists(pdf_p) else 0
    check("PDF has 25-45 pages (textbook depth)", 25 <= n <= 45, f"{n} pages")
    if tex:
        errs, over, big = compile_clean(tex_p)
        check("Compiles with no TeX errors", not errs, errs[:3] or 'no errors')
        check("No Overfull box wider than 5pt", not big, big[:3] or f'{len(over)} small overfulls')
    check("Sets chapter number to 1 (\\setcounter{chapter}{0})", '\\setcounter{chapter}{0}' in tex, '')
    tv = tex.count('\\begin{twoviews}'); check("At least 3 Two Views boxes", tv >= 3, f"{tv} twoviews")
    e, c = tex.count('\\elem'), tex.count('\\calc'); check("At least 8 Elementary and 8 Calculus labelled passages", e >= 8 and c >= 8, f"elem={e} calc={c}")
    ex = tex.count('\\begin{example}'); check("At least 10 worked examples", ex >= 10, f"{ex}")
    both = len(re.findall(r'\\begin\{example\}.*?\\end\{example\}', tex, re.S))
    dual = sum(1 for m in re.findall(r'\\begin\{example\}.*?\\end\{example\}', tex, re.S) if '\\elem' in m and '\\calc' in m)
    check("At least half of worked examples carry both Elementary and Calculus routes", both and dual >= both/2, f"{dual}/{both}")
    fig = tex.count('\\begin{tikzpicture}'); check("At least 4 TikZ/pgfplots pictures", fig >= 4, f"{fig}")
    cb = tex.count('\\begin{checkbox}'); check("At least 5 Check Your Understanding boxes", cb >= 5, f"{cb}")
    for s in ['Key equations', 'Key terms', 'Hands-on', 'Answers to Selected Exercises', 'Answers to Check Your Understanding', 'Sources and Further Reading']:
        check(f"Has '{s}' section", s in tex, '')
    check("Cites Hewitt in Sources", 'Hewitt' in tex, '')
    nex = section_items(tex, '\\section{Exercises}', 'Answers to'); check("At least 30 exercises", nex >= 30, f"{nex} items")
    si = tex.count('\\SI{'); check("Uses siunitx (>=40 \\SI)", si >= 40, f"{si}")
    # originality: 10-word n-gram overlap with handout
    try:
        import pypdf
        h = ' '.join((p.extract_text() or '') for p in pypdf.PdfReader('/Users/xsz/projects/physic/Handout_Velocity.pdf').pages)
        def grams(t):
            w = re.findall(r"[a-z]+", t.lower()); return set(tuple(w[i:i+10]) for i in range(len(w)-9))
        prose = re.sub(r'\\[a-zA-Z]+(\[[^\]]*\])?(\{[^}]*\})?', ' ', tex)
        ov = grams(h) & grams(prose)
        check("Original prose: fewer than 5 ten-word phrases copied from handout", len(ov) < 5, f"{len(ov)} shared 10-grams")
    except Exception as ex_: check("Original prose check ran", False, repr(ex_))

elif name == 'add-graphs-section':
    tex_p = os.path.join(out, 'acceleration.tex'); pdf_p = os.path.join(out, 'acceleration.pdf')
    orig = open('/Users/xsz/projects/physic/chapter/acceleration.tex').read()
    tex = open(tex_p).read() if os.path.exists(tex_p) else ''
    check("acceleration.tex was modified and acceleration.pdf exists", tex != orig and os.path.exists(pdf_p), f"changed={tex!=orig} pdf={os.path.exists(pdf_p)}")
    n = pages(pdf_p) if os.path.exists(pdf_p) else 0
    check("PDF grew beyond the original 37 pages", n > 37, f"{n} pages")
    if tex:
        errs, over, big = compile_clean(tex_p)
        check("Compiles with no TeX errors", not errs, errs[:3] or 'no errors')
        check("No Overfull box wider than 5pt", not big, big[:3] or f'{len(over)} small overfulls')
    secs = [s for s in re.findall(r'\\section\{([^}]*)\}', tex) if re.search(r'[Gg]raph', s)]
    check("A new \\section about graphs exists", bool(secs), secs)
    dex = tex.count('\\begin{example}') - orig.count('\\begin{example}'); check("Exactly two worked examples added", dex == 2, f"+{dex}")
    dfig = tex.count('\\begin{tikzpicture}') - orig.count('\\begin{tikzpicture}'); check("At least one figure added", dfig >= 1, f"+{dfig}")
    dexr = section_items(tex, '\\section{Exercises}', 'Answers to') - section_items(orig, '\\section{Exercises}', 'Answers to')
    check("Four exercises added", dexr == 4, f"+{dexr}")
    dans = section_items(tex, 'Answers to Selected Exercises', 'Sources and') - section_items(orig, 'Answers to Selected Exercises', 'Sources and')
    check("Answers added for the new exercises", dans >= 3, f"+{dans} answer items")
    dlab = (tex.count('\\elem') + tex.count('\\calc') + tex.count('\\begin{twoviews}')) - (orig.count('\\elem') + orig.count('\\calc') + orig.count('\\begin{twoviews}'))
    check("New section uses Elementary/Calculus labels", dlab >= 4, f"+{dlab} labels")
    for s in ["Galileo's Problem", 'Sources and Further Reading', 'Hang time']:
        check(f"Original content preserved: '{s}'", s in tex, '')
    ans_new = tex.count('\\item[2.') - orig.count('\\item[2.')
    check("Exercise numbering continues the chapter series (new \\item[2.NN] answers)", ans_new >= 3, f"+{ans_new}")

json.dump({"expectations": res}, open(os.path.join(run, 'grading.json'), 'w'), indent=2)
print(name, os.path.basename(run), f"{sum(r['passed'] for r in res)}/{len(res)} passed")
for r in res: print(('  PASS ' if r['passed'] else '  FAIL '), r['text'], '|', r['evidence'])
