# Generated by Django 2.1.1 on 2018-10-03 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snack_puzzle', '0008_auto_20181003_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='amount',
            field=models.FloatField(verbose_name='Ilość'),
        ),
    ]