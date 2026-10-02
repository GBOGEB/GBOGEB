# Governance directory

This directory contains **profile-repository producer evidence and thin canonical pointers**. It is not a second TRIAGE or Mission Control SSOT.

## Classification

### Profile-local producer controls — retain here

These files describe work produced and proven in `GBOGEB/GBOGEB` itself:

- `PROJECT_KNOWLEDGE_MAP_CURRENT_v0.1.yaml`
- `PROJECT_CONVERSATION_CORPUS_CURRENT_v0.1.yaml`
- `PROJECT_SOURCE_CLASS_BLOCK_GRAPH_CURRENT_v0.2.yaml`
- `PROJECT_RUN_DELTA_CURRENT_v0.3.yaml`
- their corresponding proof, repair and post-merge closure receipts

The associated scripts/tests also remain local because downstream receiver handovers bind to this repository as the producer.

### Cross-repository bridge pointers — canonical elsewhere

- `GLOBAL_EXCEL_SCHEDULE_ENGINE_TOPOLOGY_v1.yaml`
  - canonical implementation/control: `GBOGEB/pipeline-automation-hub:excel_schedule_engine/`
- `GLOBAL_MATH_PLOTS_SKILL_TOPOLOGY_v1.yaml`
- `GLOBAL_MATH_PLOTS_MIP_HARDENING_v1.yaml`
- `GLOBAL_MATH_PLOTS_WAVES_N_PLUS_2_v1.yaml`
  - canonical skill SSOT: `GBOGEB/skills`
  - canonical orchestration: `GBOGEB/pipeline-automation-hub`
  - mathematical runtime/provider: `GBOGEB/gg_MATH`

These paths are now thin pointers only. Their pre-pointer payloads are preserved under `artifacts/governance-snapshots/`. They must not receive independent readiness or implementation claims that diverge from their owning repositories.

## TRIAGE / Mission Control routing

- QPS engineering authority: `GBOGEB/cryoplant-project`
- KEB semantic/provenance parent: `GBOGEB/CODEX`
- DOW analytical/runtime parent: `GBOGEB/ABACUS`
- Mission Control and TOP7/TOP14/TOP21 cohorts: `GBOGEB/pipeline-automation-hub`

No local folder in this profile repo should be promoted to replace those authorities.

## Migration rule

The reference census is recorded in `BRIDGE_REFERENCE_CENSUS_20261002_v1.yaml`. The existing `GLOBAL_*` paths are preserved as durable pointers because historical lineage still references them. Do **not** rename or delete those pointer paths; update canonical owners first and retain immutable historical payloads under `artifacts/governance-snapshots/`.
