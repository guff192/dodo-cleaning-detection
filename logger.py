from tracker import TableEvent


def log_processing_info(video_path: str, preview_enabled: bool):
    print(f"Processing video: {video_path}")
    if preview_enabled:
        print("Preview mode ENABLED. Press 'q' to stop.")
    else:
        print("Running in background mode (faster)...")


def log_progress(frame_count: int, total_frames: int) -> None:
    if frame_count % 200 == 0:
        percentage = frame_count * 100 // total_frames
        print(
            f"\rProcessed {frame_count}/{total_frames} ({percentage}%) frames...",
            end="",
        )


def log_event(event: TableEvent) -> None:
    print(f"\n[{event.timestamp:.1f}s] Event: {event.type.value}")
