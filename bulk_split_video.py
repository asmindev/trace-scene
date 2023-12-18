import os
import time
from pathlib import Path
from datetime import timedelta

from lib.video import VideoProcessor


def split_video(video_file):
    start_time = time.time()
    if type(video_file) == str:
        video_file = Path(video_file)
    folder = video_file.parent.name
    filename = video_file.stem

    print(f"\nSplitting {filename} in {folder}...")
    video = VideoProcessor(str(video_file))
    frames = video.process_frames()
    video.save_frames_as_pickle(frames)
    end = time.time() - start_time
    delta = timedelta(seconds=float(end))
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    print(f"\nTotal time taken: {hours:02d}:{minutes:02d}:{seconds:02d}")


def process_videos(root_dir, pattern="**/*.mp4", max_workers=None):
    video_files = list(Path(root_dir).rglob(pattern))

    print(f'Found {len(video_files)} videos in "{root_dir.name}"...')
    start_time = time.time()
    videos = sorted(video_files)
    for video_file in videos:
        split_video(video_file)
    delta = timedelta(seconds=float(time.time() - start_time))
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    print(
        f"\nDone splitting all videos in {root_dir.name}! with total time taken: {hours:02d}:{minutes:02d}:{seconds:02d}"
    )


if __name__ == "__main__":
    root_directory = Path(__file__).parent / "videos"

    # Get max_workers from input

    process_videos(root_directory)
