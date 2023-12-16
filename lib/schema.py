from dataclasses import dataclass
from typing import List, Text


@dataclass
class FrameMetadata:
    series: Text
    eps: Text
    hour: Text
    minute: Text
    second: Text
    vector: List
    frame_index: int
    frame_count: int


@dataclass
class VideoFrame:
    file_name: Text
    file_hash: Text
    frames: List[FrameMetadata]
