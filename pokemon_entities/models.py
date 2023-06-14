from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.TextField()
    photo = models.ImageField(blank=True)

    def __str__(self):
        return f'{self.title}'