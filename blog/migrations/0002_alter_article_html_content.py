# Generated by Django 4.1.2 on 2022-10-29 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="article",
            name="html_content",
            field=models.TextField(blank=True, null=True),
        ),
    ]
