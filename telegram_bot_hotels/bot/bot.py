import datetime
import time
from abc import ABC, abstractmethod

import telebot

from telebot import types
from telebot.types import Message

from db.db import DatabaseHandler as db

from bot.Exceptions import DateDifferenceException, EmptyHistoryException, MinPriceException, \
    DistanceException, MaxPriceException, PriceDifferenceException, WrongNumberException
from bot import bot_settings

from Hotels_API.hotels_request import RequestHandler as rh
from Hotels_API.hotels_request import _MAX_HOTELS_NUMBER, _MAX_PHOTO_NUMBER

from loguru import logger

bot = telebot.TeleBot(bot_settings.bot_token)


class TelegramCommands(ABC):
    """
    Базовый класс, реализующий методы для работы с Telegram API.
    :param: info_dict: словарь для записи всех данных, вводимых пользователем при каждом запросе отелей.
    :param: hotels_links: словарь для записи ссылок на отели в каждом запросе для их записи в базу данных.
    :param: command: команда, отвечающая за тип сортировки отелей.
    """
    info_dict = {}
    hotels_links = {}
    command = ''

    @abstractmethod
    def get_info(self, *args):
        """
        Абстрактный метод, реализующий запрос отелей по заданному типу сортировки.
        """
        pass

    @classmethod
    def city_name(cls, message: types.Message, command: str):
        """
        Метод, реализующий получение от пользователя названия города для запроса.
        :param command: команда, отвечающая за тип сортировки отелей.
        :param message: параметр, хранящий информацию о чате и последнем сообщении от пользователя.
        """
        cls.command = command
        msg = bot.send_message(message.chat.id, 'Введите название города')
        bot.register_next_step_handler(msg, cls.set_check_in_year, True)

    @classmethod
    def set_check_in_year(cls, message: types.Message, update: bool) -> None:
        """
        Метод, реализующий запрос даты (года) заезда у пользователя.
        :param update: булева переменная, отвечающая за необходимость обновления словаря.
        :param message: параметр, хранящий информацию о чате и последнем сообщении от пользователя.
        """
        if update:
            cls.info_dict.update({'city': message.text})
            cls._delete_message(message)
            cls._send_repeat_message(message, 'city')
        check_in_out_dict = {'dict_name': 'check_in'}
        msg = bot.send_message(message.chat.id, 'Выберете дату заезда:\nВыберете год',
                               reply_markup=bot_settings.year_markup)
        bot.register_next_step_handler(msg, cls.set_check_in_out_month, check_in_out_dict)

    @classmethod
    def set_check_out_year(cls, message: types.Message) -> None:
        """
        Метод, реализующий запрос даты (года) выезда у пользователя.
        :param message: параметр, хранящий информацию о чате и последнем сообщении от пользователя.
        """
        check_in_out_dict = {'dict_name': 'check_out'}
        msg = bot.send_message(message.chat.id, 'Выберете дату выезда:\nВыберете год',
                               reply_markup=bot_settings.year_markup)
        bot.register_next_step_handler(msg, cls.set_check_in_out_month, check_in_out_dict)

    @classmethod
    def set_check_in_out_month(cls, message: types.Message, check_in_out_dict: dict) -> None:
        """
        Метод, реализующий запрос даты (месяца) заезда/выезда у пользователя.
        :param message: параметр, хранящий информацию о чате и последнем сообщении от пользователя.
        :param check_in_out_dict: Словарь, хранящий информацию о дате заезда/выезда.
        """
        check_in_out_dict.update({'year': int(message.text)})
        msg = bot.send_message(message.chat.id, 'Выберете месяц', reply_markup=bot_settings.month_markup)
        bot.register_next_step_handler(msg, cls.set_check_in_out_day, check_in_out_dict)

    @classmethod
    def set_check_in_out_day(cls, message: types.Message, check_in_out_dict: dict) -> None:
        """
        Метод, реализующий запрос даты (дня) заезда/выезда у пользователя.
        :param message: параметр, хранящий информацию о чате и последнем сообщении от пользователя.
        :param check_in_out_dict: Словарь, хранящий информацию о дате заезда/выезда.
        """
        check_in_out_dict.update({'month': message.text})
        markup_variant = ''
        for months, markup in bot_settings.month_day_dict.items():
            if message.text == 'Февраль' and check_in_out_dict.get('year') in bot_settings.leap_year:
                markup_variant = bot_settings.day_markup_var_4
            else:
                if message.text in months:
                    markup_variant = markup

        msg = bot.send_message(message.chat.id, 'Выберете день', reply_markup=markup_variant)
        bot.register_next_step_handler(msg, cls.format_date, check_in_out_dict)

    @classmethod
    def format_date(cls, message: types.Message, date_dict: dict) -> None:
        """
        Форматирование словаря с датой и временем в строку.
        :param message: параметр, хранящий информацию о чате и последнем сообщении от пользователя.
        :param date_dict: словарь, хранящий информацию о дате заезда/выезда.
        """
        date_dict.update({'day': int(message.text),
                          'month': bot_settings.month_number_dict.get(date_dict.get('month'))})
        cls._delete_message(message, 6)
        if not cls._date_check(date_dict):
            bot.send_message(message.chat.id, 'Дата введена неверно, повторите ввод.')
            if date_dict.get('dict_name') == 'check_in':
                cls.set_check_in_year(message, False)
            else:
                cls.set_check_out_year(message)
        else:
            date = datetime.date(date_dict.get('year'),
                                 date_dict.get('month'),
                                 date_dict.get('day'))
            result_dict = {date_dict.get('dict_name'): date}
            cls.info_dict.update(result_dict)
            if date_dict.get('dict_name') == 'check_out':
                cls._check_date_diff(message)
            else:
                cls._send_repeat_message(message, 'check_in')
                cls.set_check_out_year(message)

    @classmethod
    def min_price(cls, message: types.Message) -> None:
        """
        Запрос минимальной цены от пользователя.
        :param message: параметр, хранящий информацию о чате и последнем сообщении от пользователя.
        """
        msg = bot.send_message(message.chat.id, 'Введите минимальную цену за ночь (пр. "2000")',
                               reply_markup=bot_settings.price_markup)
        bot.register_next_step_handler(msg, cls._check_min_price)

    @classmethod
    def max_price(cls, message: types.Message, update: bool) -> None:
        """
        Запрос максимальной цены от пользователя.
        :param message: параметр, хранящий информацию о чате и последнем сообщении от пользователя.
        :param update: параметр, отвечающий за обновление словаря с данными для запроса.
        """
        if update:
            cls.info_dict.update({'min_price': message.text})
            cls._send_repeat_message(message, 'min_price')
            cls._delete_message(message)

        msg = bot.send_message(message.chat.id, 'Введите максимальную цену за ночь (пр. "10000")',
                               reply_markup=bot_settings.price_markup)
        bot.register_next_step_handler(msg, cls._check_max_price)

    @classmethod
    def distance_from_center(cls, message: types.Message, update=True) -> None:
        """
        Запрос необходимого максимального радиуса поиска отелей.
        :param update: параметр, отвечающий за повторный вызов функции.
        :param message: параметр, хранящий информацию о чате и последнем сообщении от пользователя.
        """
        if update:
            cls.info_dict.update({'max_price': message.text})
            cls._delete_message(message)
            cls._send_repeat_message(message, 'max_price')
        msg = bot.send_message(message.chat.id, 'Введите расстояние до центра (пр. "1.2")',
                               reply_markup=bot_settings.distance_markup)

        bot.register_next_step_handler(msg, cls._check_distance)

    @classmethod
    def hotel_number(cls, message: types.Message, update=True) -> None:
        """
        Запрос необходимого количества отелей для поиска.
        :param update: параметр, отвечающий за обновление словаря с данными для запроса.
        :param message: параметр, хранящий информацию о чате и последнем сообщении от пользователя.
        """
        if cls.command == 'best_deal' and update:
            cls.info_dict.update({'distance_from_center': message.text})
            cls._delete_message(message)
            cls._send_repeat_message(message, 'distance')

        msg = bot.send_message(message.chat.id, 'Сколько отелей хотите вывести? (max = 7)',
                               reply_markup=bot_settings.hotel_markup)
        bot.register_next_step_handler(msg, cls._hotel_number_check)

    @classmethod
    def photo(cls, message, max_number=True) -> None:
        """
        Запрос необходимости вывода фотографий.
        :param max_number: параметр, отвечающий за превышение пользователем максимального числа отелей для вывода.
        :param message: параметр, хранящий информацию о чате и последнем сообщении от пользователя.
        """
        if max_number:
            hotel_num = message.text
        else:
            hotel_num = _MAX_HOTELS_NUMBER

        cls.info_dict.update({'hotel_num': hotel_num})
        cls._send_repeat_message(message, 'hotel_num')
        cls._delete_message(message)

        msg = bot.send_message(message.chat.id,
                               text='Хотите вывести фотографии?',
                               reply_markup=bot_settings.yes_no_markup)
        bot.register_next_step_handler(msg, cls.photo_handler)

    @classmethod
    def photo_handler(cls, message: types.Message) -> None:
        """
        Обработка ответа пользователя.
        :param message: параметр, хранящий информацию о чате и последнем сообщении от пользователя.
        """
        if message.text == 'Да':
            cls.photo_number(message)
        else:
            cls.info_dict.update({'photo_num': '0'})
            cls._delete_message(message)
            cls._send_repeat_message(message, 'photo_num')
            cls.get_response(message)

    @classmethod
    def photo_number(cls, message: types.Message) -> None:
        """
        Запрос количества фотографий отеля, необходимых для вывода.
        :param message: параметр, хранящий информацию о чате и последнем сообщении от пользователя.
        """
        msg = bot.send_message(message.chat.id, 'Сколько фотографий вывести? (max = 12)',
                               reply_markup=bot_settings.photo_markup)
        bot.register_next_step_handler(msg, cls._photo_number_check)

    @classmethod
    def add_last(cls, message: types.Message, max_number=True) -> None:
        """
        Метод, необходимый для получения ответа от пользователя и добавления значения количество фотографий в словарь.
        :param message: параметр, хранящий информацию о чате и последнем сообщении от пользователя.
        """
        if max_number:
            hotel_num = message.text
        else:
            hotel_num = _MAX_PHOTO_NUMBER

        cls.info_dict.update({'photo_num': hotel_num})
        cls._delete_message(message, 4)
        cls._send_repeat_message(message, 'photo_num')
        cls.get_response(message)

    @classmethod
    def get_response(cls, message: types.Message) -> None:
        """
        Запрос информации об отелях (по данным, полученным от пользователя).
        :param message: параметр, хранящий информацию о чате и последнем сообщении от пользователя.
        """
        cls.hotels_links.clear()
        city_name, hotel_num, photo_num = cls.info_dict.get('city'), cls.info_dict.get('hotel_num'), cls.info_dict.get(
            'photo_num')
        check_in_date, check_out_date = cls.info_dict.get('check_in'), cls.info_dict.get('check_out')

        if cls.command == 'best_deal':
            min_price, max_price, distance = cls.info_dict.get('min_price'), \
                                             cls.info_dict.get('max_price'), cls.info_dict.get('distance_from_center')
            print(city_name, hotel_num, photo_num, cls.command, cls.info_dict)
            response = rh.hotels_search(city_name, cls.command, photo_num, hotel_num,
                                        min_price, max_price, float(distance), check_in_date, check_out_date)

        else:
            print(city_name, hotel_num, photo_num, cls.command, cls.info_dict)
            response = rh.hotels_search(city_name, cls.command, photo_num, hotel_num, check_in_date, check_out_date)

        if not response:
            bot.send_message(message.chat.id, 'Город не найден!\nПопробуйте еще раз.')
            return None

        elif response == 'no hotels':
            bot.send_message(message.chat.id, 'Отели не найдены!\nПопробуйте еще раз.')
            return None

        for hotel in response:
            photo_list, response_string = cls.make_response(hotel, message)
            cls.send_response(message, photo_list, response_string)

        db.database_write_short_req(userid=message.chat.id, hotelinfo=cls._make_short_req())

    @classmethod
    def send_response(cls, message: types.Message, photo_list: str or None, response_string: str) -> None:
        """
        Метод, отправляющий пользователю отредактированную информацию о найденных отелях.
        :param message: параметр, хранящий информацию о чате и последнем сообщении от пользователя.
        :param photo_list: str - строка, хранящая ссылки на фотографии.
        :param response_string: str - строка, хранящая отредактированное сообщение для вывода пользователю.
        """
        if photo_list != 'Нет фото' and photo_list is not None:
            media_group = []
            for idx, photo in enumerate(photo_list):
                media_group.append(types.InputMediaPhoto(photo, caption=response_string if idx == 0 else None))
            bot.send_media_group(message.chat.id, media_group)
        else:
            bot.send_message(message.chat.id, response_string, disable_web_page_preview=True)

    @classmethod
    def make_response(cls, hotel: dict, message: types.Message, database=True) -> tuple:
        """
        Метод, отвечающий за создание response_string и запись информации в базу данных (при необходимости).
        :param hotel: словарь с информацией об отеле.
        :param message: параметр, хранящий информацию о чате и последнее ответное сообщение пользователя.
        :param database: булева переменная, отвечающая за запись отеля в базу данных.
        :return: кортеж из двух объектов: список фотографий list[str] и отредактированную информацию по отелю str
        """
        star = hotel.get('star')
        star_string = cls._count_star(star)
        check_in = hotel.get('check_in')
        check_out = hotel.get('check_out')
        hotel_link = 'https://www.hotels.com/ho' + str(hotel.get('id'))
        cls.hotels_links.update({hotel.get('name'): hotel_link})

        info_dict = {'name': f"Название отеля: {hotel.get('name')}",
                     'address': f"Адрес отеля: {hotel.get('address')}",
                     'price': f"Цена за ночь: {hotel.get('price')}",
                     'distance_from_city_center': f"Расстояние до центра города: {hotel.get('distance_from_city_center')}",
                     'star': f"Количество звезд: {star_string} {star} из 5.0",
                     'user_rating': f"Оценка пользователей: {hotel.get('user_rating')}",
                     'check_in': f"Дата заезда: {check_in} Дата выезда: {check_out}",
                     'total_price': f"Общая стоимость: {hotel.get('total_price')}"}

        response_string = '\n'.join([value for key, value in info_dict.items() if hotel.get(key) != 'null']) \
                          + f'\n{hotel_link}'

        photo_list = hotel.get('photo')
        hotel_name = hotel.get('name')
        hotel_address = hotel.get('address')
        hotel_price = hotel.get('price')
        distance = hotel.get('distance_from_city_center')
        user_rating = hotel.get('user_rating')
        total_price = hotel.get('total_price')

        if database:
            db.database_write_hotel(name=hotel_name, address=hotel_address,
                                    user_rating=user_rating if user_rating else 'Без рейтинга',
                                    star=star,
                                    distance_from_city_centre=distance, check_in=check_in,
                                    check_out=check_out, price=hotel_price, total_price=total_price,
                                    photo=photo_list if photo_list else 'Нет фото', userid=str(message.chat.id))

        return photo_list, response_string

    @classmethod
    def _make_short_req(cls) -> str:
        """
        Создает строку, содержащую сокращенную историю запросов, сделанных пользователем.
        :return: сокращенная история запросов.
        """
        date = time.localtime()
        request_date = str(datetime.datetime(date[0], date[1], date[2], date[3], date[4], date[5]))
        request_string = f'Запрос {cls.command}\nДата и время запроса: {request_date}\n' \
                         f'Город: {cls.info_dict.get("city")}\n'
        for key, value in cls.hotels_links.items():
            request_string += f'\n{key}\n{value}\n'
        return request_string

    @classmethod
    def _send_repeat_message(cls, message: types.Message, answer_type: str) -> None:
        """
        Отправляет отредактированное сообщение с информацией
        о запросе, которую ввел пользователь.
        :param answer_type: ключ словаря, по которому функция находит необходимое значение, содержащее строку с ответом.
        """
        answer_dict = {
            'city': 'Выбранный город: {}'.format(cls.info_dict.get('city')),
            'check_in': 'Выбранная дата заезда: {}'.format(cls.info_dict.get('check_in')),
            'check_out': 'Выбранная дата выезда: {}'.format(cls.info_dict.get('check_out')),
            'hotel_num': 'Выбранное количество отелей для вывода: {}'.format(cls.info_dict.get('hotel_num')),
            'photo_num': 'Выбранное количество фото отеля для вывода: {}'.format(cls.info_dict.get('photo_num')),
            'distance': 'Выбранное расстояние до центра города: {} км'.format(
                cls.info_dict.get('distance_from_center')),
            'min_price': 'Выбранная минимальная цена отеля: {} руб'.format(cls.info_dict.get('min_price')),
            'max_price': 'Выбранная максимальная цена отеля: {} руб'.format(cls.info_dict.get('max_price'))
        }
        bot.send_message(message.chat.id, answer_dict.get(answer_type))

    @classmethod
    def _date_check(cls, date_dict: dict) -> bool:
        """
        Проверка валидности ввода даты въезда или выезда.
        :param date_dict: Словарь, хранящий информацию о дате заезда/выезда.
        :return: True/False
        """
        year = date_dict.get('year')
        month = date_dict.get('month')
        day = date_dict.get('day')
        if year not in bot_settings.years_list:
            return False
        elif month not in bot_settings.month_number_dict.values():
            return False
        elif month == 2:
            if year in bot_settings.leap_year:
                if day not in range(1, 30):
                    return False
            elif day not in range(1, 29):
                return False
        return True

    @classmethod
    def _check_date_diff(cls, message: types.Message):
        """
        Метод, предназначенный для проверки ввода даты выезда и въезда.
        :param message: параметр, хранящий информацию о чате и последнем сообщении от пользователя.
        """
        try:
            result = cls.info_dict.get('check_out') - cls.info_dict.get('check_in')
            days = int((str(result)).split()[0])
            if days < 0:
                raise DateDifferenceException

            cls._send_repeat_message(message, 'check_out')

            if cls.command == 'best_deal':
                cls.min_price(message)
            else:
                cls.hotel_number(message)
        except DateDifferenceException:
            bot.send_message(message.chat.id, DateDifferenceException.__str__())
            logger.exception('DateTimeError')
            cls.set_check_out_year(message)

    @classmethod
    def _check_min_price(cls, message: types.Message) -> None:
        """
        Метод, предназначенный для проверки ввода минимальной цены.
        :param message: параметр, хранящий информацию о чате и последнем сообщении от пользователя.
        """
        min_price = message.text
        try:
            for sym in min_price:
                if not sym.isdigit() and sym != '.':
                    raise MinPriceException
            else:
                cls.max_price(message, True)

        except MinPriceException:
            cls._delete_message(message)
            bot.send_message(message.chat.id, MinPriceException.__str__())
            logger.exception('MinPriceException')
            cls.min_price(message)

    @classmethod
    def _check_distance(cls, message: types.Message) -> None:
        """
        Метод, предназначенный для проверки ввода расстояния до центра.
        :param message: параметр, хранящий информацию о чате и последнем сообщении от пользователя.
        """
        distance = message.text
        try:
            for sym in distance:
                if not sym.isdigit() and sym != '.':
                    raise DistanceException
            else:
                cls.hotel_number(message)

        except DistanceException:
            cls._delete_message(message, 2)
            bot.send_message(message.chat.id, DistanceException.__str__())
            logger.exception('WrongDistanceException')
            cls.distance_from_center(message, False)

    @classmethod
    def _check_max_price(cls, message: types.Message) -> None:
        """
        Метод, предназначенный для проверки ввода максимальной цены и сравнении максимальной цены с минимальной.
        :param message: параметр, хранящий информацию о чате и последнем сообщении от пользователя.
        """
        max_price = message.text
        min_price = cls.info_dict.get('min_price')
        try:
            for sym in max_price:
                if not sym.isdigit() and sym != '.':
                    raise MaxPriceException
            else:
                if float(min_price) >= float(max_price):
                    raise PriceDifferenceException
                else:
                    cls.distance_from_center(message)

        except MaxPriceException:
            cls._delete_message(message)
            bot.send_message(message.chat.id, MaxPriceException.__str__())
            logger.exception('MaxPriceException')
            cls.max_price(message, False)

        except PriceDifferenceException:
            bot.send_message(message.chat.id, PriceDifferenceException.__str__())
            logger.exception('PriceDifferenceException')
            cls.max_price(message, False)

    @classmethod
    def _hotel_number_check(cls, message: types.Message) -> None:
        """
        Метод, предназначенный для проверки введенного количества отелей.
        :param message: параметр, хранящий информацию о чате и последнем сообщении от пользователя.
        """
        try:
            if not message.text.isdigit():
                raise WrongNumberException
            else:
                if int(message.text) > _MAX_HOTELS_NUMBER:
                    bot.send_message(message.chat.id, 'Выбранное количество отелей больше максимального')
                    cls.photo(message, False)
                else:
                    cls.photo(message)

        except WrongNumberException:
            cls._delete_message(message)
            bot.send_message(message.chat.id, WrongNumberException.__str__())
            logger.exception('WrongNumberException')
            cls.hotel_number(message, False)

    @classmethod
    def _photo_number_check(cls, message: types.Message) -> None:
        """
        Метод, предназначенный для проверки введенного количества фотографий отеля.
        :param message: параметр, хранящий информацию о чате и последнем сообщении от пользователя.
        """
        try:
            if not message.text.isdigit():
                raise WrongNumberException
            else:
                if int(message.text) > _MAX_PHOTO_NUMBER:
                    bot.send_message(message.chat.id, 'Выбранное количество фотографий больше максимального')
                    cls.add_last(message, False)
                cls.add_last(message)

        except WrongNumberException:
            bot.send_message(message.chat.id, WrongNumberException.__str__())
            logger.exception('WrongNumberException')
            cls.photo_number(message)

    @staticmethod
    def _delete_message(message: types.Message, delete_number: int = 2) -> None:
        """
        Удаляет последние delete_number сообщения бота и пользователя.
        :param message: параметр, хранящий информацию о чате и последнем сообщении от пользователя.
        :param delete_number: количество сообщений для удаления.
        """
        chat_id = message.chat.id
        message_id = message.message_id
        for idx in range(delete_number):
            bot.delete_message(chat_id, message_id - idx)

    @staticmethod
    def _count_star(rating: float or str) -> str:
        """
        Метод, переводящий численное количество звезд отеля в символы.
        :param rating: численное количество звезд отеля.
        :return: строка с символьным количеством звезд.
        """
        counter = 5
        star_string = ''
        if rating != 'null':
            if rating == 0.0:
                star_string = '☆☆☆☆☆'
            elif rating == 0.5:
                star_string = '⋆☆☆☆☆'
            else:
                for _ in range(int(rating)):
                    star_string += '★'
                    counter -= 1
                if rating % int(rating) != 0:
                    star_string += '⋆'
                for _ in range(counter):
                    star_string += '☆'
        return star_string


class LowPriceCommand(TelegramCommands):
    """
    Класс, наследуемый от базового класса и реализующий запрос по команде low price.
    """
    def __init__(self):
        self.command = 'low_price'

    def get_info(self, msg: types.Message):
        self.city_name(msg, self.command)


class HighPriceCommand(TelegramCommands):
    """
    Класс, наследуемый от базового класса и реализующий запрос по команде high price.
    """
    def __init__(self):
        self.command = 'high_price'

    def get_info(self, msg: types.Message):
        self.city_name(msg, self.command)


class BestDealCommand(TelegramCommands):
    """
    Класс, наследуемый от базового класса и реализующий запрос по команде best deal.
    """
    def __init__(self):
        self.command = 'best_deal'

    def get_info(self, msg: types.Message):
        self.city_name(msg, self.command)


# TODO Не работает с функциями low_price, high_price, best_deal (встроенный вызов функций bot.register_next_step не
#  работает через данный встроенный фабричный метод). Получается, что часть функций вызывается через фабричный метод,
#  а часть через bot.message_handler. Нужно ли привести к общему виду?
def bot_handler(bot):
    bot.register_message_handler(start_message, commands='start')
    # bot.register_message_handler(low_price, commands='low_price')
    # bot.register_message_handler(high_price, commands='high_price')
    # bot.register_message_handler(best_deal, commands='best_deal')
    bot.register_message_handler(help_message, commands='help')
    bot.register_message_handler(history_message, commands='history')
    bot.register_message_handler(short_history_message, commands='short_history')
    bot.register_message_handler(clear_history, commands='clear_history')


def start_message(message: types.Message):
    """
    Функция, срабатывающая по команде start.
    :param message: параметр, хранящий информацию о чате и последнем сообщении от пользователя.
    """
    db.database_user_reg(userid=message.chat.id, username=message.chat.username)
    bot.send_message(message.chat.id,
                     'Добрый день, вы обратились к агенству "TooEasyTravel"!\n' +
                     bot_settings.HELP_TEXT)


@bot.message_handler(commands='low_price')
def low_price(message: types.Message):
    """
    Функция, срабатывающая по команде low_price.
    :param message: параметр, хранящий информацию о чате и последнем сообщении от пользователя.
    """
    lp = LowPriceCommand()
    lp.get_info(message)


@bot.message_handler(commands='high_price')
def high_price(message: types.Message):
    """
    Функция, срабатывающая по команде high_price.
    :param message: параметр, хранящий информацию о чате и последнем сообщении от пользователя.
    """
    lp = HighPriceCommand()
    lp.get_info(message)


@bot.message_handler(commands='best_deal')
def best_deal(message: types.Message):
    """
    Функция, срабатывающая по команде best_deal.
    :param message: параметр, хранящий информацию о чате и последнем сообщении от пользователя.
    """
    lp = BestDealCommand()
    lp.get_info(message)


def help_message(message: types.Message):
    """
    Функция, срабатывающая по команде help.
    :param message: параметр, хранящий информацию о чате и последнем сообщении от пользователя.
    """
    bot.send_message(message.chat.id, bot_settings.HELP_TEXT)


def history_message(message: types.Message):
    """
    Функция, срабатывающая по команде history.
    :param message: параметр, хранящий информацию о чате и последнем сообщении от пользователя.
    """
    result = db.database_get_hotels(message)
    if result:
        for hotel in result:
            photo_list, response_string = TelegramCommands.make_response(hotel, message, database=False)
            photo_list = photo_list.replace("['", '')
            photo_list = photo_list.replace("']", '')
            photo_list = photo_list.replace("'", '')
            if photo_list != 'Нет фото':
                photo_list = photo_list.split(', ')
            TelegramCommands.send_response(message, photo_list, response_string)
    else:
        bot.send_message(message.chat.id, EmptyHistoryException.__str__())


def short_history_message(message: types.Message):
    """
    Функция, срабатывающая по команде short_history.
    :param message: параметр, хранящий информацию о чате и последнем сообщении от пользователя.
    """
    response_string = db.database_get_short_history(message)
    if response_string:
        for request in response_string:
            bot.send_message(message.chat.id, request, disable_web_page_preview=True)
    else:
        bot.send_message(message.chat.id, EmptyHistoryException.__str__())


def clear_history(message: types.Message):
    """
    Функция, срабатывающая по команде clear_history.
    :param message: параметр, хранящий информацию о чате и последнем сообщении от пользователя.
    """
    if db.database_clear_history(message):
        bot.send_message(message.chat.id, 'Ваша история очищена!')
