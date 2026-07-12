"""
Unlearning Shell Scripting. Chapter 5. Class definitions to find and process some files, skipping `.` and `_` directories.
"""

import abc
from dataclasses import dataclass
import logging
from pathlib import Path
import subprocess
import time


@dataclass
class Result:
    path: Path
    returncode: int
    duration: float
    output: list[str]


class FindAndProcess(abc.ABC):
    def __init__(self, base: Path, pattern: str) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.base = base
        self.pattern = pattern
        self.history: list[Result] = []

    def process_all(self) -> None:
        print()
        print(self.__class__.__name__)
        for path, directories, files in self.base.walk():
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
                if (full_path := path / name).match(self.pattern):
                    self.logger.debug(
                        "Process %r",
                        full_path,
                    )

                    start = time.perf_counter()
                    returncode, text = self.process_file(full_path)
                    end = time.perf_counter()

                    self.history.append(
                        Result(
                            full_path,
                            returncode,
                            end - start,
                            text.splitlines(),
                        )
                    )
                else:
                    self.logger.debug(
                        "No match for %r with %r",
                        full_path,
                        self.pattern,
                    )
        self.report()

    @abc.abstractmethod
    def process_file(self, path: Path) -> tuple[int, str]: ...

    def report(self) -> None:
        for result in self.history:
            print()
            print(
                f"{result.path.relative_to(self.base)} "
                f"{self.__class__.__name__} "
                f"{result.returncode} "
                f"{result.duration * 1000:.0f}msec "
            )
            for line in result.output:
                print(f"  {line}")


class FindDoctest(FindAndProcess):
    def process_file(self, path: Path) -> tuple[int, str]:
        command = [
            "python",
            "-m",
            "doctest",
            "-o",
            "ELLIPSIS",
            "-o",
            "NORMALIZE_WHITESPACE",
            str(path),
        ]
        response = subprocess.run(
            command, capture_output=True, text=True
        )
        return response.returncode, response.stdout


class FindRuffCheck(FindAndProcess):
    def process_file(self, path: Path) -> tuple[int, str]:
        command = [
            "uv",
            "tool",
            "run",
            "ruff",
            "check",
            str(path),
        ]
        response = subprocess.run(
            command, capture_output=True, text=True
        )
        return response.returncode, response.stdout


def main():
    project = (
        Path.home()
        / "Documents"
        / "Writing"
        / "Building Skills"
        / "Unlearning Shell Scripting"
    )
    book = project / "rst_book"
    FindDoctest(book / "chapters", "*.rst").process_all()
    FindRuffCheck(project / "src", "*.py").process_all()


def processed_set(output_lines: list[str]) -> set[str]:
    """Summary logs:

    -   First line: filename classname int duration

    -   Remaining lines: indented two spaces

    Plus, an optional introduction with non-indented classname line.
    """
    non_empty_lines = filter(None, output_lines)
    non_indented_lines = filter(
        lambda line: not line.startswith("  "), non_empty_lines
    )
    parsed_lines = (line.split() for line in non_indented_lines)
    first = (
        path for path, class_name, return_code, duration in parsed_lines
    )
    return set(first)


def test_find_doctest(capsys):
    project = (
        Path.home()
        / "Documents"
        / "Writing"
        / "Building Skills"
        / "Unlearning Shell Scripting"
    )
    book = project / "rst_book"
    FindDoctest(book / "chapters", "*.rst").process_all()
    out, err = capsys.readouterr()
    assert processed_set(out.splitlines()[2:]) == {
        "01-why-unlearn.rst",
        "02-some-basics.rst",
        "03-process-resource-handling.rst",
        "04-data-transformation-tools.rst",
        "05-shell-scripts-and-functions.rst",
        "06-complex-shell-logic.rst",
        "07-testing.rst",
        "08-shell-strengths.rst",
        "index.rst",
    }


def test_find_ruffcheck(capsys):
    project = (
        Path.home()
        / "Documents"
        / "Writing"
        / "Building Skills"
        / "Unlearning Shell Scripting"
    )
    book = project / "rst_book"
    FindRuffCheck(book / "src", "*.py").process_all()
    out, err = capsys.readouterr()
    print(out)
    assert processed_set(out.splitlines()[2:]) == {
        "all_tests.py",
        "awk.py",
        "cleanup_example.py",
        "find_classes.py",
        "find_classes_cli.py",
        "find_example.py",
        "summary_example.py",
        "test_awk.py",
        "test_find_example.py",
    }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
