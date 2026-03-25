import argparse
import os
import os.path

from errors import exit_with_err_description
from video import select_roi, run_preview

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Detects time bounds of people interactions with tables from restaurant's camera video"
    )
    parser.add_argument("--video", type=str, required=True)

    args = parser.parse_args()
    video = args.video

    if not os.path.exists(video):
        full_path = os.path.join(os.getcwd(), video)
        exit_with_err_description(f'Video "{full_path}" does not exist!')

    print(f"Selected video: {video}")

    roi = select_roi(video)
    x, y, w, h = roi
    print(
        f"Selected table coordinates: upper-left corner: ({x}, {y}), width: {w}, height: {h}"
    )

    run_preview(video, roi)
