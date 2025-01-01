from dataclasses import dataclass

from overrides import overrides

from cashviz.importer import CsvImporter

# pylint: disable=too-many-instance-attributes
from cashviz.models.name_mapping import NameMapping


@dataclass
class CSVNameMappingDataclass:
    name: str
    clean_name: str

    def __post_init__(self) -> None:
        self.clean_name = self.clean_name.replace("\n", "")


class NameMappingImporter(CsvImporter):
    @overrides
    def _import(self) -> None:
        # pylint: disable=no-member

        for line in self.lines:
            mappingdata = CSVNameMappingDataclass(*line.split(";"))
            mapping, created = NameMapping.objects.get_or_create(
                clean_name=mappingdata.clean_name, name=mappingdata.name
            )
            if created and self.verbose:
                print(
                    f"Adding new NameMapping({mapping.clean_name=} = {mapping.name=})"
                )
