from overrides import overrides

from cashviz.importer.importer import JsonImporter
from cashviz.models.skr import SkrAccount, SkrCategory


class SkrImporter(JsonImporter):
    @overrides
    def _import(self) -> None:
        # pylint: disable=no-member
        for obj in self.objects:
            categories = []
            for cat in obj["categories"]:
                splitted_cat = str(cat).split(" ")
                skr_category, created = SkrCategory.objects.get_or_create(
                    codes=splitted_cat[0], defaults={"text": " ".join(splitted_cat[1:])}
                )
                categories.append(skr_category)
            parent = obj["parent"] if "parent" in obj else ""
            sort_code = obj["sort_code"] if "sort_code" in obj else ""
            notes = obj["notes"] if "notes" in obj else ""
            placeholder = obj["placeholder"] if "placeholder" in obj else ""
            try:
                skr_account, created = SkrAccount.objects.get_or_create(
                    skr_id=obj["id"],
                    defaults={
                        "parent_skr_id": parent,
                        "name": obj["name"],
                        "type": obj["type"],
                        "code": obj["code"],
                        "sort_code": sort_code,
                        "description": obj["description"],
                        "leaf": obj["leaf"],
                        "notes": notes,
                        "placeholder": placeholder,
                    },
                )
                skr_account.categories.set(categories)
                if created and self.verbose:
                    print(
                        f"Adding new Skr Account({skr_account.id=} {skr_account.name=})"
                    )
            except Exception as e:
                print(e)
