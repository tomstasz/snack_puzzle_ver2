# Generated by Django 2.1.1 on 2018-10-03 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snack_puzzle', '0003_auto_20181002_2229'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='type',
            name='ingredient',
        ),
        migrations.AddField(
            model_name='ingredientrecipe',
            name='measure',
            field=models.CharField(choices=[('gram', 'g'),
                                            ('dekagram', 'dag'),
                                            ('sztuka', 'szt.'),
                                            ('szklanka', 'szklanka'),
                                            ('łyżka', 'łyżka'),
                                            ('łyżeczka', 'łyżeczka'),
                                            ('szczypta', 'szczypta'),
                                            ('pęczek', 'pęczek'),
                                            ('opakowanie', 'opak.')],
                                   default='dag',
                                   max_length=32,
                                   verbose_name='Miara'),
        ),
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='amount',
            field=models.IntegerField(verbose_name='Ilość'),
        ),
        migrations.DeleteModel(
            name='Type',
        ),
    ]
