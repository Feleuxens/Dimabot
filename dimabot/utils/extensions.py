from discord import Embed, User
from discord.ext.commands import Bot

from utils import colors
from utils.logs import get_logger

logger = get_logger(__name__)


def load_extensions(bot: Bot, *extensions: str) -> None:
    """
    Loads extensions and adds them to given bot
    :param bot: Bot to add extensions to
    :param extensions: Tuple of strings of paths with full subpath (extensions.subfolder.file)
    :return: None
    """
    for extension in extensions:
        bot.load_extension(extension)
        logger.info(f"Loaded {extension}")
    logger.info("Available cogs:")
    for cog in bot.cogs:
        logger.info(f"* {cog}")


def unload_extensions(bot: Bot, *extensions: str) -> None:
    """
    Unloads extensions from bot
    :param bot: Bot to remove extensions from
    :param extensions: Tuple of strings of paths with full subpath (extensions.subfolder.file)
    :return: None
    """
    for extension in extensions:
        bot.unload_extension(extension)
        logger.info(f"Unloaded {extension}")


async def reload_extensions(bot: Bot, author: User, *extensions: str) -> Embed:
    """
    Reloads given extensions
    :param bot: Bot to reload extensions from
    :param author: User who invoked reloading
    :param extensions: Extensions to reload with full subpath (extensions.subfolder.file)
    :return: None
    """
    reloaded_extensions = []
    for extension in extensions:
        bot.reload_extension(extension)
        reloaded_extensions.append(extension)
    logger.info(f"Reload extension(s) invoked by {author}")
    embed = Embed(title="Reloaded",
                  description="\n".join(":small_blue_diamond: " + name for name in reloaded_extensions),
                  color=colors.GREEN)
    return embed
