# Generated by Django 3.1.5 on 2021-01-09 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kassa', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='author_name',
            field=models.CharField(default='None', max_length=255, verbose_name='Автор'),
        ),
    ]
