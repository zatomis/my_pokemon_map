from django.db import models  # noqa F401


class PokemonEntity(models.Model):
    lon = models.FloatField(blank=False)
    lat = models.FloatField(blank=False)

    def __str__(self):
        return f'координаты {self.lon} {self.lat}'


class Pokemon(models.Model):
    title = models.TextField()
    photo = models.ImageField(blank=True)
    coordinats = models.ForeignKey(PokemonEntity, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.title}'