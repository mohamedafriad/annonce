# Generated by Django 4.1.2 on 2022-10-17 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_commentaire'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentaire',
            name='auteur',
            field=models.CharField(default='mohamed', max_length=250, verbose_name='Auteur'),
            preserve_default=False,
        ),
    ]