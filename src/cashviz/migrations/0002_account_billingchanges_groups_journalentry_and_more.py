# Generated by Django 4.0.6 on 2023-11-28 21:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cashviz", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Account",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("IBAN", models.CharField(max_length=40)),
                ("BIC", models.CharField(max_length=15)),
                (
                    "comment",
                    models.CharField(
                        default="", max_length=30, verbose_name="Account Comment"
                    ),
                ),
                ("bank_name", models.CharField(default="", max_length=40)),
                ("cash_account", models.BooleanField(default=False)),
                ("active", models.BooleanField(default=True)),
            ],
            options={
                "unique_together": {("IBAN", "BIC")},
            },
        ),
        migrations.CreateModel(
            name="BillingChanges",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("type", models.CharField(max_length=15)),
                ("date", models.DateField(default=None, null=True)),
                ("amount", models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name="Groups",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=30, unique=True, verbose_name="Group Name"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="JournalEntry",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                ("valuta", models.DateField()),
                ("textkey", models.CharField(max_length=30)),
                ("comment", models.CharField(max_length=100)),
                ("currency", models.CharField(max_length=30)),
                ("signed", models.FloatField(max_length=30, verbose_name="amount")),
                ("taxes", models.IntegerField(default=0)),
                (
                    "account",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="account",
                        to="cashviz.account",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="NameMapping",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=40)),
                ("clean_name", models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name="SkrAccount",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "skr_id",
                    models.CharField(
                        max_length=32, verbose_name="skr account id from gnucash"
                    ),
                ),
                (
                    "parent_skr_id",
                    models.CharField(max_length=32, verbose_name="parent skr account"),
                ),
                ("name", models.CharField(max_length=100)),
                ("type", models.CharField(max_length=100)),
                ("code", models.CharField(max_length=100)),
                ("sort_code", models.CharField(max_length=100)),
                ("description", models.CharField(max_length=100)),
                ("leaf", models.CharField(max_length=100)),
                ("notes", models.CharField(max_length=100)),
                ("placeholder", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="SkrCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("codes", models.CharField(default="", max_length=50)),
                ("text", models.CharField(max_length=500)),
            ],
        ),
        migrations.RemoveField(
            model_name="person",
            name="BIC",
        ),
        migrations.RemoveField(
            model_name="person",
            name="IBAN",
        ),
        migrations.AddField(
            model_name="person",
            name="comment",
            field=models.TextField(default=""),
        ),
        migrations.AddField(
            model_name="person",
            name="membership_fee",
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField(max_length=30, verbose_name="Category Name"),
        ),
        migrations.AlterField(
            model_name="person",
            name="member_since",
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name="person",
            name="name",
            field=models.CharField(max_length=100, verbose_name="Person Name"),
        ),
        migrations.AlterField(
            model_name="person",
            name="not_member_since",
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name="person",
            name="not_supporter_since",
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name="person",
            name="supporter_since",
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name="purpose",
            name="name",
            field=models.CharField(
                default="undefined",
                max_length=30,
                unique=True,
                verbose_name="Purpose Name",
            ),
        ),
        migrations.DeleteModel(
            name="Payment",
        ),
        migrations.AddField(
            model_name="skraccount",
            name="categories",
            field=models.ManyToManyField(to="cashviz.skrcategory"),
        ),
        migrations.AddField(
            model_name="journalentry",
            name="category",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="cashviz.category",
            ),
        ),
        migrations.AddField(
            model_name="journalentry",
            name="purpose",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="cashviz.purpose",
            ),
        ),
        migrations.AddField(
            model_name="journalentry",
            name="recipient",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="cashviz.person",
            ),
        ),
        migrations.AddField(
            model_name="journalentry",
            name="recipient_account",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="recipient_account",
                to="cashviz.account",
            ),
        ),
        migrations.AddField(
            model_name="billingchanges",
            name="person",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="cashviz.person",
            ),
        ),
        migrations.AddField(
            model_name="budget",
            name="group",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="cashviz.groups",
            ),
        ),
        migrations.AddField(
            model_name="person",
            name="account",
            field=models.ManyToManyField(to="cashviz.account"),
        ),
    ]
