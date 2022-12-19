class NoCityFoundException(Exception):
    @classmethod
    def __str__(cls):
        return f'Город не найден!'


class DateDifferenceException(Exception):
    @classmethod
    def __str__(cls):
        return f'Ошибка: дата выезда меньше даты заезда\nПовторите ввод!'


class MinPriceException(Exception):
    @classmethod
    def __str__(cls):
        return f'Минимальная цена введена неверно, введите заново!'


class MaxPriceException(Exception):
    @classmethod
    def __str__(cls):
        return f'Максимальная цена введена неверно, введите заново!'


class PriceDifferenceException(Exception):
    @classmethod
    def __str__(cls):
        return f'Минимальная цена выше максимальной! Повторите ввод.'


class DistanceException(Exception):
    @classmethod
    def __str__(cls):
        return f'Расстояние до центра введено неверно!'


class WrongNumberException(Exception):
    @classmethod
    def __str__(cls):
        return f'Введено некорректное число, повторите ввод!'


class EmptyHistoryException(Exception):
    @classmethod
    def __str__(cls):
        return 'История запросов пуста.'

