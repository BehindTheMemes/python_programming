# Задание 1 (обязательно). Мини-скрипт с обоснованным выбором коллекций
# Написать трекер книг/покупок/участников (тема на выбор — любая предметная область с «записями»), в котором сознательно использованы: 
    # • list — для меняющегося набора записей;
    # • tuple — для фиксированной структуры одной записи (например (id, name, year));
    # • dict — для быстрого поиска по ключу;
    # • set — где важна только уникальность.
# К коду - короткий README.md (3–5 предложений), объясняющий, почему выбрана 
# именно эта коллекция для каждого случая — это прямая тренировка перед аналогичным пунктом 
# в чек-листе проекта на автомате. Код должен 100% избегать всех ловушек с семинара: 
# никаких mutable default arguments, неосознанных alias’ов, list в качестве ключа и т.п.

books = [] # list
books_id_list = {} # dict
genres = set() # set

def add_book(books, books_id_list, genres, id, author, title, year, genre):
    book = (id, author, title, year)
    books.append(book)
    books_id_list[id] = book
    genres.add(genre)

add_book(books, books_id_list, genres, 1, "Эрих Мария Ремарк", "На Западном фронте без перемен", 1928, "роман")
add_book(books, books_id_list, genres, 2, "Анджей Сапковский", "Последнее желание", 1993, "фэнтези")
add_book(books, books_id_list, genres, 3, "ozon671games3", "Тихий Дэн", 2023, "триллер")
add_book(books, books_id_list, genres, 4, "Евгений Замятин", "Мы", 1920, "роман")

print("Список всех книг:")
print(books)
print("\nКнига под номером 2:")
print(books_id_list[2])
print("\nУникальные жанры:")
print(genres)

add_book(books, books_id_list, genres, 5, "Майк Омер", "Внутри убийцы", 2018, "детектив")

print("\nПосле добавления ещё одной книги:")
print(books)
print(books_id_list)
print(genres)

