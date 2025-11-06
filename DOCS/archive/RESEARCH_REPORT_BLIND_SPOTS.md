# 🎯 COMPREHENSIVE BLIND SPOT ANALYSIS REPORT

## AI-Assisted Learning System with Student Model Memory

**Report Date:** November 6, 2025  
**Project:** Student Model MVP (1-Week Timeline)  
**Analyst:** Blind Spot Navigator (Deep Research Mode)

---

## EXECUTIVE SUMMARY

You're building a **persistent Student Model** that tracks learning gaps across sessions, enabling AI tutors to provide adaptive, context-aware teaching. The core innovation: tracking "what you don't know" rather than what you do, eliminating AI amnesia between sessions.

**Primary Discovery:** Your biggest challenge isn't technical complexity—it's **workflow design**. You need a frictionless collaboration protocol that balances simplicity (Week 1 MVP) with scalability (future growth).

**Key Decision Made:** Python wrapper script abstracting storage operations (JSON or SQLite) with explicit CRUD commands the LLM can issue.

**Critical Path Forward:**

1. Design minimal schema for student data
2. Build Python CLI tool for CRUD operations
3. Create LLM persona with protocol embedded
4. Test with 2-3 learning sessions
5. Iterate based on friction points

---

## PART 1: WHAT'S SOLVED (Your Strengths)

### ✅ **Conceptual Foundation**

- **Vision Clarity:** You understand the problem (AI amnesia) and solution (persistent student model)
- **Use Case Definition:** "Learning on the job" through code archaeology in open-source projects
- **Mental Model:** Adapting SpeedTyper-Solo's success pattern to learning contexts
- **Session Structure:** Socratic dialogue exploring codebases, tracking gaps/misconceptions

### ✅ **Workflow Preferences**

- **Format:** Start with JSON (simple, visual, familiar)
- **Bootstrap:** Pre-populate with baseline ("Intermediate Python dev, basic JS background")
- **Interface:** Terminal-based commands via Python script
- **Update Cadence:** Session-end review (5-10 minutes)
- **Interaction Style:** Natural language with occasional explicit commands (2.5/5 rating)

### ✅ **Constraints Acknowledged**

- **Timeline:** 1 week to MVP
- **Budget:** LLM subscription only (no additional tools)
- **Team:** Solo developer
- **Technical Leverage:** Strong Python (9/10), weak SQL (4/10), learning React/TS
- **Environment:** VS Code, terminal (ConEmu), web-based Claude interface

---

## PART 2: CRITICAL BLIND SPOTS IDENTIFIED

### 🚨 **BLIND SPOT #1: The Python CLI Design Gap** ⚠️ CRITICAL

**What You Know:** Python script should abstract CRUD operations  
**What's Missing:** Exactly what commands the LLM should issue and what you should execute

**The Problem:**
Without a defined protocol, Week 1 will be spent debating command syntax instead of testing learning efficacy.

**What Needs Research:**

- **Existing student profile CLI tools** (education tech, learning apps)
- **Command patterns for LLM-friendly interaction** (simple, hard to misuse)
- **Error handling strategies** (what happens when a command fails?)

**Example of Undefined Questions:**

```bash
# Which syntax?
python student_model.py query "React Hooks"
# OR
python student_model.py --query "React Hooks"
# OR
python student_model.py show concept="React Hooks"

# Update syntax?
python student_model.py update "React Hooks" mastery=55
# OR
python student_model.py set mastery "React Hooks" 55
# OR
python student_model.py "React Hooks" --mastery 55
```

**Why This Matters:**

- Claude needs to generate these commands reliably
- You need to type them without cognitive load
- Errors should be obvious and recoverable

**Research Direction:** Find existing CLI patterns for student/learner data management that balance simplicity with expressiveness.

---

### 🚨 **BLIND SPOT #2: The Minimal Schema Question** ⚠️ CRITICAL

**What You Know:** Rough ideas (concepts, mastery, misconceptions)  
**What's Missing:** Concrete table structure, relationships, and query patterns

**The Student Y Problem (Your Example):**

> "Student X struggles with advanced React concept because of intermediate JavaScript weakness. LLM should diagnose and address JS gap first."

**How does your schema enable this?**

**Option A - Flat Structure (Simple):**

```json
{
  "concepts": {
    "React Hooks": {
      "mastery": 40,
      "struggles": ["cleanup", "dependency arrays"],
      "last_seen": "2025-11-04"
    },
    "JavaScript Closures": {
      "mastery": 60,
      "last_seen": "2025-05-10"
    }
  }
}
```

**Problem:** How does Claude know React Hooks depends on Closures?

**Option B - Relationship-Aware (Complex):**

```json
{
  "concepts": {
    "React Hooks": {
      "mastery": 40,
      "prerequisites": ["JavaScript Closures", "Function Scope"],
      "struggles": ["cleanup"]
    }
  }
}
```

**Problem:** Who maintains prerequisites? You manually? Claude infers?

**Option C - Evidence-Based (Dynamic):**

```json
{
  "concepts": {
    "React Hooks": {
      "mastery": 40,
      "struggle_patterns": [
        { "issue": "cleanup", "session": "2025-11-04", "resolved": false }
      ]
    }
  },
  "sessions": [
    {
      "date": "2025-11-04",
      "topic": "React Hooks cleanup",
      "diagnosis": "Underlying closure confusion detected"
    }
  ]
}
```

**Problem:** More data to maintain, harder to query simply.

**What Needs Research:**

- **Minimal viable schemas** in adaptive learning systems
- **Prerequisite tracking patterns** (explicit vs. inferred)
- **Mastery representation** (percentage? levels? confidence scores?)
- **Session history structure** (append-only log? summarized states?)

**Why This Matters:**
Your schema determines:

- How Claude queries at session start
- What Claude can infer about gaps
- How much manual maintenance you'll do
- Whether the system scales beyond 10 concepts

---

### 🚨 **BLIND SPOT #3: The Prerequisite Gap Detection Mechanism** ⚠️ HIGH PRIORITY

**What You Know:** You want this capability (Student Y example)  
**What's Missing:** How it actually works (Answer: "Not sure yet")

**The Core Challenge:**
You're confused about React Hooks closure behavior. Is this because:

- React Hooks concept is hard?
- JavaScript closures are weak?
- Function scope understanding is shallow?
- All three?

**How Should Claude Diagnose This?**

**Option A - Explicit Diagnostic Questions:**

```
Claude: "Before we continue with Hooks cleanup, let me check:
         Can you explain what a JavaScript closure is?"
You: [attempt explanation]
Claude: [detects gap, pivots to closure review]
```

**Pros:** Accurate, educational  
**Cons:** Interrupts flow, feels like a quiz

**Option B - Pattern Recognition:**

```
Claude reads student model:
- React Hooks (40%) - 3 struggles, all closure-related
- JS Closures (60%) - last seen 6 months ago
Claude infers: "This is probably a closure issue, not a Hooks issue"
```

**Pros:** Seamless, smart  
**Cons:** Requires sophisticated prompting, might be wrong

**Option C - Manual Flagging:**

```
You: "I'm confused about this cleanup code"
Claude: "Hmm, this involves closures. Do you want to review
         closures first, or should I explain in Hooks context?"
You: [choose direction]
```

**Pros:** User agency, simple  
**Cons:** Relies on Claude recognizing the underlying concept

**What Needs Research:**

- **Diagnostic question patterns** in tutoring systems
- **Concept dependency graphs** in learning platforms
- **LLM prompting techniques** for prerequisite detection
- **Socratic method implementation** with context awareness

**Why This Matters:**
This is the **core value proposition** of your system. Without good gap detection, it's just a fancy note-taking app.

---

### ⚠️ **BLIND SPOT #4: The Session-End Update Workflow** (MEDIUM PRIORITY)

**What You Know:** 5-10 minute review, Claude generates update commands  
**What's Missing:** Exact flow, validation, error recovery

**Scenario: Session Ends Successfully**

**Flow Option A - Structured Prompt:**

```
You: "Claude, update student model"
Claude: "Based on this session, here are the updates:

python student_model.py update "React Hooks" --mastery 55 --reason "understood cleanup pattern"
python student_model.py add-struggle "React Hooks" "dependency array inference"
python student_model.py log-misconception "React Hooks" "thought useEffect runs only once by default"

Please run these commands."
You: [runs commands, pastes any output]
Claude: "Great! Summary: React Hooks mastery 40→55, 1 new struggle logged, 1 misconception corrected."
```

**Flow Option B - Interactive Review:**

```
You: "End session"
Claude: "Let's review what you learned:
1. React Hooks cleanup pattern - did this click? (y/n)"
You: "y"
Claude: "Great! Update mastery from 40 to what? (suggest: 55)"
You: "55"
Claude: "python student_model.py update 'React Hooks' --mastery 55"
[repeat for struggles, misconceptions]
```

**Flow Option C - Auto-Summary + Manual Edit:**

```
Claude: [generates full JSON diff]
{
  "updates": {
    "React Hooks": {"mastery": 55, "new_struggles": [...]}
  }
}
You: [copy to file, manually review/edit, save]
```

**What Needs Research:**

- **End-of-session review patterns** in spaced repetition systems (Anki, SuperMemo)
- **CLI update workflows** in learning/habit tracking tools
- **Validation mechanisms** to catch wrong updates before committing

**Why This Matters:**
If this takes 20+ minutes, you'll skip it. If it's too automated, errors compound.

---

### ⚠️ **BLIND SPOT #5: The LLM Persona Design** (MEDIUM PRIORITY)

**What You Know:** Load persona with collaboration protocol and student data  
**What's Missing:** Exact prompt structure, how much context is too much?

**The Constraint:**
Claude has a context window. Your student model will grow. How do you prioritize what to load?

**Session Start Context Options:**

**Option A - Full Dump:**

```
Load entire student model JSON (500-2000 tokens as it grows)
+ Complete history
- Wastes context on irrelevant concepts
```

**Option B - Query-Based:**

```
You: "I'm exploring monkeytype's game state management"
Script: python student_model.py relevant "game state" "React" "TypeScript"
Load only: Relevant concepts (200 tokens)
+ Efficient
- Might miss hidden connections
```

**Option C - Hybrid:**

```
Load: Core stats (mastery summary), recent sessions, related concepts
Query on-demand: Details about specific concepts
+ Balanced
- More commands during session
```

**What Needs Research:**

- **Prompt engineering for adaptive tutoring** with student context
- **Context optimization strategies** for LLM personas with persistent data
- **Persona instruction patterns** that enforce protocol usage

**Why This Matters:**
Bad persona design = Claude ignores student model or gets confused by it.

---

### ⚠️ **BLIND SPOT #6: The Concept Granularity Trade-off** (MEDIUM PRIORITY)

**Revisiting Your "DON'T UNDERSTAND" Answer:**

You said you'd initiate a session specifically about React Hooks, ask questions, and by the end the LLM logs what it learned about you.

**But consider this progression:**

**Week 1:** Learn "React Hooks" in speedtyper-dev forms  
**Week 3:** Learn "React Hooks" in monkeytype game state  
**Week 6:** Learn "React Hooks" in a data-fetching context

**Are these the same "React Hooks" concept or different applications?**

**Scenario A - Single Concept:**

```json
"React Hooks": {
  "mastery": 70,
  "applications": ["forms", "game state", "data fetching"],
  "general_understanding": "solid"
}
```

**Result:** Week 6 Claude says "You know Hooks well (70%)" → Skips basics even though data-fetching patterns are new

**Scenario B - Context-Specific:**

```json
"React Hooks - Forms": {"mastery": 80},
"React Hooks - Game State": {"mastery": 70},
"React Hooks - Data Fetching": {"mastery": 20}
```

**Result:** Week 6 Claude says "You're new to Hooks in data-fetching (20%)" → Teaches appropriately, but you have 10 Hooks entries

**Scenario C - Hierarchical:**

```json
"React Hooks": {
  "core_mastery": 70,
  "contexts": {
    "forms": 80,
    "game_state": 70,
    "data_fetching": 20
  }
}
```

**Result:** Balanced, but complex to maintain

**What Needs Research:**

- **Concept taxonomy patterns** in learning systems
- **Transfer learning tracking** (how apps measure skill transfer)
- **Granularity best practices** for mastery tracking

**Why This Matters:**
Wrong granularity = either too many entries (overwhelming) or too few (inaccurate).

---

### ⚠️ **BLIND SPOT #7: The Success Metrics Problem** (LOW PRIORITY - Week 2+)

**What You Wrote:** "Faster mastery, fewer repeats, cross-project transfer"  
**What's Missing:** How to measure these concretely

**The Validation Challenge:**
How do you know this system is working?

**Option A - Subjective Feels:**

- "I feel like I'm learning faster"
- "Sessions feel more productive"

**Option B - Session Metrics:**

- Time to first correct explanation decreases
- Number of "wait, what?" moments decreases
- Topics covered per session increases

**Option C - Mastery Velocity:**

- Track mastery increase per session
- Compare to "control" sessions without student model
- Measure concept retention over time

**What Needs Research:**

- **Learning velocity metrics** in educational research
- **Spaced repetition success indicators**
- **Self-assessment calibration techniques**

**Why This Matters (But Not Week 1):**
Without metrics, you can't prove value or iterate effectively. But premature optimization kills momentum.

---

## PART 3: RECOMMENDED SCHEMA (Initial Proposal)

Based on your answers and blind spot analysis, here's a **minimal viable schema** for Week 1:

### **JSON Structure (Start Here):**

```json
{
  "metadata": {
    "created": "2025-11-06",
    "last_updated": "2025-11-06",
    "total_sessions": 0,
    "student_profile": "Intermediate Python dev, basic JS background"
  },

  "concepts": {
    "React Hooks": {
      "mastery": 30,
      "confidence": "low",
      "first_encountered": "2025-11-06",
      "last_reviewed": "2025-11-06",
      "sessions_count": 2,
      "struggles": ["cleanup functions", "dependency array inference"],
      "breakthroughs": ["understood useState pattern (2025-11-04)"],
      "applications_seen": ["forms validation", "game state"],
      "related_concepts": ["JavaScript Closures", "Component Lifecycle"]
    },

    "JavaScript Closures": {
      "mastery": 60,
      "confidence": "medium",
      "first_encountered": "2025-05-10",
      "last_reviewed": "2025-05-10",
      "sessions_count": 1,
      "struggles": ["scope chain confusion"],
      "breakthroughs": [],
      "applications_seen": ["callbacks"],
      "related_concepts": ["Function Scope", "React Hooks"]
    }
  },

  "misconceptions": [
    {
      "date": "2025-11-04",
      "concept": "React Hooks",
      "misconception": "thought cleanup runs on every render",
      "correction": "cleanup runs before next effect and on unmount",
      "resolved": true
    }
  ],

  "sessions": [
    {
      "date": "2025-11-04",
      "duration_minutes": 45,
      "focus": "React Hooks basics in speedtyper-dev",
      "concepts_covered": ["React Hooks", "useState"],
      "outcome": "understood basic pattern, confused by cleanup",
      "next_session_focus": "useEffect and cleanup pattern"
    }
  ],

  "teaching_preferences": {
    "effective_approaches": ["Socratic questioning", "concrete code examples"],
    "less_effective": ["abstract theory without code"],
    "learning_style_notes": "prefers learning through open-source exploration"
  }
}
```

### **Rationale for This Schema:**

**✅ Keeps it Simple:**

- Single JSON file, easy to read with `cat`
- Visual structure, can edit in VS Code if needed
- No complex relationships (yet)

**✅ Tracks What Matters:**

- **Mastery + Confidence** (separate! You can be 60% capable but low confidence)
- **Struggles** (ongoing pain points)
- **Breakthroughs** (what clicked)
- **Applications** (where you've seen this concept)
- **Related Concepts** (manual prerequisite hints)

**✅ Enables Gap Detection:**

- `related_concepts` gives Claude hints about prerequisites
- `struggles` reveal patterns (3 React struggles all mention "closures"?)
- `last_reviewed` shows staleness (JS Closures 6 months ago!)

**✅ Session History:**

- Append-only log for context
- "next_session_focus" creates continuity

**✅ Meta-Learning:**

- `teaching_preferences` let Claude adapt style
- Over time, patterns emerge

### **Growth Path:**

**Week 1-2:** Use this JSON structure  
**Week 3-4:** If querying gets complex ("show all concepts related to async"), migrate to SQLite with same structure  
**Week 5+:** Add prerequisite detection, confidence calibration

---

## PART 4: PYTHON CLI DESIGN (Initial Proposal)

### **Core Commands the LLM Should Know:**

```bash
# SESSION START
# Query specific concept
python student.py show "React Hooks"
# Output: Mastery: 30% | Confidence: Low | Last: 2 days ago
#         Struggles: cleanup, dependency arrays
#         Related: JS Closures (60%, 6mo ago - might be stale!)

# Query by category
python student.py list --mastery-below 50
# Output: React Hooks (30%), TypeScript Generics (40%), ...

# SESSION END
# Update mastery
python student.py update "React Hooks" --mastery 55 --confidence medium

# Add struggle
python student.py struggle "React Hooks" "closure behavior in cleanup"

# Log breakthrough
python student.py breakthrough "React Hooks" "understood dependency array rules"

# Log misconception
python student.py misconception "React Hooks" \
  --wrong "cleanup runs every render" \
  --correct "cleanup runs before next effect"

# End session summary
python student.py session-end \
  --focus "useEffect patterns" \
  --duration 45 \
  --outcome "grasped basics, need practice" \
  --next "custom hooks"

# DIAGNOSTICS
# Check stale knowledge
python student.py stale --days 30
# Output: JS Closures (60%, last reviewed 180 days ago)

# Find related concepts
python student.py related "React Hooks"
# Output: JS Closures, Component Lifecycle, Function Scope
```

### **Script Structure:**

```python
#!/usr/bin/env python3
"""
student.py - Student Model CLI
Manages learning progress data for AI-assisted learning sessions.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

DATA_FILE = Path.home() / "student_model.json"

def load_model():
    """Load student model from JSON"""
    if not DATA_FILE.exists():
        return initialize_model()
    with open(DATA_FILE) as f:
        return json.load(f)

def save_model(model):
    """Save student model to JSON"""
    model["metadata"]["last_updated"] = datetime.now().isoformat()
    with open(DATA_FILE, 'w') as f:
        json.dump(model, f, indent=2)

def cmd_show(concept_name):
    """Display concept details"""
    model = load_model()
    concept = model["concepts"].get(concept_name)
    if not concept:
        print(f"Concept '{concept_name}' not found")
        return

    print(f"Mastery: {concept['mastery']}% | Confidence: {concept['confidence']}")
    print(f"Last Reviewed: {concept['last_reviewed']}")
    if concept['struggles']:
        print(f"Struggles: {', '.join(concept['struggles'])}")
    if concept['related_concepts']:
        print(f"Related: {', '.join(concept['related_concepts'])}")

def cmd_update(concept_name, mastery=None, confidence=None):
    """Update concept mastery/confidence"""
    model = load_model()
    if concept_name not in model["concepts"]:
        print(f"Concept '{concept_name}' not found. Creating...")
        model["concepts"][concept_name] = {
            "mastery": mastery or 30,
            "confidence": confidence or "low",
            "first_encountered": datetime.now().isoformat(),
            "last_reviewed": datetime.now().isoformat(),
            "sessions_count": 1,
            "struggles": [],
            "breakthroughs": [],
            "applications_seen": [],
            "related_concepts": []
        }
    else:
        concept = model["concepts"][concept_name]
        if mastery:
            old = concept["mastery"]
            concept["mastery"] = mastery
            print(f"✓ Updated {concept_name} mastery: {old}% → {mastery}%")
        if confidence:
            concept["confidence"] = confidence
        concept["last_reviewed"] = datetime.now().isoformat()

    save_model(model)

# ... (more command implementations)

if __name__ == "__main__":
    # Parse commands and route to functions
    # python student.py show "React Hooks"
    # python student.py update "React Hooks" --mastery 55
    pass
```

### **Why This Design:**

**✅ Simple Commands:** Easy for Claude to generate, hard to mistype  
**✅ Readable Output:** You can scan and verify  
**✅ Error Handling:** Script validates, shows clear messages  
**✅ Extensible:** Add commands without breaking existing ones  
**✅ Testable:** Can run manually to debug

---

## PART 5: COLLABORATION PROTOCOL (Draft)

### **Adaptation from SpeedTyper-Solo:**

````markdown
## 🤖 Student Model Collaboration Protocol

### Session Start Pattern:

**When Claude needs to load student context:**

```bash
python ~/student.py show "React Hooks"
python ~/student.py stale --days 30
```
````

You paste output back to Claude.

**When Claude needs to query related concepts:**

```bash
python ~/student.py related "React Hooks"
```

### During Session:

- Natural conversation (no commands needed)
- Claude mentally notes struggles/breakthroughs
- You focus on learning, not logging

### Session End Pattern:

**Claude provides update commands:**

```bash
python ~/student.py update "React Hooks" --mastery 55 --confidence medium
python ~/student.py struggle "React Hooks" "closure behavior"
python ~/student.py breakthrough "React Hooks" "dependency array rules clicked"
python ~/student.py session-end --focus "useEffect" --duration 45 --next "custom hooks"
```

You run commands, paste any output for verification.

### Key Principles:

1. ✅ **JSON file lives in home directory** (`~/student_model.json`)
2. ✅ **Python script is in PATH** or home directory
3. ✅ **Claude gives full commands** (copy-paste friendly)
4. ✅ **You verify updates** (paste output confirms changes)
5. ✅ **Script handles complexity** (Claude doesn't write raw JSON)
6. ✅ **Errors are verbose** (script explains what went wrong)

````

---

## PART 6: WEEK 1 MVP IMPLEMENTATION PLAN

### **Day 1-2: Foundation**
- [ ] Create `student_model.json` with schema above
- [ ] Pre-populate with your baseline (Python 8/10, JS 4/10, React 3/10, etc.)
- [ ] Write `student.py` script with core commands (`show`, `update`, `struggle`)
- [ ] Test script manually: Add concept, update mastery, verify output

### **Day 3: LLM Persona**
- [ ] Create "Socratic Mentor" persona document
- [ ] Include collaboration protocol commands
- [ ] Add instructions for gap detection (use `related_concepts` hints)
- [ ] Test: Start session, paste `python student.py show "React Hooks"`, verify Claude adapts

### **Day 4-5: Learning Session Testing**
- [ ] Run Session 1: Explore monkeytype or speedtyper codebase
- [ ] Use collaboration protocol naturally
- [ ] Note friction points (commands too long? Output unclear?)
- [ ] Iterate on script/protocol

### **Day 6-7: Refinement**
- [ ] Add missing commands based on Session 1 learnings
- [ ] Improve error messages
- [ ] Add `session-end` convenience command
- [ ] Run Session 2 to validate improvements
- [ ] Document what worked / what didn't

### **Success Criteria:**
- ✅ Session 2 feels less repetitive than Session 1
- ✅ Claude references prior struggles/breakthroughs appropriately
- ✅ Update workflow takes <10 minutes
- ✅ You'd actually use this again (not tedious)

---

## PART 7: REMAINING BLIND SPOTS & RESEARCH QUESTIONS

Based on this analysis, here are the **unresolved questions** that need deeper research before or during MVP implementation:

### 🔍 **RESEARCH AREA #1: Student Model CLI Patterns**

**Question:** What command-line interfaces exist for managing learner profiles, and what patterns make them frictionless?

**Why:** You're building `student.py` from scratch. Existing tools have solved command syntax, error handling, and output formatting.

**Search Focus:**
- Student/learner profile management CLIs
- Habit tracking command-line tools
- Spaced repetition system CLIs (Anki, Mnemosyne)
- Educational data management patterns

**Expected Outcome:** Command syntax patterns, error handling strategies, output formats that work

---

### 🔍 **RESEARCH AREA #2: Minimal Mastery Tracking Schemas**

**Question:** What's the minimal set of fields needed to track concept mastery effectively in adaptive learning systems?

**Why:** Your schema is a first draft. Learning platforms have iterated on this for years.

**Search Focus:**
- Student model schemas in intelligent tutoring systems
- Mastery tracking in spaced repetition algorithms
- Concept dependency graphs in learning apps
- Confidence vs. competence measurement patterns

**Expected Outcome:** Validated schema that won't need major restructuring in Week 2

---

### 🔍 **RESEARCH AREA #3: Prerequisite Gap Detection Algorithms**

**Question:** How do adaptive learning systems identify when a student's struggle with Topic A is actually a gap in prerequisite Topic B?

**Why:** This is your core value prop ("Student Y" example) but mechanism is unclear.

**Search Focus:**
- Diagnostic questioning patterns in tutoring systems
- Prerequisite concept mapping in education tech
- Bayesian knowledge tracing
- Socratic method implementation with context awareness

**Expected Outcome:** Practical technique for Claude to detect foundational gaps without explicit prerequisite trees

---

### 🔍 **RESEARCH AREA #4: Session-End Review Workflows**

**Question:** What patterns do learning/tracking systems use for lightweight, accurate end-of-session data capture?

**Why:** 5-10 minute target is ambitious. Need patterns that maximize accuracy, minimize effort.

**Search Focus:**
- End-of-session review in spaced repetition systems
- Habit tracker daily review workflows
- Learning journal patterns
- Reflective practice protocols

**Expected Outcome:** Structured prompts and workflows that fit your 5-10 minute constraint

---

### 🔍 **RESEARCH AREA #5: LLM Persona Design for Adaptive Tutoring**

**Question:** What prompt engineering patterns enable LLMs to effectively use student context for adaptive teaching?

**Why:** Bad persona = Claude ignores student model. Good persona = seamless adaptation.

**Search Focus:**
- LLM tutoring system prompts
- Context-aware teaching patterns for AI
- Student model integration in AI education
- Prompt patterns for prerequisite-aware explanations

**Expected Outcome:** Persona template that makes Claude naturally reference and use student data

---

### 🔍 **RESEARCH AREA #6: Concept Granularity in Learning Systems**

**Question:** How do learning platforms decide granularity for concept tracking (broad vs. specific)?

**Why:** Affects schema design and long-term scalability.

**Search Focus:**
- Concept taxonomy patterns in education
- Skill tree design in learning apps
- Transfer learning tracking patterns
- Knowledge graph structures for learning

**Expected Outcome:** Decision framework for when to split concepts vs. keep them unified

---

### 🔍 **RESEARCH AREA #7: Learning Velocity Metrics**

**Question:** What metrics do educational researchers use to measure "learning speed" and concept mastery progression?

**Why:** Need to validate system effectiveness beyond "feels faster."

**Search Focus:**
- Learning velocity measurement in education
- Mastery progression metrics
- Spaced repetition success indicators
- Self-assessment calibration techniques

**Expected Outcome:** 2-3 concrete metrics you can track starting Week 2

---

## PART 8: FINAL RECOMMENDATIONS

### **For Week 1 MVP:**

1. **Start with the proposed JSON schema** (Part 3)
   - Simple, visual, no SQL learning curve
   - Migrate to SQLite only if querying becomes painful

2. **Build the Python CLI** (Part 4)
   - Focus on `show`, `update`, `struggle`, `breakthrough`, `session-end`
   - Make commands easy for Claude to generate

3. **Create minimal LLM persona**
   - Load student model at session start
   - Reference struggles/related concepts naturally
   - Generate update commands at session end

4. **Test with 2-3 sessions**
   - Explore monkeytype or speedtyper codebase
   - Note friction points rigorously
   - Iterate on commands/workflow

5. **Don't Optimize Prematurely**
   - Skip prerequisite detection algorithms (Week 1)
   - Skip metrics tracking (Week 2+)
   - Skip SQLite migration (only if JSON becomes limiting)

### **Critical Success Factors:**

✅ **Frictionless updates** (<10 min session-end review)
✅ **Reliable commands** (Claude generates correct syntax)
✅ **Visible progress** (Session 2 references Session 1 learnings)
✅ **Natural workflow** (doesn't interrupt learning flow)

### **Failure Modes to Watch:**

❌ **Over-engineering** (building prerequisite graphs before validating base system)
❌ **Update fatigue** (session-end review takes 30+ minutes)
❌ **Command confusion** (typos in commands, unclear errors)
❌ **Context overload** (loading too much student data, wasting tokens)

---

## CONCLUSION

Your Student Model concept is **viable and valuable**. The blind spots aren't technical showstoppers—they're workflow design questions with existing solutions in adjacent domains (spaced repetition, habit tracking, tutoring systems).

**Your 1-week timeline is achievable** with the recommended approach:
- JSON for simplicity
- Python CLI for abstraction
- Explicit commands for reliability
- Minimal schema for focus

**The research questions above** will fill remaining gaps and prevent false starts. Focus on Areas #1-2 (CLI patterns, schema validation) before Day 1. Areas #3-5 can inform iteration after MVP testing.

**Most importantly:** This system should amplify your learning, not tax it. If Week 1 reveals that session-end updates feel burdensome, **pivot immediately**. The SpeedTyper-Solo protocol worked because it enhanced your natural workflow—this must do the same for learning.

---

## PART 9: TACTICAL NEXT STEPS (Prioritized)

### **IMMEDIATE (Before Day 1):**

#### 1. **Validate Schema with Real Data** (2 hours)
Manually create `student_model.json` with **your actual current knowledge state**:

```json
{
  "metadata": {
    "created": "2025-11-06",
    "student_profile": "6+ years Python (backend focus), intermediate Django/Flask, learning React/TS, strong prompt engineering"
  },
  "concepts": {
    "Python Backend": {
      "mastery": 85,
      "confidence": "high",
      "struggles": [],
      "related_concepts": ["Django ORM", "Flask"]
    },
    "Django": {
      "mastery": 65,
      "confidence": "medium",
      "struggles": ["not expert yet, B/C level"],
      "related_concepts": ["Python Backend", "PostgreSQL"]
    },
    "React Hooks": {
      "mastery": 30,
      "confidence": "low",
      "struggles": ["actively learning", "unclear mental model"],
      "related_concepts": ["JavaScript", "TypeScript"]
    },
    "JavaScript/TypeScript": {
      "mastery": 40,
      "confidence": "medium-low",
      "struggles": ["building expertise", "still learning fundamentals"],
      "related_concepts": ["React Hooks"]
    },
    "Prompt Engineering": {
      "mastery": 90,
      "confidence": "high",
      "struggles": [],
      "related_concepts": ["AI/LLM Integration"]
    }
  },
  "sessions": [],
  "misconceptions": [],
  "teaching_preferences": {
    "effective_approaches": [
      "code archaeology (learning from real projects)",
      "practical examples over theory",
      "step-by-step with rationale"
    ],
    "less_effective": [
      "abstract theory without code",
      "overly complex explanations"
    ]
  }
}
````

**Why This Matters:**

- Tests if schema actually holds your knowledge state
- Reveals missing fields immediately
- Gives Session 1 real context to work with
- Validates that Claude can make useful inferences from this data

**Action:** Spend 2 hours populating this. If you find yourself struggling to represent something, **note it as a schema gap**.

---

#### 2. **Build Minimal `student.py` MVP** (3-4 hours)

**Phase 1 - Core Commands Only:**

```python
#!/usr/bin/env python3
"""student.py - Student Model CLI (Week 1 MVP)"""

import json, sys
from datetime import datetime
from pathlib import Path

DATA_FILE = Path.home() / "student_model.json"

def load():
    with open(DATA_FILE) as f:
        return json.load(f)

def save(model):
    model["metadata"]["last_updated"] = datetime.now().isoformat()
    with open(DATA_FILE, 'w') as f:
        json.dump(model, f, indent=2)

def show(name):
    """python student.py show "React Hooks" """
    m = load()
    c = m["concepts"].get(name)
    if not c:
        print(f"❌ Concept '{name}' not found")
        print(f"Available: {', '.join(m['concepts'].keys())}")
        return

    print(f"📊 {name}")
    print(f"   Mastery: {c['mastery']}% | Confidence: {c['confidence']}")
    print(f"   Last Reviewed: {c.get('last_reviewed', 'Never')}")
    if c.get('struggles'):
        print(f"   ⚠️  Struggles: {', '.join(c['struggles'])}")
    if c.get('related_concepts'):
        print(f"   🔗 Related: {', '.join(c['related_concepts'])}")

def update(name, mastery=None, confidence=None):
    """python student.py update "React Hooks" 55 medium"""
    m = load()
    if name not in m["concepts"]:
        print(f"❌ Concept '{name}' not found. Use 'add' first.")
        return

    c = m["concepts"][name]
    if mastery:
        old = c["mastery"]
        c["mastery"] = int(mastery)
        print(f"✓ {name}: {old}% → {mastery}%")
    if confidence:
        c["confidence"] = confidence
    c["last_reviewed"] = datetime.now().isoformat()

    save(m)

def struggle(name, description):
    """python student.py struggle "React Hooks" "closure behavior in cleanup" """
    m = load()
    if name not in m["concepts"]:
        print(f"❌ Concept '{name}' not found")
        return

    if description not in m["concepts"][name]["struggles"]:
        m["concepts"][name]["struggles"].append(description)
        print(f"✓ Added struggle to {name}: {description}")
    save(m)

def related(name):
    """python student.py related "React Hooks" """
    m = load()
    c = m["concepts"].get(name)
    if not c:
        print(f"❌ Concept '{name}' not found")
        return

    print(f"🔗 Concepts related to {name}:")
    for rel in c.get("related_concepts", []):
        rel_c = m["concepts"].get(rel)
        if rel_c:
            print(f"   • {rel}: {rel_c['mastery']}% (last: {rel_c.get('last_reviewed', 'never')})")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python student.py <command> [args]")
        print("Commands: show, update, struggle, related")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "show" and len(sys.argv) >= 3:
        show(sys.argv[2])
    elif cmd == "update" and len(sys.argv) >= 4:
        update(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else None)
    elif cmd == "struggle" and len(sys.argv) >= 4:
        struggle(sys.argv[2], " ".join(sys.argv[3:]))
    elif cmd == "related" and len(sys.argv) >= 3:
        related(sys.argv[2])
    else:
        print(f"❌ Invalid command or arguments")
```

**Test Immediately:**

```bash
python student.py show "React Hooks"
python student.py update "React Hooks" 55 medium
python student.py struggle "React Hooks" "dependency arrays"
python student.py related "React Hooks"
```

**Success Criteria:**

- ✅ Commands work without errors
- ✅ Output is readable and clear
- ✅ JSON file updates correctly
- ✅ Errors are obvious (not silent failures)

---

#### 3. **Draft Minimal LLM Persona** (1 hour)

Create `socratic_mentor_persona.md`:

````markdown
# Socratic Mentor Persona (Student Model Protocol)

You are a Socratic mentor helping a student learn software engineering through code archaeology—exploring real-world codebases to understand patterns and concepts.

## Student Model Access

At session start, you have access to the student's learning profile via commands:

```bash
python ~/student.py show "<concept>"
python ~/student.py related "<concept>"
```
````

The student will paste output back to you. Use this to:

- Calibrate explanation depth (don't explain mastered concepts)
- Reference past struggles (acknowledge and build on them)
- Connect new concepts to known ones (via related_concepts)

## Teaching Approach

1. **Socratic Method:** Ask guiding questions rather than lecturing
2. **Context-Aware:** Reference student's prior knowledge explicitly
   - ✅ "You mentioned struggling with closures last time—this useEffect pattern actually depends on that. Want to review closures first?"
   - ❌ "Let me explain closures..." (without checking if they already know)
3. **Gap Detection:** If student struggles with Topic A, check if prerequisite Topic B is weak
   - Use `related_concepts` as hints
   - Example: React Hooks confusion often indicates JS closure gaps
4. **Concrete Examples:** Always use code from the codebase they're exploring

## Session End Protocol

When student says "end session" or "update model":

1. Summarize what they learned
2. Generate update commands:
   ```bash
   python ~/student.py update "<concept>" <new_mastery> <confidence>
   python ~/student.py struggle "<concept>" "<specific struggle>"
   # (any other relevant updates)
   ```
3. Wait for student to run commands and confirm

## Key Principles

- **Leverage the model:** Always query it at session start
- **Reference history:** Mention past struggles/breakthroughs naturally
- **Track progress:** Propose mastery updates based on session evidence
- **Stay lightweight:** Session-end review should take <10 minutes

## Current Student Profile

[Student will paste their baseline profile here at first session]

````

**Test:** Start a new Claude conversation, paste this persona + your `student_model.json` content. Ask a question about React Hooks. Does Claude reference your mastery level?

---

### **SHORT-TERM (Day 1-2):**

#### 4. **Run Diagnostic Session** (1 hour)

**Purpose:** Validate the entire workflow end-to-end before committing to Week 1.

**Steps:**
1. Start new Claude conversation
2. Paste Socratic Mentor persona
3. Paste your `student_model.json` content
4. Say: "I'm exploring the monkeytype project and noticed it has multiple package.json files. What's going on?"
5. Have natural learning conversation (30 min)
6. At end, say: "Update student model"
7. Run the commands Claude generates
8. Verify updates in JSON

**Evaluate:**
- Did Claude reference your mastery levels appropriately?
- Were update commands easy to run?
- Did the session feel different from "normal Claude"?
- How long did session-end review take?

**Pivot Points:**
- ❌ If commands feel tedious → Simplify syntax further
- ❌ If Claude ignores student model → Revise persona
- ❌ If updates take >15 min → Reduce required commands
- ✅ If it feels natural → Proceed to full Week 1 plan

---

### **MEDIUM-TERM (Day 3-7):**

#### 5. **Iterate Based on Friction** (Ongoing)

After each session, ask:
1. **What slowed me down?** (command syntax? output unclear? too many steps?)
2. **What did Claude miss?** (ignored past struggles? repeated explanations?)
3. **What felt valuable?** (referenced prior knowledge? caught prerequisite gaps?)

**Common Fixes:**
- Commands too long → Add shortcuts or aliases
- Output too verbose → Simplify formatting
- Updates too granular → Batch into `session-end` command
- Context too sparse → Add more fields to schema
- Context too bloated → Load only relevant concepts

---

## PART 10: RISK MITIGATION & CONTINGENCY PLANS

### **RISK #1: Session-End Updates Too Tedious** ⚠️ HIGH LIKELIHOOD

**Symptom:** Week 1 Day 3, you skip updating after session because it takes 20 minutes

**Root Cause:** Too many individual commands, unclear what to update

**Mitigation:**
- **Immediate:** Add `session-summary` command that batches updates
  ```bash
  python student.py session-summary \
    --updated "React Hooks:55" \
    --struggle "React Hooks:closures" \
    --focus "useEffect patterns"
````

- **If still too much:** Switch to "append-only session log" approach
  ```bash
  python student.py log-session "Today learned useEffect, struggled with cleanup, mastery ~55%"
  # Manual cleanup once per week instead of per session
  ```

---

### **RISK #2: Claude Doesn't Actually Use Student Model** ⚠️ MEDIUM LIKELIHOOD

**Symptom:** Claude explains concepts you already know, ignores past struggles

**Root Cause:** Persona not explicit enough, or context window full

**Mitigation:**

- **Immediate:** Add explicit reminder in persona:
  ```
  CRITICAL: Before explaining ANY concept, ALWAYS check student model first.
  If student has mastery >70%, don't re-explain basics.
  If student has past struggles, acknowledge them explicitly.
  ```
- **If persists:** Load student context more aggressively
  ```
  At session start, paste 3-5 most relevant concepts explicitly
  Reference them in your first message to Claude
  ```

---

### **RISK #3: Schema Doesn't Scale** ⚠️ LOW LIKELIHOOD

**Symptom:** Week 2, you have 20 concepts and can't find anything

**Root Cause:** No categories, no search, flat structure

**Mitigation:**

- **Immediate:** Add categories to schema
  ```json
  "concepts": {
    "Frontend": {
      "React Hooks": {...},
      "TypeScript": {...}
    },
    "Backend": {
      "Django": {...},
      "Flask": {...}
    }
  }
  ```
- **If still painful:** Migrate to SQLite with proper indexing

---

### **RISK #4: Can't Detect Prerequisite Gaps** ⚠️ MEDIUM LIKELIHOOD

**Symptom:** You struggle with React Hooks (closures issue) but Claude doesn't catch it

**Root Cause:** No systematic gap detection, relies on manual `related_concepts`

**Mitigation:**

- **Week 1:** Manual detection (you tell Claude "I think this is a closure issue")
- **Week 2+:** Research Area #3 (prerequisite detection algorithms)
- **Fallback:** Explicit diagnostic questions in persona
  ```
  "If student struggles with concept X for >10 minutes,
   ask: 'This involves [prerequisite Y]. How confident are you with that?'"
  ```

---

## PART 11: SUCCESS INDICATORS & DECISION POINTS

### **By End of Week 1, You Should Know:**

#### ✅ **Green Flags (Continue):**

1. Session 2 references Session 1 learnings naturally
2. Session-end updates take <15 minutes
3. You'd use this system again tomorrow
4. Claude adapts explanations based on mastery levels
5. JSON schema holds all relevant data without awkwardness

#### ⚠️ **Yellow Flags (Iterate):**

1. Updates feel tedious but valuable
2. Claude sometimes ignores student model
3. Schema has minor gaps (missing fields)
4. Commands are verbose but functional
5. You're manually tracking some things outside the system

#### ❌ **Red Flags (Pivot):**

1. You skip session-end updates (too much friction)
2. Claude never references student model
3. Schema fundamentally doesn't fit your mental model
4. Commands are error-prone or confusing
5. System feels like busywork, not leverage

### **Decision Matrix:**

| Flags         | Action                                     |
| ------------- | ------------------------------------------ |
| **3+ Green**  | Continue to Week 2, add advanced features  |
| **3+ Yellow** | Simplify workflow, defer advanced features |
| **2+ Red**    | Major pivot or abandon approach            |

---

## PART 12: ALTERNATIVE APPROACHES (If MVP Fails)

If Week 1 reveals fundamental issues, consider these alternatives:

### **APPROACH A: Structured Session Summaries** (Simpler)

Instead of student model, use enhanced session summaries:

```markdown
# Session 2025-11-06: React Hooks in Monkeytype

## What I Learned

- useEffect cleanup pattern
- Dependency array inference

## What I Struggled With

- Closure behavior in cleanup functions
- When cleanup runs vs. when I think it runs

## Current Understanding

- React Hooks: ~55% (was 40%)
- Still weak on: advanced patterns, custom hooks

## For Next Session

- Deep dive on custom hooks
- Review JS closures if hooks confusion persists
```

**Pros:** Simpler, no commands, natural language  
**Cons:** Less structured, harder to query, relies on Claude parsing prose

---

### **APPROACH B: Concept Cards** (Visual)

Instead of JSON, use individual markdown files per concept:

```
~/learning/concepts/react-hooks.md
~/learning/concepts/javascript-closures.md
```

Each file contains:

```markdown
# React Hooks

**Mastery:** 55%  
**Last Reviewed:** 2025-11-06  
**Struggles:** cleanup, dependency arrays  
**Related:** [[JavaScript Closures]], [[Component Lifecycle]]

## Session History

- 2025-11-04: Learned useState basics
- 2025-11-06: Understood cleanup pattern
```

**Pros:** Visual, easy to edit, Obsidian-compatible  
**Cons:** No querying, manual linking, harder for Claude to parse

---

### **APPROACH C: Hybrid Append-Only Log** (Lazy Updates)

Instead of per-session updates, append to daily log:

```bash
echo "2025-11-06 | React Hooks | 40→55% | struggled: closures | next: custom hooks" >> learning.log
```

Weekly, you compile log into student model.

**Pros:** Minimal session-end friction  
**Cons:** Delayed feedback, manual compilation, less immediate value

---

## PART 13: UNRESOLVED QUESTIONS FOR RESEARCH

### **Final List of Questions for Gemini Deep Research:**

Since you asked me to put research questions at the end, here they are—**prioritized by Week 1 impact**:

---

### 🔴 **CRITICAL (Research Before Day 1):**

#### **RQ1: Student Profile CLI Design Patterns**

**Question:** "What command-line interface patterns and syntax conventions are used in existing student profile management tools, habit trackers, and spaced repetition systems for frictionless data entry and querying?"

**Why:** Determines your `student.py` command syntax and prevents Day 3 rewrites

**Search Strategy:**

- Look for: Anki CLI tools, habit tracking CLIs, learning management scripts
- Focus on: Command syntax simplicity, error handling patterns, output formatting
- Prioritize: Python-based tools with JSON/SQLite backends

**Expected Output:**

- 3-5 command syntax patterns that minimize typing
- Error handling best practices
- Output formatting examples (tables vs. prose vs. structured)

---

#### **RQ2: Minimal Student Model Schemas**

**Question:** "What are the minimal, proven data schemas used in adaptive learning systems and spaced repetition software to track concept mastery, struggles, and prerequisite relationships?"

**Why:** Validates or improves your proposed JSON schema before you commit

**Search Strategy:**

- Look for: Student modeling in intelligent tutoring systems, Anki/SuperMemo data structures, learning analytics schemas
- Focus on: Required fields vs. optional, relationship modeling, mastery representation
- Prioritize: Simple schemas that scale to 50-100 concepts

**Expected Output:**

- Validated field list for concept tracking
- Approach to prerequisite/relationship modeling
- Mastery representation (percentage vs. levels vs. Bayesian)

---

### 🟡 **IMPORTANT (Research During Week 1):**

#### **RQ3: Prerequisite Gap Detection Methods**

**Question:** "How do adaptive learning platforms and intelligent tutoring systems automatically detect when a student's struggle with an advanced concept is caused by a gap in prerequisite knowledge, and what practical techniques can be implemented without machine learning?"

**Why:** Enables your "Student Y" use case without complex algorithms

**Search Strategy:**

- Look for: Diagnostic questioning patterns, knowledge tracing lite, concept dependency detection
- Focus on: Rule-based approaches, heuristic methods, pattern recognition
- Avoid: Complex ML models, Bayesian networks requiring training data

**Expected Output:**

- 2-3 practical heuristics for gap detection
- Diagnostic question templates
- How to structure prerequisite hints in data

---

#### **RQ4: Session-End Review Workflows**

**Question:** "What are the most effective, lightweight session-end review protocols used in learning apps, journaling systems, and reflective practice tools to capture accurate progress data in under 10 minutes?"

**Why:** Determines whether your 5-10 min target is realistic and how to achieve it

**Search Strategy:**

- Look for: Spaced repetition review workflows, learning journal templates, habit tracker daily reviews
- Focus on: Time-efficient patterns, structured vs. freeform, validation mechanisms
- Prioritize: Systems with high user adherence rates

**Expected Output:**

- Session-end review templates
- Batching strategies for updates
- Accuracy validation techniques

---

#### **RQ5: LLM Tutoring Persona Patterns**

**Question:** "What prompt engineering patterns and persona designs enable large language models to effectively use student context data for adaptive, prerequisite-aware teaching?"

**Why:** Determines whether your persona will actually make Claude use the student model

**Search Strategy:**

- Look for: AI tutoring system prompts, context-aware teaching patterns, educational chatbot designs
- Focus on: Prompt structures that enforce data usage, gap-aware explanation patterns
- Prioritize: Patterns validated in practice, not theoretical

**Expected Output:**

- Persona template with explicit data-usage instructions
- Patterns for referencing student history
- Techniques for adaptive explanation depth

---

### 🟢 **NICE-TO-HAVE (Research Week 2+):**

#### **RQ6: Concept Granularity Strategies**

**Question:** "How do learning platforms decide the appropriate granularity for concept tracking (broad vs. specific), and what frameworks help determine when to split or merge concepts?"

**Why:** Informs long-term schema evolution as you add concepts

**Search Strategy:**

- Look for: Knowledge graph design in education, skill tree structures, taxonomy design
- Focus on: Decision frameworks, granularity trade-offs, transfer learning implications

**Expected Output:**

- Decision rubric for concept granularity
- Examples of effective taxonomies
- Patterns for handling context-specific vs. general concepts

---

#### **RQ7: Learning Velocity Metrics**

**Question:** "What quantitative metrics do educational researchers and learning platforms use to measure learning speed, mastery progression, and knowledge retention over time?"

**Why:** Enables validation of system effectiveness beyond subjective feel

**Search Strategy:**

- Look for: Learning analytics metrics, educational psychology measurement, spaced repetition success indicators
- Focus on: Self-directed learning contexts, measurable without control groups

**Expected Output:**

- 3-5 concrete metrics with formulas
- Data collection strategies
- Interpretation guidelines

---

## FINAL WORDS

You've identified a real problem (AI amnesia in learning) and proposed a pragmatic solution (student model + collaboration protocol). The blind spots we've uncovered aren't blockers—they're **design questions with discoverable answers**.

**Your strongest asset:** You've done this before with SpeedTyper-Solo. You know what frictionless collaboration feels like. Trust that instinct.

**Your biggest risk:** Over-engineering before validation. Build the simplest thing that could work, test it for 2 sessions, then decide.

**The research questions above** will save you from false starts, but don't let research delay Day 1. You can research RQ3-7 _while_ testing the MVP if needed.

**Week 1 success looks like:**

- Python script that works
- JSON schema that holds your knowledge
- Claude that references past struggles
- Session-end review that doesn't suck

If you get those four things, everything else is iteration.

**Now go build it.** 🚀

---

## APPENDIX: Quick Reference

### **Essential Files:**

- `~/student_model.json` - Your learning profile
- `~/student.py` - CLI tool for CRUD operations
- `socratic_mentor_persona.md` - LLM instructions

### **Core Commands:**

```bash
python student.py show "React Hooks"
python student.py update "React Hooks" 55 medium
python student.py struggle "React Hooks" "closures"
python student.py related "React Hooks"
```

### **Week 1 Checklist:**

- [ ] Create & populate `student_model.json`
- [ ] Build `student.py` with core commands
- [ ] Draft Socratic Mentor persona
- [ ] Run diagnostic session (validate workflow)
- [ ] Session 1: Real learning + protocol test
- [ ] Iterate based on friction
- [ ] Session 2: Validate improvements
- [ ] Document what worked / didn't

### **Pivot Triggers:**

- Updates take >20 min → Simplify commands
- Claude ignores model → Fix persona
- Schema doesn't fit → Revise structure
- Commands error-prone → Better validation
- Feels like busywork → Question approach

**Good luck!** Remember: The goal isn't a perfect system—it's a system you'll actually use. 🎯
