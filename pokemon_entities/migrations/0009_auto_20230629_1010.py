# Generated by Django 3.1.14 on 2023-06-29 07:10
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0008_auto_20230629_0934'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pokemonentity',
            name='pokemon',
        ),
        migrations.AddField(
            model_name='pokemonentity',
            name='main_pokemon',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pokemon', to='pokemon_entities.pokemon', verbose_name='покемон'),
        ),
    ]
