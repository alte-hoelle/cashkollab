from django.contrib import admin
from django.shortcuts import get_object_or_404, redirect
from django.urls import URLPattern, path

from cashviz.models.account import Account
from cashviz.models.billing_changes import BillingChanges
from cashviz.models.budget import Budget
from cashviz.models.category import Category
from cashviz.models.groups import Groups
from cashviz.models.journal_entry import JournalEntry
from cashviz.models.name_mapping import NameMapping
from cashviz.models.person import Person
from cashviz.models.purpose import Purpose
from cashviz.models.skr import SkrAccount, SkrCategory


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("name", "is_member", "is_supporter")
    search_fields = ["name"]
    search_help_text = "search for name"
    list_filter = ("is_member", "is_supporter")

    # def _remove_from_list(self, field_list: list, name: str):  # type: ignore[no-untyped-def, type-arg]
    #    if name in field_list:
    #        field_list.remove(name)

    def get_fields(self, request, obj: Person | None = None):  # type: ignore[no-untyped-def]
        fields = super().get_fields(request)
        fields_list = list(fields)
        # if obj:
        #    if not obj.is_supporter:
        #        self._remove_from_list(fields_list, 'supporter_since')
        #        self._remove_from_list(fields_list, 'not_supporter_since')
        #    if not obj.is_member:
        #        self._remove_from_list(fields_list, 'member_since')
        #        self._remove_from_list(fields_list, 'not_member_since')
        fields_tuple = tuple(fields_list)
        return fields_tuple


@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ("short_recipient", "short_comment", "set_purpose", "amount")
    search_fields = ["recipient__name", "comment"]
    search_help_text = "search in recipient and comment"
    list_filter = ("purpose__name",)

    def get_urls(self) -> list[URLPattern]:
        urls = super().get_urls()
        my_urls = [
            path(
                "set_purpose/<int:pk>/<str:purpose>/",
                self.set_purpose_callback,
                name="admin_payment_set_purpose",
            ),
        ]
        return my_urls + urls

    # just rename it
    # pylint: disable=no-self-use
    def amount(self, obj: JournalEntry) -> str:
        return str(obj.signed)

    # pylint: disable=no-self-use
    def set_purpose_callback(self, request, pk, purpose):  # type: ignore[no-untyped-def]
        target = get_object_or_404(JournalEntry, pk=pk)
        # pylint: disable=no-member
        target.purpose = Purpose.objects.filter(name=purpose).first()
        target.save()
        return redirect(request.META.get("HTTP_REFERER"))


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ("get_purpose_name", "amount", "decided_date", "expire_date")

    # pylint: disable=no-self-use
    def get_purpose_name(self, obj: Budget) -> str:
        return str(obj.purpose.name)

    get_purpose_name.short_description = "Purpose"  # type: ignore[attr-defined]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "identifier")


@admin.register(Purpose)
class PurposeAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(BillingChanges)
class BillingPeriodAdmin(admin.ModelAdmin):
    list_display = ("type", "date", "amount")


@admin.register(NameMapping)
class NameMappingAdmin(admin.ModelAdmin):
    list_display = ("name", "clean_name")


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("IBAN", "BIC", "bank_name", "comment")


@admin.register(Groups)
class GroupsAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(SkrCategory)
class SkrCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "codes",
        "text",
    )


@admin.register(SkrAccount)
class SkrAccountAdmin(admin.ModelAdmin):
    list_display = ("code", "type", "name", "is_account", "is_class", "is_category")
