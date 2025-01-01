from django.db.models import CharField, Model


# also know as AG or Kollektiv
class Groups(Model):
    name = CharField(max_length=30, verbose_name="Group Name", unique=True)

    def __str__(self) -> str:
        return self.name
