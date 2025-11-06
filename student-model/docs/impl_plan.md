# Implementation Plan: Persistent Student Model System
## (Revised with Workspace Context Protocol)

## Executive Summary

This plan outlines a pragmatic, phased approach to implementing the Student Model system described in the dissertation. The system maintains **strict separation of concerns**: `student.py` handles conceptual knowledge tracking, while workspace context sharing leverages native Unix tools through a battle-tested collaboration protocol.

**Key Architectural Decision:** The Student Model tracks *abstract concepts* (mastery, struggles, breakthroughs) while the Workspace Protocol provides *concrete code context* (files, grep output, directory structure). Claude synthesizes both for grounded, continuous tutoring.

---

## Phase 1: Core Infrastructure (Week 1, 7-10hrs)

**Tasks:**

- Git repo + project structure
- `student.py` skeleton with argparse
- JSON schema validation + pytest setup
- Implement: `load_model()`, `save_model()`, `initialize_model()`, `find_concept()`
- Atomic saves with backup pattern

**Critical implementation:**

```python
def save_model(model):
    model["metadata"]["last_updated"] = datetime.now().isoformat()
    if DATA_FILE.exists():
        shutil.copy(DATA_FILE, DATA_FILE.with_suffix('.json.backup'))
    temp = DATA_FILE.with_suffix('.json.tmp')
    with open(temp, 'w') as f:
        json.dump(model, f, indent=2)
    temp.replace(DATA_FILE)  # Atomic
```

**Tests:** Corrupt JSON recovery, concurrent access, backup/restore

**Deliverable:** Working CLI that initializes and persists models reliably

---

## Phase 2: Read Operations (Week 1, 2-3hrs)

**Implement commands:**

```bash
python student.py list
python student.py show "Concept Name"
python student.py related "Concept Name"
```

**Output design:** Emoji for parsing (📊, ⚠️, 💡, 🔗), copy-paste friendly, graceful missing data

**Deliverable:** Rich, informative read operations

---

## Phase 3: Write Operations (Week 1-2, 6-8hrs)

**Basic commands:**

```bash
python student.py add "Concept" 50 medium
python student.py update "Concept" --mastery 70 --confidence high
python student.py struggle "Concept" "description"
python student.py breakthrough "Concept" "description"
```

**Validation:** Mastery 0-100, confidence low|medium|high, prevent duplicates

**Batch operations (session-end):**

```bash
python student.py session-end \
  --update "React Hooks:70:medium" \
  --struggle "React Hooks:dependency confusion" \
  --breakthrough "React Hooks:understood cleanup"
```

**Deliverable:** Full CRUD + session updates <2min overhead

---

## Phase 4: Documentation & Protocol (Week 2, 12-17hrs)

### 4.1 Student Model Usage Guide

**Contents:** Installation, command reference, JSON schema, naming best practices, troubleshooting

### 4.2 Workspace Protocol Documentation

**Core patterns:**

```bash
cat path/to/file                    # View contents
grep -r "pattern" path/             # Search
find path/ -name "*.ext"            # Locate
ls -la path/                        # Structure
git log --oneline path/to/file      # History
```

**Philosophy:** Evidence-based investigation, request-response pattern, no assumptions

**Integration:** Student Model = conceptual, Workspace = concrete, Claude = synthesis

### 4.3 LLM Persona Engineering

**Key sections:**

1. **Core identity:** Socratic mentor using persistent model + workspace investigation
2. **Mandatory Phase 1:** Request `student.py show/related` before teaching
3. **Mandatory Phase 2:** Request workspace evidence before explaining
4. **Diagnostic framework:** Check model → hypothesize gap → request evidence → Socratic questions
5. **Session structure:** Start (contexts) → During (tight loops) → End (generate commands)
6. **Memory references:** Explicitly cite struggles/breakthroughs from model
7. **Failure modes:** Never assume, never teach without context

### 4.4 Complete Session Guide

**Contents:** Session init, investigation phase, termination workflow, full example transcript (Session 7), tips/best practices

**Deliverable:** All 4 docs complete and integrated

---

## Phase 5: Enhanced Features (Week 3, 5-7hrs)

**Related concepts (prerequisite graph):**

```bash
python student.py link "React Hooks" "JavaScript Closures"
python student.py unlink "React Hooks" "JavaScript Closures"
python student.py related "React Hooks"  # Shows mastery levels, flags low prerequisites
```

**Misconception tracking:**

```bash
python student.py misconception add "React Hooks" \
  --belief "useEffect cleanup runs every render" \
  --correction "runs before next effect or unmount"
python student.py misconception resolve "React Hooks" 0
python student.py misconception list
```

**Deliverable:** Prerequisite graph + explicit bug model tracking

---

## Phase 6: Quality of Life (Week 3-4, 7-9hrs)

**Interactive mode (REPL):**

```bash
python student.py interactive
> show React Hooks
> update React Hooks --mastery 75
> exit
```

Benefits: Faster iterations, no re-typing, history/autocomplete

**Export/reporting:**

```bash
python student.py export --format markdown > report.md
python student.py stats  # Total concepts, avg mastery, active struggles, etc.
```

**Validation/maintenance:**

```bash
python student.py validate  # Check orphaned relations
python student.py clean     # Remove old backups
python student.py backup    # Manual dated backup
```

**Deliverable:** Power user features + model health tools

---

## Phase 7: Testing & Refinement (Week 4, 4-6hrs)

**Real-world usage:**

- Use complete workflow for 2-3 actual learning sessions
- Measure overhead (target <5%)
- Document friction in BOTH protocols
- Test integration: Does Claude synthesize contexts correctly?

**Edge cases:**

- **Student Model:** Long descriptions, Unicode, 100+ concepts, corruption, missing file
- **Workspace:** Large files (5000 lines), binaries, permissions, detached HEAD, bad paths
- **Integration:** Concept in model but no code, code exists but not in model, multiple low-mastery prerequisites

**Deliverable:** Robust system for daily use

---

## Phase 8: Documentation & Release (Week 4, 3-4hrs)

**Finalize:**

- `README.md` - Quick start, philosophy, installation
- All 4 docs polished
- `EXAMPLES.md` - Real session transcripts
- `CONTRIBUTING.md` (if open sourcing)

**Distribution options:**

- **Simple:** Single file download (recommended for personal use)
- **Package:** PyPI with `pip install student-model-cli`
- **Personal:** Add to dotfiles, alias: `alias sm='python ~/tools/student.py'`

**Deliverable:** Production-ready, shareable system

---

## Total Time: 48-67 hours over 4 weeks

---

## Architecture: Separation of Concerns

| Component              | Responsibility                | Storage              | Commands                                        |
| ---------------------- | ----------------------------- | -------------------- | ----------------------------------------------- |
| **student.py**         | Conceptual knowledge tracking | `student_model.json` | add, show, update, struggle, breakthrough, link |
| **Workspace Protocol** | Concrete code context         | Terminal (ephemeral) | cat, grep, find, ls, git                        |
| **Claude Persona**     | Synthesis + Socratic method   | LLM reasoning        | (persona prompt)                                |

**student.py does NOT:** Parse code, track files/lines, git integration, store snippets, workspace features

**Why:** Portability, simplicity, flexibility, no duplication of Unix tools

---

## Success Criteria

**MVP (Week 2):**

- All CRUD works
- All 4 docs drafted
- Both protocols functional
- One complete session tested

**Full (Week 4):**

- Prerequisites + misconceptions working
- <5min overhead
- Natural workflow
- All docs complete
- Ready for daily use

**Long-term:**

- Still using at 3 months
- 20+ concepts tracked
- Workspace protocol second nature
- Demonstrates real learning value

---

## Example Session Flow

```bash
# 1. Conceptual context
~/student-model$ python student.py show "React Context API"
# → 45% mastery, struggle: provider-consumer connection

# 2. Claude requests workspace evidence
~/monkeytype$ cat packages/frontend/src/components/TestArea.tsx | grep -B5 -A5 "theme"
~/monkeytype$ grep -r 'ThemeContext' --include='*.tsx' src/
~/monkeytype$ cat packages/frontend/src/contexts/ThemeContext.tsx

# 3. Claude bridges contexts → Socratic discovery → breakthrough

# 4. Session end
~/student-model$ python student.py session-end \
  --update "React Context API:60:medium" \
  --breakthrough "React Context API:tunnel metaphor via ThemeContext trace" \
  --struggle "React Context API:Context vs props performance?"
```

---

## Risk Mitigation

**Technical:** Atomic saves (corruption), case-insensitive search (naming), persona testing (protocol adherence), error handling docs (workspace failures)

**Usage:** Batch ops (overhead), export/archive (size), persona reminders (forgotten updates), command templates (clunky workspace)

---

## Next Steps

1. Create repo + docs/prompts structure
2. Stub `student.py` with argparse
3. Write first test (initialization)
4. Draft `workspace_protocol.md` skeleton
5. Build Phase 1-2 (2-3 days)
6. Test real session with both protocols (week 1)

**Watch out:** Scope creep, overengineering schema, perfectionism, adding workspace features to student.py (resist!)
