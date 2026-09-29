"""The records the landing page lists: the store's own, and those of the stores it imports that are
about declarations of the dataset (S3, "Imported records"), each with the repository of the store it
comes from (`store`). The Pages workflow runs it with DATASET and IMPORTS set, and writes its output
to records.jsonl.
"""
import json
import os

from evidence_core import Dataset, Evidence
from evidence_core.store import Store, with_imports

imported = with_imports(Store.load("evidence"), os.environ["IMPORTS"])
ev = Evidence.resolve(imported.records, Dataset.load(os.environ["DATASET"]), sources=imported.sources)
kept = {r["id"] for rows in ev.by_decl.values() for r, _ in rows} | {r["id"] for r, _ in ev.orphans}
kept |= {r["id"] for rs in ev.statuses.values() for r in rs}
for r in imported.records:
    if r["id"] not in imported.sources:
        print(json.dumps({**r, "store": os.environ["GITHUB_REPOSITORY"]}, ensure_ascii=False))
    elif r["id"] in kept:
        print(json.dumps({**r, "store": imported.sources[r["id"]]}, ensure_ascii=False))
