from pathlib import Path

from cashviz.importer import (
    budget_file,
    cash_file,
    categorie_file,
    name_mapping_file,
    payment_file,
    person_file,
)
from cashviz.importer.budget import BudgetImporter
from cashviz.importer.categorie import CategorieImporter
from cashviz.importer.name_mapping import NameMappingImporter
from cashviz.importer.payments import JournalEntryImporter
from cashviz.importer.persons import PersonImporter


def import_all(path: Path, verbose: bool = False) -> None:
    # SkrImporter(skr_file.get_file_path())
    NameMappingImporter(name_mapping_file.get_file_path(path), verbose=verbose)
    PersonImporter(person_file.get_file_path(path), verbose=verbose)
    CategorieImporter(categorie_file.get_file_path(path), verbose=verbose)
    journals = payment_file.get_file_path(path) + cash_file.get_file_path(path)
    JournalEntryImporter(journals, verbose=verbose)
    BudgetImporter(budget_file.get_file_path(path), verbose=verbose)
