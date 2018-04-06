# Generated by Django 2.0.2 on 2018-04-06 15:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_auto_20180322_1736'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='slug',
            field=models.SlugField(default='slug'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='position',
            name='project',
            field=models.ForeignKey(default=12, on_delete=django.db.models.deletion.CASCADE, to='projects.Project'),
            preserve_default=False,
        ),
    ]
