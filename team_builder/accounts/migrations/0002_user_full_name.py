# Generated by Django 2.0.2 on 2018-03-02 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='full_name',
            field=models.CharField(default='', max_length=51, null=''),
            preserve_default=False,
        ),
    ]
