from django.db import models


class Pokemon(models.Model):
    title = models.CharField(verbose_name='имя', max_length=200)
    title_en = models.CharField(verbose_name='имя на английском', max_length=200, blank=True)
    title_jp = models.CharField(verbose_name='имя на японском', max_length=200, blank=True)
    description = models.TextField(verbose_name='описание покемона', blank=True)
    image = models.ImageField(verbose_name='картинка', null=True, blank=True)
    previous_evolution = models.ForeignKey(
        'self',
        verbose_name='Из кого эволюционирует',
        null=True,
        blank=True,
        related_name='next_evolutions',
        on_delete=models.SET_NULL,
    )


    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    subject = models.ForeignKey(Pokemon, verbose_name='покемон', on_delete=models.CASCADE, related_name='entities')
    lat = models.FloatField(verbose_name='широта')
    lon = models.FloatField(verbose_name='долгота')
    appeared_at = models.DateTimeField(verbose_name='появление', null=True, blank=True)
    disappeared_at = models.DateTimeField(verbose_name='исчезновение', null=True, blank=True)
    level = models.IntegerField(verbose_name='уровень', null=True, blank=True)
    health = models.IntegerField(verbose_name='здоровье', null=True, blank=True)
    strength = models.IntegerField(verbose_name='сила', null=True, blank=True)
    defence = models.IntegerField(verbose_name='защита', null=True, blank=True)
    stamina = models.IntegerField(verbose_name='выносливость', null=True, blank=True)
