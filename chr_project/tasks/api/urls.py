from django.urls import path

from .views import (ListBikesSantiago, CreateBikesSantiago)

urlpatterns = [
    path('task1/bikes_santiago/', ListBikesSantiago.as_view(), name='list_bikes_santiago'),
    path('task1/bikes_santiago_create/', CreateBikesSantiago.as_view(), name='create_bikes_santiago'),
]