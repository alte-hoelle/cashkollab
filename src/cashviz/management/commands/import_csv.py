import sqlite3
from argparse import ArgumentParser
from pathlib import Path
from typing import Any

import pandas
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            "--path",
            type=str,
            default="data/export/latest",
            help="path to a folder with exported CSVs to import. default (data/export/latest)",
        )

    def handle(self, *_args: tuple[Any], **options: dict[str, str]) -> None:
        path = str(options["path"])
        file_names = [dx.name.split(".")[0] for dx in Path(path).glob("*")]
        conn = sqlite3.connect(
            "db.sqlite3", isolation_level=None, detect_types=sqlite3.PARSE_COLNAMES
        )

        for name in file_names:
            df = pandas.read_csv(f"data/export/{name}.csv")
            df.to_sql(name, conn, if_exists="append", index=False)
