# Generated by Django 2.0.2 on 2018-04-08 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0009_auto_20180407_1658'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='slug',
            field=models.SlugField(default='slug'),
            preserve_default=False,
        ),
    ]