from django.db import models  # noqa F401
from datetime import datetime
import random


class PokemonEntity(models.Model):
    lon = models.FloatField(blank=False)
    lat = models.FloatField(blank=False)

    def __str__(self):
        return f'координаты {self.lon} {self.lat}'

class PokemonGeneration(models.Model):
    pokemon_id = models.IntegerField(default=0, blank=True)
    title_pg = models.TextField(blank=True, default="Покемон")
    photo_pg = models.ImageField(blank=True, default="")

    def __str__(self):
        return f' {self.title} {self.photo}'


class Pokemon(models.Model):
    title = models.TextField()
    title_en = models.TextField(default="EN")
    title_jp = models.TextField(default="JP")
    photo = models.ImageField(blank=True)
    # next_evolution = models.ForeignKey(PokemonGeneration, on_delete=models.CASCADE, related_name='next')
    next_evolution = models.ForeignKey("self", on_delete=models.CASCADE, related_name='next', null=True, blank=True)
    previous_evolution = models.ForeignKey("self", on_delete=models.CASCADE, related_name='previous', null=True, blank=True)
    coordinats = models.ForeignKey(PokemonEntity, on_delete=models.CASCADE)
    description = models.TextField(default="Покемон")
    appeared_at = models.DateTimeField(help_text="появится",default=datetime.now())
    disappeared_at = models.DateTimeField(help_text="пропадет",default=datetime.now())
    level = models.IntegerField(help_text="уровень", default=random.randint(5,10))
    health = models.IntegerField(help_text="здоровье", default=random.randint(5,10))
    attack = models.IntegerField(help_text="атака", default=random.randint(5,10))
    defense = models.IntegerField(help_text="защита", default=random.randint(5,10))
    stamina = models.IntegerField(help_text="выносливость", default=random.randint(5,10))

    def __str__(self):
        return f'{self.title}'