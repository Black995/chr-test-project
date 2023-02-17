from django.urls import path

from .views import (ListBikesSantiago, CreateBikesSantiago, ListSeiaSeaGob)

urlpatterns = [
    #Task 1
    path('task1/bikes_santiago/', ListBikesSantiago.as_view(), name='list_bikes_santiago'),
    path('task1/bikes_santiago_create/', CreateBikesSantiago.as_view(), name='create_bikes_santiago'),
    # Task 2
    path('task2/seia_sea/', ListSeiaSeaGob.as_view(), name='list_seia_sea'),
]