from discord import Embed, User
from discord.ext.commands import Bot

from utils.logs import get_logger

logger = get_logger(__name__)


def load_extensions(bot: Bot, *extensions: str):
    for extension in extensions:
        bot.load_extension("extensions." + extension)
        logger.info(f"Loaded {extension}")
    logger.info("Available cogs:")
    for cog in bot.cogs:
        logger.info(f"* {cog}")


def unload_extensions(bot: Bot, *extensions: str):
    for extension in extensions:
        bot.unload_extension("extensions." + extension)
        logger.info(f"Unloaded {extension}")


async def reload_extensions(bot: Bot, author: User, *extensions: str):
    reloaded_extensions = []
    for extension in extensions:
        bot.reload_extension("extensions." + extension)
        reloaded_extensions.append(extension)
    logger.info(f"Reload extension(s) invoked by {author}")
    embed = Embed(title="Reloaded",
                  description="\n".join(":small_blue_diamond: " + name for name in reloaded_extensions), color=0x1b6e00)
    return embed
