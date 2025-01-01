from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, NamedTuple


class MonthTuple(NamedTuple):
    year: int
    month: int
    name: str


@dataclass
class FilesTuple:
    name: str
    file_prefix: str

    def get_file_path(self, import_folder: Path) -> list[Path]:
        files = import_folder.glob(f"{self.file_prefix}*")
        file_paths = [f for f in files]
        print(
            f"[FilesTuple][{self.name}] found {file_paths=} in {import_folder.as_posix()}"
        )
        return file_paths


TargetAmountDict = Dict[str, float]
PurposeAmountDict = Dict[str, TargetAmountDict]
MonthsList = List[MonthTuple]
ExpensesList = List[float]
