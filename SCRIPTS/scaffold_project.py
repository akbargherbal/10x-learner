import os

# Define project structure
structure = {
    "student-model": {
        "student.py": "# student.py — Main CLI tool (conceptual knowledge only)\n\n"
                      "def main():\n"
                      "    print('Student model CLI placeholder')\n\n"
                      "if __name__ == '__main__':\n"
                      "    main()\n",
        "tests": {
            "test_cli.py": "# test_cli.py — Placeholder for CLI tests\n\n"
                           "def test_cli_placeholder():\n"
                           "    assert True\n",
            "test_model.py": "# test_model.py — Placeholder for model tests\n\n"
                             "def test_model_placeholder():\n"
                             "    assert True\n"
        },
        "examples": {
            "sample_model.json": '{\n  "name": "sample student model",\n  "version": "0.1"\n}\n'
        },
        "docs": {
            "student_model_usage.md": "# student_model_usage.md\n\n"
                                      "Documentation for using student.py CLI tool.\n",
            "workspace_protocol.md": "# workspace_protocol.md\n\n"
                                     "Notes on Unix tools for code context.\n",
            "complete_session_guide.md": "# complete_session_guide.md\n\n"
                                         "Full integrated workflow guide.\n"
        },
        "README.md": "# Student Model Project\n\n"
                     "This project defines a conceptual CLI tool and model structure.\n",
        ".gitignore": "# Ignore Python cache files\n__pycache__/\n*.pyc\n.env\n"
    }
}


def create_structure(base_path, structure_dict):
    """Recursively create folders and files for the given structure."""
    for name, content in structure_dict.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            # Folder
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            # File
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Created file: {path}")


if __name__ == "__main__":
    base_dir = os.getcwd()  # Create in current directory
    create_structure(base_dir, structure)
    print("\n✅ Project scaffold created successfully.")
