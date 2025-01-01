from pathlib import Path

from config.dataclass import HellConfig

HELL_CONFIG = HellConfig(
    allowed_hosts=[
        "10.79.30.8",
        "localhost",
        "127.0.0.1",
        "hellcash.local.hausprojekt.org",
        "hellcash.lan.alte-hoelle.de",
        "wgkasse.lan.alte-hoelle.de",
        "aczcash.lan.alte-hoelle.de",
    ],
    anon_names=False,
    transactions_repo=Path("../transactions"),
    transactions_repo_data_folder=Path("data"),  # ..transactions/data/*.csv
)
