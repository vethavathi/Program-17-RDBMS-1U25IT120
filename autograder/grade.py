
import re
import sys
from pathlib import Path

solution_file = Path("solution.sql")

if not solution_file.exists():
    print("FAIL: solution.sql not found.")
    sys.exit(1)

code = solution_file.read_text(
    encoding="utf-8",
    errors="ignore"
)

# Remove comments
code = re.sub(r"--.*", "", code)
code = re.sub(r"/\*.*?\*/", "", code, flags=re.DOTALL)

code_upper = code.upper()

passed = 0
total = 6


def check(test_name, condition):
    global passed

    if condition:
        print(f"PASS: {test_name}")
        passed += 1
    else:
        print(f"FAIL: {test_name}")


# --------------------------------------------------
# TEST 1: FOR LOOP exists
# --------------------------------------------------

for_loop = re.search(
    r"\bFOR\s+\w+\s+IN\s+\d+\s*\.\.\s*\d+\s+LOOP\b",
    code_upper
)

check(
    "TC01 - FOR LOOP is used",
    for_loop is not None
)


# --------------------------------------------------
# TEST 2: Loop starts at 1
# --------------------------------------------------

start_one = re.search(
    r"\bFOR\s+\w+\s+IN\s+1\s*\.\.",
    code_upper
)

check(
    "TC02 - Loop starts from 1",
    start_one is not None
)


# --------------------------------------------------
# TEST 3: Loop ends at 10
# --------------------------------------------------

end_ten = re.search(
    r"\.\.\s*10\s+LOOP\b",
    code_upper
)

check(
    "TC03 - Loop ends at 10",
    end_ten is not None
)


# --------------------------------------------------
# TEST 4: DBMS_OUTPUT.PUT_LINE
# --------------------------------------------------

put_line = re.search(
    r"DBMS_OUTPUT\s*\.\s*PUT_LINE\s*\(",
    code_upper
)

check(
    "TC04 - DBMS_OUTPUT.PUT_LINE is used",
    put_line is not None
)


# --------------------------------------------------
# TEST 5: BEGIN and END
# --------------------------------------------------

plsql_block = (
    re.search(r"\bBEGIN\b", code_upper) is not None
    and re.search(r"\bEND\s*;", code_upper) is not None
)

check(
    "TC05 - PL/SQL BEGIN/END block exists",
    plsql_block
)


# --------------------------------------------------
# TEST 6: No hard-coded ten output statements
# --------------------------------------------------

hardcoded_outputs = re.findall(
    r"DBMS_OUTPUT\s*\.\s*PUT_LINE\s*\(\s*['\"]?\s*(?:[1-9]|10)\s*['\"]?\s*\)",
    code_upper
)

no_hardcoding = len(hardcoded_outputs) < 10

check(
    "TC06 - Numbers are not hard-coded ten times",
    no_hardcoding
)


# --------------------------------------------------
# FINAL RESULT
# --------------------------------------------------

print()
print("--------------------------------")
print(f"TOTAL SCORE: {passed}/{total}")
print("--------------------------------")

if passed == total:
    print("AUTOGRADER RESULT: PASS")
    sys.exit(0)
else:
    print("AUTOGRADER RESULT: FAIL")
    sys.exit(1)
