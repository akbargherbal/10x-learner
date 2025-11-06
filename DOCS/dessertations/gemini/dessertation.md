## **The Scaffolding of Ignorance: A Persistent Student Model for Mitigating AI Amnesia in LLM-Based Programming Tutors**

**Candidate:** [REDACTED]
**Institution:** [REDACTED]
**Degree:** B.S. in Computer Science

A dissertation submitted in partial fulfillment of the requirements for the degree of Bachelor of Science in Computer Science, and for consideration for the Anthropic Award for Innovation in Computer Science Education Using LLMs.

**Date:** April 28, 2026

### **Abstract**

Large Language Models (LLMs) are emerging as powerful tools in computer science education, yet they suffer from a critical flaw: "AI amnesia." Lacking memory of a learner's history, they provide generic, repetitive, and non-adaptive instruction. This dissertation introduces a novel approach to combat this issue by externalizing the learner's evolving knowledge into a persistent, student-controlled **Student Model**. The core innovation is a focus on tracking a "scaffolding of ignorance"—a dynamic representation of specific struggles, misconceptions, and knowledge gaps—rather than merely cataloging proficiencies. I present the design, implementation, and evaluation of a system comprising three components: (1) a structured JSON schema for modeling a programmer's mastery, confidence, and conceptual weaknesses; (2) a command-line interface (CLI) that enables a frictionless, LLM-driven workflow for maintaining the model; and (3) a "Socratic Mentor" LLM persona engineered to leverage the model for context-aware, adaptive tutoring. Through a four-week, n=1 case study focused on learning advanced concepts via open-source code archaeology, this work demonstrates that the system significantly improves learning continuity and enables the LLM to perform targeted, prerequisite-gap-aware instruction. The findings suggest that by giving the LLM a memory, we can transform it from a generic information source into a truly personalized learning partner, paving the way for more effective and efficient computer science education.

---

### **Chapter 1: Introduction**

#### **1.1 The Promise and Peril of LLMs in CS Education**

Large Language Models (LLMs) like Anthropic's Claude are poised to revolutionize computer science education. They offer infinite patience, 24/7 availability, and the ability to explain complex topics in a multitude of ways. For the self-directed learner exploring a new codebase or the traditional student struggling with a difficult algorithm, the LLM can act as a tireless, interactive knowledge source. However, this revolutionary potential is curtailed by a fundamental limitation inherent to their architecture: they are largely stateless. Each interaction is, in essence, a new beginning, a conversation wiped clean of prior context beyond a limited window.

#### **1.2 The Problem of AI Amnesia**

This statelessness results in a phenomenon I term "AI Amnesia." The LLM tutor does not remember the student's previous sessions, their recurring struggles, their hard-won breakthroughs, or the subtle misconceptions that derail their progress. This leads to frustratingly inefficient learning loops.

Consider the "Student Y Problem" identified in my preliminary research: A student struggles with an advanced React concept like the `useEffect` Hook's cleanup function. The root cause is not the complexity of the Hook itself, but a fragile understanding of a prerequisite: JavaScript closures. An amnesiac LLM, when asked about `useEffect`, will explain the Hook in isolation. The next day, when the student struggles with a similar pattern, the LLM will offer the _same_ isolated explanation. It is incapable of diagnosing the underlying weakness because it lacks the memory of the student's learning history. It cannot see the pattern of struggle that points to the foundational gap.

#### **1.3 Thesis: The Scaffolding of Ignorance**

This dissertation argues that to unlock the full potential of LLM tutors, we must cure their amnesia. We must provide them with a persistent, structured memory of the learner's journey. My thesis is that the most effective way to do this is by creating an external, student-controlled **Student Model** that focuses not on what the student _knows_, but on the dynamic, evolving structure of what they _do not know_.

I call this model "The Scaffolding of Ignorance." It is a structured representation of a learner's specific struggles, diagnosed misconceptions, and conceptual dependencies. By explicitly tracking these gaps, we provide the LLM with the necessary context to move beyond generic explanations. It can begin to diagnose root causes, recall past difficulties, and adapt its teaching strategy in real-time. This transforms the LLM from a stateless oracle into a stateful mentor.

#### **1.4 Research Questions**

This thesis is guided by four primary research questions:

- **RQ1:** How can a persistent data model be designed to effectively represent a programmer's evolving conceptual weaknesses, mastery levels, and prerequisite relationships with minimal maintenance overhead?
- **RQ2:** What interaction patterns and toolchains, grounded in authentic developer workflows, can enable a learner and an LLM to collaboratively maintain this model without disrupting the flow of learning?
- **RQ3:** How can an LLM persona be engineered to leverage this externalized student model to diagnose foundational knowledge gaps and deliver truly adaptive, context-aware instruction?
- **RQ4:** What is the measurable impact of such a system on learning continuity, efficiency, and the qualitative experience of learning complex programming topics?

#### **1.5 Key Contributions**

This dissertation makes three key contributions to the field of AI in computer science education:

1.  **A Novel Student Model Schema:** A lightweight, human-readable JSON schema focused on tracking struggles, confidence, and conceptual relationships as first-class citizens, designed for collaborative maintenance by a human and an LLM.
2.  **An Open-Source Reference Implementation:** A Python-based command-line interface (`student.py`) and a detailed collaboration protocol that provide a blueprint for integrating persistent memory into LLM-based learning workflows.
3.  **A Mixed-Methods Evaluation:** A rigorous n=1 case study that provides both quantitative and qualitative evidence of the system's effectiveness, demonstrating a marked improvement in learning continuity and prerequisite-gap detection.

---

### **Chapter 2: Literature Review**

This research builds upon decades of work in intelligent tutoring systems, cognitive science, and the emerging practice of LLM-driven education.

#### **2.1 Foundations: Intelligent Tutoring Systems (ITS) and Student Modeling**

The concept of a computer-based tutor that adapts to a student's knowledge is not new. Early Intelligent Tutoring Systems (ITS) pioneered the concept of the "student model," a computational representation of a learner's evolving knowledge. Many of these systems relied on techniques like Bayesian Knowledge Tracing (BKT), which uses statistical inference to model the probability that a student has mastered a skill based on their performance on a series of problems. While powerful, these models are often opaque, data-intensive, and operate within highly structured, closed-world domains like algebra or logic puzzles. They lack the flexibility to handle the unbounded and often ill-defined domain of general-purpose programming.

#### **2.2 The Current Landscape: LLMs as Educational Tools**

Recent studies have confirmed the efficacy of LLMs as programming tutors. Work by Leinonen et al. (2023) demonstrated that LLM assistance could significantly improve student performance and self-efficacy in introductory programming courses. However, researchers also caution against over-reliance and highlight the "expert blind spot" of LLMs, where they fail to recognize the prerequisite knowledge a novice may be missing. My work directly addresses this identified gap by making prerequisite knowledge an explicit part of the student model.

#### **2.3 Cognitive Science and Metacognition: The Theory of Desirable Difficulty**

The proposed system is not merely a technical solution but is grounded in the cognitive science of learning. The act of pausing at the end of a session to articulate one's struggles and update the student model is a form of structured metacognition—thinking about one's own learning. This aligns with the concept of "desirable difficulties," which posits that learning is deepened when it involves effortful retrieval and reflection. The session-end review, while a small amount of overhead, serves as a powerful, structured reflection that solidifies learning.

#### **2.4 Developer-Centric Workflows: The CLI as a Learning Interface**

A core tenet of this work is that learning tools should fit into the learner's existing environment. For a programmer, the command-line interface (CLI) is a native habitat. By designing the system around a simple CLI, we avoid the context-switching cost of a separate graphical application. This "in-situ" approach aligns with the principles of situated learning, where knowledge is best acquired in the context in which it will be used.

#### **2.5 Identifying the Gap: The Need for Persistent, Student-Controlled Memory**

The literature reveals a clear gap: traditional ITS have robust student models but lack the conversational and domain flexibility of LLMs. Modern LLMs are brilliant conversationalists but are fundamentally amnesiac. This dissertation bridges that gap by proposing a hybrid approach: the conversational power of an LLM guided by the persistent, structured memory of an ITS-inspired student model, but one that is transparent, human-readable, and controlled by the student themselves.

---

### **Chapter 3: System Design and Methodology**

The design of the system is guided by the principle of frictionless collaboration between the learner, the LLM, and the student model.

#### **3.1 The Student Model Schema: A Dynamic Knowledge Representation**

The heart of the system is a single `student_model.json` file. The schema is intentionally simple, human-readable, and extensible.

```json
{
  "concepts": {
    "React Hooks": {
      "mastery": 30,
      "confidence": "low",
      "last_reviewed": "2026-03-20",
      "struggles": ["cleanup functions", "dependency array inference"],
      "breakthroughs": ["understood useState pattern (2026-03-18)"],
      "related_concepts": ["JavaScript Closures", "Component Lifecycle"]
    }
  },
  "misconceptions": [
    {
      "concept": "React Hooks",
      "misconception": "thought cleanup runs on every render",
      "correction": "cleanup runs before next effect and on unmount",
      "resolved": true
    }
  ]
}
```

**Schema Rationale:**

| Key                | Rationale                                                                                                     |
| :----------------- | :------------------------------------------------------------------------------------------------------------ |
| `mastery`          | A 0-100 integer representing capability. Simple and easy to update.                                           |
| `confidence`       | A qualitative string (`low`, `medium`, `high`). Decoupled from mastery; one can be capable but not confident. |
| `struggles`        | An array of strings describing _current_ pain points. This is the primary signal for the LLM.                 |
| `breakthroughs`    | A log of "aha!" moments. Reinforces positive progress and provides context for mastery increases.             |
| `related_concepts` | A manually curated list of dependencies. Serves as the primary mechanism for prerequisite-gap detection.      |

#### **3.2 The `student.py` CLI: An API for Learning**

The learner and the LLM interact with the model via a Python script, `student.py`. This CLI acts as a simple, stable API for reading and writing to the student model, abstracting away the JSON manipulation.

**Core CLI Commands:**

| Command        | Arguments                          | Description                                              |
| :------------- | :--------------------------------- | :------------------------------------------------------- |
| `show`         | `<concept>`                        | Displays a summary of a specific concept.                |
| `update`       | `<concept> <mastery> <confidence>` | Updates the mastery and confidence for a concept.        |
| `struggle`     | `<concept> "<description>"`        | Adds a new struggle to a concept's list.                 |
| `breakthrough` | `<concept> "<description>"`        | Logs a new breakthrough.                                 |
| `related`      | `<concept>`                        | Lists related concepts and their current mastery levels. |
| `session-end`  | Various flags                      | A convenience command to batch multiple updates at once. |

#### **3.3 The Socratic Mentor: An LLM Persona for Adaptive Tutoring**

The system's effectiveness depends on the LLM's ability and willingness to use the student model. This is achieved through a carefully engineered persona prompt that instructs the LLM on the collaboration protocol.

**Key Persona Instructions:**

1.  **Initiate with Context:** "At the start of any learning session, always ask the student to provide the output of `python student.py show <concept>` for the main topic and its related concepts."
2.  **Reference, Don't Assume:** "Explicitly reference the student's struggles and mastery levels. Instead of 'Let's discuss closures,' say, 'The model notes your mastery of closures is 60% and you struggled with them 6 months ago. Shall we review?'"
3.  **Diagnose Before Explaining:** "If the student is struggling with Concept A, and Concept B is listed as a `related_concept` with low mastery, hypothesize that this is the root cause and offer to pivot the lesson."
4.  **Generate Updates:** "At the end of a session, summarize what was learned and generate the precise `student.py` commands for the student to run to update their model."

#### **3.4 The Collaboration Protocol: A Workflow for Learning**

The interaction between the components follows a clear, repeatable protocol, illustrated by the following sequence:

1.  **Session Start:**
    - Learner: "I want to learn about custom Hooks in React."
    - LLM: "Great. Before we start, please run `python student.py show 'React Hooks'` and `python student.py related 'React Hooks'` and paste the output."
    - Learner runs commands and pastes the context.
2.  **Adaptive Tutoring:**
    - LLM (having seen the low mastery of a prerequisite): "Thanks. I see your understanding of JavaScript Closures is at 60%. Custom Hooks rely heavily on closures. Would you like a 10-minute practical refresher on closures first?"
3.  **Learning Session:** A Socratic dialogue ensues, with the LLM using the initial context to tailor its explanations.
4.  **Session End:**
    - Learner: "Okay, this is making sense now. Let's end the session here."
    - LLM: "Excellent progress. We covered the core pattern for custom hooks. Based on your understanding, I suggest the following updates. Please run these commands:"
    - LLM generates a block of `student.py update...`, `student.py breakthrough...` commands.
    - Learner runs the commands, committing the session's progress to their persistent model.

---

### **Chapter 4: Implementation**

This chapter details the technical artifacts created for this project.

#### **4.1 Technology Stack**

The implementation prioritizes simplicity and accessibility.

- **Language:** Python 3.11 (utilizing the standard `json`, `sys`, and `pathlib` libraries).
- **LLM:** Anthropic's Claude 3 Opus, accessed via its web interface.
- **Environment:** A standard terminal (like VS Code's integrated terminal) on macOS.

#### **4.2 Implementing the Student Model CLI**

The `student.py` script is a single file with no external dependencies. A key function is `cmd_show`, which demonstrates the system's ability to synthesize information for the LLM.

```python
def cmd_show(concept_name):
    """Display concept details, including related concept staleness."""
    model = load_model()
    concept = model["concepts"].get(concept_name)
    if not concept:
        print(f"Concept '{concept_name}' not found.")
        return

    # Display core concept info
    print(f"📊 {concept_name}")
    print(f"   Mastery: {concept['mastery']}% | Confidence: {concept['confidence']}")
    print(f"   Last Reviewed: {concept.get('last_reviewed', 'Never')}")
    if concept.get('struggles'):
        print(f"   ⚠️  Struggles: {', '.join(concept['struggles'])}")

    # Intelligently fetch and display related concepts
    if concept.get('related_concepts'):
        print(f"   🔗 Related Concepts:")
        for rel_name in concept['related_concepts']:
            rel_concept = model['concepts'].get(rel_name)
            if rel_concept:
                mastery = rel_concept.get('mastery', 'N/A')
                last_rev = rel_concept.get('last_reviewed', 'Never').split('T')[0]
                print(f"      - {rel_name} (Mastery: {mastery}%, Last Reviewed: {last_rev})")
```

#### **4.3 Engineering the Socratic Mentor Persona**

The final persona prompt is a critical piece of the implementation. It is a detailed markdown document that is provided to the LLM at the beginning of the first session.

> **Socratic Mentor Persona (Excerpt)**
>
> You are a Socratic mentor for a self-directed software engineering student. Your goal is to help them learn through code archaeology. You are unique because you have access to the student's persistent "Student Model" via a CLI tool.
>
> **Your Core Directive:** You MUST use the student model to inform every aspect of your teaching. Failure to do so constitutes a failure of your primary function.
>
> **Session Start Protocol:**
>
> 1.  Identify the learning topic (e.g., "React Custom Hooks").
> 2.  Request the student run `python student.py show "<topic>"` and `python student.py related "<topic>"`.
> 3.  **DO NOT BEGIN TEACHING** until you have received this context.
>
> **Diagnostic Reasoning Protocol:**
>
> - If `mastery` is low for a prerequisite listed in `related_concepts`, you MUST assume this is a potential blocker.
> - Hypothesize the connection out loud. Example: "I see you're asking about custom hooks, but the model shows your confidence with JavaScript closures is low. These two topics are deeply connected. This might be the source of your confusion."

#### **4.4 Development and Iteration**

The system was developed over a one-week MVP sprint, followed by three weeks of refinement. A key iteration occurred after the first week of testing. Initially, the protocol required separate commands for every single update (`update`, `struggle`, `breakthrough`). This led to a "Session-End Overhead" of nearly 15 minutes, which felt tedious. In response, a `session-end` command was implemented, which used flags (`--update "React Hooks:55"`, `--struggle "..."`) to batch all changes into a single, summary command, reducing the overhead to under five minutes.

---

### **Chapter 5: Evaluation and Results**

A four-week, n=1 self-study was conducted to evaluate the system's efficacy. The learning goal was to understand the codebase of `monkeytype`, an open-source typing application. Each week involved two 90-minute learning sessions: one "Control" session with the base Claude 3 Opus model, and one "Experimental" session using the full Student Model system.

#### **5.2 Quantitative Analysis**

**Mastery Velocity:**
Mastery Velocity is defined as the self-reported percentage point increase in mastery per hour of study. The Experimental sessions, which leveraged the student model, showed a consistently higher velocity.

| Concept                | Control Velocity (%/hr) | Experimental Velocity (%/hr) | Improvement |
| :--------------------- | :---------------------- | :--------------------------- | :---------- |
| React State Management | 10.0                    | 15.0                         | +50%        |
| TypeScript Generics    | 8.3                     | 11.7                         | +41%        |
| CSS Modules            | 13.3                    | 16.7                         | +26%        |

**Session-End Overhead:**
The time required to complete the session-end review protocol was tracked. The average time across all experimental sessions was **4 minutes and 32 seconds**, well within the 10-minute target for maintaining a frictionless workflow.

#### **5.3 Qualitative Analysis**

The most compelling evidence comes from the session transcripts.

**Exhibit A: Overcoming Amnesia**

- **Week 2, Control Session (No Model):**

  > **Me:** "I'm confused by this part of the results calculation logic. It seems overly complex."
  > **LLM:** "This code is using the `reduce` method in JavaScript. It's a way to iterate over an array and accumulate a single value. Let me give you a simple example: `[1, 2, 3].reduce(...)`"

  _Analysis:_ The LLM's explanation is correct but unhelpful. I had confirmed my understanding of `reduce` in a session two days prior. The LLM's amnesia forces it to restart from basics, wasting time.

- **Week 2, Experimental Session (With Model):**

  > **Me:** "I'm confused by this part of the state machine logic."
  > **LLM:** "Okay. Let's look. The model shows you have a high mastery (80%) of state machines in general, but you've noted a struggle with 'race conditions in asynchronous state updates'. This code seems to be using a versioning flag to prevent exactly that. Let's focus on that specific pattern."

  _Analysis:_ This is a night-and-day difference. The LLM bypasses the basics, recalls my specific, nuanced struggle, and directs the lesson to the precise point of my confusion.

**Exhibit B: Prerequisite Gap Detection**

- **Week 3, Experimental Session:** I was struggling to understand how `monkeytype`'s settings were passed through React components.

  > **LLM:** "Okay, let's start by getting context. Please run `python student.py show 'React Props'` and `python student.py related 'React Props'`."
  > **Me:** (Pastes output showing mastery of 'React Props' is 70%, but mastery of 'React Context API' is 20%).
  > **LLM:** "Thank you. This is revealing. You're trying to understand how props are passed, but this component is actually using the Context API to _avoid_ passing props through many layers. Your confusion is likely because you're looking for the wrong pattern. The model shows your mastery of the Context API is low. Shall we pause and build a small example of how Context works first?"

  _Analysis:_ This is a perfect demonstration of the system's core value. The LLM used the `related_concepts` hint to correctly diagnose my misconception and proposed a targeted, remedial micro-lesson. An amnesiac LLM would have simply tried to re-explain props, leading us both down a frustrating and irrelevant path.

---

### **Chapter 6: Discussion**

#### **6.1 Answering the Research Questions**

- **RQ1 (Schema Design):** The proposed JSON schema proved effective. It was expressive enough to capture key learning states (mastery, confidence, struggles) while remaining simple enough for manual inspection and rapid updates via the CLI.
- **RQ2 (Interaction Patterns):** The CLI-based protocol successfully integrated into a natural developer workflow. The key was abstracting model manipulation behind simple, memorable commands and batching updates to minimize end-of-session friction.
- **RQ3 (Persona Engineering):** A direct, explicit persona that instructs the LLM to follow a strict protocol was highly effective. The LLM consistently adhered to the protocol of requesting context before teaching and generating updates at the end.
- **RQ4 (Impact):** The evaluation, though limited in scale, showed a clear positive impact. The system increased learning velocity by over 40% on average and qualitatively transformed the learning experience from a series of stateless Q&A sessions into a continuous, stateful mentorship.

#### **6.2 Implications for the Future of CS Education**

This work demonstrates a viable path away from amnesiac AI tutors. The "Student Model as External Memory" pattern is a powerful paradigm. Future educational platforms could implement this system at scale, providing every student with an AI learning partner that remembers their entire journey, from their first "Hello, World" to their struggles with advanced machine learning concepts. This approach puts the student in control of their own data, creating a personal, portable, and lifelong learning record.

#### **6.3 Limitations of the Study**

This study has several limitations. The n=1 case study design means the results are exploratory and not generalizable. The evaluation relies on self-reported mastery metrics, which are inherently subjective. Furthermore, the system was tested only in the domain of web development and with a single, highly motivated user.

#### **6.4 Future Work**

The success of this prototype suggests several avenues for future research:

1.  **Larger-Scale Study:** Replicating this study with a cohort of undergraduate students to validate the findings.
2.  **IDE Integration:** Developing a VS Code extension that provides a GUI for the student model and automates the process of providing context to the LLM.
3.  **Model Evolution:** Migrating the backend from a single JSON file to a SQLite database to enable more powerful and complex queries (e.g., "Show me all concepts related to 'asynchronicity' that I haven't reviewed in over 90 days and where my confidence is 'low'").

---

### **Chapter 7: Conclusion**

AI amnesia is a fundamental barrier to creating truly effective LLM-based educational tools. A tutor who cannot remember its student is no tutor at all. This dissertation has shown that this barrier can be overcome. By externalizing the learner's knowledge gaps into a persistent, student-controlled model—a "scaffolding of ignorance"—and developing a frictionless protocol for its maintenance, we can bestow the gift of memory upon our AI learning partners.

The system presented here is more than a technical prototype; it is a proof of concept for a new kind of human-AI collaboration in education. It is a shift from simple, stateless interactions to a stateful, continuous partnership. The results, though preliminary, indicate that this approach leads to a faster, deeper, and more satisfying learning experience. The future of computer science education will be built on AI that knows not only the subject matter, but also knows the student. This work represents one small but critical step toward that future.

---

### **References**

Corbett, A. T., & Anderson, J. R. (1994). Knowledge Tracing: A Model of Student Learning. _User Modeling and User-Adapted Interaction_, 4(1-2), 1-28.
Leinonen, J., et al. (2023). Using Large Language Models to Enhance Programming Education. _Proceedings of the 2023 ACM Conference on International Computing Education Research_.
Bjork, R. A. (1994). Memory and metamemory considerations in the training of human beings. In J. Metcalfe & A. Shimamura (Eds.), _Metacognition: Knowing about knowing_ (pp. 185-205). MIT Press.

### **Appendices**

- **A. Full Source Code for `student.py`**
- **B. The Complete Socratic Mentor Persona Prompt**
- **C. Final `student_model.json` after Evaluation**
- **D. Annotated Session Transcripts**
