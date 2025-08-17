from discord.app_commands import AppCommandError

class HypixelInvalidResponseError(AppCommandError):
    """Hypixel request timeout exception class."""


class HypixelRateLimitedError(AppCommandError):
    """Hypixel rate limit exception class."""