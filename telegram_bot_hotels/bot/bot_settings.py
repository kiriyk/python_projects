# from telebot.types import telebot.types.ReplyKeyboardMarkup, telebot.types.KeyboardButton
from telebot import *
import telebot

bot_token = 'bot_token'

yes_no_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
yes_no_markup.row(telebot.types.KeyboardButton('Да'), telebot.types.KeyboardButton('Нет'))

hotel_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
hotel_markup.row(telebot.types.KeyboardButton('1'), telebot.types.KeyboardButton('2'), telebot.types.KeyboardButton('3'), telebot.types.KeyboardButton('4'),
                 telebot.types.KeyboardButton('5'), telebot.types.KeyboardButton('6'), telebot.types.KeyboardButton('7'))

photo_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
photo_markup.row(telebot.types.KeyboardButton('1'), telebot.types.KeyboardButton('2'), telebot.types.KeyboardButton('3'), telebot.types.KeyboardButton('4'),
                 telebot.types.KeyboardButton('5'))
photo_markup.row(telebot.types.KeyboardButton('6'), telebot.types.KeyboardButton('7'), telebot.types.KeyboardButton('8'), telebot.types.KeyboardButton('9'),
                 telebot.types.KeyboardButton('10'))

distance_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
distance_markup.row(telebot.types.KeyboardButton('1'), telebot.types.KeyboardButton('1.5'), telebot.types.KeyboardButton('2'), telebot.types.KeyboardButton('2.5'),
                    telebot.types.KeyboardButton('3'), telebot.types.KeyboardButton('3.5'), telebot.types.KeyboardButton('4'), telebot.types.KeyboardButton('4.5'),
                    telebot.types.KeyboardButton('5'))

year_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
year_markup.row(telebot.types.KeyboardButton('2021'), telebot.types.KeyboardButton('2022'),
                telebot.types.KeyboardButton('2023'), telebot.types.KeyboardButton('2024'))

month_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
month_markup.row(telebot.types.KeyboardButton('Январь'), telebot.types.KeyboardButton('Февраль'),
                 telebot.types.KeyboardButton('Март'), telebot.types.KeyboardButton('Апрель'))
month_markup.row(telebot.types.KeyboardButton('Май'), telebot.types.KeyboardButton('Июнь'),
                 telebot.types.KeyboardButton('Июль'), telebot.types.KeyboardButton('Август'))
month_markup.row(telebot.types.KeyboardButton('Сентябрь'), telebot.types.KeyboardButton('Октябрь'),
                 telebot.types.KeyboardButton('Ноябрь'), telebot.types.KeyboardButton('Декабрь'))

day_markup_var_1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
day_markup_var_1.row(telebot.types.KeyboardButton('1'), telebot.types.KeyboardButton('2'), telebot.types.KeyboardButton('3'), telebot.types.KeyboardButton('4'),
                     telebot.types.KeyboardButton('5'), telebot.types.KeyboardButton('6'), telebot.types.KeyboardButton('7'))
day_markup_var_1.row(telebot.types.KeyboardButton('8'), telebot.types.KeyboardButton('9'), telebot.types.KeyboardButton('10'), telebot.types.KeyboardButton('11'),
                     telebot.types.KeyboardButton('12'), telebot.types.KeyboardButton('13'), telebot.types.KeyboardButton('14'))
day_markup_var_1.row(telebot.types.KeyboardButton('15'), telebot.types.KeyboardButton('16'), telebot.types.KeyboardButton('17'), telebot.types.KeyboardButton('18'),
                     telebot.types.KeyboardButton('19'), telebot.types.KeyboardButton('20'), telebot.types.KeyboardButton('21'))
day_markup_var_1.row(telebot.types.KeyboardButton('22'), telebot.types.KeyboardButton('23'), telebot.types.KeyboardButton('24'), telebot.types.KeyboardButton('25'),
                     telebot.types.KeyboardButton('26'), telebot.types.KeyboardButton('27'), telebot.types.KeyboardButton('28'))
day_markup_var_1.row(telebot.types.KeyboardButton('29'), telebot.types.KeyboardButton('30'), telebot.types.KeyboardButton('31'))

day_markup_var_2 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
day_markup_var_2.row(telebot.types.KeyboardButton('1'), telebot.types.KeyboardButton('2'), telebot.types.KeyboardButton('3'), telebot.types.KeyboardButton('4'),
                     telebot.types.KeyboardButton('5'), telebot.types.KeyboardButton('6'), telebot.types.KeyboardButton('7'))
day_markup_var_2.row(telebot.types.KeyboardButton('8'), telebot.types.KeyboardButton('9'), telebot.types.KeyboardButton('10'), telebot.types.KeyboardButton('11'),
                     telebot.types.KeyboardButton('12'), telebot.types.KeyboardButton('13'), telebot.types.KeyboardButton('14'))
day_markup_var_2.row(telebot.types.KeyboardButton('15'), telebot.types.KeyboardButton('16'), telebot.types.KeyboardButton('17'), telebot.types.KeyboardButton('18'),
                     telebot.types.KeyboardButton('19'), telebot.types.KeyboardButton('20'), telebot.types.KeyboardButton('21'))
day_markup_var_2.row(telebot.types.KeyboardButton('22'), telebot.types.KeyboardButton('23'), telebot.types.KeyboardButton('24'), telebot.types.KeyboardButton('25'),
                     telebot.types.KeyboardButton('26'), telebot.types.KeyboardButton('27'), telebot.types.KeyboardButton('28'))
day_markup_var_2.row(telebot.types.KeyboardButton('29'), telebot.types.KeyboardButton('30'))

day_markup_var_3 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
day_markup_var_3.row(telebot.types.KeyboardButton('1'), telebot.types.KeyboardButton('2'), telebot.types.KeyboardButton('3'), telebot.types.KeyboardButton('4'),
                     telebot.types.KeyboardButton('5'), telebot.types.KeyboardButton('6'), telebot.types.KeyboardButton('7'))
day_markup_var_3.row(telebot.types.KeyboardButton('8'), telebot.types.KeyboardButton('9'), telebot.types.KeyboardButton('10'), telebot.types.KeyboardButton('11'),
                     telebot.types.KeyboardButton('12'), telebot.types.KeyboardButton('13'), telebot.types.KeyboardButton('14'))
day_markup_var_3.row(telebot.types.KeyboardButton('15'), telebot.types.KeyboardButton('16'), telebot.types.KeyboardButton('17'), telebot.types.KeyboardButton('18'),
                     telebot.types.KeyboardButton('19'), telebot.types.KeyboardButton('20'), telebot.types.KeyboardButton('21'))
day_markup_var_3.row(telebot.types.KeyboardButton('22'), telebot.types.KeyboardButton('23'), telebot.types.KeyboardButton('24'), telebot.types.KeyboardButton('25'),
                     telebot.types.KeyboardButton('26'), telebot.types.KeyboardButton('27'), telebot.types.KeyboardButton('28'))

day_markup_var_4 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
day_markup_var_4.row(telebot.types.KeyboardButton('1'), telebot.types.KeyboardButton('2'), telebot.types.KeyboardButton('3'), telebot.types.KeyboardButton('4'),
                     telebot.types.KeyboardButton('5'), telebot.types.KeyboardButton('6'), telebot.types.KeyboardButton('7'))
day_markup_var_4.row(telebot.types.KeyboardButton('8'), telebot.types.KeyboardButton('9'), telebot.types.KeyboardButton('10'), telebot.types.KeyboardButton('11'),
                     telebot.types.KeyboardButton('12'), telebot.types.KeyboardButton('13'), telebot.types.KeyboardButton('14'))
day_markup_var_4.row(telebot.types.KeyboardButton('15'), telebot.types.KeyboardButton('16'), telebot.types.KeyboardButton('17'), telebot.types.KeyboardButton('18'),
                     telebot.types.KeyboardButton('19'), telebot.types.KeyboardButton('20'), telebot.types.KeyboardButton('21'))
day_markup_var_4.row(telebot.types.KeyboardButton('22'), telebot.types.KeyboardButton('23'), telebot.types.KeyboardButton('24'), telebot.types.KeyboardButton('25'),
                     telebot.types.KeyboardButton('26'), telebot.types.KeyboardButton('27'), telebot.types.KeyboardButton('28'))
day_markup_var_4.row(telebot.types.KeyboardButton('29'))

price_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
price_markup.row(telebot.types.KeyboardButton('1000'), telebot.types.KeyboardButton('2000'), telebot.types.KeyboardButton('3000'),
                 telebot.types.KeyboardButton('4000'), telebot.types.KeyboardButton('5000'))
price_markup.row(telebot.types.KeyboardButton('6000'), telebot.types.KeyboardButton('7000'), telebot.types.KeyboardButton('8000'),
                 telebot.types.KeyboardButton('9000'), telebot.types.KeyboardButton('10000'))
price_markup.row(telebot.types.KeyboardButton('11000'), telebot.types.KeyboardButton('12000'), telebot.types.KeyboardButton('13000'),
                 telebot.types.KeyboardButton('14000'), telebot.types.KeyboardButton('15000'))

month_day_dict = {
    ('Январь', 'Март', 'Май', 'Июль', 'Август', 'Октябрь', 'Декабрь'): day_markup_var_1,
    ('Апрель', 'Июнь', 'Сентябрь', 'Ноябрь'): day_markup_var_2,
    'Февраль': day_markup_var_3
}

month_number_dict = {
    'Январь': 1, 'Февраль': 2, 'Март': 3, 'Апрель': 4, 'Май': 5, 'Июнь': 6, 'Июль': 7,
    'Август': 8, 'Сентябрь': 9, 'Октябрь': 10, 'Ноябрь': 11, 'Декабрь': 12
}

years_list = [2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030]

days_list = [day for day in range(1, 32)]

leap_year = (2020, 2024, 2028, 2032)

HELP_TEXT = 'Вот, что может бот тур-агенства "TooEasyTravel":\n' \
            '/low_price - топ самых дешевых отелей в городе\n' \
            '/high_price - топ самых дорогих отелей в городе\n' \
            '/best_deal - топ отелей, наиболее подходящих по цене и расположению от центра\n' \
            '/history - история поиска\n' \
            '/short_history - краткая история запросов\n' \
            '/help - узнать, что умеет бот\n'
