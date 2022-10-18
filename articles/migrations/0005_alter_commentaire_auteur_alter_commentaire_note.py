# Generated by Django 4.1.1 on 2022-10-18 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_commentaire_auteur'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentaire',
            name='auteur',
            field=models.CharField(blank=True, max_length=250, verbose_name='Auteur'),
        ),
        migrations.AlterField(
            model_name='commentaire',
            name='note',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=1, null=True, verbose_name='Note'),
        ),
    ]
