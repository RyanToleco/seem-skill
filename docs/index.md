---
layout: default
title: SEEM — Structured Episodic Event Memory
---

# 🧠 SEEM

**Structured Episodic Event Memory** for LLM agents. Built on cognitive frame theory, SEEM organizes memory hierarchically.

<p align="center">
  <a href="https://arxiv.org/abs/2601.06411"><img src="https://img.shields.io/badge/arXiv-2601.06411-b31b1b?style=flat&labelColor=555" alt="arXiv"></a>
  <a href="https://github.com"><img src="https://img.shields.io/badge/github-SEEM-181717?style=flat&labelColor=555&logo=github&logoColor=white" alt="GitHub"></a>
  <a href="#"><img src="https://img.shields.io/badge/license-MIT-2EA44F?style=flat&labelColor=555" alt="License"></a>
  <a href="#"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat&labelColor=555" alt="PRs Welcome"></a>
</p>

---

## Paper Highlights

Current LLM memory relies on static retrieval. SEEM introduces a structured alternative:

- **Beyond Static RAG** — instead of passive document retrieval, SEEM builds cognitive-inspired memory structures
- **Hierarchical Architecture** — relational facts live in a graph layer while narratives progress through dynamic episodic memory
- **Episodic Event Frames (EEFs)** — conversation streams become structured frames with precise provenance tracking
- **Reverse Provenance Expansion (RPE)** — fragmented evidence gets reconstructed into coherent narrative context
- **Agentic Associative Fusion** — cross-layer linking connects related information dynamically

---

## Key Advantages

| Advantage | Why It Matters |
|-----------|----------------|
| **Cognitive-Inspired Design** | Frame theory underpins the structure, mirroring human memory organization instead of flat storage |
| **Dual-Layer Architecture** | Facts reside in graph memory while narratives flow through episodic memory, each layer purpose-built |
| **Provenance-Aware** | Source pointers attach to every memory, so you always know where information originated |
| **Automatic Consolidation** | Related events self-merge into coherent summaries without manual intervention |
| **Native Graph Retrieval** | Relationships become navigable paths — ask "who else was there?" or "what happened before?" |
| **Adjustable Recall Depth** | Choose lite summaries for speed or full context with source text when precision matters |

---

## Quick Start

### 1. Install

```bash
pip install -r requirements.txt
```

### 2. Configure

```bash
export LLM_API_KEY="sk-xxx"
export LLM_BASE_URL="https://api.deepseek.com"
export LLM_MODEL="deepseek-chat"

export MM_ENCODER_API_KEY="sk-xxx"
export MM_ENCODER_BASE_URL="https://api.siliconflow.cn/v1"
export MM_ENCODER_MODEL="Qwen/Qwen3-Embedding-8B"
```

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

## Retrieval

SEEM defaults to **graph-based retrieval (PPR)** — following relationship paths through the knowledge graph to surface contextually relevant information.

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

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `retrieve_strategy` | `ppr` | Retrieval strategy: `dpr` / `hybrid_rrf` / `ppr` |
| `top_k_chunks` | 3 | Number of results to retrieve |
| `top_k_facts` | 5 | Number of facts to retrieve |
| `enable_integration` | `True` | Automatically merge related memories |
| `integration_window` | 3 | How often to check for merges |
| `enable_fact_graph` | `True` | Build knowledge graph |

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

