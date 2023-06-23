from django.db import models  # noqa F401


class PokemonEntity(models.Model):
    lon = models.FloatField(blank=False, verbose_name='долгота')
    lat = models.FloatField(blank=False, verbose_name='широта')
    description = models.TextField(default="Покемон", verbose_name='детальное описание покемона')
    appeared_at = models.DateTimeField(help_text="появится", verbose_name='время появления покемона')
    disappeared_at = models.DateTimeField(help_text="пропадет", verbose_name='время исчезновения покемона')
    level = models.IntegerField(help_text="уровень", verbose_name='уровень развития покемона')
    health = models.IntegerField(help_text="здоровье", verbose_name='уровень здоровья покемона')
    attack = models.IntegerField(help_text="атака", verbose_name='атака покемона')
    defense = models.IntegerField(help_text="защита", verbose_name='защита покемона')
    stamina = models.IntegerField(help_text="выносливость", verbose_name='выносливость покемона')


    def __str__(self):
        return f'{self.description} {self.lon} {self.lat}'


class Pokemon(models.Model):
    title = models.TextField(verbose_name='наименование пакемона', blank=False)
    title_en = models.TextField(blank=True, verbose_name='наименование пакемона на английском')
    title_jp = models.TextField(blank=True, verbose_name='наименование пакемона на японском')
    photo = models.ImageField(blank=True, verbose_name='изображение пакемона')
    pokemon_entities = models.ForeignKey(PokemonEntity, on_delete=models.CASCADE, related_name='pokemon', verbose_name='сущность')

    def __str__(self):
        return self.title