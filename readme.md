![Infotecs](https://journal.ib-bank.ru/files/images/news/2018-04-11_2.png)
# Тестовое задание
___
###Задание

Реализовать HTTP-сервер для предоставления информации по географическим объектам.
Данные взять с географической базы данных GeoNames.

Реализованный сервер должен предоставлять REST API сервис со следующими методами:
1.	Метод принимает идентификатор geonameid и возвращает информацию о городе.
2.	Метод принимает страницу и количество отображаемых на странице городов 
      и возвращает список городов с их информацией. 
3.	Метод принимает названия двух городов (на русском языке) и 
      получает информацию о найденных городах, а также дополнительно: 
      какой из них расположен севернее и одинаковая ли у них временная зона
      (когда несколько городов имеют одно и то же название, разрешать 
      неоднозначность выбирая город с большим населением; если население совпадает,
      брать первый попавшийся)

###Требования
В качестве решения принимается скрипт на python с описанием методов 
в файле readme.md.
Скрипт запускается следующим образом: python3 script.py

После этого по адресу 127.0.0.1 и порту 8000 можно обращаться с 
указанными выше функциями.

Программа должна читать данные из файла RU.txt, который заранее будет 
лежать в той же директории, что и программа – не требуется их скачивать по 
ссылкам в самой программе. Данные допускается держать в памяти программы и не 
работать с БД. Если вы предпочтете использовать БД, делайте это так, чтобы не
было необходимости какой-то дополнительной настройки программы, или дополнительных
требований к наличию этой БД на машине.
___

##Реализация


###Задача 1
Метод **get_geonameid** принимает параметр `geonameid`, отвечающий за id искомого
города. После он осуществляет поиск по базе данные Geoname, которую заранее
занесли в список. Поиск осуществляется путем сопоставления значения полученного
параметра и первым значением преобразованных списков. В конечном итоге метод возвращает
информацию о городе в виде специального словаря, в котором значения 
`keys` - это название полей основной таблицы, а значение `values` - информация о городе.

Код метода:

```python
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
```
Метод доступен по запросу:

`http://127.0.0.1:8000/geonameid/{geonameid}`

Пример работы метода: 

Request URL

`http://127.0.0.1:8000/geonameid/8535088`

Response body

```
{
  "geonameid": "8535088",
  "name": "Nizhnyaya Tuarma",
  "asciiname": "Nizhnyaya Tuarma",
  "alternatenames": "Nizhnjaja Tuarma,Nizhnyaya Tuarma,Нижняя Туарма",
  "latitude": "54.5373",
  "longitude": "51.6487",
  "feature class": "P",
  "feature code": "PPL",
  "country code": "RU",
  "cc2": "",
  "admin1 code": "65",
  "admin2 code": "",
  "admin3 code": "",
  "admin4 code": "",
  "population": "0",
  "elevation": "",
  "dem": "129",
  "timezone": "Europe/Samara",
  "modification date": "2013-06-05"
}
```

###Задача 2
Метод **list_of_cities** принимает два параметра:
`page`- отвечающий за количество страниц и `size` - 
отвечающий за количество элементов на странице. После по 
этим параметрам метод возвращает список с информацией о городах.

Код метода:
```python
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
```
Метод доступен по запросу:

`http://127.0.0.1:8000/cities/?page={}&size={}`

Пример работы метода: 

Request URL

`http://127.0.0.1:8000/cities/?page=2&size=3`

Response body

```
[
  {
    "geonameid": "451750",
    "name": "Zhitovo",
    "asciiname": "Zhitovo",
    "alternatenames": "",
    "latitude": "57.29693",
    "longitude": "34.41848",
    "feature class": "P",
    "feature code": "PPL",
    "country code": "RU",
    "cc2": "",
    "admin1 code": "77",
    "admin2 code": "",
    "admin3 code": "",
    "admin4 code": "",
    "population": "0",
    "elevation": "",
    "dem": "247",
    "timezone": "Europe/Moscow",
    "modification date": "2011-07-09"
  },
  {
    "geonameid": "451751",
    "name": "Zhitnikovo",
    "asciiname": "Zhitnikovo",
    "alternatenames": "",
    "latitude": "57.20064",
    "longitude": "34.57831",
    "feature class": "P",
    "feature code": "PPL",
    "country code": "RU",
    "cc2": "",
    "admin1 code": "77",
    "admin2 code": "",
    "admin3 code": "",
    "admin4 code": "",
    "population": "0",
    "elevation": "",
    "dem": "198",
    "timezone": "Europe/Moscow",
    "modification date": "2011-07-09"
  },
  {
    "geonameid": "451752",
    "name": "Zhelezovo",
    "asciiname": "Zhelezovo",
    "alternatenames": "",
    "latitude": "57.02591",
    "longitude": "34.51886",
    "feature class": "P",
    "feature code": "PPL",
    "country code": "RU",
    "cc2": "",
    "admin1 code": "77",
    "admin2 code": "",
    "admin3 code": "",
    "admin4 code": "",
    "population": "0",
    "elevation": "",
    "dem": "192",
    "timezone": "Europe/Moscow",
    "modification date": "2011-07-09"
  }
]
```




###Задача 3
Метод **two_cities_information** принимает два параметра `city1` и `city2`,
которые отвечают за название городов на *русском языке*. Из-за того, что 
в изначальной базе присутствуют города, имеющие только название на английском языке,
метод переводит полученные имена городов на английский язык и обращается к 
методу **search_by_name**, передавая ему в качестве параметров названия городов на 
русском и на английском языках. После метод находит город, который расположен севернее 
и определяет временные зоны городов. По итогу возвращается информация 
о городах в виде сформированных словарей, а также информация о городе, который
находится севернее, и информация о том, находятся ли города в одной временной зоне или нет.

Код метода two_cities_information
```python
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
```
Метод **search_by_name** получает от метода **two_cities_information** параметры
и по ним ищет совпадения в базе данных Geoname. Если совпадения были обнаружены, то
метод возвращает список, содержащий в себе информацию о городе. Если город найти не удалось
то возвращается значение `-1`.

Код метода search_by_name:
```python
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
```

Метод доступен по запросу:

`http://127.0.0.1:8000/two_cities/?city1={}&city2={}`

Пример работы метода:

Request URL

`http://127.0.0.1:8000/two_cities/?city1=Москва&city2=Новосибирск`

Response body

```
  {
    "geonameid": "524894",
    "name": "Moskva",
    "asciiname": "Moskva",
    "alternatenames": "Maskva,Moscou,Moscow,Moscu,Moscú,Moskau,Moskou,Moskovu,Moskva,Məskeu,Москва,Мәскеу",
    "latitude": "55.76167",
    "longitude": "37.60667",
    "feature class": "A",
    "feature code": "ADM1",
    "country code": "RU",
    "cc2": "",
    "admin1 code": "48",
    "admin2 code": "",
    "admin3 code": "",
    "admin4 code": "",
    "population": "11503501",
    "elevation": "",
    "dem": "161",
    "timezone": "Europe/Moscow",
    "modification date": "2020-03-31"
  },
  {
    "geonameid": "1496747",
    "name": "Novosibirsk",
    "asciiname": "Novosibirsk",
    "alternatenames": "Cen Ceper,Nobosimpirsk,Novasibirsk,Novo-Nikolaevsk,Novo-Nikolaievsk,Novo-Nikolaïevsk,Novonikolaevsk,Novonikolayevsk,Novosibir,Novosibir'sku,Novosibirs'k,Novosibirscum,Novosibirsk,Novosibirska,Novosibirskaj,Novosibirskas,Novosibirsko,Novosimpirsk,Novossibirsk,Novoszibirszk,Nowosibirsk,Nowosibirski,Nowosybirsk,OVB,Odsibiren' osh,Vil' Sibirkar,no wo sibiskh,nobosibileuseukeu,novosibirsk,novosibirska,novuoshibirusuku,nwbwsybyrsq,nwfwsybyrsk,nwwsybrsk,nwwsybyrsk,xin xi bo li ya,Çĕн Çĕпĕр,Νοβοσιμπίρσκ,Νοβοσιμπιρσκ,Виль Сибиркар,Новасібірск,Новониколаевск,Новосибирск,Новосибирскай,Новосибирьскъ,Новосибірськ,Новосібір,Одсибирень ош,Նովոսիբիրսկ,נובוסיבירסק,نوفوسيبيرسك,نووسیبرسک,نووسیبیرسک,नोवोसिबिर्स्क,โนโวซีบีสค์,ნოვოსიბირსკი,ノヴォシビルスク,新西伯利亚,新西伯利亞,노보시비르스크",
    "latitude": "55.0415",
    "longitude": "82.9346",
    "feature class": "P",
    "feature code": "PPLA",
    "country code": "RU",
    "cc2": "",
    "admin1 code": "53",
    "admin2 code": "1496742",
    "admin3 code": "",
    "admin4 code": "",
    "population": "1419007",
    "elevation": "",
    "dem": "164",
    "timezone": "Asia/Novosibirsk",
    "modification date": "2019-09-05"
  },
  "Город Москва расположен севернее",
  "Временные зоны у городов разные"
```

___
