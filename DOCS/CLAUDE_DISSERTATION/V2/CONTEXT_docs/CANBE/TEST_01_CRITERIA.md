# Phase 4.5 Test Plan: Real-World System Validation

## Purpose

Test the complete 10x Learner system in realistic learning scenarios to validate:

1. Workflow is practical and sustainable
2. Overhead is acceptable (<5% of session time)
3. Claude persona follows protocol correctly
4. Integration of Student Model + Workspace Protocol delivers value
5. System improves learning compared to standard LLM chat

**Duration:** 3-5 hours over 2-3 days  
**Test Sessions:** 3 complete learning sessions  
**Environment:** Real learning projects, actual confusion

---

## Pre-Test Setup (15 minutes)

### Setup Checklist

**Terminal Setup:**

```bash
# Terminal 1: Student Model
cd ~/Jupyter_Notebooks/10x-learner/student-model/
python student.py info  # Verify installation

# Terminal 2: Workspace
cd ~/learning-projects/  # Or wherever your code lives
ls -la  # Verify access
```

**Browser Setup:**

- [ ] Open Claude.ai (or your preferred LLM)
- [ ] Have `docs/socratic_mentor_prompt.md` ready to paste
- [ ] Bookmark for quick access

**Documentation Ready:**

- [ ] `docs/student_model_usage.md` - command reference
- [ ] `docs/workspace_protocol.md` - investigation patterns
- [ ] `docs/complete_session_guide.md` - workflow examples

**Measurement Tools:**

- [ ] Timer app (for overhead measurement)
- [ ] Notepad for friction notes
- [ ] `TEST_RESULTS.md` template ready

---

## Test Session 1: Basic Workflow Validation

**Goal:** Verify end-to-end workflow with a simple concept  
**Duration:** 30-45 minutes  
**Concept:** Choose something at 40-60% mastery (not too easy, not too hard)  
**Example:** CSS Flexbox, Array Methods, Git Branching, React State

---

### Test 1: Step-by-Step Procedure

#### **Step 1: Open Browser (0:00)**

**Action:**

1. Open browser
2. Navigate to https://claude.ai (or your LLM of choice)
3. Start new conversation

**Success Criteria:**

- [ ] LLM loads successfully
- [ ] Ready for input

---

#### **Step 2: Initialize Student Model (0:01)**

**Terminal 1:**

```bash
cd ~/Jupyter_Notebooks/10x-learner/student-model/

# If first time testing:
python student.py init --profile "Testing 10x learner system - web developer"

# Add test concept (choose yours):
python student.py add "CSS Flexbox" 45 medium
```

**Success Criteria:**

- [ ] Concept added successfully
- [ ] No errors

**Time Check:** Should take <1 minute

---

#### **Step 3: Load Persona Prompt (0:02)**

**Browser:**

1. Open `docs/socratic_mentor_prompt.md` in text editor
2. Copy ENTIRE contents (Ctrl+A, Ctrl+C)
3. Paste into Claude

**Message to Claude:**

```
Please adopt this persona for our learning session:

[Paste entire socratic_mentor_prompt.md here]

Confirm you understand the protocol.
```

**Success Criteria:**

- [ ] Claude confirms understanding
- [ ] Acknowledges mandatory protocols
- [ ] Ready to begin

**Time Check:** Should take <2 minutes total

**⚠️ Test Point:** Does Claude acknowledge the two-phase protocol?

---

#### **Step 4: Provide Student Model Context (0:04)**

**Terminal 1:**

```bash
python student.py show "CSS Flexbox"
python student.py related "CSS Flexbox"
```

**Browser:**
Copy terminal output and paste into Claude with:

```
Here's my current state with CSS Flexbox:

[Paste student.py output]

I want to understand how flexbox works by exploring [your specific project].
I'm confused about [specific thing - e.g., "why justify-content doesn't work"].
```

**Success Criteria:**

- [ ] Claude acknowledges your mastery level (45%)
- [ ] Claude acknowledges your confidence (medium)
- [ ] Claude asks about specific file/code you're confused about
- [ ] **CRITICAL:** Claude does NOT start teaching yet

**Time Check:** Should take <1 minute

**⚠️ Test Point:** Does Claude follow "Phase 1" protocol and refuse to teach without context?

---

#### **Step 5: Provide Initial Workspace Context (0:05)**

**Terminal 2:**

```bash
cd ~/your-project/

# Show the confusing file (adjust path to your real code)
cat src/components/Layout.css
# or wherever your flexbox confusion is
```

**Browser:**
Paste output into Claude:

```
Here's the file I'm confused about:

[Paste cat output]

Lines 15-20 are what I don't understand.
```

**Success Criteria:**

- [ ] Claude analyzes the specific code
- [ ] Claude asks Socratic questions (not lectures)
- [ ] Claude points to specific lines you mentioned

**Time Check:** Should take <1 minute

**⚠️ Test Point:** Does Claude request workspace evidence before explaining?

---

#### **Step 6: Investigation Loop (0:06 - 0:30)**

**Pattern:** Claude asks question → You respond → Claude requests evidence → You provide → Repeat

**Example Exchange:**

**Claude:** "Look at line 17 with `justify-content: center`. What do you think that does?"

**You:** "I think it centers items horizontally?"

**Claude:** "Good hypothesis! Let's test it. What's the `flex-direction` on line 15?"

**You:** [Reads code] "It's `column`"

**Claude:** "Aha! Here's the key - when flex-direction is column, `justify-content` works VERTICALLY, not horizontally. Let's verify this..."

[Continue investigation]

**What to Observe:**

- [ ] Does Claude ask questions before explaining?
- [ ] Does Claude ground explanations in YOUR code?
- [ ] Does Claude request more evidence when needed?
- [ ] Does investigation feel natural or forced?

**Success Criteria:**

- [ ] You had at least 3 back-and-forth exchanges
- [ ] Claude requested workspace evidence at least once more
- [ ] You discovered something (mini-breakthrough or confirmed confusion)
- [ ] Investigation stayed focused on your code

**⚠️ Test Points:**

- Does Claude reference your code specifically?
- Does Claude avoid generic tutorials?
- Does conversation flow feel helpful?

---

#### **Step 7: Session End (0:31)**

**Browser:**

```
I think I understand now. Let's end the session here.
```

**Success Criteria:**

- [ ] Claude summarizes what you learned
- [ ] Claude generates update commands for you
- [ ] Commands are copy-pasteable (in code block)

**Example Expected Response from Claude:**

````
Excellent session! You discovered that justify-content works along
the flex-direction axis, not always horizontally.

Please update your model:

```bash
cd ~/Jupyter_Notebooks/10x-learner/student-model/

python student.py update "CSS Flexbox" --mastery 60 --confidence medium

python student.py breakthrough "CSS Flexbox" \
  "understood justify-content works along flex-direction axis - tested with Layout.css column example"
````

For next session: explore `align-items` to complete your mental model.

````

**⚠️ Test Point:** Does Claude generate actual commands, not just suggestions?

---

#### **Step 8: Update Student Model (0:33)**

**Terminal 1:**
```bash
cd ~/Jupyter_Notebooks/10x-learner/student-model/

# Paste commands Claude generated
python student.py update "CSS Flexbox" --mastery 60 --confidence medium

python student.py breakthrough "CSS Flexbox" \
  "understood justify-content works along flex-direction axis"
````

**Success Criteria:**

- [ ] Commands execute without errors
- [ ] Confirmation messages appear
- [ ] Changes feel accurate to what you learned

**Time Check:** Should take <2 minutes

---

#### **Step 9: Verify Update (0:35)**

**Terminal 1:**

```bash
python student.py show "CSS Flexbox"
```

**Success Criteria:**

- [ ] Mastery updated (45% → 60%)
- [ ] Breakthrough logged correctly
- [ ] Last reviewed timestamp is today
- [ ] Data matches what you learned

---

### Test 1: Success Metrics

**Timing Metrics:**

- [ ] Total session time: 30-45 minutes
- [ ] Student Model overhead: <3 minutes total (Steps 2, 4, 8, 9)
- [ ] Overhead percentage: <10% ✅ (Target: <5% ideal)
- [ ] No single step took >2 minutes

**Protocol Adherence:**

- [ ] Claude requested Student Model before teaching
- [ ] Claude requested workspace evidence
- [ ] Claude used Socratic method (questions, not lectures)
- [ ] Claude grounded explanation in your code
- [ ] Claude generated update commands

**Value Assessment:**

- [ ] Session felt more focused than normal LLM chat
- [ ] Continuity setup (model context) was worth the overhead
- [ ] Grounding in your code was helpful
- [ ] You learned something concrete
- [ ] You would do this again

**Friction Points (Document all):**

- Terminal switching: annoying / manageable / seamless
- Command typing: clunky / acceptable / smooth
- Persona prompt: too long / just right / too short
- Claude adherence: poor / inconsistent / excellent
- Overall workflow: frustrating / acceptable / natural

---
