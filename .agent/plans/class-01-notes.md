# Plan: Class 1 notes + three companions

**Ask (2026-10-09):** notes for class 1 with interactive companions. Answers: Markdown in `Aula/class-01/`; companions A, B, C as proposed; local + published Artifacts.

**Topic:** Class 1 of the draft plan (`Map/class-plan.md`): potential outcomes, Neyman–Rubin, selection bias. `Aula/` has no slides yet, so the notes follow the draft plan and MHE Ch. 1–2 (printed pp. 3–18), read in this session.

## Deliverables

| File | Content |
|---|---|
| `Aula/class-01/class-01.ipynb` | Notebook (user switched from Markdown mid-task, kept HTML companions; Python kernel because R is not installed). Lecture notes in Markdown cells + runnable code: FAQs, potential outcomes, switching eq. (2.1.1), ATE/ATT/ATU, naive = ATT + SB, ATE version, random assignment, SUTVA, STAR tables, regression form (2.3.1–2.3.2), worked 8-person table, R simulation, pitfalls, practice pointers, links to companions |
| `Aula/class-01/companion-selection-bias.html` | A: Selection Bias Decomposer (closed form) |
| `Aula/class-01/companion-sample-size.html` | B: Bigger Sample, Same Bias (seeded simulation) |
| `Aula/class-01/companion-eight-person-table.html` | C: the 8-person table, exact enumeration |

## Shared DGP (A, B), declared on the pages as illustrative and not from MHE

- $Y_0 \sim N(\mu_0, \sigma^2)$, $\mu_0 = 5$; $z = (Y_0-\mu_0)/\sigma$
- $Y_1 = Y_0 + \tau + \gamma (Y_0 - \mu_0)$
- $D = 1\{\lambda z + \sqrt{1-\lambda^2}\,\nu > c\}$, $\nu \sim N(0,1)$, $c = \Phi^{-1}(1-\pi)$
- $E[z\mid D=1] = \lambda\,\phi(c)/\pi$, $E[z\mid D=0] = -\lambda\,\phi(c)/(1-\pi)$
- ATT $= \tau + \gamma\sigma E[z\mid D=1]$, ATU $= \tau + \gamma\sigma E[z\mid D=0]$, ATE $= \tau$
- SB $= \sigma\lambda\phi(c)/(\pi(1-\pi))$; naive = ATT + SB = ATE + SB + $(1-\pi)$(ATT − ATU)
- Density $f(y\mid D=1) = \phi(z)\,[1-\Phi((c-\lambda z)/\sqrt{1-\lambda^2})]/(\sigma\pi)$; when $|\lambda|=1$ this is a truncated normal, handled explicitly

## Steps

1. Verify the closed forms against a large Monte Carlo run in Python (scratchpad).
2. Write the notebook; its cells compute the 8-person numbers and the DGP checks.
3. Build A, B, C (load the artifact-design skill first; inline SVG; theme tokens; no CDN).
4. Verify: three control vectors per page against Python; sweeps; landmarks reachable; no NaN (headless check if a browser is available, otherwise a JS-logic check under node).
5. Publish the three Artifacts and link them from the notes.

R is not installed, so the notebook runs on the Python kernel; an R equivalent of the core simulation goes in a non-executed Markdown cell. Execute the notebook end to end with nbconvert and confirm the printed numbers match the closed forms.
