import sys


def exit_with_err_description(description: str) -> None:
    print(description, file=sys.stderr)
    exit(1)


class NonPositiveRectangleAreaException(Exception):
    def __init__(self) -> None:
        super().__init__("The area of this rectangle is not a positive number!")
