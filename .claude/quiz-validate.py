#!/usr/bin/env python3
"""
quiz-validate.py — anti-cheat + integrity validator for quiz .md files.

Reusable tool referenced by /quiz-gen. Run after generating a quiz instead of
writing an ad-hoc check:

    python ~/.claude/commands/templates/quiz-validate.py <quiz.md>

It parses the quiz format (YAML frontmatter tags; `## tag`; `Q:`; `- options`;
`<!-- base64(ans:N) -->`; `> explanation`) and reports PASS/FAIL on:

  - Parse integrity : every question has >=2 options, a decoded answer, an
                      explanation, and a tag declared in the frontmatter.
  - Answer spread   : correct letters ~evenly across A-D (each ~N/4, ±2) and the
                      longest run of the same letter is <= 2.
  - Length giveaway : NO question where the correct option is longer than EVERY
                      distractor by >= 8 chars (the perceptible margin). Target 0.
                      (Being longest by 1-2 chars is NOT exploitable, so it is
                      reported as INFO only, never a failure.)
  - Length bias     : |mean(len correct) - mean(len distractors)| <= 2.0 chars.
  - Style parity    : no question where a parenthesis/inline-formula/hedge marks
                      the correct option ALONE (or marks every option but it).
  - Numeric options : INFO only. Flags questions whose options are mostly bare
                      numbers, i.e. "compute this value" questions. /quiz-gen
                      requires math questions to be SYMBOLIC (expressions in
                      literal parameters), with numbers reserved for empirical
                      magnitudes the course quotes. Not a gate, because quoting a
                      magnitude is legitimate -- but every hit deserves a look.

Exit code 0 if all gates pass, 1 otherwise. Stdlib only.
"""
import sys, re, base64, statistics as st

GATE_MARGIN = 8        # chars: correct longer than every distractor => giveaway
GATE_BIAS   = 2.0      # chars: tolerated mean(correct)-mean(distractor) gap
HEDGES = ("necessariamente", "sempre", "nunca", "em geral", "apenas", "somente")

def parse(md):
    fm = re.match(r'^---\s*\n([\s\S]*?)\n---', md)
    tags, body = set(), md
    if fm:
        for line in fm.group(1).split("\n"):
            m = re.match(r'^\s+(\S+):\s*"', line)
            if m: tags.add(m.group(1))
        body = md[fm.end():]
    lines = body.split("\n"); i = 0; qs = []; cur = ""; stem = None
    while i < len(lines):
        l = lines[i]
        m = re.match(r'^##\s+(\S+)', l)
        if m: cur = m.group(1); stem = None; i += 1; continue
        if l.startswith("P:"):
            s = l[2:].strip(); i += 1
            while i < len(lines) and not re.match(r'^[QP]:', lines[i]) \
                    and not lines[i].startswith("##"):
                if lines[i].strip(): s += " " + lines[i].strip()
                i += 1
            stem = s or None; continue
        if l.startswith("Q: "):
            qtext = l[3:]
            i += 1
            while i < len(lines) and not lines[i].startswith("- ") \
                    and not lines[i].startswith("<!--") and lines[i].strip():
                i += 1
            opts = []
            while i < len(lines) and lines[i].startswith("- "):
                opts.append(lines[i][2:].strip()); i += 1
            ans = None
            if i < len(lines) and lines[i].startswith("<!--"):
                b = re.search(r'<!--\s*(\S+)\s*-->', lines[i])
                if b:
                    try:
                        d = base64.b64decode(b.group(1)).decode()
                        mm = re.search(r'ans:(\d+)', d)
                        if mm: ans = int(mm.group(1))
                    except Exception: pass
                i += 1
            expl = 0
            while i < len(lines) and lines[i].startswith(">"):
                expl += 1; i += 1
            qs.append({"tag": cur, "opts": opts, "ans": ans, "expl": expl,
                       "q": qtext, "stem": stem})
            continue
        i += 1
    return tags, qs

STOP = {"and", "or", "with", "the", "of", "for", "and", "que", "com", "para",
        "and", "des", "das", "dos", "aos"}
GREEK_RE = re.compile(r"\\(alpha|beta|gamma|delta|epsilon|varepsilon|theta|lambda|mu|nu|rho|sigma|tau|phi|omega|pi|psi|xi|zeta|eta|kappa)")
NUM_RE = re.compile(r"\d")
# letra matematica: comando LaTeX (\alpha) ou letra romana isolada usada como simbolo
SYM_RE = re.compile(r"\\[A-Za-z]+|[A-Za-z]{3,}")


def purely_numeric(opt):
    """True se a opcao e essencialmente um numero: tem digito e nenhuma palavra
    nem comando LaTeX que carregue significado. Captura "8,00", "$k^* = 8$",
    "0,0333" e deixa passar "rises with alpha" ou "$(s/(n+delta))^{1/(1-alpha)}$"."""
    body = re.sub(r"\$[^$]*\$", lambda m: m.group(0), opt)
    if not NUM_RE.search(body):
        return False
    if GREEK_RE.search(body):
        return False   # tem parametro literal -> simbolica, nao numerica
    # remove simbolos matematicos de uma letra e pontuacao, ve o que sobra de texto
    resto = re.sub(r"\\[A-Za-z]+", " ", body)
    resto = re.sub(r"[^A-Za-z]+", " ", resto)
    palavras = [w for w in resto.split() if len(w) >= 3 and w.lower() not in STOP]
    return len(palavras) == 0


def marked(opt):
    """Does this option carry a distinguishing style marker?"""
    return ("(" in opt) or ("$" in opt) or any(h in opt.lower() for h in HEDGES)

def main(path):
    md = open(path, encoding="utf-8").read()
    tags, qs = parse(md)
    n = len(qs)
    if n == 0:
        print("FAIL  no questions parsed — check the format"); return 1
    fails, infos = [], []

    # 1. Parse integrity
    bad = [k+1 for k, q in enumerate(qs)
           if q["ans"] is None or len(q["opts"]) < 2 or q["expl"] == 0
           or (tags and q["tag"] not in tags)]
    if bad: fails.append(f"parse integrity: questions {bad} miss answer/options/explanation/known-tag")

    # 2. Answer spread + runs
    from collections import Counter
    dist = Counter(q["ans"] for q in qs if q["ans"] is not None)
    letters = "ABCDE"; exp = n / 4
    spread = {letters[k]: dist.get(k, 0) for k in range(4)}
    if any(abs(v - exp) > 2 for v in spread.values()):
        fails.append(f"answer spread uneven: {spread} (each should be ~{exp:.0f} ±2)")
    run = mx = 0; prev = None
    for q in qs:
        run = run + 1 if q["ans"] == prev else 1; prev = q["ans"]; mx = max(mx, run)
    if mx >= 3: fails.append(f"answer run too long: {mx} same letter in a row (max 2)")

    # --- self-containment gates ------------------------------------------
    # A student sees one question, its options, and the P: stem active in the SAME
    # section. A P: does not survive a "## tag" boundary, so anything referring back
    # across one is invisible to them.
    DANGLING = re.compile(
        r"(economy above|the same economy|throughout this quiz"
        r"|\b(?:the|that|this)\s+\w+\s+above\b"
        r"|\bas before\b|\bthe previous (?:question|item)\b"
        r"|\bthat economy\b|\bthis discount factor\b)", re.I)
    dang = [i for i, q in enumerate(qs, 1)
            if not q.get("stem") and DANGLING.search(q.get("q", ""))]
    if dang:
        fails.append(f"dangling context: questions {dang} refer to a setup they do not "
                     f"carry, with no P: active in their section - restate the givens")
    secref = [i for i, q in enumerate(qs, 1)
              if re.search(r"§\s*\d+\.\d", q.get("q", ""))]
    if secref:
        fails.append(f"bare section reference in stem: questions {secref} quiz the book's "
                     f"numbering, not its substance - state it, move the ref to > Ref:")

    # 3 & 4. Length giveaway + bias  (only questions with a decoded answer)
    good = [q for q in qs if q["ans"] is not None and len(q["opts"]) >= 2]
    perceptible, uniq_longest = [], 0
    cor_len, dis_len = [], []
    for k, q in enumerate(good):
        L = [len(o) for o in q["opts"]]; c = q["ans"]
        others = L[:c] + L[c+1:]
        cor_len.append(L[c]); dis_len += others
        if L[c] - max(others) >= GATE_MARGIN: perceptible.append(k+1)
        if L[c] == max(L) and L.count(max(L)) == 1: uniq_longest += 1
    if perceptible:
        fails.append(f"length giveaway: correct is >= {GATE_MARGIN} chars longer than every "
                     f"distractor in questions {perceptible} (target 0)")
    bias = st.mean(cor_len) - st.mean(dis_len)
    if abs(bias) > GATE_BIAS:
        fails.append(f"length bias: mean(correct)-mean(distractors) = {bias:+.1f} chars "
                     f"(allowed ±{GATE_BIAS})")
    infos.append(f"correct uniquely-longest (by any margin, informational): {uniq_longest}/{len(good)}")

    # 4b. Numeric-option questions (INFO): /quiz-gen wants symbolic math
    numq = []
    for k, q in enumerate(good):
        nnum = sum(1 for o in q["opts"] if purely_numeric(o))
        if nnum >= max(2, len(q["opts"]) - 1):
            numq.append(k + 1)
    if numq:
        infos.append(f"numeric options: questions {numq} choose between bare numbers. "
                     f"/quiz-gen asks for SYMBOLIC math (expressions in literal "
                     f"parameters); numbers are only for empirical magnitudes the "
                     f"course quotes. Check each one.")

    # 5. Style parity (marker on correct alone, or on all-but-correct)
    only_corr, only_not_corr = [], []
    for k, q in enumerate(good):
        mk = [marked(o) for o in q["opts"]]; c = q["ans"]
        if mk[c] and sum(mk) == 1: only_corr.append(k+1)
        if (not mk[c]) and sum(mk) == len(mk) - 1: only_not_corr.append(k+1)
    if only_corr:
        fails.append(f"style parity: marker (paren/formula/hedge) on the correct option ALONE "
                     f"in questions {only_corr} (target 0)")
    if only_not_corr:
        fails.append(f"style parity: correct is the ONLY option WITHOUT a marker "
                     f"in questions {only_not_corr} (target 0)")

    # Report
    print(f"Quiz: {path}")
    print(f"Questions: {n} | tags: {len(tags)} | answer spread: {spread} | max run: {mx}")
    print(f"Length: mean(correct)={st.mean(cor_len):.1f} mean(distractors)={st.mean(dis_len):.1f} "
          f"bias={bias:+.1f} | perceptible(>= {GATE_MARGIN}): {len(perceptible)}")
    for s in infos: print("INFO  " + s)
    if not fails:
        print("PASS  all gates satisfied"); return 0
    for s in fails: print("FAIL  " + s)
    return 1

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python quiz-validate.py <quiz.md>"); sys.exit(2)
    sys.exit(main(sys.argv[1]))
