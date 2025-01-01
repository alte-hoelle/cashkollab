from ..helpers.types import FilesTuple
from .base_importer import CsvImporter as CsvImporter
from .base_importer import JsonImporter as JsonImporter

cash_file = FilesTuple(name="barkasse", file_prefix="barkasse")
payment_file = FilesTuple(name="payment", file_prefix="journal")
person_file = FilesTuple(name="person", file_prefix="mitglieder")
name_mapping_file = FilesTuple(name="name_mapping", file_prefix="name_mapping")
categorie_file = FilesTuple(name="categorie", file_prefix="categorie")
budget_file = FilesTuple(name="budget", file_prefix="budgets")
skr_file = FilesTuple(name="skr", file_prefix="skr49")
