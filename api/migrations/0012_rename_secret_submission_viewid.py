# Generated by Django 5.0.7 on 2024-07-16 07:54

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0011_remove_problem_compileflags_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="submission",
            old_name="secret",
            new_name="viewId",
        ),
    ]
