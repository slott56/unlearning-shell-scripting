"""
Unlearning Shell Scripting. Chapter 6. Pytest Example.
"""

from unittest.mock import MagicMock, Mock, sentinel
import pytest

import find_example

@pytest.fixture
def mock_full_path():
    return Mock(
        is_file=Mock(return_value=True),
        name=Mock(return_value=sentinel)
    )

@pytest.fixture
def mock_dir_path(mock_full_path):
    return MagicMock(
        __truediv__=Mock(return_value=mock_full_path)
    )

@pytest.fixture
def mock_base_path(mock_dir_path):
    mock_base_path = Mock(
        walk=Mock(
            return_value=[
                (mock_dir_path, [".name"], [".name", "filename"]),
            ]
        )
    )
    return mock_base_path

@pytest.fixture
def mock_fnmatch():
    return Mock(return_value=True)

@pytest.fixture
def patched_fnmatch(mock_fnmatch, monkeypatch):
    monkeypatch.setattr(find_example, 'fnmatch', mock_fnmatch)


def test_find_iter(
        mock_base_path, mock_dir_path, mock_full_path, mock_fnmatch,
        patched_fnmatch
    ):
    found = list(find_example.find_iter(mock_base_path, sentinel.PATTERN))
    assert len(found) == 1
    assert found[0] == mock_full_path
    mock_base_path.walk.assert_called_once()
    mock_full_path.is_file.assert_called_once()
    mock_fnmatch.assert_called_once_with("filename", sentinel.PATTERN)
