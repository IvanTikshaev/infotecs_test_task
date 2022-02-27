import re
import codecs
import uvicorn
from fastapi import FastAPI
from translate import Translator

app = FastAPI()

with codecs.open("RU.txt", "r", "utf-8") as ru:
    ru_lines = ru.readlines()


def dict_creation(list2):
    """
    Функция принимает список и с помощью дополнительного списка
    создает словарь для вывода информации
    :param list2: список содержащий информацию о городе: list
    :return: инофрмация в виде словаря: dict
    """
    list1 = ["geonameid", "name", "asciiname", "alternatenames",
             "latitude", "longitude", "feature class", "feature code",
             "country code", "cc2", "admin1 code", "admin2 code", "admin3 code",
             "admin4 code", "population", "elevation", "dem", "timezone", "modification date"]
    list2[18] = list2[18].replace('\n', '')
    new_dict = {list1[i]: list2[i] for i in range(19)}
    return new_dict


def search_by_name(ru_name, en_name):
    """
    Функция принимает название города на русском и английском языках.
    По этим названиям осуществляет поиск и если совпадение было найдено, то
    возвращает информацию об этом городе в виде списка.
    Если совпадений не обнаружено, то возвращает -1
    :param ru_name: название города на русском:str
    :param en_name: название города на английском:str
    :return: информацией о найденном городе в виде списка:list или -1
    """
    for line in ru_lines:
        n = re.split('\t', line)
        n3 = re.split(',', n[3])
        for i in n3:
            if i == ru_name:
                overlap = True
                break
        else:
            overlap = False
        if overlap or n[1] == en_name:
            return n
    else:
        return -1


@app.get("/geonameid/{geonameid}")
async def get_geonameid(geonameid: str):
    """
    Функция принимает id города и возвращает информацию о нем
    :param geonameid: числовое значение в виде строки тип:str
    :return: результат работы функции dict_creation: dict
    """
    for line in ru_lines:
        n = re.split('\t', line)
        if n[0] == geonameid:
            return dict_creation(n)
    else:
        return {"Информация не найдена"}


@app.get("/cities/")
async def list_of_cities(page: int, size: int):
    """
    Функция принимает номер страницы и количество элементов на страницы
    и возвращает информацию о городах с введенной страницы
    :param page: номер страницы: int
    :param size: количество элементов на страницы:int
    :return: список словарей с информацией о городах:int
    """
    if page * size > len(ru_lines) or page * size < 1:
        return {"Некорректный ввод количества страниц или количества городов на странице"}
    cityList = []
    i = (page - 1) * size
    for i in range(i, page * size):
        n = re.split('\t', ru_lines[i])
        cityList.append(dict_creation(n))
    return cityList


@app.get("/two_cities/")
async def two_cities_information(city1: str, city2: str):
    """
    Функция принимает название двух городов и возвращает информацию о них,
    а также информацию о том, какой из городов севернее, и находятся ли они
    в одной временной зоне
    :param city1: название 1го города:
    :param city2: название 2го города:
    :return: Информация о городах в виде словарей: dict
            информация о северном городе: str
            информация о временных зонах: str
    """
    translator = Translator(from_lang="russian", to_lang="english")
    trans_city1 = translator.translate(city1)
    trans_city2 = translator.translate(city2)
    city1_list = search_by_name(city1, trans_city1)
    city2_list = search_by_name(city2, trans_city2)

    if city1_list == -1:
        return ("Данный город отсутсвует или данные введены некорректно", city1)
    if city2_list == -1:
        return ("Данный город отсутсвует или данные введены некорректно", city2)
    if city1_list[4] > city2_list[4]:
        nort_city = "Город {} расположен севернее".format(city1)
    else:
        nort_city = "Город {} расположен севернее".format(city2)
    if city1_list[17] == city2_list[17]:
        timezona = "Города находятся в одной временной зоне"
    else:
        timezona = "Временные зоны у городов разные"
    return dict_creation(city1_list), dict_creation(city2_list), nort_city, timezona


if __name__ == '__main__':
    uvicorn.run("script:app", host='127.0.0.1', port=8000, reload=True)
