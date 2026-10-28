#### Задание 2 (обязательно). Свой баг-репорт 

# Самостоятельно придумать и оформить один новый баг на ту же тему (изменяемость/alias/hashable), 
# которого не было в каталоге семинара. Файл hw3/my_bug.py должен содержать три части подряд:
    # багованный код (5-10 строк);
    # комментарий в 2-3 предложения: что происходит и почему;
    # исправленная версия. 
# Запрещается просто переформулировать чужой пример с семинара 
# другими именами переменных - цель в том, чтобы придумать свою ситуацию, 
# а не скопировать готовый.

# Баг
colors = ["red", "green", "blue"]
empty = []
palette = {}
for color in colors:
    palette[color] = empty
palette["red"].append("#FF0000")
print(palette)

# Объяснение
    # Всем ключам словаря присваивается один и тот же изменяющийся список empty.
    # Поэтому изменение palette["red"] также изменяет palette["green"] и palette["blue"].


# Исправленный код
colors = ["red", "green", "blue"]
palette = {}
for color in colors:
    palette[color] = []
palette["red"].append("#FF0000")
print(palette)

#### Задание 3 (дополнительно, без дедлайна)

# Найти один из багов семинара (например, mutable default argument) в реальном 
# открытом проекте на GitHub (через поиск по коду или issue-трекер) 
# и принести ссылку на строку кода. Не оценивается, но хорошо показывает, 
# что эти баги реальны, а не выдуманы для учебных целей.

# Ссылка на фрагмент кода:
# https://github.com/run-llama/llama_index/blob/f475afd8a9bbda84f252567e045d89d07b5701b3/llama-index-instrumentation/src/llama_index_instrumentation/dispatcher.py#L93-L94

# Ссылка на соответствующую issue:
# https://github.com/run-llama/llama_index/issues/22705