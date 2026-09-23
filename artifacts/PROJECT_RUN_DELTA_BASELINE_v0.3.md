# RUN-DELTA BASELINE v0.3

**Date:** 2026-09-23  
**Repository:** `GBOGEB/GBOGEB`  
**Method:** sequential `3P* -> MIP`  
**Evidence:** exact local source bytes + deterministic v0.2 source-class/graph semantics  
**Privacy:** no raw project-chat text is published.

## 1. Run definition

`RUN_A_V02` is the controlled ten-file source set used by Source-Class + BLOCK Graph v0.2.

`RUN_B_V03` is the full currently materialized upload set: **21 physical files**.

The comparison preserves five deliberately different views:

- `CHAT_ONLY`
- `ARTEFACT_ONLY`
- `CODE_ONLY`
- `ALL_UNIQUE`
- `PHYSICAL_RAW`

Binary documents such as PDF are hash-tracked as `GENERATED_ARTIFACT / BINARY_HASH_ONLY`; they contribute to source identity and physical/unique counts but not lexical or BLOCK-graph metrics.

## 2. Source-set identity

| Metric | RUN_A_V02 | RUN_B_V03 | Delta |
|---|---:|---:|---:|
| Physical files | 10 | 21 | **+11** |
| Unique SHA objects | 8 | 14 | **+6** |
| Duplicate copies | 2 | 7 | **+5** |
| Unique source classes | 7 | 9 | **+2** |
| Classification conflicts | 0 | 0 | **0** |

Physical-set SHA-256:

- RUN_A: `5f65cfd534a41126a601953a830cccf1f482ce757f12ea9bc11ac4e9a739fc8a`
- RUN_B: `7eade723ee5b146476a0a8d6d20a08ae19fa0448d178afd41f1fc85f4d66e691`

Semantic unique-set SHA-256:

- RUN_A: `f956cc8477cf4d6eaca7b6d3aebfdbd626668f12ec1b5ad6f3078f584eb64985`
- RUN_B: `9f32b634dc68b9cc95cf5aff426f95bf179fedf9458a9cd8f9213245e705a0e2`

## 3. Added / removed semantic objects

**Added unique SHA objects: 6. Removed: 0. Retained: 8.**

| Added SHA-256 | Representative source | Source class | Parse mode |
|---|---|---|---|
| `17ed61cc8cd152ae891be07563cf86604154ece13045ef3db6aff30d71848ecd` | `patch_all_markdown_Version2_1 (2).md` | DOCUMENTATION | TEXT_PARSED |
| `409c5318e08fbf7a95ad9476e43eb615859ec70e99d47a4c925339f606bdbfc0` | `patch_all_markdown_Version2_1 (1).txt` | CODE_PYTHON | TEXT_PARSED |
| `5ab2b6e6cc2c9258ef48c7484bcd758ebcf452332a584f4759e93f4c21da2939` | `README (2)_1.txt` | DEPENDENCY_MANIFEST | TEXT_PARSED |
| `63973f757b14a883e02cafc4c44a5f9da44234f692d57e6defc8fe40339b0fe5` | `README (1)_1.txt` | DEPENDENCY_MANIFEST | TEXT_PARSED |
| `742e27d5e153a5c926ba901a960b49791e71e5b8fa82204c7aef047775fe4a32` | `patch_all_markdown_Version2_1 (1).pdf` | GENERATED_ARTIFACT | BINARY_HASH_ONLY |
| `c047b250985606473ea6983a6fc864644e5ccf2921c9599da61c57deef6e7307` | `patch_all_markdown_Version2_1 (4).txt` | GENERATED_ARTIFACT | TEXT_PARSED |

No previously controlled semantic SHA object disappeared.

## 4. Duplicate growth

RUN_B contains five duplicate groups:

- `IMPLEN_1/2/3-0509.txt` — three copies, one SHA object.
- `README (1)_1.md` + `README (4)_1.md` — two copies.
- `README (2)_1.md` + `README (3)_1.md` — two copies.
- `patch_all_markdown_Version2_1 (1).py` + `(2).py` — two copies.
- `patch_all_markdown_Version2_1 (1)/(2)/(3).txt` — three copies, one SHA object.

This is why **physical growth (+11)** is not equivalent to **semantic growth (+6)**.

## 5. Five-view delta

| View | Member delta | Byte delta | Graph-node delta | Graph-edge delta | Main class delta |
|---|---:|---:|---:|---:|---|
| CHAT_ONLY | **0** | 0 | **0** | **0** | conversation 0 |
| ARTEFACT_ONLY | **+3** | +124,866 | **+58** | **+57** | documentation +1; generated artifact +2 |
| CODE_ONLY | **+3** | +3,654 | **+30** | **+28** | Python +1; dependency manifests +2 |
| ALL_UNIQUE | **+6** | +128,520 | **+88** | **+85** | six new unique objects |
| PHYSICAL_RAW | **+11** | +145,123 | **+187** | **+179** | includes five extra duplicate copies |

### Key interpretation

The conversation evidence did **not** change between the two runs. All measured graph growth is attributable to newly materialized artefact/code sources and duplicate physical copies.

This means project-level frequency drift must not be described as “the conversation changed.”

## 6. BLOCK / KEB / STEP anchors

Across `ALL_UNIQUE`:

| Anchor | RUN_A | RUN_B | Delta |
|---|---:|---:|---:|
| BLOCK | 7 | 7 | **0** |
| KEB | 9 | 9 | **0** |
| STEP_in | 0 | 0 | **0** |
| STEP_out | 0 | 0 | **0** |

There is **no new explicit BLOCK/KEB/STEP execution vocabulary** in the newly added semantic source objects.

Therefore no new recursive execution edge may be inferred from the added files.

## 7. HUMAN / VISUAL / quantitative drift

Across `ALL_UNIQUE`:

| Signal | RUN_A | RUN_B | Delta |
|---|---:|---:|---:|
| HUMAN | 41 | 41 | **0** |
| VISUAL | 30 | 32 | **+2** |
| quantitative | 0 | 0 | **0** |

The +2 VISUAL occurrences are entirely in the `ARTEFACT_ONLY` lane. `CHAT_ONLY` drift is zero for all three signals.

## 8. Source-class delta — unique semantic objects

| Source class | RUN_A | RUN_B | Delta |
|---|---:|---:|---:|
| CONVERSATION_TRANSCRIPT | 1 | 1 | 0 |
| HANDOVER_BUNDLE | 1 | 1 | 0 |
| SOURCE_INDEX | 1 | 1 | 0 |
| DOCUMENTATION | 2 | 3 | **+1** |
| CODE_PYTHON | 1 | 2 | **+1** |
| CODE_SHELL | 1 | 1 | 0 |
| WORKFLOW_CONFIG | 1 | 1 | 0 |
| DEPENDENCY_MANIFEST | 0 | 2 | **+2** |
| GENERATED_ARTIFACT | 0 | 2 | **+2** |

## 9. 3P*

### Refresh
PASS. Current producer main and MissionControl master were refreshed before the v0.3 branch.

### Probe
PASS. The first new information is not a source-class regression: it is the divergence between physical-file growth and semantic-source growth.

### Rank
PASS. Run-delta baselining is the correct next edge; no v0.2 source-class repair is justified.

### Prepare
PASS. The v0.3 comparator implements exact SHA-set delta, five views, graph/anchor drift, HUMAN/VISUAL/quantitative drift and binary hash-only handling.

### Prove
LOCAL PASS. Hosted exact-head proof pending.

### Commit
HOLD until hosted proof passes.

## 10. MIP

### Modernize
PASS. Source-set change is now explicit and reproducible rather than inferred from a latest snapshot.

### Innovate
PASS. Five simultaneous views prevent physical duplication, chat evidence, code growth and artefact growth from being conflated.

### Perpetuate
PASS_PENDING_HOSTED_PROOF_AND_MERGE. Comparator, unit tests, workflow, machine control and this human report establish the v0.3 restart surface.

## 11. Next predicate after v0.3 merge

Use the next exact materialized source set as `RUN_C` and compare it against this controlled RUN_B baseline.

Escalate only when a real delta exists, such as:

- removed SHA objects;
- source-class conflict;
- new/removed BLOCK/KEB/STEP anchors;
- CHAT_ONLY graph change;
- unexpected binary/text parser-mode transition;
- material HUMAN/VISUAL/quantitative drift.

No source-class repair is justified by the present delta.
