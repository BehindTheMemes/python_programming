#### Задание 6*. Конфиг с доступом через точку

# В файле hw4/config.py напишите класс Config, который оборачивает вложенный словарь (например, прочитанный из JSON)
# и дает доступ к значениям через атрибуты, на чтение и на запись:

class Config:
    def __init__(self, data):
        # Используется object.__setattr__, чтобы не вызвать __setattr__
        # при создании внутреннего атрибута
        object.__setattr__(self, '_data', data)

    def __getattr__(self, name):
        # Вызывается, если обычным способом атрибут не найден
        data = object.__getattribute__(self, '_data')

        if name not in data:
            raise AttributeError(
                f"{type(self).__name__!s} has no attribute {name!r}"
            )

        value = data[name]

        # Вложенный словарь оборачивается только при обращении к нему
        if isinstance(value, dict):
            return Config(value)

        return value

    def __setattr__(self, name, value):
        # Все пользовательские атрибуты записываются в исходный словарь
        data = object.__getattribute__(self, '_data')
        data[name] = value

    def __dir__(self):
        # Ключи словаря добавляются к стандартным именам атрибутов
        data = object.__getattribute__(self, '_data')
        return sorted(set(object.__dir__(self)) | set(data.keys()))

    def to_dict(self):
        return object.__getattribute__(self, '_data')

if __name__ == '__main__':
    raw = {'db': {'host': 'localhost', 'port': 5432}, 'debug': True}
    cfg = Config(raw)
    assert cfg.debug is True
    assert cfg.db.host == 'localhost' and cfg.db.port == 5432
    assert getattr(cfg, 'timeout', 30) == 30
    assert hasattr(cfg.db, 'user') is False
    cfg.db.port = 6543                    # запись меняет исходный словарь
    assert raw['db']['port'] == 6543
    cfg.timeout = 10
    assert raw['timeout'] == 10
    assert cfg.to_dict() is raw
    assert 'db' in dir(cfg)               # подсказка: метод __dir__

# Требования: используйте __getattr__ и __setattr__, вложенные словари оборачивайте в Config при обращении,
# для отсутствующего ключа бросайте AttributeError. 

# В комментарии объясните:
# 1. почему hasattr и getattr со значением по умолчанию перестанут работать, если бросать KeyError;

# hasattr(obj, name) возвращает False, если при обращении к атрибуту возникает AttributeError. 
# Если выбросить KeyError, исключение не будет обработано функцией hasattr, и программа завершится с ошибкой.

# 2. как вы избежали бесконечной рекурсии при обращении к собственному атрибуту, в котором хранится словарь.

# Для обращения к собственному атрибуту используется object.__getattribute__(self, '_data'), 
# который получает внутренний атрибут напрямую, минуя пользовательскую логику __getattr__ 
# и избегая бесконечной рекурсии.