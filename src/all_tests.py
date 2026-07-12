"""
Unlearning Shell Scripting.  Chapter 3.  The all_tests application.
"""

from concurrent import futures
from contextlib import redirect_stdout
import doctest
import io
from pathlib import Path
import subprocess


def run_subprocess(chapter: Path) -> tuple[Path, list[str]]:
    """Use subprocess.run()"""
    command = [
        "python",
        "-m",
        "doctest",
        "-o",
        "ELLIPSIS",
        "-o",
        "NORMALIZE_WHITESPACE",
        str(chapter),
    ]
    response = subprocess.run(command, capture_output=True, text=True)
    return (chapter, response.stdout.splitlines())


def run_directly(chapter: Path) -> tuple[Path, list[str]]:
    """Run doctest directly."""
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        run, passed = doctest.testfile(
            str(chapter),
            module_relative=False,
            optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS,
            report=True,
        )
    return (chapter, buffer.getvalue().splitlines())


def main() -> None:
    project = (
        Path.home()
        / "Documents"
        / "Writing"
        / "Building Skills"
        / "Unlearning Shell Scripting"
    )
    book = project / "rst_book"
    with futures.ProcessPoolExecutor() as pool:
        path_iter = (book / "chapters").glob("*.rst")
        results = pool.map(run_subprocess, path_iter)
        for chapter, text in results:
            if text:
                print(chapter.name, "FAILED")
                for line in text:
                    print(line)
                print()
            else:
                print(chapter.name, "PASSED")


# Tests require pytest.
def test_all_tests(capsys):
    main()
    out, err = capsys.readouterr()
    assert out.splitlines() == [
        "index.rst PASSED",
        "03-process-resource-handling.rst PASSED",
        "05-shell-scripts-and-functions.rst PASSED",
        "02-some-basics.rst PASSED",
        "04-data-transformation-tools.rst PASSED",
        "06-complex-shell-logic.rst PASSED",
        "08-shell-strengths.rst PASSED",
        "01-why-unlearn.rst PASSED",
        "07-testing.rst PASSED",
    ]


if __name__ == "__main__":
    main()
