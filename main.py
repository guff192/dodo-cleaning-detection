import argparse
import os
import os.path

from errors import exit_with_err_description
from video import select_roi, process_video

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

    process_video(video, roi)
