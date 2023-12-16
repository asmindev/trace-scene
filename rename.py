import os
from pathlib import Path

movie = Path(__file__).parent / "videos"


def refactor():
    """
    Renames files in the given directory by adding a three-digit index at the beginning of each file name.

    Parameters:
        None

    Returns:
        None
    """
    for root, dirs, files in os.walk(movie):
        sort = sorted(files)
        for index, file in enumerate(sort, 1):
            filepath = os.path.join(root, file)
            _, ext = os.path.splitext(filepath)
            new_filename = f"{index:03d}{ext}"
            new_filepath = os.path.join(root, new_filename)
            os.rename(filepath, new_filepath)
            print(f"Renaming {_} to {new_filename}")


refactor()
