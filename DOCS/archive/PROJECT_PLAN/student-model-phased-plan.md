# Student Model: Two-Week Implementation Plan

**Conservative Estimates | Evidence-Driven | Incremental Testing**

---

## Phase 0: Pre-Implementation (30 minutes)

### Goal
Verify we have everything needed to start archaeological sessions.

### Tasks

**0.1: Repository Setup** (10 min)
```bash
# Clone monkeytype
git clone https://github.com/monkeytypegame/monkeytype.git
cd monkeytype

# Open in editor
code .

# Verify structure
ls packages/
```

**0.2: Create Session Documentation Structure** (10 min)
```bash
# In your learning project folder
mkdir -p student-model-sessions
cd student-model-sessions

# Create templates
touch SESSION_TEMPLATE.md
touch TRACKING_TEMPLATE.md
```

**0.3: Review Confusion Point** (10 min)
- Read monkeytype root README.md
- Skim packages/ directory
- List specific questions about monorepo architecture
- Example questions:
  - Why separate packages for backend/frontend/contracts?
  - How do they share TypeScript types?
  - What's in each package.json?
  - What problem does this solve vs single package?

### Success Criteria
- ✅ Monkeytype repository cloned and accessible
- ✅ Documentation structure created
- ✅ 3-5 specific questions about monorepo written down

### Deliverable
- `CONFUSION_POINTS.md` with initial questions

---

## Phase 1: Archaeological Sessions (Week 1, Days 1-4, 4-6 hours total)

### Goal
Run 2-3 archaeological sessions exploring monorepo architecture, manually tracking what happens to understanding.

---

### Session 1: Package Structure Investigation (Day 1-2, 1.5-2 hours)

**1.1: Session Setup** (5 min)
- Start session with Claude
- Upload project context document
- State confusion point: "Let's explore monkeytype's monorepo architecture"

**1.2: Initial Hypothesis Formation** (10 min)
- Claude asks: "Why do you think they use multiple packages?"
- You form hypothesis based on intuition
- Document: "My initial theory is..."

**1.3: Evidence Gathering - Root Level** (20 min)
Claude requests files:
```bash
cat package.json
cat lerna.json  # or turbo.json, or similar
cat packages/README.md  # if exists
ls -la packages/
```

You share outputs, Claude analyzes:
- What's the monorepo tool? (Lerna, Turborepo, npm workspaces?)
- How are packages linked?
- What's the dependency structure?

**1.4: Evidence Gathering - Package Level** (30 min)
Claude requests:
```bash
cat packages/backend/package.json
cat packages/frontend/package.json
cat packages/contracts/package.json
```

Investigate:
- What dependencies does each have?
- Do they reference each other? How?
- What scripts are defined?
- Any shared tooling?

**1.5: Hypothesis Revision** (15 min)
Based on evidence:
- Does your initial hypothesis hold?
- What surprised you?
- What patterns are emerging?

**1.6: Pattern Synthesis** (20 min)
Claude guides:
- "What problem does separating packages solve?"
- "How does this compare to a monolith structure?"
- "When would you use this pattern?"

**1.7: Session Documentation** (20 min)
Create `SESSION_01_SUMMARY.md`:
```markdown
# Session 1: Monorepo Package Structure

## Starting Understanding
- Mastery: 10%
- Confusion: Why separate packages?
- Hypothesis: "I think it's for organizing code"

## Investigation
- Files examined: [list]
- Key discoveries: [list]
- Surprises: [list]

## Ending Understanding
- Mastery: 40%
- New understanding: "It's for independent deployment and shared code reuse"
- Remaining confusion: "How do types stay in sync?"

## Evidence of Understanding Change
- Question I asked: "Why not just use folders?"
- Hypothesis I formed: "Maybe for npm publishing?"
- Aha moment: "Oh! They can version packages independently"
- Misconception corrected: "Thought it was just code organization, but it's about dependency management"

## What Claude Did Well
- Asked diagnostic questions
- Requested specific files
- Connected to my Python package experience

## What Claude Could Improve
- Spent too long on basic npm workspace explanation (I already know Python virtual envs)
```

### Success Criteria
- ✅ 2+ hours of investigation completed
- ✅ Hypothesis formed → tested → revised
- ✅ Mastery level change documented (10% → ~40%)
- ✅ Evidence of learning moments captured
- ✅ Teaching calibration notes recorded

---

### Session 2: Shared Code & Type Safety (Day 2-3, 1.5-2 hours)

**2.1: Session Restoration** (5 min)
- Upload project context
- Upload Session 1 summary
- Claude calibrates: "Last time you understood package structure basics but were confused about type sharing. Let's explore that."

**2.2: New Hypothesis** (10 min)
- "How do frontend and backend share TypeScript types?"
- Form hypothesis based on Session 1 learning

**2.3: Evidence Gathering** (40 min)
Claude requests:
```bash
# Look for shared types
cat packages/contracts/src/index.ts
grep -r "from '@monkeytype/contracts'" packages/backend/
grep -r "from '@monkeytype/contracts'" packages/frontend/

# Check build process
cat packages/contracts/package.json
cat packages/contracts/tsconfig.json
```

Investigate:
- What's in the contracts package?
- How is it built?
- How do other packages consume it?
- What happens when types change?

**2.4: Pattern Application** (20 min)
Claude asks:
- "Could you identify another example of shared code in this repo?"
- "What would break if contracts package didn't exist?"
- "How would you add a new shared utility?"

**2.5: Session Documentation** (20 min)
Create `SESSION_02_SUMMARY.md` using same template

**2.6: Cross-Session Pattern Analysis** (15 min)
After documenting, compare Sessions 1 & 2:
- What patterns repeat? (e.g., "needed concrete examples before understanding")
- What teaching approaches worked? (e.g., "connecting to Python packages")
- What evidence types revealed mastery? (e.g., "successfully found another example")

### Success Criteria
- ✅ Built on Session 1 understanding
- ✅ Mastery increased (40% → ~65%)
- ✅ Applied pattern independently
- ✅ Cross-session patterns identified

---

### Session 3: Build & Deployment (Day 3-4, 1.5-2 hours)

**3.1: Session Restoration** (5 min)
- Upload context + both previous summaries
- Claude calibrates based on 65% mastery

**3.2: Final Investigation** (60 min)
Explore build/deployment:
```bash
cat turbo.json  # or lerna.json
cat .github/workflows/*.yml  # CI/CD
npm run build --workspaces  # See what happens
```

Questions:
- How are packages built?
- What's the deployment strategy?
- How do they handle versioning?
- What's the developer workflow?

**3.3: Complete Picture Synthesis** (30 min)
Claude asks:
- "Explain the full monorepo architecture in your own words"
- "When would you use this vs alternatives?"
- "What would you do differently for a smaller project?"

**3.4: Session Documentation** (15 min)
Create `SESSION_03_SUMMARY.md`

### Success Criteria
- ✅ Can explain monorepo architecture end-to-end
- ✅ Can compare to alternatives (monolith, polyrepo)
- ✅ Mastery reaches 75-85%
- ✅ Three sessions of learning data collected

---

## Phase 2: Pattern Analysis (Week 1, Days 5-7, 3-4 hours total)

### Goal
Analyze what happened across the three sessions to understand what the Student Model needs to capture.

---

### Day 5: Evidence Synthesis (1.5-2 hours)

**2.1: Review All Session Summaries** (30 min)
Read Sessions 1-3, highlighting:
- Every statement about mastery level
- Every "aha moment"
- Every misconception corrected
- Every teaching approach that worked/didn't work
- Every time you wished Claude remembered something

**2.2: Create Evidence Inventory** (45 min)
Create `EVIDENCE_ANALYSIS.md`:
```markdown
# Evidence of Understanding Change

## Mastery Trajectory
- Session 1: 10% → 40% (package structure basics)
- Session 2: 40% → 65% (type sharing, cross-package deps)
- Session 3: 65% → 85% (complete architecture understanding)

## Learning Moments by Type

### Explicit Questions (revealed confusion)
1. "Why not just use folders?" - Session 1
2. "How do types stay in sync?" - Session 1
3. "What happens when contracts change?" - Session 2

### Hypotheses Formed (revealed reasoning)
1. "I think it's for code organization" → Wrong, it's dependency management
2. "Maybe for npm publishing?" → Partially right
3. "Types must be manually copied" → Wrong, they're imported

### Successful Applications (revealed mastery)
1. Found 3 more shared packages independently - Session 2
2. Explained architecture without prompting - Session 3
3. Compared to Python poetry workspace - Session 2

### Misconceptions Corrected
1. Thought monorepo = organization, actually = dependency management
2. Thought types needed manual sync, actually = build process
3. Thought all packages must be published, actually = private packages OK

## Teaching Calibration

### What Worked
- Connecting to Python package experience
- Socratic questions ("What would break if...?")
- Requesting specific files, not theory dumps
- Building Session 2 on Session 1 explicitly

### What Didn't Work
- Session 1: Too much time on npm workspaces basics (I knew virtual envs)
- Session 2: Assumed I understood build tools (needed more context)

## Information Claude Should Have Known

### From Session 1 (would have improved Session 2)
- My Python packaging experience → could have skipped basics
- My confusion about build processes → needed more emphasis

### From Session 2 (would have improved Session 3)
- My understanding of type sharing → could move faster on CI/CD
- My preference for workflow diagrams → should have drawn architecture
```

**2.3: Identify Schema Requirements** (30 min)
Create `SCHEMA_REQUIREMENTS.md`:
```markdown
# What the Student Model Must Capture

## Required Tables (Validated by Evidence)

### 1. Concepts
**Why needed:** Sessions 1-3 covered 8 distinct concepts:
- Monorepo vs monolith
- Package.json workspaces
- Cross-package dependencies
- TypeScript path aliases
- Shared contracts pattern
- Build orchestration
- Independent versioning
- CI/CD for monorepos

**Required fields:**
- concept_name (e.g., "monorepo-architecture")
- category (e.g., "architecture-patterns")
- first_encountered (session_id, timestamp)
- description (brief)

### 2. Mastery States
**Why needed:** My understanding changed measurably each session (10→40→65→85%).

**Required fields:**
- concept_id
- mastery_percentage (0-100)
- confidence_level (how sure is Claude about this assessment?)
- last_updated
- current_struggle (text - what's still confusing?)

### 3. Learning Events
**Why needed:** 15+ distinct moments where evidence revealed understanding:
- Questions asked (9 times)
- Hypotheses formed (7 times)
- Successful applications (4 times)
- Misconceptions corrected (3 times)

**Required fields:**
- concept_id
- session_id
- timestamp
- event_type (question | hypothesis | application | misconception)
- evidence_text (what was said/done)
- mastery_change (did this reveal higher/lower mastery?)

### 4. Misconceptions
**Why needed:** 3 significant wrong beliefs that, if not tracked, would resurface.

**Required fields:**
- concept_id
- misconception_text
- correct_understanding
- discovered_session_id
- resolved (boolean - do I still have this misconception?)

### 5. Teaching Approaches
**Why needed:** Clear patterns emerged:
- Socratic questioning: highly effective (5 instances)
- Connecting to Python: highly effective (3 instances)
- Theory-first: ineffective (2 instances)
- Concrete examples: highly effective (4 instances)

**Required fields:**
- approach_type
- effectiveness_rating (1-5)
- concept_id (which concepts worked with this approach)
- notes

## Optional but Valuable

### 6. Session Summaries
Keep the markdown files, but add:
- session_id (FK to events)
- mastery_snapshot (JSON of all concept masteries at session end)

## What We DON'T Need (Validated by Absence)

- ❌ Files viewed (not useful - too granular)
- ❌ Time spent per concept (doesn't predict mastery)
- ❌ Comparative mastery (me vs others - not relevant)
- ❌ Skill prerequisites graph (emerged naturally, don't need to model)
```

### Success Criteria
- ✅ Evidence inventory complete
- ✅ Schema requirements justified by actual data
- ✅ Clear distinction between required vs optional fields

---

### Days 6-7: Schema Design (1.5-2 hours)

**2.4: Create Initial Schema** (60 min)
Create `STUDENT_MODEL_SCHEMA_V01.sql`:
```sql
-- Version 0.1: Minimal viable schema based on Sessions 1-3 evidence

CREATE TABLE concepts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    category TEXT,
    description TEXT,
    first_encountered DATE DEFAULT CURRENT_DATE
);

CREATE TABLE mastery_states (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    concept_id INTEGER NOT NULL,
    mastery_percentage INTEGER CHECK(mastery_percentage >= 0 AND mastery_percentage <= 100),
    confidence_level INTEGER CHECK(confidence_level >= 1 AND confidence_level <= 5),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    current_struggle TEXT,
    FOREIGN KEY (concept_id) REFERENCES concepts(id)
);

CREATE TABLE learning_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    concept_id INTEGER NOT NULL,
    session_number INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    event_type TEXT CHECK(event_type IN ('question', 'hypothesis', 'application', 'misconception', 'explanation')),
    evidence_text TEXT NOT NULL,
    mastery_before INTEGER,
    mastery_after INTEGER,
    FOREIGN KEY (concept_id) REFERENCES concepts(id)
);

CREATE TABLE misconceptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    concept_id INTEGER NOT NULL,
    misconception_text TEXT NOT NULL,
    correct_understanding TEXT NOT NULL,
    discovered_session INTEGER,
    resolved BOOLEAN DEFAULT 0,
    resolution_session INTEGER,
    FOREIGN KEY (concept_id) REFERENCES concepts(id)
);

CREATE TABLE teaching_approaches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    approach_type TEXT NOT NULL,
    effectiveness_rating INTEGER CHECK(effectiveness_rating >= 1 AND effectiveness_rating <= 5),
    concept_id INTEGER,
    notes TEXT,
    session_number INTEGER,
    FOREIGN KEY (concept_id) REFERENCES concepts(id)
);

-- Indexes for common queries
CREATE INDEX idx_mastery_concept ON mastery_states(concept_id);
CREATE INDEX idx_events_concept ON learning_events(concept_id);
CREATE INDEX idx_events_session ON learning_events(session_number);
CREATE INDEX idx_misconceptions_resolved ON misconceptions(resolved);
```

**2.5: Create Population Script Template** (30 min)
Create `populate_student_model.py`:
```python
#!/usr/bin/env python3
"""
Populate Student Model from session summaries.
Usage: python populate_student_model.py SESSION_01_SUMMARY.md
"""

import sqlite3
import sys
from datetime import datetime

def parse_session_summary(filepath):
    """Extract structured data from session markdown."""
    with open(filepath) as f:
        content = f.read()
    
    # TODO: Parse sections:
    # - Starting/Ending Understanding
    # - Evidence of Understanding Change
    # - What Claude Did Well/Could Improve
    
    return {
        'concepts': [],
        'mastery_changes': [],
        'events': [],
        'misconceptions': [],
        'teaching_notes': []
    }

def insert_concepts(conn, concepts):
    """Insert or update concepts."""
    cursor = conn.cursor()
    for concept in concepts:
        cursor.execute("""
            INSERT OR IGNORE INTO concepts (name, category, description)
            VALUES (?, ?, ?)
        """, (concept['name'], concept.get('category'), concept.get('description')))
    conn.commit()

def insert_mastery_state(conn, concept_name, mastery, confidence, struggle):
    """Update current mastery state for a concept."""
    cursor = conn.cursor()
    concept_id = cursor.execute(
        "SELECT id FROM concepts WHERE name = ?", (concept_name,)
    ).fetchone()[0]
    
    cursor.execute("""
        INSERT INTO mastery_states (concept_id, mastery_percentage, confidence_level, current_struggle)
        VALUES (?, ?, ?, ?)
    """, (concept_id, mastery, confidence, struggle))
    conn.commit()

def insert_learning_events(conn, events, session_number):
    """Log learning events from session."""
    cursor = conn.cursor()
    for event in events:
        concept_id = cursor.execute(
            "SELECT id FROM concepts WHERE name = ?", (event['concept'],)
        ).fetchone()[0]
        
        cursor.execute("""
            INSERT INTO learning_events 
            (concept_id, session_number, event_type, evidence_text, mastery_before, mastery_after)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (concept_id, session_number, event['type'], event['evidence'], 
              event.get('mastery_before'), event.get('mastery_after')))
    conn.commit()

def main():
    if len(sys.argv) < 2:
        print("Usage: python populate_student_model.py SESSION_XX_SUMMARY.md")
        sys.exit(1)
    
    session_file = sys.argv[1]
    db_path = "student_model.db"
    
    # Parse session summary
    data = parse_session_summary(session_file)
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    
    # Insert data
    insert_concepts(conn, data['concepts'])
    # ... etc
    
    conn.close()
    print(f"✅ Populated from {session_file}")

if __name__ == "__main__":
    main()
```

**2.6: Document Week 1 Findings** (30 min)
Create `WEEK_1_REPORT.md`:
```markdown
# Week 1: Archaeological Practice + Evidence Analysis

## What We Accomplished
- ✅ 3 archaeological sessions completed
- ✅ Monorepo mastery: 10% → 85%
- ✅ 15+ learning moments documented
- ✅ Evidence-based schema designed
- ✅ Population script template created

## Key Findings

### 1. Archaeological Learning Works
Went from confused about monorepos to explaining architecture independently in 3 sessions.
This validates the learning method itself.

### 2. Evidence Types Are Consistent
Same 5 types appeared across all sessions:
- Questions (revealed confusion)
- Hypotheses (revealed reasoning)
- Applications (revealed mastery)
- Misconceptions (revealed wrong models)
- Teaching approaches (revealed what works)

### 3. Student Model Schema Is Justified
Every table in the schema maps to actual data from the 3 sessions.
Not theoretical - empirically needed.

### 4. Manual Tracking Is Feasible But Painful
Took 20 minutes per session to document.
Worth it for the insights, but automation would help.

## Concerns & Risks

### Risk 1: Mastery Percentages Feel Arbitrary
Going from 40% to 65% - how do we know it's really 65% and not 55%?
**Mitigation:** Add confidence level field. Don't over-index on exact numbers.

### Risk 2: Parsing Session Summaries Is Brittle
The population script assumes structured markdown.
**Mitigation:** Start with manual population, automate later.

### Risk 3: Schema Might Not Generalize
This schema works for monorepo learning. Will it work for other concepts?
**Mitigation:** Test with a different confusion point (Week 2).

## Decision Point: Build It?

**Arguments For:**
- Schema is evidence-based, not theoretical
- Manual population is tractable (5-10 min/session)
- Week 2 sessions will test if it actually helps Claude

**Arguments Against:**
- Could just structure session summaries better
- Adds complexity before fully validating value
- Might be solving a problem that doesn't hurt enough

**Recommendation:** Proceed to Phase 3 (build v0.1) but keep it minimal.
- Implement schema as-is
- Manual population only
- Test in 2-3 sessions
- Evaluate honestly: does it help?
```

### Success Criteria
- ✅ SQL schema created
- ✅ Population script templated
- ✅ Week 1 findings documented
- ✅ Go/no-go decision made

---

## Phase 3: Student Model v0.1 (Week 2, Days 1-4, 4-5 hours total)

### Goal
Build the simplest working Student Model that lets Claude query your learning state at session start.

---

### Day 1: Database Setup (1-1.5 hours)

**3.1: Initialize Database** (15 min)
```bash
cd student-model-sessions/
sqlite3 student_model.db < STUDENT_MODEL_SCHEMA_V01.sql

# Verify tables created
sqlite3 student_model.db ".tables"
# Should show: concepts, mastery_states, learning_events, misconceptions, teaching_approaches
```

**3.2: Populate from Sessions 1-3** (45 min)
Manually enter data from session summaries:

```sql
-- Session 1: Monorepo basics
INSERT INTO concepts (name, category, description) VALUES 
('monorepo-architecture', 'architecture-patterns', 'Using multiple packages in single repo'),
('npm-workspaces', 'build-tools', 'NPM feature for linking local packages'),
('package-dependencies', 'architecture-patterns', 'How packages depend on each other');

INSERT INTO mastery_states (concept_id, mastery_percentage, confidence_level, current_struggle) VALUES
((SELECT id FROM concepts WHERE name='monorepo-architecture'), 40, 3, 'Still unclear on build process'),
((SELECT id FROM concepts WHERE name='npm-workspaces'), 60, 4, NULL),
((SELECT id FROM concepts WHERE name='package-dependencies'), 50, 3, 'Type sharing mechanism unclear');

INSERT INTO learning_events (concept_id, session_number, event_type, evidence_text, mastery_before, mastery_after) VALUES
((SELECT id FROM concepts WHERE name='monorepo-architecture'), 1, 'question', 'Why not just use folders?', 10, 20),
((SELECT id FROM concepts WHERE name='monorepo-architecture'), 1, 'hypothesis', 'I think its for code organization', 20, 25),
((SELECT id FROM concepts WHERE name='monorepo-architecture'), 1, 'misconception', 'Thought monorepo = organization, actually = dependency management', 25, 40);

INSERT INTO misconceptions (concept_id, misconception_text, correct_understanding, discovered_session, resolved) VALUES
((SELECT id FROM concepts WHERE name='monorepo-architecture'), 
 'Monorepo is just for organizing code into folders', 
 'Monorepo enables independent package versioning and dependency management',
 1, 1);

-- Repeat for Sessions 2-3...
```

**3.3: Create Query Scripts** (20 min)
Create `query_student_model.py`:
```python
#!/usr/bin/env python3
"""
Query student model for current learning state.
Usage: python query_student_model.py [concept_name]
"""

import sqlite3
import sys
import json

def get_current_mastery_summary(conn):
    """Get all concepts and current mastery levels."""
    cursor = conn.cursor()
    results = cursor.execute("""
        SELECT 
            c.name,
            c.category,
            ms.mastery_percentage,
            ms.confidence_level,
            ms.current_struggle,
            ms.last_updated
        FROM concepts c
        JOIN mastery_states ms ON c.id = ms.concept_id
        ORDER BY ms.last_updated DESC
    """).fetchall()
    
    return [
        {
            'concept': row[0],
            'category': row[1],
            'mastery': row[2],
            'confidence': row[3],
            'struggle': row[4],
            'updated': row[5]
        }
        for row in results
    ]

def get_teaching_approaches(conn):
    """Get effective teaching approaches."""
    cursor = conn.cursor()
    results = cursor.execute("""
        SELECT approach_type, AVG(effectiveness_rating) as avg_rating, COUNT(*) as usage_count
        FROM teaching_approaches
        GROUP BY approach_type
        HAVING avg_rating >= 4
        ORDER BY avg_rating DESC
    """).fetchall()
    
    return [{'approach': row[0], 'rating': row[1], 'uses': row[2]} for row in results]

def get_active_misconceptions(conn):
    """Get unresolved misconceptions."""
    cursor = conn.cursor()
    results = cursor.execute("""
        SELECT c.name, m.misconception_text, m.correct_understanding
        FROM misconceptions m
        JOIN concepts c ON m.concept_id = c.id
        WHERE m.resolved = 0
    """).fetchall()
    
    return [
        {'concept': row[0], 'wrong': row[1], 'correct': row[2]}
        for row in results
    ]

def main():
    conn = sqlite3.connect("student_model.db")
    
    print("=== Student Model Summary ===\n")
    
    print("## Current Mastery Levels")
    for item in get_current_mastery_summary(conn):
        struggle_note = f" (Struggling: {item['struggle']})" if item['struggle'] else ""
        print(f"- {item['concept']}: {item['mastery']}% (confidence: {item['confidence']}/5){struggle_note}")
    
    print("\n## Effective Teaching Approaches")
    for approach in get_teaching_approaches(conn):
        print(f"- {approach['approach']}: {approach['rating']:.1f}/5 rating ({approach['uses']} uses)")
    
    print("\n## Active Misconceptions to Watch")
    misconceptions = get_active_misconceptions(conn)
    if misconceptions:
        for m in misconceptions:
            print(f"- {m['concept']}: '{m['wrong']}' → '{m['correct']}'")
    else:
        print("- None")
    
    conn.close()

if __name__ == "__main__":
    main()
```

Test it:
```bash
python query_student_model.py
```

Expected output:
```
=== Student Model Summary ===

## Current Mastery Levels
- monorepo-architecture: 85% (confidence: 4/5)
- typescript-path-aliases: 70% (confidence: 3/5) (Struggling: Build configuration unclear)
- npm-workspaces: 75% (confidence: 4/5)

## Effective Teaching Approaches
- socratic-questioning: 4.5/5 rating (5 uses)
- connect-to-python: 5.0/5 rating (3 uses)
- concrete-examples: 4.2/5 rating (4 uses)

## Active Misconceptions to Watch
- None
```

### Success Criteria
- ✅ Database created with schema
- ✅ Data from Sessions 1-3 populated
- ✅ Query script returns formatted summary
- ✅ Takes <10 minutes to populate a session

---

### Days 2-3: Test with New Confusion Point (2-3 hours)

**3.4: Pick Second Confusion Point** (10 min)
Choose something different to test schema generalization:
- React Server Components?
- Next.js file-based routing?
- Monkeytype's state management?

**3.5: Run Session 4 with Student Model** (90 min)
At session start:
```bash
python query_student_model.py > session_04_context.txt
```

Provide to Claude:
- Project context document
- `session_04_context.txt` output
- "We're exploring [new confusion point]. Use the student model context to calibrate your teaching."

**During session:**
- Note when Claude references your past learning
- Note when Claude's teaching feels well-calibrated
- Note any queries you wish Claude could run

**After session:**
- Document in `SESSION_04_SUMMARY.md`
- Manually populate database with new data
- Run query script again to see updated state

**3.6: Run Session 5** (90 min)
Repeat the process. This time:
- Test if Claude remembers Session 4 learning
- Test if mastery trajectory is visible
- Test if teaching calibration improves

### Success Criteria
- ✅ Student Model works for a different confusion point
- ✅ Claude demonstrably uses the model data
- ✅ Teaching calibration improves (subjective but noticeable)
- ✅ Population workflow is <10 min per session

---

### Day 4: Refinement (1 hour)

**3.7: Evaluate What's Working** (30 min)
Review Sessions 4-5, ask:
- Did Claude reference past learning appropriately?
- Did mastery levels feel accurate?
- Did teaching approaches data help?
- What queries would have been useful but aren't possible?

**3.8: Schema Adjustments** (30 min)
If needed:
- Add missing fields
- Remove unused tables
- Improve query scripts

Update schema to v0.2 if changes made.

### Success Criteria
- ✅ Honest evaluation of Student Model utility
- ✅ Schema refined based on real usage
- ✅ Query scripts improved

---

## Phase 4: Validation & Iteration (Week 2, Days 5-6, 2-3 hours)

### Goal
Decide if the Student Model actually solves the problem better than alternatives.

---

### Day 5: Comparison Test (1.5-2 hours)

**4.1: Run Session 6 WITHOUT Student Model** (90 min)
To establish baseline:
- Don't load student model at start
- Only provide: project context + previous session summary
- See how long context restoration takes
- Note when Claude should have known something but didn't

**4.2: Run Session 7 WITH Student Model** (90 min)
Same confusion point complexity:
- Load student model at start
- Time context restoration
- Note when Claude references past learning effectively

**4.3: Compare Results** (30 min)
Create `MODEL_COMPARISON.md`:
```markdown
# Student Model A/B Test

## Session 6 (Without Model)
- Context restoration time: 8 minutes
- Times Claude asked about past learning: 5
- Times Claude re-explained known concepts: 3
- Teaching calibration rating: 3/5

## Session 7 (With Model)
- Context restoration time: 2 minutes
- Times Claude asked about past learning: 0
- Times Claude re-explained known concepts: 0
- Teaching calibration rating: 5/5

## Conclusion
Model saves ~6 minutes per session and improves calibration.
Over 50 sessions, that's 300 minutes (5 hours) saved.
More importantly: teaching quality is noticeably better.

## Decision: Keep or Discard?
- [X] Keep - clear value demonstrated
- [ ] Discard - not worth the overhead
- [ ] Refine - needs changes but has potential
```

### Success Criteria
- ✅ A/B comparison completed
- ✅ Measurable difference in context restoration time
- ✅ Subjective improvement in teaching quality
- ✅ Clear decision on continuing

---

### Day 6: Automation & Polish (1-1.5 hours)

**4.4: Improve Population Script** (45 min)
If keeping the model, reduce friction:

```python
# Enhanced populate_student_model.py

def auto_extract_from_summary(filepath):
    """
    Parse structured markdown sections automatically.
    Looks for patterns like:
    - "Mastery: 40%" or "## Ending Understanding"
    - "Misconception: X → Y"
    - "Question: ..."
    """
    # TODO: Add regex patterns for common formats
    pass

def propose_updates(session_data):
    """
    Print proposed database updates for user to confirm.
    
    Example output:
    ---
    PROPOSED UPDATES:
    
    Concept: monorepo-architecture
    - Current mastery: 40%
    - Proposed new mastery: 65%
    - Reason: Successfully applied pattern 3 times
    
    New misconception detected:
    - "Build happens in parallel" → "Build is orchestrated by Turborepo"
    
    Accept? [y/N]
    ---
    """
    pass
```

**4.5: Create Session Start Template** (15 min)
Create `START_SESSION.md`:
```markdown
# Session [NUMBER] Start Template

## Pre-Session Checklist
- [ ] Run: `python query_student_model.py > context.txt`
- [ ] Upload to Claude: `PROJECT_CONTEXT.md`
- [ ] Upload to Claude: `context.txt`
- [ ] State today's confusion point

## During Session
- [ ] Note: Times Claude references past learning
- [ ] Note: Teaching calibration (too basic/just right/too advanced)
- [ ] Note: New concepts encountered
- [ ] Note: Aha moments or misconceptions

## Post-Session Checklist
- [ ] Write: `SESSION_XX_SUMMARY.md`
- [ ] Run: `python populate_student_model.py SESSION_XX_SUMMARY.md`
- [ ] Verify: `python query_student_model.py` shows updates
- [ ] Time spent: Document how long population took
```

**4.6: Document Final Workflow** (15 min)
Update `PROJECT_CONTEXT.md` with:
```markdown
## Student Model Workflow (Week 2+)

### Before Each Session (2 min)
1. `python query_student_model.py > context.txt`
2. Upload `PROJECT_CONTEXT.md` + `context.txt` to Claude
3. State confusion point

### During Session (0 overhead)
- Learn naturally
- Mentally note: calibration, aha moments, misconceptions

### After Session (8 min)
1. Write session summary: 5 min
2. Populate database: 3 min
   - Run `python populate_student_model.py SESSION_XX_SUMMARY.md`
   - Confirm proposed updates

### Weekly Review (30 min)
- Run analytics queries
- Review mastery trajectories
- Adjust teaching approach preferences
```

### Success Criteria
- ✅ Population time reduced to <5 minutes
- ✅ Session workflow documented
- ✅ Templates created for consistency

---

## Phase 5: Evaluation & Next Steps (Week 2, Day 7, 1-2 hours)

### Goal
Honest assessment of whether this system delivers value, and plan for continued use or pivot.

---

**5.1: Calculate Success Metrics** (30 min)

Review all 7 sessions and score:

```markdown
# Two-Week Evaluation

## Metric 1: Context Restoration Time
- Sessions 1-3 (no model): avg 7 minutes
- Sessions 4-7 (with model): avg 2 minutes
- **Improvement: 71% reduction**

## Metric 2: Teaching Calibration
Rate each session 1-5 (too basic → just right → too advanced):
- Session 1: 3/5 (some unnecessary npm basics)
- Session 2: 4/5 (mostly good)
- Session 3: 4/5 (well calibrated)
- Session 4: 5/5 (perfect calibration with model)
- Session 5: 5/5 (referenced past learning 4x)
- Session 6 (no model): 3/5 (re-explained known concepts)
- Session 7 (with model): 5/5 (built perfectly on past work)
- **Improvement: Model sessions averaged 5/5 vs 3.5/5 without**

## Metric 3: Learning Velocity
- Monorepo mastery: 3 sessions to reach 85%
- [Second confusion point]: X sessions to reach Y%
- **Baseline established for future comparison**

## Metric 4: Cross-Session Pattern Recognition
- Times Claude explicitly linked to past learning: 12 instances
- Times Claude caught me using old misconception: 2 instances
- **Value confirmed: patterns compound across sessions**
```

**5.2: Cost-Benefit Analysis** (20 min)

```markdown
# Is It Worth It?

## Costs
- Initial setup: 8 hours (schema design, population scripts)
- Per-session overhead: 8 minutes (5 min summary, 3 min population)
- Ongoing: ~10 min/week reviewing data

## Benefits
- Time saved per session: 5 minutes (context restoration)
- Teaching quality improvement: measurable (3.5 → 5.0 rating)
- Compounding effect: earlier sessions inform later ones
- Meta-learning: can now see patterns in my own learning

## Break-Even Analysis
- Setup cost: 8 hours = 480 minutes
- Per-session benefit: 5 minutes saved + better learning (hard to quantify)
- Conservative: Break even after 96 sessions (480/5)
- Realistic: Break even after ~30 sessions (accounting for quality improvement)

## Verdict
- [ ] Not worth it - too much overhead
- [X] Worth it - clear value after Week 2
- [ ] Maybe - needs longer test period
```

**5.3: Identify Gaps & Future Improvements** (30 min)

```markdown
# What's Missing?

## Current Limitations
1. **Manual population is tedious** - 3 minutes per session adds up
2. **Mastery percentages feel arbitrary** - hard to calibrate accurately
3. **Schema doesn't capture learning pace** - some concepts stick fast, others slow
4. **No visualization** - can't easily see trajectory over time
5. **Misconception tracking underused** - only caught 2 instances

## Potential Improvements (Priority Order)

### P0: Must Have (Next 2 Weeks)
- [ ] Semi-automated population (Claude proposes updates, I confirm)
- [ ] Confidence intervals on mastery (40% ± 15%)
- [ ] Session-to-session mastery visualization (simple chart)

### P1: Should Have (Month 2)
- [ ] Learning velocity metrics (sessions to 80% mastery)
- [ ] Prerequisite concept mapping (X requires understanding Y)
- [ ] Cross-project pattern library (patterns from speedtyper + monkeytype)

### P2: Nice to Have (Month 3+)
- [ ] Natural language query interface ("Show concepts I learned quickly")
- [ ] Export to markdown for sharing
- [ ] Integration with session summary tool

## What NOT to Build
- ❌ Web dashboard (markdown + CLI is fine)
- ❌ AI-driven mastery assessment (I should confirm)
- ❌ Social features (this is personal learning)
- ❌ Mobile app (desktop workflow works)
```

**5.4: Write Two-Week Report** (20 min)

Create `TWO_WEEK_REPORT.md`:
```markdown
# Student Model: Two-Week Implementation Report

**Period:** [Start Date] - [End Date]  
**Sessions Completed:** 7 archaeological sessions  
**Total Time Invested:** 18 hours (8 setup, 10 learning sessions)

---

## Executive Summary

Built a Student Model system to help Claude maintain context about my learning across sessions. After 7 sessions testing the system:

**✅ Success:** The system works. Context restoration time dropped 71%, teaching calibration improved measurably, and cross-session pattern recognition is now possible.

**⚠️ Caveat:** Setup overhead was significant (8 hours), and per-session maintenance (8 minutes) is manageable but not trivial.

**📊 Recommendation:** Continue using the system with semi-automation improvements planned.

---

## What We Built

### Week 1: Archaeological Practice (4 sessions)
- Explored monkeytype monorepo architecture
- Went from 10% → 85% mastery in 3 sessions
- Documented 15+ learning moments
- Designed evidence-based schema (5 tables)

### Week 2: Student Model Implementation (3 sessions)
- Built SQLite database with schema
- Created query + population scripts
- Tested with second confusion point
- A/B tested model vs no-model sessions

---

## Key Findings

### 1. The Core Hypothesis Was Correct
Claude forgets everything between sessions. This creates real friction in learning:
- Repeatedly explaining background: 7 minutes per session
- Teaching mis-calibrated: concepts re-explained or skipped
- Patterns not recognized: connections across sessions missed

The Student Model solves all three problems.

### 2. Evidence Types Are Predictable
Every session generated the same 5 types of evidence:
- Questions (reveal confusion)
- Hypotheses (reveal reasoning)
- Applications (reveal mastery)
- Misconceptions (reveal wrong models)
- Teaching approaches (reveal what works)

This consistency validates the schema design.

### 3. Manual Population Is Acceptable
Takes 8 minutes per session (5 min summary, 3 min database):
- Annoying but not prohibitive
- Forces reflection on learning
- Higher quality than full automation would be
- Could be reduced to 5 minutes with better scripts

### 4. The A/B Test Was Convincing
Session 6 (no model) vs Session 7 (with model):
- Context restoration: 8 min → 2 min
- Teaching calibration: 3/5 → 5/5
- Pattern recognition: 0 instances → 4 instances

The difference was immediately noticeable.

---

## Lessons Learned

### What Worked
1. **Evidence-first design:** Running sessions before building schema ensured we built what's actually needed
2. **SpeedTyper-Solo methodology:** Conservative estimates, incremental testing, fast failure detection
3. **Hybrid population:** Claude proposes, I confirm - best of automation + accuracy
4. **Simple tech stack:** SQLite + Python + markdown - no unnecessary complexity

### What Didn't Work
1. **Initial time estimates:** Underestimated schema design time (planned 2hr, took 4hr)
2. **Mastery percentages:** Numbers feel arbitrary, hard to calibrate accurately
3. **Misconception tracking:** Expected to catch more than we did (2 instances only)

### Surprises
1. **Teaching approaches table was most valuable:** Knowing I learn best with Socratic questioning + Python connections = huge calibration win
2. **Cross-session pattern recognition exceeded expectations:** Claude linked concepts across 4 sessions, something I wouldn't have noticed
3. **Compounding is real:** Session 7 felt 2x more effective than Session 1, not just faster

---

## Metrics Summary

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Context restoration time | <5 min | 2 min | ✅ Exceeded |
| Teaching calibration | >4/5 | 5/5 | ✅ Met |
| Learning velocity | 30% improvement | TBD (need more data) | ⏳ In progress |
| Cross-session transfer | >70% | 100% (12/12 opportunities) | ✅ Exceeded |

---

## Decision: Continue?

**YES** - with refinements.

The Student Model delivers measurable value:
- Saves 5+ minutes per session
- Improves teaching quality noticeably
- Enables compounding across projects
- Provides meta-learning insights

Next steps:
1. Reduce population time to <5 min (improve scripts)
2. Add confidence intervals to mastery scores
3. Test with third confusion point (validate generalization)
4. Consider whether to add prerequisite mapping

---

## What Would I Do Differently?

If starting over:
1. **Run 5 sessions before building anything** - more evidence = better schema
2. **Start with even simpler schema** - maybe 3 tables instead of 5
3. **Build query scripts first** - understand what questions matter before optimizing schema
4. **Test A/B comparison earlier** - confirms value faster

But overall, the phased approach worked well. Glad we didn't build infrastructure until we had evidence it was needed.

---

## For Future Me

When reading this in 6 months:

**If you're maintaining the system:** The 8 minutes per session is worth it. Don't get lazy and skip population - the compound effect depends on consistency.

**If you're considering abandoning it:** Review the A/B comparison (Session 6 vs 7). The difference was stark. Unless something changed, you need this.

**If you're considering expanding it:** Resist feature creep. The current system solves the core problem. Only add complexity if there's a new problem to solve.

---

## Appendix: Session Summaries

[Link to SESSION_01 through SESSION_07 markdown files]

## Appendix: Database Schema

[Link to STUDENT_MODEL_SCHEMA_V01.sql]

## Appendix: Code

[Link to query_student_model.py and populate_student_model.py]
```

---

### Success Criteria
- ✅ Honest evaluation completed
- ✅ Metrics calculated
- ✅ Decision made on continuing
- ✅ Future improvements identified
- ✅ Two-week report written

---

## Post-Implementation: Maintenance Plan

### Weekly Routine (30 minutes)

**Sunday Review:**
```bash
# Run analytics
python query_student_model.py

# Generate trajectory report
python analyze_learning_velocity.py  # TODO: build this

# Review:
# - Which concepts need more attention?
# - Are any misconceptions resurfacing?
# - What teaching approaches are working best?
```

### Monthly Routine (1 hour)

**Last Sunday of Month:**
- Export database for backup: `cp student_model.db backups/model_$(date +%Y%m).db`
- Review all sessions from the month
- Calculate meta-metrics:
  - Average mastery gain per session
  - Most/least effective teaching approaches
  - Concepts that consistently take longer to master
- Update teaching approach preferences in database

### Quarterly Routine (2 hours)

**End of Quarter:**
- Schema review: Do we need new tables/fields?
- Script optimization: Can population be faster?
- Cross-project analysis: What patterns appear across multiple codebases?
- Write quarterly report for future reference

---

## Risk Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Database corruption | Low | High | Weekly backups to `backups/` folder |
| Schema doesn't generalize | Medium | High | Test with 3+ different confusion points |
| Population becomes too tedious | Medium | Medium | Automate where possible, keep <5 min |
| Mastery scores become inaccurate | Medium | Medium | Add confidence intervals, periodic validation |
| System abandoned after 2 weeks | Low | High | A/B test proves value, write "don't abandon" note |

---

## Scope Boundaries

### In Scope ✅
- Tracking concept mastery across sessions
- Recording learning events and patterns
- Identifying effective teaching approaches
- Preserving misconception corrections
- Enabling Claude to query learning state
- Supporting code archaeology method

### Out of Scope ❌
- Automated mastery assessment (Claude proposes, human confirms)
- Web dashboard or fancy UI (CLI + markdown sufficient)
- Integration with other learning tools
- Social/sharing features
- Mobile access
- Real-time session recording
- Video/audio capture
- Spaced repetition scheduling
- Curriculum planning

---

## Rollback Plan

### If Student Model Doesn't Work

**Option 1: Revert to Enhanced Session Summaries**
Keep writing session summaries but add structured sections:
```markdown
## Mastery Updates
- Concept: monorepo-architecture | 40% → 65%
- Concept: npm-workspaces | 50% → 75%

## Misconceptions Corrected
- Wrong: "Monorepo is for organization"
- Right: "Monorepo enables independent versioning"
```

**Option 2: Revert to Basic Session Summaries**
Go back to SpeedTyper-Solo style summaries without structured data.

**Option 3: Try Different Tool**
Explore existing tools like Anki, Roam Research, Obsidian with learning plugins.

### How to Decide

If after 10 sessions:
- Context restoration still takes >5 minutes → Model isn't working, try Option 1
- Teaching calibration hasn't improved → Model isn't helping, try Option 1
- Population takes >10 minutes → Too much overhead, try Option 2
- No cross-session pattern recognition → Core value missing, try Option 3

---

## Success Criteria Summary

### Phase 0: Pre-Implementation ✅
- Repository cloned and accessible
- Documentation structure created
- Initial confusion points identified

### Phase 1: Archaeological Sessions ✅
- 3 sessions completed with manual tracking
- Mastery trajectory documented (10% → 85%)
- Evidence types identified and catalogued
- Teaching calibration notes recorded

### Phase 2: Pattern Analysis ✅
- Evidence inventory created
- Schema requirements justified
- Week 1 report written
- Go/no-go decision made

### Phase 3: Student Model v0.1 ✅
- Database created with schema
- Sessions 1-3 data populated
- Query scripts functional
- Sessions 4-5 completed with model
- Population workflow <10 minutes

### Phase 4: Validation ✅
- A/B comparison completed
- Measurable improvements documented
- Decision made on continuing
- Automation improvements identified

### Phase 5: Evaluation ✅
- Metrics calculated
- Cost-benefit analysis done
- Two-week report written
- Future improvements prioritized

---

## Appendix A: File Structure

```
student-model-sessions/
├── student_model.db                    # SQLite database
├── backups/                            # Monthly database backups
│   └── model_202411.db
├── SESSION_01_SUMMARY.md               # Session summaries
├── SESSION_02_SUMMARY.md
├── ...
├── SESSION_07_SUMMARY.md
├── CONFUSION_POINTS.md                 # Initial questions
├── EVIDENCE_ANALYSIS.md                # Week 1 findings
├── SCHEMA_REQUIREMENTS.md              # Schema justification
├── STUDENT_MODEL_SCHEMA_V01.sql        # Database schema
├── query_student_model.py              # Query current state
├── populate_student_model.py           # Populate from summaries
├── analyze_learning_velocity.py        # Analytics (TODO)
├── SESSION_TEMPLATE.md                 # Template for consistency
├── TRACKING_TEMPLATE.md                # Evidence tracking template
├── START_SESSION.md                    # Pre-session checklist
├── WEEK_1_REPORT.md                    # Week 1 findings
├── MODEL_COMPARISON.md                 # A/B test results
├── TWO_WEEK_REPORT.md                  # Final evaluation
└── PROJECT_CONTEXT.md                  # For Claude (this doc lives elsewhere)
```

---

## Appendix B: Example Session Summary

```markdown
# Session 3: Monorepo Build & Deployment

**Date:** 2025-11-XX  
**Duration:** 1.5 hours  
**Confusion Point:** How is monorepo built and deployed?  
**Previous Mastery:** monorepo-architecture 65%

---

## Starting State
- **What I Know:** Package structure, type sharing, dependencies
- **What Confuses Me:** Build orchestration, deployment strategy, CI/CD
- **Hypothesis:** "They probably build each package independently"

---

## Investigation

### Files Examined
1. `turbo.json` - Build orchestration config
2. `.github/workflows/deploy.yml` - CI/CD pipeline
3. `packages/backend/package.json` - Build scripts
4. `packages/frontend/package.json` - Build scripts

### Key Discoveries
1. Turborepo orchestrates builds based on dependency graph
2. Only changed packages get rebuilt (caching)
3. Deployment is per-package, not monolithic
4. CI runs tests in parallel across packages

### Surprises
- Build caching is more sophisticated than I expected
- They deploy packages independently (not all at once)
- CI/CD is actually simpler than monolith (isolated tests)

---

## Ending State
- **New Mastery:** monorepo-architecture 85%
- **What I Now Understand:** Complete picture from packages → build → deploy
- **Remaining Confusion:** None on basics, but advanced patterns (caching strategies) unclear

---

## Evidence of Learning

### Questions Asked
1. "How does Turborepo know what order to build?" → Revealed I didn't understand dependency graphs
2. "What happens if one package fails tests?" → Revealed concern about blast radius

### Hypotheses Formed
1. "Build must happen in parallel" → Correct!
2. "They deploy everything together" → Wrong, it's independent

### Successful Applications
1. Drew architecture diagram without prompting
2. Explained to Claude how I'd add a new package
3. Compared to Python poetry workspaces correctly

### Misconceptions Corrected
- Wrong: "All packages deployed together"
- Right: "Packages can be deployed independently based on changes"

---

## Teaching Calibration

### What Claude Did Well ✅
- Connected build orchestration to dependency management (Session 1 concept)
- Used Socratic questioning: "What would happen if...?"
- Provided concrete CI/CD example instead of theory

### What Claude Could Improve ⚠️
- Spent time explaining basic CI/CD concepts I already knew from backend work
- Could have asked about my CI/CD experience upfront

### Overall Rating: 4/5
(Just right, but minor calibration miss on CI/CD basics)

---

## Next Session
- Confusion point: React Server Components in monkeytype?
- Or: Deep dive into build caching strategies?
```

---

## Appendix C: Key Principles (Reminders)

From SpeedTyper-Solo methodology:

1. **Working solutions over perfect architecture**
   - Build minimum viable version first
   - Refine based on real usage
   - Don't over-engineer

2. **Evidence-based decisions**
   - Every schema field justified by actual data
   - Every feature validated by need
   - No speculative building

3. **Incremental testing**
   - Test each phase before moving to next
   - Clear success criteria per phase
   - Fast failure detection

4. **Conservative time estimates**
   - Assume tasks take longer than expected
   - Build in buffer for unknowns
   - Better to finish early than run late

5. **Documentation is for future self**
   - Write like you'll forget everything
   - Assume you'll need to pause and resume
   - Make it easy to pick up where you left off

---

## Final Notes

This plan is a living document. As we progress:
- Update phase completion status
- Document deviations from plan
- Note what worked differently than expected
- Adjust time estimates for future phases

The goal is not to follow the plan perfectly, but to have a framework that enables pragmatic progress while maintaining quality and learning from each phase.

Good luck, future self! 🚀
