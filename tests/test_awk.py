"""
Unlearning Shell Scripting. Chapter 4. Test for the awk.py app.
"""

import subprocess
from textwrap import dedent


def test_awk():
    standard_input = dedent("""\
        first line of data
        second line
    """)
    proc = subprocess.run(
        "python src/awk.py",
        shell=True,
        input=standard_input,
        capture_output=True,
        text=True
    )
    assert proc.returncode == 0
    assert proc.stdout.splitlines() == [
        'line first',
        'line second'
    ]
