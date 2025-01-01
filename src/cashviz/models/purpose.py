from django.db.models import CharField, Model


class Purpose(Model):
    name = CharField(
        max_length=30, verbose_name="Purpose Name", default="undefined", unique=True
    )

    def __str__(self) -> str:
        return self.name
