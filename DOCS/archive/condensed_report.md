# Condensed Report: The Student Model for AI-Assisted Learning Through Code Archaeology

## Introduction: The Memory Problem in AI Learning

AI language models suffer from "amnesia" across sessions, forgetting users' skills, gaps, and progress. This hinders effective teaching in technical domains like software engineering, where continuity is key. Unlike a human tutor who builds on past lessons, AI starts fresh each time, leading to inefficiency.

This report proposes the **Student Model**: a persistent system tracking what learners _don't know_ to enable adaptive AI tutoring. Drawing from the SpeedTyper-Solo project (a 38-session AI collaboration that achieved the desired outcome with the help of an LLM coding assistant while shipping code), we adapt its memory systems for learning via code archaeology—exploring codebases to uncover patterns.

Goal: Preserve comprehensiveness while halving length by merging redundancies, shortening examples, and focusing on core insights.

## Part 1: Lessons from SpeedTyper-Solo

A Python developer forked speedtyper.dev into a solo app, modifying Next.js/NestJS code, migrating databases, and optimizing startup (from 10 minutes to 4 seconds). Success relied on a **three-layer memory system**:

- **Session summaries**: Detailed markdown recaps of accomplishments, blockers, decisions, and plans.
- **Collaboration protocol**: Terminal-based workflow where the AI requests files/outputs on-demand, saving 70% tokens.
- **Strategic docs**: Stable references like tech stack overviews and roadmaps.

This created a shared problem space (the codebase), enabling compounding velocity (3x in week 1 to 166x in week 2). Summaries primarily served the AI, preventing rework.

## Part 2: Adapting to Learning Contexts

Development has clear feedback (e.g., code compiles). Learning lacks this; "unknown unknowns" hide until probed. The problem space shifts to the learner's mind: skills, gaps, history.

Without persistence, the AI can't adapt—e.g., forgetting a React hooks struggle from session 10 by 16. Human tutors build student profiles over time; AI needs a similar mechanism.

## Part 3: Avoiding Wrong Solutions

A Knowledge Graph (tracking sessions, patterns, relationships) focuses on human recall (e.g., grep summaries). But the AI needs data more. Session summaries worked in SpeedTyper-Solo because they preserved AI context; apply similarly to learning.

## Part 4: The Student Model Core

Track "what you don't know":

- **Known unknowns**: Explicit confusions.
- **Unknown unknowns**: Revealed misconceptions.
- **Mastery trajectory**: Evolving understanding (e.g., 40% hooks mastery).
- **Learning patterns**: Effective teaching styles.

**Schema (SQLite, minimal)**:

- **Concepts**: E.g., "React hooks" with category/description.
- **Mastery States**: Per-concept percentage, confidence, struggles, timestamp.
- **Events**: Logs of questions, hypotheses, reactions, applications.
- **Misconceptions**: Corrected errors (e.g., "monorepo for performance, actually versioning").
- **Teaching Approaches**: What works (e.g., Socratic vs. direct).

**Workflow**:

- Start: The AI queries model (e.g., "React hooks: 40%, struggles with cleanup").
- During: Log evidence from interactions.
- End: Update mastery (hybrid manual/auto, 5-min review).
- Validation: Confidence scores, diagnostic questions.

This enables calibration: Skip basics, anchor to knowns, save tokens (200 vs. 500+ for prose recaps).

## Part 5: Benefits and Compounding

- **Adaptive Teaching**: Calibrate explanations (e.g., link Context API to hooks knowledge).
- **Compound Learning**: Patterns transfer across projects (e.g., speedtyper-solo to monkeytype).
- **Meta-Learning**: Reveal styles (e.g., Socratic accelerates 2x; visuals for async).
- **Efficiency**: 20% more context window for exploration; velocity steepens like SpeedTyper-Solo.

**Scenarios**:

- Multi-project: Query mastery to build on priors.
- Diagnostic: Spot recurring struggles (e.g., concurrency from past sessions).
- Pattern Transfer: Reference prior exposures (e.g., defensive rendering).

## Part 6: Socratic Integration

Code archaeology uses hypothesis-evidence-synthesis. Student Model enables adaptive Socratic questions: Build on knowns (e.g., "Link to composition from speedtyper-solo"). Tracks misconceptions to intervene early.

## Part 7: Objections and Failures

- **Over-Engineering**: Start with structured summaries; database for cross-history queries.
- **Inaccuracy**: Mitigate with confidence, validation; explicit corrections.
- **Rigidity**: Treat as advisory; validate per-session.
- **Privacy**: Local SQLite, user-editable.
- **Failures**: Inaccurate tracking (underestimate mastery); optimization theater (build only after need proven); fake understanding (probe periodically).

Structured summaries may solve 80%; test first.

## Part 8: Philosophical Shifts

From knowledge retrieval to AI understanding the learner. Infrastructure for dialogue (like medical records). Embraces dynamic learning: Trajectories over static mastery.

Systems multiply output (Skill × Time × AI + Systems). Student Model amplifies learning compounding.

## Part 9: Implementation Plan

**Bootstrap**:

1. Run session 1 without model; note needed data.
2. Design schema from reality.
3. Manual population (prompts for concepts/struggles).
4. Automate (scripts for queries/updates).

**Metrics**:

- Context time → 0.
- Fewer repeats.
- Faster mastery.
- Cross-project transfer.

Refine iteratively: Week 1 proof-of-concept (3 sessions); Week 2 schema tweaks; Week 3 automation.

## Part 10: Vision and Token Economics

Long-term: Career companion for personalized, cross-domain learning. Analytics reveal meta-patterns (e.g., master architecture in 5 sessions).

Current tax: 500+ tokens/session on recaps. Model: 200 tokens query → 20% more exploration, compounding insights.

## Conclusion: Test the Hypothesis

The Student Model helps AI learn to teach, born from SpeedTyper-Solo's pragmatic systems. Solves acute memory issue in compounding learning domains.

Start small: One archaeological session to validate need. If yes, build; if no, summaries suffice. Systems serve the work—evidence-based, fast failures.
