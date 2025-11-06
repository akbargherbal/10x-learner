# Testing Guide

## Running Tests

### Quick Test Run

```bash
# Run all tests
pytest

# Run with output
pytest -v

# Run specific test file
pytest tests/test_core_data.py
```

### With Coverage

```bash
# Generate coverage report
pytest --cov=student --cov-report=term-missing

# Generate HTML coverage report
pytest --cov=student --cov-report=html
# Then open htmlcov/index.html
```

### Running Specific Tests

```bash
# Run specific test class
pytest tests/test_core_data.py::TestSaveLoad -v

# Run specific test function
pytest tests/test_core_data.py::TestSaveLoad::test_save_and_load_roundtrip -v

# Run tests matching pattern
pytest -k "save" -v
```

## Test Structure

### Phase 1 Tests (Current)

**`tests/test_core_data.py`** - Core data operations
- Model creation and validation
- Save/load with error handling
- Backup/restore functionality
- Atomic writes
- Concept finding

**`tests/test_cli.py`** - CLI integration
- Command parsing
- Help text
- Placeholder tests for future commands

**`tests/test_model.py`** - Model structure
- Placeholder tests for Phase 2-5 features

### Test Categories

**Unit Tests**: Test individual functions in isolation
- `TestDefaultModel`
- `TestValidation`
- `TestFindConcept`

**Integration Tests**: Test component interactions
- `TestSaveLoad`
- `TestLoadErrors`
- `TestAtomicWrites`

**CLI Tests**: Test end-to-end command behavior
- `TestCLIInit`
- `TestCLIInfo`

## Writing New Tests

### Pattern for Data Tests

```python
def test_something(self, temp_data_file, monkeypatch):
    """Test description."""
    monkeypatch.setattr('student.DATA_FILE', temp_data_file)
    
    # Test code here
    model = load_model()
    # assertions...
```

### Pattern for Error Tests

```python
def test_error_condition(self, temp_data_file, monkeypatch, capsys):
    """Test error handling."""
    monkeypatch.setattr('student.DATA_FILE', temp_data_file)
    
    # Create error condition
    with open(temp_data_file, 'w') as f:
        f.write("corrupt data")
    
    # Test recovery
    model = load_model()
    
    # Check output
    captured = capsys.readouterr()
    assert "error message" in captured.out.lower()
```

## Fixtures

### `temp_data_file`

Provides isolated temporary file for testing. Automatically cleans up.

```python
def test_something(self, temp_data_file, monkeypatch):
    monkeypatch.setattr('student.DATA_FILE', temp_data_file)
    # temp_data_file is a Path object to use for testing
```

### `capsys`

Captures stdout/stderr for testing output messages.

```python
def test_output(self, capsys):
    print("test message")
    captured = capsys.readouterr()
    assert "test message" in captured.out
```

### `monkeypatch`

Temporarily override module attributes (like DATA_FILE path).

```python
def test_with_custom_path(self, monkeypatch):
    monkeypatch.setattr('student.DATA_FILE', Path('/tmp/test.json'))
    # Now student.DATA_FILE points to test location
```

## Test Coverage Goals

### Phase 1 (Current)
- ✅ Core data operations: 100%
- ✅ Error handling: 100%
- ✅ Validation: 100%

### Phase 2 (Target)
- Read operations: 100%
- Output formatting: 90%+

### Phase 3 (Target)
- Write operations: 100%
- Data validation: 100%

### Overall Target
- Total coverage: 90%+
- Critical paths: 100%

## CI/CD Integration (Future)

When ready for CI/CD, add:

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest --cov=student --cov-report=xml
      - uses: codecov/codecov-action@v3
```

## Debugging Tests

### Run with print output

```bash
pytest -s  # Shows print() statements
```

### Run with PDB on failure

```bash
pytest --pdb  # Drops into debugger on failure
```

### Run with verbose tracebacks

```bash
pytest -vv  # Very verbose
pytest --tb=long  # Long traceback format
```

## Common Issues

### Import Errors

Make sure you're in the project root:
```bash
cd /path/to/student-model
pytest
```

### Fixture Not Found

Check that fixture is imported or defined in the test file or `conftest.py`.

### Tests Pass Locally But Fail in CI

Usually timing or path issues. Use fixtures to avoid hardcoded paths.

## Next Steps

As you implement Phase 2-3, add tests following these patterns:

1. Write test first (TDD)
2. Run test, watch it fail
3. Implement feature
4. Run test, watch it pass
5. Refactor if needed
6. Commit with test + implementation together

Happy testing! 🧪
