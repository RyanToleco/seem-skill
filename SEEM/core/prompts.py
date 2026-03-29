"""SEEM Skill Prompt Templates"""

# Episodic Memory Extraction Prompt
EPISODIC_EXTRACTION_SYSTEM_PROMPT = """You are an expert at extracting structured episodic memories from conversation turns. Each turn may contain text, timestamps, speaker information, and image descriptions.

Your task is to extract:
1. A concise 1-3 sentence summary in active voice
2. Structured events with participants, actions, time, location, reason, and method

Output STRICT JSON format with no markdown:
{
  "summary": "1-3 sentence active-voice summary",
  "events": [
    {
      "participants": ["person1", "person2"],
      "action": ["complete action with subject+verb+object"],
      "time": "ISO 8601 time or null",
      "location": "location or null",
      "reason": "why it happened or null",
      "method": "how it happened or null"
    }
  ]
}

Rules:
- SUMMARY: 1-3 concise active-voice sentences describing what happened
- EVENTS: Each event captures one distinct occurrence
  - participants: List involved people/entities (resolve coreferences); use "user" for the conversation initiator
  - action: Core action statements with subject+verb+object (keep atomic)
  - time: Resolve relative expressions ("yesterday", "last Monday", "next week") using the conversation timestamp into ISO 8601 format (e.g. "2026-03-19"). For events spanning a time period, use the START time only — the duration or range should be captured by "action" or "method" fields instead (e.g. action: ["Alice went on a week-long business trip"], time: "2026-03-16"). Use null if no time info
  - location: Specific place if stated; null otherwise
  - reason: Why it happened (clearly stated only); null otherwise
  - method: How it happened (clearly stated only); null otherwise
- Frequency/regularity expressions ("every week", "always", "twice a day") are NOT time values — put them in "method" or "reason" depending on context
- For image descriptions ([Image: ...]), extract scene participants and actions
- DO NOT invent details; prefer null over guessing
- LANGUAGE: Use the same language as the input conversation for all string values (summary, actions, location, reason, method). Do NOT translate.
- Output PURE JSON only, no markdown fences"""

# Judge & Integrate Prompt
JUDGE_INTEGRATE_SYSTEM_PROMPT = """You are a memory integration gatekeeper. Determine whether to merge a NEW memory with existing CANDIDATE memories.

CRITICAL CONSTRAINTS:
1. ACTION LIMIT: Each event's "action" ≤5 items. Split if more.
2. CHUNK LIMIT: Total chunks after integration ≤10. Reject if exceeded.
3. SLOT INTEGRITY: Keep participants/action/time/location/reason/method separate.

Integration Criteria (RELAXED):
- STRONG coherence: Same entity/topic with clear temporal or causal link (including evolving stances, status changes, follow-ups) → INTEGRATE
- MODERATE coherence: Same topic/theme, related context → INTEGRATE
- WEAK coherence: Only vague topic similarity → REJECT

Decision Process:
1. Check chunk constraint first → Reject if >10
2. Evaluate coherence: STRONG or MODERATE → Integrate; WEAK → Reject
3. Verify action count ≤5 per event; split if needed

Integration Guidelines:
- Use both structured memory (summary+events) AND original observations
- Merge structured info while preserving all original observations
- Split events by speaker/time/topic to maintain clarity
- When integrating memories that span a time range, order events chronologically and let the summary capture how the situation evolved
- LANGUAGE: Use the same language as the input memories for all string values (integrated_summary, integration_reason, actions, location, reason, method). Do NOT translate.

Output STRICT JSON (no markdown):
{
  "integrated_with_ids": [],
  "integration_reason": "",
  "coherence_level": "STRONG|MODERATE|WEAK",
  "chunk_count_check": {"new_memory_chunks": 0, "total_after_integration": 0, "exceeds_limit": false},
  "integrated_summary": "",
  "integrated_events": []
}

If integrating (integrated_with_ids non-empty):
- integrated_with_ids: List of memory_id values from the candidates you want to merge with. Copy the EXACT memory_id string from the input, e.g. ["a3f1c2d4e5b6"]
- integration_reason: Why integration helps
- coherence_level: "STRONG" or "MODERATE"
- chunk_count_check: Total chunks calculation
- integrated_summary: Merged 1-3 sentence summary
- integrated_events: Merged events (≤5 actions each, split by speaker/time/topic)

If rejecting (integrated_with_ids empty []):
- integration_reason: Why keep separate
- coherence_level: Actual level determined
- chunk_count_check: Still provide calculation
- integrated_summary: "" (empty string)
- integrated_events: [] (empty list)

Example input format:
NEW MEMORY:
- Summary: ...
- Events: [...]
- Chunk Count: N
- All Associated Original Observations (N total):
  [Obs 1] (Speaker: ..., Time: ...)
    ...
  [Obs 2] (Speaker: ..., Time: ...)
    ...

CANDIDATE [memory_id=a1b2c3d4e5f6]:
- Summary: ...
- Events: [...]
- Chunk Count: N
- All Associated Original Observations (N total):
  [Obs 1] (Speaker: ..., Time: ...)
    ...

Example output (integrating with one candidate):
{
  "integrated_with_ids": ["a1b2c3d4e5f6"],
  "integration_reason": "Both memories describe the same conversation about...",
  "coherence_level": "STRONG",
  "chunk_count_check": {"new_memory_chunks": 1, "total_after_integration": 3, "exceeds_limit": false},
  "integrated_summary": "Alice asked Lena about...",
  "integrated_events": [...]
}

Example output (rejecting):
{
  "integrated_with_ids": [],
  "integration_reason": "Different topics, no clear connection",
  "coherence_level": "WEAK",
  "chunk_count_check": {"new_memory_chunks": 1, "total_after_integration": 1, "exceeds_limit": false},
  "integrated_summary": "",
  "integrated_events": []
}"""

# Query 5W1H Extraction Prompt (for Hybrid RRF)
QUERY_5W1H_SYSTEM_PROMPT = """Extract the 5W1H elements from the following query for episodic-memory retrieval. Focus on retrievable event information rather than broad topic labels.

LANGUAGE: Use the same language as the input query for all extracted values. Do NOT translate.

Output STRICT JSON format:
{
  "who": "persons/entities mentioned or null",
  "what": "main action/event or null",
  "when": "time expression or null",
  "where": "location or null",
  "why": "reason or null",
  "how": "method or null"
}

Rules:
- who: People/entities explicitly mentioned or clearly referred to
- what: Main event/action in retrievable form (concise action phrase, not abstract topic)
- when/where/why/how: Fill only if stated or clearly implied; otherwise null
- Resolve coreferences when clear
- Preserve concrete names and time expressions from the query
- For image-related queries, include relevant visual event/entity information
- If uncertain, prefer null over guessing
- Output PURE JSON only, no markdown fences"""

# Format 5W1H Text
def format_5w1h_text(who: str, what: str, when: str, where: str, why: str, how: str) -> str:
    """Format 5W1H elements for retrieval text"""
    parts = []
    if who:
        parts.append(f"Who: {who}")
    if what:
        parts.append(f"What: {what}")
    if when:
        parts.append(f"When: {when}")
    if where:
        parts.append(f"Where: {where}")
    if why:
        parts.append(f"Why: {why}")
    if how:
        parts.append(f"How: {how}")
    
    return " | ".join(parts) if parts else ""


# ============================================================
# Batch Integration Prompt (Strategy C: single LLM call for w pending memories)
# ============================================================

BATCH_JUDGE_INTEGRATE_SYSTEM_PROMPT = """You are a memory integration gatekeeper operating in BATCH mode.
You receive multiple NEW memories (pending window) and must decide how to merge them,
both among themselves and with EXISTING candidate memories from the knowledge base.

CRITICAL CONSTRAINTS:
1. ACTION LIMIT: Each event's "action" field has ≤5 items. Split if more.
2. CHUNK LIMIT: Total chunks after any merge ≤10. Reject a merge group if exceeded.
3. SLOT INTEGRITY: Keep participants/action/time/location/reason/method separate.

Integration Criteria (RELAXED):
- STRONG coherence: Same entity/topic with clear temporal or causal link → INTEGRATE
- MODERATE coherence: Same topic/theme, related context → INTEGRATE
- WEAK coherence: Only vague topic similarity → DO NOT MERGE

You will receive:
1. PENDING MEMORIES: The w new memories that triggered this batch (each has a pending_id like "p1", "p2", ...).
2. CANDIDATE MEMORIES: Existing memories retrieved as candidates (each has a memory_id like "a1b2c3").

Your task:
- Partition all memories (pending + candidates) into merge groups.
- Each group that contains ≥2 members should produce a merged summary + events.
- Singletons (groups of 1) stay as-is; no merge output needed.
- A pending memory may merge with other pending memories AND/OR candidate memories.

Output STRICT JSON (no markdown):
{
  "merge_groups": [
    {
      "members": ["p1", "a1b2c3"],           // IDs of memories in this group
      "coherence_level": "STRONG",            // STRONG | MODERATE | WEAK
      "chunk_count_check": {"total": 3, "exceeds_limit": false},
      "integrated_summary": "Merged summary...",
      "integrated_events": [...]
    },
    {
      "members": ["p2"],                      // singleton — no merge needed
      "coherence_level": "WEAK",
      "chunk_count_check": {"total": 1, "exceeds_limit": false},
      "integrated_summary": "",
      "integrated_events": []
    }
  ]
}

Rules:
- Every pending_id (p1, p2, ...) MUST appear in exactly one merge_groups entry.
- Candidate memory_ids that are NOT mentioned in any group stay untouched.
- If a group has ≥2 members AND coherence is STRONG or MODERATE: fill integrated_summary + integrated_events.
- If a group has only 1 member OR coherence is WEAK: set integrated_summary="" and integrated_events=[].
- If chunk_count_check.exceeds_limit is true, do NOT merge; keep as singleton.
- Order events chronologically within integrated_events.
- LANGUAGE: Use the same language as the input memories for all string values (integrated_summary, integration_reason, actions, location, reason, method). Do NOT translate.
- Output PURE JSON only, no markdown fences."""


# Fact Extraction Prompt (optional, for direct fact extraction from text)
FACT_EXTRACTION_SYSTEM_PROMPT = """You are an expert at extracting structured facts from text. Extract subject-predicate-object triples that represent factual information.

Output STRICT JSON format:
{
  "facts": [
    ["subject", "predicate", "object"],
    ...
  ]
}

Rules:
- Each fact is a triple: [subject, predicate, object]. ALL three elements MUST be non-empty.
- Subject: The entity performing the action or being described
- Predicate: The relationship or action (verb phrase)
- Object: The entity, value, or concept being acted upon or described
- Scan the ENTIRE sentence for the object — it may appear before or after the predicate, or be separated by clauses. Do NOT leave object empty just because it is not adjacent to the predicate.
- If the object is implied by context but not directly stated, extract it from surrounding text.
- If the object truly cannot be determined after scanning the full passage, use "未知" as a placeholder instead of leaving it empty.
- Keep predicates concise and atomic
- Extract only explicitly stated facts, do not infer beyond what the text supports
- LANGUAGE: Use the same language as the input text for all extracted elements (subject, predicate, object). Do NOT translate.
- Output PURE JSON only, no markdown fences"""


# Fact Rerank Prompt (for reranking facts during retrieval)
FACT_RERANK_SYSTEM_PROMPT = """You are an expert fact reranker.
Given a question and a list of candidate facts (triples), select and order the most relevant facts.
LANGUAGE: Preserve the language of the input facts. Do NOT translate.
Return strict JSON only:
{
  "fact": [["subject", "predicate", "object"], ...]
}
Only keep facts that are truly useful for answering the question.
Output ONLY a valid JSON object. No extra text, no explanations, no trailing commas."""
