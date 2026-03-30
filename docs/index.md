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

## Why SEEM? Redefining Long-Term AI Memory

Most AI agents "forget" or lose context during long conversations because they rely on fragmented, flat memory systems. SEEM (Structured Episodic Event Memory) changes the game by giving LLMs a human-like, dual-layer memory. Instead of just searching for random text snippets, SEEM organizes information into a Graph Memory Layer for rock-solid facts and an Episodic Memory Layer to track the "story" of the interaction. This ensures your agent remains logically consistent and contextually aware, no matter how long the session lasts.

SEEM consistently outperforms strong baselines across long-term dialogue understanding, complex reasoning, and logical consistency tasks.

| Benchmark | Metric | SEEM | A-MEM | NV-Embed-v2 |
|-----------|--------|:-----------:|:-----:|:-----------:|
| LongMemEval | Accuracy (%) | **65.0** | 55.2 | 58.4 |
| LoCoMo | F1 Score | **61.1** | 44.6 | 57.9 |
| LoCoMo | LLM-Judge (J) | **78.0** | 61.9 | 74.7 |

The secret to SEEM’s performance lies in its ability to reconstruct the "big picture." While other frameworks struggle with scattered evidence, our Reverse Provenance Expansion (RPE) mechanism allows the agent to pull in the full narrative context from just a single clue.

## Memory Representation Showcase

### Memory Summary

Each memory entry is anchored by a concise **summary** that captures the core narrative. Attached to the summary is **provenance metadata** — speaker, timestamp range, involved entities, and links to the original source utterances.

<p align="center">
  <img src="figs/Memory_Summary.png" width="85%" alt="Memory Summary Example">
  <br>
  <em>A memory summary with its associated provenance metadata.</em>
</p>

### Episodic Event

Within each memory, individual **events** are extracted with six dedicated slots: *participants*, *action*, *time*, *location*, *reason*, and *method*. The action slot captures only the core occurrence, while temporal, spatial, and causal details occupy their own slots.

<p align="center">
  <img src="figs/Memory_Event.png" width="85%" alt="Episodic Event Example">
  <br>
  <em>An extracted event with six dedicated slots.</em>
</p>

### Semantic Facts

Events are further decomposed into **relational facts** — triples that connect entities through predicates. These facts form a knowledge graph linking entities across memories, enabling graph-aware retrieval over relational structures.

<p align="center">
  <img src="figs/Semantic_Facts.png" width="85%" alt="Semantic Facts Example">
  <br>
  <em>Relational facts extracted from events, forming a cross-memory knowledge graph.</em>
</p>

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

## Python API

```python
from SEEM import SEEMSkill, SEEMConfig

skill = SEEMSkill(SEEMConfig())

# Store
mid = skill.store({"text": "Lena asked about dogs", "speaker": "Alice"})

# Recall
result = skill.recall({"text": "What did Lena ask?"}, top_k=3)
```

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

## OpenClaw Skill

SEEM is packaged as an [OpenClaw](https://docs.openclaw.ai) agent skill. To install:

1. Copy the `SEEM/` directory into your workspace's `skills/` folder.
2. Set the required environment variables (`LLM_API_KEY`, `MM_ENCODER_API_KEY`) in your OpenClaw config or shell profile.
3. The agent will automatically discover the skill and use it for structured memory operations.

No additional configuration is needed. The agent reads `SKILL.md` to understand when and how to invoke store, recall, and display commands.

## Citation

```bibtex
@article{lu2026seem,
  title   = {Structured Episodic Event Memory},
  author  = {Zhengxuan Lu and Dongfang Li and Yukun Shi and Beilun Wang and Longyue Wang and Baotian Hu},
  journal = {arXiv preprint arXiv:2601.06411},
  year    = {2026}
}
```
