import json
from typing import List

from overrides import EnforceOverrides, final


class JsonImporter(EnforceOverrides):
    def __init__(self, files: str | list[str], verbose: bool = False):
        self.files = files
        self.objects: List[dict] = []
        self.verbose = verbose
        self.read()
        self._import()

    @final
    def read(self) -> None:
        print(f"reading document[s]: {self.files}")
        if isinstance(self.files, str):
            self.files = [self.files]
        for file in self.files:
            with open(file) as opened_file:
                if opened_file is not None:
                    self.objects = json.load(opened_file)

    def _import(self) -> None:
        pass


class CsvImporter(EnforceOverrides):
    def __init__(self, files: str | list[str], verbose: bool = False):
        self.files = files
        print(f"[CsvImporter][__init__] {files=}")
        self.lines: List[str] = []
        self.verbose = verbose
        self.read()
        self._import()

    @final
    def read(self) -> None:
        print(f"[CsvImporter][read] reading document[s]: {self.files}")
        self.lines = []
        if isinstance(self.files, str):
            self.files = [self.files]
        for file in self.files:
            print(f"[CsvImporter][read] open file: {file}")
            if file != "":
                with open(file, encoding="utf-8") as opened_file:
                    if opened_file is not None:
                        try:
                            lines = opened_file.readlines()
                            self.lines += lines
                            print(
                                f"[CsvImporter][read] read lines count: {len(lines)} total: {len(self.lines)}"
                            )
                        except UnicodeDecodeError as e:
                            print(f"Error in {file}")
                            print(e)
                    else:
                        print("[CsvImporter][read] opened_file is None")

    def _import(self) -> None:
        pass
