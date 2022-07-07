from django.db import models


class MoscowCities(models.Model):
    city_name = models.CharField(max_length=30)
    city_url = models.CharField(max_length=255)
    city_population = models.IntegerField()

    def __str__(self):
        return self.city_name
