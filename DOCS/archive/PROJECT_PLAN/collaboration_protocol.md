## Collaboration Protocol: Code Archaeology Sessions

**Adapted from SpeedTyper-Solo** | **Optimized for Investigation-Heavy Workflow**

---

### Core Principle

**Minimum Friction, Maximum Clarity**

The learner and tutor (Claude) work in the same terminal environment. Claude requests specific files/outputs, learner provides them. No assumptions, no guessing—everything is evidence-based.

---

### File System Context

**Learner's Working Directory:**

```bash
~/learning-projects/
```

**Current Project Structure (will evolve):**

```
~/learning-projects/
├── student-model-sessions/           # Session docs and Student Model DB
│   ├── student_model.db
│   ├── SESSION_XX_SUMMARY.md
│   └── *.py (query/population scripts)
│
└── codebase-under-investigation/     # Changes per confusion point
    └── (e.g., monkeytype/, react/, nextjs-example/)
```

---

### Command Patterns

#### 1. When Claude Needs to See a File

**Pattern:**

```bash
cat ~/learning-projects/codebase-under-investigation/path/to/file
```

**Example:**

```bash
cat ~/learning-projects/monkeytype/packages/backend/package.json
```

**Learner:** Copy-paste the full output back to Claude.

---

#### 2. When Claude Needs Specific Lines or Context

**Pattern:**

```bash
cat path/to/file | grep -A 10 -B 5 "searchTerm"
```

**Example:**

```bash
cat ~/learning-projects/monkeytype/turbo.json | grep -A 5 "pipeline"
```

**Flags:**

- `-A N`: Show N lines After match
- `-B N`: Show N lines Before match
- `-C N`: Show N lines of Context (before and after)

---

#### 3. When Claude Needs to Search Across Files

**Pattern:**

```bash
grep -r "searchTerm" --include="*.extension" path/to/directory/
```

**Examples:**

```bash
# Find all TypeScript imports of a module
grep -r "from '@monkeytype/contracts'" --include="*.ts" ~/learning-projects/monkeytype/packages/

# Find all React hooks usage
grep -r "useState\|useEffect" --include="*.tsx" ~/learning-projects/react-example/
```

---

#### 4. When Claude Needs to Find Files

**Pattern:**

```bash
find path/to/directory -name "filename"
find path/to/directory -type f -name "*.extension"
```

**Examples:**

```bash
# Find all package.json files
find ~/learning-projects/monkeytype -name "package.json"

# Find all TypeScript config files
find ~/learning-projects/monkeytype -name "tsconfig*.json"
```

---

#### 5. When Claude Needs Directory Structure

**Pattern:**

```bash
ls -la path/to/directory
tree -L 2 path/to/directory  # If tree is installed
```

**Example:**

```bash
ls -la ~/learning-projects/monkeytype/packages/
```

---

#### 6. When Claude Needs Git History (for Context)

**Pattern:**

```bash
cd path/to/repo
git log --oneline -10 path/to/file
git show commit-hash:path/to/file
```

**Example:**

```bash
cd ~/learning-projects/monkeytype
git log --oneline -10 packages/backend/package.json
```

---

#### 7. When Checking Build/Run Outputs

**Pattern:**

```bash
cd path/to/project
npm run command 2>&1 | head -20  # Show first 20 lines of output
```

**Example:**

```bash
cd ~/learning-projects/monkeytype
npm run build 2>&1 | head -30
```

---

#### 8. When Querying Student Model

**Pattern:**

```bash
cd ~/learning-projects/student-model-sessions
python query_student_model.py
python query_student_model.py [concept_name]  # Once implemented
```

**Example:**

```bash
python query_student_model.py > session_04_context.txt
cat session_04_context.txt
```

---

#### 9. When Editing Files (Rare in Investigation Mode)

**Pattern:**
Claude provides full code block → Learner copy-pastes into editor.

**Example:**

```bash
code ~/learning-projects/student-model-sessions/SESSION_04_SUMMARY.md
```

Claude says:

```
Here's the content for SESSION_04_SUMMARY.md:

[Full markdown block]

Copy-paste this into the file.
```

---

### Key Protocol Rules

#### 1. ✅ Always Use Full Absolute Paths

```
✅ cat ~/learning-projects/monkeytype/package.json
❌ cat package.json
❌ cat ./package.json
```

#### 2. ✅ Claude Requests, Learner Provides

```
Claude: "Can you run: cat ~/learning-projects/monkeytype/README.md"
Learner: [pastes output]
Claude: [analyzes output and asks next question]
```

**Never:**

- Learner uploads entire codebases proactively
- Claude assumes file contents
- Claude invents outputs

#### 3. ✅ Tight Feedback Loop

```
Request → Output → Analysis → Next Request
```

Keep cycles short. Don't request 10 files at once—request, analyze, then decide what's needed next.

#### 4. ✅ Full Code Blocks, Not Diffs

When Claude provides code to edit:

```
✅ Provide full file content
❌ Provide diffs or partial snippets
```

Learner should be able to copy-paste directly.

#### 5. ✅ Terminal-First Workflow

Prefer terminal commands over GUI actions:

```
✅ grep -r "search" path/
❌ "Open VS Code search and type..."
```

Faster, reproducible, and saves tokens.

---

### Investigation Workflow Pattern

#### Typical Session Flow:

**1. Session Start**

```bash
# Load Student Model context
cd ~/learning-projects/student-model-sessions
python query_student_model.py > context.txt
cat context.txt
```

**2. Identify Confusion Point**

```
Learner: "I want to understand how monkeytype's build system works"
Claude: "What's your current hypothesis?"
Learner: "I think each package builds independently"
```

**3. Gather Evidence**

```bash
# Claude requests root-level build config
cat ~/learning-projects/monkeytype/turbo.json

[Learner pastes output]

# Claude analyzes, asks follow-up
Claude: "I see a pipeline definition. Can you show me a specific package's build script?"

cat ~/learning-projects/monkeytype/packages/backend/package.json
```

**4. Systematic Investigation**

```bash
# Claude requests related files based on findings
cat ~/learning-projects/monkeytype/packages/backend/package.json | grep "build"

# Or search across packages
grep -r "turbo run" --include="package.json" ~/learning-projects/monkeytype/
```

**5. Hypothesis Revision**

```
Claude: "Based on what we've seen, does your hypothesis still hold?"
Learner: "No, I see now that Turborepo orchestrates them"
Claude: "Right. What evidence confirms that?"
```

**6. Session Documentation** (when learner requests)

```bash
code ~/learning-projects/student-model-sessions/SESSION_04_SUMMARY.md

[Claude provides full template with findings]
```

---

### Special Cases

#### When Investigating Large Files

```bash
# Don't dump entire file
❌ cat huge-file.ts

# Use grep or head/tail
✅ cat huge-file.ts | grep -A 5 "function buildPipeline"
✅ head -50 huge-file.ts
✅ tail -30 huge-file.ts
```

#### When File Doesn't Exist

```bash
Learner: "cat: no such file or directory"

Claude: "Ah, the file might be elsewhere. Can you run:
find ~/learning-projects/monkeytype -name 'turbo.json'"
```

#### When Output Is Too Long

```bash
# Use head to limit output
npm run build 2>&1 | head -50

# Or save to file and examine
npm run build 2>&1 > build-output.txt
cat build-output.txt | grep "ERROR"
```

#### When Debugging Encoding Issues

```bash
# Show character codes
head -1 file.js | od -c

# Check file encoding
file file.js

# Show hex dump
hexdump -C file.js | head -3
```

---

### Communication Guidelines

#### Claude's File Requests Should Be:

- ✅ **Specific:** Exact paths, not "look at the backend package"
- ✅ **Justified:** "Let's check X to test your hypothesis"
- ✅ **Incremental:** One file at a time, analyze, then next

#### Learner's Responses Should Be:

- ✅ **Complete:** Full output, not summarized
- ✅ **Verbatim:** Copy-paste exactly, don't paraphrase
- ✅ **Timely:** If command fails, show error immediately

---

### What This Protocol Prevents

❌ **Wasted Tokens:** Uploading entire codebases when only 3 files matter  
❌ **Assumptions:** Claude guessing file contents  
❌ **Friction:** Switching between tools (terminal → GUI → terminal)  
❌ **Confusion:** Ambiguous references like "the backend file"  
❌ **Stale Context:** Claude working from outdated mental model of files

---

### Adaptation Notes

**For Different Codebases:**

- Adjust paths: `~/learning-projects/{codebase-name}/`
- Adjust file extensions: `--include="*.py"`, `--include="*.ts"`, etc.
- Adjust build commands: `npm run`, `cargo build`, `python -m`, etc.

**For Different Learning Domains:**

- Git workflows: Use `git log`, `git show`, `git diff`
- Database patterns: Use `sqlite3`, `.schema`, SQL queries
- Python projects: Use `cat requirements.txt`, `python -m module`, etc.

**The core pattern stays the same:**
Claude requests evidence → Learner provides → Claude analyzes → Repeat
