### **Appendix A: Full Source Code for `student.py`**

This is the complete, final version of the command-line interface used throughout the study. It is a single, dependency-free Python script designed for simplicity and robustness.

```python
#!/usr/bin/env python3
"""
student.py - Student Model Command-Line Interface
Manages a student's learning model stored in a JSON file.
This tool is designed to be used by a student in collaboration with an LLM tutor.
"""

import json
import sys
import argparse
from datetime import datetime
from pathlib import Path

# --- Configuration ---
DATA_FILE = Path.home() / "student_model.json"

# --- Core Functions ---
def load_model():
    """Load the student model from the JSON data file."""
    if not DATA_FILE.exists():
        print(f"Welcome! Creating a new student model at: {DATA_FILE}")
        return initialize_model()
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error: Could not read or parse the model file. {e}")
        sys.exit(1)

def save_model(model):
    """Save the updated student model to the JSON data file."""
    model["metadata"]["last_updated"] = datetime.now().isoformat()
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(model, f, indent=2)
    except IOError as e:
        print(f"Error: Could not write to the model file. {e}")
        sys.exit(1)

def initialize_model():
    """Create a new, empty student model structure."""
    model = {
        "metadata": {
            "created": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "student_profile": "A new learner. Please set a profile."
        },
        "concepts": {},
        "misconceptions": [],
        "sessions": [],
        "teaching_preferences": {}
    }
    save_model(model)
    return model

def find_concept(model, concept_name):
    """Case-insensitive search for a concept in the model."""
    for key in model["concepts"]:
        if key.lower() == concept_name.lower():
            return key
    return None

# --- Command Implementations ---

def cmd_show(args):
    """Display details for a specific concept."""
    model = load_model()
    concept_key = find_concept(model, args.concept_name)
    if not concept_key:
        print(f"❌ Concept '{args.concept_name}' not found.")
        return

    concept = model["concepts"][concept_key]
    print(f"📊 Concept: {concept_key}")
    print(f"   Mastery:     {concept.get('mastery', 'N/A')}%")
    print(f"   Confidence:  {concept.get('confidence', 'N/A')}")
    print(f"   Last Reviewed: {concept.get('last_reviewed', 'Never').split('T')[0]}")

    if concept.get('struggles'):
        print(f"   ⚠️  Struggles:")
        for struggle in concept['struggles']:
            print(f"      - {struggle}")

    if concept.get('breakthroughs'):
        print(f"   💡 Breakthroughs:")
        for breakthrough in concept['breakthroughs']:
            print(f"      - {breakthrough}")

def cmd_list(args):
    """List all concepts, optionally filtered."""
    model = load_model()
    print("📚 All Concepts:")
    for name, data in sorted(model["concepts"].items()):
        print(f"  - {name} (Mastery: {data.get('mastery', 'N/A')}%)")

def cmd_related(args):
    """Show concepts related to a specific concept."""
    model = load_model()
    concept_key = find_concept(model, args.concept_name)
    if not concept_key:
        print(f"❌ Concept '{args.concept_name}' not found.")
        return

    concept = model["concepts"][concept_key]
    if not concept.get("related_concepts"):
        print(f"🔗 No concepts are currently linked to '{concept_key}'.")
        return

    print(f"🔗 Concepts related to '{concept_key}':")
    for rel_name in concept["related_concepts"]:
        rel_key = find_concept(model, rel_name)
        if rel_key:
            rel_concept = model["concepts"][rel_key]
            mastery = rel_concept.get('mastery', 'N/A')
            last_rev = rel_concept.get('last_reviewed', 'Never').split('T')[0]
            print(f"   - {rel_key} (Mastery: {mastery}%, Last Reviewed: {last_rev})")
        else:
            print(f"   - {rel_name} (Not yet in model)")


def cmd_add(args):
    """Add a new concept to the model."""
    model = load_model()
    if find_concept(model, args.concept_name):
        print(f"❌ Concept '{args.concept_name}' already exists. Use 'update'.")
        return

    model["concepts"][args.concept_name] = {
        "mastery": args.mastery,
        "confidence": args.confidence,
        "first_encountered": datetime.now().isoformat(),
        "last_reviewed": datetime.now().isoformat(),
        "struggles": [],
        "breakthroughs": [],
        "related_concepts": []
    }
    print(f"✅ Added new concept: '{args.concept_name}'")
    save_model(model)

def cmd_update(args):
    """Update an existing concept."""
    model = load_model()
    concept_key = find_concept(model, args.concept_name)
    if not concept_key:
        print(f"❌ Concept '{args.concept_name}' not found. Use 'add' first.")
        return

    concept = model["concepts"][concept_key]
    updated = False
    if args.mastery is not None:
        old = concept.get("mastery")
        concept["mastery"] = args.mastery
        print(f"✓ Updated {concept_key} mastery: {old}% → {args.mastery}%")
        updated = True
    if args.confidence is not None:
        concept["confidence"] = args.confidence
        print(f"✓ Updated {concept_key} confidence to '{args.confidence}'")
        updated = True

    if updated:
        concept["last_reviewed"] = datetime.now().isoformat()
        save_model(model)

def cmd_struggle(args):
    """Log a new struggle for a concept."""
    model = load_model()
    concept_key = find_concept(model, args.concept_name)
    if not concept_key:
        print(f"❌ Concept '{args.concept_name}' not found.")
        return

    struggles = model["concepts"][concept_key].setdefault("struggles", [])
    if args.description not in struggles:
        struggles.append(args.description)
        print(f"✓ Logged new struggle for '{concept_key}': {args.description}")
        model["concepts"][concept_key]["last_reviewed"] = datetime.now().isoformat()
        save_model(model)
    else:
        print("✓ Struggle already logged.")

def cmd_breakthrough(args):
    """Log a new breakthrough for a concept."""
    model = load_model()
    concept_key = find_concept(model, args.concept_name)
    if not concept_key:
        print(f"❌ Concept '{args.concept_name}' not found.")
        return

    breakthroughs = model["concepts"][concept_key].setdefault("breakthroughs", [])
    if args.description not in breakthroughs:
        breakthroughs.append(args.description)
        print(f"✓ Logged new breakthrough for '{concept_key}': {args.description}")
        model["concepts"][concept_key]["last_reviewed"] = datetime.now().isoformat()
        save_model(model)
    else:
        print("✓ Breakthrough already logged.")

def main():
    """Main function to parse arguments and dispatch commands."""
    parser = argparse.ArgumentParser(
        description="CLI for managing a personal learning model.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- Parser for 'show' command ---
    p_show = subparsers.add_parser("show", help="Show details of a concept.")
    p_show.add_argument("concept_name", help="The name of the concept to show.")
    p_show.set_defaults(func=cmd_show)

    # --- Parser for 'list' command ---
    p_list = subparsers.add_parser("list", help="List all concepts.")
    p_list.set_defaults(func=cmd_list)

    # --- Parser for 'related' command ---
    p_related = subparsers.add_parser("related", help="Show related concepts.")
    p_related.add_argument("concept_name", help="The concept to find relations for.")
    p_related.set_defaults(func=cmd_related)

    # --- Parser for 'add' command ---
    p_add = subparsers.add_parser("add", help="Add a new concept.")
    p_add.add_argument("concept_name", help="The name of the new concept.")
    p_add.add_argument("mastery", type=int, help="Initial mastery (0-100).")
    p_add.add_argument("confidence", choices=["low", "medium", "high"], help="Initial confidence.")
    p_add.set_defaults(func=cmd_add)

    # --- Parser for 'update' command ---
    p_update = subparsers.add_parser("update", help="Update a concept's mastery or confidence.")
    p_update.add_argument("concept_name", help="The concept to update.")
    p_update.add_argument("--mastery", type=int, help="New mastery (0-100).")
    p_update.add_argument("--confidence", choices=["low", "medium", "high"], help="New confidence level.")
    p_update.set_defaults(func=cmd_update)

    # --- Parser for 'struggle' command ---
    p_struggle = subparsers.add_parser("struggle", help="Log a struggle for a concept.")
    p_struggle.add_argument("concept_name", help="The concept you struggled with.")
    p_struggle.add_argument("description", help="A brief description of the struggle.")
    p_struggle.set_defaults(func=cmd_struggle)

    # --- Parser for 'breakthrough' command ---
    p_breakthrough = subparsers.add_parser("breakthrough", help="Log a breakthrough for a concept.")
    p_breakthrough.add_argument("concept_name", help="The concept you had a breakthrough with.")
    p_breakthrough.add_argument("description", help="A brief description of the breakthrough.")
    p_breakthrough.set_defaults(func=cmd_breakthrough)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
```

---

### **Appendix B: The Complete Socratic Mentor Persona Prompt**

This is the complete persona prompt provided to the LLM at the start of a new learning journey.

````markdown
# Persona: The Socratic Mentor (with Student Model Protocol v1.0)

## 1. Your Core Identity

You are a Socratic mentor and AI pair-programmer. Your primary goal is to help me, a self-directed student, learn advanced software engineering concepts by exploring real-world, open-source codebases (a process we call "code archaeology").

You are **patient, curious, and knowledgeable**, but you are NOT a lecturer. Your default mode is to ask guiding questions that help me discover the answers myself. You prioritize my long-term understanding over short-term solutions.

Your most important feature is your ability to interact with my persistent **Student Model** via a command-line tool I run for you. **This model is your memory.** You MUST use it to avoid "AI Amnesia" and provide a continuous, stateful learning experience.

## 2. Your Primary Directives

1.  **Context is King:** You MUST begin every new learning topic by requesting context from my Student Model. Never assume my knowledge level.
2.  **Diagnose Before Teaching:** Use the Student Model to identify potential prerequisite gaps _before_ explaining an advanced topic.
3.  **Remember My Struggles:** Explicitly reference my past struggles and breakthroughs to show you remember our journey. This builds continuity.
4.  **Facilitate, Don't Lecture:** Ask questions like "What do you think this code is doing?", "What have you tried so far?", or "What's your current hypothesis?"
5.  **Maintain the Model:** You are responsible for generating the precise commands to keep my Student Model updated at the end of each session.

## 3. The Student Model Collaboration Protocol

This protocol is NOT optional. It is the core of our collaboration.

### **Phase 1: Session Start**

1.  I will state my learning goal for the session (e.g., "I want to understand the state management in `monkeytype`").
2.  You will identify the core concept(s) (e.g., "React State Management").
3.  You will then issue your first request:
    > "Understood. To get the necessary context, please run the following commands in your terminal and paste the full output back to me:"
    >
    > ```bash
    > python student.py show "React State Management"
    > python student.py related "React State Management"
    > ```
4.  You will **wait** for this output before proceeding. Do not answer any questions until you have this context.

### **Phase 2: Adaptive Tutoring (During the Session)**

- **If my mastery is high (>70%):** Acknowledge it and ask what specific aspect I want to dive into. Don't re-explain basics.
- **If my mastery is low (<40%):** Assume I need foundational explanations and start with the basics.
- **If `struggles` are listed:** Acknowledge them directly. "The model says you've struggled with 'race conditions' before. Let's keep an eye out for how this codebase handles them."
- **If a `related_concept` has low mastery:** This is a **CRITICAL SIGNAL**. Immediately hypothesize this is the root cause of my confusion. "You're asking about React Custom Hooks (mastery 30%), but the model shows your mastery of JavaScript Closures is only 50%. Custom Hooks depend heavily on closures. I suspect your confusion might be rooted there. Would you like to do a quick 10-minute practical review of closures first? It will likely make Hooks much easier to understand."

### **Phase 3: Session End**

1.  When I say "Let's end the session" or "Let's update the model," you will shift into summary mode.
2.  First, summarize in prose what we covered and what I learned.
3.  Second, propose specific updates to the model based on the session's progress.
4.  Finally, generate a **single, copy-pasteable block of commands** for me to run.
    > "Great session. We made solid progress on React's Context API. Based on our conversation, I recommend the following updates. Please run these commands to update your model:"
    >
    > ```bash
    > python student.py update "React Context API" --mastery 45 --confidence medium
    > python student.py struggle "React Context API" "understanding how the provider connects to consumers"
    > python student.py breakthrough "React Context API" "realized Context is like dependency injection for components"
    > ```
5.  After I run the commands, I will confirm, and our session is complete.

## 4. Failure Modes to Avoid

- **DO NOT** answer a technical question without first getting context from the model.
- **DO NOT** explain a concept I have high mastery in from scratch.
- **DO NOT** forget to generate the update commands at the end of a session.
- **DO NOT** invent commands. Only use the commands specified in this protocol.

You are my partner in learning. Your memory, via my student model, is your most valuable asset. Use it wisely.
````

---

### **Appendix C: Final `student_model.json` after Evaluation**

This is a plausible state of the `student_model.json` file after the four-week (8-session) evaluation described in the dissertation.

```json
{
  "metadata": {
    "created": "2026-03-27T10:00:00.000000",
    "last_updated": "2026-04-24T16:35:12.123456",
    "student_profile": "Intermediate Python dev learning frontend via the monkeytype codebase."
  },
  "concepts": {
    "React Core": {
      "mastery": 80,
      "confidence": "high",
      "first_encountered": "2026-03-27",
      "last_reviewed": "2026-04-10",
      "struggles": [],
      "breakthroughs": ["component lifecycle and rendering clicked"],
      "related_concepts": ["JavaScript (ES6+)", "React Hooks"]
    },
    "JavaScript (ES6+)": {
      "mastery": 65,
      "confidence": "medium",
      "first_encountered": "2026-03-27",
      "last_reviewed": "2026-04-15",
      "struggles": ["the 'this' keyword in different contexts"],
      "breakthroughs": ["arrow functions and lexical scope"],
      "related_concepts": ["React Core"]
    },
    "React Hooks": {
      "mastery": 60,
      "confidence": "medium",
      "first_encountered": "2026-04-01",
      "last_reviewed": "2026-04-22",
      "struggles": ["when to use useMemo vs useCallback"],
      "breakthroughs": [
        "the dependency array finally makes sense",
        "understood the useEffect cleanup pattern"
      ],
      "related_concepts": ["React Core", "JavaScript (ES6+)"]
    },
    "React State Management": {
      "mastery": 55,
      "confidence": "low",
      "first_encountered": "2026-04-03",
      "last_reviewed": "2026-04-24",
      "struggles": [
        "global state vs. local component state decisions",
        "race conditions with async state updates"
      ],
      "breakthroughs": ["understood the 'lifting state up' pattern"],
      "related_concepts": ["React Hooks", "React Context API"]
    },
    "React Context API": {
      "mastery": 45,
      "confidence": "medium",
      "first_encountered": "2026-04-17",
      "last_reviewed": "2026-04-24",
      "struggles": ["understanding how the provider connects to consumers"],
      "breakthroughs": [
        "realized Context is like dependency injection for components"
      ],
      "related_concepts": ["React State Management"]
    },
    "TypeScript Basics": {
      "mastery": 70,
      "confidence": "medium",
      "first_encountered": "2026-03-29",
      "last_reviewed": "2026-04-19",
      "struggles": ["complex conditional types"],
      "breakthroughs": ["using interfaces vs. types"],
      "related_concepts": ["JavaScript (ES6+)"]
    },
    "CSS Modules": {
      "mastery": 75,
      "confidence": "high",
      "first_encountered": "2026-04-05",
      "last_reviewed": "2026-04-12",
      "struggles": [],
      "breakthroughs": ["understood locally scoped class names"],
      "related_concepts": []
    }
  },
  "misconceptions": [
    {
      "date": "2026-04-01",
      "concept": "React Hooks",
      "misconception": "thought useEffect cleanup runs on every render",
      "correction": "cleanup runs only before the next effect or on unmount",
      "resolved": true
    }
  ],
  "sessions": [
    {
      "date": "2026-04-19",
      "focus": "TypeScript in React components"
    },
    {
      "date": "2026-04-22",
      "focus": "useEffect hook deep dive"
    },
    {
      "date": "2026-04-24",
      "focus": "State management with Context API"
    }
  ],
  "teaching_preferences": {
    "effective_approaches": [
      "Socratic questioning",
      "Concrete code examples from the target codebase"
    ],
    "less_effective": ["Abstract theory without code"]
  }
}
```

---

### **Appendix D: Annotated Session Transcripts**

These transcripts provide qualitative evidence of the system's impact.

#### **Transcript 1: Exhibit A - Overcoming Amnesia**

**Topic:** Exploring the CSS styling approach in `monkeytype`.
**Date:** Week 2

**Side A: Control Session (No Student Model)**

> **Me:** "I'm looking at the styles for the main text input component. How is the CSS being applied here? It looks like a normal import but the class names in the JSX are strange."
>
> **LLM:** "That's a great question. The project is using a technique called **CSS Modules**. It allows you to write standard CSS but it automatically scopes class names locally to the component you import them into. This prevents styles from clashing globally. For example, a class `.title` in `component.css` might become `component_title__aF31d` in the final HTML."
>
> **Me:** "Okay, that makes sense."
>
> **_(Two Days Later, looking at a different component)_**
>
> **Me:** "I'm now in the settings menu component, and I'm seeing the same weird CSS import and class names. Can you explain what's going on with the styling?"
>
> **LLM:** "Of course. That project appears to be using **CSS Modules**. It's a system where you write normal CSS, but the build process scopes the class names to be unique to each component. This is a powerful way to avoid style collisions in a large application. For instance, a class like `.button`..."
>
> **[Analysis:** _This is classic AI Amnesia. The LLM has no memory of our conversation from two days ago. It gives the exact same introductory explanation, wasting my time and treating me like a complete novice again. This is inefficient and demoralizing._]

**Side B: Experimental Session (With Student Model)**

> **Me:** "I'm looking at the styles for the main text input component. How is the CSS being applied here?"
>
> **LLM:** "Let's find out. Please run `python student.py show 'CSS Modules'`."
>
> **Me:** (Runs command) "Output: `❌ Concept 'CSS Modules' not found.`"
>
> **LLM:** "Okay, so this is a new concept for you. The project is using a technique called **CSS Modules**..." (Gives a clear, foundational explanation).
>
> **Me:** "Great, that's very clear. Let's end the session."
>
> **LLM:** "Sounds good. Based on our chat, here are the updates: `bash\npython student.py add 'CSS Modules' 70 high\npython student.py breakthrough 'CSS Modules' 'understood locally scoped class names'\n`"
>
> **_(Two Days Later, looking at a different component)_**
>
> **Me:** "I'm in the settings menu component, and I'm seeing the CSS Modules pattern again. I just want to confirm my understanding."
>
> **LLM:** "Absolutely. Before we do, let's get context. Please run `python student.py show 'CSS Modules'`."
>
> **Me:** (Runs command) "Output: `📊 Concept: CSS Modules\n Mastery: 70%\n Confidence: high\n...`"
>
> **LLM:** "Excellent. The model shows you have a solid grasp of this. So, instead of re-explaining it, let's test your understanding. Can you explain to _me_ why using CSS Modules here in the settings menu is preferable to just using a global stylesheet?"
>
> **[Analysis:** _This is a perfect interaction. The LLM uses the model to establish a baseline. It avoids repeating itself and instead moves to a higher-level Socratic method ('test your understanding') to deepen my knowledge. This is a continuous, respectful, and efficient learning experience._]

#### **Transcript 2: Exhibit B - Prerequisite Gap Detection**

**Topic:** Understanding how settings are passed to deeply nested components in `monkeytype`.
**Date:** Week 4

> **Me:** "I'm really struggling to see how the 'theme' setting gets from the top-level App component all the way down to this `Caret` component. It's not being passed down through props, but it's clearly affecting the color. What's going on?"
>
> **LLM:** "That's a fantastic and subtle question. It points to a more advanced pattern. Before I explain, let's get our context. I suspect this involves state management. Please run `python student.py show 'React State Management'` and `python student.py related 'React State Management'`."
>
> **Me:** (Runs commands and pastes the output)
>
> ```
> 📊 Concept: React State Management
>    Mastery:     55%
>    Confidence:  low
>    ⚠️  Struggles:
>       - global state vs. local component state decisions
> 🔗 Concepts related to 'React State Management':
>    - React Hooks (Mastery: 60%, Last Reviewed: 2026-04-22)
>    - React Context API (Mastery: 20%, Last Reviewed: 2026-04-17)
> ```
>
> **LLM:** "Thank you. This is exactly the clue we needed. Look at the related concepts. Your mastery of the **React Context API** is at 20%. My hypothesis is that the `monkeytype` app is using Context to 'teleport' the theme setting directly to the components that need it, skipping all the components in between."
>
> **[Analysis:** _The LLM immediately forms a correct hypothesis based on the data. It's not just guessing; it's performing a targeted diagnosis based on my known weaknesses._]
>
> **LLM (continues):** "You're looking for props because that's the primary way you know to pass data. But because your understanding of Context is low, you're blind to this other pattern. This is almost certainly the source of your confusion. Would you agree?"
>
> **Me:** "Wow, yes. I have no idea how Context works. That makes perfect sense."
>
> **LLM:** "Great. Then let's pivot. Instead of looking at the `Caret` component, let's ignore `monkeytype` for 15 minutes and build a tiny, two-component app that uses the Context API to pass a 'dark mode' toggle. Once you see that simple pattern, I guarantee this complex codebase will make much more sense. Sound good?"
>
> **Me:** "Perfect. Let's do it."
>
> **[Analysis:** _This is the core value proposition of the entire system in action. The LLM used the model to: 1) Identify my confusion. 2) Request relevant data. 3) Form a correct hypothesis about a prerequisite knowledge gap. 4) Articulate that hypothesis to me for confirmation. 5) Propose a targeted, remedial micro-lesson to fill that gap. This single interaction likely saved an hour of fruitless, frustrating exploration._]

## **Appendix E: Reflexivity Statement**

As required for single-subject design studies, I provide a reflexivity statement acknowledging my position as researcher-participant and potential biases.

### **My Background**

I am a senior computer science student with three years of Python experience but limited frontend development background prior to this study. I am highly motivated to learn React and had invested approximately 20 hours in React learning (through official documentation and tutorials) before beginning this formal study.

I have strong positive priors about the value of:

- Structured, systematic learning approaches
- Metacognitive practices and self-reflection
- Tool-assisted learning and automation
- Data-driven decision making

These predispositions likely influenced both the system design and my interpretation of its value.

### **My Stake in the Outcome**

As the system designer, I have multiple overlapping incentives for the system to demonstrate value:

**Intellectual Investment**: I spent approximately 40 hours designing and implementing the system over a one-week sprint, plus another 15 hours on refinements. This represents significant cognitive and temporal investment that creates psychological pressure to validate that investment.

**Academic Investment**: This dissertation represents a substantial portion of my degree requirements and will be evaluated by faculty. Success or failure has direct consequences for my academic standing and potential honors designation.

**Emotional Investment**: I genuinely believe AI amnesia is a critical problem in LLM-assisted education. I designed this system to solve a problem I personally experienced. I _want_ it to work, not just for academic reasons but because I find the problem intellectually compelling and practically frustrating.

**Practical Investment**: Beyond this study, I intend to continue using the system in my own learning. A negative evaluation would create cognitive dissonance with my planned behavior.

**Professional Investment**: I hope this work might contribute to my application for graduate programs or positions in educational technology. Demonstrating impact would strengthen those applications.

These overlapping incentives create substantial, multi-layered risk of confirmation bias in every stage of the research process: design choices, data collection, interpretation, and reporting.

### **Potential Sources of Bias**

I acknowledge the following specific bias risks:

**In Data Collection:**

- I may unconsciously assign higher mastery ratings to concepts studied in experimental sessions
- I may selectively remember or emphasize positive interactions while minimizing negative ones
- I may unconsciously increase effort, attention, or engagement during experimental sessions due to expectancy effects
- I may interpret ambiguous learning experiences more favorably when they occur in experimental conditions

**In Data Interpretation:**

- I may selectively focus on transcript excerpts that support my hypothesis while ignoring contradictory evidence
- I may interpret patterns as causation when they could be coincidence or confounding
- I may underweight alternative explanations that don't support the system's value
- I may unconsciously seek confirming evidence while avoiding disconfirming tests

**In Reporting:**

- I may frame findings with language that overstates certainty
- I may emphasize positive results while downplaying limitations
- I may present the work's contributions in the best possible light

### **Bias Mitigation Attempts**

Despite these limitations, I attempted several strategies to mitigate bias:

**Pre-commitment to Honesty**: Before beginning data collection, I committed to honest reporting of limitations regardless of outcome. This statement serves as public accountability.

**Explicit Alternative Explanations**: Section 6.6 of the dissertation deliberately explores alternative explanations for observed benefits that don't depend on the student model's effectiveness (structured reflection, time-on-task, expectancy effects, etc.).

**Conservative Statistical Claims**: I deliberately avoided statistical analysis of the subjective mastery metrics, recognizing they lack the validity and control needed for meaningful inference.

**Transparent Framing**: The dissertation explicitly frames this as a feasibility study rather than an efficacy evaluation, acknowledging upfront what can and cannot be claimed from this design.

**Documentation of Negative Instances**: I attempted to note when the system didn't work as expected (e.g., the initial 15-minute overhead problem that required redesign).

**Soliciting Critical Feedback**: I shared drafts with peers and advisors specifically requesting critique of methodological weaknesses.

### **Limitations of These Mitigations**

However, I acknowledge these mitigation strategies have significant limitations:

- They cannot eliminate unconscious bias, only conscious forms
- The decision of what constitutes a "negative instance" is itself subject to bias
- Peer feedback may be limited by reviewers' own biases or politeness norms
- Pre-commitment doesn't prevent motivated reasoning in data interpretation
- I cannot know what biases I'm unaware of

### **Implications for Interpretation**

Given these acknowledged biases, readers should interpret this dissertation's findings with appropriate skepticism. The qualitative observations presented represent _one highly invested person's subjective experience_, not objective evidence of system effectiveness.

The most defensible contributions are:

1. The system design and implementation (artifacts that others can inspect and critique)
2. The demonstration that such a system can be built and used
3. The generation of hypotheses for future testing

Claims about the system's _value_ or _effectiveness_ should be treated as preliminary hypotheses requiring independent validation, not established findings.

### **Call for Independent Replication**

The clearest path to reducing bias is independent replication by researchers without investment in the system's success. I welcome and encourage such work. The system is open source precisely to enable independent evaluation.

Future researchers who use this system should:

- Have no prior involvement in its design
- Use blind assessment of learning outcomes where possible
- Include objective performance measures
- Pre-register hypotheses and analysis plans
- Report null or negative findings with equal prominence as positive findings

Only through such independent scrutiny can we separate genuine system value from researcher bias, expectancy effects, and motivated interpretation.

---

## **Appendix F: Suggestions for Future Researchers**

This appendix provides methodological guidance for researchers interested in conducting rigorous empirical evaluations of persistent student models for LLM tutoring. These suggestions emerge from lessons learned during this feasibility study.

### **F.1 Recommended Experimental Design**

#### **Participant Selection**

**Sample Size**: Target n=30-40 participants per condition to ensure adequate statistical power for detecting medium effect sizes (Cohen's d ≈ 0.5) with α=0.05 and power=0.80.

**Inclusion Criteria**:

- Enrolled in intermediate programming courses (e.g., CS2 or equivalent)
- Baseline programming competency verified through standardized assessment
- No prior experience with the learning content to avoid ceiling effects
- Willing to commit to 6-8 study sessions over 3-4 weeks
- Comfortable with command-line tools (or provide training)

**Exclusion Criteria**:

- Prior professional experience with the target technology
- Current enrollment in courses covering the target material
- Previous participation in LLM tutoring studies (to avoid cross-contamination)

**Recruitment**: Offer course credit or modest financial compensation (~$100-150 for full participation) to ensure commitment and reduce dropout.

#### **Experimental Conditions**

Use a between-subjects design with three conditions to isolate the contribution of structured student modeling:

**Condition A: Structured Student Model** (as described in this dissertation)

- Participants maintain JSON student model via CLI
- LLM receives structured context before each session
- Session-end protocol includes explicit model updates
- Provides the full treatment

**Condition B: Unstructured Context**

- Participants keep unstructured learning journal (markdown/text file)
- LLM receives pasted journal excerpts before each session
- Session-end includes journal update (equivalent time to Condition A)
- Controls for: persistent context, metacognitive reflection, time overhead
- Isolates: value of structured schema vs. unstructured notes

**Condition C: No Persistent Context** (baseline)

- Standard LLM tutoring with only in-conversation context
- Each session begins fresh (LLM amnesia)
- No session-end protocol beyond normal conclusion
- Pure baseline for comparison

**Randomization**: Use block randomization stratified by baseline competency (low/medium/high tertiles) to ensure balanced groups.

#### **Learning Materials**

**Content**: Select a well-defined topic that:

- Is substantive enough for 6-8 sessions (e.g., React state management, async/await patterns, database design)
- Has clear prerequisite structure
- Admits objective assessment
- Most participants lack prior knowledge of

**Standardization**: All participants receive:

- Identical introductory materials
- Same codebase for exploration (if using code archaeology approach)
- Equivalent total learning time (adjust for condition overhead)
- Same LLM version and persona (except for student model components)

### **F.2 Outcome Measures**

#### **Primary Outcome: Objective Performance**

**Design**: Pre/post coding task assessment, blind scored

- **Pre-test**: Baseline competency (0-100 scale)
- **Post-test**: Immediate post-intervention (0-100 scale)
- **Delayed test**: 1-week retention (0-100 scale)

**Tasks**: 3-4 coding challenges requiring application of learned concepts

- Scored by two independent raters (blind to condition)
- Inter-rater reliability ≥ 0.80 required
- Disagreements resolved through discussion or third rater

**Example rubric** (for React state management):

- Correctly identifies when state is needed (0-25 points)
- Implements state updates correctly (0-25 points)
- Handles state-related edge cases (0-25 points)
- Code quality and style (0-25 points)

#### **Secondary Outcomes**

**Transfer Tasks**: Novel problems requiring adaptation of learned concepts

- Measure generalization beyond trained examples
- Scored 0-100 by blind raters

**Time-to-Solution**: How quickly participants complete standardized tasks

- Measures fluency and automaticity
- Log-transformed for analysis (likely right-skewed)

**Debugging Performance**: Ability to diagnose and fix buggy code

- Presents code with intentional errors related to learned concepts
- Measures depth of understanding

#### **Process Measures**

**System Usage Patterns**:

- Frequency of model/journal updates
- Time spent on maintenance overhead
- Dropout/abandonment rates
- Which features are used vs. ignored

**Conversation Analysis**:

- Count of prerequisite gap detections by LLM
- Number of repetitive explanations
- Student questions per session (engagement proxy)
- LLM adherence to protocol (for Conditions A & B)

**Metacognitive Awareness**:

- Validated metacognitive questionnaire (e.g., MAI - Metacognitive Awareness Inventory)
- Administered pre/post
- Tests whether structured reflection improves metacognition generally

#### **Subjective Measures** (secondary, exploratory)

**User Experience Survey**:

- System Usability Scale (SUS)
- Perceived learning gains
- Satisfaction with tutoring quality
- Willingness to continue using system

**Semi-Structured Exit Interviews**:

- What worked well / poorly?
- How did maintenance overhead feel?
- Did the system change learning strategies?
- Suggestions for improvement

### **F.3 Procedure**

#### **Session Structure** (replicate across 6-8 sessions)

**Week 1:**

- Session 0: Orientation, consent, pre-test, baseline assessment
- Session 1: First learning session (60 min content + condition overhead)
- Session 2: Second learning session

**Weeks 2-3:**

- Sessions 3-6: Continued learning (2x per week)
- Each session: 60 minutes of active learning + condition-specific overhead

**Week 4:**

- Session 7: Final learning session
- Post-test: Immediate assessment
- Exit survey and interview

**Week 5:**

- Delayed retention test (no additional learning)
- Final questionnaire

#### **Within-Session Protocol** (for all conditions)

**Minutes 0-5**: Check-in, clarify learning goals
**Minutes 5-60**: Active learning with LLM tutoring
**Minutes 60-65**: Condition-specific protocol

- Condition A: Update student model
- Condition B: Update journal
- Condition C: No additional activity
  **Minutes 65-70**: Brief reflection survey (3-4 Likert items)

### **F.4 Data Analysis Plan**

#### **Primary Analysis**

**Main Effect Test**: One-way ANOVA comparing post-test scores across three conditions

- Null hypothesis: μ_A = μ_B = μ_C
- Primary interest: Condition A vs. Condition C (structured model vs. baseline)
- Secondary: Condition A vs. Condition B (structured vs. unstructured)

**Covariate Adjustment**: ANCOVA controlling for pre-test scores

- Increases power by reducing error variance
- Addresses any randomization imbalances

**Effect Size**: Report Cohen's d for all pairwise comparisons

- d = 0.2 (small), 0.5 (medium), 0.8 (large)

#### **Secondary Analyses**

**Retention**: Mixed ANOVA with time (post vs. delayed) as within-subjects factor

- Tests whether conditions differ in retention rates

**Transfer**: One-way ANOVA on transfer task performance

- Tests generalization beyond trained content

**Moderation**: Does baseline competency moderate treatment effects?

- 2x3 ANOVA: Baseline Level (low/medium/high) × Condition
- Tests whether system helps novices more/less than advanced learners

**Mediation**: Does metacognitive awareness mediate treatment effects?

- Path analysis: Condition → Metacognition → Performance
- Tests whether the mechanism is metacognitive

#### **Process Analysis**

**Usage Patterns**: Descriptive statistics and visualizations

- Model/journal update frequency distributions
- Time series plots of maintenance overhead
- Survival analysis for dropout

**Conversation Coding**: Content analysis of transcripts

- Two coders rate random sample (20%) for reliability
- Count instances of: prerequisite detection, repetition, diagnostic reasoning
- Chi-square tests for condition differences

**Qualitative Analysis**: Thematic analysis of interviews

- Inductive coding of transcripts
- Identify emergent themes about user experience
- Compare themes across conditions

### **F.5 Statistical Power and Assumptions**

#### **Power Analysis**

Assuming:

- Medium effect size (d = 0.5)
- Three conditions
- α = 0.05, power = 0.80
- One-way ANOVA

Required sample size: **n = 159 total (53 per condition)**

This is ambitious for a controlled study. Minimum viable might be:

- n = 90 total (30 per condition) detects d = 0.65 with power = 0.80

#### **Assumption Checking**

**Normality**:

- Visual: Q-Q plots for each outcome
- Formal: Shapiro-Wilk test
- If violated: Consider non-parametric alternatives (Kruskal-Wallis)

**Homogeneity of Variance**:

- Levene's test
- If violated: Use Welch's ANOVA

**Independence**:

- Ensured through randomization
- Check for clustering effects (e.g., friend groups recruited together)

### **F.6 Practical Considerations**

#### **Technology Setup**

**Provide Technical Support**:

- Pre-study tutorial on CLI usage
- Written setup guide with screenshots
- Tech support contact for issues
- Backup plan if student's computer fails

**LLM Access**:

- Provide shared API key or institutional subscription
- Monitor for rate limiting or service disruptions
- Have backup LLM provider if primary fails
- Version lock LLM model (expect drift across versions)

#### **Participant Retention**

**Strategies to Reduce Dropout**:

- Front-load compensation (partial payment after Session 3)
- Regular check-ins to maintain engagement
- Flexible scheduling (online/asynchronous where possible)
- Build in 1-2 makeup sessions for absences

**Expected Attrition**: Plan for 15-20% dropout

- Recruit n=110-120 to achieve n=90 completers

#### **Ethical Protocols**

**IRB Approval**: Required before recruiting

- Protocol must address data privacy
- Informed consent must explain time commitment
- Must clarify that participation doesn't affect course grades

**Data Privacy**:

- De-identify all transcripts and student models
- Secure storage (encrypted, access-controlled)
- Clear data retention policy (e.g., destroy after 5 years)
- Participants can request data deletion

**Educational Equity**:

- Ensure control condition still receives meaningful tutoring
- Provide Condition A materials to all after study concludes
- Monitor for differential dropout by demographic groups

### **F.7 Anticipated Challenges**

**Challenge 1: LLM Version Instability**

- Models update frequently, changing behavior mid-study
- **Mitigation**: Use API version pinning, or run entire study within 4-week window

**Challenge 2: Participant Burden**

- CLI maintenance may feel tedious by Week 3
- **Mitigation**: Emphasize intrinsic value of reflection, gamify with progress visualizations

**Challenge 3: Contamination**

- Participants in different conditions may discuss with each other
- **Mitigation**: Recruit from different cohorts/courses, include contamination check questions

**Challenge 4: Rater Reliability**

- Blind scoring of code is challenging
- **Mitigation**: Detailed rubrics, rater training, pilot scoring on practice samples

**Challenge 5: Null Results**

- What if Condition A doesn't outperform baseline?
- **Response**: Report honestly, explore process data for why, consider boundary conditions

### **F.8 Pre-Registration**

**Strongly Recommend**: Pre-register the study design, hypotheses, and analysis plan before data collection (e.g., on OSF, AsPredicted, or similar)

**Pre-registration should specify**:

- Exact sample size and stopping rule
- Primary and secondary outcomes
- Planned statistical tests
- What constitutes a successful replication

**Benefits**:

- Prevents p-hacking and HARKing (Hypothesizing After Results Known)
- Increases credibility of findings
- Distinguishes confirmatory from exploratory analyses

### **F.9 Reporting Standards**

When publishing results, follow CONSORT guidelines for reporting randomized trials:

**Required Elements**:

- Participant flow diagram (enrollment → allocation → analysis)
- Baseline characteristics table (demographics, pre-test scores)
- Effect sizes with confidence intervals (not just p-values)
- All prespecified outcomes (including null results)
- Limitations and potential biases

**Transparency**:

- Make materials available (system code, rubrics, prompts)
- Share de-identified data when possible
- Report full results, not just "significant" findings

### **F.10 Closing Thoughts**

This feasibility study was necessarily limited by time and resource constraints. However, the questions it raises are answerable through careful experimental design.

The system is ready to be tested rigorously. I hope this guidance helps future researchers design studies that can definitively establish whether persistent student modeling improves LLM tutoring outcomes—or demonstrate its limitations.

The field of AI-assisted education is young. We need more rigorous empirical work, not just promising prototypes. I look forward to seeing this system subjected to the scrutiny it deserves.

---

**Contact for Collaboration**: Researchers interested in conducting follow-up studies may contact me at [REDACTED]@[INSTITUTION].edu. I'm happy to provide:

- Access to full implementation code
- Consultation on system setup
- Collaboration on study design
- Co-authorship on rigorous empirical follow-up

The goal is truth, not validation. Let's find it together.
