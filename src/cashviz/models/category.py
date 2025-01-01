from typing import Iterable

from django.db.models import CharField, Model


class Category(Model):
    name = CharField(max_length=30, verbose_name="Category Name")
    identifier = CharField(max_length=2)

    def save(
        self,
        force_insert: bool = False,
        force_update: bool = False,
        using: str | None = None,
        update_fields: Iterable[str] | None = None,
    ) -> None:
        if self.name == "":
            self.name = "undefined"
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self) -> str:
        return self.name
