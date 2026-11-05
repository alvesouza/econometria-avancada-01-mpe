---
description: Fetch and cache macro data for notebook projects — FRED, World Bank WDI, Penn World Table, Maddison, BCB SGS, IBGE SIDRA, Ipeadata — into a provenance registry so notebooks stay reproducible offline. Discovers and confirms every series code before downloading; --offline never touches the network.
argument-hint: <series-or-concept-or-topic> [--project <slug>] [--source fred|wdi|pwt|maddison|bcb|sidra|ipea] [--from YYYY] [--to YYYY] [--offline] [--refresh]
allowed-tools: Read Grep Glob Bash PowerShell Write Edit AskUserQuestion WebFetch WebSearch
---

Fetch the data described by `$ARGUMENTS`, cache it to disk, and record where every number came
from.

A notebook that downloads its own data is not reproducible: the series gets revised, the
endpoint changes, the network is absent, and the figure silently becomes a different figure.
This command is the only thing in the project that touches a data API. Notebooks read the cache.

## The rule that governs this entire command

**You do not know the current series codes, indicator codes, dataset versions, sheet names or
URL shapes. Neither do I.** They change, and a plausible-looking wrong code returns a
plausible-looking wrong series — the worst possible failure, because nothing errors.

So:

- Endpoint **patterns** below are stable enough to write down. Every concrete **code**,
  **version**, **file name** and **sheet name** is marked *to verify* and must be confirmed by
  a probe **in this run** before any bulk download.
- **Discover, then confirm, then fetch.** Search the provider's own metadata or search API,
  print the candidates with their names, units and date ranges, and have the user confirm the
  match. Only then download.
- Record in the registry what you actually verified, with the access date. **Never silently
  reuse an unverified code** on a later run.
- If you cannot confirm a code, say so and stop. A missing series is a reportable outcome; a
  wrong series is a corrupted study.

## Source reference — patterns to verify, never to assume

Probe each with a **single** call for one short range before fetching anything in bulk.

**FRED** (US and international macro)
- Keyed API: `https://api.stlouisfed.org/fred/series/observations?series_id=<ID>&api_key=<KEY>&file_type=json`
  Needs `FRED_API_KEY` **in the environment**, from `.env` (gitignored). Never hardcode it.
- Keyless CSV: `https://fred.stlouisfed.org/graph/fredgraph.csv?id=<ID>` — no key, one series.
- Discovery: the keyed `fred/series/search?search_text=...`, or the website's search. Confirm
  the **units** and **seasonal adjustment** from `fred/series` before using a series — the same
  concept exists in levels, percent change, and SA/NSA variants, and picking wrong is invisible.

**World Bank WDI** (cross-country)
- `https://api.worldbank.org/v2/country/<ISO3|all>/indicator/<CODE>?format=json&per_page=500`
- **Two traps.** The response is a **two-element array**: `[metadata, data]` — the rows are in
  element 1, not 0. And it **pages**: read `page`/`pages` from the metadata and loop, or you
  silently get the first 50 rows.
- Discovery: `https://api.worldbank.org/v2/indicator?format=json&per_page=...` or the WDI site.

**Penn World Table** and **Maddison Project** (GGDC, Groningen)
- Distributed as **versioned spreadsheet releases**, not an API. Resolve the **current release**
  from the GGDC site in this run and **record the version and the download URL**. Do not
  hardcode a version number from memory — PWT and Maddison both have multiple releases and the
  variable sets differ between them.
- **Inspect sheet names** with `pandas.ExcelFile(...).sheet_names`; do not guess. Releases
  typically ship a documentation/legend sheet — read it, and quote the variable definitions you
  rely on into the registry.
- PWT variable choice is a real modelling decision, not a detail: output concepts differ
  (national-accounts vs expenditure- vs output-side PPP), and there are separate variables for
  employment, hours, human capital, capital stock and TFP. **Name the exact variable and
  quote its definition from the release's own documentation** in the registry, because a
  development-accounting result changes with that choice.
- `openpyxl` is installed, so `.xlsx` reads work.

**BCB SGS** (Banco Central do Brasil)
- `https://api.bcb.gov.br/dados/serie/bcdata.sgs.<CODE>/dados?formato=json`
- **Date trap**: `dataInicial`/`dataFinal` are `dd/MM/yyyy`, and the returned `data` field is
  too — parse with `dayfirst=True` or every day/month pair under 13 silently transposes.
- There is a **row cap** per request for long daily series; page by date range when a long
  pull returns suspiciously few rows.
- Discovery: the SGS web interface lists codes with names, units and frequency. Confirm the
  **unit** — SGS carries the same concept as an index, a monthly percent and a 12-month
  accumulated percent under different codes.

**IBGE SIDRA**
- `https://apisidra.ibge.gov.br/values/t/<TABLE>/...` with period, variable, territory and
  classification segments.
- **The first returned row is a header row**, not data — drop it, or the whole column becomes
  strings.
- Tables, variables and classifications must be **discovered** from SIDRA's own table pages;
  the segment grammar is not guessable.

**Ipeadata**
- OData service. Take the entity list from the **service document / `$metadata`** rather than
  assuming entity names, then query the series by its code.

**Offline** (`--offline`) — a first-class path, not a fallback hack
- Never touches the network. Builds an explicit, hand-entered or synthetic dataset.
- Every synthetic file is stamped **`SYNTHETIC`**: in the registry, in a header comment in the
  CSV, and in a `synthetic: true` field. `/lab` and `/explainer` propagate that into figure
  titles, so a synthetic series can never be mistaken for an observation.

## Instructions

### Step 1: Resolve what is being asked for

`$ARGUMENTS` may be a series code, a concept ("Brazilian inflation", "US M1", "GDP per worker
across countries"), or a course topic that implies a set. Map it to the **lecture** and its
`rules/*.md` file, so the data serves stated economics rather than arriving orphaned.

Examples of the mapping for this course — the **concepts** are settled, the **codes are not and
must be discovered**:

| Lecture | Topic | What to look for |
|---|---|---|
| 1 | Measurement | nominal and real GDP, a deflator, a PPP conversion factor |
| 2–3 | Growth | long-run GDP per capita (Maddison); GDP per worker, capital, hours, human capital, TFP (PWT) |
| 4 | Consumption | aggregate consumption and disposable income; a real interest rate |
| 5 | Labour | participation, employment, hours, unemployment |
| 7 | Money and inflation | a price index and its inflation rate; a monetary aggregate and the base; a policy rate; money growth vs inflation across countries for the long-run relation |

### Step 2: Ask once

One `AskUserQuestion` round, only on what changes the result: the **source family**, the
**frequency and date range**, and whether to **reuse or refresh** an already-cached series.
Recommend from `$ARGUMENTS` and from what the registry already holds.

### Step 3: Discover and confirm the codes

Search the provider's metadata. Print a table of candidates — code, name, units, frequency,
date range — and have the user confirm. Then fetch **one short range** of the chosen series and
show the first and last few rows, with units, **before** pulling the full history.

This step is the whole point of the command. Do not skip it because a code "looks right".

### Step 4: Fetch

- Explicit timeout; retry only on transient failures (timeout, 429, 5xx) with backoff; honour
  `Retry-After`. Never retry a 400 or 404 — fix the query instead.
- Identify the client in a `User-Agent`. Respect rate limits and terms of use.
- Write CSV as the baseline (`pyarrow` is **not installed**, so parquet is best-effort only;
  add it alongside CSV if pyarrow appears, never instead of it).
- Cache into the project's `data/` (see `/lab-init`), one file per series, named by source and
  code: `data/<source>_<code>.csv`.
- **Three outcomes, and you must say which happened**: fetched fresh · served from cache ·
  fell back to offline. Never present cache or synthetic data as a fresh fetch.

### Step 5: Sanity-check before declaring success

Run every check and report what each found. A silent wrong series is the failure mode this
command exists to prevent.

1. Non-empty, and the row count is plausible for the frequency and range.
2. Dates parse, are monotonic, have no duplicates, and the gaps match the stated frequency.
3. **Units are stated and sane.** An inflation series of `0.05` versus `5.0` versus `105.2`
   (index) are three different objects. State the unit in the registry and check the magnitude
   against what the concept should be.
4. No placeholder sentinels treated as data (`-999`, `..`, empty strings → `NaN`).
5. For a cross-country pull: how many countries, how many missing, and which were dropped.
6. Print the head and tail with the index, so a transposed date or an off-by-a-decade is visible.

### Step 6: Write the registry

One machine-readable registry per project, `data/registry.json`, plus a human-readable table in
`data/README.md`. Per series:

```json
{
  "key": "bcb_433",
  "source": "BCB SGS",
  "code": "433",
  "name": "<the provider's own series name, verbatim>",
  "units": "<as stated by the provider>",
  "frequency": "monthly",
  "query": "<the exact URL or query used>",
  "verified_how": "<the probe that confirmed the code, name and units>",
  "accessed": "2026-09-12",
  "rows": 0, "date_range": ["", ""],
  "file": "data/bcb_433.csv", "sha256": "<checksum of the cached file>",
  "synthetic": false,
  "serves": "lecture 7 — rules/07_moeda_inflacao.md",
  "notes": "<revisions, seasonal adjustment, breaks, anything that would change a result>"
}
```

The checksum is what makes a figure traceable: if the cache changes, the registry disagrees and
the notebook's result is suspect.

### Step 7: Report

A provenance table: key, source, code, name, units, frequency, rows, range, fresh/cache/offline,
and which lecture it serves. Then the exact loader cell for the notebook:

```python
import pandas as pd
from pathlib import Path
DATA = Path("data")
ipca = pd.read_csv(DATA / "bcb_433.csv", parse_dates=["date"], index_col="date")
```

Close with what could **not** be verified, and what a future run should re-check.

## Important

- **Never fabricate or approximate a series.** If a download fails, the series is reported
  missing. Do not substitute a similar series, interpolate a gap you did not measure, or fill
  from memory — a number nobody can trace is worse than a hole in the table.
- **Synthetic data is labelled everywhere** it travels: registry, file header, and any figure
  built from it.
- **API keys come from the environment**, loaded from the gitignored `.env`. Never hardcode,
  never echo, never commit, never write a key into the registry. `.env.example` documents the
  variable names with no values.
- **Check the licence before committing bulk data.** `.gitignore` already excludes `Livros/` and
  `NotebookLM/sources/` for copyright; data redistribution is the same question. Cache locally,
  commit the registry, and commit raw data only when the licence allows it. Verify with
  `git check-ignore -v <path>` instead of assuming.
- **Units and vintage are part of the data.** A series without its unit and access date is not
  reusable, and revisions are why the access date matters.
- **Stay inside the course's economics.** Data serves a model from Kurlat chs. 1–7, 9–11 or
  Benigno. No time-series econometrics — no unit-root testing, no VARs, no cointegration. Plot
  it, average it, compute a growth rate, scatter it across countries; that is the level the
  course works at.
- **One concept, one series, one file.** Do not build wide multi-concept tables in the cache;
  join in the notebook where the join is visible.

## Ecosystem

- `/lab-init` → creates the `data/` directory and the loader cell this command fills.
- `/lab` → calls this command when an analysis needs series, then writes the analysis.
- `rules/*.md` → where the economics the data serves is written down; the `serves` field points back.
- `/explainer` → a beat that plots real data takes it from here, with provenance, never from a scene file.
- `/study-map` → can cross-reference a series to the lecture and exercise that use it.
- `/setup-study` copies this command into new study projects.
