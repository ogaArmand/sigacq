# Generated by Django 4.1.8 on 2024-10-11 15:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_pisciculture', '0006_especepoisson_indice_conversion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mortalite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mortalite', models.FloatField(null=True)),
                ('date_mortalite', models.DateField()),
                ('poisson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_pisciculture.poisson')),
            ],
        ),
        migrations.CreateModel(
            name='alimentation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ration_recommande', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_pisciculture.rationalimentaire')),
            ],
        ),
    ]
