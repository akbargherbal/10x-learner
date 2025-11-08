# Workspace Context Protocol for Learning

## Overview

The **Workspace Context Protocol** defines how learners share their code investigation environment with an LLM tutor using standard Unix command-line tools. This protocol complements the Student Model system by providing **concrete code context** to ground abstract conceptual knowledge.

### Core Philosophy

**Evidence-Based Investigation:** The LLM never assumes file contents, directory structure, or implementation details. Every claim about the codebase must be supported by evidence explicitly provided through terminal commands.

**Request-Response Pattern:** The LLM requests specific evidence → You provide exact command output → The LLM analyzes → Repeat. This creates a tight feedback loop that prevents wasted context and keeps both parties grounded in facts.

---

## Separation of Concerns

| System | Responsibility | Example |
|--------|---------------|---------|
| **Student Model** | Abstract conceptual knowledge | "React Context API: 45% mastery, struggling with provider pattern" |
| **Workspace Protocol** | Concrete code context | "ThemeContext.tsx line 50: `useContext(ThemeContext)`" |
| **Claude** | Synthesis & Socratic teaching | "Your struggle with providers maps to this specific code pattern..." |

The Student Model tracks **what you understand** across all projects. The Workspace Protocol shows **what you're currently looking at** in a specific codebase.

---

## Core Command Patterns

### 1. File Viewing

**Purpose:** Examine specific file contents

```bash
# View entire file
cat path/to/file.ts

# View with line numbers
cat -n path/to/file.ts

# View specific line range (if supported)
sed -n '45,60p' path/to/file.ts

# View with context around pattern
grep -B 5 -A 5 "pattern" path/to/file.ts
```

**When to use:**
- LLM asks: "Can you show me the file where X is defined?"
- You've mentioned a specific file as confusing
- Following up on grep results to see full context

**Example request from LLM:**
> "Let's examine the component you're confused about. Please run: `cat packages/frontend/src/components/TestArea.tsx`"

---

### 2. Searching Across Files

**Purpose:** Find patterns, usage examples, definitions

```bash
# Basic recursive search
grep -r "pattern" path/

# Search specific file types
grep -r "pattern" path/ --include="*.ts" --include="*.tsx"

# Show filenames only
grep -rl "pattern" path/

# Show context (lines before/after)
grep -r -B 3 -A 3 "pattern" path/

# Case-insensitive search
grep -ri "pattern" path/

# Search for whole word only
grep -rw "pattern" path/
```

**When to use:**
- Finding where a function/class is defined
- Seeing all usage examples of a pattern
- Tracing how data flows through files
- Understanding project-wide conventions

**Example request from LLM:**
> "To understand how theme data flows, run: `grep -r 'ThemeContext' --include='*.tsx' src/`"

---

### 3. Directory Structure

**Purpose:** Understand project layout, find relevant files

```bash
# List directory contents
ls -la path/

# Recursive tree view (if tree is installed)
tree path/ -L 2  # 2 levels deep
tree path/ -L 2 -I 'node_modules|dist'  # ignore folders

# Find specific files
find path/ -name "*.tsx" -type f
find path/ -name "*Context*" -type f

# Find recently modified files
find path/ -name "*.ts" -type f -mtime -7  # last 7 days
```

**When to use:**
- Starting investigation of unfamiliar codebase
- Finding where components/modules live
- Understanding project organization
- Locating relevant files before detailed examination

**Example request from LLM:**
> "Let's see the component structure. Run: `ls -la packages/frontend/src/components/`"

---

### 4. Git History & Context

**Purpose:** Understand evolution, find relevant commits

```bash
# File history (compact)
git log --oneline path/to/file

# File history (with diffs)
git log -p path/to/file

# Show specific commit content
git show commit_hash:path/to/file

# See what changed in a commit
git show commit_hash

# Find when line was added (blame)
git blame path/to/file | grep "pattern"

# Search commit messages
git log --grep="context" --oneline
```

**When to use:**
- Understanding why code is structured a certain way
- Finding when a feature was added
- Seeing examples in commit diffs
- Tracing evolution of confusing code

**Example request from LLM:**
> "Let's see when this Context pattern was introduced. Run: `git log --oneline packages/frontend/src/contexts/ThemeContext.tsx`"

---

### 5. Code Structure & Dependencies

**Purpose:** Understand imports, exports, relationships

```bash
# Find imports of a module
grep -r "from.*ThemeContext" src/ --include="*.tsx"

# Find all exports in a file
grep "export" path/to/file.ts

# See package dependencies
cat package.json | grep -A 20 "dependencies"

# Find TypeScript interfaces
grep -r "interface.*Theme" src/ --include="*.ts"
```

**When to use:**
- Tracing dependency chains
- Understanding module relationships
- Finding type definitions
- Mapping data flow

**Example request from LLM:**
> "Let's see what components use this Context. Run: `grep -r 'useContext(ThemeContext)' src/ --include='*.tsx'`"

---

## Investigation Workflow

### Phase 1: High-Level Orientation

**Goal:** Understand project structure and locate relevant areas

```bash
# 1. See top-level structure
ls -la
cat README.md  # if exists

# 2. Understand organization
tree src/ -L 2 -I 'node_modules|dist'
# or
find src/ -type d -maxdepth 2

# 3. Find relevant files
find src/ -name "*Context*" -type f
find src/ -name "*Theme*" -type f
```

**LLM behavior:** Asks broad questions, requests structure overview, helps you narrow scope

---

### Phase 2: Targeted Investigation

**Goal:** Examine specific files and patterns

```bash
# 4. View file structure (without full content)
grep "^import\|^export\|^function\|^class\|^const.*=" path/to/file.ts

# 5. Search for specific patterns
grep -r "useContext" src/ --include="*.tsx"

# 6. View relevant files
cat src/contexts/ThemeContext.tsx
cat src/components/TestArea.tsx
```

**LLM behavior:** Requests specific evidence, tests hypotheses, asks what you observe

---

### Phase 3: Deep Dive

**Goal:** Understand specific confusing sections

```bash
# 7. Focus on problematic area
cat -n src/components/TestArea.tsx | sed -n '45,60p'

# 8. Trace dependencies
grep -r "ThemeContext" src/ --include="*.tsx"

# 9. See historical context (if relevant)
git log -p --follow src/contexts/ThemeContext.tsx
```

**LLM behavior:** Connects concrete code to abstract concepts from Student Model, explains patterns, asks Socratic questions

---

## Integration with Student Model

### Complete Session Flow

#### **Step 1: Load Conceptual Context** (Student Model)

```bash
terminal1:~/student-model$ python student.py show "React Context API"
terminal1:~/student-model$ python student.py related "React Context API"
```

Output provides:
- Current mastery level
- Known struggles
- Recent breakthroughs
- Prerequisite concepts and their status

**Paste this output into Claude** to establish conceptual baseline.

---

#### **Step 2: Provide Concrete Context** (Workspace Protocol)

```bash
terminal2:~/your-project$ ls -la src/components/
terminal2:~/your-project$ cat src/components/ConfusingComponent.tsx
```

**Paste command outputs into Claude** to ground the discussion in actual code.

---

#### **Step 3: Iterative Investigation**

Claude now has both:
- **Abstract knowledge:** "Student at 45% mastery, struggling with provider pattern"
- **Concrete situation:** "Looking at line 50 of TestArea.tsx which uses useContext"

Claude can:
- Connect your logged struggle to this specific code
- Check prerequisites (Closures at 55% - might be relevant)
- Request additional evidence to test hypotheses
- Provide targeted explanation that bridges abstract ↔ concrete

**Example dialogue:**

```
Claude: "I see useContext on line 50. Your model shows you're at 60%
        mastery with React Hooks. What do you think useContext() 
        returns here?"

You: "The theme object?"

Claude: "Right direction! Let's verify. Run:
        grep -r 'ThemeContext' src/ --include='*.tsx'"

[You paste grep output]

Claude: "Look at line 3 of App.tsx in your grep results. What do 
        you see wrapping the component tree?"

You: "ThemeContext.Provider..."

Claude: "Exactly! This is the provider-consumer pattern you marked
        as a struggle. The Provider at the top 'broadcasts' the value,
        and useContext 'receives' it anywhere below. Let's see the
        Provider definition to understand the connection..."
```

---

#### **Step 4: Session End** (Back to Student Model)

```bash
terminal1:~/student-model$ python student.py session-end \
  --update "React Context API:60:medium" \
  --breakthrough "React Context API:understood provider-consumer by tracing ThemeContext in real code" \
  --struggle "React Context API:still unclear when Context better than props"
```

**Optional:** Document the session

```bash
terminal1:~/student-model$ code SESSION_07_context_investigation.md
```

---

## Command Templates

Save these in your shell profile for quick access:

```bash
# Add to ~/.bashrc or ~/.zshrc

# Quick file view
alias catnum='cat -n'

# Search in source files
alias grepsrc='grep -r --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx"'

# Compact tree
alias tree2='tree -L 2 -I "node_modules|dist|build"'
alias tree3='tree -L 3 -I "node_modules|dist|build"'

# Git shortcuts
alias glogfile='git log --oneline'
alias gshowfile='git show'
```

---

## Best Practices

### ✅ DO:

1. **Start broad, narrow progressively**
   - Begin with directory structure (ls, tree)
   - Then search patterns (grep)
   - Finally examine files (cat)

2. **Provide exact command output**
   - Copy-paste complete terminal output
   - Include command prompts if they add context
   - Don't summarize or paraphrase

3. **Let the LLM guide investigation**
   - Wait for specific evidence requests
   - Trust the Socratic process
   - Resist urge to dump everything at once

4. **Use context flags with grep**
   - `-B 3 -A 3` provides surrounding lines
   - Helps LLM see patterns without requesting full file

5. **Combine commands when logical**
   ```bash
   cat src/App.tsx | grep -B 5 -A 5 "Provider"
   ```

### ❌ DON'T:

1. **Don't assume the LLM knows file contents**
   - Even if you mentioned a file earlier
   - Even if it's a "common" file (README, package.json)
   - Always provide evidence when requested

2. **Don't paste massive outputs**
   - If a file is 1000+ lines, ask LLM: "This file is large. Which section?"
   - Use grep to narrow before cat
   - Consider showing structure first: `grep "^function\|^class\|^const" file.ts`

3. **Don't editorialize in outputs**
   - Provide raw command output
   - Don't add comments like "// THIS IS THE CONFUSING PART"
   - Let the LLM ask questions about what you find confusing

4. **Don't context-switch unnecessarily**
   - Have terminal ready before starting session
   - Keep both terminal windows open
   - Avoid switching to IDE/browser mid-investigation

---

## Troubleshooting

### Problem: Command produces too much output

**Solution:** Narrow with additional flags

```bash
# Instead of:
cat very_large_file.ts  # 2000 lines

# Do:
grep -B 5 -A 5 "relevantPattern" very_large_file.ts
# or
sed -n '100,200p' very_large_file.ts  # specific range
```

---

### Problem: Can't find the relevant file

**Solution:** Incremental discovery

```bash
# Start broad
find src/ -name "*.tsx"

# Narrow by pattern
find src/ -name "*Theme*"

# Or search content
grep -rl "ThemeContext" src/
```

---

### Problem: grep returns binary file matches

**Solution:** Exclude binary files

```bash
grep -rI "pattern" src/  # -I skips binary files
# or
grep -r "pattern" src/ --include="*.ts" --include="*.tsx"
```

---

### Problem: Git commands fail

**Solution:** Check you're in a git repo

```bash
git status  # Verify git repo
cd path/to/project  # Navigate to root if needed
```

---

### Problem: Permission denied

**Solution:** Check file permissions, use sudo if appropriate

```bash
ls -la path/to/file  # Check permissions
# If it's truly restricted, explain to LLM:
"I don't have access to this file, but I can see [alternative evidence]"
```

---

## Examples

### Example 1: Understanding React Context

**Your question:** "I don't understand how theme data gets to this component"

**LLM:** "Let's start with structure. Run: `ls -la src/components/`"

```bash
terminal2:~/monkeytype$ ls -la src/components/
drwxr-xr-x  TestArea.tsx
drwxr-xr-x  Header.tsx
...
```

**LLM:** "Now show me the confusing component: `cat src/components/TestArea.tsx`"

```bash
terminal2:~/monkeytype$ cat src/components/TestArea.tsx
import { useContext } from 'react';
import { ThemeContext } from '../contexts/ThemeContext';

export const TestArea = () => {
  const theme = useContext(ThemeContext);  // <-- Where does theme come from?
  ...
```

**LLM:** "I see useContext on line 5. Let's find where ThemeContext is provided: `grep -r 'ThemeContext.Provider' src/`"

```bash
terminal2:~/monkeytype$ grep -r 'ThemeContext.Provider' src/
src/App.tsx:  return <ThemeContext.Provider value={theme}>
```

**LLM:** "Aha! App.tsx has the Provider. Show me that: `cat src/App.tsx`"

[Process continues...]

---

### Example 2: Tracing Authentication Flow

**Your question:** "How does JWT authentication work in this API?"

**LLM:** "First, let's see the API structure: `ls -la src/api/`"

**LLM:** "Now search for JWT usage: `grep -r 'jwt\|JWT' src/api/ -i`"

**LLM:** "I see middleware/auth.ts mentioned. Show me: `cat src/api/middleware/auth.ts`"

**LLM:** "This middleware checks tokens. Where are tokens attached to requests? `grep -r 'Authorization' src/api/`"

[Process continues...]

---

## Advanced Patterns

### Pattern 1: Tracing Data Flow

```bash
# 1. Find where data enters
grep -r "useState\|useReducer" src/ --include="*.tsx"

# 2. Trace through components
grep -r "props\.theme" src/ --include="*.tsx"

# 3. See where it's consumed
grep -r "theme\." src/ --include="*.tsx"
```

---

### Pattern 2: Understanding Dependencies

```bash
# 1. See what this module imports
head -20 src/components/TestArea.tsx | grep "^import"

# 2. Find who imports this module
grep -r "from.*TestArea" src/ --include="*.tsx"

# 3. Visualize the web
# (Combine outputs to understand relationships)
```

---

### Pattern 3: Historical Investigation

```bash
# 1. When was this pattern introduced?
git log --oneline --follow src/contexts/ThemeContext.tsx

# 2. What was the commit message?
git log --grep="context" --oneline

# 3. See the actual changes
git show abc123:src/contexts/ThemeContext.tsx
```

---

## Integration with Persona Prompt

The LLM persona is trained to:

1. **Request workspace context naturally**
   - "Let's ground this in your code. Run: `cat ...`"
   - "To test that hypothesis: `grep ...`"

2. **Never assume, always verify**
   - Won't proceed without evidence
   - Explicitly states: "I don't know what's in that file until you show me"

3. **Guide investigation incrementally**
   - Requests one command at a time
   - Analyzes output before next request
   - Maintains tight feedback loop

4. **Bridge workspace ↔ student model**
   - "Your model shows you struggled with X. Line 50 of this file is exactly that pattern..."
   - "You had a breakthrough with Y last week. This code uses the same principle..."

---

## Summary

The Workspace Protocol provides **concrete grounding** for **abstract conceptual knowledge**. By combining:

- **Student Model:** "I understand React Context at 45%, struggling with providers"
- **Workspace Protocol:** "Here's actual Provider code from the project I'm learning"
- **Claude Synthesis:** "Your struggle maps to this pattern because..."

You create a **continuous, evidence-based, grounded** learning experience that addresses AI amnesia while maintaining practical workflow efficiency.

The protocol is:
- ✅ Based on standard Unix tools (no new software)
- ✅ Terminal-native (fits developer workflow)
- ✅ Evidence-based (no assumptions)
- ✅ Incremental (tight feedback loops)
- ✅ Single-purpose (complements, doesn't replace Student Model)

**Next:** See `complete_session_guide.md` for end-to-end workflow examples.
