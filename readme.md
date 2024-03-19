# Telegram Auth Wall

Это пример приложения на FastAPI, которое прячет статический сайт за авторизацией через Телеграм.

Объясняю всё здесь: https://habr.com/ru/articles/801121/

![](https://habrastorage.org/r/w1560/getpro/habr/upload_files/c66/996/6b5/c669966b5a0d409c7521779dbbc91411.png)

Код предназначен для того, чтобы вы отредактировали его под свои задачи.


## Как настроить эту штучку

1. Отредактировать страницу входа в [`src/templates/login.html`](src/templates/login.html).
   Можно оставить всё как есть и вставить юзернейм бота на 54-й строке.
   Или сверстать свою страничку и [сгенерировать кнопку.](https://core.telegram.org/widgets/login)
2. Собрать список id пользователей в `whitelist.py`. 
3. Положить свои статические файлы в `site/`, либо поменять в [`src/__init__.py`](src/__init__.py) строку `'site/'`
   на нужный путь.

## Как запустить

1. Установить зависимости [через Poetry:](https://python-poetry.org/docs/)
   ```shell
   poetry install
   ```
2. Задать переменные окружения: случайную строку `JWT_SECRET_KEY` и токен бота `BOT_TOKEN`.
3. Запустить как обычное приложение FastAPI.

Например, быстро потестить приложение локально (на 80 порте, чтобы работал Telegram Login Widget) можно так:

```shell
sudo BOT_TOKEN=... JWT_SECRET_KEY=... uvicorn src:app --reload --port 80
```
