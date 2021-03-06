# Generated by Django 2.1.1 on 2018-10-03 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snack_puzzle', '0006_auto_20181003_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='measure',
            field=models.CharField(choices=[('g', 'gram'),
                                            ('dag', 'dekagram'),
                                            ('szt.', 'szt.'),
                                            ('szklan.', 'szklanka'),
                                            ('łyż.', 'łyżka'),
                                            ('łyżecz.', 'łyżeczka'),
                                            ('szczypta', 'szczypta'),
                                            ('pęczek', 'pęczek'),
                                            ('opak.', 'opak.'),
                                            ('l.', 'l.')],
                                   default='dag',
                                   max_length=32,
                                   null=True,
                                   verbose_name='Miara'),
        ),
    ]
