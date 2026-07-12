"""
Unlearning Shell Scripting.  Chapter 6. Cleanup Example.
"""

from pathlib import Path
import subprocess


def run_with_cleanup(some_argument: Path) -> Path:
    try:
        subprocess.run(
            ["some", "command", str(some_argument)],
            check=True,
        )
        output_file = some_argument.with_suffix(".out")
        return output_file
    except subprocess.CalledProcessError:
        # Cleanup everything but the log.
        for cleanup in some_argument.parent.glob("*.*"):
            if cleanup.suffix == ".log":
                continue
            cleanup.unlink()
        raise


import unittest
from unittest.mock import Mock, patch, sentinel


class CleanupFixture(unittest.TestCase):
    def setUp(self) -> None:
        self.path_1 = Mock()
        self.path_log = Mock()
        self.path_2 = Mock()
        self.parent_path = Mock(
            name="Path.parent",
            glob=Mock(
                return_value=[
                    self.path_1,
                    self.path_log,
                    self.path_2,
                ]
            ),
        )
        self.new_path = Mock()
        self.new_path.name = sentinel.NEW_NAME

        self.mock_path = Mock(
            name="Path instance",
            with_suffix=Mock(return_value=self.new_path),
        )
        self.mock_path.parent = self.parent_path


class TestCleanup(CleanupFixture):
    def test_success(self) -> None:
        with patch(
            "subprocess.run",
            Mock(return_value=Mock(name="mock result")),
        ) as mocked_run:
            result = run_with_cleanup(self.mock_path)
            mocked_run.assert_called_once_with(
                ["some", "command", str(self.mock_path)],
                check=True,
            )
            self.assertEqual(result.name, sentinel.NEW_NAME)
            self.mock_path.with_suffix.assert_called_once_with(".out")
            self.mock_path.parent.glob.assert_not_called()

    def test_fail(self) -> None:
        with patch(
            "subprocess.run",
            Mock(
                side_effect=subprocess.CalledProcessError(
                    cmd=f"some command {self.mock_path!s}", returncode=2
                )
            ),
        ) as mocked_run:
            self.assertRaises(
                subprocess.CalledProcessError,
                run_with_cleanup,
                self.mock_path,
            )
            mocked_run.assert_called_once_with(
                ["some", "command", str(self.mock_path)],
                check=True,
            )
            self.mock_path.parent.glob.assert_called_once_with("*.*")
            path_1, path_log, path_2 = (
                self.mock_path.parent.glob.return_value
            )
            path_1.unlink.assert_called_once_with()
            path_2.unlink.assert_called_once_with()
            path_log.assert_not_called()
