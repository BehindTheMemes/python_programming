#### Задание 3. Поисковый индекс

# В файле hw4/search_index.py реализуйте класс SearchIndex: простую поисковую систему по текстовым документам
# на основе инвертированного индекса (словарь «слово -> множество id документов»). Так устроен поиск
# в поисковиках, IDE и базах данных.

# Требования:
# - add(doc_id, text) добавляет документ. Слова приводятся к нижнему регистру, разделители и знаки препинания
  # отбрасываются (используйте re.findall(r'\w+', text.lower())). 
  # Повторное добавление того же doc_id заменяет старый текст;
# - search_all(*words) возвращает множество id документов, в которых есть все слова;
# - search_any(*words) возвращает множество id документов, в которых есть хотя бы одно слово;
# - remove(doc_id) удаляет документ из индекса; слово, которое больше не встречается ни в одном документе,
  # должно исчезнуть из индекса полностью;
# - top_words(n) возвращает n самых частых слов по всем документам в виде списка пар (слово, количество);
# - поиск по словам не должен перебирать все документы: сложность search_* зависит от числа слов в запросе
  # и размера найденных множеств, а не от общего числа документов.

import re
from collections import Counter

class SearchIndex:
    # Поисковый индекс на основе инвертированного индекса.
    # documents хранит частоты слов для каждого документа,
    # inverted_index хранит множество ID документов для каждого слова,
    # word_counts хранит суммарное количество вхождений каждого слова
    
    def __init__(self):
        self.documents = {}
        self.inverted_index = {}
        self.word_counts = Counter()

    def add(self, doc_id, text):
        # Добавляет документ или заменяет существующий
        if doc_id in self.documents:
            self.remove(doc_id)

        words = Counter(re.findall(r'\w+', text.lower()))
        self.documents[doc_id] = words

        for word, count in words.items():
            self.inverted_index.setdefault(word, set()).add(doc_id)
            self.word_counts[word] += count

    def search_all(self, *words):
        # Возвращает ID документов, содержащих все указанные слова
        if not words:
            return set()

        words = [word.lower() for word in words]

        # Если слова нет в индексе, пересечение пустое
        if any(word not in self.inverted_index for word in words):
            return set()

        # Начало с самого маленького множества
        words.sort(key=lambda word: len(self.inverted_index[word]))

        result = self.inverted_index[words[0]].copy()

        for word in words[1:]:
            result.intersection_update(self.inverted_index[word])
            if not result:
                break

        return result

    def search_any(self, *words):
        # Возвращает ID документов, содержащих хотя бы одно слово
        result = set()

        for word in words:
            result.update(self.inverted_index.get(word.lower(), set()))

        return result

    def remove(self, doc_id):
        # Удаляет документ и очищает индекс от неиспользуемых слов
        if doc_id not in self.documents:
            return

        words = self.documents.pop(doc_id)

        for word, count in words.items():
            doc_ids = self.inverted_index[word]
            doc_ids.remove(doc_id)

            self.word_counts[word] -= count

            if not doc_ids:
                del self.inverted_index[word]

            if self.word_counts[word] == 0:
                del self.word_counts[word]

    def top_words(self, n):
        # Возвращает n самых частых слов и их суммарные частоты
        if n <= 0:
            return []

        return sorted(
            self.word_counts.items(),
            key=lambda item: (-item[1], item[0])
        )[:n]

    def search_ranked(self, query, limit=10):
        # Возвращает ID документов по убыванию релевантности
        if limit <= 0:
            return []

        query_words = Counter(re.findall(r'\w+', query.lower()))
        scores = Counter()

        for word, query_count in query_words.items():
            for doc_id in self.inverted_index.get(word, set()):
                scores[doc_id] += (
                    self.documents[doc_id][word]
                )

        return sorted(
            scores,
            key=lambda doc_id: (-scores[doc_id], doc_id)
        )[:limit]

if __name__ == '__main__':
    idx = SearchIndex()
    idx.add(1, 'Python is a programming language.')
    idx.add(2, 'A dict is a hash table; a set is a hash table too!')
    idx.add(3, 'Python dict and set are fast.')
    assert idx.search_all('python') == {1, 3}
    assert idx.search_all('dict', 'set') == {2, 3}
    assert idx.search_all('python', 'hash') == set()
    assert idx.search_any('language', 'fast') == {1, 3}
    assert idx.search_all('PYTHON') == {1, 3}
    assert idx.search_all('nothing') == set()
    assert idx.top_words(2) == [('a', 5), ('is', 3)]
    idx.remove(1)
    assert idx.search_all('python') == {3}
    assert idx.search_any('language', 'programming') == set()
    idx.add(3, 'Totally new text')
    assert idx.search_all('python') == set()
    assert idx.search_all('new') == {3}

# Подумайте, какие структуры данных хранить, чтобы remove и повторный add работали без перебора всего индекса.
# Выбор коротко обоснуйте в docstring класса.

# 3*. Добавьте search_ranked(query, limit=10): принимает строку запроса и возвращает список id документов,
# отсортированных по релевантности. Релевантность документа: сумма количеств вхождений слов запроса в документе.
# Документы без единого слова запроса в результат не попадают; при равной релевантности первым идет меньший id.