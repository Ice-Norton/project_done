# Generated by Django 5.1.2 on 2025-03-05 10:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="candidateprofile",
            name="cv",
            field=models.FileField(default=False, upload_to="resume/"),
        ),
        migrations.AddField(
            model_name="candidateprofile",
            name="resume",
            field=models.TextField(default=False),
        ),
    ]
