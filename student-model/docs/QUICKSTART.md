# Quick Start Guide

## Installation (30 seconds)

```bash
# 1. Clone or navigate to project
cd student-model

# 2. Install test dependencies (optional)
pip install -r requirements.txt

# 3. Verify setup
./verify_setup.sh  # or: bash verify_setup.sh
```

## First Use (1 minute)

```bash
# Initialize your model
python student.py init --profile "Self-taught web developer"

# Check it worked
python student.py info

# Look at the file
cat ~/student_model.json
```

## Current Commands (Phase 1)

```bash
# Initialize new model
python student.py init [--profile "description"]

# Show model information
python student.py info

# Show help
python student.py --help
```

## Testing (30 seconds)

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=student

# Run specific tests
pytest tests/test_core_data.py -v
```

## Project Structure

```
student-model/
├── student.py              # Main CLI tool
├── README.md               # Full documentation
├── requirements.txt        # Dependencies
├── tests/                  # Test suite
│   ├── test_core_data.py   # Core tests
│   ├── test_cli.py         # CLI tests
│   └── test_model.py       # Structure tests
├── docs/                   # Documentation
│   ├── impl_plan.md        # 4-week roadmap
│   ├── complete_session_guide.md
│   ├── workspace_protocol.md
│   └── socratic_mentor_prompt.md
└── examples/
    └── sample_model.json   # Example data
```

## Data Location

- **Model:** `~/student_model.json`
- **Backup:** `~/student_model.json.backup` (auto-created on save)

## Quick Reference

### What Works Now (Phase 1 ✅)
- ✅ Initialize new model
- ✅ View model info
- ✅ Robust save/load with backups
- ✅ Automatic corruption recovery

### Coming Next (Phase 2)
- ⏳ `list` - List all concepts
- ⏳ `show "Concept"` - Show concept details
- ⏳ `related "Concept"` - Show related concepts

### Coming Soon (Phase 3)
- ⏳ `add "Concept" mastery confidence` - Add concept
- ⏳ `update "Concept" --mastery X` - Update concept
- ⏳ `struggle "Concept" "description"` - Log struggle
- ⏳ `breakthrough "Concept" "description"` - Log breakthrough

## Common Tasks

### View Your Model
```bash
cat ~/student_model.json | python -m json.tool
```

### Backup Your Model
```bash
cp ~/student_model.json ~/student_model_backup_$(date +%Y%m%d).json
```

### Reset Model
```bash
rm ~/student_model.json ~/student_model.json.backup
python student.py init
```

### Check Test Coverage
```bash
pytest --cov=student --cov-report=term-missing
```

## Troubleshooting

### "No model found"
```bash
# Initialize a new model
python student.py init
```

### "Corrupt JSON"
```bash
# Automatic restore from backup happens automatically
# Or manually restore:
cp ~/student_model.json.backup ~/student_model.json
```

### Tests fail with import errors
```bash
# Make sure you're in project root
cd /path/to/student-model
pytest
```

### Want to use different file location
```bash
# Edit student.py, change this line:
DATA_FILE = Path.home() / "student_model.json"
# To:
DATA_FILE = Path("/your/custom/path/model.json")
```

## Next Steps

1. **Read the docs:**
   - `README.md` - Project overview
   - `docs/complete_session_guide.md` - How to use with AI tutor
   - `docs/impl_plan.md` - What's being built

2. **Try it out:**
   - Initialize your model
   - Look at `examples/sample_model.json` for inspiration
   - Run tests to understand behavior

3. **Wait for Phase 2:**
   - Read operations coming next session
   - Then Phase 3 (write operations)
   - Then you can actually use it!

## Getting Help

- **Implementation plan:** `docs/impl_plan.md`
- **Testing guide:** `TESTING.md`
- **Phase 1 summary:** `PHASE1_COMPLETE.md`
- **Full README:** `README.md`

---

**Status:** Phase 1 Complete ✅ | Ready for Phase 2  
**Last Updated:** November 6, 2025
