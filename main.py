import solvers
import sys

if len(sys.argv) != 2 and len(sys.argv) != 3:
    print(f'expected 1 or 2 arguments to main.py, got {len(sys.argv) - 1} arg(s)', file=sys.stderr, end='\n', flush=True)
    sys.exit(1)

arg: str = sys.argv[1]
example_str: str | None = sys.argv[-1] if len(sys.argv) == 3 else None
example: bool = False
day: int | None = None
run_all: bool = False

if example_str is not None:
    if example_str == 'example':
        example = True
    else:
        print(f"expected 'example' or nothing for trialing argument, got {repr(arg)}", file=sys.stderr, end='\n', flush=True)
        sys.exit(1)

if arg == 'latest':
    pass

elif arg == 'all':
    if example:
        print(f"got 'example' with 'all', not supported", file=sys.stderr, end='\n', flush=True)
        sys.exit(1)
    day = None
    run_all = True

else:
    try:
        day = int(arg)
        if not 1 <= day <= 12:
            raise ValueError
    except ValueError as ex:
        print(f"expected 'latest', 'all', or day number as integer 1 to 12, got {repr(arg)}", file=sys.stderr, end='\n', flush=True)
        sys.exit(1)

try:
    if not run_all:
        solvers.solve(day, example)
    else:
        solvers.profile(samples=100)

except KeyboardInterrupt as err:
    print('solver cancelled by user', file=sys.stderr, end='\n', flush=True)
    sys.exit(1)

except solvers.SolverError as err:
    print(err, file=sys.stderr, end='\n', flush=True)
    sys.exit(1)
