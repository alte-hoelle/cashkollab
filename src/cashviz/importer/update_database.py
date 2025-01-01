from pathlib import Path

from git import Repo

from cashviz.importer.import_all import import_all
from cashviz.models.account import Account
from cashviz.models.billing_changes import BillingChanges
from cashviz.models.budget import Budget
from cashviz.models.category import Category
from cashviz.models.groups import Groups
from cashviz.models.journal_entry import JournalEntry
from cashviz.models.name_mapping import NameMapping
from cashviz.models.person import Person
from cashviz.models.purpose import Purpose
from cashviz.models.skr import SkrAccount, SkrCategory
from config import HELL_CONFIG


def pull_transactions(path: Path) -> bool:
    repo: Repo = Repo(path)
    repo.active_branch.commit = repo.commit(
        "HEAD~1"
    )  # letzten commit vergessen, falls jemand amendet hat
    repo.head.reset(
        working_tree=True
    )  # lokale aenderungen verwerfen (aus dem vergessenen commit)
    repo.remotes.origin.pull()  # neu pullen
    return True


def delete_database() -> None:
    NameMapping.objects.all().delete()
    Budget.objects.all().delete()
    Category.objects.all().delete()
    Purpose.objects.all().delete()
    Account.objects.all().delete()
    Person.objects.all().delete()
    Groups.objects.all().delete()
    BillingChanges.objects.all().delete()
    JournalEntry.objects.all().delete()
    SkrCategory.objects.all().delete()
    SkrAccount.objects.all().delete()


def update_database() -> None:
    repo_path = HELL_CONFIG.transactions_repo.resolve()
    data_path = repo_path / HELL_CONFIG.transactions_repo_data_folder
    print(f"import from {data_path=}")
    if pull_transactions(repo_path):
        delete_database()
        import_all(data_path, verbose=False)
