# Generated by Django 3.0.4 on 2021-07-02 11:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bundle_id', models.CharField(blank=True, max_length=256, null=True)),
                ('app_name', models.CharField(blank=True, max_length=512, null=True)),
                ('description', models.CharField(blank=True, max_length=512, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='VersionApp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_ipa', models.FileField(blank=True, null=True, upload_to='files/')),
                ('file_plist', models.FileField(blank=True, null=True, upload_to='file_plist/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.Application')),
            ],
        ),
    ]
