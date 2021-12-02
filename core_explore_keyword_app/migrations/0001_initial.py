# Generated by Django 3.2 on 2021-10-08 20:54

from django.db import migrations, models

import core_explore_keyword_app.components.search_operator.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("core_main_app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ExploreKeyword",
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
            ],
            options={
                "verbose_name": "core_explore_keyword_app",
                "permissions": (
                    ("access_explore_keyword", "Can access explore keyword"),
                ),
                "default_permissions": (),
            },
        ),
        migrations.CreateModel(
            name="SearchOperator",
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
                        max_length=200,
                        unique=True,
                        validators=[
                            core_explore_keyword_app.components.search_operator.models.validate_name
                        ],
                    ),
                ),
                (
                    "xpath_list",
                    models.JSONField(
                        unique=True,
                        validators=[
                            core_explore_keyword_app.components.search_operator.models.validate_xpath_list
                        ],
                    ),
                ),
                ("dot_notation_list", models.JSONField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="PersistentQueryKeyword",
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
                ("user_id", models.CharField(max_length=200)),
                ("content", models.TextField(blank=True, null=True)),
                ("data_sources", models.JSONField(blank=True, default=list)),
                ("creation_date", models.DateTimeField(auto_now_add=True)),
                (
                    "name",
                    models.CharField(
                        blank=True, max_length=200, null=True, unique=True
                    ),
                ),
                (
                    "templates",
                    models.ManyToManyField(
                        blank=True, default=[], to="core_main_app.Template"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
