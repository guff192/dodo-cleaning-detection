def log_processing_info(video_path: str, preview_enabled: bool):
    print(f"Processing video: {video_path}")
    if preview_enabled:
        print("Preview mode ENABLED. Press 'q' to stop.")
    else:
        print("Running in background mode (faster)...")


def log_progress(frame_count: int, total_frames: int) -> None:
    if frame_count % 500 == 0:
        print(f"\rProcessed {frame_count}/{total_frames} ({frame_count * 100 // total_frames}%) frames...", end="")
