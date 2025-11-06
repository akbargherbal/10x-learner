# Implementation Plan: Persistent Student Model System
## (Revised with Workspace Context Protocol)

## Executive Summary

This plan outlines a pragmatic, phased approach to implementing the Student Model system described in the dissertation. The system maintains **strict separation of concerns**: `student.py` handles conceptual knowledge tracking, while workspace context sharing leverages native Unix tools through a battle-tested collaboration protocol.

**Key Architectural Decision:** The Student Model tracks *abstract concepts* (mastery, struggles, breakthroughs) while the Workspace Protocol provides *concrete code context* (files, grep output, directory structure). Claude synthesizes both for grounded, continuous tutoring.

---

## Phase 1: Core Infrastructure (Week 1)

### 1.1 Project Setup

**Goal:** Foundation with proper structure and testing

```bash
# Project structure
student-model/
├── student.py           # Main CLI tool (conceptual knowledge only)
├── tests/
│   ├── test_cli.py
│   └── test_model.py
├── examples/
│   └── sample_model.json
├── docs/
│   ├── student_model_usage.md       # student.py command reference
│   ├── workspace_protocol.md        # Unix tools for code context
│   └── complete_session_guide.md    # Full integrated workflow
├── README.md
└── .gitignore
```

**Tasks:**

- [ ] Initialize git repo
- [ ] Create `student.py` skeleton with argparse structure
- [ ] Implement JSON schema validation
- [ ] Set up pytest with basic test coverage
- [ ] Create sample model for testing
- [ ] Create documentation structure

**Deliverable:** Working CLI that can initialize an empty model + doc scaffolding

**Time estimate:** 4-6 hours

### 1.2 Core Data Operations

**Goal:** Reliable model persistence (conceptual data only)

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

## Phase 4: Documentation & Protocol Design (Week 2)

### 4.1 Student Model Usage Guide

**Create:** `docs/student_model_usage.md`

**Goal:** Complete reference for `student.py` commands

**Contents:**

1. Installation and setup
2. Command reference (all commands with examples)
3. JSON schema explanation
4. Best practices for concept naming
5. Troubleshooting

**Deliverable:** Self-contained command reference

**Time estimate:** 2-3 hours

### 4.2 Workspace Protocol Documentation

**Create:** `docs/workspace_protocol.md`

**Goal:** Define how learners share code context using Unix tools

**Contents:**

1. **Core Philosophy:**
   - Evidence-based investigation
   - Request-response pattern
   - No assumptions, only facts

2. **Command Patterns:**
   ```bash
   # View file contents
   cat path/to/file
   
   # Search across files
   grep -r "pattern" path/ --include="*.ext"
   
   # Locate files
   find path/ -name "*.ext"
   
   # Show directory structure
   ls -la path/
   tree path/ -L 2  # if available
   
   # File history
   git log --oneline path/to/file
   git show commit:path/to/file
   ```

3. **Investigation Workflow:**
   - Start with high-level structure (ls, find)
   - Narrow down to relevant files (grep)
   - Examine specific files (cat)
   - Trace dependencies (grep imports)

4. **Integration with Student Model:**
   - Student Model = conceptual context
   - Workspace = concrete context
   - Claude synthesizes both

5. **Example Sessions:** (Adapted from proposal)
   - Tracing React Context in monkeytype
   - Understanding JWT authentication
   - Debugging async/await patterns

**Deliverable:** Battle-tested protocol adapted for learning

**Time estimate:** 3-4 hours

### 4.3 LLM Persona Engineering

**Create:** `prompts/socratic_mentor_v1.md`

**Goal:** Persona that leverages both Student Model and Workspace Protocol

**Key sections:**

1. **Core Identity:**
   ```
   You are a Socratic programming mentor who maintains continuity
   across sessions using a persistent Student Model and investigates
   code through evidence-based workspace exploration.
   ```

2. **Mandatory Protocol - Phase 1 (Conceptual Context):**
   ```
   You MUST begin every new topic by requesting:
   
   python student.py show '<topic>'
   python student.py related '<topic>'
   
   DO NOT BEGIN TEACHING until you receive this output.
   This is your memory of the student's conceptual understanding.
   ```

3. **Mandatory Protocol - Phase 2 (Concrete Context):**
   ```
   Before explaining abstract concepts, ground them in the
   student's actual code. Request specific evidence:
   
   - "Please run: cat path/to/confusing-file.ts"
   - "Let's see the structure: ls -la src/components/"
   - "Search for usage: grep -r 'functionName' src/"
   
   NEVER assume file contents. Always request evidence.
   ```

4. **Diagnostic Reasoning Framework:**
   ```
   When student shows confusion:
   
   1. Check Student Model for related concepts with mastery <50%
   2. Hypothesize prerequisite gap explicitly
   3. Request code evidence to test hypothesis
   4. Use Socratic questions to guide discovery
   5. Connect concrete code to abstract concept
   ```

5. **Session Structure:**
   
   **Start:**
   - Request Student Model context
   - Ask what student is investigating
   - Request relevant workspace context
   
   **During:**
   - Tight question → evidence → analysis loops
   - Reference struggles/breakthroughs from model
   - Bridge concrete code to abstract concepts
   
   **End:**
   - Generate session-end commands
   - Suggest session documentation structure

6. **Explicit Memory References:**
   ```
   When you see struggles or breakthroughs in the model:
   
   ✅ "The model notes you struggled with X three weeks ago..."
   ✅ "You had a breakthrough with Y last session..."
   ✅ "Your prerequisite concept Z is at 55% mastery..."
   
   ❌ Never pretend to remember without checking the model
   ```

7. **Failure Modes to Avoid:**
   - Starting teaching without context
   - Assuming file contents
   - Providing generic explanations
   - Ignoring prerequisite gaps
   - Forgetting about logged struggles

**Deliverable:** Persona prompt that drives integrated protocol

**Time estimate:** 4-6 hours (includes iteration/testing)

### 4.4 Complete Session Guide

**Create:** `docs/complete_session_guide.md`

**Goal:** End-to-end workflow combining all components

**Contents:**

1. **Session Initialization:**
   ```bash
   # Terminal 1: Conceptual context
   cd ~/learning-projects/student-model
   python student.py show "Topic"
   python student.py related "Topic"
   # [Paste into Claude]
   
   # Terminal 2: Workspace context
   cd ~/learning-projects/actual-codebase
   # Ready for investigation commands
   ```

2. **Investigation Phase:**
   - Example dialogue showing request-response loops
   - How Claude bridges model + workspace
   - Socratic questioning patterns

3. **Session Termination:**
   ```bash
   # Update model
   cd ~/learning-projects/student-model
   python student.py session-end \
     --update "Topic:70:medium" \
     --breakthrough "Topic:description" \
     --struggle "Topic:remaining-confusion"
   
   # Document session (optional)
   code SESSION_N_topic_name.md
   ```

4. **Complete Example:** Full transcript of Session 7 (React Context API)

5. **Tips and Best Practices:**
   - When to create new concepts
   - How to name concepts consistently
   - Balancing detail vs overhead
   - Managing large prerequisite graphs

**Deliverable:** Self-contained guide for new users

**Time estimate:** 3-4 hours

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
   - JavaScript Closures (Mastery: 55%, Last: 2026-04-15) ⚠️ LOW
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

## Phase 8: Documentation & Release (Week 4)

### 8.1 Complete Documentation

**Finalize:**

- `README.md` - Quick start, philosophy, installation
- `docs/student_model_usage.md` - Complete command reference
- `docs/workspace_protocol.md` - Unix tools guide
- `docs/complete_session_guide.md` - Full integrated workflow
- `prompts/socratic_mentor_v1.md` - LLM persona
- `EXAMPLES.md` - Sample sessions with real transcripts
- `CONTRIBUTING.md` - If open sourcing

### 8.2 Package for Distribution

**Options based on your goals:**

**Option A: Simple Distribution** (Recommended for personal use)
- Single `student.py` file (no dependencies)
- Users download and run
- Minimal packaging

**Option B: Package** (If you want practice/wider sharing)
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

- **Core implementation (student.py):** 20-25 hours
- **Documentation & protocols:** 12-17 hours
- **Enhancement features:** 10-15 hours
- **Testing & refinement:** 6-10 hours

**Total: 48-67 hours** spread over 4 weeks

---

## Architecture & Separation of Concerns

### Clear Boundaries

| Component | Responsibility | Storage | Commands |
|-----------|---------------|---------|----------|
| **student.py** | Conceptual knowledge tracking | `student_model.json` | add, show, update, struggle, breakthrough, link |
| **Workspace Protocol** | Concrete code context | Terminal (ephemeral) | cat, grep, find, ls, git |
| **Claude Persona** | Synthesis & Socratic method | LLM reasoning | (persona prompt) |

### What student.py Does NOT Do

❌ Parse code files
❌ Track specific files or line numbers
❌ Maintain git integration
❌ Store code snippets
❌ Workspace-aware features
❌ Project-specific data

✅ Only tracks abstract concepts across all projects

### Why This Matters

1. **Portability:** Student Model useful across different codebases
2. **Simplicity:** Single-purpose tool, easy to maintain
3. **Flexibility:** Workspace protocol adapts to any project structure
4. **No Duplication:** Don't reinvent Unix tools

---

## Risk Mitigation

### Technical Risks

**Risk:** JSON corruption during save
**Mitigation:** Atomic writes with backup (implemented in Phase 1)

**Risk:** Concept naming inconsistency
**Mitigation:** Case-insensitive search (Phase 1) + validation warnings

**Risk:** LLM doesn't follow protocol
**Mitigation:** Iterative persona testing (Phase 4), mandatory language

**Risk:** Workspace commands fail (permissions, missing files)
**Mitigation:** Document error handling patterns, teach graceful recovery

### Usage Risks

**Risk:** Session-end overhead too high
**Mitigation:** Batch operations (Phase 3), interactive mode (Phase 6)

**Risk:** Model becomes too large
**Mitigation:** Export/archive features, consider deprecating old concepts

**Risk:** User forgets to update model
**Mitigation:** Include reminders in persona, make updates rewarding

**Risk:** Workspace commands feel clunky
**Mitigation:** Provide common command templates in docs, shell aliases

---

## Success Criteria

### Minimum Viable Product (End of Week 2)

- ✅ All CRUD operations work
- ✅ Output is readable and useful
- ✅ Workspace protocol documented
- ✅ Persona prompt drives both protocols
- ✅ Can complete one full learning session with both systems

### Full Feature Set (End of Week 4)

- ✅ Prerequisite tracking functional
- ✅ Student Model overhead <5 minutes
- ✅ Workspace commands feel natural
- ✅ System feels natural to use
- ✅ Documentation complete (all 4 docs)
- ✅ Ready for daily use or sharing

### Long-term Success

- ✅ Still using it 3 months later
- ✅ Model contains 20+ concepts
- ✅ Workspace protocol is second nature
- ✅ Can demonstrate value in real learning
- ✅ Others find it useful (if shared)

---

## Next Steps

**Immediate actions:**

1. Create project directory and git repo
2. Set up docs/ and prompts/ directories
3. Stub out `student.py` with argparse skeleton
4. Write first test (model initialization)
5. Draft skeleton for `workspace_protocol.md`

**First milestone (2-3 days):**

- Basic add/show/list commands working
- Workspace protocol document drafted
- Can manually test a simple workflow

**First real test (1 week):**

- Use complete integrated system in actual learning session
- Document what feels clunky in BOTH protocols
- Iterate based on friction points

---

## Personal Adaptation Notes

Given your profile:

✅ **Strengths this plays to:**
- Python-first implementation (your comfort zone)
- CLI tool (terminal-friendly)
- Unix tools (you already know grep, cat, find)
- Automation focus (reduces manual work)
- Pragmatic over perfect (MVP first)

⚠️ **Watch out for:**
- Scope creep on "nice to have" features
- Overengineering the schema
- Spending too much time on persona tuning
- Perfectionism on documentation
- Adding workspace features to student.py (resist!)

🎯 **Recommended approach:**
- Build Phase 1-3 in first week (core functionality)
- Draft all 4 docs in parallel (Phase 4)
- Test with real learning in week 2 using BOTH protocols
- Only build Phase 5-6 features if genuinely needed
- Keep both systems simple and single-purpose

---

## Appendix: Example Session Flow

### Complete Integrated Workflow

**Session 7: Understanding React Context API in Monkeytype**

```bash
# PHASE 1: Conceptual Context
terminal1:~/student-model$ python student.py show "React Context API"
terminal1:~/student-model$ python student.py related "React Context API"
```

*[Paste into Claude]*

```
📊 Concept: React Context API
   Mastery:     45%
   Confidence:  low
   ⚠️  Struggles:
      - how provider connects to consumers

🔗 Concepts related to 'React Context API':
   - React Hooks (Mastery: 60%, Last: 2 days ago) ✓
   - JavaScript Closures (Mastery: 55%, Last: 1 week ago) ⚠️ LOW
```

---

**Claude:** *"I see you're at 45% mastery with Context API and struggling with the provider-consumer pattern. Before we start, what are you currently investigating?"*

**You:** *"I'm looking at monkeytype's theme system. Components use 'theme' but I can't find where it's passed as a prop."*

---

```bash
# PHASE 2: Concrete Context
terminal2:~/monkeytype$ cat packages/frontend/src/components/TestArea.tsx | grep -B 5 -A 5 "theme"
```

*[Paste output into Claude]*

---

**Claude:** *"Perfect. This is exactly where your struggle lives. I see `useContext(ThemeContext)` on line 50. What do you think useContext() does?"*

**You:** *"Gets the theme somehow?"*

**Claude:** *"Right direction. Let's find where ThemeContext is created. Can you run: `grep -r 'ThemeContext' --include='*.tsx' packages/frontend/src/`"*

---

```bash
terminal2:~/monkeytype$ grep -r 'ThemeContext' --include='*.tsx' packages/frontend/src/
```

*[Paste output]*

---

**Claude:** *"Excellent evidence! Look at App.tsx - do you see the pattern?"*

**You:** *"There's a ThemeProvider wrapping stuff..."*

**Claude:** *"Exactly! This is the provider-consumer pattern you marked as a struggle. Let's see the Provider: `cat packages/frontend/src/contexts/ThemeContext.tsx`"*

---

```bash
terminal2:~/monkeytype$ cat packages/frontend/src/contexts/ThemeContext.tsx
```

*[Paste output]*

---

**Claude:** *"Now let's connect all three pieces: [synthesis]. Does this trace clarify that connection?"*

**You:** *"Oh! The Provider puts the value in the tunnel, and useContext pulls it out?"*

**Claude:** *"Perfect! Let's update your model to capture this breakthrough."*

---

```bash
# PHASE 3: Session End
terminal1:~/student-model$ python student.py session-end \
  --update "React Context API:60:medium" \
  --breakthrough "React Context API:understood provider-consumer as tunnel metaphor by tracing ThemeContext" \
  --struggle "React Context API:when to use Context vs props - performance implications?"

terminal1:~/student-model$ code SESSION_07_context_api.md
```

---

This example shows how the two systems work together seamlessly:
- **Student Model** provided high-level conceptual context (45% mastery, known struggle)
- **Workspace Protocol** provided concrete evidence (actual code, grep results)
- **Claude** bridged both to create targeted, grounded learning experience
