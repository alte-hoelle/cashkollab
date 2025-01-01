from dataclasses import dataclass

from overrides import overrides

from cashviz.importer import CsvImporter
from cashviz.models.category import Category


# pylint: disable=too-many-instance-attributes
@dataclass
class CSVCategorieDataclass:
    identifier: str
    name: str

    def __post_init__(self) -> None:
        if self.identifier == "":
            self.identifier = "undefined"
        self.name = self.name.replace("\n", "")
        if self.name == "":
            self.name = "undefined"


class CategorieImporter(CsvImporter):
    @overrides
    def _import(self) -> None:
        # pylint: disable=no-member
        for line in self.lines:
            categoriedata = CSVCategorieDataclass(*line.split(";"))
            categorie, created = Category.objects.get_or_create(
                identifier=categoriedata.identifier,
                defaults={"name": categoriedata.name},
            )
            if created:
                print(f"Adding new Category({categorie.identifier=} {categorie.name=})")
