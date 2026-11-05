# Topic narrations + NotebookLM audio: Poisson, Monte Carlo, bootstrap — plan (2026-10-31)

Decisions (asked 2026-10-31): TTS one file per topic, detailed, split into parts above ~90 min;
audio 1 Custom prompt per topic, Monte Carlo 2 (MC methods; MCMC) → 4 prompts, Hard,
file-subject, ≤ 5,000 chars, no language line.

## Sources per topic (study notes first, then books at printed pages)

| Topic | Notes | Books |
|---|---|---|
| Poisson | `Notas/L01/L01-02-poisson-mle-properties.md`, `L01-03-coal-mining-change-point.md`, `L01-04-first-bayesian-poisson.md`, `Notas/L02/L02-06-gaussian-vs-poisson-regression.md`, `Notas/L03/L03-02-conjugate-sequential-updating.md` (Gamma–Poisson), Poisson entries of the L01/L03 formulas and pitfalls notes | B Ex. 2.1.2, 2.2.3–2.2.4, 3.2.5, §3.4, §6.5; G §2.2, §7.1.1 |
| Monte Carlo | `Notas/L01/L01-05-comparing-estimators-mse-bootstrap.md` (MC study), `Notas/L03/L03-06-monte-carlo-simulation.md`, `L03-07-markov-chains-gibbs.md`, `L03-08-metropolis-hastings-hmc.md` | MS App. B, App. C §C.5; G Ch. 5–7 |
| Bootstrap | `Notas/L01/L01-05-comparing-estimators-mse-bootstrap.md` (bootstrap parts), `Notas/L02/L02-03-cross-validation-motorcycle.md` (bootstrap bands, if covered) | I §5.2 (pp. 212–215); MS §10.5 Nota 3 (pp. 339–340) for the bootstrap SE — MS §B.6 is accept–reject / importance sampling / SIR, not the bootstrap (found 2026-10-31) |

## Outputs

- `Leituras/topic-poisson-narrated[-partK].txt`, `topic-monte-carlo-narrated[-partK].txt`, `topic-bootstrap-narrated[-partK].txt`
- `NotebookLM/audio/topic-poisson-audio.md`, `topic-monte-carlo-audio-part1.md` (MC integration, accept–reject, importance sampling, MC studies of estimators), `topic-monte-carlo-audio-part2.md` (Gibbs, MH, switch point), `topic-bootstrap-audio.md`; rows added to `NotebookLM/README.md`.

## Verification

Narrations: speechify Step 6 checks (no `$ \ ^ _ { }`, no markdown/table remnants). Audio: chars ≤ 5,000;
every backticked source name exists in `NotebookLM/sources/`.
