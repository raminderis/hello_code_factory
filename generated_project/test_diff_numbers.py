import builtins
from io import StringIO
import sys
import pytest

from main import diff_numbers, main


# -----------------------------
# Tests for add_numbers()
# -----------------------------

def test_diff_numbers_valid():
    assert diff_numbers(3, 2) == 1
    assert diff_numbers(20, 10) == 10


def test_diff_numbers_invalid_type():
    with pytest.raises(ValueError):
        diff_numbers("a", 5)

    with pytest.raises(ValueError):
        diff_numbers(5, None)


# -----------------------------
# Integration test for main()
# -----------------------------

def test_main_integration(monkeypatch, capsys):
    # Simulate two valid inputs: 4 and 6
    inputs = iter(["6", "4"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))

    # Capture stdout
    main()

    output = capsys.readouterr().out.lower()

    # Check key phrases
    assert "6 - 4 = 2" in output