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