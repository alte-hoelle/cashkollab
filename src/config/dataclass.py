from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class CreditConfig:
    mapping: dict[str, str]


@dataclass
class SpendingConfig:
    exclude: list[str]


@dataclass
class HellConfig:
    allowed_hosts: list[str]
    anon_names: bool
    transactions_repo: Path
    transactions_repo_data_folder: Path
    spending: SpendingConfig = field(default_factory=lambda: SpendingConfig([]))
    credit: CreditConfig = field(default_factory=lambda: CreditConfig({}))
