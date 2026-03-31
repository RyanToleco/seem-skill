# SEEM

**Structured Episodic Event Memory** for LLM agents. Built on cognitive frame theory, SEEM organizes memory hierarchically.

<p align="center">
  <img src="docs/figs/Memory_Layer.png" width="90%" alt="SEEM Memory Architecture">
  <br>
  <em>Overview of the SEEM hierarchical memory architecture.</em>
</p>

<p align="center">
  <img src="docs/figs/Memory_Fusion.png" width="85%" alt="Memory Fusion Process">
  <br>
  <em>Overview of the associative consolidation and fusion.</em>
</p>

[arXiv:2601.06411](https://arxiv.org/abs/2601.06411) | [OpenClaw Skill](https://clawhub.ai/ryantoleco/seem-skill) | MIT License

## Key Advantages

- **Beyond Static RAG** — builds cognitive-inspired memory structures instead of passive document retrieval
- **Dual-Layer Architecture** — relational facts in graph memory, narratives in episodic memory
- **Episodic Event Frames** — conversation streams become structured frames with provenance tracking
- **Native Graph Retrieval** — PPR-based traversal over knowledge graph for multi-hop queries
- **Automatic Consolidation** — related events self-merge without manual intervention
- **Adjustable Recall Depth** — Lite (facts+episodic) / Pro (+chunks) / Max (+backfill)

## Quick Start

```bash
pip install -r SEEM/requirements.txt
```

```bash
export LLM_API_KEY="sk-xxx"
export LLM_BASE_URL="https://api.deepseek.com"
export LLM_MODEL="deepseek-chat"

export MM_ENCODER_API_KEY="sk-xxx"
export MM_ENCODER_BASE_URL="https://api.siliconflow.cn/v1"
export MM_ENCODER_MODEL="Qwen/Qwen3-Embedding-8B"
```

## CLI

```bash
# Store
python SEEM/scripts/cli_memory.py store --speaker "Alice" --text "Lena asked about dogs"

# Recall
python SEEM/scripts/cli_memory.py recall --query "What did Lena ask?"
python SEEM/scripts/cli_memory.py recall --query "..." --strategy ppr --mode pro --top-k 5

# Browse
python SEEM/scripts/cli_memory.py facts                  # knowledge graph
python SEEM/scripts/cli_memory.py facts --entity "Lena"  # filter by entity
python SEEM/scripts/cli_memory.py display                # detailed view
python SEEM/scripts/cli_memory.py view                   # compact 5W1H view

# Manage
python SEEM/scripts/cli_memory.py stats
python SEEM/scripts/cli_memory.py clear --yes
```

## Python API

```python
from SEEM import SEEMSkill, SEEMConfig

skill = SEEMSkill(SEEMConfig())

mid = skill.store({"text": "Lena asked about dogs", "speaker": "Alice"})
result = skill.recall({"text": "What did Lena ask?"}, top_k=3)
# result = {"memories": [...], "facts": [...]}
```

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `retrieve_strategy` | `ppr` | `dpr` / `hybrid_rrf` / `ppr` |
| `top_k_chunks` | 3 | Chunks to retrieve |
| `top_k_facts` | 5 | Fact triples to retrieve |
| `enable_integration` | `True` | Auto-merge related memories |
| `integration_window` | 3 | Batch size for merge checks |
| `enable_fact_graph` | `True` | Build knowledge graph |

## Citation

```bibtex
@article{lu2026seem,
  title   = {Structured Episodic Event Memory},
  author  = {Zhengxuan Lu and Dongfang Li and Yukun Shi and Beilun Wang and Longyue Wang and Baotian Hu},
  journal = {arXiv preprint arXiv:2601.06411},
  year    = {2026}
}
```
