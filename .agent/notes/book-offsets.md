# Printed → PDF page offsets (measured 2026-10-19 from page-number lines; PDF page = printed + offset)

Use with `pdftotext -f <printed+offset> -l <...> -layout "Livros/<file>" -`. Spot-check one page before quoting; front-matter and chapter-opening pages can shift by 1.

| Abbrev. | File in `Livros/` | Offset |
|---|---|---|
| B | `Bolfarine, Sandoval - Introdução à Inferência Estatística (2010).pdf` | +6 |
| W | `Wooldridge J.M-Introductory econometrics. A modern approach-Cengage Learning (2016).pdf` (6e) | +24 |
| T | `Ruey S. Tsay - Analysis of Financial Time Series, Third Edition (...).pdf` | +27 |
| I | `James, Witten, Hastie, Tibshirani, Taylor - An Introduction to Statistical Learning with Applications in Python (2023).pdf` (ISLP) | varies by chapter: **+10 in Ch. 2**, +9 in Ch. 4, **+8 in Ch. 5 and Ch. 7** (found while writing the L01/L02 notes); always verify |
| G | `Edward Greenberg - Introduction to Bayesian Econometrics (2007, Cambridge University Press) - libgen.li.pdf` (1e) | +15 |
| AME | `Izbicki, Mendonça - Aprendizado de Máquina_ uma abordagem estatística (2020).pdf` | +18 |
| MHE | `Joshua D. Angrist, ... (2008).pdf` | +16 (from BOOKS.md) |
| MS | `Morettin, Singer - Estatística e Ciência de Dados (versão preliminar, abril 2021).pdf` | +10 in Apêndice B (p. 478 = PDF 488; measured 2026-10-31) |

Markdown conversions (`Livros/*.md`) exist for most books: grep them to find a section, then confirm the page in the PDF.
