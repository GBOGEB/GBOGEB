# Project Keyword / Block Map v0.1

**Date:** 2026-09-18  
**Repository:** `GBOGEB/GBOGEB`  
**Method:** sequential `3P* -> MIP`  
**Evidence class:** `SOURCE-SUPPORTED` for the exact repository corpus named below; project-chat-wide frequency remains `POSTULATED/UNMEASURED` until the complete chat corpus is materialized.

## 1. Purpose

This is the first governed project knowledge-map surface for the BASIC / KEB / recursive-build vocabulary. It is designed to become a machine-readable and human-readable bridge between:

`CONVERSATION -> BLOCK -> KEB -> STEP_in -> execution -> STEP_out -> receipt -> recursive build`

The map is not a new engineering authority. It is a navigation, parsing, discovery, smoke-test and handover layer.

## 2. Exact measured corpus

The following repository files were measured exactly at the branch start point `8dd088430155fb014ae74dcf23f9f8020015ff27`:

| File | Characters | Lines |
|---|---:|---:|
| `README.md` | 915 | 24 |
| `artifacts/PROJECT_CHAT_CATALOGUE_v1.0.md` | 6,863 | 157 |
| `artifacts/DMAIC_v1.0.md` | 9,804 | 246 |
| `artifacts/MASTER_DOCS_v1.0.md` | 11,119 | 253 |
| **Total source footprint** | **28,701** | **680** |

## 3. Lexical frequency baseline

These are exact lexical counts for the measured corpus above, not the whole historical ChatGPT project:

| Term / phrase | Exact count |
|---|---:|
| GitHub | 54 |
| DeepAgent | 34 |
| baseline | 28 |
| digital twin | 24 |
| DMAIC | 22 |
| for | 19 |
| dashboard | 13 |
| MCP | 5 |
| VISUAL | 4 |
| handover | 4 |
| RTM | 4 |
| BLOCK | 1 |
| if | 1 |
| conversation | 1 |
| def | 0 |
| while | 0 |
| STEP_in | 0 |
| STEP_out | 0 |
| KEB | 0 |
| HUMAN | 0 |
| quantitative | 0 |
| manifest | 0 |
| recursive | 0 |

### Interpretation guard

Zero does **not** mean absent from the wider project. It means absent in this exact four-file corpus. In particular, `KEB`, `GLOB`, `3P*`, `MIP`, recursive controls and step anchors are already present in the wider repository ecosystem, but are not yet represented in these older GBOGEB profile artifacts.

## 4. Controlled vocabulary / parser classes

| Class | Examples | Parser intent |
|---|---|---|
| STRUCTURE | BLOCK, KEB, STEP_in, STEP_out | Build execution graph and recursive anchors |
| CONTROL_FLOW | def, if, for, while | Detect code-like execution semantics |
| GOVERNANCE | 3P*, 3PR, 3PC, MIP, DMAIC, GLOB | Bind proof/restart/control semantics |
| HUMAN | HUMAN, conversation, handover, business card | Preserve usable human transfer surfaces |
| VISUAL | VISUAL, dashboard, graph, RYG | Quality/readability/navigation layer |
| QUANT | quantitative, frequency, KPI, runtime | Measured evidence and trend layer |
| TRACEABILITY | RTM, manifest, baseline, receipt | Provenance and change tracking |
| FEDERATION | MCP, GitHub, DeepAgent, CODEX, ABACUS, GBOGEB_RH | External/agent/repo interfaces |

## 5. BASIC digital-twin mirror rule

The digital twin must be a reflection, not a second truth store:

```text
SOURCE / MASTER
      |
      v
 [STEP_in]
      |
   [BLOCK]
      |
    [KEB]
      |
  execute / parse / map / analyse
      |
 [STEP_out]
      |
   RECEIPT
      |
  OUTPUT / TWIN
      |
 compare(hash + semantic anchors)
      |
 recursive update only if impacted
```

The twin may normalize, index, render and derive views, but source authority remains explicit and hashes/lineage must make divergence visible.

## 6. Conversation tuple

Canonical tuple proposal:

```text
(sender, recipient, intent, source_ref, STEP_in, BLOCK, KEB,
 action, observation, STEP_out, receipt_ref, next_predicate)
```

This lets the same conversation be rendered as:
- sequential human transcript;
- JSON/YAML execution records;
- graph edges;
- PDF preview;
- handover/business card;
- recursive build input.

## 7. Human visual contract

A BASIC review surface should show:

- RYG / PASS-HOLD-FAIL status;
- entry and exit anchors;
- source and output hashes;
- changed / unchanged / missing;
- current first-red;
- runtime per block;
- artefact links;
- evidence class;
- human owner / machine executor;
- current and prior receipt.

For long conversation PDFs, the default visual-QA slice is:
1. title page;
2. table of contents / execution index;
3. a representative middle block;
4. final four pages.

This is a preview rule, not a substitute for full semantic validation.

## 8. 3P* sequential result

### 3PR — Refresh
PASS. Current GBOGEB main, MissionControl master and QPS recursive authority were read before write.

### Probe
PASS. The older GBOGEB artifact set exposes Digital Twin / DMAIC / GitHub vocabulary but lacks the newer BLOCK / KEB / STEP anchor and recursive-governance vocabulary.

### Rank
PASS. Highest-value bounded change is a parser + manifest + smoke gate, not a rewrite of historical artifacts.

### 3PC — Prepare
PASS. Bounded branch created from exact GBOGEB main.

### 3PC — Prove
PASS by construction path: dependency-free parser plus unit smoke and GitHub Actions workflow have been added. Runtime CI evidence is pending GitHub execution on the PR.

### 3PC — Commit
HOLD until PR checks/merge; no authority transfer and no engineering/formal credit.

## 9. MIP result

### Modernize — PASS
Introduced a dependency-free parser that separates lexical frequency from structural code signals and explicitly labels corpus coverage.

### Innovate — PASS
Introduced a reusable tuple/block model that can serve chat, code, document, visual and external-agent lanes without treating one representation as authority for another.

### Perpetuate — PASS/PENDING MERGE
Added a repository-native CURRENT control file, artifact map, tests and CI smoke. Perpetuation becomes fully controlled only after PR merge and later measured-corpus expansion.

## 10. Next bounded expansion

1. Materialize exported project conversations into a governed corpus.
2. Run the same mapper over exact chat exports.
3. Add GLOB / 3P* / MIP / KEB / HUMAN / VISUAL / STEP anchors to the controlled dictionary.
4. Emit JSON + CSV + Markdown frequency tables.
5. Add graph edges for BLOCK input/output and KEB ownership.
6. Generate conversation PDF preview receipts with title/TOC/representative middle/final-four-pages QA.
7. Keep project-wide claims withheld until source coverage is explicit.
