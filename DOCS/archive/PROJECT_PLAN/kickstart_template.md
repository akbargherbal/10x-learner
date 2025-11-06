# Session Kickstart Template

**Purpose:** This template provides the structure for initializing a learning session. Fill in the variables based on current project state.

---

## Template Structure

```
This is Session [NUMBER]. [PHASE_CONTEXT]

Today's Confusion Point: [CONFUSION_POINT]

I'll share the key documents for this session:
1. TUTOR_PERSONA.md (defines your teaching approach)
2. PROJECT_CONTEXT.md (project overview and methodology)
3. COLLABORATION_PROTOCOL.md (how we interact)
4. [STUDENT_MODEL_CONTEXT] (if available)
5. [PREVIOUS_SESSION_SUMMARY] (if exists)
6. PHASED_PLAN.md (project roadmap)

---

## Current State

**Phase:** [PHASE_NUMBER] - [PHASE_NAME]
**Phase Goal:** [GOAL]
**Session Goal:** [SPECIFIC_SESSION_GOAL]

[MASTERY_SNAPSHOT]

---

## Codebase Context

**Repository:** [REPO_NAME]
**Location:** ~/learning-projects/[CODEBASE_NAME]/
**Focus Area:** [SPECIFIC_AREA]

---

## Important Notes

- When you need a specific file to investigate, explicitly request it with full path
- Use the collaboration protocol for all file operations
- Reference the Student Model silently—don't mention it explicitly to me
- [PHASE_SPECIFIC_NOTES]

---

Let's begin!
```

---

## Variable Definitions

### [NUMBER]
- Session count (1, 2, 3, ...)

### [PHASE_CONTEXT]
Options:
- "We're in Phase 0 (Pre-Implementation). No Student Model exists yet."
- "We're in Phase 1 (Archaeological Practice). Testing the learning method."
- "We're in Phase 2 (Pattern Analysis). Analyzing what happened in sessions 1-3."
- "We're in Phase 3 (Student Model v0.1). Testing the database."
- "We're in Phase 4 (Validation). Comparing with vs without model."
- "We're in Phase 5 (Evaluation). Final assessment."

### [CONFUSION_POINT]
What we're exploring this session:
- "Monkeytype's monorepo architecture"
- "React Server Components in Next.js"
- "Turborepo build orchestration"
- etc.

### [STUDENT_MODEL_CONTEXT]
If Student Model exists:
```
4. Student Model Context (generated from database):

Current Mastery Levels:
- monorepo-architecture: 65% (confidence: 3/5, struggling with: build process)
- npm-workspaces: 75% (confidence: 4/5)

Effective Teaching Approaches:
- socratic-questioning: 4.5/5
- connect-to-python: 5.0/5
- concrete-examples: 4.2/5

Active Misconceptions: None
```

If Student Model doesn't exist yet:
```
(No Student Model available yet—we're building evidence for it)
```

### [PREVIOUS_SESSION_SUMMARY]
If exists:
```
5. Previous Session Summary:

Last session (Session X) we explored [TOPIC].
- Started at [X%] mastery
- Ended at [Y%] mastery
- Key discovery: [INSIGHT]
- Remaining confusion: [OPEN_QUESTION]
```

If first session:
```
(This is the first session—no previous context)
```

### [MASTERY_SNAPSHOT]
If Student Model exists:
```
Based on previous sessions:
- Concept A: [X%] mastery
- Concept B: [Y%] mastery
- etc.
```

If no Student Model:
```
This is session [X] exploring [TOPIC]. No formal mastery tracking yet.
```

### [SPECIFIC_SESSION_GOAL]
Examples:
- "Understand why monkeytype uses multiple package.json files"
- "Trace how types are shared between frontend and backend"
- "Map the build orchestration pipeline"
- "Populate Student Model with Session 1-3 data"

### [PHASE_SPECIFIC_NOTES]
Phase-dependent reminders:
- Phase 1: "Remember to document learning moments for schema design"
- Phase 3: "At session end, we'll populate the Student Model database"
- Phase 4: "This is an A/B test—I won't load the Student Model to compare"

---

## Example: Actual Kickstart for Session 1

```markdown
This is Session 1. We're in Phase 1 (Archaeological Practice). No Student Model exists yet—we're gathering evidence to design it.

Today's Confusion Point: Monkeytype's monorepo architecture—specifically, why they use multiple package.json files and how packages interact.

I'll share the key documents for this session:
1. TUTOR_PERSONA.md (defines your teaching approach)
2. PROJECT_CONTEXT.md (project overview and methodology)
3. COLLABORATION_PROTOCOL.md (how we interact)
4. PHASED_PLAN.md (two-week roadmap)

(No Student Model or previous session summary available yet)

---

## Current State

**Phase:** Phase 1 - Archaeological Sessions  
**Phase Goal:** Run 2-3 sessions exploring monorepo architecture, manually track learning  
**Session Goal:** Understand package structure and why it's organized this way

**Self-Reported Skill Levels:**
- React basics: 70%
- TypeScript: 60%
- Monorepo architecture: 10% (seen it, don't understand it)

---

## Codebase Context

**Repository:** Monkeytype  
**Location:** ~/learning-projects/monkeytype/  
**Focus Area:** packages/ directory structure

---

## Important Notes

- When you need a specific file to investigate, explicitly request it with: `cat ~/learning-projects/monkeytype/path/to/file`
- At the end of the session, we'll spend 20 minutes documenting what happened to my understanding (evidence for schema design)
- Remember: I have strong Python background—connect to Python packaging when relevant

---

Let's begin!
```

---

## Example: Actual Kickstart for Session 4 (With Student Model)

```markdown
This is Session 4. We're in Phase 3 (Student Model v0.1). The database is live and populated with Sessions 1-3 data.

Today's Confusion Point: React Server Components in Next.js—when to use them vs client components.

I'll share the key documents for this session:
1. TUTOR_PERSONA.md
2. PROJECT_CONTEXT.md
3. COLLABORATION_PROTOCOL.md
4. STUDENT_MODEL_CONTEXT.txt (generated from database)
5. SESSION_03_SUMMARY.md (previous session)

---

## Current State

**Phase:** Phase 3 - Student Model v0.1 Testing  
**Phase Goal:** Validate that the Student Model improves teaching calibration  
**Session Goal:** Explore React Server Components architecture

**Student Model Context** (from database):

Current Mastery Levels:
- monorepo-architecture: 85% (confidence: 4/5)
- npm-workspaces: 75% (confidence: 4/5)
- typescript-path-aliases: 70% (confidence: 3/5, struggling with: build configuration)

Effective Teaching Approaches:
- socratic-questioning: 4.5/5 rating
- connect-to-python: 5.0/5 rating
- concrete-examples: 4.2/5 rating

Active Misconceptions: None

**Previous Session:** Session 3 explored monorepo build orchestration. Went from 65% → 85% mastery on monorepo-architecture. Key discovery: Turborepo caches builds based on dependency graph.

---

## Codebase Context

**Repository:** Next.js Documentation Examples  
**Location:** ~/learning-projects/nextjs-app-router-example/  
**Focus Area:** app/ directory with Server Components

---

## Important Notes

- Use the Student Model context to calibrate your teaching—don't re-explain monorepo concepts I already understand
- When you need files, request with full paths
- At session end, we'll document and populate the database with today's learning

---

Let's begin!
```

---

## Usage Instructions

**For Session Start:**

1. Copy this template
2. Fill in variables based on:
   - Current phase (from PHASED_PLAN.md)
   - Session number
   - Student Model state (query database if exists)
   - Previous session summary (if exists)
3. Attach required documents:
   - TUTOR_PERSONA.md (always)
   - PROJECT_CONTEXT.md (always)
   - COLLABORATION_PROTOCOL.md (always)
   - STUDENT_MODEL_CONTEXT.txt (if Phase 3+)
   - SESSION_XX_SUMMARY.md (previous session, if exists)
   - PHASED_PLAN.md (optional but helpful)
4. Paste filled template to Claude
5. Begin investigation

**Session-Specific Variations:**

- **First session:** No Student Model, no previous summary
- **Phase 1 (Sessions 1-3):** Emphasize documenting learning moments
- **Phase 2 (Days 5-7):** Not an investigation session—provide analysis tasks
- **Phase 3 (Sessions 4-5):** Test Student Model, note if it helps
- **Phase 4 (Sessions 6-7):** A/B test—alternate with/without model
- **Phase 5 (Day 7):** Evaluation session, not investigation

---

## Version History

- **v1.0** (Nov 5, 2025) - Initial template with variables defined