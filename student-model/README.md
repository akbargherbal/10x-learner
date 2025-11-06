# Student Model Project

A CLI tool for tracking conceptual knowledge mastery across learning sessions, designed to give AI tutors persistent memory of your learning journey.

## Status: Phase 1 Complete ✅

**Current Implementation:**
- ✅ Core data operations (load, save, initialize)
- ✅ Atomic writes with backup
- ✅ JSON corruption recovery
- ✅ Case-insensitive concept search
- ✅ Comprehensive test suite
- ✅ Full documentation

**Next Steps:** Phase 2 - Read Operations (`list`, `show`, `related` commands)

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

### Check Model Info

```bash
python student.py info
```

Shows metadata, concept count, and statistics.

## Project Philosophy

This project implements a **persistent Student Model** system that:

1. **Tracks conceptual knowledge** (not specific files or code)
2. **Maintains continuity** across learning sessions
3. **Complements workspace investigation** (using standard Unix tools)
4. **Enables AI tutors** to provide adaptive, personalized teaching

See `docs/impl_plan.md` for full architectural vision.

## Current Features (Phase 1)

### Robust Data Persistence

- **Atomic writes**: No data corruption from interrupted saves
- **Automatic backups**: Previous version always preserved
- **Corruption recovery**: Falls back to backup if JSON is corrupt
- **Validation**: Ensures model structure before saving

### Commands

```bash
# Initialize new model
python student.py init [--profile "description"]

# Show model information
python student.py info
```

## Data Structure

Your model is stored as JSON in `~/student_model.json`:

```json
{
  "schema_version": "1.0",
  "metadata": {
    "created": "2025-11-06T10:00:00",
    "last_updated": "2025-11-06T14:30:00",
    "student_profile": "Your profile"
  },
  "concepts": {},
  "sessions": []
}
```

See `examples/sample_model.json` for a complete example with concepts.

## Testing

Run the comprehensive test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=student --cov-report=html

# Run specific test file
pytest tests/test_core_data.py -v
```

**Current test coverage:** Core data operations (Phase 1.2) fully tested.

## Documentation

- **`docs/impl_plan.md`** - Complete implementation roadmap (Phase 1-8)
- **`docs/complete_session_guide.md`** - End-to-end session workflow
- **`docs/workspace_protocol.md`** - Using Unix tools for code context
- **`docs/socratic_mentor_prompt.md`** - LLM persona for tutoring
- **`docs/student_model_usage.md`** - Command reference (coming in Phase 2)

## Architecture

### Separation of Concerns

| Component | Purpose | Storage |
|-----------|---------|---------|
| **Student Model** (this tool) | Abstract conceptual knowledge | `student_model.json` |
| **Workspace Protocol** | Concrete code context | Terminal (ephemeral) |
| **AI Tutor (Claude)** | Synthesis & Socratic teaching | LLM reasoning |

The Student Model tracks **what you understand** (mastery levels, struggles, breakthroughs).

The Workspace Protocol shows **what you're looking at** (actual code via `cat`, `grep`, etc.).

The AI Tutor **bridges both** to provide grounded, continuous learning.

## Development Roadmap

- [x] **Phase 1.1:** Project Setup (Week 1)
- [x] **Phase 1.2:** Core Data Operations (Week 1)
- [ ] **Phase 2:** Read Operations - `list`, `show`, `related` (Week 1)
- [ ] **Phase 3:** Write Operations - `add`, `update`, `struggle`, `breakthrough` (Week 1-2)
- [ ] **Phase 4:** Documentation & Protocol Design (Week 2)
- [ ] **Phase 5:** Enhanced Features - Prerequisites, Misconceptions (Week 3)
- [ ] **Phase 6:** Quality of Life - Interactive mode, Export (Week 3-4)
- [ ] **Phase 7:** Testing & Refinement (Week 4)
- [ ] **Phase 8:** Documentation & Release (Week 4)

See `docs/impl_plan.md` for detailed breakdown.

## Contributing

This is currently a personal learning project. If you'd like to adapt it:

1. Fork the repository
2. Review the implementation plan
3. Check existing tests for patterns
4. Submit PRs with test coverage

## Design Principles

1. **Single Purpose**: Only track conceptual knowledge (no code storage)
2. **Simple Data**: Plain JSON, human-readable
3. **Robust**: Atomic writes, backups, validation
4. **Terminal-Native**: CLI-first, scriptable
5. **Test-Driven**: All features tested before release

## FAQ

**Q: Where is my data stored?**  
A: `~/student_model.json` by default. Backups in `~/student_model.json.backup`.

**Q: Is this like Anki for programming?**  
A: Similar goal (spaced learning) but different approach. This tracks understanding depth, not flashcard-style recall.

**Q: Can I use this without an AI tutor?**  
A: Yes, but it's designed to complement AI tutoring. Manual usage is supported but less ergonomic.

**Q: What if I have multiple learning projects?**  
A: The Student Model tracks concepts across all projects. Use the Workspace Protocol to provide project-specific code context.

**Q: Can I export my learning progress?**  
A: Export/reporting features coming in Phase 6.

## License

[Choose your license - MIT suggested for open source]

## Contact

[Your contact information]

---

**Last Updated:** November 2025 (Phase 1 Complete)