# Generated by Django 4.1.1 on 2022-10-16 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='categorie',
            field=models.CharField(blank=True, max_length=50, verbose_name='Catégorie'),
        ),
    ]
