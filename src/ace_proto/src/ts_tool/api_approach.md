# API Approach
## What agents actually need (ranked)

1) `get_public_interface` → KEEP (high value)
- **Why**: Gives a token-lean map of everything callable/usable: classes → methods, functions, constants, with signatures (and return types if known).
- **Agent use**: Planning (“which function do I call?”), generating calls, writing wrappers, quick diffing across versions.
- **Position** it as the single source of truth for the surface area.

2) `get_entity` (detail = `signature|full|summary`) → KEEP (critical)
- **Why**: Precise, on-demand fetch of one thing at the right granularity.
- **Agent use**: “Give me just the signature of Foo.bar,” or “show full source so I can patch.”
- **Tip**: Always include line/byte spans in the response for surgical edits.

3) `get_source_code` / `get_signature` / `get_documentation` → KEEP (thin conveniences)
- Why: These are just ergonomic shorthands around get_entity that reduce prompt tokens and branching.
- Agent use: Templateable steps like “pull signature → synthesize call → verify.”

4) `detect_language` / `get_supported_languages` → KEEP (utilities)
- **Why**: Routing and validation.
- **Agent use**: Decide parser; early fail if unsupported.

5) `get_code_summary` → KEEP, but narrowly (optional, fast header)
- **Why**: A cheap pre-scan for: total lines, counts, top names. Great for indexing, routing, and making a tiny “front-matter” without crawling everything.
- **Agent use**: “Is this file worth deeper parse?” “Which top-N entities to inspect next?”
- **Rule of thumb**: If you already called `get_public_interface`, you often don’t need get_code_summary. Keep it for speed when you want quick triage.


| API                       | Keep?        | Role                                | When it earns its keep                          |
| ------------------------- | ------------ | ----------------------------------- | ----------------------------------------------- |
| `get_public_interface`    | ✅            | authoritative surface (signatures)  | planning, tool wiring, diffing, code search UIs |
| `get_entity`              | ✅            | precise fetch at chosen granularity | targeted reads/edits, patching, refactors       |
| `get_source_code`         | ✅            | convenience for FULL                | patch/apply/verify loops                        |
| `get_signature`           | ✅            | convenience for SIGNATURE           | call-synthesis pipelines                        |
| `get_documentation`       | ✅            | convenience for docs                | doc-aware retrieval, help overlays              |
| `detect_language`         | ✅            | routing                             | before parse                                    |
| `get_supported_languages` | ✅            | capability check                    | gating / UX hints                               |
| `get_code_summary`        | ✅ (optional) | fast triage header                  | indexing, skim-filters, front-matter generation |
