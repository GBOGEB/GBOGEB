# Project Source-Class Purity + BLOCK Graph v0.2

**Date:** 2026-09-22  
**Repository:** `GBOGEB/GBOGEB`  
**Execution model:** sequential `3P* -> MIP`  
**Raw-source policy:** raw project-chat text remains local/private; this public artifact contains only basenames, hashes, counts, classifications and graph statistics.

## 1. Why this slice exists

The v0.1 corpus established exact hashing and duplicate-aware frequency. The next defect class is **source mixing**: a conversation transcript, a handover bundle, Python code and a source inventory can all contain words such as `manifest`, `handover`, `for` or `BLOCK`, but those occurrences do not mean the same thing.

v0.2 therefore applies the rule:

`CLASSIFY SOURCE -> DEDUPLICATE BY SHA256 -> MEASURE WITHIN CLASS -> BUILD STRUCTURAL GRAPH -> FEDERATE RECEIPT`

No frequency is promoted to engineering, compliance or requirements authority.

## 2. Measured local corpus

Ten physical source files were measured from the supplied project material. They resolve to eight unique byte objects.

| Source | Class | SHA-256 | Graph nodes |
|---|---|---|---:|
| `IMPLEN_1-0509.txt` | CONVERSATION_TRANSCRIPT | `80d7069d142878e4a957f1d14635a45e07cbccbc94d878ed4eb4a540d4576c26` | 261 |
| `IMPLEN_2-0509.txt` | CONVERSATION_TRANSCRIPT | same exact bytes | 261 |
| `IMPLEN_3-0509.txt` | CONVERSATION_TRANSCRIPT | same exact bytes | 261 |
| `patch_all_markdown_Version2_1 (1).md` | HANDOVER_BUNDLE | `984313fccf81b6f355c9a96402647235f58632f3f0b6941b6879e6c44197700e` | 50 |
| `MAIN CODE artefact for smoking, rec_HANDOVER_file locaiton - in MASTER.txt` | SOURCE_INDEX | `45c64f7ef2cba5915055fcc5fad765c27ff068ee6db5e30c8c7c3baf3317a1a7` | 1 |
| `README (1)_1.md` | DOCUMENTATION | `20ab72e4bfc7eaba201fe500d4f1ba43884cfdc3fdb07b1caa438e8557f046ce` | 27 |
| `README (2)_1.md` | DOCUMENTATION | `7227c78118421f895c8f82b090c6cfdfaacd88808966e6303740a3d674a9da0d` | 22 |
| `patch_all_markdown_Version2_1 (1).py` | CODE_PYTHON | `8e1636309f73fe7fcb76829ea6861f901af645db40bc2bea33a999a2b69571b7` | 6 |
| `patch_all_markdown_Version2_1 (1).sh` | CODE_SHELL | `07c80dbf77e725a2dc607c33a8a55f97040626a01219731b247816748ab2a188` | 3 |
| `patch_all_markdown_Version2_1 (1).yml` | WORKFLOW_CONFIG | `a60f2efd9ef3f5a17dbf74989ef5240c1fbe0db8c97bd38c47b5bb19887dcf51` | 0 |

### Coverage metrics

- Physical files: **10**
- Unique byte objects: **8**
- Duplicate physical copies: **2**
- Unique source classes observed: **7**
- Classification conflicts across identical hashes: **0**
- Source-class purity on unique hashes: **8/8 = 100%**
- Privacy-safe structural graph: **370 nodes / 363 sequential edges**

The three `IMPLEN_*` files remain one semantic object, not three votes.

## 3. Source-class frequency separation

Selected unique-content counts:

| Signal | Conversation | Handover | Source index | Documentation | Python | Shell | Workflow |
|---|---:|---:|---:|---:|---:|---:|---:|
| BLOCK | 6 | 0 | 1 | 0 | 0 | 0 | 0 |
| KEB | 6 | 0 | 0 | 0 | 0 | 0 | 0 |
| HUMAN | 39 | 2 | 0 | 0 | 0 | 0 | 0 |
| VISUAL | 30 | 0 | 0 | 0 | 0 | 0 | 0 |
| manifest | 65 | 40 | 3 | 0 | 4 | 0 | 0 |
| handover | 80 | 11 | 6 | 1 | 1 | 0 | 1 |
| `def` lexical | 42 | 8 | 0 | 2 | 2 | 0 | 0 |
| `if` lexical | 25 | 27 | 0 | 1 | 3 | 4 | 1 |
| `for` lexical | 140 | 28 | 11 | 13 | 1 | 0 | 0 |
| Word | 121 | 0 | 1 | 1 | 0 | 0 | 0 |
| Excel | 88 | 0 | 0 | 21 | 0 | 0 | 0 |
| Python | 44 | 7 | 0 | 17 | 0 | 0 | 3 |
| VBA | 42 | 0 | 0 | 16 | 0 | 0 | 0 |
| DeepAgent | 46 | 0 | 0 | 0 | 0 | 0 | 0 |
| MCP | 44 | 0 | 0 | 0 | 0 | 0 | 0 |
| DMAIC | 57 | 7 | 1 | 0 | 0 | 0 | 0 |
| recursive | 8 | 15 | 5 | 0 | 0 | 0 | 0 |
| status | 118 | 0 | 5 | 0 | 0 | 0 | 1 |
| runtime | 67 | 0 | 0 | 0 | 0 | 0 | 0 |

This demonstrates why one global frequency table is insufficient. For example, `manifest` is strongly present in both conversation and handover artifacts; `for` is mostly ordinary prose in conversation but also appears as actual control flow in code.

## 4. BLOCK graph

The graph is deliberately **structural**, not semantic. It does not infer intent or engineering meaning.

Node types:

- `BLOCK_EXPLICIT`: explicit `BLOCK` token.
- `KEB_MARKER`: explicit KEB token.
- `STEP_IN` / `STEP_OUT`: explicit pipeline anchors.
- `BLOCK_CONVERSATION_TURN`: derived only from explicit speaker markers.
- `BLOCK_SECTION`: derived only from explicit Markdown headings.
- `CONTROL_DEF`: explicit Python function structure.
- `CONTROL_FLOW`: explicit code `if/for/while` structure.

Raw labels are **not emitted**. Every node carries only source hash, line number, node type, evidence type and `label_sha256`.

### Graph by source class

| Source class | Unique sources | Nodes | Edges | Main observed node types |
|---|---:|---:|---:|---|
| CONVERSATION_TRANSCRIPT | 1 | 261 | 260 | 148 section blocks; 18 speaker-turn blocks; 42 defs; 41 control-flow; 6 explicit BLOCK; 6 KEB |
| HANDOVER_BUNDLE | 1 | 50 | 49 | 22 section blocks; 8 defs; 20 control-flow |
| DOCUMENTATION | 2 | 49 | 47 | 46 section blocks; 2 defs; 1 control-flow |
| CODE_PYTHON | 1 | 6 | 5 | 2 defs; 4 control-flow |
| CODE_SHELL | 1 | 3 | 2 | 2 section/comment headings; 1 control-flow |
| SOURCE_INDEX | 1 | 1 | 0 | 1 explicit BLOCK |
| WORKFLOW_CONFIG | 1 | 0 | 0 | none under current structural grammar |

## 5. Digital-twin mirror contract

The graph is a **reflection of observed structure**, not a replacement truth store.

```text
raw/private source
      |
      +--> SHA256 identity
      |
      +--> source class
      |
      +--> lexical + structural metrics
      |
      +--> privacy-safe graph (hashed labels)
                  |
                  v
            public control / receipt
```

If two sources share a hash but classify differently, the run exposes a `classification_conflict` rather than silently selecting one.

## 6. 3P*

### Refresh
PASS. Current `GBOGEB/GBOGEB` main and current MissionControl master were refreshed before this branch.

### Probe
PASS. v0.1 controlled duplicates but still mixed heterogeneous source classes in one semantic aggregate.

### Rank
PASS. The first-red is source-class purity before any further global frequency ranking or recursive graph analytics.

### Prepare
PASS. Local implementation and five deterministic tests pass across classification, privacy, deduplication and graph sequencing.

### Prove
PENDING hosted exact-head GitHub Actions proof.

### Commit
HOLD until hosted proof is green.

## 7. MIP

### Modernize
PASS. Aggregation is now source-class-first and duplicate-aware.

### Innovate
PASS. BLOCK graphs are hash-labelled and privacy-safe while retaining exact source line positions and evidence types.

### Perpetuate
PASS_PENDING_HOSTED_PROOF_AND_MERGE. CI, tests, CURRENT controls and this artifact make the method restart-discoverable.

## 8. Next edge after merge

After hosted proof and merge:

1. add more exact conversation exports by SHA-256;
2. introduce explicit `STEP_in/STEP_out` anchors only when actually present or generated by a governed pipeline transform;
3. build cross-run change statistics on graph shape, source-class frequency and new/removed blocks;
4. keep `CHAT_ONLY`, `ARTEFACT_ONLY`, `CODE_ONLY`, `ALL_UNIQUE` and `PHYSICAL_RAW` as distinct analytical views.
