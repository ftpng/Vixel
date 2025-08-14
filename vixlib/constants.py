import os
from typing import Text
from dotenv import load_dotenv
from requests_cache import CachedSession

load_dotenv()


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

CACHE = CachedSession(
    cache_name=f"{DIR}vixlib/cache/mojang_cache", 
    expire_after=60
)

ERROR_CHANNEL = int(os.getenv("ERROR_CHANNEL"))

OVERALL_STARS_CHANNEL    = int(os.getenv("OVERALL_STARS_CHANNEL"))
OVERALL_STATS_CHANNEL    = int(os.getenv("OVERALL_STATS_CHANNEL"))
OVERALL_WLR_CHANNEL      = int(os.getenv("OVERALL_WLR_CHANNEL"))
OVERALL_FKDR_CHANNEL     = int(os.getenv("OVERALL_FKDR_CHANNEL"))
OVERALL_KDR_CHANNEL      = int(os.getenv("OVERALL_KDR_CHANNEL"))
OVERALL_BBLR_CHANNEL     = int(os.getenv("OVERALL_BBLR_CHANNEL"))
OVERALL_WINSTREAK_CHANNEL = int(os.getenv("OVERALL_WINSTREAK_CHANNEL"))

SOLOS_STATS_CHANNEL      = int(os.getenv("SOLOS_STATS_CHANNEL"))
SOLOS_WLR_CHANNEL        = int(os.getenv("SOLOS_WLR_CHANNEL"))
SOLOS_FKDR_CHANNEL       = int(os.getenv("SOLOS_FKDR_CHANNEL"))
SOLOS_KDR_CHANNEL        = int(os.getenv("SOLOS_KDR_CHANNEL"))
SOLOS_BBLR_CHANNEL       = int(os.getenv("SOLOS_BBLR_CHANNEL"))
SOLOS_WINSTREAK_CHANNEL  = int(os.getenv("SOLOS_WINSTREAK_CHANNEL"))

DOUBLES_STATS_CHANNEL    = int(os.getenv("DOUBLES_STATS_CHANNEL"))
DOUBLES_WLR_CHANNEL      = int(os.getenv("DOUBLES_WLR_CHANNEL"))
DOUBLES_FKDR_CHANNEL     = int(os.getenv("DOUBLES_FKDR_CHANNEL"))
DOUBLES_KDR_CHANNEL      = int(os.getenv("DOUBLES_KDR_CHANNEL"))
DOUBLES_BBLR_CHANNEL     = int(os.getenv("DOUBLES_BBLR_CHANNEL"))
DOUBLES_WINSTREAK_CHANNEL = int(os.getenv("DOUBLES_WINSTREAK_CHANNEL"))

THREES_STATS_CHANNEL     = int(os.getenv("THREES_STATS_CHANNEL"))
THREES_WLR_CHANNEL       = int(os.getenv("THREES_WLR_CHANNEL"))
THREES_FKDR_CHANNEL      = int(os.getenv("THREES_FKDR_CHANNEL"))
THREES_KDR_CHANNEL       = int(os.getenv("THREES_KDR_CHANNEL"))
THREES_BBLR_CHANNEL      = int(os.getenv("THREES_BBLR_CHANNEL"))
THREES_WINSTREAK_CHANNEL = int(os.getenv("THREES_WINSTREAK_CHANNEL"))

FOURS_STATS_CHANNEL      = int(os.getenv("FOURS_STATS_CHANNEL"))
FOURS_WLR_CHANNEL        = int(os.getenv("FOURS_WLR_CHANNEL"))
FOURS_FKDR_CHANNEL       = int(os.getenv("FOURS_FKDR_CHANNEL"))
FOURS_KDR_CHANNEL        = int(os.getenv("FOURS_KDR_CHANNEL"))
FOURS_BBLR_CHANNEL       = int(os.getenv("FOURS_BBLR_CHANNEL"))
FOURS_WINSTREAK_CHANNEL  = int(os.getenv("FOURS_WINSTREAK_CHANNEL"))

FOUR_VS_FOUR_STATS_CHANNEL    = int(os.getenv("FOUR_VS_FOUR_STATS_CHANNEL"))
FOUR_VS_FOUR_WLR_CHANNEL      = int(os.getenv("FOUR_VS_FOUR_WLR_CHANNEL"))
FOUR_VS_FOUR_FKDR_CHANNEL     = int(os.getenv("FOUR_VS_FOUR_FKDR_CHANNEL"))
FOUR_VS_FOUR_KDR_CHANNEL      = int(os.getenv("FOUR_VS_FOUR_KDR_CHANNEL"))
FOUR_VS_FOUR_BBLR_CHANNEL     = int(os.getenv("FOUR_VS_FOUR_BBLR_CHANNEL"))
FOUR_VS_FOUR_WINSTREAK_CHANNEL = int(os.getenv("FOUR_VS_FOUR_WINSTREAK_CHANNEL"))

