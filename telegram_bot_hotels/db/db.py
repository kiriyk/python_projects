from peewee import *
from telegram import *
# from telegram import Message
import telegram

from bot.Exceptions import EmptyHistoryException

db = SqliteDatabase('db/users.db')


class Users(Model):
    """
    Класс, отвечающий за таблицу Users в базе данных.
    """
    id = PrimaryKeyField()
    userid = CharField()
    username = CharField()

    class Meta:
        database = db


class Request(Model):
    """
    Класс, отвечающий за таблицу Request в базе данных.
    """
    id = PrimaryKeyField()
    userid = CharField()
    name = TextField()
    address = TextField()
    user_rating = IntegerField()
    star = IntegerField()
    distance_from_city_centre = TextField()
    check_in = DateField()
    check_out = DateField()
    price = TextField()
    total_price = TextField()
    photo = TextField()

    class Meta:
        database = db


class ShortRequest(Model):
    """
    Класс, отвечающий за таблицу short_request в базе данных.
    """
    id = PrimaryKeyField()
    userid = CharField()
    hotelinfo = TextField()

    class Meta:
        database = db


class DatabaseHandler():
    """
    Класс, реализующий методы взаимодействия с таблицами в базе данных.
    """
    req = Request
    short_req = ShortRequest
    user = Users

    @classmethod
    def database_user_reg(cls, **kwargs):
        """
        Метод, реализующий запись новых пользователей в таблицу.
        """
        with db:
            cls.user.create(**kwargs)

    @classmethod
    def database_write_hotel(cls, **kwargs):
        """
        Метод, реализующий запись информации об отелях в таблицу.
        """
        with db:
            cls.req.create(**kwargs)

    @classmethod
    def database_write_short_req(cls, **kwargs):
        """
        Метод, реализующий краткую запись информации о запросе пользователя.
        """
        with db:
            cls.short_req.create(**kwargs)

    @classmethod
    def database_get_hotels(cls, message) -> list or None:
        """
        Метод, реализующий получение информации о запрошенных отелях из базы данных.
        :param message: параметр, хранящий информацию о чате и последнем сообщении от пользователя.
        :return: список отелей с информацией о них.
        """
        with db:
            result = cls.req.select().where(cls.req.userid == str(message.chat.id)).dicts()
            try:
                result_list = [hotel for hotel in result]
                if not result_list:
                    raise EmptyHistoryException
                return result_list
            except EmptyHistoryException:
                return None

    @classmethod
    def database_get_short_history(cls, message) -> list or None:
        """
        Метод, реализующий получение кракой информации о запросе пользователя.
        :param message: параметр, хранящий информацию о чате и последнем сообщении от пользователя.
        :return: список с информацией о запросах.
        """
        with db:
            result = cls.short_req.select().where(cls.short_req.userid == str(message.chat.id))
            try:
                result_list = [request.hotelinfo for request in result]
                if not result_list:
                    raise EmptyHistoryException
                return result_list
            except EmptyHistoryException:
                return None

    @classmethod
    def database_clear_history(cls, message):
        """
        Метод, реализующий очистку истории запросов пользователя.
        :param message: параметр, хранящий информацию о чате и последнем сообщении от пользователя.
        """
        with db:
            cls.req.delete().where(cls.req.userid == str(message.chat.id)).execute()
            cls.short_req.delete().where(cls.short_req.userid == str(message.chat.id)).execute()
            return True


if __name__ == '__main__':
    db.connect()
    db.create_tables([Users, Request])
