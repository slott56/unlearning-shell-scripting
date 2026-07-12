"""
Unlearning Shell Scripting. Chapter 4. AWK demo.
"""

import sys


def main():
    for line in sys.stdin:
        row = line.split()
        print(row[1], row[0])


if __name__ == "__main__":
    main()
