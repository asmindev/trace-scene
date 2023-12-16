import pickle
import zlib
from pathlib import Path
from lib.schema import FrameMetadata


class AddToCollection:
    def __init__(self, file_hash):
        self.file_hash = file_hash

    def get_data(self):
        with open(f"database/{self.file_hash}.pickle", "rb") as f:
            raw = zlib.decompress(f.read())
            print(raw)

    def show_data(self):
        data = self.get_data()
        print(data)


tes = AddToCollection("36d1cdbc4834a8acaff9803793c0a790")
tes.show_data()
