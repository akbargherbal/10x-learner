# Complete Session Guide: Integrated Learning Protocol

## Overview

This guide demonstrates the complete workflow combining:
1. **Student Model** (conceptual memory)
2. **Workspace Protocol** (concrete code context)  
3. **Socratic Mentor LLM** (synthesis and guided discovery)

By the end of this guide, you'll understand how to run effective learning sessions that maintain continuity while grounding abstract concepts in real code.

---

## Prerequisites

### Required Setup

```bash
# 1. Student Model CLI installed
~/student-model/student.py  # or wherever you installed it

# 2. Learning project cloned
~/learning-projects/monkeytype/  # or your chosen codebase

# 3. Terminal setup
# Two terminal windows/panes:
# - Terminal 1: For student model commands
# - Terminal 2: For workspace investigation
```

### First-Time Setup

```bash
# Initialize your student model
cd ~/student-model
python student.py init

# This creates ~/student_model.json with:
{
  "metadata": {
    "created": "2025-11-06T10:00:00",
    "student_profile": "Self-taught developer learning modern web dev"
  },
  "concepts": {},
  "misconceptions": [],
  "sessions": []
}
```

---

## Session Structure

Every learning session follows this three-phase protocol:

```
┌─────────────────────────────────────────────────────────────┐
│ PHASE 1: Initialization                                      │
│ • Load Student Model context                                 │
│ • Declare learning goal                                      │
│ • Provide initial workspace context                          │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ PHASE 2: Investigation                                       │
│ • Socratic questioning                                       │
│ • Evidence gathering (workspace commands)                    │
│ • Hypothesis testing                                         │
│ • Bridging abstract ↔ concrete                               │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ PHASE 3: Closure                                             │
│ • Update Student Model                                       │
│ • Document session (optional)                                │
│ • Identify next learning goals                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Complete Example: Session 7

### Context

**Learning Goal:** Understand React Context API by exploring monkeytype's theme system

**Prior State:**
- React Context API: 45% mastery, struggling with provider-consumer pattern
- React Hooks: 60% mastery (prerequisite)
- JavaScript Closures: 55% mastery (prerequisite - flagged as low)

---

## PHASE 1: Initialization (5 minutes)

### Step 1.1: Load Conceptual Context

**Terminal 1:**
```bash
cd ~/student-model
python student.py show "React Context API"
python student.py related "React Context API"
```

**Output:**
```
📊 Concept: React Context API
   Mastery:       45%
   Confidence:    low
   First Encountered: 2025-10-28
   Last Reviewed:     2025-11-01
   ⚠️  Struggles:
      - how provider connects to consumers
      - when to use Context vs props drilling
   💡 Breakthroughs:
      - understood that Context avoids prop threading
   🔗 Related Concepts:
      - React Hooks (Mastery: 60%, Last: 2025-11-05) ✓
      - JavaScript Closures (Mastery: 55%, Last: 2025-10-29) ⚠️ LOW
      - React Core (Mastery: 80%, Last: 2025-10-15) ✓
```

### Step 1.2: Paste into Claude

Copy the entire output and paste it into your LLM conversation. Then add context:

**You:**
```
[Paste student model output above]

I want to understand React Context API by exploring how monkeytype 
implements its theme system. I'm looking at components that use 
'theme' but I can't figure out where it comes from.
```

### Step 1.3: LLM Acknowledges Context

**Claude:**
```
Perfect! I can see from your model that you're at 45% mastery with 
Context API and specifically struggling with "how provider connects 
to consumers." You have solid React Hooks knowledge (60%) which is 
good since Context uses hooks, but your JavaScript Closures are at 
55% which might become relevant.

Let's investigate the monkeytype theme system to make this concrete. 
First, can you show me the component where you're confused about 
where 'theme' comes from?

Please run: `cat packages/frontend/src/components/TestArea.tsx`
```

**Note:** Claude has now:
- ✅ Acknowledged your conceptual state
- ✅ Identified your specific struggle
- ✅ Noted potential prerequisite gap
- ✅ Asked for concrete evidence

---

## PHASE 2: Investigation (30-60 minutes)

### Step 2.1: Provide Initial Code Evidence

**Terminal 2:**
```bash
cd ~/learning-projects/monkeytype
cat packages/frontend/src/components/TestArea.tsx
```

**Output:**
```typescript
import React, { useContext } from 'react';
import { ThemeContext } from '../contexts/ThemeContext';
import { TypingTest } from './TypingTest';

export const TestArea: React.FC = () => {
  const theme = useContext(ThemeContext);  // <-- WHERE DOES THIS COME FROM?
  
  return (
    <div className={`test-area theme-${theme.mode}`}>
      <TypingTest />
      <style>
        {theme.customCSS}
      </style>
    </div>
  );
};
```

**You:**
```
[Paste output above]

Line 5 is what confuses me. useContext(ThemeContext) returns the theme, 
but I don't see theme passed as a prop anywhere.
```

### Step 2.2: Socratic Questioning

**Claude:**
```
Excellent! You've identified the exact line. Let's think about this:

1. You're right - 'theme' is NOT passed as a prop to TestArea
2. Yet somehow useContext(ThemeContext) gives you a theme object
3. This is the "provider-consumer" pattern you marked as a struggle

Before we trace where theme comes from, what's your current hypothesis 
about how useContext() gets data? Take a guess - even if you're unsure.
```

**You:**
```
Um... maybe it's like a global variable that useContext reads? 
Or maybe ThemeContext stores the value somehow?
```

**Claude:**
```
Good thinking! You're on the right track with "ThemeContext stores 
the value." It's not quite a global variable, but there IS a storage 
mechanism. Let's find it.

The pattern is:
1. Someone creates the "storage" (ThemeContext)
2. Someone puts data INTO the storage (Provider)
3. Someone reads FROM the storage (useContext)

Let's find step 2 - where data goes INTO ThemeContext. Run this:
`grep -r 'ThemeContext.Provider' packages/frontend/src/ --include="*.tsx"`
```

### Step 2.3: Evidence Gathering

**Terminal 2:**
```bash
grep -r 'ThemeContext.Provider' packages/frontend/src/ --include="*.tsx"
```

**Output:**
```
packages/frontend/src/App.tsx:      <ThemeContext.Provider value={theme}>
packages/frontend/src/contexts/ThemeContext.tsx:  return <ThemeContext.Provider value={currentTheme}>
```

**You:**
```
[Paste output]

So there's a Provider in App.tsx and in ThemeContext.tsx itself?
```

**Claude:**
```
Excellent observation! Yes, you found TWO mentions. Let's see the 
ThemeContext.tsx file first since that's probably where the Context 
is created and the Provider is defined. Run:

`cat packages/frontend/src/contexts/ThemeContext.tsx`
```

### Step 2.4: Deep Dive

**Terminal 2:**
```bash
cat packages/frontend/src/contexts/ThemeContext.tsx
```

**Output:**
```typescript
import { createContext, useState, ReactNode } from 'react';

// 1. Create the "storage container"
export const ThemeContext = createContext<Theme>(defaultTheme);

// 2. Create a component that fills the container
export const ThemeProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [currentTheme, setCurrentTheme] = useState<Theme>(defaultTheme);
  
  // ... theme switching logic ...
  
  return (
    <ThemeContext.Provider value={currentTheme}>
      {children}
    </ThemeContext.Provider>
  );
};
```

**You:**
```
[Paste output]

Ok so ThemeContext is created with createContext, and ThemeProvider 
wraps things in ThemeContext.Provider...
```

### Step 2.5: Synthesis and Teaching Moment

**Claude:**
```
YES! Now let's connect this to your struggle. You said you don't 
understand "how provider connects to consumers." Let me show you with 
the actual code you just shared:

**The Three Pieces:**

1. **Create the tunnel** (line 4):
   `createContext` makes a "data tunnel" called ThemeContext

2. **Put data in the tunnel** (lines 7-15):
   ThemeProvider wraps children in `<ThemeContext.Provider value={currentTheme}>`
   This BROADCASTS currentTheme into the tunnel

3. **Read from the tunnel** (TestArea.tsx line 5):
   `useContext(ThemeContext)` RECEIVES whatever was broadcast

Think of it like a radio station:
- createContext = assigns a frequency (e.g. FM 101.5)
- Provider = broadcasts data on that frequency
- useContext = tunes in to that frequency to receive data

The key insight: TestArea doesn't need theme as a prop because it 
"tunes in" to the ThemeContext frequency!

Now, where is ThemeProvider actually used? Let's check App.tsx:
`cat packages/frontend/src/App.tsx | grep -B 10 -A 10 ThemeProvider`
```

### Step 2.6: Final Evidence

**Terminal 2:**
```bash
cat packages/frontend/src/App.tsx | grep -B 10 -A 10 ThemeProvider
```

**Output:**
```typescript
import { ThemeProvider } from './contexts/ThemeContext';

function App() {
  return (
    <ThemeProvider>
      <Router>
        <Header />
        <MainContent>
          <TestArea />    {/* <-- This can now access theme! */}
        </MainContent>
      </Router>
    </ThemeProvider>
  );
}
```

**You:**
```
[Paste output]

OH! So ThemeProvider wraps the whole app, which means any component 
inside (like TestArea) can useContext to get the theme. The "connection" 
is that TestArea is wrapped by ThemeProvider!
```

**Claude:**
```
EXACTLY! That's the breakthrough! Let me connect this to your model:

**Your logged struggle:** "how provider connects to consumers"

**The answer:** Consumers (TestArea) must be CHILDREN of Provider 
(wrapped inside <ThemeProvider>). The "connection" is the component 
tree itself!

If TestArea were OUTSIDE <ThemeProvider>, useContext would fail. 
The wrapping creates the connection.

**Visual:**
```
<ThemeProvider>  ← broadcasts theme
    ↓
  <Router>
    ↓
  <TestArea>  ← receives theme via useContext
```

This is why it's called "provider-consumer" - the Provider WRAPS 
consumers in the tree.

Does this click with your mental model now?
```

**You:**
```
Yes! The "tunnel" metaphor helps. Provider creates the tunnel, 
consumers tune in, but ONLY if they're wrapped by the Provider.

I think I get it now. Let me update my model.
```

---

## PHASE 3: Closure (5 minutes)

### Step 3.1: Claude Generates Update Commands

**Claude:**
```
Excellent! You've had a real breakthrough with the provider-consumer 
pattern. Let's update your Student Model to capture this learning.

Based on our session, please run these commands:

```bash
cd ~/student-model

python student.py update "React Context API" --mastery 60 --confidence medium

python student.py breakthrough "React Context API" \
  "understood provider-consumer pattern by tracing ThemeContext in monkeytype - providers wrap consumers in component tree, creating the 'connection'"

python student.py struggle "React Context API" \
  "still unclear when to use Context vs props drilling - performance implications?"

python student.py link "React Context API" "Component Tree Architecture"
```

The remaining struggle about when to use Context vs props is a great 
topic for next session!
```

### Step 3.2: Execute Update Commands

**Terminal 1:**
```bash
cd ~/student-model

python student.py update "React Context API" --mastery 60 --confidence medium

python student.py breakthrough "React Context API" \
  "understood provider-consumer pattern by tracing ThemeContext in monkeytype - providers wrap consumers in component tree, creating the 'connection'"

python student.py struggle "React Context API" \
  "still unclear when to use Context vs props drilling - performance implications?"

python student.py link "React Context API" "Component Tree Architecture"
```

**Output:**
```
✅ Updated 'React Context API': mastery 45% → 60%, confidence low → medium
✅ Added breakthrough to 'React Context API'
✅ Added struggle to 'React Context API'
✅ Linked 'React Context API' → 'Component Tree Architecture'
```

### Step 3.3: Verify Update

**Terminal 1:**
```bash
python student.py show "React Context API"
```

**Output:**
```
📊 Concept: React Context API
   Mastery:       60%  ⬆️ +15%
   Confidence:    medium  ⬆️
   Last Reviewed:     2025-11-06  ← TODAY
   ⚠️  Struggles:
      - when to use Context vs props drilling - performance implications?
   💡 Breakthroughs:
      - understood that Context avoids prop threading
      - understood provider-consumer pattern by tracing ThemeContext 
        in monkeytype - providers wrap consumers in component tree
   🔗 Related Concepts:
      - React Hooks (60%)
      - JavaScript Closures (55%) ⚠️
      - React Core (80%)
      - Component Tree Architecture (NEW!)
```

### Step 3.4: Optional Session Documentation

**Terminal 1:**
```bash
code SESSION_07_react_context.md
```

**Template (filled by you):**
```markdown
# Session 7: React Context API Investigation

**Date:** 2025-11-06
**Duration:** 45 minutes
**Project:** monkeytype theme system

## Goal
Understand how React Context API implements provider-consumer pattern

## Starting State
- Mastery: 45%
- Struggle: how provider connects to consumers

## Investigation Process
1. Started with TestArea.tsx showing useContext usage
2. Searched for Provider with grep
3. Examined ThemeContext.tsx to see Provider definition
4. Checked App.tsx to see Provider wrapping
5. Traced the connection through component tree

## Key Insights
- Provider must WRAP consumers in component tree
- "Connection" is the parent-child relationship
- useContext only works inside Provider's children
- Radio station metaphor: createContext = frequency, Provider = broadcaster, useContext = receiver

## Breakthrough
Finally understood that provider-consumer pattern is about component 
tree structure, not some magic global state. Providers wrap consumers!

## Remaining Questions
- When is Context better than props drilling?
- Performance implications?
- Can providers be nested?

## Ending State
- Mastery: 60%
- Confidence: medium
- New link: Component Tree Architecture

## Next Session Ideas
- Explore Context performance vs props
- Investigate nested providers in monkeytype
- Try implementing custom Context for practice
```

---

## Session Patterns

### Pattern 1: Starting with Low Mastery (<30%)

If your mastery is very low, spend more time on fundamentals:

**You:**
```
[Paste student model showing React Hooks at 25%]

I want to understand useEffect but I'm really confused.
```

**Claude:**
```
I see you're at 25% mastery with Hooks. Before we dive into useEffect 
specifically, let's make sure your foundation is solid. 

Your model shows JavaScript Closures at 30% and React Core at 40%. 
useEffect involves both concepts. Let's check: what's your understanding 
of what a React component IS? 

Then we'll ground it in code: `cat` a simple component from your project.
```

**Key:** Claude checks prerequisites and may recommend remedial work before advancing.

---

### Pattern 2: Detecting Prerequisite Gaps

**Claude:**
```
[After seeing your confusion about custom Hooks]

Wait - I'm checking your related concepts. You have JavaScript Closures 
at 55%, marked as LOW. Custom Hooks depend heavily on closure behavior. 

I suspect your confusion about custom Hooks is actually confusion about 
closures. Let's test this hypothesis. In the custom Hook code you showed, 
what do you think the function returned by useTimer "remembers"?

[If you can't answer clearly]

Let's pause on custom Hooks and strengthen closures first. This is a 
prerequisite gap. Would you like to do a brief closure review session, 
or do you want to push forward and risk continued confusion?
```

**Key:** Claude uses prerequisite tracking to diagnose confusion roots.

---

### Pattern 3: Building on Recent Breakthroughs

**You:**
```
[Paste student model showing recent breakthrough with useEffect cleanup]

I'm now trying to understand useMemo...
```

**Claude:**
```
Great! I see you had a breakthrough with useEffect cleanup last session 
(2 days ago). useMemo is similar in some ways - it also takes a dependency 
array and optimizes when things run.

Let's leverage what you learned. In your useEffect breakthrough, you 
understood that cleanup runs before the NEXT effect. What do you think 
useMemo does when its dependencies change?

[Guides investigation building on prior success]
```

**Key:** Claude creates continuity by referencing recent learning.

---

## Common Pitfalls and Solutions

### Pitfall 1: Skipping Student Model Context

❌ **Wrong:**
```
You: "I'm confused about React Context"
[Jump straight to code without loading model]
```

✅ **Right:**
```
You: [Load and paste student model first]
Then: "I'm confused about React Context"
```

**Why it matters:** Claude can't tailor teaching to your level or struggles without context.

---

### Pitfall 2: Dumping Too Much Code at Once

❌ **Wrong:**
```
You: [Paste 5 files totaling 500 lines]
"I'm confused about all of this"
```

✅ **Right:**
```
You: "I'm confused about how theme flows through the app"
Claude: "Let's start with the entry point: `cat src/App.tsx`"
You: [Paste just App.tsx]
Claude: "I see ThemeProvider. Now let's see its definition: `cat src/contexts/ThemeContext.tsx`"
```

**Why it matters:** Incremental investigation maintains focus and prevents overwhelm.

---

### Pitfall 3: Not Updating Model After Session

❌ **Wrong:**
```
[Have breakthrough, close laptop, forget to update model]
[Next session: Claude has no memory of breakthrough]
```

✅ **Right:**
```
[At end of every session, run update commands]
[Next session: Claude sees breakthrough in model]
```

**Why it matters:** The entire system depends on persistent memory. No update = amnesia returns.

---

### Pitfall 4: Vague Struggle Descriptions

❌ **Wrong:**
```
python student.py struggle "React Hooks" "it's confusing"
```

✅ **Right:**
```
python student.py struggle "React Hooks" \
  "don't understand when useEffect cleanup runs - does it run on every render or only on unmount?"
```

**Why it matters:** Specific struggles enable targeted future teaching.

---

## Tips for Effective Sessions

### 1. Prepare Your Workspace

Before starting any session:
```bash
# Terminal 1: Student Model
cd ~/student-model
python student.py list  # Review what you have

# Terminal 2: Project
cd ~/learning-projects/your-project
ls -la  # Orient yourself
```

### 2. Set a Clear Goal

Be specific:
- ✅ "Understand how monkeytype's theme system uses Context"
- ❌ "Learn React"

### 3. Trust the Socratic Process

Don't rush to answers:
- Claude asks: "What do you think X does?"
- You guess (even if unsure)
- Claude guides: "Let's test that: run Y command"
- Evidence confirms or refutes
- Insight emerges

### 4. Take Breaks

If a session exceeds 60 minutes, consider:
- Pausing and resuming later
- Splitting into multiple sessions
- Each session = one focused concept

### 5. Document Notable Sessions

Not every session needs documentation, but document:
- Major breakthroughs
- Complex investigations
- Sessions you might reference later

### 6. Review Your Model Weekly

```bash
python student.py list
python student.py stats
```

Helps you:
- Identify stale concepts
- Plan next learning priorities
- Celebrate progress

---

## Example Session Templates

### Quick Investigation (20-30 min)

For when you encounter confusion while coding:

```
1. Load model: `show "Concept"` + `related "Concept"`
2. Paste into Claude with: "Quick question about X in my code..."
3. Investigate with workspace commands
4. Update model: `session-end --update "Concept:+5:same"`
```

---

### Deep Dive (60-90 min)

For dedicated learning time:

```
1. Load model: `show "Concept"` + `related "Concept"`
2. Declare goal: "I want to deeply understand X by exploring Y codebase"
3. Extended investigation with multiple grep/cat cycles
4. Update model: full session-end with breakthrough + new struggle
5. Document session in markdown
```

---

### Prerequisite Remediation (30-45 min)

When Claude detects a gap:

```
1. Load model for BOTH main concept and prerequisite
2. Focus on prerequisite concept
3. Find examples in codebase
4. Update BOTH concepts (prerequisite improved, note in main concept)
```

---

## Next Steps

After reading this guide:

1. **Try a practice session**
   - Pick a simple concept (e.g., "Array Methods")
   - Add it to your model: `python student.py add "Array Methods" 40 low`
   - Run a short session investigating .map() or .reduce() in a codebase
   - Update model afterward

2. **Read the other docs**
   - `student_model_usage.md` - Complete command reference
   - `workspace_protocol.md` - Detailed command patterns
   - `prompts/socratic_mentor_v1.md` - The LLM persona

3. **Start building your model**
   - Add 5-10 concepts you're currently learning
   - Set initial mastery/confidence estimates
   - Link prerequisites
   - Start using in real sessions

4. **Iterate**
   - The first few sessions will feel awkward
   - You'll find your rhythm after 3-4 sessions
   - Adjust commands/workflow to your preference

---

## Summary

Effective sessions combine:

| Phase | Student Model | Workspace Protocol | Claude |
|-------|--------------|-------------------|--------|
| **Init** | Provide conceptual context | Provide initial code context | Acknowledge both |
| **Investigate** | Referenced for struggles/gaps | Incremental evidence gathering | Bridge abstract ↔ concrete |
| **Close** | Updated with new state | (ephemeral, no updates) | Generate update commands |

The magic happens when Claude synthesizes:
- **What you know** (from Student Model)
- **What you're looking at** (from Workspace)
- **How to bridge them** (Socratic method)

This creates:
- ✅ Continuity (memory across sessions)
- ✅ Context (grounded in real code)
- ✅ Development (progressive understanding)

**Result:** AI tutoring that feels like working with a mentor who actually knows you and your journey.
