import os
from pathlib import Path


def get_base_dir() -> Path:
    possible_base_dir = os.getcwd()
    if "/src" in possible_base_dir:
        splitted = possible_base_dir.split("/src")
        possible_base_dir = splitted[0]
    return Path(possible_base_dir)
