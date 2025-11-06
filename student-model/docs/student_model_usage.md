# Student Model CLI - Command Reference

Complete reference for all `student.py` commands (Phases 1-3).

---

## Phase 1: Core Commands

### `init`

Initialize a new student model file at `~/student_model.json`.

**Usage:**

```bash
python student.py init [--profile "Your profile description"]
```

**Arguments:**

- `--profile` (optional): A string to describe the student. Helpful for sharing your model with a tutor.

**Behavior:**

- If `~/student_model.json` already exists, prompts for confirmation before overwriting.
- Creates the base model structure with metadata.

**Example:**

```bash
python student.py init --profile "Computer Science student learning web development"
```

---

### `info`

Display metadata and high-level statistics about your student model.

**Usage:**

```bash
python student.py info
```

**Output:**

- Model file location
- Creation and last updated dates
- Student profile
- Total number of concepts and sessions
- Average mastery across all concepts

**Example Output:**

```
📊 Student Model Information
   Location:      /home/user/student_model.json
   Created:       2024-01-01
   Last Updated:  2024-01-15
   Profile:       Computer Science student

   Total Concepts: 12
   Total Sessions: 5
   Avg Mastery:    64.2%
```

---

## Phase 2: Read Operations

### `list`

List all tracked concepts with summary information, sorted by mastery level (descending).

**Usage:**

```bash
python student.py list
```

**Output Columns:**

- **Indicator**: Emoji representing mastery level
  - ✅ 80%+ (High mastery)
  - 🟡 60-79% (Good progress)
  - 🟠 40-59% (Developing)
  - 🔴 <40% (Needs work)
- **Name**: The concept name
- **Mastery**: Percentage (0-100)
- **Confidence**: low, medium, or high (with ⚠️ for low)
- **Last Reviewed**: Date of last update

**Example Output:**

```
📚 Tracked Concepts (3 total)

✅ JavaScript Closures                    85%  high         (last: 2024-01-10)
🟡 React Hooks                            65%  medium       (last: 2024-01-15)
🔴 Async/Await Patterns                   35%  ⚠️  low      (last: 2024-01-12)

Legend: ✅ 80%+  🟡 60-79%  🟠 40-59%  🔴 <40%
```

---

### `show`

Display detailed information for a single concept.

**Usage:**

```bash
python student.py show "Concept Name"
```

**Arguments:**

- `Concept Name`: Name of the concept (case-insensitive)

**Output:**

- Mastery and Confidence levels
- First Encountered and Last Reviewed dates
- List of logged **Struggles** (⚠️)
- List of logged **Breakthroughs** (💡)
- List of **Related Concepts** (🔗) with their mastery levels

**Example:**

```bash
python student.py show "React Hooks"
```

**Example Output:**

```
📊 Concept: React Hooks
   Mastery:          65%
   Confidence:       medium
   First Encountered: 2024-01-01
   Last Reviewed:     2024-01-15
   ⚠️  Struggles:
      - confused about dependency arrays
      - closure behavior in useEffect
   💡 Breakthroughs:
      - understood cleanup functions
      - realized hooks are just functions
   🔗 Related Concepts:
      - JavaScript Closures (Mastery: 85%, Last: 2024-01-10) ✓
      - React Core (Mastery: 45%, Last: 2024-01-05) ⚠️ LOW
```

---

### `related`

List all concepts related to a specific concept.

**Usage:**

```bash
python student.py related "Concept Name"
```

**Arguments:**

- `Concept Name`: Name of the concept (case-insensitive)

**Output:**

- List of related concepts with mastery, confidence, and last reviewed date
- ⚠️ LOW flag for concepts with mastery <60% (prerequisite gaps)

**Example:**

```bash
python student.py related "React Hooks"
```

**Example Output:**

```
🔗 Concepts related to 'React Hooks':
   - JavaScript Closures                 85%  high       (last: 2024-01-10) ✓
   - React Core                          45%  medium     (last: 2024-01-05) ⚠️ LOW
   - Event Loop                          (not tracked yet)
```

---

## Phase 3: Write Operations

### `add`

Add a new concept to your model.

**Usage:**

```bash
python student.py add "Concept Name" <mastery> <confidence> [--related "Concept1,Concept2"]
```

**Arguments:**

- `Concept Name`: Name of the new concept
- `mastery`: Integer 0-100 (initial mastery level)
- `confidence`: One of: `low`, `medium`, `high`
- `--related` (optional): Comma-separated list of related concepts

**Validation:**

- Mastery must be 0-100
- Confidence must be low, medium, or high
- Prevents duplicate concepts (case-insensitive check)

**Examples:**

```bash
# Basic usage
python student.py add "FastAPI" 30 low

# With related concepts
python student.py add "React Hooks" 40 medium --related "JavaScript Closures,React Core"
```

**Output:**

```
✅ Added concept: 'FastAPI'
   Mastery: 30%
   Confidence: low
```

---

### `update`

Update an existing concept's mastery and/or confidence.

**Usage:**

```bash
python student.py update "Concept Name" [--mastery N] [--confidence LEVEL]
```

**Arguments:**

- `Concept Name`: Name of the concept (case-insensitive)
- `--mastery` (optional): New mastery level (0-100)
- `--confidence` (optional): New confidence level (low, medium, high)

**Behavior:**

- At least one of `--mastery` or `--confidence` should be provided
- Updates the `last_reviewed` timestamp automatically
- Shows before/after values

**Examples:**

```bash
# Update mastery only
python student.py update "React Hooks" --mastery 70

# Update confidence only
python student.py update "React Hooks" --confidence high

# Update both
python student.py update "React Hooks" --mastery 85 --confidence high
```

**Output:**

```
✅ Updated 'React Hooks':
   mastery 65% → 85%
   confidence medium → high
```

---

### `struggle`

Log a difficulty or confusion with a concept.

**Usage:**

```bash
python student.py struggle "Concept Name" "description of struggle"
```

**Arguments:**

- `Concept Name`: Name of the concept (case-insensitive)
- `description`: Text describing the struggle

**Behavior:**

- Appends to the concept's struggles list
- Prevents duplicate entries
- Updates `last_reviewed` timestamp
- Concept must exist (use `add` first if needed)

**Examples:**

```bash
python student.py struggle "React Hooks" "confused about dependency arrays"
python student.py struggle "Async/Await" "don't understand when to use .catch()"
```

**Output:**

```
✅ Logged struggle for 'React Hooks'
   "confused about dependency arrays"
```

---

### `breakthrough`

Log an insight or breakthrough with a concept.

**Usage:**

```bash
python student.py breakthrough "Concept Name" "description of insight"
```

**Arguments:**

- `Concept Name`: Name of the concept (case-insensitive)
- `description`: Text describing the breakthrough

**Behavior:**

- Appends to the concept's breakthroughs list
- Prevents duplicate entries
- Updates `last_reviewed` timestamp
- Concept must exist (use `add` first if needed)

**Examples:**

```bash
python student.py breakthrough "React Hooks" "realized hooks are just functions"
python student.py breakthrough "JavaScript Closures" "understood lexical scope connection"
```

**Output:**

```
✅ Logged breakthrough for 'React Hooks'
   💡 "realized hooks are just functions"
```

---

### `link`

Create a relationship between two concepts (e.g., prerequisites).

**Usage:**

```bash
python student.py link "Concept Name" "Related Concept"
```

**Arguments:**

- `Concept Name`: Main concept (must exist)
- `Related Concept`: Related/prerequisite concept (can be untracked)

**Behavior:**

- Creates a one-way link (Concept → Related)
- Prevents duplicate links (case-insensitive)
- Warns if related concept doesn't exist yet
- The link is still created even if the related concept isn't tracked

**Examples:**

```bash
python student.py link "React Hooks" "JavaScript Closures"
python student.py link "FastAPI" "Python Type Hints"
```

**Output:**

```
✅ Linked 'React Hooks' → 'JavaScript Closures'
```

**If related concept doesn't exist:**

```
⚠️  'Python Type Hints' not tracked yet.
   Link will be created, but you should add it:
   python student.py add "Python Type Hints" 0 low
✅ Linked 'FastAPI' → 'Python Type Hints'
```

---

### `unlink`

Remove a relationship between two concepts.

**Usage:**

```bash
python student.py unlink "Concept Name" "Related Concept"
```

**Arguments:**

- `Concept Name`: Main concept (must exist)
- `Related Concept`: Related concept to unlink (case-insensitive)

**Examples:**

```bash
python student.py unlink "React Hooks" "JavaScript Closures"
```

**Output:**

```
✅ Unlinked 'React Hooks' ✗ 'JavaScript Closures'
```

---

## Common Workflows

### Starting a New Learning Topic

```bash
# 1. Add the concept
python student.py add "FastAPI Basics" 20 low

# 2. Link prerequisites
python student.py link "FastAPI Basics" "Python Type Hints"
python student.py link "FastAPI Basics" "Async/Await"

# 3. Verify setup
python student.py show "FastAPI Basics"
```

### During a Learning Session

```bash
# 1. Check current status
python student.py show "FastAPI Basics"

# 2. Log struggles as you encounter them
python student.py struggle "FastAPI Basics" "confused about dependency injection"

# 3. Log breakthroughs
python student.py breakthrough "FastAPI Basics" "understood how Depends() works"
```

### End of Session Update

```bash
# Update progress
python student.py update "FastAPI Basics" --mastery 60 --confidence medium
```

### Reviewing Progress

```bash
# See all concepts
python student.py list

# Check specific concept
python student.py show "FastAPI Basics"

# Check prerequisites
python student.py related "FastAPI Basics"
```

---

## Tips and Best Practices

### Concept Naming

- Use clear, specific names: "React Context API" not "Context"
- Be consistent with casing: "JavaScript Closures" not "javascript closures"
- Use the same name format across related concepts

### Mastery Scale Guidelines

- **0-20%**: Just heard of it, no practical understanding
- **20-40%**: Can follow tutorials, need guidance
- **40-60%**: Can use with reference, some independence
- **60-80%**: Comfortable using, can solve problems
- **80-100%**: Deep understanding, can teach others

### Confidence Levels

- **low**: Uncertain, need to verify everything
- **medium**: Generally comfortable, occasional doubts
- **high**: Very confident, rare mistakes

### Struggles vs Breakthroughs

- **Struggles**: Specific confusions or roadblocks
  - Good: "confused about when useEffect cleanup runs"
  - Too vague: "useEffect is hard"
- **Breakthroughs**: Specific insights or "aha!" moments
  - Good: "realized cleanup runs before next effect"
  - Too vague: "understood useEffect better"

### Related Concepts

- Link prerequisites (concepts needed to understand this one)
- Link related topics (concepts in the same domain)
- Review `python student.py related <concept>` to spot prerequisite gaps

---

## Troubleshooting

### "Concept not found"

- Check spelling: `python student.py list` to see all concepts
- Search is case-insensitive, but must match exactly otherwise

### "Model structure is invalid"

- Backup file may be corrupt
- Use `python student.py init` to create a fresh model
- Old model will be backed up to `~/student_model.json.backup`

### Changes not saving

- Check disk space
- Verify write permissions on `~/student_model.json`
- Look for error messages in output

### Need to start over

```bash
# Backup your current model
cp ~/student_model.json ~/student_model.json.archive

# Create fresh model
python student.py init
```

---

## File Location

Default: `~/student_model.json`

To use a different location, modify the `DATA_FILE` constant in `student.py` or set it via environment variable (future feature).
