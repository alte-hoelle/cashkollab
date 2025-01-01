# Generated by Django 4.0.5 on 2022-07-04 16:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cashviz", "0001_initial"),
        ("hellusers", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="helluser",
            name="person",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="cashviz.person",
            ),
        ),
    ]
