# Generated by Django 2.1.1 on 2018-10-20 13:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('snack_puzzle', '0014_auto_20181020_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='ingredient',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='snack_puzzle.Ingredient',
                verbose_name='Składnik'
            ),
        ),
    ]
