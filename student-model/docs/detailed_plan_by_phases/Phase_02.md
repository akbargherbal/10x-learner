## Phase 2: Read Operations (Week 1)

### 2.1 Viewing Commands

**Goal:** Rich, informative output for context gathering

**Implement commands:**

```bash
python student.py list
python student.py show "Concept Name"
python student.py related "Concept Name"
```

**Output design considerations:**

- Use emoji for visual parsing (📊, ⚠️, 💡, 🔗)
- Format for easy copy-paste into LLM conversations
- Handle missing data gracefully
- Color coding (optional: use `colorama` if you want it)

**Example implementation:**

```python
def cmd_show(args):
    model = load_model()
    concept_key = find_concept(model, args.concept_name)

    if not concept_key:
        print(f"❌ Concept '{args.concept_name}' not found.")
        return

    concept = model["concepts"][concept_key]
    print(f"📊 Concept: {concept_key}")
    print(f"   Mastery:       {concept.get('mastery', 'N/A')}%")
    print(f"   Confidence:    {concept.get('confidence', 'N/A')}")
    print(f"   Last Reviewed: {concept.get('last_reviewed', 'Never').split('T')[0]}")

    if concept.get('struggles'):
        print(f"   ⚠️  Struggles:")
        for struggle in concept['struggles']:
            print(f"      - {struggle}")

    if concept.get('breakthroughs'):
        print(f"   💡 Breakthroughs:")
        for breakthrough in concept['breakthroughs']:
            print(f"      - {breakthrough}")
```

**Deliverable:** All read operations functional with rich output

**Time estimate:** 2-3 hours

---