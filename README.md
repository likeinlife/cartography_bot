# Description

Телеграм-бот, написанный на aiogram3, для получения координат по номенклатуре топографической карты, и наоборот

# Installation & launch

1. `git clone git@github.com:likeinlife/cartography_bot.git` - склонируйте репозиторий
2. `poetry install` - установите все необходимые зависимости с помощью poetry
3. Создайте `.env` файл, ориентируясь на шаблон `sample.env`
4. `poetry shell` - при необходимости, активируйте виртуальное окружение
5. `make` - запустите проект.

# Env

- BOT_TOKEN - bot token
- ADMIN_ID - admin telegram id
- DEV_MODE - enable dev mode(enable some commands)
- PUBLIC - enable public use
- DISABLE_STREAM_HANDLER - disable stream logging output

# Screenshot

![](./static/telegram_screenshot.png)
