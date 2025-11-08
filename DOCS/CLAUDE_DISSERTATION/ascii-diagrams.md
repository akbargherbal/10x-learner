# System Architecture Diagrams (ASCII)

## Instructions for Insertion

These diagrams should be inserted at the locations indicated. Each diagram is self-contained and can be copied directly into the dissertation.

---

## DIAGRAM 1: Tripartite System Architecture
**INSERT LOCATION:** Chapter 1.3 (Research Approach) after paragraph introducing dual-context architecture
**OR:** Chapter 3 introduction before 3.1 (Design Principles)

```
┌─────────────────────────────────────────────────────────────────┐
│                         THE STUDENT                             │
│                    (Human Learner/User)                         │
└──────────────────┬────────────────────────────┬─────────────────┘
                   │                            │
                   │ Updates & Queries          │ Investigates & Shares
                   │                            │
                   ▼                            ▼
        ┌──────────────────────┐    ┌──────────────────────┐
        │   STUDENT MODEL      │    │  WORKSPACE PROTOCOL  │
        │   (Persistent)       │    │  (Ephemeral)         │
        ├──────────────────────┤    ├──────────────────────┤
        │ • Concepts           │    │ • File contents      │
        │ • Mastery levels     │    │ • Grep results       │
        │ • Confidence         │    │ • Directory struct   │
        │ • Struggles          │    │ • Git history        │
        │ • Breakthroughs      │    │ • Command outputs    │
        │ • Prerequisites      │    │                      │
        │                      │    │                      │
        │ ABSTRACT             │    │ CONCRETE             │
        │ CONCEPTUAL           │    │ CODE EVIDENCE        │
        │                      │    │                      │
        │ Tool: student.py     │    │ Tools: cat, grep,    │
        │ Storage: JSON file   │    │   find, ls, git      │
        └──────────┬───────────┘    └──────────┬───────────┘
                   │                            │
                   │ Provides context           │ Provides evidence
                   │                            │
                   └──────────────┬─────────────┘
                                  │
                                  ▼
                    ┌─────────────────────────┐
                    │        CLAUDE           │
                    │   (LLM Synthesis)       │
                    ├─────────────────────────┤
                    │ • Socratic questioning  │
                    │ • Prerequisite diagnosis│
                    │ • Bridges abstract ←→   │
                    │   concrete contexts     │
                    │ • Generates updates     │
                    │                         │
                    │ Configured via:         │
                    │ Persona prompt          │
                    │ (Appendix B)            │
                    └─────────────────────────┘
                                  │
                                  ▼
                    ┌─────────────────────────┐
                    │   GROUNDED, CONTINUOUS  │
                    │   ADAPTIVE TUTORING     │
                    └─────────────────────────┘
```

**Figure Caption:**
*Figure 1: The tripartite system architecture. The Student Model provides persistent conceptual memory across all projects and sessions. The Workspace Protocol provides ephemeral concrete evidence from the current codebase. Claude synthesizes both contexts to deliver grounded, continuous tutoring. The student maintains full control over both information flows.*

---

## DIAGRAM 2: Mandatory Two-Phase Protocol
**INSERT LOCATION:** Chapter 3.5 (Collaboration Workflow) at the beginning, before Phase 1 description

```
SESSION INITIALIZATION: Mandatory Two-Phase Context Loading
═══════════════════════════════════════════════════════════

Phase 1: CONCEPTUAL CONTEXT (Student Model)
────────────────────────────────────────────
    
    Student                          Claude
       │                               │
       │  "I want to learn React      │
       │   Context API"                │
       │ ─────────────────────────────>│
       │                               │
       │                               │ REFUSES to teach
       │                               │ until context loaded
       │                               │
       │  <────────────────────────────│
       │  "Please run:                 │
       │   python student.py show      │
       │     'React Context API'       │
       │   python student.py related   │
       │     'React Context API'"      │
       │                               │
       │  [Runs commands]              │
       │  [Pastes output]              │
       │ ─────────────────────────────>│
       │                               │
       │                               │ NOW HAS:
       │                               │ • Mastery: 45%
       │                               │ • Struggles logged
       │                               │ • Prerequisites known
       │                               │
       
       ▼                               ▼
       
Phase 2: CONCRETE CONTEXT (Workspace Protocol)
───────────────────────────────────────────────

    Student                          Claude
       │                               │
       │                               │ "What file are you
       │  <────────────────────────────│  confused about?"
       │                               │
       │  "TestArea.tsx component"     │
       │ ─────────────────────────────>│
       │                               │
       │                               │ REQUESTS evidence
       │  <────────────────────────────│ (never assumes)
       │  "Run:                        │
       │   cat packages/frontend/      │
       │     src/components/           │
       │     TestArea.tsx"             │
       │                               │
       │  [Runs command]               │
       │  [Pastes output]              │
       │ ─────────────────────────────>│
       │                               │
       │                               │ NOW HAS:
       │                               │ • Actual file contents
       │                               │ • Line numbers
       │                               │ • Specific code pattern
       │                               │
       
       ▼                               ▼

Phase 3: SYNTHESIS & INVESTIGATION
──────────────────────────────────

    Student                          Claude
       │                               │
       │                               │ "Your model shows you
       │  <────────────────────────────│  struggled with provider
       │                               │  pattern. Line 50 of
       │                               │  TestArea.tsx is exactly
       │                               │  that pattern..."
       │                               │
       │                               │ Socratic question:
       │  <────────────────────────────│ "What do you think
       │                               │  useContext returns?"
       │                               │
       │  "The theme object?"          │
       │ ─────────────────────────────>│
       │                               │
       │                               │ "Let's verify. Run:
       │  <────────────────────────────│  grep -r 'ThemeContext'
       │                               │    src/"
       │                               │
       │  [Investigation continues...] │
       
       ▼                               ▼
```

**Figure Caption:**
*Figure 2: The mandatory two-phase protocol for session initialization. Claude refuses to teach until both conceptual context (Student Model) and concrete context (Workspace evidence) are loaded. This prevents both AI amnesia (teaching without memory) and assumption-based tutoring (teaching without evidence). The synthesis phase connects abstract struggles to specific code patterns.*

---

## DIAGRAM 3: Separation of Concerns
**INSERT LOCATION:** Chapter 4.3 (Workspace Protocol Implementation) at the beginning
**OR:** Chapter 3.1 (Design Principles) after "Evidence Over Assumption" principle

```
ARCHITECTURAL SEPARATION: Persistent vs. Ephemeral
═══════════════════════════════════════════════════

┌─────────────────────────┐        ┌─────────────────────────┐
│    STUDENT MODEL        │        │  WORKSPACE PROTOCOL     │
│    (student.py)         │        │  (Unix Tools)           │
├─────────────────────────┤        ├─────────────────────────┤
│                         │        │                         │
│ WHAT IT TRACKS:         │        │ WHAT IT PROVIDES:       │
│                         │        │                         │
│ • Abstract concepts     │        │ • Concrete file contents│
│   ("React Context API") │        │   (actual .tsx code)    │
│                         │        │                         │
│ • Self-assessed mastery │        │ • Search results        │
│   (0-100 scale)         │        │   (grep output)         │
│                         │        │                         │
│ • Subjective confidence │        │ • Directory structure   │
│   (low/medium/high)     │        │   (ls output)           │
│                         │        │                         │
│ • Logged struggles      │        │ • Historical context    │
│   ("provider pattern")  │        │   (git log)             │
│                         │        │                         │
│ • Captured breakthroughs│        │ • Dependency info       │
│   ("understood closures")│       │   (package.json)        │
│                         │        │                         │
│ • Prerequisite graph    │        │ • Runtime output        │
│   (manually curated)    │        │   (error messages)      │
│                         │        │                         │
├─────────────────────────┤        ├─────────────────────────┤
│                         │        │                         │
│ CHARACTERISTICS:        │        │ CHARACTERISTICS:        │
│                         │        │                         │
│ ✓ Persistent across     │        │ ✓ Ephemeral (session-   │
│   all sessions          │        │   specific)             │
│                         │        │                         │
│ ✓ Portable across       │        │ ✓ Project-specific      │
│   projects              │        │                         │
│                         │        │                         │
│ ✓ Manually maintained   │        │ ✓ Always current (from  │
│                         │        │   live workspace)       │
│                         │        │                         │
│ ✓ Simple (JSON schema)  │        │ ✓ No custom tools       │
│                         │        │   (uses cat, grep, etc.)│
│                         │        │                         │
│ ✓ Slow-changing         │        │ ✓ Fast-changing (code   │
│   (mastery evolves      │        │   changes constantly)   │
│   gradually)            │        │                         │
│                         │        │                         │
├─────────────────────────┤        ├─────────────────────────┤
│                         │        │                         │
│ WHAT IT DOES NOT DO:    │        │ WHAT IT DOES NOT DO:    │
│                         │        │                         │
│ ✗ Parse code            │        │ ✗ Store anything        │
│ ✗ Track specific files  │        │ ✗ Maintain state        │
│ ✗ Store code snippets   │        │ ✗ Track concepts        │
│ ✗ Git integration       │        │ ✗ Assess mastery        │
│ ✗ Workspace features    │        │ ✗ Persistent memory     │
│                         │        │                         │
└─────────────────────────┘        └─────────────────────────┘
           │                                    │
           │                                    │
           └──────────────┬─────────────────────┘
                          │
                          │ Both contexts flow to:
                          │
                          ▼
            ┌──────────────────────────┐
            │         CLAUDE           │
            │    (Integration Layer)   │
            ├──────────────────────────┤
            │                          │
            │ Bridges ABSTRACT ←→      │
            │         CONCRETE         │
            │                          │
            │ "Your logged struggle    │
            │  with provider pattern   │
            │  (Student Model) maps to │
            │  this code on line 50    │
            │  (Workspace evidence)..."│
            │                          │
            └──────────────────────────┘
```

**Figure Caption:**
*Figure 3: Separation of concerns between Student Model and Workspace Protocol. The Student Model tracks persistent conceptual knowledge that follows the learner across all projects and time. The Workspace Protocol provides ephemeral concrete evidence from the current project session. This architectural boundary enables both continuity (persistent model) and grounding (current code) without requiring complex integration or custom code parsing tools.*

---

## DIAGRAM 4: Evidence-Based Investigation Loop
**INSERT LOCATION:** Chapter 3.5 (Collaboration Workflow) in Phase 3 section
**OR:** Chapter 4.3 (Workspace Protocol Implementation) in "Investigation Workflow" section

```
THE INVESTIGATION LOOP: Request → Evidence → Analysis → Repeat
═══════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────┐
│                    ITERATION N                              │
│                                                             │
│  Claude                                         Student     │
│    │                                               │        │
│    │ 1. REQUEST with rationale                    │        │
│    │    "To understand X, let's find Y.           │        │
│    │     Run: grep -r 'pattern' src/"             │        │
│    │ ─────────────────────────────────────────────>│        │
│    │                                               │        │
│    │                                               │        │
│    │                                2. EXECUTE      │        │
│    │                                   command      │        │
│    │                                               │        │
│    │                                3. PROVIDE      │        │
│    │                                   exact output │        │
│    │ <─────────────────────────────────────────────│        │
│    │    [Pastes grep results showing               │        │
│    │     5 files matching 'pattern']               │        │
│    │                                               │        │
│    │                                               │        │
│    │ 4. ANALYZE evidence                           │        │
│    │    • Acknowledge what's seen                  │        │
│    │    • Point out relevant parts                 │        │
│    │    • Connect to Student Model context         │        │
│    │                                               │        │
│    │    "I see 5 matches. Look at line 3           │        │
│    │     - TestArea.tsx. This is the component     │        │
│    │     you mentioned struggling with..."         │        │
│    │                                               │        │
│    │                                               │        │
│    │ 5. SOCRATIC QUESTION or NEXT REQUEST          │        │
│    │                                               │        │
│    │    Option A: Ask clarifying question          │        │
│    │    "What do you think happens on line 50?"    │        │
│    │ ─────────────────────────────────────────────>│        │
│    │                                               │        │
│    │    OR                                         │        │
│    │                                               │        │
│    │    Option B: Request more evidence            │        │
│    │    "Let's see that file:                      │        │
│    │     cat src/components/TestArea.tsx"          │        │
│    │ ─────────────────────────────────────────────>│        │
│    │                                               │        │
└────┼───────────────────────────────────────────────┼────────┘
     │                                               │
     │                                               │
     ▼                                               ▼
┌─────────────────────────────────────────────────────────────┐
│                    ITERATION N+1                            │
│                                                             │
│    [Process repeats with new context from previous answer  │
│     or new evidence from next command]                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘


KEY PRINCIPLES:
───────────────

1. ONE COMMAND AT A TIME
   ✓ Request → Response → Analyze → Next Request
   ✗ Never: "Run these 3 commands..."

2. ALWAYS PROVIDE RATIONALE
   ✓ "To understand X, let's see Y..."
   ✗ Never: "Run: cat file.ts" (no context)

3. ANALYZE BEFORE NEXT REQUEST
   ✓ Acknowledge → Point out → Connect → Then request more
   ✗ Never: Immediately request next command without analysis

4. TIGHT FEEDBACK LOOP
   ✓ 10-30 second cycle per iteration
   ✗ Avoid: Long explanations between evidence requests

5. ADAPT BASED ON EVIDENCE
   ✓ Change investigation direction based on findings
   ✗ Never: Follow predetermined script ignoring evidence


EXAMPLE SEQUENCE:
─────────────────

Request 1: "Run: ls -la src/components/"
Evidence 1: [Shows TestArea.tsx exists]
Analysis 1: "I see TestArea.tsx. Let's examine it."
Request 2: "Run: cat src/components/TestArea.tsx"
Evidence 2: [Shows useContext on line 50]
Analysis 2: "Line 50 uses useContext. Where's the Provider?"
Request 3: "Run: grep -r 'ThemeContext.Provider' src/"
Evidence 3: [Shows Provider in App.tsx line 15]
Analysis 3: "Found it! Let's connect these pieces..."
[Socratic questioning begins based on concrete evidence]
```

**Figure Caption:**
*Figure 4: The evidence-based investigation loop. Claude requests concrete evidence with clear rationale, analyzes the output, then either asks Socratic questions or requests additional evidence. This tight feedback loop prevents assumptions, maintains focus, and models investigation methodology for the learner. The cycle repeats until sufficient context is gathered for grounded explanation.*

---

## DIAGRAM 5: Session Timeline (Optional - Information Flow)
**INSERT LOCATION:** Chapter 5.2 (Qualitative Observations) or Chapter 3.5 end
**This diagram shows temporal flow through a complete session**

```
COMPLETE SESSION TIMELINE
═════════════════════════

Time    Phase           Student Actions              Claude Actions
────    ─────           ───────────────              ──────────────

0:00    SESSION START
        
0:01    Phase 1:        Run:                         Request Student
        Conceptual      python student.py show       Model context
        Context         python student.py related    
                        
                        Paste output ──────────────> Parse context:
                                                     • Mastery: 45%
                                                     • Struggles noted
                                                     • Prerequisites: 55%

0:02    Phase 2:        Mention confusing file       Request workspace
        Workspace                                    evidence
        Context         
                        Run: cat path/to/file ─────> Receive concrete
                        Paste output                 code
                        
0:03-   Phase 3:        Answer Socratic questions    Ask questions
0:30    Investigation   
        Loop            Run: grep ... ──────────────> Request more
                        Paste output                 evidence
                        
                        Explain confusion            Analyze
                        
                        Run: cat other-file ────────> Bridge abstract
                        Paste output                 ←→ concrete
                        
                        "OH! I get it now"           Validate insight
                        
0:31    Phase 4:        Signal end:                  Summarize learning
        Session End     "Let's stop here"
                        
                                        <────────────Generate commands:
                                                     python student.py
                                                       update ...
                                                       breakthrough ...
                                                       struggle ...
                        
0:33                    Copy-paste commands
                        Execute updates
                        
0:35                    Verify:                      [Session complete]
                        python student.py show
                        
────────────────────────────────────────────────────────────────

OVERHEAD BREAKDOWN:
───────────────────

Student Model:  ~2 minutes   (0:01-0:02, 0:33-0:35)
                             Initial context + Final updates
                             
Workspace:      ~0-2 minutes (Blended into investigation)
                             Commands feel like exploration,
                             not overhead
                             
Total Overhead: ~2-4 minutes (2-4% of 90-minute session)


COGNITIVE ACTIVITIES:
─────────────────────

Student Model:  • Reflection (what did I learn?)
                • Self-assessment (mastery change?)
                • Metacognition (what still confuses me?)
                
Workspace:      • Investigation (running commands)
                • Discovery (finding patterns)
                • Analysis (understanding code)
                
Both:           • Active learning (not passive)
                • Evidence-based reasoning
                • Structured thinking
```

**Figure Caption:**
*Figure 5: Complete session timeline showing temporal flow of a typical 35-minute learning session. Student Model overhead (~2 minutes) occurs at start and end. Workspace commands blend into natural investigation workflow. Total overhead remains under 5% while providing both continuity (Student Model) and grounding (Workspace evidence). The session structure scaffolds metacognitive reflection while maintaining focus on concrete code exploration.*

---

## END OF DIAGRAMS

**Summary of Diagrams:**
- Diagram 1: High-level system architecture (tripartite)
- Diagram 2: Mandatory two-phase protocol workflow
- Diagram 3: Separation of concerns (persistent vs ephemeral)
- Diagram 4: Investigation loop mechanics
- Diagram 5: Session timeline (optional - shows temporal flow)

**Recommended Insertions:**
- Diagram 1: Chapter 1.3 or Chapter 3 introduction
- Diagram 2: Chapter 3.5 beginning
- Diagram 3: Chapter 4.3 beginning or Chapter 3.1
- Diagram 4: Chapter 3.5 Phase 3 or Chapter 4.3
- Diagram 5: Chapter 5.2 or Chapter 3.5 end (optional)

All diagrams use pure ASCII characters and should render correctly in any monospace font.