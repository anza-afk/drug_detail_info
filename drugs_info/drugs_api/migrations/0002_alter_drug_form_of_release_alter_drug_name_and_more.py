# Generated by Django 4.0.6 on 2022-10-31 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drugs_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drug',
            name='form_of_release',
            field=models.CharField(max_length=2048, null=True, verbose_name='Лекарственная форма'),
        ),
        migrations.AlterField(
            model_name='drug',
            name='name',
            field=models.CharField(db_index=True, max_length=1024, unique=True, verbose_name='Наименование'),
        ),
        migrations.AlterField(
            model_name='drug',
            name='pharmacological_class',
            field=models.CharField(max_length=2048, null=True, verbose_name='Фармакологическая группа'),
        ),
        migrations.AlterField(
            model_name='drug',
            name='recipe_only',
            field=models.BooleanField(default=None, null=True, verbose_name='Требуется рецепт'),
        ),
    ]
