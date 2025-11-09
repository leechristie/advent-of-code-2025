import solvers
import sys

# check for number of arguments
if len(sys.argv) != 2 and len(sys.argv) != 3:
    print(f'expected 1 or 2 arguments to main.py, got {len(sys.argv) - 1} arg(s)', file=sys.stderr, end='\n', flush=True)
    sys.exit(1)

arg: str = sys.argv[1]
example_str: str | None = sys.argv[-1] if len(sys.argv) == 3 else None
status: int
example: bool = False

# check if 'example' for appended (set example flag if so)
if example_str is not None:
    if example_str == 'example':
        example = True
    else:
        print(f"expected 'example' or nothing for trialing argument, got {repr(arg)}", file=sys.stderr, end='\n', flush=True)
        sys.exit(1)

# if 'latest', allow `solve` to choose the latest puzzle
if arg == 'latest':
    status = solvers.solve(None, example)
    sys.exit(status)

# parse the input day
try:
    day: int = int(arg)
    if not 1 <= day <= 12:
        raise ValueError
except ValueError:
    print(f"expected 'latest', or day number as integer 1 to 12, got {repr(arg)}", file=sys.stderr, end='\n', flush=True)
    sys.exit(1)

# request solve for the specified day
status = solvers.solve(day, example)
sys.exit(status)
