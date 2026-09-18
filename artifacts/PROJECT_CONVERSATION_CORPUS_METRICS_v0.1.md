# Project Conversation Corpus Metrics v0.1

**Date:** 2026-09-18  
**Evidence class:** exact local-materialized source metadata + aggregate counts  
**Privacy rule:** raw conversation text is not committed to the public repository.

## Corpus coverage

Four physical historical files were measured:

| Source | Bytes | Characters | Lines | SHA-256 |
|---|---:|---:|---:|---|
| `IMPLEN_1-0509.txt` | 100,683 | 99,365 | 2,769 | `80d7069d142878e4a957f1d14635a45e07cbccbc94d878ed4eb4a540d4576c26` |
| `IMPLEN_2-0509.txt` | 100,683 | 99,365 | 2,769 | `80d7069d142878e4a957f1d14635a45e07cbccbc94d878ed4eb4a540d4576c26` |
| `IMPLEN_3-0509.txt` | 100,683 | 99,365 | 2,769 | `80d7069d142878e4a957f1d14635a45e07cbccbc94d878ed4eb4a540d4576c26` |
| `patch_all_markdown_Version2_1 (1).md` | 18,187 | 18,181 | 511 | `984313fccf81b6f355c9a96402647235f58632f3f0b6941b6879e6c44197700e` |

### Dedupe finding

The three `IMPLEN_*-0509.txt` files are byte-identical.

- Physical files: **4**
- Unique content objects: **2**
- Duplicate files: **2**
- Raw characters: **307,975**
- Unique-content characters: **117,547**
- Raw lines: **8,818**
- Unique-content lines: **3,280**

For semantic/project-frequency interpretation, the unique-content aggregate is the controlled view. Raw aggregation is retained only as physical-ingest volume.

## Unique-content lexical frequency

| Term | Count |
|---|---:|
| for | 168 |
| Word | 121 |
| status | 118 |
| manifest | 105 |
| handover | 91 |
| Excel | 88 |
| PPT | 80 |
| runtime | 67 |
| DMAIC | 64 |
| Markdown | 63 |
| if | 52 |
| Python | 51 |
| def | 50 |
| DeepAgent | 46 |
| MCP | 44 |
| VBA | 42 |
| HUMAN | 41 |
| GitHub | 30 |
| VISUAL | 30 |
| recursive | 23 |
| decision | 22 |
| CSV | 14 |
| JSON | 14 |
| dashboard | 13 |
| baseline | 11 |
| PDF | 8 |
| BLOCK | 6 |
| KEB | 6 |
| conversation | 6 |
| while | 1 |
| STEP_in | 0 |
| STEP_out | 0 |
| GLOB | 0 |
| 3P | 0 |
| MIP | 0 |
| RTM | 0 |
| YAML | 0 |
| receipt | 0 |
| quantitative | 0 |
| digital twin | 0 |

## Structural signals — unique content

| Signal | Count |
|---|---:|
| Python function definitions | 50 |
| Python `if` statements | 31 |
| Python `for` statements | 30 |
| Python `while` statements | 0 |
| KEB markers | 9 |
| BLOCK markers | 6 |
| STEP_in anchors | 0 |
| STEP_out anchors | 0 |

## Interpretation

This older historical corpus is strongly oriented toward:

1. document-tool orchestration: Word / Excel / PPT / VBA / Python / Markdown;
2. handover, manifest and runtime status;
3. human-readable / visual control;
4. DeepAgent / MCP integration;
5. DMAIC and recursive packaging.

The later governance vocabulary (`GLOB`, `3P*`, `MIP`, explicit `STEP_in/STEP_out`) is absent from this source set. That absence is temporal/corpus-specific and must not be generalized to the current project.

## Control rule

Never rank concepts using physical-file frequency when duplicate content exists. Report both:

- `aggregate_raw` for ingest/storage/runtime volume;
- `aggregate_unique` for semantic/project-frequency interpretation.

This avoids a single duplicated conversation becoming three votes.
