from django.db.models import (
    CASCADE,
    CharField,
    DateField,
    FloatField,
    ForeignKey,
    Model,
)

from cashviz.models.person import Person

# modell represents changes in fee and support change


class BillingChanges(Model):
    type = CharField(max_length=15)
    date = DateField(default=None, null=True)
    amount = FloatField(default=0.0)
    person = ForeignKey(Person, on_delete=CASCADE, default=None)

    def __str__(self) -> str:
        return str(self.person.name)
