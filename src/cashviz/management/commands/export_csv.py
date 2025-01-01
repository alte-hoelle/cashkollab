import sqlite3
from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
from django.core.management.base import BaseCommand

export_base_path = Path("data/export")


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, _parser: ArgumentParser) -> None:
        pass

    def handle(self, *_args: tuple[Any], **_options: dict[Any, Any]) -> None:
        conn = sqlite3.connect(
            "db.sqlite3", isolation_level=None, detect_types=sqlite3.PARSE_COLNAMES
        )
        tables = pd.read_sql_query(
            "SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%'",
            conn,
        )
        table_names = [row["name"] for index, row in tables.iterrows() if row["name"]]
        export_base_path.mkdir(exist_ok=True)
        export_path = export_base_path.joinpath(datetime.now().isoformat())
        export_path.mkdir(exist_ok=True)
        export_latest_path = export_base_path.joinpath("latest")
        if export_latest_path.exists():
            export_latest_path.unlink()
        export_latest_path.symlink_to(Path(export_path.resolve()))
        for name in table_names:
            db_df = pd.read_sql_query(f"SELECT * FROM {name}", conn)
            db_df.to_csv(f"{export_path.as_posix()}/{name}.csv", index=False)
