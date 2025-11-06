# Student Model: Project Context

**Last Updated:** November 5, 2025  
**Current Phase:** Pre-Implementation (Phase 0)  
**Session Count:** 0 archaeological sessions completed

---

## What This Project Is

The Student Model is a system that helps AI assistants (like me) understand what a learner doesn't know yet, so we can teach more effectively across multiple sessions.

**The Core Problem:** AI language models have no memory between sessions. If you tell me in session 5 that you struggle with React hooks, I'll know it temporarily. By session 15, I'll have forgotten unless you tell me again. This makes learning inefficient—every session requires re-explaining your background, skill level, and learning history.

**The Solution:** A lightweight SQLite database that tracks:
- Concepts you're learning (e.g., "React useEffect", "monorepo architecture")
- Your current mastery level for each concept (0-100%)
- Your learning trajectory over time (how understanding evolves)
- Misconceptions that have been discovered and corrected
- Which teaching approaches work best for you

**Why This Matters:** Unlike development projects where the problem space is the codebase, in learning the problem space is the student's mind. I can't see what you understand or struggle with unless you tell me. The Student Model preserves that information across sessions, enabling adaptive teaching that compounds over time.

---

## What We're NOT Building

- ❌ A knowledge graph for you to query your learning
- ❌ A comprehensive note-taking system
- ❌ A curriculum or course structure
- ❌ An automated assessment tool
- ❌ A productivity tracker

The Student Model is FOR ME (the AI), not for you. You already have your own memory. I don't.

---

## The Learning Method: Code Archaeology

We're using "archaeological sessions" to explore existing codebases and learn architectural patterns by reverse-engineering decisions.

**The Protocol:**
1. **Identify confusion point** - Pick something in a codebase you don't understand
2. **Form hypothesis** - "I think they did this because..."
3. **Gather evidence** - Inspect files, git history, documentation
4. **Revise understanding** - Test hypothesis against evidence
5. **Synthesize pattern** - Extract the generalizable lesson
6. **Document discovery** - Log what changed in your understanding

**Why Archaeology?** Unlike traditional learning (lecture → practice), archaeology builds genuine understanding by having you investigate real production code and discover patterns yourself. It's Socratic teaching applied to software.

**Starting Confusion Point:** Monkeytype's monorepo architecture - why multiple package.json files, how packages relate, what problem this solves.

---

## Collaboration Protocol

We follow a terminal-first workflow similar to the SpeedTyper-Solo project:

**How We Work Together:**
1. You tell me what confusion point we're exploring
2. I request specific files: "Please run `cat packages/backend/package.json`"
3. You copy-paste the output
4. I analyze and ask diagnostic questions
5. We iterate until you've synthesized the pattern
6. We document what changed in your understanding

**Why This Protocol:**
- Saves tokens (I only see files I need, when I need them)
- Shares the same workspace (you see what I see)
- Makes evidence explicit (no assumptions about file contents)
- Enables precise investigation (I can request exactly what's needed)

**Critical:** I cannot see your filesystem, terminal output, or open files unless you share them. Always wait for my explicit file requests rather than uploading entire codebases.

---

## Your Current State

**Background:**
- Strong Python backend developer (self-rated 8/10)
- Learning frontend: React, TypeScript, Next.js
- Recently completed SpeedTyper-Solo fork project (38 sessions)
  - Went from 20% React proficiency to 75%
  - Learned through doing, not courses
  - Built session summary system that preserved context

**Current Skill Levels (Self-Reported):**
- React basics: 70% (components, JSX, props)
- React hooks: 40% (useState solid, useEffect struggles)
- TypeScript: 60% (basic typing, generics unclear)
- Next.js: 50% (pages work, advanced features unknown)
- Monorepo architecture: 10% (seen it, don't understand it)

**Learning Patterns:**
- Prefers hands-on exploration over theory-first
- Learns well through Socratic questioning
- Benefits from connecting new concepts to Python knowledge
- Needs concrete examples before abstract explanations
- Time constraint: 1-2 hours per session max

**Projects Completed:**
1. SpeedTyper-Solo (38 sessions, Oct-Nov 2024)
   - Forked multiplayer typing app → solo local version
   - Migrated PostgreSQL → SQLite
   - Removed Docker, multiplayer, auth
   - Improved startup time 150x (10min → 4sec)
   - Built session summary system for context preservation

**Active Confusion Points:**
1. **Monorepo architecture** (starting point)
   - Why multiple package.json files?
   - How do packages share code?
   - What's the purpose vs monolith?
   - What problem does this solve?

---

## Success Metrics for This Project

**How We'll Know It's Working:**

1. **Context Restoration Time:** How long you spend at session start explaining your background
   - Target: <2 minutes (vs current ~5-10 minutes)

2. **Teaching Calibration:** How often I explain things you already know or confuse you with advanced material
   - Target: "Just right" explanations >80% of the time

3. **Learning Velocity:** Sessions needed to go from "confused" to "can apply independently"
   - Baseline: TBD from first 3 sessions
   - Target: Improve by 30% with Student Model

4. **Cross-Project Transfer:** Whether I recognize when you've seen a pattern before in different codebases
   - Target: Explicitly link to past learning >70% of the time

**Tracking Method:** At the end of each session, you'll rate 1-5:
- How well calibrated was my teaching? (too basic / just right / too advanced)
- Did I waste time explaining things you already knew?
- Did I reference your past learning appropriately?

---

## The Student Model Schema (Proposed)

**NOT YET IMPLEMENTED** - This is the working hypothesis after the first few sessions prove the need.

**Table 1: concepts**
- Tracks individual units of knowledge
- Fields: name, category, description, first_encountered_date

**Table 2: mastery_states**
- Current understanding of each concept
- Fields: concept_id, mastery_percentage, confidence, last_updated, current_struggles (text)

**Table 3: mastery_events**
- History log of learning moments
- Fields: concept_id, timestamp, event_type (question/hypothesis/success/failure), evidence (text)

**Table 4: misconceptions**
- Incorrect beliefs discovered and corrected
- Fields: concept_id, misconception (text), correction (text), discovered_date, resolved

**Table 5: teaching_approaches**
- What works for this learner
- Fields: approach_type (socratic/example/diagram/etc), effectiveness_rating, concept_id, notes

**Population Strategy:** Hybrid
- Automatic: I observe your interactions and propose updates during session
- Manual: You confirm/correct my assessments at session end (~5 minutes)
- Similar to SpeedTyper session summaries: I draft, you finalize

---

## Current Phase: Week 1 (Validation)

**Goal:** Prove that code archaeology generates valuable learning insights before building any infrastructure.

**What We're Doing:**
- Days 1-4: Run 2-3 archaeological sessions (monorepo confusion point)
- Days 5-7: Analyze what happened to your understanding
- Deliverable: Evidence-based schema requirements

**What We're NOT Doing Yet:**
- Building databases
- Writing population scripts
- Automating anything

**Why This Order:** The SpeedTyper-Solo session summaries weren't designed upfront—they emerged from the pain of lost context. Similarly, the Student Model schema should emerge from actual archaeological sessions, not theoretical speculation.

---

## Key Files & Resources

**This Session:**
- `REPORT_10X_LEARNER.md` - The full theoretical foundation (you don't have access to this in future sessions)
- `speedtyper_plan.md` - Reference implementation plan format

**To Be Created:**
- `PROJECT_CONTEXT.md` - This document (for future Claude sessions)
- `PHASED_PLAN.md` - Two-week implementation roadmap
- `SESSION_01_SUMMARY.md` - First archaeological session documentation
- `STUDENT_MODEL_SCHEMA.sql` - Database schema (Week 2)

**Monkeytype Repository:**
- URL: https://github.com/monkeytypegame/monkeytype
- Focus: packages/ directory structure
- Starting files: Root package.json, packages/*/package.json

---

## Session Handoff Protocol

**When starting a new session, the human will provide:**
1. This project context document
2. The phased plan
3. Previous session summary (if exists)
4. Current phase indicator (e.g., "Starting Phase 1, Session 2")
5. Any specific files to analyze

**What I should do:**
1. Read context doc to understand project state
2. Check phase goals and current progress
3. Review previous session summary for continuity
4. Begin with calibration question: "Last session we explored X and you understood Y. Does that still feel accurate?"
5. Request specific files as needed (never assume I have access)

**What I should NOT do:**
- Re-explain the Student Model concept (it's in this doc)
- Ask you to upload entire codebases
- Make assumptions about file contents
- Forget that this system is FOR ME, not for you

---

## Critical Reminders for Future Claude

1. **The human already has SpeedTyper-Solo experience** - They know how to write session summaries, follow protocols, build pragmatically. Don't lecture about these topics.

2. **Evidence over theory** - We're following SpeedTyper-Solo methodology: working solutions, incremental testing, fast failure detection. Don't over-engineer.

3. **I'm the primary user** - The Student Model exists so I can understand this learner better across sessions. It's not a productivity tool for them.

4. **Time constraints are real** - Sessions are 1-2 hours max. Keep archaeological investigations focused and achievable.

5. **Socratic teaching is the method** - Ask diagnostic questions, guide investigation, let them discover patterns. Don't lecture unless they explicitly ask.

6. **Context is never free** - Always request files explicitly. Never assume you know file contents. The protocol exists for a reason.

---

## Questions to Ask If Context Is Missing

If you're starting a session and something is unclear:

- "Which phase are we in? What's the goal for today?"
- "What was your mastery level for X concept last session?"
- "Can you share the previous session summary?"
- "What confusion point are we exploring today?"
- "Which files should I request to start investigating?"

Don't proceed with assumptions. Ask.

---

## Version History

- **v0.1** (Nov 5, 2025) - Initial context document, pre-implementation
- **Future versions will log:** Phase completions, schema iterations, metric improvements
