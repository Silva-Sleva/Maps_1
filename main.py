import sys
from io import BytesIO  # Этот класс поможет нам сделать картинку из потока байт

import requests
from PIL import Image


def map_spn(jresp):
    lo_con = jresp['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']["boundedBy"]['Envelope']['lowerCorner']
    r_con = jresp['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']["boundedBy"]['Envelope']['upperCorner']
    a, b = map(float, lo_con.split())
    a1, b1 = map(float, r_con.split())
    return ','.join([str(abs(a - a1)), str(abs(b - b1))])


# Пусть наше приложение предполагает запуск:
# python search.py Москва, ул. Ак. Королева, 12
# Тогда запрос к геокодеру формируется следующим образом:
# toponym_to_find = " ".join(sys.argv[1:])
toponym_to_find = 'Великий Новгород, Большая Московская, 132'
# toponym_to_find = 'Австралия'

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    # обработка ошибочной ситуации
    pass

# Преобразуем ответ в json-объект
json_response = response.json()
# Получаем первый топоним из ответа геокодера.
toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
# Координаты центра топонима:
toponym_coodrinates = toponym["Point"]["pos"]
# Долгота и широта:
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

delta = "0.005"
apikey = "ce9c9bb1-bc41-4b06-b3e8-ae123466049b"

# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": map_spn(json_response),
    "apikey": apikey,

}

map_api_server = "https://static-maps.yandex.ru/v1"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)
im = BytesIO(response.content)
opened_image = Image.open(im)
opened_image.show()  # Создадим картинку и тут же ее покажем встроенным просмотрщиком операционной системы
