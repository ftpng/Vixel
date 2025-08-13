import discord
import logging
from io import StringIO
from traceback import format_exception

from .handlers import CustomTimedRotatingFileHandler
from vixlib import LOGS_DIR, ERROR_CHANNEL


def setup_logging(logs_dir: str = LOGS_DIR):
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(CustomTimedRotatingFileHandler(logs_dir=logs_dir))


logger = logging.getLogger(__name__)


def log_critical(error: Exception) -> None:
    logger.critical(error)


def log_error(error: Exception) -> None:
    logger.error(error)


def log_warning(warning: Exception) -> None:
    logger.warning(warning)


def log_info(info: str) -> None:
    logger.info(info)


async def log_error_msg(
    bot: discord.Client, 
    error: Exception, 
    metadata: dict = None
) -> None:
    traceback_str = ''.join(format_exception(type(error), error, error.__traceback__))
    logger.error(traceback_str)

    if bot is None:
        return

    await bot.wait_until_ready()
    error_channel = await bot.fetch_channel(ERROR_CHANNEL)

    tb_file = discord.File(fp=StringIO(traceback_str), filename="traceback.txt")

    error_message = f"Error: `{error}`\n"
    if metadata:
        error_message += "\n".join([f"{k}: `{v}`" for k, v in metadata.items()])
    error_message += "\nTraceback:"

    try:
        await error_channel.send(content=error_message, file=tb_file)
    except discord.Forbidden as warning:
        log_warning(warning)


async def handle_slash_errors(
    interaction: discord.Interaction, 
    error: Exception
) -> None:

    message = (
        "An error has occurred while running your command, please try again!\n"
        "If the issue persists, please report this to **Vixel's Dev Team**!"
    )
    try:
        await interaction.edit_original_response(content=message)
    except discord.errors.NotFound:
        pass

    await log_error_msg(
        interaction.client,
        error,
        metadata={
            "Invoked By": f"{interaction.user} ({interaction.user.id})",
            "Latency": f"{int(interaction.client.latency * 1000)}ms",
            "Server": f"{interaction.guild.name if interaction.guild else 'DM'} "
                      f"({interaction.guild.id if interaction.guild else 'DM'})"
        }
    )