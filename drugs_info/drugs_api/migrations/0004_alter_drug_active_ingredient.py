# Generated by Django 4.0.5 on 2022-07-01 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drugs_api', '0003_remove_drug_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drug',
            name='active_ingredient',
            field=models.CharField(max_length=1024, verbose_name='Действующее вещество'),
        ),
    ]