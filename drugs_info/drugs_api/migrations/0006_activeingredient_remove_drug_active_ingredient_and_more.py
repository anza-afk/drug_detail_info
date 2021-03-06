# Generated by Django 4.0.5 on 2022-07-04 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drugs_api', '0005_alter_drug_active_ingredient'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActiveIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=256, unique=True, verbose_name='Наименование')),
            ],
        ),
        migrations.RemoveField(
            model_name='drug',
            name='active_ingredient',
        ),
        migrations.AddField(
            model_name='drug',
            name='active_ingredient',
            field=models.ManyToManyField(to='drugs_api.activeingredient', verbose_name='Действующее вещество'),
        ),
    ]
