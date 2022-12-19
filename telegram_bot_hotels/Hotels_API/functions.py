def key_search(key_to_find: str, dictionary: dict) -> str or None:
    """
    Метод рекурсивного поиска значения по ключу в словаре.

    :param key_to_find: заданный для поиска ключ.
    :param dictionary: словарь, в котором необходимо найти значение.
    :return result: найденное значение, в противном случае - None.
    """
    if key_to_find in dictionary.keys():
        return dictionary.get(key_to_find)

    for key in dictionary.values():
        if isinstance(key, dict):
            result = key_search(key_to_find, key)
            if result:
                break
    else:
        return None

    return result
