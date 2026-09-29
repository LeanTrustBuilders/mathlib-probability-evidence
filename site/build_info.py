"""What the landing page says about this build: the dataset (which Mathlib, read by what, kept where),
the catalogue merged into it, the store and the stores it imports, and the tools' versions. The Pages workflow runs it after building the
front ends, with the environment it set (DATASET, CATALOGUE_TAG, IMPORTS, TW_COMMIT), and writes
its output to build.json.
"""
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import evidence_core
import evidence_store
import referee_site
from evidence_core.store import Store, with_imports

env = os.environ.get
meta = json.loads((Path(env("DATASET")) / "meta.json").read_text(encoding="utf-8"))
store = Store.load("evidence")
commit = meta["library"]["commit"]
where = store.config["datasets"]
facets = [f["name"] for f in meta.get("facets", [])]
imports = with_imports(store, env("IMPORTS")).read if env("IMPORTS") else []

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
    "store": {"repo": env("GITHUB_REPOSITORY"), "name": store.name},
    "imports": [{"repo": i["repo"], "name": i["name"], "commit": i["commit"]} for i in imports],
    "tools": {"referee-site": referee_site.__version__, "evidence-core": evidence_core.__version__,
              "evidence-store": evidence_store.__version__, "trust-web": (env("TW_COMMIT") or "")[:7]},
    "run": f"{env('GITHUB_SERVER_URL')}/{env('GITHUB_REPOSITORY')}/actions/runs/{env('GITHUB_RUN_ID')}"
           if env("GITHUB_RUN_ID") else None,
    "built": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
}, indent=1))
