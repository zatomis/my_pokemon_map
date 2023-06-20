from django.db import models  # noqa F401
from datetime import datetime
import random


class PokemonEntity(models.Model):
    lon = models.FloatField(blank=False, verbose_name='долгота')
    lat = models.FloatField(blank=False, verbose_name='широта')

    def __str__(self):
        return f'координаты {self.lon} {self.lat}'


class Pokemon(models.Model):
    title = models.TextField(verbose_name='наименование пакемона', blank=False)
    title_en = models.TextField(verbose_name='наименование пакемона на английском')
    title_jp = models.TextField(verbose_name='наименование пакемона на японском')
    photo = models.ImageField(blank=True, verbose_name='изображение пакемона')
    next_evolution = models.ForeignKey("self", on_delete=models.CASCADE, related_name='next', null=True, blank=True, verbose_name='потомок покемона')
    previous_evolution = models.ForeignKey("self", on_delete=models.CASCADE, related_name='previous', null=True, blank=True, verbose_name='предок покемона')
    coordinats = models.ForeignKey(PokemonEntity, on_delete=models.CASCADE, verbose_name='координаты на карте', blank=False)
    description = models.TextField(default="Покемон", verbose_name='детальное описание покемона')
    appeared_at = models.DateTimeField(help_text="появится", blank=False, verbose_name='время появления покемона',blank=False)
    disappeared_at = models.DateTimeField(help_text="пропадет", blank=False, verbose_name='время исчезновения покемона',blank=False)
    level = models.IntegerField(help_text="уровень", blank=False, verbose_name='уровень развития покемона')
    health = models.IntegerField(help_text="здоровье", blank=False, verbose_name='уровень здоровья покемона')
    attack = models.IntegerField(help_text="атака", blank=False, verbose_name='атака покемона')
    defense = models.IntegerField(help_text="защита", blank=False, verbose_name='защита покемона')
    stamina = models.IntegerField(help_text="выносливость", blank=False, verbose_name='выносливость покемона')

    def __str__(self):
        return self.title