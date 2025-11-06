# Student Model: Two-Week Implementation Plan

**Conservative Estimates | Evidence-Driven | Incremental Testing**

---

## Overview

**Goal:** Build a Student Model that helps Claude maintain context about your learning across sessions.

**Method:** Run archaeological sessions first, analyze evidence, then build database schema based on real needs.

**Timeline:** 2 weeks (12-16 hours total)

---

## Phase 0: Pre-Implementation (30 min)

**Goal:** Verify everything is ready to start.

**Tasks:**
- Clone monkeytype repository
- Create session documentation folder structure
- Write down 3-5 initial questions about monorepo architecture

**Deliverable:** `CONFUSION_POINTS.md` with initial questions

**Success Criteria:**
- ✅ Repository accessible
- ✅ Folder structure created
- ✅ Specific questions documented

---

## Phase 1: Archaeological Sessions (Week 1, Days 1-4, 4-6 hours)

**Goal:** Run 2-3 archaeological sessions exploring monorepo architecture, manually tracking what happens to understanding.

### Session 1: Package Structure (1.5-2 hours)

**Investigation Flow:**
1. Form hypothesis about why multiple packages exist
2. Request and examine root-level files (package.json, lerna.json/turbo.json)
3. Request and examine package-level files (packages/*/package.json)
4. Revise hypothesis based on evidence
5. Synthesize pattern: what problem does this solve?

**Deliverable:** `SESSION_01_SUMMARY.md`

**Key Documentation:**
- Starting mastery % → Ending mastery %
- Hypotheses formed and revised
- Aha moments and misconceptions corrected
- Teaching calibration notes (too basic/just right/too advanced)

---

### Session 2: Shared Code & Type Safety (1.5-2 hours)

**Investigation Flow:**
1. Build on Session 1 understanding
2. Investigate how packages share TypeScript types
3. Examine contracts/shared package structure
4. Test understanding by finding another shared code example
5. Synthesize pattern

**Deliverable:** `SESSION_02_SUMMARY.md`

**Cross-Session Analysis:**
After documenting, compare Sessions 1 & 2:
- What teaching patterns repeat?
- What evidence types reveal mastery?
- What should Claude have remembered from Session 1?

---

### Session 3: Build & Deployment (1.5-2 hours)

**Investigation Flow:**
1. Investigate build orchestration (turbo.json/lerna.json)
2. Examine CI/CD workflows (.github/workflows/)
3. Understand deployment strategy
4. Synthesize complete picture: explain architecture end-to-end

**Deliverable:** `SESSION_03_SUMMARY.md`

**Success Criteria for Phase 1:**
- ✅ 2+ hours of investigation per session
- ✅ Mastery trajectory documented (e.g., 10% → 40% → 65% → 85%)
- ✅ 15+ learning moments captured across all sessions
- ✅ Teaching calibration notes recorded

---

## Phase 2: Pattern Analysis (Week 1, Days 5-7, 3-4 hours)

**Goal:** Analyze sessions 1-3 to understand what the Student Model needs to capture.

### Day 5: Evidence Synthesis (1.5-2 hours)

**Tasks:**
1. Review all session summaries, highlight:
   - Mastery level changes
   - Aha moments
   - Misconceptions corrected
   - Effective teaching approaches
   - Times Claude should have remembered something

2. Create `EVIDENCE_ANALYSIS.md`:
   - Mastery trajectory across sessions
   - Learning moments by type (questions/hypotheses/applications/misconceptions)
   - Teaching calibration patterns
   - Information Claude should have known from previous sessions

3. Create `SCHEMA_REQUIREMENTS.md`:
   - Required tables (justified by evidence from sessions 1-3)
   - Required fields per table
   - What we DON'T need (validated by absence)

**Deliverables:**
- `EVIDENCE_ANALYSIS.md`
- `SCHEMA_REQUIREMENTS.md`

---

### Days 6-7: Schema Design (1.5-2 hours)

**Tasks:**
1. Create `STUDENT_MODEL_SCHEMA_V01.sql` with 5 tables:
   - concepts (name, category, description, first_encountered)
   - mastery_states (concept_id, mastery_%, confidence, last_updated, current_struggle)
   - learning_events (concept_id, session_number, event_type, evidence_text, mastery_before/after)
   - misconceptions (concept_id, misconception_text, correct_understanding, resolved)
   - teaching_approaches (approach_type, effectiveness_rating, concept_id, notes)

2. Create `populate_student_model.py` template (manual population for now)

3. Create `query_student_model.py` (outputs current mastery summary)

4. Write `WEEK_1_REPORT.md`:
   - What we accomplished
   - Key findings (schema justified by data)
   - Concerns & risks
   - Go/no-go decision

**Deliverables:**
- `STUDENT_MODEL_SCHEMA_V01.sql`
- `populate_student_model.py` (template)
- `query_student_model.py`
- `WEEK_1_REPORT.md`

**Success Criteria:**
- ✅ Every table justified by actual session data
- ✅ Population workflow takes <10 minutes per session
- ✅ Clear decision: proceed or pivot?

---

## Phase 3: Student Model v0.1 (Week 2, Days 1-4, 4-5 hours)

**Goal:** Build simplest working Student Model that Claude can query at session start.

### Day 1: Database Setup (1-1.5 hours)

**Tasks:**
1. Initialize database: `sqlite3 student_model.db < STUDENT_MODEL_SCHEMA_V01.sql`
2. Manually populate data from Sessions 1-3 (SQL inserts)
3. Test query script: `python query_student_model.py`

**Expected Output:**
```
=== Student Model Summary ===

Current Mastery Levels:
- monorepo-architecture: 85% (confidence: 4/5)
- npm-workspaces: 75% (confidence: 4/5)
...

Effective Teaching Approaches:
- socratic-questioning: 4.5/5
- connect-to-python: 5.0/5
...
```

**Success Criteria:**
- ✅ Database created and populated
- ✅ Query script works
- ✅ Population takes <10 minutes

---

### Days 2-3: Test with New Confusion Point (2-3 hours)

**Tasks:**
1. Pick second confusion point (different from monorepo)
2. Run Session 4 WITH Student Model:
   - Generate context: `python query_student_model.py > session_04_context.txt`
   - Provide context to Claude at session start
   - Note when Claude references past learning appropriately
3. Document session: `SESSION_04_SUMMARY.md`
4. Populate database with Session 4 data
5. Run Session 5 (repeat process)

**Success Criteria:**
- ✅ Student Model works for different confusion point
- ✅ Claude uses model data demonstrably
- ✅ Teaching calibration improves (subjective but noticeable)

---

### Day 4: Refinement (1 hour)

**Tasks:**
1. Evaluate what's working:
   - Did Claude reference past learning appropriately?
   - Did mastery levels feel accurate?
   - What queries would be useful but aren't possible?
2. Adjust schema if needed (create v0.2)
3. Improve query scripts based on real usage

**Deliverable:** Schema v0.2 (if changes needed)

---

## Phase 4: Validation (Week 2, Days 5-6, 2-3 hours)

**Goal:** Decide if Student Model actually solves the problem better than alternatives.

### Day 5: A/B Comparison (1.5-2 hours)

**Tasks:**
1. Run Session 6 WITHOUT Student Model:
   - Only provide: project context + previous session summary
   - Time context restoration
   - Note when Claude should have known something

2. Run Session 7 WITH Student Model:
   - Load student model context
   - Time context restoration
   - Note when Claude references past learning

3. Create `MODEL_COMPARISON.md`:
   - Context restoration time: Session 6 vs 7
   - Teaching calibration rating: Session 6 vs 7
   - Times Claude asked about past learning
   - Times Claude re-explained known concepts
   - Decision: Keep, Discard, or Refine?

**Success Criteria:**
- ✅ Measurable difference in context restoration time
- ✅ Subjective improvement in teaching quality
- ✅ Clear decision on continuing

---

### Day 6: Automation & Polish (1-1.5 hours)

**If keeping the model:**

**Tasks:**
1. Enhance `populate_student_model.py`:
   - Auto-extract from structured markdown
   - Propose updates for user confirmation
2. Create `START_SESSION.md` (checklist template)
3. Update `PROJECT_CONTEXT.md` with final workflow:
   - Before session: 2 min (generate context)
   - During session: 0 overhead
   - After session: 8 min (document + populate)

**Deliverables:**
- Enhanced population script
- Session start checklist
- Updated workflow documentation

---

## Phase 5: Evaluation (Week 2, Day 7, 1-2 hours)

**Goal:** Honest assessment and planning for continued use.

### Day 7: Final Evaluation (1-2 hours)

**Tasks:**
1. Calculate success metrics:
   - Context restoration time: avg before vs after
   - Teaching calibration: avg rating before vs after
   - Learning velocity: baseline established
   - Cross-session pattern recognition: instances

2. Cost-benefit analysis:
   - Setup cost: X hours
   - Per-session overhead: Y minutes
   - Time saved per session: Z minutes
   - Break-even analysis
   - Verdict: Worth it?

3. Identify gaps & future improvements:
   - Current limitations
   - P0/P1/P2 improvements
   - What NOT to build

4. Write `TWO_WEEK_REPORT.md`:
   - Executive summary
   - What we built
   - Key findings
   - Lessons learned
   - Metrics summary
   - Decision & next steps

**Deliverable:** `TWO_WEEK_REPORT.md`

**Success Criteria:**
- ✅ Honest evaluation completed
- ✅ Metrics calculated
- ✅ Decision made on continuing
- ✅ Future roadmap identified

---

## Summary: Time Investment

| Phase | Time | Deliverables |
|-------|------|--------------|
| Phase 0 | 0.5h | Setup, confusion points |
| Phase 1 | 4-6h | 3 session summaries |
| Phase 2 | 3-4h | Evidence analysis, schema design |
| Phase 3 | 4-5h | Database, 2 test sessions |
| Phase 4 | 2-3h | A/B comparison, polish |
| Phase 5 | 1-2h | Final evaluation |
| **Total** | **15-21h** | **Complete Student Model system** |

---

## Key Principles

1. **Evidence first** - Run sessions before building schema
2. **Conservative estimates** - Assume tasks take longer
3. **Incremental testing** - Test each phase before next
4. **Fast failure detection** - Decide to pivot early if not working
5. **Working solutions over perfect architecture** - Build minimum viable version

---

## Decision Points

### End of Phase 1:
- If sessions don't generate clear learning insights → Rethink method
- If documentation takes >30 min per session → Simplify template

### End of Phase 2:
- If schema feels too complex → Reduce to 3 tables
- If evidence doesn't justify all tables → Cut unnecessary ones

### End of Phase 3:
- If population takes >15 min per session → Add automation
- If Student Model doesn't improve calibration → Consider alternatives

### End of Phase 4:
- If A/B test shows no difference → Discard system
- If overhead > time saved → Simplify or abandon

---

## Rollback Options

If Student Model doesn't deliver value:

1. **Enhanced Session Summaries** - Keep structured sections without database
2. **Basic Session Summaries** - Revert to SpeedTyper-Solo style
3. **Different Tool** - Explore Anki, Roam Research, Obsidian

---

## Version History

- **v1.0** (Nov 5, 2025) - Initial phased plan
- **v2.0** (Nov 5, 2025) - Condensed version (1640 → 400 lines)