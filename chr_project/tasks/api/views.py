from datetime import datetime, date
import urllib3
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select #este lo estoy probando

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from rest_framework.generics import (ListAPIView, ListCreateAPIView)
from tasks.models import Network, Location, Station, Extra
from .serializers import (LocationSerializer, NetworkSerializer, StationSerializer, ExtraSerializer, SeiaSeaSerializer)




"""
    Vista para prueba de acceso a la API de citybik
"""
class ListBikesSantiago(ListAPIView):
    model = Network
    queryset = Network.objects.all()

    def get(self, request):
        http = urllib3.PoolManager()
        url = 'http://api.citybik.es/v2/networks/bikesantiago'
        resp = http.request('GET', url)

        return Response(data=json.loads(resp.data))

"""
    Registro de la información de la API en la BD
"""
class CreateBikesSantiago(ListCreateAPIView):
    model = Network
    queryset = Network.objects.all()

    def create(self, request):
        http = urllib3.PoolManager()
        url = 'http://api.citybik.es/v2/networks/bikesantiago'
        data_string = http.request('GET', url)
        data=json.loads(data_string.data)

        location = {
            "city": data['network']['location']['city'],
            "country": data['network']['location']['country'],
            "latitude": data['network']['location']['latitude'],
            "longitude": data['network']['location']['longitude'],
        }

        # Buscamos si ya fue registrada esta localización
        try:
            loc = Location.objects.filter(city=location['city'], country=location['country']).first()
        except Location.DoesNotExist:
            loc = None

        # Si no está registrada entonces se registra
        if(not loc):
            serializer_location = LocationSerializer(data=location)
            serializer_location.is_valid(raise_exception=True)
            loc = serializer_location.save()

        network = {
            "id": data['network']['id'],
            "name": data['network']['name'],
            "href": data['network']['href'],
            "gbfs_href": data['network']['gbfs_href'],
            "company": data['network']['company']
        }

        # Buscamos si ya fue registrada esta red
        try:
            net = Network.objects.get(id=network['id'])
        except Network.DoesNotExist:
            net = None

        if(not net):
            serializer_network = NetworkSerializer(data=network)
            serializer_network.is_valid(raise_exception=True)
            net = serializer_network.save(location=loc)

        # iteramos entre todas las estaciones
        for s in data['network']['stations']:
            
            extra = {
                "uid": s['extra']['uid'],
                "address": s['extra']['address'],
                "altitude": s['extra']['altitude'],
                "ebikes": s['extra']['ebikes'],
                "has_ebikes": s['extra']['has_ebikes'],
                "last_updated": s['extra']['last_updated'],
                "normal_bikes": s['extra']['normal_bikes'],
                "payment": s['extra']['payment'],
                "payment_terminal": s['extra']['payment-terminal'],
                "post_code": s['extra']['post_code'] if 'post_code' in s['extra'] else None,
                "renting": s['extra']['renting'],
                "returning": s['extra']['returning'],
                "slots": s['extra']['slots'],
            }

            # Buscamos si ya fue registrada la información extra
            try:
                ex = Extra.objects.get(uid=extra['uid'])
            except Extra.DoesNotExist:
                ex = None

            if(not ex):
                serializer_extra = ExtraSerializer(data=extra)
                serializer_extra.is_valid(raise_exception=True)
                ex = serializer_extra.save()

            station = {
                "id": s['id'],
                "free_bikes": s['free_bikes'],
                "latitude": s['latitude'],
                "longitude": s['longitude'],
                "name": s['name'],
                "timestamp": s['timestamp'],
                "empty_slots": s['empty_slots'],
                "network": net.id
            }
            
            # Buscamos si ya fue registrada la estación
            try:
                st = Station.objects.get(id=station['id'])
            except Station.DoesNotExist:
                st = None
                
            if(not st):
                serializer_station = StationSerializer(data=station)
                serializer_station.is_valid(raise_exception=True)
                st = serializer_station.save(station_extra=ex)

        return Response({"mensaje": "data saved successfully."})


# receive the date directly from the scrapper and transforms it to a format compatible for the db.
def format_date_to_db(unformatted_date):
    if '-' in unformatted_date:
        complete_date = unformatted_date.split('-')
    elif '/' in unformatted_date:
        complete_date = unformatted_date.split('/')
    date_day, date_month, date_year = int(complete_date[0]), int(complete_date[1]), int(complete_date[2])
    return date(date_year, date_month, date_day)


"""
    Vista para prueba de acceso al portal seia.sea.gob
"""
class ListSeiaSeaGob(ListCreateAPIView):
    model = Network
    queryset = Network.objects.all()

    def create(self, request):

        # En primer lugar, accedemos a la página para obtener los valores de la paginación
        chrome_driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        chrome_driver.get('https://seia.sea.gob.cl/busqueda/buscarProyectoAction.php')
        xpath_select = f"//select[@name='pagina_offset']"
        select = Select(chrome_driver.find_element(By.XPATH, xpath_select))

        xpath_table = f"//table[@class='tabla_datos']"
        table = []
        for index in range(len(select.options)):

            # Seleccionado elemento del select
            WebDriverWait(chrome_driver, 15).until(ec.visibility_of_element_located((By.XPATH, xpath_select)))
            select = Select(chrome_driver.find_element(By.XPATH, xpath_select))
            select.select_by_index(index)

            # Obtenemos la tabla para iterar sobre sus datos
            WebDriverWait(chrome_driver, 15).until(ec.visibility_of_element_located((By.XPATH, xpath_table)))
            current_table = chrome_driver.find_element(By.XPATH, xpath_table)
            rows = current_table.find_elements(By.TAG_NAME, 'tr')

            for row in rows: 
                col = row.find_elements(By.TAG_NAME,'td')            
                if(len(col) > 1):
                    seia = {
                        "nombre": col[1].text,
                        "tipo": col[2].text,
                        "region": col[3].text,
                        "tipologia": col[4].text,
                        "titular": col[5].text,
                        "inversion": float(col[6].text.replace(',', '.').replace('.', '')),
                        "fecha_ingreso": format_date_to_db(col[7].text),
                        "estado": col[8].text
                    }
                    serializer_seia = SeiaSeaSerializer(data=seia)
                    serializer_seia.is_valid(raise_exception=True)
                    serializer_seia.save()
                    table.append(seia)

        return Response({"data": table})
