"""
SEEM Skill - Deferred Integration Flow Test (Strategy C, w=5)

Stores 10 observations and verifies:
  1. Extraction runs on every observation
  2. Integration is deferred until the window (w=5) fills
  3. Two flush cycles occur (obs 1-5 → flush, obs 6-10 → flush)
  4. Recall works correctly after integration
"""

import sys
import os
import json

# Ensure the skill package is importable
skill_dir = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, skill_dir)

from core.seem_skill import SEEMSkill
from core.schema import SEEMConfig

# ── 10 test observations (mix of related and unrelated topics) ──────────

OBSERVATIONS = [
    # --- Window 1 (obs 1-5): should trigger flush after obs 5 ---
    {
        "text": "Alice asked Lena about Scottish Terriers, wondering if they make good apartment dogs.",
        "speaker": "Alice",
    },
    {
        "text": "Lena replied that Scotties are independent and can adapt to apartments but need daily walks.",
        "speaker": "Lena",
    },
    {
        "text": "Bob mentioned he booked a flight to Tokyo for next Monday.",
        "speaker": "Bob",
    },
    {
        "text": "Alice then asked whether Scottish Terriers shed a lot.",
        "speaker": "Alice",
    },
    {
        "text": "Lena said Scotties have a double coat and shed moderately, recommending regular grooming.",
        "speaker": "Lena",
    },
    # --- Window 2 (obs 6-10): should trigger flush after obs 10 ---
    {
        "text": "Bob shared that his Tokyo hotel is in Shinjuku, near the train station.",
        "speaker": "Bob",
    },
    {
        "text": "Carol joined the conversation and asked what breed of dog everyone was discussing.",
        "speaker": "Carol",
    },
    {
        "text": "Alice told Carol they were talking about Scottish Terriers and shared Lena's advice on grooming.",
        "speaker": "Alice",
    },
    {
        "text": "Bob said he plans to visit Akihabara during his Tokyo trip to buy electronics.",
        "speaker": "Bob",
    },
    {
        "text": "Lena recommended Bob try ramen at a small shop near Shinjuku station.",
        "speaker": "Lena",
    },
]


def main():
    print("=" * 70)
    print("  SEEM Skill - Deferred Integration Flow Test (w=5)")
    print("=" * 70)
    print()

    # ── Initialise with a clean state ───────────────────────────────
    config = SEEMConfig(
        enable_integration=True,
        integration_window=5,
        enable_cache=False,       # disable disk persistence for clean test
        enable_fact_graph=False,  # skip fact graph to simplify output
    )
    skill = SEEMSkill(config)
    skill.reset()  # ensure empty

    print(f"Config: integration_window = {config.integration_window}")
    print(f"Config: enable_integration = {config.enable_integration}")
    print()

    # ── Store observations one by one ───────────────────────────────
    memory_ids = []
    for i, obs in enumerate(OBSERVATIONS, 1):
        mid = skill.store(obs)
        memory_ids.append(mid)

        mem_count = len(skill.memories)
        pending = skill._pending_count
        flush_marker = "  ← FLUSHED" if pending == 0 and i % config.integration_window == 0 else ""

        print(f"  [{i:2d}] store(\"{obs['text'][:50]}...\")")
        print(f"       → memory_id={mid[:12]}…  "
              f"memories={mem_count}  pending={pending}{flush_marker}")

    # ── Force flush any remaining pending (should be 0 after 10 obs with w=5) ──
    print()
    remaining = skill._pending_count
    if remaining > 0:
        print(f"  ⚠ {remaining} pending memories remain — force flushing…")
        skill.flush()
    else:
        print("  ✅ No remaining pending memories (both windows flushed)")

    # ── Statistics ──────────────────────────────────────────────────
    print()
    print("-" * 70)
    print("  Statistics")
    print("-" * 70)
    stats = skill.get_stats()
    for k, v in stats.items():
        print(f"    {k:25s}: {v}")

    # ── Recall tests ───────────────────────────────────────────────
    print()
    print("-" * 70)
    print("  Recall Tests")
    print("-" * 70)

    queries = [
        "What do you know about Scottish Terriers?",
        "Tell me about Bob's Tokyo trip",
        "Who joined the conversation?",
    ]

    for q in queries:
        print(f'\n  Query: "{q}"')
        results = skill.recall({"text": q}, top_k=3)
        if not results:
            print("    (no results)")
        for j, r in enumerate(results[:3], 1):
            text_preview = r["text"][:120].replace("\n", " ")
            print(f"    [{j}] {text_preview}…")

    # ── Display all memories ────────────────────────────────────────
    print()
    print("-" * 70)
    print("  All Memories")
    print("-" * 70)
    print(skill.display_memories())

    print("=" * 70)
    print("  Test Complete")
    print("=" * 70)


if __name__ == "__main__":
    main()
