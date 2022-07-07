from rest_framework.serializers import ModelSerializer
from telegramDB.api.models import MoscowCities


class CitiesSerializer(ModelSerializer):
    class Meta:
        model = MoscowCities
        fields = [
            "city_name",
            "city_url",
            "city_population"
        ]


