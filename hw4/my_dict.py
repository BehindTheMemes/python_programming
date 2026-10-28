#### Задание 1. Своя хеш-таблица

# В файле hw4/my_dict.py реализуйте класс MyDict: упрощенный словарь на основе хеш-таблицы с цепочками.
# Внутри класса нельзя использовать dict и set, только списки и кортежи.

#Требования:
# - корзины хранятся в списке списков, номер корзины: hash(key) % len(self._buckets);
# - при коллизии пары (key, value) лежат в одной корзине, нужный ключ ищется через ==;
# - операции: d[key] = value, d[key], del d[key], key in d, len(d), d.get(key, default=None);
# - отсутствующий ключ в d[key] и del d[key] вызывает KeyError;
# - когда число элементов становится больше 2/3 от числа корзин, число корзин увеличивается в 2 раза и все пары
# раскладываются заново;
# - метод stats() возвращает кортеж (число корзин, число элементов, длина самой длинной корзины);
# - __repr__ выводит содержимое в виде MyDict({'a': 1, 'b': 2}).

from time import perf_counter

class MyDict:
    def __init__(self, size=8):
        if size < 1:
            raise ValueError("Размер таблицы должен быть положительным")
        self._buckets = [[] for _ in range(size)]
        self._entries = []
        self._len = 0

    def _find_index(self, key):
        bucket = self._buckets[hash(key) % len(self._buckets)]
        for idx in bucket:
            entry = self._entries[idx]
            if entry is not None and entry[0] == key:
                return idx
        return -1

    def _resize(self, new_size):
        new_buckets = [[] for _ in range(new_size)]
        for idx, entry in enumerate(self._entries):
            if entry is not None:
                new_buckets[hash(entry[0]) % new_size].append(idx)
        self._buckets = new_buckets

    def __setitem__(self, key, value):
        idx = self._find_index(key)
        if idx != -1:
            self._entries[idx][1] = value
            return

        self._entries.append([key, value])
        idx = len(self._entries) - 1
        self._buckets[hash(key) % len(self._buckets)].append(idx)
        self._len += 1

        if self._len * 3 > len(self._buckets) * 2:
            self._resize(len(self._buckets) * 2)

    def __getitem__(self, key):
        idx = self._find_index(key)
        if idx == -1:
            raise KeyError(key)
        return self._entries[idx][1]

    def __delitem__(self, key):
        bucket_idx = hash(key) % len(self._buckets)
        bucket = self._buckets[bucket_idx]

        for pos, idx in enumerate(bucket):
            entry = self._entries[idx]
            if entry is not None and entry[0] == key:
                bucket.pop(pos)
                self._entries[idx] = None
                self._len -= 1
                return

        raise KeyError(key)

    def __contains__(self, key):
        return self._find_index(key) != -1

    def __len__(self):
        return self._len

    def get(self, key, default=None):
        idx = self._find_index(key)
        if idx == -1:
            return default
        return self._entries[idx][1]

    def stats(self):
        longest = 0
        for bucket in self._buckets:
            if len(bucket) > longest:
                longest = len(bucket)
        return (len(self._buckets), self._len, longest)

    def __repr__(self):
        parts = []
        for key, value in self.items():
            parts.append(f"{key!r}: {value!r}")
        return "MyDict({" + ", ".join(parts) + "})" 

    # 1* – порядок вставки, как у настоящего dict
    def keys(self):
        return [entry[0] for entry in self._entries if entry is not None]

    def values(self):
        return [entry[1] for entry in self._entries if entry is not None]

    def items(self):
        return [(entry[0], entry[1]) for entry in self._entries if entry is not None]

    def __iter__(self):
        return iter(self.keys())

class BadHash:
    """Ключи с одинаковым хешем для проверки коллизий."""

    def __init__(self, value):
        self.value = value

    def __hash__(self):
        return 42

    def __eq__(self, other):
        return isinstance(other, BadHash) and self.value == other.value

    def __repr__(self):
        return f"BadHash({self.value})"

if __name__ == '__main__':
    d = MyDict()
    for i in range(1000):
        d[f'key{i}'] = i
    assert len(d) == 1000
    assert d['key42'] == 42
    assert 'key7' in d and 'nope' not in d
    d['key42'] = -1
    assert d['key42'] == -1 and len(d) == 1000
    del d['key42']
    assert 'key42' not in d and len(d) == 999
    assert d.get('nope') is None and d.get('nope', 0) == 0
    for bad in (lambda: d['nope'], lambda: d.__delitem__('nope')):
        try:
            bad()
            assert False, 'ожидали KeyError'
        except KeyError:
            pass
    buckets, size, longest = d.stats()
    assert size == 999 and size <= buckets * 2 / 3
    print("Статистика строковых ключей:", d.stats())

    # Проверка сохранения порядка вставки
    order = MyDict()
    order['a'] = 1
    order['b'] = 2
    order['c'] = 3
    order['b'] = 20
    del order['a']
    order['d'] = 4

    assert order.keys() == ['b', 'c', 'd']
    assert order.values() == [20, 3, 4]
    assert order.items() == [('b', 20), ('c', 3), ('d', 4)]
    assert list(order) == ['b', 'c', 'd']
    assert repr(order) == "MyDict({'b': 20, 'c': 3, 'd': 4})"
    print("Проверка порядка:", order)

    # Эксперимент: 1000 ключей с одинаковым хешем
    bad = MyDict()
    start = perf_counter()
    for i in range(1000):
        bad[BadHash(i)] = i
    elapsed = perf_counter() - start

    print("Статистика одинаковых хешей:", bad.stats())
    print(f"Время вставки 1000 ключей: {elapsed:.6f} с")
    assert len(bad) == 1000
    assert bad[BadHash(42)] == 42

# Ответьте в комментарии в конце файла (2-3 предложения на вопрос):
# 1. Почему при увеличении таблицы пары нельзя просто скопировать в корзины с теми же номерами?
    # При увеличении таблицы меняется количество корзин, поэтому
    # результат hash(key) % len(self._buckets) может измениться.
    # Поэтому элементы необходимо распределить по новым корзинам заново.
# 2. Что показывает `stats()` для 1000 строковых ключей и что он покажет, если ключами будут объекты,
# у которых `__hash__` всегда возвращает 42? Проверьте экспериментом, замерьте время вставки 1000 таких ключей.
    # Для ключей с одинаковым хешем результат будет (2048, 1000, 1000),
    # поскольку все элементы попадут в одну корзину.
    # Время вставки: 0.127499 с

# 1* Добавьте keys(), values(), items() и __iter__, которые возвращают элементы в порядке вставки,
# как настоящий dict. Порядок должен сохраняться после увеличения таблицы и корректно работать после удаления.
# Подсказка: вспомните схему компактного словаря с лекции (массив индексов + плотный массив записей).

