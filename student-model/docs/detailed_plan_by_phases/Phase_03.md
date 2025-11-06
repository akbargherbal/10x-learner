## Phase 3: Write Operations (Week 1-2)

### 3.1 Basic Modification Commands

**Implement:**

```bash
python student.py add "Concept" 50 medium
python student.py update "Concept" --mastery 70 --confidence high
python student.py struggle "Concept" "description"
python student.py breakthrough "Concept" "description"
```

**Validation rules:**

- Mastery: 0-100 integer
- Confidence: low|medium|high enum
- Prevent duplicate concepts (suggest update instead)
- Prevent duplicate struggles/breakthroughs

**Implementation pattern:**

```python
def cmd_add(args):
    model = load_model()

    # Check for existing
    if find_concept(model, args.concept_name):
        print(f"❌ Concept '{args.concept_name}' already exists. Use 'update'.")
        return

    # Add new concept
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
```

**Deliverable:** Full CRUD operations on concepts

**Time estimate:** 4-5 hours

### 3.2 Batch Operations (Overhead Reduction)

**Goal:** Minimize session-end friction

**Implement session-end helper:**

```bash
python student.py session-end \
  --update "React Hooks:70:medium" \
  --struggle "React Hooks:dependency confusion" \
  --breakthrough "React Hooks:understood cleanup"
```

This runs multiple operations atomically in one command.

**Alternative approach (if preferred):**
Shell script that takes structured input:

```bash
# session_update.sh
python student.py update "$1" --mastery "$2" --confidence "$3"
python student.py struggle "$1" "$4"
python student.py breakthrough "$1" "$5"
```

**Deliverable:** Session updates take <2 minutes

**Time estimate:** 2-3 hours

---