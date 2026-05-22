from pathlib import Path


def test_project_structure_exists():
    expected_paths = [
        "src",
        "tests",
        "data/input",
        "data/output",
        "reports",
        "Makefile",
        "requirements.txt",
        "pytest.ini",
    ]

    for path in expected_paths:
        assert Path(path).exists(), f"missing required path: {path}"
