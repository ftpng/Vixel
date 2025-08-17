import os
from typing import Text
from dotenv import load_dotenv; load_dotenv()


TOKEN: Text = os.getenv("TOKEN")
LOGS_DIR: Text = os.getenv("LOGS_DIR")
DIR: Text = os.getenv("DIR")

SUPPORT_SERVER: str = "https://discord.gg/ST4zHBvKYd"
LOGO: str = "https://media.discordapp.net/attachments/1403695079981449246/1403871541229522994/logo_aqua.png?ex=689920c2&is=6897cf42&hm=63191adf7dcfb6b21f23a3acba3b7fc901a9805cf356cdfcf542e8887c60e3f1&=&format=webp&quality=lossless&width=960&height=960"
INVITE: str = "https://discord.com/oauth2/authorize?client_id=1392765255540674602&permissions=277025770560&integration_type=0&scope=bot"

HEAD_IMAGE = "https://cravatar.eu/helmavatar/"

EMBED_COLOR = 0x55FFFF
LIGHT_GREEN = 0x55FF55
LIGHT_RED = 0xFF5555

GREEN_DOT: int = "<:GreenDot:1404572042631581726>"
RED_DOT: int = "<:RedDot:1404572039947223093>"

ERROR_MESSAGE: str = (
    "An error has occurred while running your command, please try again!\n"
    "If the issue persists, please report this to **Vixel's Dev Team**!"
)
