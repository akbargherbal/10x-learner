## Phase 1: Core Infrastructure (Week 1)

### 1.1 Project Setup

**Goal:** Foundation with proper structure and testing

```bash
# Project structure
student-model/
├── student.py           # Main CLI tool (conceptual knowledge only)
├── tests/
│   ├── test_cli.py
│   └── test_model.py
├── examples/
│   └── sample_model.json
├── docs/
│   ├── student_model_usage.md       # student.py command reference
│   ├── workspace_protocol.md        # Unix tools for code context
│   └── complete_session_guide.md    # Full integrated workflow
├── README.md
└── .gitignore
```

**Tasks:**

- [ ] Initialize git repo
- [ ] Create `student.py` skeleton with argparse structure
- [ ] Implement JSON schema validation
- [ ] Set up pytest with basic test coverage
- [ ] Create sample model for testing
- [ ] Create documentation structure

**Deliverable:** Working CLI that can initialize an empty model + doc scaffolding

**Time estimate:** 4-6 hours

### 1.2 Core Data Operations

**Goal:** Reliable model persistence (conceptual data only)

**Implement:**

- `load_model()` - with error handling for corrupt JSON
- `save_model()` - atomic writes with backup
- `initialize_model()` - create new student model
- `find_concept()` - case-insensitive search

**Critical details:**

```python
# Atomic save pattern
def save_model(model):
    model["metadata"]["last_updated"] = datetime.now().isoformat()

    # Backup existing
    if DATA_FILE.exists():
        backup = DATA_FILE.with_suffix('.json.backup')
        shutil.copy(DATA_FILE, backup)

    # Write to temp, then atomic rename
    temp = DATA_FILE.with_suffix('.json.tmp')
    with open(temp, 'w') as f:
        json.dump(model, f, indent=2)
    temp.replace(DATA_FILE)
```

**Tests:**

- Corrupt JSON recovery
- Concurrent access (if multi-process)
- Backup/restore functionality

**Deliverable:** Robust data layer with full test coverage

**Time estimate:** 3-4 hours

---