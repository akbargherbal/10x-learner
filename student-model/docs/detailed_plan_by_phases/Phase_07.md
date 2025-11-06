## Phase 7: Testing & Refinement (Week 4)

### 7.1 Real-World Usage with Both Protocols

**Test with actual learning:**

- Pick a new concept (e.g., FastAPI, async/await)
- Use complete integrated workflow for 2-3 real sessions:
  1. Start with Student Model context
  2. Investigate with workspace commands
  3. Update model at session end
- Document friction points in BOTH protocols
- Measure actual overhead time

**Specific tests:**

- Does Student Model overhead stay <5%?
- Do workspace commands feel natural?
- Does Claude correctly synthesize both contexts?
- Are session-end updates burdensome?

**Iteration priorities:**

1. Reduce any >30 second workflows
2. Fix unintuitive command syntax
3. Improve error messages
4. Add missing shortcuts
5. Refine persona prompt if Claude deviates from protocol

### 7.2 Edge Case Handling

**Test scenarios:**

**Student Model:**

- Very long struggle descriptions
- Unicode in concept names
- 100+ concepts (performance)
- Corrupted JSON recovery
- Missing data file

**Workspace Protocol:**

- Very large file outputs (cat on 5000-line file)
- Binary files
- Permission errors
- Git repo in detached HEAD state
- Non-existent paths

**Integration:**

- Student Model shows concept, but workspace has no relevant code
- Workspace shows code for concept not in model yet
- Multiple related concepts all have low mastery

**Deliverable:** Robust system for daily use

**Time estimate:** 4-6 hours

---