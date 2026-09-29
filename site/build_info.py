"""What the landing page says about this build: the dataset (which Mathlib, read by what, kept where),
the catalogue merged into it, and the tools' versions. The Pages workflow runs it after building the
front ends, with the environment it set (DATASET, CATALOGUE_TAG, IMPORTS, TW_COMMIT), and writes
its output to build.json.
"""
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import evidence_core
import evidence_store
import trust_site

env = os.environ.get
meta = json.loads((Path(env("DATASET")) / "meta.json").read_text(encoding="utf-8"))
store = json.loads(Path("evidence/store.json").read_text(encoding="utf-8"))
commit = meta["library"]["commit"]
where = store["datasets"]
facets = [f["name"] for f in meta.get("facets", [])]
manifest = Path(env("IMPORTS") or ".", "imports.json")
imports = json.loads(manifest.read_text(encoding="utf-8")) if manifest.exists() else []

print(json.dumps({
    "library": {"repo": meta["library"]["repo"], "commit": commit},
    "lean": (meta.get("lean") or {}).get("version") or meta.get("toolchain"),
    "producer": meta.get("producer") or {},
    "spec": meta.get("spec"),
    "hasher": meta.get("hasher") or {},
    "nodes": (meta.get("counts") or {}).get("nodes"),
    "kernel": any(f.startswith("check.kernel") for f in facets),
    "dataset": {"repo": where["repo"],
                "tag": where["tag"].replace("{commit12}", commit[:12]).replace("{commit}", commit)},
    "catalogue": {"repo": "LeanTrustBuilders/mathlib-catalogue", "tag": env("CATALOGUE_TAG")}
                 if env("CATALOGUE_TAG") else None,
    "imports": [{"repo": i["repo"], "commit": i.get("commit")} for i in imports],
    "tools": {"referee-site": trust_site.__version__, "evidence-core": evidence_core.__version__,
              "evidence-store": evidence_store.__version__, "trust-web": (env("TW_COMMIT") or "")[:7]},
    "run": f"{env('GITHUB_SERVER_URL')}/{env('GITHUB_REPOSITORY')}/actions/runs/{env('GITHUB_RUN_ID')}"
           if env("GITHUB_RUN_ID") else None,
    "built": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
}, indent=1))
