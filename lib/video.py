import os
from typing import Generator, Tuple, List, Dict, Text
from datetime import timedelta

from PIL import Image
from moviepy.video.io.VideoFileClip import VideoFileClip

from .schema import FrameMetadata
from .chroma import collection
from .predict import Img2VecPredictor
from .utils import Pickle


class VideoProcessor(Pickle):
    def __init__(self, video_path):
        self.video = VideoFileClip(video_path)
        self.total_frames = self.video.duration * self.video.fps
        self.__frame_per_second = 2
        self.predict = Img2VecPredictor()
        super().__init__(file_name=self.get_series_info()["series"])

    def get_series_info(self) -> Dict[str, str]:
        """
        Extracts series information from the video filename.

        Returns:
            dict: A dictionary containing the series name and episode number.
                - "series" (str): The name of the series.
                - "episode" (str): The episode number.
        """
        folder, file_name = os.path.split(self.video.filename)
        folder_path = os.path.abspath(folder).split(os.sep)

        series = folder_path[len(folder_path) - 1]
        episode, _ = os.path.splitext(file_name)
        return {"series": series, "episode": episode}

    def get_timestamp(self, duration) -> Tuple[int, int, int]:
        """
        Calculate the hours, minutes, and seconds from a given duration in seconds.

        Parameters:
            duration (int): The duration in seconds.

        Returns:
            tuple: A tuple containing the hours, minutes, and seconds.
        """
        hours, remainder = divmod(duration.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return hours, minutes, seconds

    def process_frames(self) -> Generator[FrameMetadata, None, None]:
        """
        Processes the frames of a video and yields FrameMetadata objects.

        Returns:
            Generator[FrameMetadata, None, None]: A generator that yields FrameMetadata objects.
        """

        frame_count = 0
        duration = timedelta(seconds=0)
        predict = Img2VecPredictor()
        for i, frame in enumerate(self.video.iter_frames(self.__frame_per_second)):
            frame_count += 1
            im = Image.fromarray(frame).convert("RGB")
            vector = predict.vectorize(image=im)

            if vector is None:
                continue
            data = self.get_series_info()
            series = data["series"]
            episode = data["episode"]
            hour, minute, second = self.get_timestamp(duration)

            frame_metadata = FrameMetadata(
                series=series,
                eps=episode,
                hour=hour,
                minute=minute,
                second=second,
                frame_index=i,
                vector=vector,
                frame_count=frame_count,
            )

            if frame_count >= self.__frame_per_second:
                frame_count = 0
                duration += timedelta(seconds=1)
            yield frame_metadata

    def save_frames_as_pickle(
        self, frames: Generator[FrameMetadata, None, None] = None
    ):
        """
        Saves the frames to the pickle file.

        Args:
            frames (List[FrameMetadata], optional): The frames to be saved. Defaults to None.

        Returns:
            None
        """
        embeddings = []
        total_frames = self.video.duration * self.__frame_per_second
        for index, frame in enumerate(frames, 1):
            percentage = (index / total_frames) * 100
            print(
                f"Saving frame {frame.frame_index} Series: {frame.series} with episode {frame.eps} {frame.hour:02d}:{frame.minute:02d}:{frame.second:02d} {frame.frame_index}{frame.frame_count} ({percentage:.2f}%)",
                end="\r",
            )
            embeddings.append(frame)
        self.save(embeddings=embeddings)


if __name__ == "__main__":
    import time

    starttime = time.time()

    video_processor = VideoProcessor(
        "/home/zett/project/nafis/video-search/videos/ALL OF US ARE DEAD/002.mp4"
    )
    frames: List[FrameMetadata] = video_processor.process_frames()

    video_processor.save_frames_as_pickle(frames=frames)
    taken = f"{time.time() - starttime}"
    # use divide by 60
    delta = timedelta(seconds=float(taken))
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    print(f"\nTotal time taken: {hours:02d}:{minutes:02d}:{seconds:02d}")
