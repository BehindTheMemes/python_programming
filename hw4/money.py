#### Задание 2. Хешируемый класс-значение

# В файле hw4/money.py напишите класс Money с полями amount (целое число копеек) и currency (строка, например 'RUB').

# Требования:
    # - два объекта равны, если совпадают сумма и валюта; сравнение с объектом другого типа возвращает NotImplemented;
    # - объекты можно использовать как ключи словаря и элементы множества, контракт a == b  =>  hash(a) == hash(b) выполняется;
    # - после создания поля изменить нельзя: m.amount = 5 и m.extra = 1 вызывают AttributeError
        # (подсказка: __slots__ и __setattr__; внутри __init__ можно использовать object.__setattr__);
    # - m1 + m2 складывает суммы одной валюты и возвращает новый объект; для разных валют бросает ValueError;
    # - __repr__ возвращает `Money(1500, 'RUB').

# Также напишите функцию total_by_currency(payments), которая принимает список Money
# и возвращает словарь {валюта: Money} с суммой по каждой валюте.

class Money:
    __slots__ = ('amount', 'currency')

    def __init__(self, amount: int, currency: str):
        object.__setattr__(self, 'amount', amount)
        object.__setattr__(self, 'currency', currency)

    def __setattr__(self, name, value):
        raise AttributeError('Money is immutable')

    def __eq__(self, other):
        if not isinstance(other, Money):
            return NotImplemented

        return self.amount == other.amount and self.currency == other.currency

    def __hash__(self):
        return hash((self.amount, self.currency))

    def __add__(self, other):
        if not isinstance(other, Money):
            return NotImplemented

        if self.currency != other.currency:
            raise ValueError('Cannot add Money with different currencies')

        return Money(self.amount + other.amount, self.currency)

    def __repr__(self):
        return f"Money({self.amount}, {self.currency!r})"

def total_by_currency(payments):
    totals = {}

    for payment in payments:
        if payment.currency in totals:
            totals[payment.currency] = totals[payment.currency] + payment
        else:
            totals[payment.currency] = Money(
                payment.amount,
                payment.currency
            )

    return totals

if __name__ == '__main__':
    assert len({Money(100, 'RUB'), Money(100, 'RUB'), Money(100, 'USD')}) == 2
    prices = {Money(100, 'RUB'): 'сто рублей'}
    assert prices[Money(100, 'RUB')] == 'сто рублей'
    assert Money(100, 'RUB') + Money(50, 'RUB') == Money(150, 'RUB')
    for action in (lambda m: setattr(m, 'amount', 5), lambda m: setattr(m, 'extra', 1)):
        try:
            action(Money(1, 'RUB'))
            assert False, 'ожидали AttributeError'
        except AttributeError:
            pass
    try:
        Money(1, 'RUB') + Money(1, 'USD')
        assert False, 'ожидали ValueError'
    except ValueError:
        pass
    pays = [Money(100, 'RUB'), Money(5, 'USD'), Money(250, 'RUB')]
    assert total_by_currency(pays) == {'RUB': Money(350, 'RUB'), 'USD': Money(5, 'USD')}

# В комментарии (3-4 предложения) объясните, что сломалось бы, если бы поля можно было менять после того,
# как объект положили в множество или использовали как ключ. Сошлитесь на пример с Point из лекции.

# Если бы поля amount и currency можно было изменять после добавления
# объекта в множество или использования его в качестве ключа словаря,
# значение его хеша могло бы измениться, и Питон не смог бы корректно
# найти объект в исходной корзине хеш-таблицы. 
# Такая же проблема возникает с Point, если изменить координаты точки после
# добавления её в множество. Поэтому объекты, используемые как ключи
# словарей или элементы множеств, должны сохранять стабильный хеш.