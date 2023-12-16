import json
import zlib
import pickle
from hashlib import md5
from pathlib import Path
from typing import List

from .schema import FrameMetadata, VideoFrame


class Pickle:
    def __init__(self, file_name):
        self.file_name = file_name
        self.file_hash = md5(file_name.encode("utf-8")).hexdigest()
        self.static = Path(Path(__file__).parent).parent / "database"
        Path(self.static).mkdir(exist_ok=True)

    def __repr__(self) -> str:
        return f"<Pickle {self.file_hash}>"

    def save_log(self):
        file_json = f"{self.static}/log.json"
        if not Path(file_json).exists():
            Path(file_json).touch()
            with open(file_json, "w") as f:
                data = [
                    dict(
                        index=0,
                        name=self.file_name,
                        hash=self.file_hash,
                        episode=1,
                        db_exists=False,
                    )
                ]
                f.write(json.dumps(data))
        else:
            with open(file_json, "r") as f:
                data = json.loads(f.read())
                for index, d in enumerate(data):
                    if d["hash"] == self.file_hash:
                        data[index]["episode"] += 1
                        with open(file_json, "w") as f:
                            f.write(json.dumps(data))
                        return
                data.append(
                    dict(
                        index=len(data),
                        name=self.file_name,
                        hash=self.file_hash,
                        db_exists=False,
                    )
                )
                with open(file_json, "w") as f:
                    f.write(json.dumps(data, indent=4))
            return

    def save(self, embeddings: List[FrameMetadata]) -> None:
        if not Path(f"{self.static}/{self.file_hash}.pickle").exists():
            data = VideoFrame(
                file_name=self.file_name, file_hash=self.file_hash, frames=[embeddings]
            )
            with open(f"{self.static}/{self.file_hash}.pickle", "wb") as f:
                f.write(zlib.compress(pickle.dumps(data)))
        else:
            # load old data
            with open(f"{self.static}/{self.file_hash}.pickle", "rb") as f:
                data: VideoFrame = pickle.loads(zlib.decompress(f.read()))
                data.frames.extend(embeddings)
                with open(f"{self.static}/{self.file_hash}.pickle", "wb") as f:
                    f.write(zlib.compress(pickle.dumps(data)))
        self.save_log()
