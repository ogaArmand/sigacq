# Generated by Django 4.1.8 on 2024-11-26 22:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_pisciculture', '0015_bande_poisson_bande'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bande',
            old_name='taux_mortalite',
            new_name='mortalite',
        ),
    ]
