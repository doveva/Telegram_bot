from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from telegramDB.api.serializers import CitiesSerializer
from telegramDB.api.models import MoscowCities


class CitiesCreateListAPIView(generics.ListCreateAPIView):
    serializer_class = CitiesSerializer

    def get_queryset(self):
        name = self.request.query_params.get("name")
        queryset = MoscowCities.objects.filter(city_name__icontains=name)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.queryset.delete()
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)

