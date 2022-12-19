from abc import ABC
import requests
import json
from datetime import date

from bot.Exceptions import NoCityFoundException

from Hotels_API.settings import BASE_REQUEST
from Hotels_API.functions import key_search
from Hotels_API.settings import url_loc, url_hotels, url_photo, QUERYSTRING, HEADERS, \
    _MAX_HOTELS_NUMBER, _MAX_PHOTO_NUMBER


from loguru import logger


class Request(ABC):
    """
    Базовый класс запросов, в котором реализуются абстрактные методы.
    """

    @classmethod
    def get_querystring(cls) -> dict[str, str]:
        """Получение словаря параметров для запроса заданного города."""
        return QUERYSTRING

    @classmethod
    def get_headers(cls) -> dict[str, str]:
        """Получение значений адреса запроса и "ключа" пользователя."""
        return HEADERS

    @classmethod
    def get_base_request(cls) -> dict[str, str]:
        """Получение словаря с параметрами базового запроса отелей."""
        return BASE_REQUEST


class BaseRequest(Request):
    """
    Общий класс, в котором реализуется метод запроса заданного города.

    :param: _location_dict: dict словарь для временного хранения кодов городов по названию города.
    """
    _location_dict = {}
    request = ''

    @logger.catch
    def get_destination_id(self, city: str) -> str or bool:
        """
        Метод запроса города, заданного пользователем. Если город не найден - возвращается None.
        :param city: заданный пользователем город.
        :return destination_id: необходимый для поиска отелей код города.
        """

        query = self.get_querystring()

        if city not in self._location_dict:
            query["query"] = city
            result = json.loads(requests.request('GET', url_loc, headers=self.get_headers(), params=query).text)

            try:
                if not result['suggestions'][0]['entities']:
                    raise NoCityFoundException
                else:
                    destination_id = result['suggestions'][0]['entities'][0]['destinationId']

                self._location_dict[city] = destination_id
                return destination_id
            except NoCityFoundException:
                logger.exception('NoCityFound')
                return None

        return self._location_dict.get(city)


class Hotels(BaseRequest):
    """
    Класс, в котором реализуются методы для запроса и обработки данных об отелях.

    :param: _MAX_PHOTO_NUMBER: int максимальное число запрашиваемых фотографий. Ограничено, чтобы сообщение не было
    слишком громоздким.
    :param: _MAX_HOTELS_NUMBER: int максимальное число запрашиваемых отелей. Ограничено, чтобы не засорять чат
    большим количеством сообщений.
    """

    def __init__(self, city: str, photo_number: str, hotels_number: str, check_in_date: date, check_out_date: date):
        """
        Конструктор класса Hotels.

        :param city: запрашиваемый город.
        :param photo_number: заданное количество фотографий отеля.
        :param hotels_number: заданное количество отелей.
        :param check_in_date: заданная дата заезда.
        :param check_out_date: заданная дата выезда.
        """
        self.check_out_date = check_out_date
        self.check_in_date = check_in_date
        self.city = city
        self.hotels_number = self._max_quantity(hotels_number, 'hotel')
        self.photo_number = self._max_quantity(photo_number, 'photo')
        self.request = self.get_request()

    def get_request(self) -> dict:
        """
        Метод редактирования словаря для запроса отелей.

        :return:req_dict - обновленный словарь с датами заезда, выезда, кодом города и количеством запрашиваемых отелей.
        """

        dest_id = self.get_destination_id(self.city)
        req_dict = self.get_base_request()
        new_dict = {"checkIn": str(self.check_in_date), "checkOut": str(self.check_out_date),
                    'destinationId': dest_id, 'pageSize': self.hotels_number}
        req_dict.update(new_dict)
        return req_dict

    def get_hotels_list(self) -> list[dict] or bool:
        """
        Метод выполняет запрос к API для получения списка отелей по заданным параметрам. Если запрашиваемые отели не
        находятся, то возвращается строка: 'no hotels'.

        :return: hotels_list - список отелей
        """

        hotels_list = []
        print('request -', self.request)
        if not self.request['destinationId']:
            return None

        response_result = requests.request('GET', url=url_hotels, headers=self.get_headers(), params=self.request).text
        result = json.loads(response_result)

        if not key_search('results', result):
            return 'no hotels'
        for hotel in result['data']['body']['searchResults']['results']:
            hotels_list.append(self.get_hotel_info(hotel, self.photo_number,
                                                   self.check_in_date, self.check_out_date))
        return hotels_list

    @classmethod
    def get_hotel_info(cls, hotel: dict, photo_number: int, check_in_date: date, check_out_date) -> dict:
        """
        Данный метод получает отдельно каждый отель (словарь) и приводит его к необходимому виду.

        :param hotel: словарь с данными об отеле.
        :param photo_number: количество фото отеля для вывода.
        :param check_in_date: дата заезда.
        :param check_out_date: дата выезда.
        :return: возвращает словарь, приведенный к нужному виду.
        """
        address = key_search('countryName', hotel) + ', ' + key_search('locality', hotel)
        if hotel['address'].get('streetAddress'):
            address += ', ' + hotel['address']['streetAddress']
        if hotel['address'].get('extendedAddress'):
            address += ', ' + hotel['address']['extendedAddress']

        price = key_search('current', hotel)
        star = key_search('starRating', hotel)
        user_rating = key_search('rating', hotel)
        photo_list = HotelPhoto.get_photo(hotel, photo_number)

        return {
            'id': str(key_search('id', hotel)),
            'name': key_search('name', hotel),
            'address': address,
            'distance_from_city_center': cls._distance_convert(hotel),
            'price': price if price else 'Цена по запросу',
            'star': star if star else 'null',
            'user_rating': user_rating if user_rating else 'null',
            'check_in': str(check_in_date),
            'check_out': str(check_out_date),
            'total_price': cls._total_price_count(price, check_out_date - check_in_date),
            'photo': photo_list
        }

    @classmethod
    def _max_quantity(cls, number: str, key: str) -> int:
        """
        Проверка ввода количества отелей и фотографий, необходимых для вывода. Если введенное число превышает
        максимальное, то возвращается максимальное.

        :param number: количество параметра, введенное пользователем.
        :param key: необходимый для проверки параметр (photo или hotel).
        :return number: проверенное количество, заданного параметра
        """

        max_number = {'photo': _MAX_PHOTO_NUMBER,
                      'hotel': _MAX_HOTELS_NUMBER}
        number = int(number)

        if number > max_number.get(key):
            return max_number.get(key)
        return number

    @classmethod
    def _distance_convert(cls, hotel: dict) -> str:
        """
        Перевод миль в километры.

        :param hotel: словарь с данными об отеле.
        :return: отредактированное количество километров.
        """
        convert_mi_to_km_coefficient = 1.609344

        for mark in key_search('landmarks', hotel):
            if mark['label'] in ('City center', 'Центр города'):
                distance = mark.get('distance').split()
                break
        else:
            return 'null'
        kilometers = float(distance[0]) * convert_mi_to_km_coefficient

        return '{:.1f} km'.format(kilometers)

    @classmethod
    def _total_price_count(cls, price: str, days: str) -> str:
        """
        Метод, рассчитывающий стоимость проживания на весь заданный срок.

        :param price: цена за сутки.
        :param days: заданный срок проживания в днях.
        :return total_price: str общая стоимость проживания.
        """
        if price:
            price = price.split()[0]
            price = int(price.replace(',', ''))
            days = int((str(days)).split()[0])
            total_price = '{0:,} RUB'.format(price * days)
            return total_price
        else:
            return 'Цена по запросу'


class HotelPhoto(Hotels):
    """
    Класс, в котором реализуется получение и редактирование ссылки фотографии отеля.
    """

    @classmethod
    def get_photo(cls, hotel: dict, photo_number: int) -> list[str] or None:
        """
        Метод, получения данных о фотографиях заданного отеля и редактирования ссылки на фотографии.

        :param hotel: словарь с данными об отеле.
        :param photo_number: запрашиваемое пользователем количество фотографий.
        :return возвращает список со ссылками на фотографии. Если пользователь не запросил фотографии, то
        возвращается значение None:
        """
        hotel_id = {'id': hotel['id']}
        if not photo_number:
            return None

        try:
            result = json.loads(requests.request('GET', url=url_photo,
                                                 headers=cls.get_headers(), params=hotel_id).text)
            images_list = result.get('hotelImages')
            return [images_list[idx]['baseUrl'].replace('{size}', 'z') for idx in range(0, photo_number)]
        except json.decoder.JSONDecodeError:
            return None


class LowPrice(Hotels):
    """
    Класс, реализующий запрос отелей с сортировкой по минимальной цене.
    """

    def __init__(self, city: str, photo_number: str, hotels_number: str, check_in_date: date, check_out_date: date):
        super().__init__(city, photo_number, hotels_number, check_in_date, check_out_date)

    def get_request(self) -> dict:
        """
        Метод, переопределяющий метод базового класса, реализующий обновление словаря с параметрами для запроса
        отелей.

        :return: словарь, обновленный по типу сортировки.
        """

        req_dict = super().get_request()
        new_dict = {'sortOrder': 'PRICE'}
        req_dict.update(new_dict)
        return req_dict


class HighPrice(Hotels):
    def __init__(self, city: str, photo_number: str, hotels_number: str, check_in_date: date, check_out_date: date):
        super().__init__(city, photo_number, hotels_number, check_in_date, check_out_date)

    def get_request(self) -> dict:
        """
        Метод, переопределяющий метод базового класса, реализующий обновление словаря с параметрами для запроса
        отелей.

        :return: словарь, обновленный по типу сортировки.
        """

        req_dict = super().get_request()
        new_dict = {'sortOrder': 'PRICE_HIGHEST_FIRST'}
        req_dict.update(new_dict)
        return req_dict


class BestDeal(Hotels):
    def __init__(self, city: str, photo_number: str, hotels_number: str,  price_min: str, price_max: str,
                 distance_from_centre: float, check_in_date: date, check_out_date: date):
        """
        Конструктор класса BestDeal.

        :param price_min: заданная минимальная стоимость отеля.
        :param price_max: заданная максимальная стоимость отеля.
        :param distance_from_centre: заданное расстояние от отеля до центра города.
        """
        self.price_min = price_min
        self.price_max = price_max
        self.distance_from_centre = distance_from_centre
        print(self.distance_from_centre, self.price_min, self.price_max)
        super().__init__(city, photo_number, hotels_number, check_in_date, check_out_date)

    def get_request(self) -> dict:
        """
        Метод, переопределяющий метод базового класса, реализующий обновление словаря с параметрами для запроса
        отелей.

        :return: словарь, с обновленным типом сортировки, минимальной и максимальной ценами.
        """

        req_dict = super().get_request()
        new_dict = {'sortOrder': 'DISTANCE_FROM_LANDMARK', 'priceMin': self.price_min, 'priceMax': self.price_max}
        req_dict.update(new_dict)
        return req_dict

    def get_hotels_list(self) -> list[dict]:
        """
        Метод, переопределяющий метод базового класса, реализующий получение словаря с данными об отелях, а также
        удаление отелей, не подходящих под параметры запроса.

        :return: список словарей с данными об отелях.
        """

        hotels_list = super().get_hotels_list()
        hotels_to_remove = []
        if hotels_list != 'no hotels':
            for hotel in hotels_list:
                distance = float(hotel['distance_from_city_center'].split()[0])
                if distance > self.distance_from_centre:
                    hotels_to_remove.append(hotel)

            for hotel in hotels_to_remove:
                hotels_list.remove(hotel)
        return hotels_list


class RequestHandler:
    """
    Класс, реализующий паттерн - фабричный метод.

    :param: low_price: экземпляр класса LowPrice.
    :param: high_price: экземпляр класса HighPrice.
    :param: best_deal: экземпляр класса BestDeal.
    """
    low_price = LowPrice
    high_price = HighPrice
    best_deal = BestDeal

    COMMANDS = {
        'low_price': low_price,
        'high_price': high_price,
        'best_deal': best_deal
    }

    @classmethod
    def hotels_search(cls, city: str, sort_parameter: str, *args, **kwargs):
        """
        Метод, реализующий интерфейс доступа к методам и классам Hotels API из других модулей.

        :param city: запрашиваемый город.
        :param sort_parameter: тип сортировки отелей.
        :return:
        """
        result = cls.COMMANDS[sort_parameter](city, *args, **kwargs).get_hotels_list()
        return result
