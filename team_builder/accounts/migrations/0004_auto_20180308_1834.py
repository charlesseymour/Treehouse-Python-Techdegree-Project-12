# Generated by Django 2.0.2 on 2018-03-09 00:34

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20180303_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=accounts.models.user_directory_path),
        ),
    ]
