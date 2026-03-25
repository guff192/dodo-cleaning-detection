import sys


def exit_with_err_description(description: str) -> None:
    print(description, file=sys.stderr)
    exit(1)
