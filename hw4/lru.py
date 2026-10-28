#### Задание 5*. LRU-кэш на обычном словаре

# В файле hw4/lru.py реализуйте класс LRUCache(capacity): кэш ограниченного размера, который при переполнении
# выбрасывает элемент, к которому дольше всего не обращались (Least Recently Used). Такие кэши стоят перед
# базами данных, в браузерах и в functools.lru_cache.

# Требования:
    # - get(key, default=None) и put(key, value) работают за O(1) в среднем;
    # - обращение через get и перезапись через put делают ключ «самым свежим»;
    # - при добавлении нового ключа сверх capacity удаляется самый старый ключ;
    # - len(cache), key in cache (проверка не должна делать ключ свежим);
    # - используйте только обычный dict и то, что порядок вставки в нем гарантирован. OrderedDict использовать нельзя.

class LRUCache:
    def __init__(self, capacity):
        if capacity < 0:
            raise ValueError("capacity не может быть отрицательным")

        self.capacity = capacity
        self.cache = {}

    def get(self, key, default=None):
        if key not in self.cache:
            return default

        value = self.cache.pop(key)
        self.cache[key] = value  # Делаем ключ самым свежим
        return value

    def put(self, key, value):
        if self.capacity == 0:
            return

        if key in self.cache:
            del self.cache[key]
        elif len(self.cache) >= self.capacity:
            # Удаляем первый ключ в порядке вставки — самый старый
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]

        # Вставка в конец делает ключ самым свежим
        self.cache[key] = value

    def __len__(self):
        return len(self.cache)

    def __contains__(self, key):
        # Проверка наличия не обновляет порядок ключей
        return key in self.cache

if __name__ == '__main__':
    c = LRUCache(2)
    c.put('a', 1)
    c.put('b', 2)
    assert c.get('a') == 1        # теперь 'a' свежее, чем 'b'
    c.put('c', 3)                 # вытесняется 'b'
    assert 'b' not in c and c.get('a') == 1 and c.get('c') == 3
    c.put('a', 10)                # перезапись делает 'a' свежим
    c.put('d', 4)                 # вытесняется 'c'
    assert c.get('c') is None and c.get('a') == 10 and len(c) == 2

# В комментарии объясните, почему удаление самого старого элемента работает за O(1)
# и какую конструкцию вы для этого использовали.

# В Python 3.7+ словарь dict сохраняет порядок вставки ключей. 
# Конструкция next(iter(self.cache)) получает первый ключ словаря без перебора всех элементов, 
# т.е. за O(1). Затем del self.cache[oldest_key] удаляет элемент по ключу, тоже за O(1).