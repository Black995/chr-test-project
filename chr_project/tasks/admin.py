from django.contrib import admin
from . import models

admin.site.register(models.Extra)
admin.site.register(models.Station)
admin.site.register(models.Location)
admin.site.register(models.Network)