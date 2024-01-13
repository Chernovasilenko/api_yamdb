# API для YaMDb
# Описание
YaMDb собирает отзывы пользователей на произведения. Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка».
В данном проекте реализовано API для этой платформы. С помощью API пользователи могут оставлять к произведениям текстовые отзывы и ставить произведению оценку в диапазоне от одного до десяти; из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв. Пользователи могут оставлять комментарии к отзывам. Добавлять произведения, категории и жанры может только администратор.
# Технологии
- Python 3.9
- Django 3.2.16
- Django REST Framework 3.12.4
- SQLite3
- JWT
# Установка
Клонировать репозиторий и перейти в него в командной строке:

```bash
git clone git@github.com:Chernovasilenko/api_yamdb
```

```bash
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```bash
python3 -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```
Выполнить миграции:

```bash
python3 manage.py migrate
```

Заполнить базу данных контентом из csv файлов:

```bash
python3 manage.py load_data
```

Запустить проект:

```bash
python3 manage.py runserver
```

# Примеры запросов к API

Получить список всех произведений (GET):

```
http://127.0.0.1:8000/api/v1/titles/
```

Получить список всех отзывов произведения (GET):

```
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
```
Подробная документация со всеми примерами запросов будет доступна после запуска проекта по адресу:

```
http://127.0.0.1:8000/redoc/
```

# Разработчики
- [Александр Черновасиленко](https://github.com/Chernovasilenko) - Тимлид/Python-разработчик
- [Александр Кузнецов](https://github.com/NotJustEspo) - Python-разработчик
- [Дора Логинова](https://github.com/DoraLoginova) - Python-разработчик
