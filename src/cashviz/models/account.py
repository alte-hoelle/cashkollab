from django.db.models import BooleanField, CharField, Model


class Account(Model):
    IBAN = CharField(max_length=40)
    BIC = CharField(max_length=15)
    comment = CharField(max_length=30, verbose_name="Account Comment", default="")
    bank_name = CharField(max_length=40, default="")
    cash_account = BooleanField(default=False)
    active = BooleanField(default=True)

    class Meta:
        unique_together = ("IBAN", "BIC")

    def __str__(self) -> str:
        return self.comment
