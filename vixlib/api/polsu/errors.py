from discord.app_commands import AppCommandError

class PolsuInvalidResponseError(AppCommandError):
    """Polsu request timeout or invalid response exception."""

class PolsuRateLimitedError(AppCommandError):
    """Polsu rate limit exception."""