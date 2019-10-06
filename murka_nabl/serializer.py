from django.db.models import QuerySet


class Serializer:
    """
    Серелизатор данных
    """

    def __init__(self, data, allowed, image_size=None, add_static=None, add_children=None):
        """
        :param data: Объект или кверисет объектов
        :param allowed: Что хотим получить из этого объекта
        :param image_size: В каком виде нам нужны картинки
        Пример:
            Serializer(
                User.objects.filter(**filter),
                (
                    'username',
                    'guid',
                    'avatar',
                    {
                        'game': ['game_id', 'title'],
                        'category': [
                            'category',
                            'internal_name',
                        ],
                    },
                ),
                {
                    'avatar': 'icon',
                }
            )
         Тем самым на выходе мы получим от пользователей только имя, гуид и аватарку, при этом аватарка будет самой
         маленькой.
        """
        if image_size is None:
            image_size = {}

        if add_static is None:
            add_static = {}

        if add_children is None:
            add_children = {}

        self.add_static = add_static
        self.image_size = image_size
        self.add_children = add_children
        self.allowed = allowed
        self.data = data

    def __filter(self, item, name=''):
        """
        Обработка кастомных типов данных.
        :param item: Содержимое поля из модели
        :param name: Имя этого поля
        на выходе получаем то, что можно преобразовать в JSON
        """

        if hasattr(item, '__dict__'):
            # Проверка на класс
            return item.__str__()

        return item

    def __getter(self, obj):
        """
        Вытаскиваем из модели то что нам нужно
        :param obj: Объект модели
        :return: dict готовый на выход
        """
        result = {}
        for item in self.allowed:
            if isinstance(item, str):
                result.update({
                    item: self.__filter(
                        getattr(obj, item, ''))
                })
            else:
                for key in item.keys():
                    if 'ManyRelatedManager' in str(type(getattr(obj, key))) \
                            or 'RelatedManager' in str(type(getattr(obj, key))):
                        _many_result = []
                        for many_item in getattr(obj, key).all():
                            many_ser_object = Serializer(many_item, item[key])
                            _many_result += many_ser_object.serialize()

                        result.update({
                            key: _many_result
                        })
                        continue

                    ser_object = Serializer(getattr(obj, key), item[key])
                    try:
                        _data = ser_object.serialize()[0]
                    except IndexError:
                        _data = {}

                    result.update({
                        key: _data
                    })

        if self.add_static:
            result.update(self.add_static)

        return result

    def serialize(self):
        """
        Внешняий метод, запускающий серелизацию.
        :return:
        """
        # Если дата вдруг пришла пустая. Ибо тот же .first() при пустате вернет None
        if self.data is None:
            return []

        # Если нам придет список объектов
        if isinstance(self.data, QuerySet):
            result = []
            for item in self.data:
                result.append(self.__getter(item))

            return result

        # Ну или объект всего 1
        return [self.__getter(self.data)]
