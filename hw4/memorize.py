#### Задание 4. Кэширование через замыкание

# В файле hw4/memoize.py напишите функцию memoize(func), которая возвращает новую функцию с кэшем результатов.
# Используйте замыкание: кэш (словарь) живет в объемлющей функции, а не в глобальной переменной.

# Требования:
    # - ключ кэша строится из позиционных и именованных аргументов, f(1, b=2) и f(1, b=3) кэшируются отдельно;
    # - если аргументы нехешируемые (например, список), функция вызывается без кэша и не падает;
    # - у возвращаемой функции есть атрибуты hits и misses (число попаданий и промахов кэша)
        # и метод cache_clear(), который очищает кэш и обнуляет счетчики (вспомните __dict__ у функций);
    # - у возвращаемой функции сохраняются __name__ и __doc__ исходной.

import time
from functools import wraps

def memoize(func):
    cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            key = (args, tuple(sorted(kwargs.items())))
            hash(key)
        except TypeError:
            # Аргументы нехешируемые — вызываем функцию без кэша
            return func(*args, **kwargs)

        if key in cache:
            wrapper.hits += 1
            return cache[key]
        
        wrapper.misses += 1
        result = func(*args, **kwargs)
        cache[key] = result
        return result

    wrapper.hits = 0
    wrapper.misses = 0

    def cache_clear():
        cache.clear()
        wrapper.hits = 0
        wrapper.misses = 0

    wrapper.cache_clear = cache_clear
    return wrapper

if __name__ == '__main__':
    calls = []

    def slow_square(x, power=2):
        '''Возводит в степень.'''
        calls.append(x)
        return x ** power

    sq = memoize(slow_square)
    assert sq(3) == 9 and sq(3) == 9 and sq(3, power=3) == 27
    assert calls == [3, 3]
    assert (sq.hits, sq.misses) == (1, 2)
    assert sq.__name__ == 'slow_square' and sq.__doc__ == 'Возводит в степень.'
    total = memoize(sum)
    assert total([1, 2, 3]) == 6 and total([1, 2, 3]) == 6   # нехешируемый аргумент: вызов без кэша
    assert (total.hits, total.misses) == (0, 0)
    sq.cache_clear()
    assert (sq.hits, sq.misses) == (0, 0)
    sq(3)
    assert calls[-1] == 3

# Эксперимент с рекурсией. Есть рекурсивная функция:

def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

# Сравните два варианта и для каждого выведите misses после вызова с n = 30 и время работы:

fast_fib = memoize(fib)     # вариант A – измеряем до переопределения имени fib
start = time.perf_counter()
fast_fib(30)
time_a = time.perf_counter() - start
misses_a = fast_fib.misses

fib = memoize(fib)          # вариант B – заменяем глобальное имя fib обёрткой
start = time.perf_counter()
fib(30)
time_b = time.perf_counter() - start
misses_b = fib.misses

print(f"A: misses={misses_a}, время={time_a:.6f} с")
print(f"B: misses={misses_b}, время={time_b:.6f} с")

# Один из вариантов ускоряет вычисление в тысячи раз, другой почти не помогает. В комментарии объясните почему,
# используя правило LEGB: какое имя ищет рекурсивный вызов fib(n - 1) внутри функции и в какой момент.

# Имя fib не является локальным именем функции, поэтому Python ищет его в глобальной области видимости модуля 
# во время выполнения рекурсивного вызова, а не при первоначальном определении функции.
# В варианте A глобальное имя fib всё ещё ссылается на исходную функцию, поэтому рекурсия обходит кэш, 
# в то время как в варианте B глобальное имя fib уже ссылается на обёртку memoize, 
# поэтому каждый рекурсивный вызов проходит через кэш.