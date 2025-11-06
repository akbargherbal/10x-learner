#!/bin/bash
# verify_setup.sh - Verify Phase 1 setup is complete

echo "🔍 Verifying Student Model Phase 1 Setup..."
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1)
if [[ $? -eq 0 ]]; then
    echo "✅ $python_version"
else
    echo "❌ Python 3 not found"
    exit 1
fi
echo ""

# Check project structure
echo "Checking project structure..."
required_files=(
    "student.py"
    "README.md"
    ".gitignore"
    "requirements.txt"
    "tests/test_core_data.py"
    "tests/test_cli.py"
    "tests/test_model.py"
    "docs/impl_plan.md"
    "docs/complete_session_guide.md"
    "docs/workspace_protocol.md"
    "docs/socratic_mentor_prompt.md"
    "examples/sample_model.json"
)

all_present=true
for file in "${required_files[@]}"; do
    if [[ -f "$file" ]]; then
        echo "✅ $file"
    else
        echo "❌ $file (missing)"
        all_present=false
    fi
done
echo ""

if [[ "$all_present" = false ]]; then
    echo "❌ Some required files are missing"
    exit 1
fi

# Check if pytest is installed
echo "Checking test dependencies..."
if python3 -c "import pytest" 2>/dev/null; then
    echo "✅ pytest installed"
else
    echo "⚠️  pytest not installed. Run: pip install -r requirements.txt"
fi
echo ""

# Check if student.py is executable
echo "Checking student.py..."
if python3 student.py --help > /dev/null 2>&1; then
    echo "✅ student.py runs successfully"
else
    echo "❌ student.py has errors"
    exit 1
fi
echo ""

# Run a quick test
echo "Running quick functionality test..."
if python3 -c "from student import get_default_model, validate_model; m = get_default_model(); assert validate_model(m)" 2>/dev/null; then
    echo "✅ Core functions work"
else
    echo "❌ Core functions have errors"
    exit 1
fi
echo ""

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Phase 1 Setup Complete!"
echo ""
echo "Next steps:"
echo "  1. Install test dependencies: pip install -r requirements.txt"
echo "  2. Run tests: pytest -v"
echo "  3. Initialize your model: python student.py init"
echo "  4. Check model info: python student.py info"
echo ""
echo "Ready to proceed to Phase 2!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
