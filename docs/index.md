---
layout: default
title: SEEM — Structured Episodic Event Memory
---

# 🧠 SEEM

**Structured Episodic Event Memory** for LLM agents. Built on cognitive frame theory, SEEM organizes memory hierarchically.

<p align="center">
  <img src="figs/Memory_Layer.png" width="90%" alt="SEEM Memory Architecture">
  <br>
  <em>Overview of the SEEM hierarchical memory architecture.</em>
</p>

<p align="center">
  <img src="figs/Memory_Fusion.png" width="85%" alt="Memory Fusion Process">
  <br>
  <em>Overview of the associative consolidation and fusion.</em>
</p>

<p align="center">
  <a href="https://arxiv.org/abs/2601.06411"><img src="https://img.shields.io/badge/arXiv-2601.06411-b31b1b?style=flat&labelColor=555" alt="arXiv"></a>
  <a href="https://github.com"><img src="https://img.shields.io/badge/github-SEEM-181717?style=flat&labelColor=555&logo=github&logoColor=white" alt="GitHub"></a>
  <a href="#"><img src="https://img.shields.io/badge/license-MIT-2EA44F?style=flat&labelColor=555" alt="License"></a>
</p>

---

## Memory Representation Showcase

SEEM produces three complementary memory views from raw dialogue turns, each serving a distinct retrieval and reasoning purpose.

### Memory Summary

Each memory entry is anchored by a concise **summary** together with **provenance metadata**: speaker, timestamp range, entity list, and source utterance links. This provides a high-level snapshot of what happened, who was involved, and where the information came from.

<p align="center">
  <img src="figs/Memory_Summary.png" width="85%" alt="Memory Summary Example">
  <br>
  <em>Memory summary with provenance tracking — speaker, time range, linked entities, and source utterances.</em>
</p>

### Episodic Event Frames

SEEM decomposes each memory into structured **events** with six dedicated slots: *participants*, *action*, *time*, *location*, *reason*, and *method*. Each slot is strictly separated — actions contain only the core event, while temporal, spatial, and causal information occupy their own slots. This enables precise cross-event querying and reasoning.

<p align="center">
  <img src="figs/Memory_Event.png" width="85%" alt="Episodic Event Frame Example">
  <br>
  <em>Structured event with six episodic slots — participants, action, time, location, reason, and method each occupy a dedicated slot.</em>
</p>

### Semantic Fact Graph

From extracted events, SEEM builds a **knowledge graph** of relational triples — each connecting a subject entity to an object through a predicate. Entities are linked across memories, forming a connected graph that supports multi-hop traversal and graph-aware retrieval. This layer captures relational knowledge that complements the narrative structure of episodic memory.

<p align="center">
  <img src="figs/Semantic_Facts.png" width="85%" alt="Semantic Fact Graph Example">
  <br>
  <em>Knowledge graph of relational facts — subject-predicate-object triples with cross-memory entity linking.</em>
</p>

---

## Paper Highlights

Conventional LLM memory systems predominantly rely on static retrieval. SEEM introduces a structured alternative:

- **Beyond Static RAG** — instead of passive document retrieval, SEEM builds cognitive-inspired memory structures
- **Hierarchical Architecture** — relational facts live in a graph layer while narratives progress through dynamic episodic memory
- **Episodic Event Frames (EEFs)** — conversation streams become structured frames with provenance tracking
- **Reverse Provenance Expansion (RPE)** — backfill mechanism reconstructs fragmented evidence into coherent narrative context
- **Associative Fusion** — cross-layer linking connects related information dynamically

---

## Key Advantages

| Advantage | Description |
|-----------|-------------|
| **Cognitive-Inspired Design** | Memory structure grounded in frame theory, reflecting human memory organization with hierarchical episodic and graph-based representations. |
| **Dual-Layer Architecture** | Relational facts reside in a graph layer while narratives progress through dynamic episodic memory, each with dedicated retrieval mechanisms. |
| **Provenance-Aware** | Every memory carries source pointers, enabling tracking of where information originated. |
| **Automatic Consolidation** | Related events merge into coherent summaries through an LLM-judged integration pipeline without manual intervention. |
| **Graph-Aware Retrieval** | Personalized PageRank traverses the knowledge graph along entity relationships to surface contextually relevant memories. |
| **Adjustable Recall Depth** | Three recall modes (Lite, Pro, Max) control context granularity, from concise fact-based summaries to full source text with backfill. |

---

## Quick Start

### 1. Install

```bash
pip install -r requirements.txt
```

### 2. Configure

Set environment variables for API access:

```bash
export LLM_API_KEY="sk-xxx"
export LLM_BASE_URL="https://api.deepseek.com"
export LLM_MODEL="deepseek-chat"

export MM_ENCODER_API_KEY="sk-xxx"
export MM_ENCODER_BASE_URL="https://api.siliconflow.cn/v1"
export MM_ENCODER_MODEL="Qwen/Qwen3-Embedding-8B"
```

Alternatively, edit `config.py` to change default settings such as retrieval strategy, embedding model, and integration parameters. Environment variables take priority over `config.py` values.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `retrieve_strategy` | `ppr` | Retrieval strategy: `dpr` / `hybrid_rrf` / `ppr` |
| `top_k_chunks` | 3 | Number of results to retrieve |
| `top_k_facts` | 5 | Number of facts to retrieve |
| `enable_integration` | `True` | Automatically merge related memories |
| `integration_window` | 3 | How often to check for merges |
| `enable_fact_graph` | `True` | Build knowledge graph |

### 3. Use

```bash
# Store a message
python scripts/cli_memory.py store --speaker "Alice" --text "Lena asked about dogs"

# Recall relevant memories
python scripts/cli_memory.py recall --query "What did Lena ask?"

# View the knowledge graph
python scripts/cli_memory.py facts

# Browse all memories
python scripts/cli_memory.py display

# Check stats
python scripts/cli_memory.py stats
```

---

## Python API

```python
from SEEM import SEEMSkill, SEEMConfig

skill = SEEMSkill(SEEMConfig())

# Store
mid = skill.store({"text": "Lena asked about dogs", "speaker": "Alice"})

# Recall
result = skill.recall({"text": "What did Lena ask?"}, top_k=3)
```

---

## CLI Reference

```bash
# Store
cli_memory.py store --text "message"
cli_memory.py store --speaker "Alice" --text "message"
cli_memory.py store --dialogue-id "D1:1" --speaker "Alice" --text "message"
cli_memory.py store --text "check this out" --image-path photo.jpg --image-caption "a dog"

# Recall
cli_memory.py recall --query "your question"
cli_memory.py recall --query "your question" --strategy ppr --mode pro --top-k 5

# Browse
cli_memory.py facts                  # knowledge graph
cli_memory.py facts --entity "Lena"  # filter by entity
cli_memory.py display                # detailed view
cli_memory.py view                   # compact view

# Manage
cli_memory.py stats
cli_memory.py clear --yes
```
---

## OpenClaw Skill

SEEM is packaged as an [OpenClaw](https://docs.openclaw.ai) agent skill. To install:

1. Copy the `SEEM/` directory into your workspace's `skills/` folder.
2. Set the required environment variables (`LLM_API_KEY`, `MM_ENCODER_API_KEY`) in your OpenClaw config or shell profile.
3. The agent will automatically discover the skill and use it for structured memory operations.

No additional configuration is needed. The agent reads `SKILL.md` to understand when and how to invoke store, recall, and display commands.

---

## Citation

```bibtex
@article{lu2026seem,
  title   = {Structured Episodic Event Memory},
  author  = {Zhengxuan Lu and Dongfang Li and Yukun Shi and Beilun Wang and Longyue Wang and Baotian Hu},
  journal = {arXiv preprint arXiv:2601.06411},
  year    = {2026}
}
```
