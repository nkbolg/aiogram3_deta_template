import logging

from aiogram import Bot, Dispatcher
from fastapi import FastAPI
from basic_handlers import router as basic_router
from config import Settings


def get_webhook_path(conf):
    return f"/bot/{conf.bot_token.get_secret_value()}"


def get_webhook_url(conf, webhook_path):
    return conf.deta_space_app_hostname + webhook_path


def setup_dispatcher():
    """Точка входа в приложение"""

    # включение логирования
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s: "
               "%(filename)s: "
               "%(levelname)s: "
               "%(funcName)s(): "
               "%(lineno)d:\t"
               "%(message)s",
    )

    # получение класса хранящего конфигурируемые параметры
    sett = Settings()

    logging.info("Application started")

    # создание и запуск объекта бота
    bot = Bot(token=sett.bot_token.get_secret_value())
    dispatcher = Dispatcher()

    dispatcher.include_router(basic_router)

    return dispatcher, bot


def setup_app():
    app = FastAPI(openapi_url=None, docs_url=None, redoc_url=None)
    sett = Settings()

    webhook_path = get_webhook_path(sett)
    webhook_url = get_webhook_url(sett, webhook_path)

    dispatcher, bot = setup_dispatcher()

    @app.post(webhook_path)
    async def bot_webhook(update: dict):
        res = await dispatcher.feed_webhook_update(bot, update)
        return res

    @app.get("/")
    async def setup():
        await bot.set_webhook(url=webhook_url, drop_pending_updates=True)
        return "Webhook Updated"

    return app


app = setup_app()
