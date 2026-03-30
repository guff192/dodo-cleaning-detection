import sys


def exit_with_err_description(description: str) -> None:
    print(description, file=sys.stderr)
    exit(1)


class CantOpenVideo(Exception):
    def __init__(self, video_path: str | None = None) -> None:
        msg = 'Can\'t open video'
        if video_path:
            msg += ': ' + video_path
        msg += '!'

        super().__init__(msg)


class NonPositiveRectangleAreaException(Exception):
    def __init__(self) -> None:
        super().__init__("The area of this rectangle is not a positive number!")
