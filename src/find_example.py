"""
Unlearning Shell Scripting.  Chapter 4. The find_iter function.
"""

from pathlib import Path
from fnmatch import fnmatch
from typing import Iterable


def find_iter(base: Path, pattern: str) -> Iterable[Path]:
    for path, directories, files in base.walk():
        to_skip = [
            dir
            for dir in directories
            if dir.startswith(".") or dir.startswith("_")
        ]
        for name in to_skip:
            directories.remove(name)
        for name in files:
            if name.startswith("."):
                continue
            if fnmatch(name, pattern):
                if (full_path := path / name).is_file():
                    yield full_path


def main():
    project = Path.cwd()
    for path in find_iter(project, "*.py"):
        print(path.relative_to(project))


def test_find_example(capsys):
    main()
    out, err = capsys.readouterr()
    assert out.splitlines() == [
        "demo/the_service.py",
        "tests/test_find_example.py",
        "tests/test_awk.py",
        "src/summary_example.py",
        "src/awk.py",
        "src/find_classes.py",
        "src/find_classes_cli.py",
        "src/all_tests.py",
        "src/find_example.py",
        "src/cleanup_example.py",
    ]


if __name__ == "__main__":
    main()
