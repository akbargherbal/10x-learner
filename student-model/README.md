# Student Model Project

A CLI tool for tracking conceptual knowledge mastery across learning sessions, designed to give AI tutors persistent memory of your learning journey.

## Status: Phase 3 Complete ✅

**Current Implementation:**
- ✅ Core data operations (load, save, initialize)
- ✅ Atomic writes with backup & corruption recovery
- ✅ Case-insensitive concept search
- ✅ **Read Operations** (`list`, `show`, `related`)
- ✅ **Write Operations** (`add`, `update`, `struggle`, `breakthrough`, `link`, `unlink`)
- ✅ Comprehensive test suite (66 passing tests, 73% coverage)
- ✅ Full CRUD functionality

**Next Steps:** Phase 4 - Documentation & Protocol Design

## Quick Start

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd student-model

# Install dependencies (for testing)
pip install -r requirements.txt
```

### Initialize Your Model

```bash
python student.py init --profile "Your learning profile description"
```

This creates `~/student_model.json` with the base structure.

### Basic Usage

```bash
# Add a new concept
python student.py add "React Hooks" 45 medium

# View all concepts
python student.py list

# See detailed info
python student.py show "React Hooks"

# Update progress
python student.py update "React Hooks" --mastery 60 --confidence high

# Log learning insights
python student.py struggle "React Hooks" "confused about dependency arrays"
python student.py breakthrough "React Hooks" "understood closure connection"

# Link related concepts
python student.py link "React Hooks" "JavaScript Closures"
```

## Project Philosophy

This project implements a **persistent Student Model** system that:

1. **Tracks conceptual knowledge** (not specific files or code)
2. **Maintains continuity** across learning sessions
3. **Complements workspace investigation** (using standard Unix tools)
4. **Enables AI tutors** to provide adaptive, personalized teaching

See `docs/impl_plan.md` for full architectural vision.

## Current Features (Phases 1-3)

### Robust Data Persistence

- **Atomic writes**: No data corruption from interrupted saves
- **Automatic backups**: Previous version always preserved
- **Corruption recovery**: Falls back to backup if JSON is corrupt
- **Validation**: Ensures model structure before saving

### Read Operations

```bash
# Show model information
python student.py info

# List all concepts
python student.py list

# Show concept details
python student.py show "Concept Name"

# Show related concepts
python student.py related "Concept Name"
```

### Write Operations

```bash
# Add new concept
python student.py add "Concept Name" <mastery> <confidence>
# Example: python student.py add "FastAPI" 30 low

# Update existing concept
python student.py update "Concept Name" [--mastery N] [--confidence LEVEL]

# Log a struggle
python student.py struggle "Concept Name" "description of difficulty"

# Log a breakthrough
python student.py breakthrough "Concept Name" "description of insight"

# Link concepts (prerequisites/related)
python student.py link "Concept Name" "Related Concept"

# Unlink concepts
python student.py unlink "Concept Name" "Related Concept"
```

## Data Structure

Your model is stored as JSON in `~/student_model.json`. Each concept tracks:

- **Mastery**: 0-100% understanding
- **Confidence**: low, medium, or high
- **Struggles**: List of difficulties encountered
- **Breakthroughs**: List of insights gained
- **Related Concepts**: Prerequisite relationships
- **Timestamps**: First encountered, last reviewed

See `examples/sample_model.json` for a complete example.

## Testing

Run the comprehensive test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=student --cov-report=html

# Run with verbose output
pytest -v
```

**Current Test Coverage:** 73% (66 passing tests, 4 skipped)

## Development Roadmap

- [x] **Phase 1.1:** Project Setup
- [x] **Phase 1.2:** Core Data Operations
- [x] **Phase 2:** Read Operations - `list`, `show`, `related`
- [x] **Phase 3:** Write Operations - `add`, `update`, `struggle`, `breakthrough`, `link`, `unlink`
- [ ] **Phase 4:** Documentation & Protocol Design
- [ ] **Phase 5:** Enhanced Features - Prerequisites, Misconceptions
- [ ] **Phase 6:** Quality of Life - Interactive mode, Export
- [ ] **Phase 7:** Testing & Refinement
- [ ] **Phase 8:** Documentation & Release

See `docs/impl_plan.md` for detailed breakdown.

## Design Principles

1. **Single Purpose**: Only track conceptual knowledge
2. **Simple Data**: Plain JSON, human-readable
3. **Robust**: Atomic writes, backups, validation
4. **Terminal-Native**: CLI-first, scriptable
5. **Test-Driven**: All features tested before release

## Documentation

- `docs/student_model_usage.md` - Complete command reference
- `docs/impl_plan.md` - Full implementation plan
- `docs/workspace_protocol.md` - Code investigation workflow
- `docs/complete_session_guide.md` - Integrated session examples
- `docs/PHASE3_QUICK_START.md` - Quick integration guide

## Contributing

This is a personal learning project, but suggestions and feedback are welcome!

## License

[Your chosen license]