from vixlib import TOKEN
from app.bot.helpers.client import Client
from vixlib.logging import setup_logging


if __name__ == '__main__':
    setup_logging()
    Client().run(TOKEN, root_logger=True)