# How I Became a 10x Learner: Building My Own AI Tutor to Conquer Code

Hey everyone, I'm Akbar, a recent Computer Science grad. Last year, I turned my senior thesis into a personal experiment that transformed how I learn programming. The result? I went from fumbling through tutorials and Stack Overflow rabbit holes to systematically mastering complex concepts—like React Hooks, JavaScript closures, and full-stack web dev—in weeks instead of months. I call it becoming a "10x learner," not because I'm some prodigy, but because I hacked together a system that makes AI tutors remember me, diagnose my blind spots, and guide me like a real mentor.

In this article, I'll break down the problem I was facing, the system I built (detailed in my thesis), how it works in practice, and why it supercharged my learning. If you're a self-taught dev, a student wrestling with codebases, or anyone using tools like ChatGPT/Claude for learning, this might change your game. All the code is open-source—links at the end.

## The Frustration: Why AI Tutors Forget You

Picture this: It's 2 AM, and I'm staring at a React codebase, confused about custom Hooks. I fire up Claude (Anthropic's LLM) and ask for help. It gives a solid explanation. Cool, I think I get it. But the next day, when I hit a similar snag, Claude starts from scratch again—like we never talked. No memory of my "aha" moment yesterday, no recollection of my shaky grasp on prerequisites like closures. It's like Groundhog Day for debugging.

This is "AI amnesia." LLMs are brilliant at one-off answers but terrible at building on past interactions. In education, that's deadly. Learning isn't isolated Q&A; it's a journey. Human tutors remember your weak spots, spot patterns in your confusion, and connect dots over time. AI? Not so much.

In my thesis, I called this the "cost of amnesia": repetitive explanations, missed root causes (like prerequisite gaps), and a transactional feel that kills momentum. As a self-learner diving into open-source projects like monkeytype, I needed better. So, I built a system to give AI a memory—and force it to ground everything in my actual code.

## The Breakthrough: A Dual-Context AI Tutor System

My solution is a tripartite setup: a persistent "Student Model" for conceptual knowledge, a "Workspace Protocol" for concrete code evidence, and a Socratic LLM persona to tie it all together. It's not fancy—no ML training, just smart prompting, a JSON file, and terminal commands. But it works.

### 1. The Student Model: Your Brain's External Hard Drive

This is the core: a JSON file that tracks what you know (and crucially, what you _don't_). It's like a personal CRM for your learning gaps.

- **Key Fields**: For each concept (e.g., "React Hooks"):
  - Mastery (0-100%): Self-assessed progress.
  - Confidence (low/medium/high): Because knowing facts ≠ feeling confident.
  - Struggles: Specific pain points, like "dependency arrays confuse me."
  - Breakthroughs: Wins, like "finally got cleanup functions."
  - Related Concepts: Prerequisites, forming a graph (e.g., Hooks depend on Closures).

I manage it with a simple CLI tool, `student.py` (Python script, no deps). Commands like:

```
python student.py add "React Hooks" 30 low
python student.py struggle "React Hooks" "when to use useMemo vs useCallback"
python student.py breakthrough "React Hooks" "understood useEffect cleanup via timer example"
```

Output is pretty and pasteable into chats:

```
📊 Concept: React Hooks
   Mastery: 60%
   Confidence: medium
   ⚠️ Struggles: dependency array inference
   💡 Breakthroughs: understood useEffect cleanup
   🔗 Related: JavaScript Closures (55%)
```

This model persists across sessions and projects. No more re-explaining your baseline to AI.

### 2. The Workspace Protocol: No Assumptions, Only Evidence

Conceptual memory is great, but AI still hallucinates about your code. Enter the Workspace Protocol: force the LLM to request _proof_ from your actual files using Unix tools.

- Tools: `cat` (view files), `grep` (search), `ls` (structure), `find` (locate), `git` (history).
- Rule: LLM never assumes. It asks for evidence incrementally.

Example: Instead of guessing, it says, "To understand data flow, run `grep -r 'useContext' src/` and paste the output."

This turns tutoring into an investigation. You run commands, paste results, and the AI analyzes. It prevents wrong advice and teaches you debugging skills as a bonus.

### 3. The Socratic Mentor: AI as Your Patient Guide

I configured Claude with a detailed prompt (full in my thesis appendix) to act as a Socratic mentor. Key rules:

- **Mandatory Protocol**: Won't teach until you paste Student Model output _and_ workspace evidence.
- **Diagnostic Flow**: Checks prerequisites. If Hooks are at 30% and Closures at 50%, it hypothesizes: "Your confusion might stem from closures. Let's test that."
- **Socratic Style**: Questions over lectures. "What do you think happens on line 15?"
- **End-of-Session**: Summarizes, generates update commands for the model.

The prompt enforces: No generic answers. Always bridge abstract (model) to concrete (code).

## How It Works: A Real Session Walkthrough

Let's say I'm stuck on React Context in a frontend project.

1. **Start**: I tell Claude, "Help with React Context API."

   Claude: "First, paste output from `python student.py show 'React Context API'` and `python student.py related 'React Context API'`."

2. **Load Conceptual Context**: I run the commands. Model shows 45% mastery, struggle with "provider patterns," prerequisite "React Core" at 80%.

   Claude: "Got it—you're at 45% with a noted struggle on providers. What file is confusing you?"

3. **Load Concrete Context**: I say "TestArea.tsx." Claude: "Run `cat src/components/TestArea.tsx` and paste."

   I paste the code.

4. **Investigate**: Claude spots useContext on line 50. "Your model notes provider struggles. Line 50 uses useContext—where's the Provider? Run `grep -r 'ThemeContext.Provider' src/`."

   Loop continues: Analyze output, ask questions, request more evidence.

5. **Breakthrough**: I say, "Oh, it avoids prop drilling!" Claude: "Yes! That's a breakthrough. Update your model: `python student.py breakthrough 'React Context API' 'understood prop drilling avoidance'`."

6. **Wrap Up**: Summarizes insights, suggests next steps.

A 30-minute session feels like pair-programming with a mentor who knows my history.

## The Experiment: 4 Weeks, 1 Guinea Pig (Me)

For my thesis feasibility study, I used this on myself over four weeks, learning advanced web dev (React, Node, databases) via monkeytype codebase. Sessions: 90-120 minutes, 3-4x/week.

- **Overhead**: ~2-4 minutes/session for model updates/commands. Totally worth it.
- **Qualitative Wins**:
  - Caught prerequisite gaps 3x (e.g., closures blocking Hooks).
  - Reduced repetition: AI referenced past breakthroughs.
  - Deeper understanding: Evidence requests taught me grep/git mastery.
  - Metacognition boost: Updating the model forced reflection.
- **Metrics**: Mastery scores rose 20-40% per concept. Struggles resolved from 12 to 3. But n=1—take with salt.

Why 10x? Time to "get" concepts dropped from days to hours. I tackled harder projects faster, with less frustration.

## Lessons Learned: Becoming a 10x Learner

1. **Track Your Ignorance**: Cataloging struggles isn't depressing—it's empowering. It turns vague confusion into actionable fixes.
2. **Demand Evidence**: Don't let AI assume. This protocol made me a better investigator.
3. **Reflect Actively**: End-of-session updates crystallized learning.
4. **Prerequisites Matter**: The model/graph exposed hidden gaps early.
5. **AI as Partner, Not Oracle**: Socratic questioning built intuition, not just answers.

Limitations: It's manual (no auto-updates), CLI-only (not for everyone), and untested on others. Ethical note: Your model is private—keep it that way.

## Try It Yourself

Repo: [GitHub link placeholder—fork my thesis code].

- Setup: Clone, create `student-model.json`, chat with Claude using the prompt.
- Adapt: Tweak for your stack (add Python/Java tools).

If you build on this, hit me up—I'd love to hear. Who knows, maybe we'll make 100x learners next.

Thanks for reading. Now go scaffold your ignorance and level up.

_[Based on my thesis, B.S. Computer Science. Thesis: "The Scaffolding of Ignorance: A Persistent Student Model for Mitigating AI Amnesia in LLM-Based Programming Tutors."]_
