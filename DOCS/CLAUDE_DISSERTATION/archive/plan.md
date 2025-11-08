# Implementation Plan: Persistent Student Model System

## Executive Summary

This plan outlines a pragmatic, phased approach to implementing the Student Model system described in the dissertation. Given your Python-centric background and automation-first mindset, I've structured this as an iterative build with clear milestones and minimal overhead.

---

## Phase 1: Core Infrastructure (Week 1)

### 1.1 Project Setup

**Goal:** Foundation with proper structure and testing

```bash
# Project structure
student-model/
├── student.py           # Main CLI tool
├── tests/
│   ├── test_cli.py
│   └── test_model.py
├── examples/
│   └── sample_model.json
├── README.md
└── .gitignore
```

**Tasks:**

- [ ] Initialize git repo
- [ ] Create `student.py` skeleton with argparse structure
- [ ] Implement JSON schema validation
- [ ] Set up pytest with basic test coverage
- [ ] Create sample model for testing

**Deliverable:** Working CLI that can initialize an empty model

**Time estimate:** 4-6 hours

### 1.2 Core Data Operations

**Goal:** Reliable model persistence

**Implement:**

- `load_model()` - with error handling for corrupt JSON
- `save_model()` - atomic writes with backup
- `initialize_model()` - create new student model
- `find_concept()` - case-insensitive search

**Critical details:**

```python
# Atomic save pattern
def save_model(model):
    model["metadata"]["last_updated"] = datetime.now().isoformat()

    # Backup existing
    if DATA_FILE.exists():
        backup = DATA_FILE.with_suffix('.json.backup')
        shutil.copy(DATA_FILE, backup)

    # Write to temp, then atomic rename
    temp = DATA_FILE.with_suffix('.json.tmp')
    with open(temp, 'w') as f:
        json.dump(model, f, indent=2)
    temp.replace(DATA_FILE)
```

**Tests:**

- Corrupt JSON recovery
- Concurrent access (if multi-process)
- Backup/restore functionality

**Deliverable:** Robust data layer with full test coverage

**Time estimate:** 3-4 hours

---

## Phase 2: Read Operations (Week 1)

### 2.1 Viewing Commands

**Goal:** Rich, informative output for context gathering

**Implement commands:**

```bash
python student.py list
python student.py show "Concept Name"
python student.py related "Concept Name"
```

**Output design considerations:**

- Use emoji for visual parsing (📊, ⚠️, 💡, 🔗)
- Format for easy copy-paste into LLM conversations
- Handle missing data gracefully
- Color coding (optional: use `colorama` if you want it)

**Example implementation:**

```python
def cmd_show(args):
    model = load_model()
    concept_key = find_concept(model, args.concept_name)

    if not concept_key:
        print(f"❌ Concept '{args.concept_name}' not found.")
        return

    concept = model["concepts"][concept_key]
    print(f"📊 Concept: {concept_key}")
    print(f"   Mastery:       {concept.get('mastery', 'N/A')}%")
    print(f"   Confidence:    {concept.get('confidence', 'N/A')}")
    print(f"   Last Reviewed: {concept.get('last_reviewed', 'Never').split('T')[0]}")

    if concept.get('struggles'):
        print(f"   ⚠️  Struggles:")
        for struggle in concept['struggles']:
            print(f"      - {struggle}")

    if concept.get('breakthroughs'):
        print(f"   💡 Breakthroughs:")
        for breakthrough in concept['breakthroughs']:
            print(f"      - {breakthrough}")
```

**Deliverable:** All read operations functional with rich output

**Time estimate:** 2-3 hours

---

## Phase 3: Write Operations (Week 1-2)

### 3.1 Basic Modification Commands

**Implement:**

```bash
python student.py add "Concept" 50 medium
python student.py update "Concept" --mastery 70 --confidence high
python student.py struggle "Concept" "description"
python student.py breakthrough "Concept" "description"
```

**Validation rules:**

- Mastery: 0-100 integer
- Confidence: low|medium|high enum
- Prevent duplicate concepts (suggest update instead)
- Prevent duplicate struggles/breakthroughs

**Implementation pattern:**

```python
def cmd_add(args):
    model = load_model()

    # Check for existing
    if find_concept(model, args.concept_name):
        print(f"❌ Concept '{args.concept_name}' already exists. Use 'update'.")
        return

    # Add new concept
    model["concepts"][args.concept_name] = {
        "mastery": args.mastery,
        "confidence": args.confidence,
        "first_encountered": datetime.now().isoformat(),
        "last_reviewed": datetime.now().isoformat(),
        "struggles": [],
        "breakthroughs": [],
        "related_concepts": []
    }

    print(f"✅ Added new concept: '{args.concept_name}'")
    save_model(model)
```

**Deliverable:** Full CRUD operations on concepts

**Time estimate:** 4-5 hours

### 3.2 Batch Operations (Overhead Reduction)

**Goal:** Minimize session-end friction

**Implement session-end helper:**

```bash
python student.py session-end \
  --update "React Hooks:70:medium" \
  --struggle "React Hooks:dependency confusion" \
  --breakthrough "React Hooks:understood cleanup"
```

This runs multiple operations atomically in one command.

**Alternative approach (if preferred):**
Shell script that takes structured input:

```bash
# session_update.sh
python student.py update "$1" --mastery "$2" --confidence "$3"
python student.py struggle "$1" "$4"
python student.py breakthrough "$1" "$5"
```

**Deliverable:** Session updates take <2 minutes

**Time estimate:** 2-3 hours

---

## Phase 4: LLM Persona Engineering (Week 2)

### 4.1 Persona Prompt Development

**Create structured prompt in markdown:**
`prompts/socratic_mentor_v1.md`

**Key sections:**

1. Core identity and goals
2. Mandatory protocol (context retrieval)
3. Diagnostic reasoning framework
4. Session structure (start/during/end)
5. Failure modes to avoid

**Critical language patterns:**

- Use "MUST" not "should" for mandatory behaviors
- Explicit protocol steps with exact commands
- Examples of good/bad interactions
- Emphasis on student model as "sacred context"

**Testing approach:**

- Create test scenarios (concept with gaps)
- Paste persona + scenario into Claude
- Verify it requests context before teaching
- Iterate on language for consistency

**Deliverable:** Persona prompt that drives desired behavior >90% of time

**Time estimate:** 4-6 hours (includes iteration)

### 4.2 Protocol Documentation

**Create user guide:**
`docs/collaboration_protocol.md`

**Contents:**

- Quick start for new users
- Session workflow walkthrough
- Example conversations (good and bad)
- Troubleshooting common issues
- Tips for effective concept naming

**Deliverable:** Clear documentation for onboarding

**Time estimate:** 2-3 hours

---

## Phase 5: Enhanced Features (Week 3)

### 5.1 Related Concepts (Prerequisite Graph)

**Implement:**

```bash
python student.py link "React Hooks" "JavaScript Closures"
python student.py unlink "React Hooks" "JavaScript Closures"
python student.py related "React Hooks"
```

**Data structure:**

```python
"concepts": {
  "React Hooks": {
    ...
    "related_concepts": ["JavaScript Closures", "React Core"]
  }
}
```

**Smart related command output:**

```
🔗 Concepts related to 'React Hooks':
   - JavaScript Closures (Mastery: 55%, Last: 2026-04-15) ⚠️  LOW
   - React Core (Mastery: 80%, Last: 2026-04-10) ✅
```

Flag low-mastery prerequisites for LLM attention.

**Deliverable:** Prerequisite tracking functional

**Time estimate:** 3-4 hours

### 5.2 Misconception Tracking

**Implement:**

```bash
python student.py misconception add "React Hooks" \
  --belief "useEffect cleanup runs every render" \
  --correction "runs before next effect or unmount"

python student.py misconception resolve "React Hooks" 0
python student.py misconception list
```

**Deliverable:** Explicit bug model tracking

**Time estimate:** 2-3 hours

---

## Phase 6: Quality of Life (Week 3-4)

### 6.1 Interactive Mode (Optional but Recommended)

**Implement REPL-style interface:**

```bash
python student.py interactive
> show React Hooks
> update React Hooks --mastery 75
> exit
```

Benefits:

- Faster iterations during session-end
- No command re-typing
- History/autocomplete (use `cmd` module)

**Implementation:**

```python
import cmd

class StudentModelREPL(cmd.Cmd):
    intro = "Student Model Interactive Mode. Type 'help' or '?'"
    prompt = '(student) '

    def do_show(self, arg):
        """Show concept: show React Hooks"""
        args = argparse.Namespace(concept_name=arg)
        cmd_show(args)

    def do_exit(self, arg):
        """Exit interactive mode"""
        return True
```

**Deliverable:** Optional interactive mode for power users

**Time estimate:** 3-4 hours

### 6.2 Export/Reporting

**Implement:**

```bash
python student.py export --format markdown > learning_report.md
python student.py stats
```

**Stats output:**

```
📈 Learning Statistics:
   Total Concepts:     12
   Avg Mastery:        64%
   High Confidence:    5
   Active Struggles:   8
   Recent Activity:    3 concepts in last 7 days
```

Useful for:

- Sharing with instructors
- Portfolio documentation
- Progress tracking

**Deliverable:** Export and stats commands

**Time estimate:** 2-3 hours

### 6.3 Validation & Maintenance

**Implement:**

```bash
python student.py validate  # Check for orphaned relations, etc.
python student.py clean     # Remove old backups
python student.py backup    # Manual backup to dated file
```

**Deliverable:** Model health tools

**Time estimate:** 2 hours

---

## Phase 7: Testing & Refinement (Week 4)

### 7.1 Real-World Usage

**Test with actual learning:**

- Pick a new concept (e.g., FastAPI, async/await)
- Use system for 2-3 real learning sessions
- Document friction points
- Measure actual overhead time

**Iteration priorities:**

1. Reduce any >30 second workflows
2. Fix unintuitive command syntax
3. Improve error messages
4. Add missing shortcuts

### 7.2 Edge Case Handling

**Test scenarios:**

- Very long struggle descriptions
- Unicode in concept names
- 100+ concepts (performance)
- Corrupted JSON recovery
- Missing data file
- Concurrent access

**Deliverable:** Robust tool for daily use

**Time estimate:** 4-6 hours

---

## Phase 8: Documentation & Release (Week 4)

### 8.1 Complete Documentation

**Create:**

- `README.md` - Quick start, installation
- `USAGE.md` - Detailed command reference
- `PROTOCOL.md` - LLM collaboration guide
- `EXAMPLES.md` - Sample workflows
- `CONTRIBUTING.md` - If open sourcing

### 8.2 Package for Distribution

**Options based on your goals:**

**Option A: Simple Distribution**

- Single `student.py` file (no dependencies)
- Users download and run
- Minimal packaging

**Option B: Package (if you want practice)**

```bash
pip install student-model-cli
```

- Create `setup.py` or `pyproject.toml`
- Publish to PyPI
- Entry point: `student` command

**Option C: Personal Use**

- Add to your dotfiles
- Alias for convenience: `alias sm='python ~/tools/student.py'`

**Deliverable:** Ready for use/sharing

**Time estimate:** 3-4 hours

---

## Total Time Estimate

- **Core implementation:** 20-30 hours
- **Enhancement features:** 10-15 hours
- **Testing & refinement:** 6-10 hours
- **Documentation:** 4-6 hours

**Total: 40-60 hours** spread over 4 weeks

---

## Risk Mitigation

### Technical Risks

**Risk:** JSON corruption during save
**Mitigation:** Atomic writes with backup (implemented in Phase 1)

**Risk:** Concept naming inconsistency
**Mitigation:** Case-insensitive search (Phase 1) + validation warnings

**Risk:** LLM doesn't follow protocol
**Mitigation:** Iterative persona testing (Phase 4), clear mandatory language

### Usage Risks

**Risk:** Session-end overhead too high
**Mitigation:** Batch operations (Phase 3), interactive mode (Phase 6)

**Risk:** Model becomes too large
**Mitigation:** Export/archive features, consider deprecating old concepts

**Risk:** User forgets to update model
**Mitigation:** Include reminders in persona, make updates rewarding

---

## Success Criteria

### Minimum Viable Product (End of Week 2)

- ✅ All CRUD operations work
- ✅ Output is readable and useful
- ✅ Persona prompt drives basic protocol
- ✅ Can complete one full learning session

### Full Feature Set (End of Week 4)

- ✅ Prerequisite tracking functional
- ✅ Session overhead <5 minutes
- ✅ System feels natural to use
- ✅ Documentation complete
- ✅ Ready for daily use or sharing

### Long-term Success

- ✅ Still using it 3 months later
- ✅ Model contains 20+ concepts
- ✅ Can demonstrate value in real learning
- ✅ Others find it useful (if shared)

---

## Next Steps

**Immediate actions:**

1. Create project directory and git repo
2. Stub out `student.py` with argparse skeleton
3. Write first test (model initialization)
4. Implement `load_model()` and `save_model()`

**First milestone (2-3 days):**

- Basic add/show/list commands working
- Can manually test a simple workflow

**First real test (1 week):**

- Use system in actual learning session
- Document what feels clunky
- Iterate based on friction points

---

## Optional Enhancements (Future)

These weren't in the dissertation but could add value:

### VS Code Extension

- Inline concept lookup
- Quick update from editor
- Prerequisite graph visualization

### Web Dashboard (Flask/HTMX)

- Visual prerequisite graph
- Progress charts
- Searchable concept browser

### Spaced Repetition Integration

- Flag concepts for review based on time decay
- Integration with Anki or similar

### LLM Integration Script

- Auto-paste context into Claude/ChatGPT
- Parse and execute session-end commands
- Reduce manual copy-paste

---

## Personal Adaptation Notes

Given your profile:

✅ **Strengths this plays to:**

- Python-first implementation (your comfort zone)
- CLI tool (terminal-friendly)
- Automation focus (reduces manual work)
- Pragmatic over perfect (MVP first)

⚠️ **Watch out for:**

- Scope creep on "nice to have" features
- Overengineering the schema
- Spending too much time on persona tuning
- Perfectionism on documentation

🎯 **Recommended approach:**

- Build Phase 1-3 in first week (core functionality)
- Test with real learning in week 2
- Only build Phase 5-6 features if you find them genuinely needed
- Keep it simple and usable

---

Would you like me to:

1. Generate the complete `student.py` skeleton with argparse structure?
2. Create the initial test suite structure?
3. Draft the Socratic Mentor persona prompt?
4. Design the prerequisite graph data structure in more detail?

Let me know which component you'd like to tackle first, and I can provide detailed implementation guidance.
