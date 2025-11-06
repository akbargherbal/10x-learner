## Phase 5: Enhanced Features (Week 3)

### 5.1 Related Concepts (Prerequisite Graph)

**Implement:**

```bash
python student.py link "React Hooks" "JavaScript Closures"
python student.py unlink "React Hooks" "JavaScript Closures"
python student.py related "React Hooks"
```

**Data structure:**

```python
"concepts": {
  "React Hooks": {
    ...
    "related_concepts": ["JavaScript Closures", "React Core"]
  }
}
```

**Smart related command output:**

```
🔗 Concepts related to 'React Hooks':
   - JavaScript Closures (Mastery: 55%, Last: 2026-04-15) ⚠️ LOW
   - React Core (Mastery: 80%, Last: 2026-04-10) ✅
```

Flag low-mastery prerequisites for LLM attention.

**Deliverable:** Prerequisite tracking functional

**Time estimate:** 3-4 hours

### 5.2 Misconception Tracking

**Implement:**

```bash
python student.py misconception add "React Hooks" \
  --belief "useEffect cleanup runs every render" \
  --correction "runs before next effect or unmount"

python student.py misconception resolve "React Hooks" 0
python student.py misconception list
```

**Deliverable:** Explicit bug model tracking

**Time estimate:** 2-3 hours

---