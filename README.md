# Evidence about Mathlib's probability theory

An evidence store about [Mathlib](https://github.com/leanprover-community/mathlib4)'s probability
theory, and four front ends that show it, published at
<https://leantrustbuilders.github.io/mathlib-probability-evidence/>:

- **the Referee site** (`site/`): Mathlib's probability theory read as a referee does, with every
  declaration's reviews and coverage under the reader's policy;
- **trust's front end** (`trust/`): the dependency tree of a declaration, with what reviewers accepted
  marked as trusted;
- **one claim's page** (`claim/`): the strong law of large numbers, with every review of what it
  rests on;
- **Reviewed-by** (`reviewed-by/`): every declaration, searchable, with its review marks and tests.

All four read the same records (`evidence/`) against the same dataset of Mathlib, so a record shows
up in each, with its status against the current code.

## Adding to it

Open an issue with one of the [forms](https://github.com/LeanTrustBuilders/mathlib-probability-evidence/issues/new/choose):
review a declaration, report a problem, ask a question, propose a test, list a test, name a result.
Intake turns it into a record in `evidence/records/`, keyed by the declaration's hashes in the
dataset, and rebuilds the pages. Commands in comments change a record's state (`/withdraw`,
`/answered`, `/met <declaration>`, …). Records are never anonymous, and an AI agent's are labelled as
such.

## How it is built

- `evidence/store.json`: the library (Mathlib, root `Mathlib`), where its datasets are (the releases
  `mathlib-dataset-<commit12>` of [Mathlib Explorer](https://github.com/LeanTrustBuilders/mathlib-explorer)),
  and the claims (the probability results of Mathlib's lists of famous theorems).
- `.github/workflows/evidence-intake.yml` and `evidence-check.yml`: the store, by
  [evidence-store](https://github.com/LeanTrustBuilders/evidence-store).
- `.github/workflows/pages.yml`: the newest dataset, with the
  [Mathlib catalogue](https://github.com/LeanTrustBuilders/mathlib-catalogue) merged in, and the four
  front ends from it: `trust-site build` and `trust-site claim` from
  [referee-site](https://github.com/LeanTrustBuilders/referee-site),
  [trust-web](https://github.com/LeanTrustBuilders/trust-web) on `trust-site trust-index --modules`, and
  the page of [Reviewed-by](https://github.com/LeanTrustBuilders/reviewed-by-pilot) with the settings
  `site/reviewed-by.json`.
- `site/index.html`: the landing page: how the pieces fit together, the records with links into each
  front end, and what this build was made from (`site/build_info.py` writes it as `build.json`).
