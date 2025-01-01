from django.db.models import CharField, ManyToManyField, Model


class SkrCategory(Model):
    codes = CharField(max_length=50, default="")
    text = CharField(max_length=500)

    def __str__(self) -> str:
        return self.text


class SkrAccount(Model):
    skr_id = CharField(max_length=32, verbose_name="skr account id from gnucash")
    parent_skr_id = CharField(max_length=32, verbose_name="parent skr account")
    name = CharField(max_length=100)
    type = CharField(max_length=100)
    code = CharField(max_length=100)
    sort_code = CharField(max_length=100)
    description = CharField(max_length=100)
    categories = ManyToManyField(SkrCategory)
    leaf = CharField(max_length=100)
    notes = CharField(max_length=100)
    placeholder = CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

    def code_class(self) -> int:
        return int(self.code[0])

    def is_account(self) -> bool:
        return len(self.code) == 4 and not self.is_class() and not self.is_category()

    def is_category(self) -> bool:
        return len(self.code) == 4 and self.code[2:] == "00"

    def is_class(self) -> bool:
        return len(self.code) == 1
