from vixlib import TOKEN
from app.bot.helpers.client import Client


if __name__ == '__main__':
    Client().run(TOKEN, root_logger=True)