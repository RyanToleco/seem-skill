"""
SEEM Skill - Full Flow Test (w=5, persistence ON)

Resets all memory, stores 10 observations with disk persistence,
then verifies data survived by re-loading from disk.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.seem_skill import SEEMSkill
from core.schema import SEEMConfig

OBSERVATIONS = [
    {"text": "Alice asked Lena about Scottish Terriers, wondering if they make good apartment dogs.", "speaker": "Alice"},
    {"text": "Lena replied that Scotties are independent and can adapt to apartments but need daily walks.", "speaker": "Lena"},
    {"text": "Bob mentioned he booked a flight to Tokyo for next Monday.", "speaker": "Bob"},
    {"text": "Alice then asked whether Scottish Terriers shed a lot.", "speaker": "Alice"},
    {"text": "Lena said Scotties have a double coat and shed moderately, recommending regular grooming.", "speaker": "Lena"},
    {"text": "Bob shared that his Tokyo hotel is in Shinjuku, near the train station.", "speaker": "Bob"},
    {"text": "Carol joined the conversation and asked what breed of dog everyone was discussing.", "speaker": "Carol"},
    {"text": "Alice told Carol they were talking about Scottish Terriers and shared Lena's advice on grooming.", "speaker": "Alice"},
    {"text": "Bob said he plans to visit Akihabara during his Tokyo trip to buy electronics.", "speaker": "Bob"},
    {"text": "Lena recommended Bob try ramen at a small shop near Shinjuku station.", "speaker": "Lena"},
]

def main():
    print("=" * 70)
    print("  SEEM Full Flow Test — persistence ON, w=5")
    print("=" * 70)

    # ── Step 1: Fresh init with persistence enabled ─────────────────
    config = SEEMConfig(
        enable_integration=True,
        integration_window=5,
        enable_cache=True,        # ← persistence ON
        enable_fact_graph=False,
    )
    skill = SEEMSkill(config)

    # ── Step 2: Reset everything (clean slate) ──────────────────────
    print("\n[Step 1] Resetting all memory …")
    skill.reset()
    print(f"  memories={len(skill.memories)}  chunks={len(skill.chunk_store)}")

    # ── Step 3: Store 10 observations ───────────────────────────────
    print("\n[Step 2] Storing 10 observations …")
    for i, obs in enumerate(OBSERVATIONS, 1):
        mid = skill.store(obs)
        pending = skill._pending_count
        flush = " ← FLUSH" if pending == 0 and i % config.integration_window == 0 else ""
        print(f"  [{i:2d}] pending={pending}  mem={len(skill.memories)}{flush}  "
              f"\"{obs['text'][:55]}…\"")

    # ── Step 4: Verify disk persistence ─────────────────────────────
    print("\n[Step 3] Verifying disk persistence …")
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    files = sorted(os.listdir(data_dir)) if os.path.isdir(data_dir) else []
    print(f"  data dir: {data_dir}")
    for f in files:
        fpath = os.path.join(data_dir, f)
        size = os.path.getsize(fpath)
        print(f"    {f:35s}  {size:>8,} bytes")

    # ── Step 5: Reload from disk (simulate restart) ─────────────────
    print("\n[Step 4] Simulating restart — re-loading from disk …")
    skill2 = SEEMSkill(config)   # __init__ calls load_from_disk()
    print(f"  memories  = {len(skill2.memories)}")
    print(f"  chunks    = {len(skill2.chunk_store)}")
    print(f"  entities  = {len(skill2.entity_embeddings)}")
    print(f"  bm25_docs = {len(skill2.bm25_documents)}")

    # ── Step 6: Recall on reloaded instance ─────────────────────────
    print("\n[Step 5] Recall tests on reloaded instance …")
    queries = [
        "What do you know about Scottish Terriers?",
        "Tell me about Bob's Tokyo trip",
        "Who joined the conversation?",
    ]
    for q in queries:
        results = skill2.recall({"text": q}, top_k=3)
        print(f'\n  Q: "{q}"')
        for j, r in enumerate(results[:3], 1):
            print(f"    [{j}] {r['text'][:100].replace(chr(10),' ')}…")

    # ── Step 7: Stats ───────────────────────────────────────────────
    print("\n[Step 6] Final stats (reloaded instance):")
    for k, v in skill2.get_stats().items():
        print(f"    {k:25s}: {v}")

    print("\n" + "=" * 70)
    print("  Done")
    print("=" * 70)

if __name__ == "__main__":
    main()
