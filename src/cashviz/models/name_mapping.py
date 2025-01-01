from django.db.models import CharField, Model


class NameMapping(Model):
    name = CharField(max_length=40)
    clean_name = CharField(max_length=15)

    def __str__(self) -> str:
        return self.name
