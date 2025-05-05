from abc import ABC, abstractmethod
import random

# -------------------------
# 1. Интерфейс Итератора (Iterator)
# -------------------------

# Интерфейс Итератора определяет методы для обхода коллекции.
class Iterator(ABC):
    @abstractmethod
    def has_next(self):
        """
        Проверяет, есть ли еще элементы для обхода.
        Возвращает True, если есть следующий элемент, и False в противном случае.
        """
        pass

    @abstractmethod
    def next(self):
        """
        Возвращает следующий элемент коллекции.
        Если элементов больше нет, может возвращать None или выбрасывать исключение.
        """
        pass

# -------------------------
# 2. Интерфейс Коллекции (IterableCollection)
# -------------------------

# Интерфейс Коллекции определяет метод для создания итератора.
class IterableCollection(ABC):
    @abstractmethod
    def create_iterator(self, type_="sequential") -> Iterator:
        """
        Создает и возвращает объект итератора для обхода коллекции.
        Параметр type_ определяет тип итератора (например, последовательный, случайный).
        """
        pass

# -------------------------
# 3. Конкретная коллекция (ConcreteCollection)
# -------------------------

# Класс CityAttractions представляет конкретную коллекцию достопримечательностей.
class CityAttractions(IterableCollection):  # Реализует интерфейс IterableCollection
    def __init__(self):
        """
        Инициализирует коллекцию достопримечательностей.
        Каждая достопримечательность содержит список экспонатов.
        """
        self._attractions = {
            "Эрмитаж": ["Картина 1", "Картина 2", "Статуя 1"],
            "Исаакиевский собор": ["Мозаика 1", "Люстра", "Витраж"],
            "Петропавловская крепость": ["Пушка", "Музей истории"]
        }

    def create_iterator(self, type_="sequential"):
        """
        Создает и возвращает объект итератора в зависимости от типа обхода.
        - "sequential" — последовательный обход (пешком).
        - "bus" — обход на автобусе (только достопримечательности).
        - "random_walk" — случайный обход (случайные достопримечательности).
        """
        if type_ == "bus":
            return BusIterator(self._attractions)  # Используется BusIterator
        elif type_ == "random_walk":
            return RandomWalkIterator(self._attractions)  # Используется RandomWalkIterator
        return SequentialIterator(self._attractions)  # По умолчанию SequentialIterator

# -------------------------
# 4. Конкретные итераторы (ConcreteIterators)
# -------------------------

# Итератор для последовательного обхода (пешком)
class SequentialIterator(Iterator):
    def __init__(self, attractions):
        """
        Инициализирует итератор для последовательного обхода всех достопримечательностей и их экспонатов.
        """
        self._attractions = attractions
        self._keys = list(attractions.keys())  # Список ключей (достопримечательностей)
        self._current_attraction = 0  # Текущая достопримечательность
        self._current_exhibit = 0  # Текущий экспонат внутри достопримечательности

    def has_next(self):
        """
        Проверяет, есть ли еще достопримечательности для обхода.
        """
        return self._current_attraction < len(self._keys)

    def next(self):
        """
        Возвращает следующий элемент (достопримечательность + экспонат).
        Если все экспонаты одной достопримечательности закончились, переходит к следующей.
        """
        key = self._keys[self._current_attraction]
        exhibits = self._attractions[key]

        if self._current_exhibit < len(exhibits):
            exhibit = exhibits[self._current_exhibit]
            self._current_exhibit += 1
            return f"{key}: {exhibit}"
        else:
            self._current_attraction += 1
            self._current_exhibit = 0
            return self.next() if self.has_next() else None

# Итератор для обхода на автобусе (только достопримечательности)
class BusIterator(Iterator):
    def __init__(self, attractions):
        """
        Инициализирует итератор для обхода только по достопримечательностям без экспонатов.
        """
        self._attractions = attractions
        self._keys = list(attractions.keys())
        self._index = 0

    def has_next(self):
        """
        Проверяет, есть ли еще достопримечательности для обхода.
        """
        return self._index < len(self._keys)

    def next(self):
        """
        Возвращает название следующей достопримечательности.
        """
        key = self._keys[self._index]
        self._index += 1
        return key

# Итератор для случайной прогулки (заход в случайные достопримечательности)
class RandomWalkIterator(Iterator):
    def __init__(self, attractions):
        """
        Инициализирует итератор для случайного обхода достопримечательностей.
        Перемешивает список достопримечательностей для случайного порядка.
        """
        self._attractions = attractions
        self._keys = list(attractions.keys())
        random.shuffle(self._keys)  # Перемешиваем список достопримечательностей
        self._current_attraction = 0  # Текущая достопримечательность
        self._current_exhibit = 0  # Текущий экспонат внутри достопримечательности

    def has_next(self):
        """
        Проверяет, есть ли еще достопримечательности для обхода.
        """
        return self._current_attraction < len(self._keys)

    def next(self):
        """
        Возвращает следующий элемент (достопримечательность + экспонат).
        Если все экспонаты одной достопримечательности закончились, переходит к следующей.
        """
        key = self._keys[self._current_attraction]
        exhibits = self._attractions[key]

        if self._current_exhibit < len(exhibits):
            exhibit = exhibits[self._current_exhibit]
            self._current_exhibit += 1
            return f"{key}: {exhibit}"
        else:
            self._current_attraction += 1
            self._current_exhibit = 0
            return self.next() if self.has_next() else None

# -------------------------
# 5. Клиентский код (Client)
# -------------------------

def main():

    # Создаем объект коллекции
    city = CityAttractions()

    # Обходим коллекцию пешком
    print("Пешком:")
    iterator = city.create_iterator()  # Получаем итератор по умолчанию (SequentialIterator)
    while iterator.has_next():
        print(iterator.next())

    # Обходим коллекцию на автобусе
    print("\nНа автобусе:")
    bus_iterator = city.create_iterator("bus")  # Получаем BusIterator
    while bus_iterator.has_next():
        print(bus_iterator.next())

    # Обходим коллекцию случайным образом
    print("\nСлучайная прогулка:")
    random_walk_iterator = city.create_iterator("random_walk")  # Получаем RandomWalkIterator
    while random_walk_iterator.has_next():
        print(random_walk_iterator.next())

# Запуск приложения
main()