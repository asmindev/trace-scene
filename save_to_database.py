from pathlib import Path
import time
from datetime import timedelta
from lib.utils import Pickle
from lib.schema import VideoFrame
from lib.chroma import collection
from lib.frame import Frame


def main(files):
    for file in files:
        # get file name
        start = time.time()
        file_name = file.stem
        pickle = Pickle(file_hash=file_name)
        if pickle.is_db_exists():
            data: VideoFrame = pickle.get_data()
            length = len(data.frames)
            for index, frame in enumerate(data.frames):
                _, fhash = Frame()._generate_hash_frame(frame)
                insert_frame = dict(
                    series=frame.series,
                    eps=frame.eps,
                    hour=frame.hour,
                    minute=frame.minute,
                    second=frame.second,
                    frame_index=frame.frame_index,
                )
                collection.add(
                    ids=[fhash], embeddings=[frame.vector], metadatas=[insert_frame]
                )
                percentage = (index / length) * 100

                print(
                    f"Saving {frame.series} with episode {frame.eps} {fhash} ({percentage:.2f}%)",
                    end="\r",
                )
            pickle.edit_exists_in_database()
            end = time.time() - start
            delta = timedelta(seconds=float(end))
            hours, remainder = divmod(delta.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            print(f"\nTotal time taken: {hours:02d}:{minutes:02d}:{seconds:02d}")
        else:
            print(f"file hash {pickle.file_hash} already exists in database")
            print("Skipping...")


if __name__ == "__main__":
    databases = Path(__file__).parent / "database"
    # get all file with pickle extension
    files = [f for f in databases.iterdir() if f.suffix == ".pickle"]
    main(files)
