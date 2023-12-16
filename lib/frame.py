from typing import Tuple
from hashlib import md5

from .schema import FrameMetadata


class Frame:
    def __init__(self):
        """
        Initializes the Frame class

        Returns:
            None
        """
        pass

    def _generate_hash_frame(self, metadata: FrameMetadata) -> Tuple[str, str]:
        """
        Generates the metadata for a frame.

        Parameters:
            metadata (Metadata): The metadata object containing the information to generate the frame's metadata.

        Returns:
            tuple: A tuple containing the frame name and frame hash.
        """
        frame_name = f"{metadata.series}_{metadata.eps}_{metadata.hour:02d}_{metadata.minute:02d}_{metadata.second:02d}_{metadata.frame_count:04d}"
        frame_hash = md5(frame_name.encode("utf-8")).hexdigest()
        return frame_name, frame_hash
