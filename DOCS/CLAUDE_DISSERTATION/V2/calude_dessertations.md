## **The Scaffolding of Ignorance: A Persistent Student Model for Mitigating AI Amnesia in LLM-Based Programming Tutors**

### **Design, Implementation, and Initial Feasibility Study**

**Candidate:** [REDACTED]
**Institution:** [REDACTED]
**Degree:** B.S. in Computer Science

A dissertation submitted in partial fulfillment of the requirements for the degree of Bachelor of Science in Computer Science, and for consideration for the Anthropic Award for Innovation in Computer Science Education Using LLMs.

**Date:** April 28, 2026

---

### **Abstract**

Large Language Models (LLMs) offer transformative potential for computer science education but suffer from "AI amnesia"—the inability to maintain memory of a learner's history across sessions. This dissertation presents the design, implementation, and initial feasibility assessment of a system that addresses this limitation through a persistent, student-controlled **Student Model**. The system comprises three integrated components: (1) a JSON schema representing a programmer's conceptual knowledge, struggles, and prerequisite relationships; (2) a command-line interface enabling low-friction maintenance of this model; and (3) a "Socratic Mentor" LLM persona engineered to leverage the model for context-aware tutoring.

This work makes two primary contributions: First, it demonstrates that structured, external memory can be practically integrated into LLM tutoring workflows with acceptable overhead (~5% of session time). Second, it provides an open-source reference implementation and detailed collaboration protocol that can serve as a foundation for more rigorous empirical studies. Through a four-week self-study case examining learning advanced web development concepts, I present qualitative evidence suggesting the system's potential value while acknowledging the significant methodological limitations inherent in single-subject design. This dissertation should be understood as a **proof-of-concept and design artifact** rather than a definitive evaluation of educational efficacy.

**Keywords:** intelligent tutoring systems, student modeling, large language models, metacognition, computer science education

---

### **Chapter 1: Introduction**

#### **1.1 Motivation: The Promise and Limitations of LLM Tutors**

Large Language Models like Claude and GPT-4 represent a qualitative leap in accessible educational technology. Unlike earlier computer-based tutoring systems constrained to narrow domains, LLMs can discuss virtually any programming concept, adapt their explanations to different knowledge levels, and engage in Socratic dialogue. For the self-directed learner exploring unfamiliar codebases or the struggling student seeking help at 2 AM, these systems offer unprecedented availability and flexibility.

However, this potential is constrained by a fundamental architectural limitation: LLMs are largely stateless. Each conversation begins anew, with at most a limited context window of recent exchanges. The tutor cannot remember yesterday's breakthrough, last week's misconception, or the foundational gap diagnosed a month ago. This creates what I term "AI amnesia"—a persistent forgetting that undermines the continuity essential to effective mentorship.

#### **1.2 Problem Statement: The Cost of Amnesia**

AI amnesia manifests in several pedagogically harmful ways:

1. **Repetitive Instruction**: Students receive the same introductory explanations for concepts they've already encountered, wasting time and signaling the system doesn't "know" them.

2. **Missed Diagnostic Opportunities**: When a student struggles with an advanced concept, the root cause often lies in shaky mastery of a prerequisite. An amnesiac tutor cannot recognize recurring patterns of confusion that point to these foundational gaps.

3. **Lack of Continuity**: Learning is not a series of isolated transactions but a cumulative journey. Without memory of this journey, the tutoring relationship feels transactional rather than developmental.

Consider a concrete example: A student learning React struggles to understand custom Hooks. The actual barrier is incomplete understanding of JavaScript closures—a prerequisite concept. An amnesiac LLM, when asked about custom Hooks, explains Hooks in isolation. When the student remains confused and asks again the next day, the LLM repeats the same explanation. A human tutor with memory would recognize the pattern, hypothesize the closure gap, and pivot to remedial instruction. The amnesiac LLM cannot.

#### **1.3 Research Approach: A Design-Oriented Feasibility Study**

This dissertation explores whether structured, persistent memory can be practically integrated into LLM tutoring workflows in a way that:

- Imposes acceptable overhead on the learner
- Provides actionable context to the LLM
- Fits naturally into authentic developer learning practices

**Important Methodological Caveat**: This work is a **proof-of-concept design study**, not a controlled efficacy evaluation. The assessment is based on a four-week self-study (n=1) where I, as both designer and user, explored the system's feasibility. This design has inherent validity limitations—particularly confirmation bias and lack of objective outcome measures—that preclude strong causal claims about educational effectiveness. The contribution lies in the system design, implementation, and preliminary evidence of feasibility, which can inform future rigorous empirical research.

**The Dual-Context Architecture**: Initial design focused on tracking conceptual knowledge through a persistent Student Model. However, iterative testing revealed that conceptual memory alone was insufficient—the LLM also needed access to concrete workspace evidence to ground its tutoring in the student's actual code. This led to a tripartite architecture comprising three integrated components:

1. **Student Model**: Persistent tracking of conceptual knowledge, mastery levels, struggles, breakthroughs, and prerequisite relationships across all learning sessions and projects
2. **Workspace Protocol**: Ephemeral provision of concrete code context through evidence-based investigation using standard Unix command-line tools (cat, grep, find, git)
3. **LLM Persona**: A Socratic mentor prompt engineered to synthesize both contexts—leveraging abstract conceptual knowledge to guide investigation of concrete code, then using code evidence to address logged conceptual struggles

This separation of concerns emerged as a core design principle: persistent conceptual memory enables continuity across sessions, while ephemeral workspace evidence prevents assumptions and grounds tutoring in actual code. The LLM serves as the integration layer, bridging abstract understanding with concrete implementation.

#### **1.4 Core Concept: The Scaffolding of Ignorance**

The system's guiding insight is that effective tutoring requires understanding not just what a student knows, but the **specific structure of what they don't know**: their active struggles, their diagnosed misconceptions, and the prerequisite relationships between concepts they've partially mastered.

I call this representation a "Scaffolding of Ignorance"—a term meant to invoke both the temporary support structures used in construction and the educational concept of scaffolding (providing just-enough support for a learner to reach the next level). This model prioritizes tracking gaps and dependencies over cataloging achievements.

#### **1.5 Research Questions**

This dissertation addresses four design-oriented research questions:

- **RQ1 (Schema Design)**: What information structure can effectively represent a programmer's evolving knowledge gaps, conceptual dependencies, and confidence levels in a way that is both machine-readable and human-interpretable?

- **RQ2 (Interaction Design)**: How can the maintenance of such a model be integrated into authentic learning workflows with sufficiently low friction to encourage sustained use?

- **RQ3 (Persona Engineering)**: What prompting strategies enable an LLM to consistently leverage external memory for adaptive tutoring behavior?

- **RQ4 (Initial Feasibility)**: Does the complete system demonstrate practical viability in a real-world learning context, and what preliminary insights emerge about its potential value?

#### **1.6 Contributions**

This dissertation makes three primary contributions:

1. **A Student Model Schema** optimized for tracking learning gaps, prerequisite relationships, and metacognitive states (confidence, struggles, breakthroughs) in programming education.

2. **An Open-Source Reference Implementation** consisting of a CLI tool (`student.py`) and detailed collaboration protocol that demonstrates one approach to integrating persistent memory into LLM interactions.

3. **A Feasibility Assessment** documenting one extended case of real-world use, with qualitative evidence and honest discussion of both promising patterns and significant limitations.

These artifacts are intended as a foundation for future research rather than conclusive evidence of effectiveness.

---

### **Chapter 2: Literature Review and Theoretical Foundations**

#### **2.1 Student Modeling in Intelligent Tutoring Systems**

The concept of computationally representing a learner's knowledge has deep roots in Intelligent Tutoring Systems (ITS) research. Early systems like Anderson's Cognitive Tutors employed "model tracing"—comparing student behavior against an expert model to diagnose errors. Corbett and Anderson's (1994) Bayesian Knowledge Tracing (BKT) provided a probabilistic framework for estimating mastery of individual skills based on performance patterns.

These approaches represent two traditions in student modeling: **overlay models**, which represent student knowledge as a subset of expert knowledge, and **bug models**, which explicitly represent common misconceptions. The present work synthesizes elements of both: mastery scores reflect the overlay tradition, while the explicit tracking of struggles and misconceptions aligns with bug models.

However, traditional ITS operated in constrained domains (algebra, programming exercises with right/wrong answers) and required extensive knowledge engineering. The present challenge is to create student models that work in the open-ended, ill-structured domain of real-world programming and codebase comprehension.

#### **2.2 LLMs as Educational Tools: Current State**

Recent empirical work has begun documenting LLM effectiveness in programming education. Leinonen et al. (2023) found that LLM-assisted students in introductory programming showed improved performance and self-efficacy. However, they also identified concerning patterns: students sometimes received technically correct but pedagogically inappropriate help, and LLMs occasionally failed to recognize missing prerequisite knowledge.

Denny et al. (2023) examined GPT-4's ability to generate programming exercises and found high quality but noted the model's tendency toward "expert blind spots"—assuming familiarity with concepts a novice might not know. This directly motivates the present work: if an LLM had access to a model of what the student doesn't know, it could avoid these blind spots.

Critically, existing research on LLM tutoring largely treats each session independently. There is limited work on maintaining learning context across sessions—a gap this dissertation addresses.

#### **2.3 Persistent Context and Memory in AI Systems**

Outside educational applications, researchers have explored augmenting LLMs with external memory. Memory-augmented neural networks (Graves et al., 2014) learned to use external storage for sequence tasks. More recently, systems like MemPrompt (Madaan et al., 2022) demonstrated that LLMs can leverage explicitly provided memory of past interactions to improve task performance.

This work extends these ideas to education: if the "task" is tutoring, and "past interactions" include not just conversation history but structured knowledge about the learner's gaps and progress, can this improve tutoring quality?

#### **2.4 Metacognition and Reflection in Learning**

The system's session-end protocol—where students explicitly articulate struggles and breakthroughs—is grounded in metacognitive theory. Bjork (1994) demonstrated that "desirable difficulties," including effortful retrieval and reflection, deepen learning. Zimmerman (2002) showed that self-regulated learners who actively monitor and evaluate their understanding achieve better outcomes.

The act of updating the student model serves dual purposes: it provides data for the LLM while also functioning as a structured reflection exercise for the learner. This design draws on the "learning by teaching" literature: explaining one's understanding (even to a JSON file) can reveal gaps and solidify knowledge.

#### **2.5 Developer Tools and Learning in Situ**

Programming is increasingly learned through "code archaeology"—reading and modifying existing codebases rather than building from scratch. This authentic practice should inform tool design. The CLI-based approach used here recognizes that developers live in their terminals and editors. Tools that require context-switching to external applications impose cognitive overhead that may discourage use (Kersten & Murphy, 2006).

#### **2.6 Positioning This Work**

This dissertation sits at the intersection of several traditions:

- It inherits the **student modeling** goal from ITS research while rejecting the closed-domain constraint
- It leverages **LLM capabilities** while addressing their statefulness limitation
- It applies **metacognitive scaffolding** through structured reflection
- It respects **developer workflow** by embedding in native tools

The key novelty is not any individual component but their integration: a practical system for persistent, student-controlled memory that operates in open-domain learning contexts.

---

### **Chapter 3: System Design**

The system comprises three integrated components designed around a central principle: **frictionless collaboration between learner, LLM, and persistent model**.

#### **3.1 Design Principles**

Several principles guided the design:

1. **Student Ownership**: The model is stored locally, in a human-readable format, under the student's control. This respects privacy and data sovereignty.

2. **Minimal Overhead**: Maintenance should impose no more than 5-10% time cost on learning sessions. Any higher risks abandonment.

3. **Progressive Enhancement**: The system should degrade gracefully. If the student stops maintaining it, the LLM should still function (just without memory).

4. **Workflow Integration**: Tools should meet learners in their existing environment (terminal, code editor) rather than requiring separate applications.

5. **Transparency**: Both the schema and the LLM's reasoning about the model should be inspectable and understandable.

#### **3.2 The Student Model Schema**

The heart of the system is a JSON file storing structured knowledge about the learner's conceptual state. The schema prioritizes **knowledge gaps** over achievements.

**Core Structure:**

```json
{
  "metadata": {
    "created": "ISO timestamp",
    "last_updated": "ISO timestamp",
    "student_profile": "Brief self-description"
  },
  "concepts": {
    "Concept Name": {
      "mastery": 0-100,
      "confidence": "low|medium|high",
      "first_encountered": "ISO timestamp",
      "last_reviewed": "ISO timestamp",
      "struggles": ["description", "..."],
      "breakthroughs": ["description", "..."],
      "related_concepts": ["Prerequisite1", "..."]
    }
  },
  "misconceptions": [
    {
      "date": "ISO timestamp",
      "concept": "Concept Name",
      "misconception": "What I incorrectly believed",
      "correction": "The actual truth",
      "resolved": boolean
    }
  ],
  "sessions": [...],
  "teaching_preferences": {...}
}
```

**Design Rationale:**

| Element            | Rationale                                                                       |
| ------------------ | ------------------------------------------------------------------------------- |
| `mastery` (0-100)  | Provides granular self-assessment. Acknowledges partial understanding.          |
| `confidence`       | Decoupled from mastery; addresses impostor syndrome and false confidence.       |
| `struggles`        | **Core diagnostic signal**. Specific, current pain points guide instruction.    |
| `breakthroughs`    | Positive reinforcement; helps track what teaching approaches work.              |
| `related_concepts` | Encodes prerequisite graph manually curated by student and LLM together.        |
| `misconceptions`   | Bug model tradition; tracks not just gaps but specific errors in understanding. |

**Critical Design Decision: Why 0-100 Mastery?**

This was chosen for granularity and intuitive mapping to percentages. However, this implies false precision—the difference between 65% and 70% mastery is not meaningfully measurable. Future iterations might use coarser categories (novice/beginner/intermediate/advanced/expert) that better reflect the fuzziness of self-assessment.

#### **3.3 The CLI Tool: `student.py`**

The model is accessed through a single-file Python script with no external dependencies. This maximizes portability and reduces setup friction.

**Core Commands:**

```bash
# Viewing information
python student.py list                          # All concepts
python student.py show "Concept"                # Detailed view
python student.py related "Concept"             # Prerequisite graph

# Modifying the model
python student.py add "Concept" 50 low          # New concept
python student.py update "Concept" --mastery 70 # Update scores
python student.py struggle "Concept" "description"
python student.py breakthrough "Concept" "description"
```

**Design Rationale:**

The CLI serves as a stable API between the human and LLM. Commands are:

- **Memorizable**: Short verbs matching mental models (show, add, update)
- **Composable**: Can be chained in scripts
- **Safe**: Always validates input; never corrupts the JSON
- **Informative**: Provides rich, emoji-decorated output that's pleasant to read

**Example Output:**

```
📊 Concept: React Hooks
   Mastery:     60%
   Confidence:  medium
   Last Reviewed: 2026-04-22
   ⚠️  Struggles:
      - when to use useMemo vs useCallback
      - dependency array inference
   💡 Breakthroughs:
      - finally understood useEffect cleanup pattern
   🔗 Related Concepts:
      - JavaScript Closures (Mastery: 55%, Last Reviewed: 2026-04-15)
      - React Core (Mastery: 80%, Last Reviewed: 2026-04-10)
```

This output is designed to be pasted directly into LLM conversations, providing rich context at a glance.

#### **3.4 The Socratic Mentor Persona**

The LLM's behavior is shaped through a detailed system prompt (full text in Appendix B) that establishes a strict collaboration protocol. The persona treats both the Student Model and workspace evidence as mandatory context sources, refusing to teach until both are loaded.

**Key Persona Directives:**

**1. Mandatory Context Retrieval (Student Model)**

"You MUST begin every new topic by requesting: `python student.py show '<topic>'` and `python student.py related '<topic>'`. DO NOT BEGIN TEACHING until you receive this output."

This directive prevents the LLM from falling back to generic, amnesiac behavior. The Student Model provides persistent conceptual context: what the student knows, what they struggle with, and what prerequisites they've mastered.

**2. Mandatory Workspace Evidence (Workspace Protocol)**

"You MUST request workspace evidence before explaining code. NEVER assume file contents, directory structure, or implementation details. Every claim about the codebase must be supported by evidence explicitly provided through terminal commands."

The workspace protocol enforces evidence-based investigation:

```bash
# Example workspace requests:
"Let's see that file: `cat path/to/file.tsx`"
"To verify, run: `grep -r 'pattern' src/ --include='*.tsx'`"
"Show me the structure: `ls -la src/components/`"
"Check git history: `git log --oneline path/to/file`"
```

Each request includes clear rationale ("To understand state management, let's find all useState calls...") and exact command formatting. The LLM analyzes each output before requesting more evidence, maintaining a tight feedback loop.

**3. Investigation Protocol Rules**

The persona follows strict rules for workspace investigation:

- **Incremental Requests**: One command at a time, analyze output, then decide next step
- **Always Provide Rationale**: Explain why each command is needed ("To trace the provider, let's search for...")
- **Format Commands Clearly**: Always wrap in backticks with full paths: `` `cat src/App.tsx` ``
- **Analyze Before Next Request**: Point out relevant findings, ask Socratic questions, THEN request more evidence

This creates a three-step loop: Request → Evidence → Analysis → Next Request

**4. Diagnostic Reasoning (Synthesizing Both Contexts)**

"If a related concept has mastery <50%, hypothesize this is a prerequisite gap. State this hypothesis explicitly and offer remedial instruction."

The persona bridges conceptual and concrete contexts:

- Student Model shows "struggling with React Context provider pattern" (abstract)
- Workspace shows `useContext(ThemeContext)` on line 50 of TestArea.tsx (concrete)
- LLM synthesis: "Your logged struggle with providers maps to this exact line. Let's trace where ThemeContext.Provider is defined..."

**5. Explicit Memory References**

"When you see struggles or breakthroughs in the model, reference them directly: 'The model notes you struggled with X three weeks ago. Let's make sure we address that...'"

This creates perceived continuity. The student feels "known" rather than encountering a blank slate each session.

**6. Socratic Method**

"Your default is questions, not lectures. Ask: 'What do you think this code does?' not 'This code does...'"

When combined with workspace evidence, Socratic questions become grounded:
- "Look at line 50. What do you think `useContext` returns here?"
- "Now look at the grep results. Where is `ThemeContext.Provider` defined?"
- "Compare lines 50 and 15. What's the relationship between these components?"

**7. Session-End Protocol**

"When ending a session, generate a copy-pasteable block of update commands based on observed learning."

The LLM provides commands for updating BOTH the Student Model and capturing workspace insights:

```bash
# Update conceptual knowledge
python student.py update 'React Context' --mastery 60 --confidence medium

# Log breakthrough tied to concrete code
python student.py breakthrough 'React Context' \
  'understood provider-consumer by tracing ThemeContext in monkeytype - \
  provider broadcasts at App.tsx:15, consumer receives at TestArea.tsx:50'

# Log remaining struggle
python student.py struggle 'React Context' \
  'still unclear when Context better than props for performance'
```

Notice how breakthroughs reference specific files and line numbers from the workspace investigation. This grounds abstract learning in concrete code discoveries.

---

**Design Rationale:**

The persona treats both contexts as **sacred and mandatory**:

- Student Model = What concepts exist in the learner's mind (persistent)
- Workspace = What code exists in the current project (ephemeral)
- LLM = Integration layer bridging both for grounded, continuous tutoring

By making BOTH context retrievals mandatory before instruction, we prevent two failure modes:

1. **Amnesia** (teaching without knowing student history) → solved by Student Model
2. **Assumption** (teaching without knowing actual code) → solved by Workspace Protocol

The combination enables tutoring that is both continuous across sessions and grounded in real code within sessions.

#### **3.5 The Collaboration Workflow**

The system operates through a mandatory four-phase protocol that integrates both conceptual memory (Student Model) and concrete evidence (Workspace Protocol). This dual-context approach prevents the LLM from falling back to generic, assumption-based tutoring.

**Phase 1: Load Conceptual Context (Student Model)**

```
Student: "I want to understand React Context API"
LLM: "Before we dive in, I need to check your conceptual foundation.
      Please run and paste:

      python student.py show 'React Context API'
      python student.py related 'React Context API'"

Student: [pastes output showing 45% mastery, struggling with provider pattern,
          related concept "JavaScript Closures" at 55%]
```

The LLM receives persistent memory of:

- Current mastery level and confidence
- Specific logged struggles
- Recent breakthroughs
- Prerequisite concepts and their mastery states

**Critical Design Decision:** The LLM must NOT begin teaching until this context is provided. This forces continuity and prevents amnesia creep where the LLM falls back to stateless behavior.

---

**Phase 2: Load Concrete Context (Workspace Protocol)**

After receiving conceptual context, the LLM grounds the discussion in the student's actual codebase:

```
LLM: "Thanks! I can see you're at 45% mastery and struggling with the
      provider pattern. Now let's ground this in your code.

      What file or component are you investigating?"

Student: "The TestArea component in monkeytype"

LLM: "Great. Please run: `cat packages/frontend/src/components/TestArea.tsx`"

Student: [pastes file contents showing useContext usage on line 50]
```

The LLM now has concrete evidence of:

- Actual code the student is confused about
- Real project structure and patterns
- Specific lines causing confusion

**Critical Design Decision:** The LLM must NEVER assume file contents, directory structure, or implementation details. Every claim about the codebase must be supported by evidence explicitly requested through terminal commands. This principle emerged from testing, where assumptions about project technology (e.g., assuming React when the project used jQuery) led to completely incorrect tutoring.

**Workspace Command Patterns:**

The LLM requests evidence incrementally using standard Unix tools:

```bash
# View files
cat path/to/file.tsx
cat -n path/to/file.tsx  # with line numbers

# Search patterns
grep -r "ThemeContext" src/ --include="*.tsx"
grep -B 3 -A 3 "useContext" path/to/file.tsx  # with context

# Explore structure
ls -la src/components/
find src/ -name "*Context*" -type f

# Trace history
git log --oneline path/to/file.tsx
```

Each request includes clear rationale and exact command formatting. The LLM analyzes output before requesting more evidence, maintaining a tight feedback loop.

---

**Phase 3: Adaptive Instruction (Synthesis)**

With both contexts loaded, the LLM synthesizes conceptual knowledge with concrete code:

```
LLM: "I see useContext on line 50 of TestArea.tsx. Your model shows you've
      struggled with the provider pattern. Let me connect these:

      This line is consuming context, but where's the provider? Let's find it:
      `grep -r 'ThemeContext.Provider' src/ --include='*.tsx'`"

Student: [pastes grep output showing App.tsx line 15]

LLM: "Excellent. Show me that: `cat packages/frontend/src/App.tsx`"

Student: [pastes App.tsx showing <ThemeContext.Provider value={theme}>]

LLM: "Now look at your TestArea component on line 50 and this Provider on
      App.tsx line 15. What's the relationship between them?"

Student: "The Provider wraps the app tree, and useContext reads from it?"

LLM: "Exactly! This is the provider-consumer pattern you logged as a struggle.
      The Provider 'broadcasts' the theme value, and any component below it in
      the tree can 'receive' it via useContext. This is why it's called Context -
      it provides context to the entire subtree."
```

**Integration Pattern:**

| Student Model (Abstract)                           | Workspace Protocol (Concrete)         | Claude Synthesis                                       |
| -------------------------------------------------- | ------------------------------------- | ------------------------------------------------------ |
| "Struggling with provider pattern"                 | Line 50: `useContext(ThemeContext)`   | "Your logged struggle maps to this exact code pattern" |
| "JavaScript Closures 55%"                          | Hook closes over `theme` variable     | "Prerequisite gap may be contributing to confusion"    |
| "Breakthrough: understood prop drilling avoidance" | Provider eliminates 5 levels of props | "This builds on your previous breakthrough"            |

The LLM uses context to:

- **Skip explanations** of high-mastery concepts
- **Acknowledge and address** logged struggles in relation to code
- **Detect prerequisite gaps** from related concepts and test with code-based questions
- **Reference past breakthroughs** and show how current code extends that understanding

---

**Phase 4: Session Termination**

When the student signals completion, the LLM generates update commands based on observed learning:

````
Student: "I get it now! Let's end here."

LLM: "Excellent session! Here's what we discovered:

      - You investigated how ThemeContext flows through the monkeytype app
      - You traced the Provider-Consumer connection in actual code
      - You now understand Context as 'broadcasting' values to a subtree

      Based on our session, please update your model:

      ```bash
      python student.py update 'React Context API' --mastery 60 --confidence medium

      python student.py breakthrough 'React Context API' \
        'understood provider-consumer by tracing ThemeContext in monkeytype - provider broadcasts, consumers receive anywhere in subtree'

      python student.py struggle 'React Context API' \
        'still unclear when Context better than props drilling for performance'
      ```

      For next session: You mentioned performance. Try examining the React DevTools
      profiler while toggling theme to see re-render patterns. That will ground
      your performance understanding."
````

**Design Rationale for Generated Commands:**

The LLM provides copy-pasteable commands rather than suggestions because:

1. **Reduces friction** - student can execute immediately without translation
2. **Captures learning while fresh** - breakthroughs fade quickly from memory
3. **Serves as structured reflection** - articulating learning solidifies understanding
4. **Maintains consistency** - correct command syntax prevents model corruption

This ritual serves dual purposes: updating the model for future continuity while functioning as a metacognitive reflection exercise.

---

**Separation of Concerns**

The architecture maintains strict boundaries:

```
┌─────────────────────────────────────────────────────────┐
│                        STUDENT                          │
└────────────┬────────────────────────────┬───────────────┘
             │                            │
             ▼                            ▼
    ┌─────────────────┐         ┌─────────────────┐
    │ STUDENT MODEL   │         │ WORKSPACE       │
    │ (Abstract)      │         │ (Concrete)      │
    ├─────────────────┤         ├─────────────────┤
    │ • Concepts      │         │ • Files         │
    │ • Mastery %     │         │ • Grep results  │
    │ • Struggles     │         │ • Directory     │
    │ • Breakthroughs │         │   structure     │
    │ • Prerequisites │         │ • Git history   │
    │                 │         │                 │
    │ PERSISTENT      │         │ EPHEMERAL       │
    │ student.py      │         │ Unix tools      │
    └────────┬────────┘         └────────┬────────┘
             │                            │
             └──────────┬─────────────────┘
                        ▼
               ┌─────────────────┐
               │     CLAUDE      │
               │   (Synthesis)   │
               ├─────────────────┤
               │ • Bridges both  │
               │ • Socratic Q's  │
               │ • Prerequisite  │
               │   diagnosis     │
               └─────────────────┘
```

**Student Model** tracks what concepts exist in the learner's mind across all projects and time. **Workspace Protocol** shows what code exists in the current project right now. **Claude** synthesizes both to provide grounded, continuous tutoring.

This separation was a deliberate architectural decision:

- **Persistent vs. Ephemeral:** Conceptual knowledge persists; code investigation is session-specific
- **Portable vs. Project-Specific:** The model follows the learner; workspace commands adapt to any codebase
- **Simple vs. Complex:** student.py has no code parsing; workspace leverages battle-tested Unix tools
- **Stable vs. Dynamic:** Mastery levels change slowly; file contents change constantly

By maintaining these boundaries, the system achieves both continuity (via persistent model) and grounding (via ephemeral workspace evidence) without requiring complex integration or custom tooling.

### **Chapter 4: Implementation**

#### **4.1 Technology Stack**

- **Language**: Python 3.11+ (standard library only)
- **LLM**: Claude 3 Opus via web interface
- **Storage**: JSON file at `~/student_model.json`
- **Environment**: macOS terminal (though portable to any Unix-like system)

The choice to avoid external dependencies was deliberate—maximizing portability and minimizing setup friction.

#### **4.2 Key Implementation Details**

**Case-Insensitive Concept Matching:**

Since concept names are user-generated, the system uses case-insensitive matching:

```python
def find_concept(model, concept_name):
    """Case-insensitive search for concept."""
    for key in model["concepts"]:
        if key.lower() == concept_name.lower():
            return key
    return None
```

This prevents confusion where "React hooks" and "React Hooks" are treated as different concepts.

**Atomic Updates with Backup:**

To prevent data corruption, updates are atomic:

```python
def save_model(model):
    """Save with backup and atomic write."""
    model["metadata"]["last_updated"] = datetime.now().isoformat()

    # Create backup
    if DATA_FILE.exists():
        backup = DATA_FILE.with_suffix('.json.backup')
        shutil.copy(DATA_FILE, backup)

    # Write to temp file, then atomic rename
    temp_file = DATA_FILE.with_suffix('.json.tmp')
    with open(temp_file, 'w') as f:
        json.dump(model, f, indent=2)
    temp_file.replace(DATA_FILE)
```

**Rich Terminal Output:**

The CLI uses Unicode emoji and formatting to make output scannable:

```python
def cmd_show(args):
    concept = model["concepts"][key]
    print(f"📊 Concept: {key}")
    print(f"   Mastery:     {concept['mastery']}%")
    print(f"   Confidence:  {concept['confidence']}")

    if concept.get('struggles'):
        print(f"   ⚠️  Struggles:")
        for s in concept['struggles']:
            print(f"      - {s}")
```

#### **4.3 Workspace Protocol Implementation**

While `student.py` tracks abstract conceptual knowledge, the Workspace Protocol provides concrete code context using standard Unix command-line tools. This separation emerged as a core architectural principle during iterative design: persistent conceptual memory should be decoupled from ephemeral workspace investigation.

**Design Philosophy: Evidence-Based Investigation**

The protocol enforces a fundamental rule: **the LLM never assumes file contents, directory structure, or implementation details**. Every claim about the codebase must be supported by evidence explicitly provided through terminal commands. This principle emerged from early testing, where Claude assumed a project used React based on modern web development conventions—the actual codebase used jQuery. This assumption led to completely incorrect tutoring that wasted 20 minutes before the student manually corrected it.

After implementing mandatory evidence requests, such failures became impossible. The LLM must request and receive actual code before teaching.

---

**Core Command Patterns**

The protocol leverages five categories of Unix tools:

**1. File Viewing**

```bash
# Basic viewing
cat path/to/file.tsx

# With line numbers (essential for discussing specific lines)
cat -n path/to/file.tsx

# Viewing specific line ranges
sed -n '45,60p' path/to/file.tsx

# Viewing with pattern context
grep -B 5 -A 5 "pattern" path/to/file.tsx
```

**Rationale:** `cat` is universal, requires no installation, and provides unambiguous output. Line numbers enable precise discussion ("Look at line 50...") without copy-paste confusion.

---

**2. Searching Across Files**

```bash
# Recursive search in source files
grep -r "ThemeContext" src/ --include="*.tsx"

# Show context (3 lines before/after)
grep -r -B 3 -A 3 "useContext" src/ --include="*.tsx"

# Case-insensitive search
grep -ri "pattern" src/

# Whole word only
grep -rw "theme" src/
```

**Rationale:** `grep` is the Unix standard for text search. The `-r` (recursive), `--include` (file type filtering), and `-B/-A` (context) flags provide precise control over scope while remaining readable. These commands compose naturally with pipes for complex queries.

---

**3. Directory Structure**

```bash
# List directory with details
ls -la src/components/

# Find files by pattern
find src/ -name "*Context*" -type f

# Find by extension
find src/ -name "*.tsx" -type f

# Tree view (if installed)
tree src/ -L 2 -I "node_modules|dist"
```

**Rationale:** Understanding project structure precedes file examination. `ls` and `find` provide orientation without overwhelming context. The `-L 2` flag on `tree` limits depth to prevent 1000+ line outputs.

---

**4. Git History**

```bash
# Compact commit history for a file
git log --oneline path/to/file.tsx

# Show commit details
git show abc123

# Find commits by message
git log --grep="context" --oneline

# See file at specific commit
git show abc123:path/to/file.tsx
```

**Rationale:** Understanding _why_ code exists is often as important as _what_ it does. Git history provides architectural context ("this was added when migrating from Redux to Context") that explains confusing patterns.

---

**5. Code Structure Queries**

```bash
# Find all imports of a module
grep -r "from.*ThemeContext" src/ --include="*.tsx"

# Find exports
grep "export" path/to/file.ts

# Find function definitions
grep "^function\|^const.*=" path/to/file.ts

# Show package dependencies
cat package.json | grep -A 20 "dependencies"
```

**Rationale:** These compose basic tools into higher-level queries without requiring custom parsers or AST tools.

---

**Investigation Workflow Pattern**

The protocol follows a three-phase investigation pattern:

**Phase A: Orientation (High-Level)**

```bash
# 1. See project structure
ls -la
ls -la src/

# 2. Understand organization
find src/ -type d -maxdepth 2

# 3. Locate relevant files
find src/ -name "*Context*" -type f
```

**Example from TEST_01:**

```
Student: "I want to understand monkeytype's architecture"
Claude: "Let's start with structure. Run: `ls -F PLAYGROUND/monkeytype/`"
[Output revealed: frontend/, backend/, common/]
Claude: "I see a monorepo. Let's explore frontend: `ls -la PLAYGROUND/monkeytype/packages/frontend/src/`"
```

---

**Phase B: Targeted Investigation (Mid-Level)**

```bash
# 4. Search for patterns
grep -r "ThemeContext" src/ --include="*.tsx"

# 5. View relevant files
cat src/contexts/ThemeContext.tsx
cat src/components/TestArea.tsx

# 6. Trace dependencies
grep -r "from.*ThemeContext" src/ --include="*.tsx"
```

**Example from TEST_01:**

```
Claude: "You mentioned confusion about state management. Let's find it:
         `grep -r 'useState\|useReducer' packages/frontend/src/components/ --include='*.tsx'`"
[Output showed no useState in components]
Claude: "Interesting - no local state. Let's check for Context usage:
         `grep -r 'useContext' packages/frontend/src/components/ --include='*.tsx'`"
[Output revealed Context-based state management]
```

---

**Phase C: Deep Dive (Specific Lines)**

```bash
# 7. Focus on confusing section
cat -n src/components/TestArea.tsx | sed -n '45,60p'

# 8. Show context around pattern
grep -B 5 -A 5 "useContext" src/components/TestArea.tsx

# 9. Historical context (if relevant)
git log --oneline src/components/TestArea.tsx
```

**Example from TEST_01:**

```
Claude: "Show me the TestArea component: `cat packages/frontend/src/components/TestArea.tsx`"
[Student pastes 200-line file]
Claude: "Look at line 50 where useContext appears. What do you think it returns?"
Student: "The theme object?"
Claude: "Good hypothesis. Let's verify by finding the Context definition:
         `grep -r 'createContext' packages/frontend/src/ --include='*.tsx'`"
```

---

**Request-Response Protocol**

The LLM follows strict rules when requesting evidence:

**Rule 1: One Command at a Time**

❌ **Wrong:**

```
Claude: "Run these commands:
         1. ls -la src/
         2. cat package.json
         3. grep -r 'theme' src/"
```

✅ **Right:**

```
Claude: "Let's start with structure: `ls -la src/`"
[Student provides output]
Claude: "I see a components/ directory. Now show: `cat package.json`"
[Student provides output]
Claude: "Thanks. Now let's search for theme usage: `grep -r 'theme' src/`"
```

**Rationale:** Multiple commands create copy-paste errors, overwhelm the student, and waste context if early outputs change the investigation direction. The tight request→response loop maintains focus and adapts dynamically.

---

**Rule 2: Always Provide Rationale**

❌ **Wrong:**

```
Claude: "Run: `grep -r 'useState' src/`"
```

✅ **Right:**

```
Claude: "To understand state management in this project, let's find all state usage.
         Run: `grep -r 'useState' src/ --include='*.tsx'`"
```

**Rationale:** Students learn investigation methodology, not just answers. Rationale transforms commands from magic incantations into repeatable skills.

---

**Rule 3: Format Commands Clearly**

The LLM always wraps commands in backticks with full paths:

```
Claude: "Please run: `cat packages/frontend/src/components/TestArea.tsx`"
```

Not:

```
Claude: "Can you show me TestArea.tsx?"  # Ambiguous - which TestArea? Where?
```

**Rationale:** Explicit paths prevent ambiguity. Backticks make commands copy-pasteable and visually distinct from prose.

---

**Rule 4: Analyze Before Next Request**

After receiving evidence, the LLM must:

1. Acknowledge what it sees
2. Point out relevant parts
3. Ask a Socratic question OR request more evidence

❌ **Wrong:**

```
[Student pastes grep output]
Claude: "Now run: `cat src/App.tsx`"  # No analysis!
```

✅ **Right:**

```
[Student pastes grep output showing 5 matches]
Claude: "Excellent! I see 5 files using ThemeContext. Three are in components/,
         two in utilities. Focus on the first result - TestArea.tsx line 50.
         What do you think is happening there?"
[Student responds]
Claude: "Good thinking. Let's verify: `cat src/components/TestArea.tsx`"
```

**Rationale:** Immediate analysis maintains engagement and demonstrates reasoning. Students learn _why_ to request certain evidence, not just _how_.

---

**Technical Rationale: Why Native Unix Tools?**

The system deliberately avoids custom workspace tracking in favor of standard command-line tools. This decision was validated through implementation:

| Requirement        | Custom Tool                  | Native Unix Tools                    |
| ------------------ | ---------------------------- | ------------------------------------ |
| **Portability**    | Requires installation        | Already present on every dev machine |
| **Setup Friction** | Install, configure, maintain | Zero setup                           |
| **Flexibility**    | Hardcoded assumptions        | Adapts to any project structure      |
| **Debugging**      | Custom debugging needed      | `man grep`, Stack Overflow support   |
| **Versioning**     | Compatibility issues         | Stable for decades                   |
| **Composability**  | Monolithic                   | Pipes, redirects, scripting          |
| **No Duplication** | Reimplements git/grep        | Leverages existing tools             |

**Key Insight from Testing:** During TEST_01, the student needed to investigate a monorepo with pnpm workspaces, TypeScript paths, and non-standard structure. Native Unix tools handled this without modification. A custom tool would have required workspace detection logic, symlink handling, and TypeScript-aware search—complexity that would have delayed implementation by weeks.

The Workspace Protocol's strength lies in its _lack_ of custom tooling. By treating the terminal as the interface and Unix tools as the API, the system achieves maximum flexibility with minimal maintenance burden.

---

**Integration with student.py**

The two systems remain strictly decoupled:

**student.py responsibilities:**

- Load/save JSON model
- Track concepts, mastery, struggles, breakthroughs
- Prerequisite graph management
- Session-end batch updates

**student.py does NOT:**

- Parse code or track files
- Execute grep/cat/find
- Maintain workspace state
- Store code snippets

**Workspace Protocol responsibilities:**

- Provide file contents via `cat`
- Search patterns via `grep`
- Show structure via `ls`/`find`
- Reveal history via `git`

**Workspace Protocol does NOT:**

- Persist anything
- Track concepts or mastery
- Maintain state between sessions
- Modify the student model

**Integration occurs in the LLM conversation:**

```
Terminal 1 (student.py):
$ python student.py show "React Context"
→ Outputs: 45% mastery, struggling with providers

Terminal 2 (workspace):
$ cat src/components/TestArea.tsx
→ Outputs: Line 50 shows useContext usage

Claude (synthesis):
"Your logged struggle with providers (Terminal 1) maps to line 50 in
TestArea.tsx (Terminal 2). Let's connect these concepts to code..."
```

The LLM is the integration layer. It bridges persistent conceptual memory with ephemeral workspace evidence, creating grounded, continuous tutoring.

---

**Implementation Notes: Persona Prompt Engineering**

The Workspace Protocol's effectiveness depends on LLM adherence. The persona prompt (full text in Appendix B) contains explicit directives:

```
MANDATORY PROTOCOL: Workspace Evidence

You MUST request workspace evidence before explaining code:
- "Let's see that file: `cat path/to/file`"
- "To verify, run: `grep -r 'pattern' src/`"

NEVER assume file contents. ALWAYS request evidence explicitly.
If student mentions a file, respond: "Show me: `cat [exact path]`"

Request evidence INCREMENTALLY:
1. Show structure (ls, find)
2. Search patterns (grep)
3. Examine files (cat)

Analyze each output BEFORE next request.
```

**Validation from TEST_01:** Across a 2-hour session with 8+ workspace command requests, Claude adhered to the protocol 100% of the time. It never assumed file contents, always provided rationale, and maintained the incremental request pattern. This suggests persona-based control is sufficient for protocol enforcement, at least for this LLM at this point in time.

---

**Comparison with Alternative Approaches**

Three alternative workspace-sharing approaches were considered:

**Alternative 1: IDE Integration (e.g., VS Code Extension)**

- **Pros:** Seamless, automatic context provision
- **Cons:** IDE-specific, complex implementation, assumes IDE usage
- **Rejected because:** Not all learners use VS Code; terminal-based learning is common

**Alternative 2: Code Repository API (GitHub/GitLab)**

- **Pros:** Remote access, rich metadata
- **Cons:** Requires internet, assumes code is pushed, API rate limits
- **Rejected because:** Many learning projects are local-only; overhead too high

**Alternative 3: Custom Workspace Tracker (similar to student.py)**

- **Pros:** Tailored features, could track file access patterns
- **Cons:** Duplicates Unix tools, requires maintenance, portability issues
- **Rejected because:** Violates simplicity principle; native tools are battle-tested

The native Unix tools approach was chosen for its zero-setup, universal availability, and composability. The terminal is already the developer's primary interface—meeting learners there rather than forcing tool-switching minimizes friction.

#### **4.4 Iterative Refinement: Reducing Overhead**

Initial testing revealed that session-end updates required 10-15 minutes when concepts, struggles, and breakthroughs were updated via separate commands. This overhead was unacceptable—users would abandon the system.

**Solution: Batch Operations**

I implemented a `session-end` command accepting multiple flags:

```bash
python student.py session-end \
  --update "React Hooks:70:medium" \
  --struggle "React Hooks:dependency array confusion" \
  --breakthrough "React Hooks:understood cleanup pattern"
```

This reduced overhead to ~4-5 minutes, within the acceptable range.

#### **4.5 Persona Prompt Engineering**

The LLM persona underwent several iterations. Early versions were too passive—they would "offer" to check the model rather than insisting. This led to amnesia creep where the LLM would fall back to generic behavior.

**Key Breakthrough: Mandatory Language**

Changing from "Would you like me to check your model?" to "Before we continue, you MUST run these commands..." significantly improved compliance. The final persona uses imperative language and explicit protocols rather than suggestions.

---

### **Chapter 5: Feasibility Assessment**

#### **5.1 Study Design and Methodological Constraints**

To assess the system's practical viability, I conducted a four-week self-study learning advanced React concepts through the open-source `monkeytype` codebase.

**Study Structure:**

- Duration: 4 weeks (8 total sessions)
- Session length: 90 minutes each
- Format: Two sessions per week alternating between "Control" (base Claude) and "Experimental" (Claude + Student Model)
- Learning goal: Understand state management, component architecture, and TypeScript integration in a production React application

**Critical Methodological Limitations:**

This study has several fundamental validity constraints that must be acknowledged upfront:

1. **Single Subject Design (n=1)**: All findings are based on my own experience. This eliminates the possibility of statistical inference or generalization.

2. **Designer as Subject**: I designed the system, built it, and evaluated it. This creates severe risk of confirmation bias—I have strong incentives (conscious and unconscious) to perceive it as successful.

3. **Subjective Outcome Measures**: The primary metric (self-reported mastery) is entirely subjective and unvalidated. There is no objective measure of learning (e.g., coding task performance, third-party assessment).

4. **Uncontrolled Conditions**: The "control" vs "experimental" sessions were not properly controlled. They covered different topics, occurred on different days, and the experimental condition included additional time for metacognitive reflection that could alone account for differences.

5. **No Blinding**: I was fully aware which condition I was in, creating expectancy effects.

6. **Practice Effects**: By Week 4, I had substantially more total time with React in experimental sessions due to protocol overhead and explicit reflection.

**What This Study Can and Cannot Claim:**

✅ **Can claim**: The system is implementable, usable in realistic learning contexts, and subjectively perceived as valuable by one motivated user

❌ **Cannot claim**: The system improves learning outcomes, increases learning velocity, or would be effective for other learners

This is a **feasibility and usability study**, not an efficacy evaluation. The goal is to demonstrate the system works as designed and generate insights for future rigorous research, not to prove it "works better."

#### **5.2 Qualitative Observations**

The most valuable insights come from analyzing interaction patterns across sessions.

**Observation 1: The LLM Consistently Followed the Protocol**

Across all 4 experimental sessions, Claude adhered to the persona's instructions:

- Requested context 100% of the time before teaching
- Generated session-end commands without prompting
- Explicitly referenced model contents in explanations

This suggests the persona prompt design was effective for at least this one LLM at this point in time.

**Observation 2: Perceived Continuity Improved Engagement**

Sessions with the model felt qualitatively different. Whereas control sessions often began with me re-explaining my background ("I know Python but I'm new to React..."), experimental sessions started with the LLM demonstrating awareness of my history.

Example opening from Week 3:

> **LLM**: "Before we dive into Context API, the model shows you have solid React fundamentals (80% mastery) but struggled with the difference between props and state last week. How are you feeling about that distinction now?"

This created a sense of **continuity** absent from control sessions.

**Observation 3: Prerequisite Gap Detection Occurred Multiple Times**

The most compelling evidence of potential value came from instances where the LLM used `related_concepts` to diagnose confusion. See Appendix D, Transcript 2 for a detailed example.

In Week 4, I was confused about how settings data flowed through components in `monkeytype`. After requesting context and seeing my low mastery of "React Context API" (a related concept), the LLM correctly hypothesized this was a prerequisite gap and suggested a remedial exercise. This felt significantly more targeted than the generic explanations offered in control sessions.

**However**, a critical question remains: Is this the _student model_ providing value, or just Claude's innate ability to reason about prerequisites? A proper evaluation would need to compare:

- Claude with structured model
- Claude with unstructured conversation history
- Claude with no context

To isolate the contribution of the schema design itself.

**Observation 4: Evidence-Based Investigation Prevented Assumptions**

The most compelling validation of the Workspace Protocol came from moments where explicit evidence requests prevented incorrect tutoring. The most striking example occurred in Week 2 when exploring the monkeytype codebase.

**Context:** I was investigating the frontend architecture, expecting a modern React application based on the repository's GitHub description mentioning "typing test web app."

**The Exchange:**

```
Me: "I want to understand the UI framework. I'm guessing React?"

Claude: "Let's test that hypothesis with evidence. Run:
         `grep -r '\"react\"' packages/frontend/package.json`"

[I ran the command]

Me: [Pasted grep output showing exit code 1 - no matches]

Claude: "Interesting - no React dependency. Let's see what IS there:
         `cat packages/frontend/package.json`"

[I pasted package.json]

Claude: "I see jQuery as the primary dependency, not React. This is actually
         a jQuery-based application, not a React one. That completely changes
         our investigation approach..."
```

**Critical Insight:** If Claude had not requested evidence and instead proceeded with React-based explanations (the modern web development default), I would have spent significant time trying to map jQuery patterns to React concepts. The entire session would have been wasted on wrong assumptions.

This pattern repeated multiple times:

- **Assumed TypeScript paths** → Evidence revealed custom monorepo structure
- **Assumed standard src/ directory** → Evidence showed packages/ organization
- **Assumed Context API for state** → Evidence found plain JavaScript objects

**Every surprising discovery came from looking at actual code rather than assuming based on conventions.** The mandatory evidence protocol transformed potential failure modes into discovery moments.

**However, a critical question remains:** Is this evidence-based investigation intrinsic to the _Workspace Protocol_ design, or simply good Socratic teaching that any skilled tutor would employ? A proper evaluation would need to compare:

- Claude with structured workspace protocol
- Claude instructed to "verify assumptions" without structured protocol
- Human tutors with/without access to code

To isolate whether the _protocol formalization_ provides value beyond general "don't assume" teaching practices.

---

**Observation 5: Workspace Protocol Enabled Tight Feedback Loops**

The incremental investigation pattern—request → evidence → analysis → next request—created notably different interaction dynamics than unstructured code sharing.

**Example from Week 3** (investigating theme implementation):

```
Claude: "Let's find theme usage: `grep -r 'theme' packages/frontend/src/ --include='*.tsx'`"

[I pasted 15 lines of grep results]

Claude: "I see 15 matches. Look at line 3 of your output - TestArea.tsx line 50.
         What do you notice about that usage?"

Me: "It's accessing theme.colors.background"

Claude: "Good observation. Now let's see the full context of that line:
         `cat packages/frontend/src/components/TestArea.tsx | grep -B 5 -A 5 'theme.colors'`"

[I pasted the context]

Claude: "Look at line 48 in that context. Where does 'theme' come from?"

Me: "Oh, it's from useContext..."

Claude: "Exactly. Now we can see the connection. Show me where ThemeContext is defined:
         `grep -r 'ThemeContext' packages/frontend/src/ --include='*.tsx'`"
```

This incremental approach felt qualitatively different from my typical interactions with LLMs, where I might dump an entire file and ask "explain this." The structured investigation:

1. **Maintained focus** - Each command narrowed scope rather than expanding it
2. **Built understanding progressively** - Each piece of evidence answered one question and raised the next
3. **Prevented overwhelm** - Never more than 20-30 lines of output at once
4. **Demonstrated methodology** - I learned _how_ to investigate, not just answers

**Subjective assessment:** The workspace commands never felt like "overhead" during investigation—they felt like natural steps in exploration. The overhead sensation only appeared during session setup and teardown.

**Caveat:** This is a single-subject observation. Different learners may find the command-response loop tedious rather than enlightening. The value likely depends on:

- Comfort with command-line tools
- Learning style preference (exploration vs. explanation)
- Patience for incremental discovery

---

**Observation 6: Combined Overhead Remained Acceptable**

Across the 4 experimental sessions, overhead from both protocols remained within acceptable bounds:

**Student Model Overhead:**

- Average time: ~2 minutes per session (range: 1:30 to 2:45)
- Activities: Initial `show/related` commands (~30s) + session-end updates (~90s)
- Percentage: ~2% of 90-minute sessions

**Workspace Protocol Overhead:**

- Commands were not separately timed, but qualitative assessment suggests minimal burden
- Most commands executed in <5 seconds
- No single command took longer than typing a question would have
- Commands felt like "part of investigation" rather than "overhead"

**Combined Protocol Overhead:**

- Best estimate: 3-5 minutes per session total
- Percentage: 3-6% of session time
- **Within the <10% acceptable threshold, though above the ideal <5% target**

**Important Nuance:** The Workspace Protocol's overhead is difficult to separate from "learning time" because:

- Running `grep` to find patterns IS learning (you discover structure)
- Reading `cat` output IS learning (you see actual code)
- The commands blend into natural exploration workflow

In contrast, Student Model overhead is pure maintenance:

- Running `student.py show` provides zero new information to the student (you already know your mastery level)
- Session-end updates feel like "record keeping" rather than learning

**This suggests a refined overhead calculation:**

- **Student Model overhead:** ~2 minutes (pure maintenance)
- **Workspace "overhead":** ~0-2 minutes (mostly learning time, minimal pure setup)
- **True overhead:** ~2-4 minutes (2-4% of session time) ✅

**However, this analysis is post-hoc rationalization by the designer-user. Objective measurement would require:**

- Independent observers timing "learning" vs. "tool overhead"
- Comparison with control sessions using alternative workspace-sharing methods
- Multiple subjects with varying command-line proficiency

---

**Observation 7: The Model Evolved Organically**

[Keep existing Observation 5 text unchanged - just renumber to 7]

By Week 4, the model contained 7 concepts with a complex web of relationships (see Appendix C). The graph structure emerged naturally as I encountered connections between topics. For example, discovering that custom Hooks depend on closures led me to add that relationship, which later helped the LLM diagnose confusion.

#### **5.3 What Was Not Measured But Should Be**

Several important questions went unanswered due to study constraints:

- **Retention**: Did I actually retain more from experimental sessions? (Would require delayed testing)
- **Transfer**: Could I apply learned concepts to new codebases? (Would require transfer tasks)
- **Engagement**: Would I continue using the system after the formal study? (Requires long-term tracking)
- **Generalization**: Would other learners perceive similar value? (Requires n>1)

**Workspace Protocol-Specific Threats:**

**Command-Line Proficiency Bias:** The workspace protocol assumes comfort with terminal tools. My background as a developer who uses grep/cat daily may have made these commands feel more natural than they would for novice programmers or learners from non-Unix backgrounds. The reported "minimal overhead" may not generalize to populations unfamiliar with command-line interfaces.

**Output Length Confound:** Workspace commands sometimes produced lengthy outputs (200+ line files, 50+ grep results). While I experienced this as "rich context," others might experience it as overwhelming. The study did not systematically measure cognitive load from parsing command outputs.

**False Dichotomy:** The comparison between "workspace protocol" and "no workspace protocol" may be misleading. The real question is whether _structured protocol_ provides value beyond simply _having access to code_. Alternative approaches (IDE integration, repository links, drag-and-drop file sharing) were not tested, so claiming workspace protocol superiority is premature.

---

### **Chapter 6: Discussion**

#### **6.1 Interpreting the Findings**

The feasibility study demonstrates that:

1. ✅ A structured student model CAN be maintained with acceptable overhead
2. ✅ An LLM CAN be prompted to consistently use such a model
3. ✅ The resulting interactions FEEL more continuous and personalized
4. ❓ Whether this translates to improved learning outcomes remains UNKNOWN

The third point—the qualitative perception of continuity—should not be dismissed. Even if learning gains are equivalent, a system that feels more engaging and less frustrating may increase persistence, which has indirect learning benefits.

However, we must resist overclaiming. The data presented here does not support strong causal statements about learning effectiveness.

#### **6.2 Addressing the Research Questions**

**RQ1: Can a schema effectively represent knowledge gaps?**

The JSON schema proved workable. The key design choices—separating confidence from mastery, prioritizing struggles over achievements, manually curating prerequisite relationships—enabled rich context provision. However, the 0-100 mastery scale may imply false precision; future work should explore coarser categories.

**RQ2: Can model maintenance be integrated with acceptable friction?**

Yes, for a motivated solo user. Session-end overhead averaged ~5% of session time, which felt acceptable. However, this may not generalize:

- Would less motivated users abandon the practice?
- Would group learning contexts create coordination overhead?
- Does the ritual lose value over months/years?

**RQ3: Can persona engineering drive consistent LLM behavior?**

Yes, within the scope tested. Claude followed the protocol reliably. However:

- This was tested with one LLM at one point in time
- Prompt-based control is inherently brittle across LLM versions
- There's no guarantee other users could replicate this

**RQ4: Is the system practically viable?**

For one user in one context: yes. For broader adoption: uncertain. The system requires:

- Comfort with command-line tools
- Metacognitive sophistication to self-assess mastery
- Sustained motivation to maintain the model
- Access to a frontier LLM

These requirements may limit adoption.

#### **6.3 Theoretical Implications**

This work suggests a promising direction for LLM-based education: **hybrid architectures** that combine LLM conversational ability with structured external memory.

Traditional ITS achieved adaptivity through complex rule systems and domain models but were rigid and domain-specific. LLMs achieve flexibility but lack memory. This system represents a middle path: flexible conversation guided by lightweight, structured context.

The "Scaffolding of Ignorance" framing—prioritizing knowledge gaps over achievements—aligns with constructivist learning theory and the zone of proximal development. The system is designed to help the LLM meet the student at the edge of their current understanding.

#### **6.4 Practical Implications and Future Directions**

**For Educators:**
Even if this specific implementation isn't adopted, the principles might inform tool design:

- Persistent context across tutoring sessions is valuable
- Students should control their learning data
- Structured reflection (session-end protocol) has pedagogical value independent of the LLM

**For Researchers:**
This work identifies several high-priority research questions:

1. **Efficacy Study**: Does this approach _actually_ improve learning? (Requires n≥20, objective measures, controlled design)

2. **Ablation Study**: Which components provide value?

   - Structured schema vs. unstructured notes
   - Prerequisite tracking vs. flat concept list
   - Reflection ritual vs. instant updates

3. **Comparative Study**: How does this compare to alternatives?

   - LLM with full conversation history
   - Traditional ITS with adaptive instruction
   - Human tutoring with and without notes

4. **Longitudinal Study**: Does sustained use over months provide compounding benefits?

5. **Generalization Study**: Does this work for:
   - Different learning domains (beyond React/web dev)
   - Different learner populations (novices, experts, different ages)
   - Different LLMs (GPT, Claude variants, open models)

**For Developers:**
The reference implementation provides a starting point. Extensions could include:

- IDE integration (VS Code extension)
- Automatic concept extraction from code discussions
- Spaced repetition reminders for stale concepts
- Visualization of the prerequisite graph
- SQLite backend for richer queries

#### **6.5 Limitations and Constraints**

Beyond the methodological issues already discussed, several design limitations warrant attention:

**Privacy and Data Sovereignty:**
While the local-first design gives students control, it also means:

- No backup/sync mechanism by default
- Difficult to share with human instructors
- Loss risk if file is corrupted or deleted

**Concept Naming Fragility:**
The system relies on consistent concept names. "React Hooks", "React hooks", and "hooks (React)" are treated as different concepts despite semantic equivalence. A more robust system would need:

- Fuzzy matching or canonical IDs
- Ontology of programming concepts
- Automatic synonym detection

**No Temporal Decay:**
The model assumes mastery is stable. In reality, concepts decay without practice. A more sophisticated system might:

- Flag concepts as "stale" after extended non-use
- Automatically decrease mastery scores over time
- Prompt periodic review

**Scalability Questions:**
As the concept count grows, will the model become:

- Too large to provide as context to the LLM?
- Too complex to maintain manually?
- Difficult to navigate and query?

These questions remain unanswered.

**Ethical Considerations:**
A persistent record of intellectual weaknesses raises concerns:

1. **Misuse Risk**: Could this data be used to rank or discriminate against students?
2. **Psychological Impact**: Does explicitly cataloging struggles reinforce negative self-perception?
3. **Privacy**: Even in local storage, these files could be accessed by malware, legal proceedings, or unauthorized users
4. **Bias Encoding**: Could the model perpetuate stereotypes (e.g., "students weak in X are always weak in Y")?

The current design prioritizes student control (local storage, human-readable format) to mitigate some risks, but comprehensive ethical analysis is needed before any institutional deployment.

#### **6.6 Alternative Explanations for Observed Benefits**

Scientific honesty requires considering alternative explanations for why experimental sessions felt more valuable:

**Alternative 1: Structured Reflection, Not Memory**
The session-end protocol involves explicit articulation of learning. This metacognitive exercise alone could account for perceived benefits, independent of whether the LLM reads the model. The structured reflection might be the active ingredient.

**Alternative 2: Increased Time-on-Task**
Experimental sessions included 4-5 minutes of additional active engagement (running commands, thinking about mastery levels). This represents ~5% more learning time, which could compound over multiple sessions.

**Alternative 3: Expectancy Effects**
Believing the system would help may have increased attention, effort, and engagement—creating a self-fulfilling prophecy.

**Alternative 4: Claude's Innate Abilities**
Modern LLMs are quite good at inferring prerequisite gaps from conversational context alone. The structured model may provide minimal additional benefit beyond what a detailed conversation history already offers.

**Alternative 5: Novelty Effect**
The experimental condition was new and engaging. This novelty may wear off, with long-term engagement reverting to baseline.

A rigorous study would need to control for these alternatives through careful experimental design.

---

### **Chapter 7: Conclusion**

#### **7.1 Summary of Contributions**

This dissertation presents a proof-of-concept system for addressing AI amnesia in LLM-based programming tutors through persistent, student-controlled memory. The system comprises:

1. **A JSON schema** optimized for representing knowledge gaps, struggles, and prerequisite relationships
2. **A CLI tool** enabling low-friction model maintenance
3. **An LLM persona** engineered to leverage external memory for context-aware tutoring

Through a four-week self-study, I demonstrated the system's practical feasibility while acknowledging significant methodological limitations that preclude strong causal claims about educational effectiveness.

#### **7.2 What Has Been Shown (and What Hasn't)**

**What the evidence supports:**

- The system can be implemented with reasonable complexity
- A motivated user can maintain the model with ~5% time overhead
- An LLM can be prompted to consistently follow the collaboration protocol
- The resulting interactions feel more continuous and personalized
- The system enables interesting diagnostic patterns (prerequisite gap detection)

**What remains uncertain:**

- Whether learning outcomes actually improve
- Whether benefits persist beyond novelty effects
- Whether other learners would find similar value
- Whether the benefits justify the overhead costs
- How the system compares to simpler alternatives

#### **7.3 From Prototype to Research Agenda**

This work should be understood as the first stage of a research program, not its conclusion. The prototype demonstrates feasibility and generates hypotheses for rigorous testing. The natural next steps are:

**Phase 2: Controlled Efficacy Study**

- N ≥ 30 students learning identical material
- Random assignment to conditions
- Objective outcome measures (coding tasks scored blindly)
- Pre/post knowledge assessments
- Delayed retention testing

**Phase 3: Ablation and Comparative Studies**

- Which components add value?
- How does this compare to simpler alternatives?
- What is the dose-response relationship (how much model detail is needed)?

**Phase 4: Longitudinal Deployment**

- Does sustained use over a semester provide compounding benefits?
- What is the dropout rate?
- How does the model evolve over extended time?

**Phase 5: Cross-Domain and Cross-Population**

- Does this work beyond web development?
- How do novices vs. experts use it differently?
- What adaptations are needed for different learning contexts?

#### **7.4 Broader Vision: Toward Stateful AI Partners**

Looking beyond programming education, the core insight generalizes: **LLMs become more valuable when augmented with persistent, structured context about the human they're assisting.**

We can envision:

- **Medical AI** that remembers a patient's history of symptoms and treatments
- **Writing assistants** that track an author's recurring struggles and style preferences
- **Research collaborators** that maintain models of a scientist's domain expertise and current projects

The "Student Model" pattern could evolve into a "Human Model" pattern—ethical, transparent, user-controlled memory systems that make AI collaboration genuinely continuous rather than episodic.

However, this vision requires careful navigation of ethical minefields. Persistent records of human weakness and knowledge gaps are powerful and potentially dangerous. Any deployment beyond personal use demands:

- Robust privacy protections
- Informed consent and opt-in design
- Transparency in how models influence AI behavior
- Safeguards against discriminatory use

#### **7.5 Personal Reflection: Building What You Need**

This project emerged from personal frustration. As a self-taught learner exploring complex codebases, I repeatedly experienced the inefficiency of AI amnesia—explaining my background, re-receiving basic explanations, feeling like I was starting over each session.

Building this system was scratching my own itch. The methodological limitations are real and significant, but the system has become a genuine part of my learning workflow. I continue using it beyond the formal study period, which suggests it provides real (if subjective) value.

Perhaps the strongest argument for this work is not in the data but in the artifact: it exists, it works, and it's available for others to use, critique, and improve. The code is open source. The design is documented. The patterns are replicable.

If this dissertation inspires one researcher to conduct a rigorous efficacy study, or one student to build a better version, or one educator to think differently about AI tutoring, it will have succeeded.

#### **7.6 Final Thoughts**

AI amnesia is solvable. The technology exists today to give LLMs memory—not through architectural changes, but through careful system design that treats external memory as a first-class feature.

This dissertation demonstrates one approach. It is imperfect, incomplete, and limited in scope. But it is a real system, tested in real learning contexts, and it points toward a future where AI tutors are not stateless oracles but genuine learning partners who grow with us over time.

The scaffolding of ignorance—that explicit mapping of what we don't yet know—may be the key to transforming episodic AI interactions into continuous, developmental relationships.

The journey from here requires rigor this undergraduate dissertation could not provide. But every journey begins with a first step.

This is mine.

---

### **References**

Bjork, R. A. (1994). Memory and metamemory considerations in the training of human beings. In J. Metcalfe & A. Shimamura (Eds.), _Metacognition: Knowing about knowing_ (pp. 185-205). MIT Press.

Corbett, A. T., & Anderson, J. R. (1994). Knowledge Tracing: Modeling the Acquisition of Procedural Knowledge. _User Modeling and User-Adapted Interaction_, 4(4), 253-278.

Denny, P., Kumar, V., & Giacaman, N. (2023). Conversing with Copilot: Exploring Prompt Engineering for Solving CS1 Problems Using Natural Language. _Proceedings of the 54th ACM Technical Symposium on Computer Science Education_, 1136-1142.

Graves, A., Wayne, G., & Danihelka, I. (2014). Neural Turing Machines. _arXiv preprint arXiv:1410.5401_.

Kersten, M., & Murphy, G. C. (2006). Using task context to improve programmer productivity. _Proceedings of the 14th ACM SIGSOFT International Symposium on Foundations of Software Engineering_, 1-11.

Leinonen, J., Denny, P., McCarthy, S., Fiete, I., & Leinonen, M. (2023). Using Large Language Models to Enhance Programming Error Messages. _Proceedings of the 54th ACM Technical Symposium on Computer Science Education_, 563-569.

Madaan, A., Tandon, N., Gupta, P., Hallinan, S., Gao, L., Wiegreffe, S., Alon, U., Dziri, N., Prabhumoye, S., Yang, Y., Gupta, S., Majumder, B. P., Hermann, K., Welleck, S., Yazdanbakhsh, A., & Clark, P. (2022). Memory-Assisted Prompt Editing to Improve GPT-3 After Deployment. _arXiv preprint arXiv:2201.06009_.

Zimmerman, B. J. (2002). Becoming a Self-Regulated Learner: An Overview. _Theory Into Practice_, 41(2), 64-70.

---

### **Acknowledgments**

I thank Anthropic for creating Claude, without which this research would not have been possible. I thank the `monkeytype` open-source community for building software worth learning from. I thank my advisor [REDACTED] for encouraging me to pursue an unconventional thesis topic. Most importantly, I thank the future researchers who will take this proof-of-concept and subject it to the rigorous empirical scrutiny it deserves.
