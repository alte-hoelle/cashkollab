from django.db.models import CASCADE, DateField, FloatField, ForeignKey, Model, URLField

from cashviz.models.groups import Groups
from cashviz.models.purpose import Purpose


class Budget(Model):
    purpose = ForeignKey(Purpose, on_delete=CASCADE, default=None)
    group = ForeignKey(Groups, on_delete=CASCADE, default=None)
    amount = FloatField()
    decided_date = DateField()
    expire_date = DateField()
    url = URLField(max_length=200)

    def __str__(self) -> str:
        return str(self.purpose.name)
