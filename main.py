import argparse
import os
import os.path

from analytics import print_statistics
from config import OUTPUT_VIDEO_NAME
from errors import exit_with_err_description
from video import render_output_video, select_roi, process_video

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Detects time bounds of people interactions with tables from restaurant's camera video"
    )
    parser.add_argument("--video", type=str, required=True)
    parser.add_argument(
        "--preview", action="store_true", help="Show live detection preview (slow)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=OUTPUT_VIDEO_NAME,
        help="Name of the output video file",
    )

    args = parser.parse_args()
    video = args.video

    if not os.path.exists(video):
        full_path = os.path.join(os.getcwd(), video)
        exit_with_err_description(f'Video "{full_path}" does not exist!')

    print(f"Selected video: {video}")

    roi = select_roi(video)

    events = process_video(video, roi, args.preview)

    print_statistics(events)

    output_path = os.path.join(os.getcwd(), args.output)
    render_output_video(video, output_path, events, roi)
