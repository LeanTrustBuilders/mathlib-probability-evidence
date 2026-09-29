# Evidence about Mathlib's probability theory

An evidence store about [Mathlib](https://github.com/leanprover-community/mathlib4)'s probability
theory, shared with the libraries built on Mathlib, and three front ends that show it, published at
<https://leantrustbuilders.github.io/mathlib-probability-evidence/>:

- **the Referee site** (`site/`): Mathlib's probability theory read as a referee does, with every
  declaration's reviews and coverage under the reader's policy;
- **trust's front end** (`trust/`): the dependency tree of a declaration, with what reviewers accepted
  marked as trusted;
- **one claim's page** (`claim/`): the strong law of large numbers, with every review of what it
  rests on.

All three read the same records (`evidence/`) against the same dataset of Mathlib, so a record shows
up in each, with its status against the current code.

## Shared with the libraries built on Mathlib

A record names its declaration by what it means, not by the library it was made in, so it applies
wherever the declaration is used (S3's
[imported records](https://github.com/LeanTrustBuilders/specs/blob/main/S3-evidence.md#imported-records)):

- [Tau Ceti's Reviewed-by page](https://leantrustbuilders.github.io/reviewed-by-pilot/) and
  [LeanMachineLearning's site](https://leantrustbuilders.github.io/site-pilot/lml/) import this
  store: the reviews made here of the Mathlib declarations they rest on show on their pages, marked
  with this store, beside their own;
- this store imports theirs (`imports` in `evidence/store.json`): a review of a Mathlib declaration
  filed from either library is kept in that library's store, and shows here too.

A page shows an imported record with its status against its own dataset, without the buttons that
would change its state (its own store's to set), and the reader's policy says whether imported
reviews count.

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
  [Mathlib catalogue](https://github.com/LeanTrustBuilders/mathlib-catalogue) merged in, the stores this
  one imports (`evidence-store fetch-imports`), and the three front ends from them:
  [referee-site](https://github.com/LeanTrustBuilders/referee-site)'s `build` and `claim`, and
  [trust-web](https://github.com/LeanTrustBuilders/trust-web) on `referee-site trust-index --modules`, each
  with `--imports`.
- `site/index.html`: the landing page: how the pieces fit together and how the store is shared, the
  records with links into each front end (`site/records.py`: this store's, and the imported ones about
  Mathlib's declarations), and what this build was made from (`site/build_info.py` writes it as
  `build.json`).
