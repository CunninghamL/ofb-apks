# Generated by Django 3.0.4 on 2021-07-07 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0002_auto_20210707_0426'),
    ]

    operations = [
        migrations.AddField(
            model_name='versionapp',
            name='version_name',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
