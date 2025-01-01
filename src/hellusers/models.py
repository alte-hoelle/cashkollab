from django.contrib.auth.models import AbstractUser
from django.db.models import SET_NULL, ForeignKey

from cashviz.models.person import Person


class HellUser(AbstractUser):
    person = ForeignKey(Person, on_delete=SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
